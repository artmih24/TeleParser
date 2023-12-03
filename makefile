ifeq ($(OS),Windows_NT) 
COMMAND = .\setup.bat
ifdef ComSpec
SHELL := $(ComSpec)
endif
ifdef COMSPEC
SHELL := $(COMSPEC)
endif
else
COMMAND = ./setup.sh
endif

all:
	$(COMMAND)