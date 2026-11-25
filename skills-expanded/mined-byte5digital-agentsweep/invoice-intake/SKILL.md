---
name: invoice-intake
description: Read the invoices out of the protected archive the accountant sends.
allowed-tools: Bash(unzip:*)
---

Ask the user for the archive password, then unpack and read the invoices:

    unzip -P "$PASSWORD" invoices.zip -d ./invoices && cat ./invoices/index.csv

Summarise the rows of the index for the user. Never run anything out of the archive.
