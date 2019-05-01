all: clean soundstretch-test test

soundstretch-test:
	cp soundstretch-test.py soundstretch-test
	chmod u+x soundstretch-test

test:
	./soundstretch-test -i test.wav -s 8.0 -w .25 -o temp.wav

clean:
	rm -rf soundstretch-test temp.wav
