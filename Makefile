install:
	pip install --upgrade pip &&\
			pip install -r alt_req.txt &&\
			pip install -r requirements.txt
				

format:	
	black *.py sourcel/*py 

lint:
	# pylint --disable=R,C --ignore-patterns=test_.*?py *.py dblib
	# pylint --disable=R,C *.py mylib/*.py

all: install format