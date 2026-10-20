<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-guardianrg
description: CTF writeups and security challenges by GuardianRG.
---

# Writeups by GuardianRG

Source repository: `/repos/GuardianRG`

## Repository Index

- pentest-report/README.md

## Writeup Content


### File: pentest-report/README.md

# pentest-report
Pentest Report Sample Template, intended for course use, not production


## Prerequisites

Install Latexmk

```
apt-get install latexmk texlive-latex-extra texlive-fonts-extra texlive-lang-european

```

Copy the sample file:
```
cp pentest-report-sample.tex pentest-report.tex
```

You can then process the LaTeX report using:
```
pdflatex pentest-report
```

and show using evince pentest-report.pdf. Then start adding your own stuff.

To use fancy fonts and stuff copy the latexmkrc file:

```
cp latexmkrc-sample $HOME/.latexmkrc
```
Then look into the provided style file about fontspec.

NOTE: if you want to use minted - must allow shell stuff as shown in the latexmkrc sample!


## Running and using

Processing the LaTeX file is done using this:
```
latexmk pentest-report
```

