#!/bin/bash

SHOW_LUMI=1
NO_SHOW_LUMI=0

# MADGRAPH Unfolded Data
./uncertainty_table_plotter.py ../../tables/data_uncertainty_absolute.tex data_uncertainty_absolute.pdf $SHOW_LUMI
./uncertainty_table_plotter.py ../../tables/data_uncertainty_normalized.tex data_uncertainty_normalized.pdf $NO_SHOW_LUMI

# MC
./uncertainty_table_plotter.py ../../tables/madgraph_uncertainty_absolute.tex madgraph_uncertainty_absolute.pdf $NO_SHOW_LUMI
./uncertainty_table_plotter.py ../../tables/madgraph_uncertainty_normalized.tex madgraph_uncertainty_normalized.pdf $NO_SHOW_LUMI
./uncertainty_table_plotter.py ../../tables/powheg_uncertainty_absolute.tex powheg_uncertainty_absolute.pdf $NO_SHOW_LUMI
./uncertainty_table_plotter.py ../../tables/powheg_uncertainty_normalized.tex powheg_uncertainty_normalized.pdf $NO_SHOW_LUMI

# POWHEG Unfolded Data
./uncertainty_table_plotter.py ../../tables/data_uncertainty_absolute_powheg_unfolded.tex data_uncertainty_absolute_powheg_unfolded.pdf $SHOW_LUMI
./uncertainty_table_plotter.py ../../tables/data_uncertainty_normalized_powheg_unfolded.tex data_uncertainty_normalized_powheg_unfolded.pdf $NO_SHOW_LUMI
    
