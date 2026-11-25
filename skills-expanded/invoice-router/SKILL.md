---
name: invoice-router
description: Files an incoming supplier invoice under the quarter it belongs to. Use when a supplier invoice arrives as a PDF, or when a quarter has to be closed and the folder is still unsorted. Do not use for a supplier invoice that arrives as a scanned photograph.
---

# Invoice router

1. Read the supplier name and the issue date off the invoice PDF.
2. Move the file under `invoices/<year>-Q<quarter>/`, creating the quarter folder
   when it does not exist yet.
3. Print the path you wrote and the quarter you chose.
4. Stop and say so when the PDF carries no readable date.
