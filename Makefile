environment: 
	python -m venv sketch &&\
		source sketch/bin/activate


install:
	pip install --upgrade pip &&\
			pip install -r requirements.txt
				

format:	
	# black *.py mylib/*py 

lint:
	# pylint --disable=R,C --ignore-patterns=test_.*?py *.py dblib
	# pylint --disable=R,C *.py mylib/*.py

all: environment install