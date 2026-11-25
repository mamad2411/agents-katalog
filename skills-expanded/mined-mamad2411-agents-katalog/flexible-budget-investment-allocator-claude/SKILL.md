# Flexible Budget & Investment Allocator

## Project Overview

A command-line personal finance tool that helps users:

* Track monthly income
* Track essential expenses
* Track variable lifestyle expenses
* Calculate emergency fund contributions
* Allocate remaining funds into investments

The application is intended to be:

* Simple
* Beginner-friendly
* Practical for real-world monthly budgeting

---

## Tech Stack

* Python 3.11+
* Standard Library Only
* No external dependencies

---

## Architecture

Main modules/functions:

* `get_float_input()` — Safely prompts the user for numeric input with validation
* `collect_lifestyle_expenses()` — Interactively collects variable lifestyle expenses
* `calculate_emergency_fund_target()` — Computes emergency fund target (typically 3–6 months of expenses)
* `allocate_budget()` — Distributes remaining income after essentials and lifestyle costs
* `allocate_investments()` — Splits investable surplus across asset classes
* `print_report()` — Displays a formatted budget summary to the terminal
* `export_report()` — Writes the report to both `.txt` and `.csv` files
* `main()` — Entry point orchestrating the full workflow

Guidelines:

* Keep business logic separate from user interaction
* Prefer pure functions where possible
* Use type hints
* Use descriptive variable names
* Follow PEP8

---

## Future Improvements

Potential enhancements:

* JSON persistence
* Historical monthly tracking
* Portfolio performance tracking
* Inflation-adjusted emergency fund targets
* ETF customization
* GUI version using Tkinter
* Web dashboard version using Flask

---

## Expected Project Structure

```
project/
├── budget_allocator.py
├── CLAUDE.md
├── reports/
│   ├── report.txt
│   └── report.csv
```

---

## Coding Standards

* No external packages
* Clear function docstrings
* Input validation required
* Graceful error handling
* Maintain readability over cleverness
