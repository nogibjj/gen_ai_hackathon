install:
	pip install --upgrade pip &&\
    python -m venv sketch pip &&\
		source sketch\bin\activate &&\
			pip install -r requirements.txt
				

format:	
	# black *.py mylib/*py 

lint:
	# pylint --disable=R,C --ignore-patterns=test_.*?py *.py dblib
	# pylint --disable=R,C *.py mylib/*.py

all: install