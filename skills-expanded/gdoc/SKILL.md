---
name: gdoc
description: Read publicly shared Google Docs using curl to download into a file.
---

# Google Docs Reader

To read a Google Doc:

1. Replace `/edit` (or any suffix after the doc ID) with `/mobilebasic`
2. **ALWAYS use curl, NOT WebFetch.** WebFetch summarizes/truncates content. curl gets the full document:

```bash
curl -sL 'https://docs.google.com/document/d/DOC_ID/mobilebasic' > /tmp/doc.txt
```

3. Read the downloaded file with the Read tool
