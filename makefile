LATEXMK=latexmk

MAIN=thesis
MAIN_PDF=$(MAIN).pdf
MAIN_TEX=$(MAIN).tex
HELPER_FILES=makefile thesis.bib my_definitions.tex mnthesis.cls variables.tex
CHAPTERS:=$(wildcard ./chapters/*.tex)
FIGURES := $(wildcard figures/*.pdf)
PACKAGED_FIGURES := $(wildcard packaged_figures/*.tex)
TABLES := $(wildcard tables/*.tex)
QCD_FIGURES := $(wildcard figures/qcd_fits/*.pdf)

all: $(MAIN_PDF)

# Update the time stamp on the dummy file to force recompilation
$(MAIN_PDF): force $(MAIN_TEX) $(HELPER_FILES) $(CHAPTERS) $(FIGURES) $(PACKAGED_FIGURES) $(QCD_FIGURES) $(TABLES)
	$(LATEXMK) -pdf $(MAIN_TEX)

.PHONY: clean force all tidy

# Clean up all the regeneratable files except for the final document (the .pdf)
tidy:
	$(LATEXMK) -c $(MAIN_TEX)

# Clean up all the regeneratable files, including the final document
clean:
	$(LATEXMK) -C $(MAIN_TEX)
