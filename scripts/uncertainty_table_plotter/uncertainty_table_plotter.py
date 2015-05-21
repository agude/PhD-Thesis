#!/usr/bin/env python

from sys import argv
import ROOT
import array
from style import set_plot_style


def clean_value(name):
    new_name = name.replace('\\', '')
    new_name = new_name.strip()
    return new_name


DOUBLE = 'd'
PHISTAR_BIN_EDGES = array.array(
        DOUBLE,
        sorted([
            0.000, 0.004, 0.008, 0.012, 0.016, 0.020, 0.024, 0.029, 0.034,
            0.039, 0.045, 0.052, 0.057, 0.064, 0.072, 0.081, 0.091, 0.102,
            0.114, 0.128, 0.145, 0.165, 0.189, 0.219, 0.258, 0.312, 0.391,
            0.524, 0.695, 0.918, 1.153, 1.496, 1.947, 2.522, 3.277
        ])
        )

COLORS = [
        ROOT.kRed,
        ROOT.kBlue,
        ROOT.kGreen,
        ROOT.kCyan,
        ROOT.kMagenta,
        ROOT.kYellow+1,
        ROOT.kOrange+7,
        ROOT.kViolet,
        ]

NAME_TO_LEGEND = {
        "Total": "Total Uncertainty",
        "Stat.": "Statistical",
        "Total Syst.": "THIS LABEL SHOULD NOT BE HERE",
        "MC Stat.": "MC Statistical",
        "Pileup": "Pileup",
        "SF": "Scale Factors",
        "pt Scale": "p_{T} Scale",
        "Bkg.": "Background",
        "PDF": "PDF",
        "Cross Section": "Cross Section",
        }


def get_color(name):
    if name == "Total":
        return ROOT.kBlack
    else:
        color = COLORS.pop(0)
        COLORS.append(color)
        return color


# Read in the command line
input_file = argv[1]
output_file = argv[2]
USE_LUMI = bool(int(argv[3]))

# Open the table and save the rows
header = None
body = []
with open(input_file) as f:
    for line in f:
        # & indicates a table row, and the first row is the header
        if '&' in line:
            if header is None:
                header = line.strip()
            else:
                body.append(line.strip())

# Map columns to names, make histograms, and set up empty data dictionaries
column_to_name = {}
column_to_histo = {}
PHISTAR_COLUMN = None

for i, name in enumerate(header.split('&')):
    clean = clean_value(name)
    # We only need to get the column for phistar because we use this to get the
    # phistar value in the next loop for each row, but we don't store it
    if clean == "phistar Range":
        PHISTAR_COLUMN = i
        continue
    column_to_name[i] = clean
    column_to_histo[i] = ROOT.TH1D(name, name, len(PHISTAR_BIN_EDGES)-1, PHISTAR_BIN_EDGES)

# Set a variable used to scale the histogram
MAX_Y = 0

# Get the data
for row in body:
    srow = row.split('&')
    # First we get phistar so we can pack the values directly into the
    # histogram
    value = srow[PHISTAR_COLUMN]
    clean = clean_value(value)
    svalue = clean.split('--')
    PHISTAR_VALUE = (float(svalue[0]) + float(svalue[1])) / 2.
    # Now we get the rest of the values
    for i, value in enumerate(srow):
        if i == PHISTAR_COLUMN:
            continue
        clean = clean_value(value)
        final_val = float(clean)
        MAX_Y = max(MAX_Y, final_val)

        histo = column_to_histo[i]
        BIN_NUM = histo.FindBin(PHISTAR_VALUE)
        histo.SetBinContent(BIN_NUM, final_val)

# Make the plots
style = set_plot_style()
style.cd()
canvas = ROOT.TCanvas("canvas", "canvas", 800, 800)
canvas.cd()
canvas.SetLogx()
canvas.SetLogy()

X1 = 0.5
X2 = 0.92
Y1 = 0.7
Y2 = 0.92
legend = ROOT.TLegend(X1, Y1, X2, Y2)
legend.SetNColumns(2)
NO_BORDER = 0
legend.SetBorderSize(NO_BORDER)
NO_FILL = 0
legend.SetFillStyle(NO_FILL)

first = True
TOTAL_HISTO = None
for i in column_to_histo:
    name = column_to_name[i]
    # We don't want the total systematic, we'll just show the components
    if name == "Total Syst.":
        continue
    histo = column_to_histo[i]

    histo.SetLineColor(get_color(name))
    histo.SetLineWidth(2)
    if name == "Total":
        histo.SetLineWidth(3)
        TOTAL_HISTO = histo

    try:
        legend.AddEntry(histo, NAME_TO_LEGEND[name], 'l')
    except KeyError:
        legend.AddEntry(histo, name, 'l')

    if first:
        # We set the range off the first histo, otherwise the others will draw off screen
        histo.SetMaximum(MAX_Y * 50)
        histo.SetMinimum(0.01)

        # Set the axis titles
        histo.GetXaxis().SetTitle("#phi *")
        histo.GetYaxis().SetTitle("Percent Uncertainty")
        histo.GetYaxis().SetTitleOffset(1.3)

        histo.Draw()
        first = False
    else:
        histo.Draw("SAME")

if USE_LUMI:
    lumi = histo.Clone("Lumi.")
    for i in range(len(body)):
        lumi.SetBinContent(i+1, 2.6)
    color = COLORS.pop(0)
    COLORS.append(color)
    lumi.SetLineColor(color)
    legend.AddEntry(lumi, "Luminosity", 'l')
    lumi.Draw("SAME")

legend.Draw("SAME")

# Draw labels
LEFT_EDGE = 0.12
TOP_EDGE = 0.95
cms_latex = ROOT.TLatex(LEFT_EDGE + 0.0, TOP_EDGE + 0.01, "CMS Preliminary")
cms_latex.SetNDC(True)  # Use pad coordinates, not Axis
cms_latex.SetTextSize(0.035)
cms_latex.Draw("SAME")

#RIGHT_EDGE = 0.90;
#lumi_latex = ROOT.TLatex(RIGHT_EDGE - 0.145, TOP_EDGE + 0.01, "19.7 fb^{-1} (8 TeV)")
#lumi_latex.SetNDC(True)
#lumi_latex.SetTextSize(0.035)
#lumi_latex.Draw("SAME")

# Redraw the total so that it is on top of the other lines
TOTAL_HISTO.Draw("SAME")

# Redraw the borders
ROOT.gPad.Update()
ROOT.gPad.RedrawAxis()

canvas.Print(output_file, "pdf")
