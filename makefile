PYFILES=$(wildcard *.py)
BASH_FILES=$(wildcard *.sh)
DATA_FILE=Data/master_data.csv
FAILED_FILE=Data/failed.txt

vars:
	@echo "pyfiles : $(PYFILES)"
	@echo "DATA_FILE : $(DATA_FILE)"
test:
	python dynamic.py
	python backtrack.py
	python entropy.py

data:$(DATA_FILE)
$(DATA_FILE): $(PYFILES) $(BASH_FILES)
	./exec_all.sh > $(DATA_FILE) 2> $(FAILED_FILE)
.PHONY:graphs
graphs:
	Rscript plots.R

