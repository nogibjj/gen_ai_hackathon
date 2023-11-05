env:
	python3 -m venv .env &&\
			source .env/bin/activate &&\
			pip install --upgrade pip &&\
			pip install -r alt_req.txt &&\
			pip install -r requirements.txt

install:
	pip install --upgrade pip &&\
			pip install -r alt_req.txt &&\
			pip install -r requirements.txt
				

format:	
	black *.py source/*py 

lint:
	pylint --disable=R,C *.py source/*.py pages/*.py

all: install format lint
