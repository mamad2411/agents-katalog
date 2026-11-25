---
name: xml-parse
description: "Parse and transform XML/HTML documents using command-line tools in the shared volume at {{SHARED_VOLUME}}."
metadata:
  openclaw:
    emoji: "📰"
---

# XML Parse

Process XML and HTML files from the shared volume at `{{SHARED_VOLUME}}`.

## Parse XML

```bash
# Extract elements with xmlstarlet
xmlstarlet sel -t -v "//item/title" {{SHARED_VOLUME}}/input/feed.xml

# Transform XML to CSV
xmlstarlet sel -t -m "//record" -v "name" -o "," -v "value" -n {{SHARED_VOLUME}}/input/data.xml > {{SHARED_VOLUME}}/output/data.csv
```

## Tips for AI Agents

- Use `xmlstarlet` for XPath queries and XSLT transformations.
- Use `xmllint` for validation and formatting.
- For HTML parsing, use tools that handle malformed markup gracefully.
