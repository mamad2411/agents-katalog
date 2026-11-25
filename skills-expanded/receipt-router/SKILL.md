---
name: receipt-router
description: Files a till receipt under the month it was issued in. Use when receipts have piled up in one folder, or when the user asks for a monthly total of what they spent. Do not use for payroll statements or for bank exports.
---

# Receipt router

1. Read the date off each receipt and set aside anything that carries no date.
2. Move the file under `receipts/<year>-<month>/`, creating the month folder when
   it does not exist yet.
3. Write the month total beside the files you moved, then print it.
4. Stop and say so when two receipts carry the same date and the same amount.
