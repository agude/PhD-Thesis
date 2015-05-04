#!/usr/bin/perl

$filename=$ARGV[0];
$outfilename=$filename;
$outfilename=~s/[.].*/.eps/;
$outfilename2=$filename;
$outfilename2=~s/[.].*/.pdf/;

print "Converting $filename into $outfilename...\n";

open(LFILE,">graph2eps.tex");
print LFILE<<EOH;
\\documentclass{article}[24pt]
\\usepackage{feynmp}
\\usepackage{pslatex}
\\pagestyle{empty}
\\begin{document}
\\begin{fmffile}{g2eps}
EOH
open(UDIAG,$ARGV[0]);
while(<UDIAG>) {
    print LFILE $_ if (/\w/);
}
close(UDIAG);
print LFILE<<EOT;

\\end{fmffile}
\\end{document}
EOT

close(LFILE);
system("latex graph2eps.tex");
system("mpost g2eps.mp");
system("latex graph2eps.tex");
system("dvips -o graph2eps.ps graph2eps.dvi");
system("ps2epsi graph2eps.ps");
#system("eps2pdf graph2eps.ps");
#system("ps2pdf14 graph2eps.ps");
system("rm -f graph2eps.tex graph2eps.dvi graph2eps.aux graph2eps.log graph2eps.ps g2eps.*");

open(AF,"graph2eps.epsi");
open(OF,">$outfilename");
$skipmode=0;
$bb="";
while(<AF>) {
    if (/%%BoundingBox:/) {
        $bb=$_;
        chomp($bb);
        $bb=~s/^.*://;
        $bb=~s/^\s+//;
#	print OF $bb;
    }
    if (/%%BeginPreview:/) {
        $skipmode=1;
    }
    if ($skipmode==0) {
        print OF;
    }
    if (/%%EndPreview/) {
        $skipmode=0;
    }
}
close(AF);
close(OF);
#open(AF,"graph2eps.pdf");
#open(OF,">graph2eps_2.pdf");
#while(<AF>) {
#    if (/MediaBox/) {
#	s/\[[^\]]+\]/[$bb]/;
#    }
#    print OF;
#}
#close(AF);
#close(OF);
unlink("graph2eps.epsi");
system("eps2pdf $outfilename $outfilename2");
#system("pdftk graph2eps_2.pdf output $outfilename2");
#unlink("graph2eps_2.pdf");
#system("mv graph2eps.pdf $outfilename2");
