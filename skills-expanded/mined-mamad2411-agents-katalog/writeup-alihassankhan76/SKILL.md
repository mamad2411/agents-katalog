<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-alihassankhan76
description: CTF writeups and security challenges by alihassankhan76.
---

# Writeups by alihassankhan76

Source repository: `/repos/alihassankhan76`

## Repository Index

- ai-bug-report-generator/README.md

## Writeup Content


### File: ai-bug-report-generator/README.md

# 🛡️ AI Bug Report Generator

An AI-powered tool that helps bug bounty hunters and security researchers generate professional, structured vulnerability reports using GPT.

---

## 🚀 Live Demo

👉 [Click here to try the app](https://ai-bug-report-generator-8hmgtkstrspserr6cgcqvw.streamlit.app/)

---

## ✨ Features

- Choose vulnerability type (IDOR, 2FA Bypass, OAuth, etc.)
- Enter asset scope, steps to reproduce, impact, and remediation
- Instantly generate structured bug bounty reports (markdown format)
- Built with GPT and fine-tuned prompts to output professional reports
- Clean and minimal Streamlit UI for quick use

---

## 🧠 How It Works

1. You input details of a bug
2. The app sends the data to OpenAI API (GPT-3.5-turbo or GPT-4)
3. A clean, ready-to-submit bug bounty report is generated

---

## 🛠 Tech Stack

- **Python**
- **Streamlit**
- **OpenAI API**
- **dotenv**

---

## 📦 Run Locally

```bash
git clone https://github.com/alihassankhan76/ai-bug-report-generator.git
cd ai-bug-report-generator
pip install -r requirements.txt

