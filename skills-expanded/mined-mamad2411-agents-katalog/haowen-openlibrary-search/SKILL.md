---
name: haowen-openlibrary-search
description: This skill queries the Open Library Search API using CLIs like `http` and `jq`.
---

# openlibrary-search

## 📖 Skill Overview

This skill enables agents (or developers) to query the **Open Library Search API** directly from the command line using `http` (httpie). Responses are parsed with `jq` to extract structured fields like titles, authors, publication years, and IDs. The agent always reports the **total number of records found** (`num_found`) before presenting detailed results.

✅ All searches must include `mode=ebooks` and `has_fulltext=true` to prioritize ebook records with full text.

⚠️ **Workflow Rule:**

- Agents can perform **general searches** on works or authors given a query term.
- When the user provides a **work ID** (`key`) or **author ID** (`author_key`), agents must use the corresponding detail endpoints to fetch more information.

---

## 🔑 Endpoints

- **Works Search**: `https://openlibrary.org/search.json`
- **Author Search**: `https://openlibrary.org/search/authors.json`
- **Work Details**: `https://openlibrary.org/works/<work_id>.json`
- **Author Details**: `https://openlibrary.org/authors/<author_id>.json`
- **Cover Images**: `https://covers.openlibrary.org/{type}/olid/{OLID}-{size}.jpg`

---

## 🚀 Usage Examples

### 1. General Search for Works

```bash
http GET https://openlibrary.org/search.json q=="harry potter" limit==5 mode==ebooks has_fulltext==true \
| jq '{
        total_records: .num_found,
        results: [.docs[] | {
          title: .title,
          subtitle: .subtitle,
          work_id: .key,
          year: .first_publish_year,
          has_fulltext: .has_fulltext,
          author: .author_name,
          author_id: .author_key
        }]
      }'
```

➡️ Extract the `work_id` (e.g., `OL82563W`) or `author_id` (e.g., `OL23919A`) from the results.

---

### 2. General Search for Authors

```bash
http GET https://openlibrary.org/search/authors.json q=="tolkien" mode==ebooks has_fulltext==true \
| jq '{total_records: .num_found, results: [.docs[] | {name, key}]}'
```

➡️ Extract the `author_id` (e.g., `OL26320A`) from the results.

---

### 3. Get Work Details (when User Provides Work ID)

```bash
http GET https://openlibrary.org/works/OL82563W.json \
| jq '{title, description, subjects, edition_count}'
```

---

### 4. Get Author Details (when User Provides Author ID)

```bash
http GET https://openlibrary.org/authors/OL26320A.json \
| jq '{name, bio, birth_date, death_date}'
```

---

### 5. Cover Image by OLID

```bash
http GET https://covers.openlibrary.org/b/olid/OL23919A-M.jpg --download --output cover.jpg
```

---

## 🧩 Agent Integration Guidelines

- **General Search First**: Always perform a search to obtain `work_id` or `author_id` before fetching details.
- **Report `num_found`**: Always tell the user how many records were found.
- **Work Details**: Use the Work ID endpoint only after the ID is provided or retrieved.
- **Author Details**: Use the Author ID endpoint only after the ID is provided or retrieved.
- **Parsing**: Use `jq` filters to extract relevant fields.
- **Pagination**: Handle `page` and `limit` for browsing.
- **Availability**: Always include `mode=ebooks` and `has_fulltext=true` in searches.
- **Images**: Fetch covers using OLID and the Covers API.

---

## ✅ Best Practices

- Use `http --pretty=none --print=b` for clean JSON output.
- Pipe to `jq` for structured parsing.
- Limit fields to reduce payload size.
- Handle `num_found` to inform users of total available results.
- Use Work/Author detail endpoints only after IDs are retrieved via search or provided by the user.
