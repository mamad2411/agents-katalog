---
name: exporter
description: Exports the ledger to CSV. Use when the user asks for a CSV of the ledger, or when an export is due at month end.
---

# Exporter

1. Run the exporter over the ledger.
2. Stop when the CSV row count matches the ledger row count.

```python
import csv
import json
import os
import sys

def rows(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    for entry in data["entries"]:
        yield entry["date"], entry["amount"], entry["memo"]

def export(src, dst):
    with open(dst, "w", encoding="utf-8", newline="") as f:
        out = csv.writer(f)
        out.writerow(["date", "amount", "memo"])
        for row in rows(src):
            out.writerow(row)
    return os.path.getsize(dst)

if __name__ == "__main__":
    print(export(sys.argv[1], sys.argv[2]))
```
