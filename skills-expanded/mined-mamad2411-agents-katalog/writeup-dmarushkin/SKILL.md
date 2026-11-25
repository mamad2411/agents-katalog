<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-dmarushkin
description: CTF writeups and security challenges by dmarushkin.
---

# Writeups by dmarushkin

Source repository: `/repos/dmarushkin`

## Repository Index

- pentest_reports/README.md

## Writeup Content


### File: pentest_reports/README.md

# Pentest rmarkdown reports in Kali linux

## Manual install all:

1. install r studio

`sudo apt-get install r-base -y`

2. install rmarkdown package

`sudo R -e "install.packages('rmarkdown', repos='http://cran.rstudio.com/')"`

`sudo R -e "install.packages('ggplot2', repos='http://cran.rstudio.com/')"`

3. Install editR from https://github.com/swarm-lab/editR

4. install pandoc

`sudo apt-get install pandoc -y`

5. install full xelatex (with cyrillic)

` sudo apt-get install texlive-full -y`

6. Install extra fonts

```
sudo apt-get install ttf-mscorefonts-installer -y

#export LC_ALL=“en_US.UTF-8”
#export LC_CTYPE=“en_US.UTF-8”

#sudo dpkg-reconfigure locales

locale-gen --purge en_US.UTF-8
echo -e ‘LANG=“en_US.UTF-8”\nLANGUAGE=“en_US:en”\n’ > /etc/default/locale
```

To render report just use build.sh or this command:

`R -e rmarkdown::render"(‘report.rmd’,output_file=‘report.pdf’)"`

