#!/usr/bin/env python

from sys import argv
import ROOT
import array
from style import set_plot_style


DOUBLE = 'd'
BIN_EDGES = array.array(
        DOUBLE,
        # The -2.3, and 2.2 are to give some space on the edges
        sorted([
            -2.3, -2.1, -2, -1.556, -1.442, -0.8, 0, 0.8, 1.442, 1.556, 2, 2.1, 2.2,
            ])
        )

COLORS = [
        ROOT.kRed,
        ROOT.kBlue,
        ROOT.kGreen,
        ROOT.kMagenta,
        ROOT.kYellow+1,
        ROOT.kOrange+7,
        ROOT.kViolet,
        ]

MARKERS = [
        ROOT.kFullCircle,
        ROOT.kFullTriangleUp,
        ROOT.kFullTriangleDown,
        ROOT.kFullStar,
        ]


def get_color():
    color = COLORS.pop(0)
    COLORS.append(color)
    return color


def get_marker():
    marker = MARKERS.pop(0)
    MARKERS.append(marker)
    return marker


def make_histo(name, title):
    histo = ROOT.TH1D(name, title, len(BIN_EDGES)-1, BIN_EDGES)
    histo.Sumw2()
    return histo


def extract_tuple(entry):
    # Takes a string like: $0.741^{+0.003}_{-0.003}$
    trimmed = entry[1:-2]
    strimmed = trimmed.split('{')
    value = float(strimmed[0][0:-1])
    up_err = float(strimmed[1][0:-2])
    down_err = float(strimmed[2][0:-1])
    return (value, up_err, down_err)


def line_to_tuples(line):
    sline = [i.strip() for i in line.split('&')]

    # Get the bin in eta
    # After the split we end up with:
    # [ '\numrange', '-2.1}', '-2}' ]
    zero_split = sline[0].split('{')
    left_edge = float(zero_split[1].strip('}'))
    right_edge = float(zero_split[2].strip('}'))
    bin_center = (right_edge + left_edge) / 2.

    tuples = [bin_center, []]
    for i in range(1, 5):
        tuples[1].append(extract_tuple(sline[i]))

    return tuples


def fill_histograms_from_table(file, is_data=True):
    postfix = "_mc"
    if is_data:
        postfix = "_data"

    histos = [
            make_histo("30_40"+postfix, "30--40 GeV"),
            make_histo("40_50"+postfix, "40--50 GeV"),
            make_histo("50_70"+postfix, "50--70 GeV"),
            make_histo("70_250"+postfix, "70--250 GeV"),
            ]

    with open(file) as f:
        for line in f:
            # & indicates a table row, and the first row is the header
            if 'numrange' in line:
                clean_line = line.replace('\\', '')
                (BIN_CENTER, tuples) = line_to_tuples(clean_line)
                for i in range(len(tuples)):
                    (VALUE, UP_ERR, DOWN_ERR) = tuples[i]
                    histo = histos[i]
                    BIN_NUM = histo.FindBin(BIN_CENTER)
                    ERR = max(abs(UP_ERR), abs(DOWN_ERR))
                    histo.SetBinContent(BIN_NUM, VALUE)
                    histo.SetBinError(BIN_NUM, ERR)

    return histos


# Read in the command line
data_file = argv[1]
mc_file = argv[2]
output_file = argv[3]

data_histos = fill_histograms_from_table(data_file, is_data=True)
mc_histos = fill_histograms_from_table(mc_file, is_data=False)

# Make Ratios
ratios = []
for i in range(len(data_histos)):
    data_histo = data_histos[i]
    mc_histo = mc_histos[i]

    data_histo.Divide(mc_histo)

# Set a variable used to scale the histogram
MAX_Y = 0

# Make the plots
style = set_plot_style()
style.cd()
canvas = ROOT.TCanvas("canvas", "canvas", 800, 800)
canvas.cd()

X1 = 0.45
X2 = 0.92
Y1 = 0.72
Y2 = 0.92
legend = ROOT.TLegend(X1, Y1, X2, Y2)
legend.SetNColumns(2)
NO_BORDER = 0
legend.SetBorderSize(NO_BORDER)
NO_FILL = 0
legend.SetFillStyle(NO_FILL)

first = True
for histo in data_histos:
    name = histo.GetTitle()
    color = get_color()
    histo.SetLineColor(color)
    histo.SetMarkerColor(color)
    histo.SetMarkerSize(1.5)
    histo.SetMarkerStyle(get_marker())
    histo.SetLineWidth(2)
    legend.AddEntry(histo, name, 'p')

    if first:
        # We set the range off the first histo, otherwise the others will draw off screen
        histo.SetMaximum(1.1)
        histo.SetMinimum(0.9)
        histo.SetAxisRange(-2.3, 2.3, "X")

        # Set the axis titles
        histo.GetXaxis().SetTitle("#eta")
        histo.GetYaxis().SetTitle("Data Trigger Efficiency / MC Trigger Efficiency")
        histo.GetYaxis().SetTitleOffset(1.4)

        histo.Draw("E")
        first = False
    else:
        histo.Draw("SAME E")

legend.Draw("SAME")

# Draw labels
LEFT_EDGE = 0.12
TOP_EDGE = 0.95
cms_latex = ROOT.TLatex(LEFT_EDGE + 0.0, TOP_EDGE + 0.01, "CMS Preliminary")
cms_latex.SetNDC(True)  # Use pad coordinates, not Axis
cms_latex.SetTextSize(0.035)
cms_latex.Draw("SAME")

# Draw line
line = ROOT.TLine(-2.3, 1, 2.3, 1)
line.SetLineWidth(3)
line.SetLineStyle(ROOT.kDashed)
line.Draw("SAME")

#RIGHT_EDGE = 0.90;
#lumi_latex = ROOT.TLatex(RIGHT_EDGE - 0.145, TOP_EDGE + 0.01, "19.7 fb^{-1} (8 TeV)")
#lumi_latex.SetNDC(True)
#lumi_latex.SetTextSize(0.035)
#lumi_latex.Draw("SAME")

# Redraw the borders
ROOT.gPad.Update()
ROOT.gPad.RedrawAxis()

canvas.Print(output_file, "pdf")
