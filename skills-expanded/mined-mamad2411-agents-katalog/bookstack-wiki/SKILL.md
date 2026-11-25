---
name: bookstack-wiki
description: Self-hosted wiki and documentation with BookStack
version: 1.0.0
tags: [wiki, documentation, knowledge-base, self-hosted]
---

# BookStack – Self-Hosted Wiki

BookStack organises knowledge into shelves, books, chapters, and pages
for intuitive team documentation.

- **GitHub**: github.com/BookStackApp/BookStack (16 000+ ⭐)
- **License**: MIT
- **Security**: LDAP/SAML/OIDC auth support. No malware.

## Environment Variables

| Variable | Description |
|---|---|
| `{{BOOKSTACK_URL}}` | Base URL of BookStack |
| `{{BOOKSTACK_TOKEN_ID}}` | API token ID |
| `{{BOOKSTACK_TOKEN_SECRET}}` | API token secret |

## Usage Examples

### List books

```bash
curl -s "{{BOOKSTACK_URL}}/api/books" \
  -H "Authorization: Token {{BOOKSTACK_TOKEN_ID}}:{{BOOKSTACK_TOKEN_SECRET}}"
```

### Create a page

```bash
curl -s -X POST "{{BOOKSTACK_URL}}/api/pages" \
  -H "Authorization: Token {{BOOKSTACK_TOKEN_ID}}:{{BOOKSTACK_TOKEN_SECRET}}" \
  -H "Content-Type: application/json" \
  -d '{"book_id": 1, "name": "New Page", "html": "<p>Content</p>"}'
```

## AI Agent Tips

- Hierarchical structure: Shelves → Books → Chapters → Pages.
- Full REST API for CRUD on all content types.
- WYSIWYG and Markdown editors built-in.
- Role-based permissions and LDAP/SAML authentication.
