# Jeremy's script
DIA_TO_EPS_SCRIPT = ./graph2eps.perl
EPS_TO_PDF_SCRIPT = epstopdf

# A list of all the diagram files, all the eps files, and all the pdf files
DIARGAMS := $(wildcard *.dia)
EPSES := $(DIARGAMS:.dia=.eps)
PDFS := $(DIARGAMS:.dia=.pdf)

# By default, make the PDFs
all: $(PDFS)

# All eps files depend on the same named dia file
%.eps: %.dia
	$(DIA_TO_EPS_SCRIPT) $^

# All pdf files depend on the same named eps file
%.pdf: %.eps
	$(EPS_TO_PDF_SCRIPT) $^

# Clean up targets
clean-eps:
	rm -f *.eps

clean-pdf:
	rm -f *.pdf

clean: clean-eps clean-pdf
