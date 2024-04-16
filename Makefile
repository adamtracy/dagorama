# In case you want to run the code locally.  Note this does NOT install the graphviz 
# dependency (brew install graphviz should do it i think)
venv:
	LOCAL_DEV=1 ./install.sh

run-local: venv
	. venv/bin/activate && python main.py --run_workflows

test-local: venv
	. venv/bin/activate && pytest

clean:
	rm -rf venv
	rm -rf output/*
	rm -rf .pytest_cache
	rm -rf poetry.lock
	for d in $(shell find . -name __pycache__); do rm -rf $$d; done