# Funko — curation hints

## What belongs here

Funko's character figure lines, organized one nested collection per product
line. Curated so far:

- [`pop/`](pop/CLAUDE.md) — Pop! vinyl figures, Funko's flagship line.

Other Funko lines (Soda, Mystery Minis, Vinyl Gold, Bitty Pop!, and more)
would each be their own sibling directory here (`funko/soda/`, ...) when
curated — a Pop! figure and a Soda figure are different products, not
variants of one line.

## Directory structure

```
funko/
  CLAUDE.md
  _collection.yaml               # Funko itself
  <line>/                         # e.g. "pop"
    CLAUDE.md
    item-attributes.schema.json
    _collection.yaml
    ...
```
