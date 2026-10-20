# GitHub Copilot Instructions — Swiss Tax Advisor

## Project Overview
This repository provides an open-source AI agent skill for Swiss personal income and wealth tax calculation across all 26 cantons.

## Guidelines for Copilot
1. **Deterministic Calculations Only**: All tax rates, progression tiers, and cantonal deductions must be handled by Python scripts in `scripts/`. Do not perform arithmetic estimations in chat.
2. **Local Profile System**: All user data is preserved in `./user/profile.json` and `./user/tax_YYYY.json` managed via `scripts/user_profile.py`.
3. **Conversational App Experience**: Do not display shell commands or json strings to users. Guide the user politely with questions, then present clear CHF summary tables.
4. **Data Protection**: AHV (756.xxxx.xxxx.xx) and IBAN (CHxx **** **** **** xxxx x) must always be masked.
