---
name: receipt-sorter
description: Sorts a folder of scanned receipts into month folders and writes a total per month. Use when receipts have piled up in one directory, when the user asks for a monthly total of what they spent, or when a receipt has to be filed under the month it was issued in.
version: 0.3.0
---

# Receipt sorter

1. List every file in the folder the user named. Stop if it holds no images or PDFs.
2. Read the date off each receipt and move the file into `YYYY-MM/`.
3. When two receipts carry the same date and the same amount, keep the larger file
   and move the other into `duplicates/` rather than deleting it.
4. Write `YYYY-MM/total.md` with one line per receipt and the sum at the bottom.
5. Print the folders you created, the totals you wrote, and anything you set aside
   as a duplicate.
