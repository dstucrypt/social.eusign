all: setup

venv/bin/activate:
	if which virtualenv-2.7 >/dev/null; then virtualenv-2.7 venv; else virtualenv venv; fi

run: venv/bin/activate requirements.txt
	. venv/bin/activate; python app.py 

setup: venv/bin/activate requirements.txt
	. venv/bin/activate; pip install -Ur requirements.txt
