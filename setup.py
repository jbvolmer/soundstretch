from setuptools import setup,find_packages

long_description = '''

# sound stretch 1.2

This uses the Paulstretch algorithm that is released under Public Domain

## usage:

from soundstretch import SoundStretch

#### use default settings

SoundStretch("input.wav","result.wav")

#### use specific stretch factor and window size settings

SoundStretch("input.wav", "result.wav", 8.0, 0.25)

## Requirements

- Numpy

- Scipy

'''

setup(\
	name='soundstretch',
	version='1.2',
	description='SoundStretch based on Paulstretch algorithm',
    long_description=long_description,
    long_description_content_type="text/markdown",
	url='https://github.com/jbvolmer/soundstretch',
	author='J. Volmer',
	author_email='josephbvolmer@gmail.com',
	license='Public Domain',
	packages=find_packages(),
	install_requires=[
		"numpy",
		"scipy",
	],
	zip_safe=False)

