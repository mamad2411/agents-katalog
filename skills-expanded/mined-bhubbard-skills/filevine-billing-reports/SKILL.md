---
name: filevine-billing-reports
description: Skill for generating and analyzing Filevine billing and financial reports
---

# Filevine Billing Reports Skill

## Overview
This skill provides specialized knowledge for building and interpreting financial, billing, and time-tracking reports within Filevine. It focuses on ensuring accurate invoicing, tracking WIP (Work in Progress), and analyzing firm profitability.

## Key Metrics to Track
1. **Billable Hours vs. Billed Hours**: Understand the difference between recorded time and invoiced time.
2. **Realization Rate**: Calculate the percentage of recorded time that actually gets billed and collected.
3. **Aged Receivables (AR)**: Monitor unpaid invoices categorized by age (30, 60, 90+ days).
4. **Expense Tracking**: Ensure all hard and soft costs are accurately logged to projects for reimbursement.

## Report Configuration Guidelines
- **Time Entries**: Create detailed reports showing unbilled time entries grouped by timekeeper and project.
- **Invoices**: Build summary reports for generated invoices, including their current status (Draft, Sent, Paid, Void).
- **Trust Balances**: Essential reports to monitor client trust account balances, ensuring compliance with legal accounting rules.

## Data Quality Checks
- Periodically review reports for negative time entries, zero-dollar expenses that should be billable, or unassigned timekeepers.
- Validate that the billing rates applied match the agreed-upon fee schedules for the client or project type.
