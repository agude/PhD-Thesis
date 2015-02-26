LATEXMK=latexmk

MAIN=thesis
MAIN_PDF=$(MAIN).pdf
MAIN_TEX=$(MAIN).tex
HELPER_FILES=makefile thesis.bib my_definitions.tex mnthesis.cls
CHAPTERS:=$(wildcard ./chapters/*.tex)
FIGURES := $(wildcard figures/*.pdf)

all: $(MAIN_PDF)

# Update the time stamp on the dummy file to force recompilation
.refresh:
	touch .refresh

$(MAIN_PDF): $(MAIN_TEX) $(HELPER_FILES) $(CHAPTERS) .refresh
	$(LATEXMK) -pdf $(MAIN_TEX) 

force:
	touch .refresh
	$(MAKE) $(MAIN_PDF)

.PHONY: clean force all tidy

# Clean up all the regeneratable files except for the final document (the .pdf)
tidy:
	$(LATEXMK) -c $(MAIN_TEX)

# Clean up all the regeneratable files, including the final document
clean:
	$(LATEXMK) -C $(MAIN_TEX)
