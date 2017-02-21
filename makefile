all:  clean init build  

build: 
	pyi-makespec -F -n itoyparser_32 --paths=$(shell pwd)/src src/main/itoyparser.py
	pyinstaller itoyparser_32.spec
	echo "Done"

clean:
	rm -rvf dist build ITOYINPUT ITOYOUTPUT *.spec 

init:
	mkdir ITOYINPUT ITOYOUTPUT 



