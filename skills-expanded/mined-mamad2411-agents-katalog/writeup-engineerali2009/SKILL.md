<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-engineerali2009
description: CTF writeups and security challenges by engineerali2009.
---

# Writeups by engineerali2009

Source repository: `/repos/engineerali2009`

## Repository Index

- latex-pentesting-templates/README.md

## Writeup Content


### File: latex-pentesting-templates/README.md

# Introduction

These are my LaTeX report templates. These reports templates are oriented towards IT security people.

## Contents
* [Previews](#previews)
* [Requirements](#requirements)
* [Prerequisites](#prerequisites)
* [Usage](#usage)
* [Useful Utilities and Resources](#useful-utilities-and-resources)
* [References](#references)

# Previews

This previews don't work on Firefox, if you're using Firefox download the PDF files instead.

[report-pentest](report-pentest.pdf)

[report-pentest-modern](report-pentest-modern.pdf)

[report-application-security](report-application-security.pdf)


# Requirements

- LaTeX (eg. [TeX Live](http://www.tug.org/texlive/)) in order to install packages.
- Zathura (optional) - PDF Reader
- [latexmk](https://mg.readthedocs.io/latexmk.html)  - Perl Script Compiler for LaTeX

Examples for common Linux distros:

- Arch Linux: `pacman -S texlive-most latexmk`
- openSUSE: `zypper in texlive-scheme-medium latexmk`
- Ubuntu: `apt install texlive-latex-recommended texlive-fonts-extra texlive-latex-extra latexmk`
- Kali Linux or ParrotOS: `apt install -y texlive-full zathura latexmk --fix-missing`

Example for Windows:

1. [Stawberry Perl](https://strawberryperl.com/) perl compiler that works with LaTeX.
2. [MiKTeX](https://miktex.org/) in order to install packages.
3. [LaTeX Workshop Visual Studio Code Workshop Extension](https://github.com/James-Yu/LaTeX-Workshop)


**If you're in Linux then you may want to read this**

**Change The Default PDF Application**

```bash
xdg-mime query default application/pdf 
```
Output the current PDF application
```bash
xdg-mime default zathura.desktop application/pdf
```
Change the PDF application to zathura as default.

**latexmk Configuration**

```bash
cd ~/.config
```
Navigate to your configuration directory.
```bash
mkdir latexmk; cd latexmk; touch latexmkrc; cd ..
```
Create a latexmk configuration file.
```bash
chown $USER:your_group -R latexmk
```
Assign the correct ownership.

**latexmk usage**

```bash
latexmk -pdf filename.tex 
```
Compile a `.tex` file to PDF format.

**zathura usage**

```bash
zathura filename.pdf
```
Open a PDF file with `zathura`.

## Prerequisites

You need to install the LaTeX packages before you can use this templates.

```tex
titlesec
geometry
graphicx
xcolor
tcolorbox
fancyhdr
hyperref
listings
parskip
caption
smartdiagram
zed-csp
float
colortbl
tabularx
apacite
anyfontsize
lastpage
```
# Usage

1. Change the string `CompanyName` with name of your `company` and change `Client Company` with company name of your client.
2. Change Lorem Ipsum with what you will need to write.
3. Modify it however you want

# Useful Utilities and Resources

Fonts: 
- https://www.overleaf.com/learn/latex/Font_typefaces
- https://en.m.wikibooks.org/wiki/LaTeX/Fonts

Tables: https://texblog.org/2019/06/03/control-the-width-of-table-columns-tabular-in-latex/

Tables Generator: https://www.latex-tables.com/#

Visual Studio Code LaTeX Utilities: https://marketplace.visualstudio.com/items?itemName=tecosaur.latex-utilities

# References

I used this reports as references:

Pentest: https://github.com/juliocesarfort/public-pentesting-reports/blob/master/OffensiveSecurity/penetration-testing-sample-report-2013.pdf

Pentest Modern Look: https://github.com/hmaverickadams/TCM-Security-Sample-Pentest-Report

