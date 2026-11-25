---
name: get_book
version: 1.0.0
license: MIT
---

# get_book

Get full details of a single book by its numeric `id`. Returns the book object,
or `{ "found": false }` when no book has that id.

## Arguments

- `id` (number, required): book id.

## Example

```json
{ "id": 1 }
```