#!/usr/bin/env python3

'''
SoundStretch
based on Paul's Extreme Sound Stretch algorithm (Paulstretch)

'''

import sys
import os
from numpy import *
import scipy.io.wavfile
import wave
import argparse

################################################################################

class SoundStretch(object):
    def __init__(self, sample_file, outfilename, stretch=8.0, windowsize_seconds=0.25):
        (samplerate,smp) = self.load_wav(sample_file)
        self.samplerate=samplerate
        self.smp=smp
        self.stretch=stretch
        self.windowsize_seconds=windowsize_seconds
        self.outfilename=outfilename
        self.pstretch()
    def load_wav(self,  filename):
        try:
            wavedata=scipy.io.wavfile.read(filename)
            samplerate=int(wavedata[0])
            smp=wavedata[1]*(1.0/32768.0)
            smp=smp.transpose()
            if len(smp.shape)==1: smp=tile(smp,(2,1))
            return (samplerate,smp)
        except:
            print("Error loading wav: {}".format(filename))
            return None
    def optimize_windowsize(self,n):
        orig_n=n
        while True:
            n=orig_n
            while (n%2)==0: n/=2
            while (n%3)==0: n/=3
            while (n%5)==0: n/=5
            if n<2: break
            orig_n+=1
        return orig_n
    def pstretch(self):
        nchannels=self.smp.shape[0]
        outfile=wave.open(self.outfilename,"wb")
        outfile.setsampwidth(2)
        outfile.setframerate(self.samplerate)
        outfile.setnchannels(nchannels)
        windowsize=int(self.windowsize_seconds*self.samplerate)
        windowsize=16 if windowsize<16 else windowsize
        windowsize=self.optimize_windowsize(windowsize)
        windowsize=int(windowsize/2)*2
        half_windowsize=int(windowsize/2)
        nsamples=self.smp.shape[1]
        end_size=int(self.samplerate*0.05)
        end_size=16 if end_size<16 else end_size
        self.smp[:,nsamples-end_size:nsamples]*=linspace(1,0,end_size)
        start_pos=0.0
        displace_pos=(windowsize*0.5)/self.stretch
        window=pow(1.0-pow(linspace(-1.0,1.0,windowsize),2.0),1.25)
        old_windowed_buf=zeros((2,windowsize))
        done=False
        while not done:
            istart_pos=int(floor(start_pos))
            buf=self.smp[:,istart_pos:istart_pos+windowsize]
            buf=buf if buf.shape[1]>=windowsize else append(buf,zeros((2,windowsize-buf.shape[1])),1)
            buf=buf*window
            freqs=abs(fft.rfft(buf))
            ph=random.uniform(0,2*pi,(nchannels,freqs.shape[1]))*1j
            freqs=freqs*exp(ph)
            buf=fft.irfft(freqs)
            buf*=window
            output=buf[:,0:half_windowsize] + old_windowed_buf[:,half_windowsize:windowsize]
            old_windowed_buf=buf
            output[output>1.0]=1.0
            output[output<-1.0]=-1.0
            flattened=output.ravel(order='F') 
            frames=int16( flattened * 32767.0 ).tostring()
            outfile.writeframes(frames)
            start_pos+=displace_pos
            sys.stdout.write ("%d %% \r" % int(100.0*start_pos/nsamples))
            sys.stdout.flush()
            if start_pos>=nsamples: done=True
        if done: print("100 %")
        outfile.close()
        return os.path.exists(self.outfilename) and os.path.isfile(self.outfilename)


################################################################################

