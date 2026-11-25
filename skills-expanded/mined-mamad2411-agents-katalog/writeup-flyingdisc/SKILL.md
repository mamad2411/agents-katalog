<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-flyingdisc
description: CTF writeups and security challenges by flyingdisc.
---

# Writeups by flyingdisc

Source repository: `/repos/flyingdisc`

## Repository Index

- practical-machine-learning/README.md

## Writeup Content


### File: practical-machine-learning/README.md

# Practical Machine Learning
Coursera's Data Science Specialization, Practical Machine Learning's project, Prediction Assignment Writeup.

## Background  ##

Using devices such as JawboneUp, NikeFuelBand, and Fitbitit is now possible to collect a large amount of data about personal activity relatively inexpensively. These type of devices are part of the quantified self movement - a group of enthusiasts who take measurements about themselves regularly to improve their health, to find patterns in their behavior, or because they are tech geeks. One thing that people regularly do is quantify how much of a particular activity they do, but they rarely quantify how well they do it.

In this project, the goal is to use data from `accelerometers` on the `belt`, `forearm`, `arm`, and `dumbell` of 6 participants. They were asked to perform barbell lifts correctly and incorrectly in 5 different ways. More information is available from the [website](http://groupware.les.inf.puc-rio.br/har) (see the section on the Weight Lifting Exercise Dataset).

## Data ##

The training data for this project are available [here](https://d396qusza40orc.cloudfront.net/predmachlearn/pml-training.csv). 
The test data are available [here](https://d396qusza40orc.cloudfront.net/predmachlearn/pml-testing.csv). 

The data for this project come from this [source](http://groupware.les.inf.puc-rio.br/har). If you use the document you create for this class for any purpose please cite them as they have been very generous in allowing their data to be used for this kind of assignment.

## Project's rubric ##

The goal of the project is to predict the manner in which they did the exercise. This is the `classe` variable in the training set. Use any of the other variables to predict with.     

Create a report describing how to build the model, how to use cross validation, what the expected out of sample error is, and why make the choices. Then use the prediction model to predict 20 different test cases.        

The submission should consist of a link to (this) Github repo with the R markdown and compiled HTML file describing the analysis. Please constrain the text of the writeup to < 2000 words and the number of figures to be
less than 5. It will make it easier for the graders to submit a repo with a gh-pages branch so the HTML page can be viewed online.    

## Machine Learning Model ##

**Tool:** [XGBoost](https://github.com/dmlc/xgboost), an implementation of tree-based extreme gradient boosting algorithm. A very fast and accurate method to do cross validation, fitting and predicting.   

## HTML report page (gh-pages) ##

Please open [this GitHub link](http://flyingdisc.github.io/practical-machine-learning/).  

The HTML file is in the `gh-pages` branch.    
The R markdown file (Rmd) is in the `master` branch.     

----------

