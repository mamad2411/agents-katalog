---
name: django-orm-nplusone
description: >
  Fix Django ORM N+1 queries: select_related, prefetch_related, Prefetch objects, only/defer,
  annotation aggregation, and query-count assertions in tests. Use when Django N+1, duplicate
  SQL in DEBUG toolbar, slow list views, Missing select_related, or owned Django performance
  tuning of ORM access patterns.
---

# Django ORM N+1

## Scope And Authorization

- **In scope:** Django codebases and databases you own; performance tests on non-prod data copies when possible.
- **Out of scope:** Running heavy EXPLAIN on production primary without approval.
- Prefer measuring with toolbar/logs before micro-optimizing.
- Redact PII in captured SQL logs.
- Pair with `django-async-views-pitfalls`, DB indexing skills, and `code-quality-standards`.

## When To Use

- List/detail pages issue 1 + N queries per row.
- Django Debug Toolbar shows repeated similar SQL.
- Serializers (DRF) touch nested relations in loops.
- Admin changelists slow with related objects.
- Tests should freeze query counts for critical paths.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Async ORM pitfalls | `django-async-views-pitfalls` |
| Schema migration safety | `database-migration-safety` |
| Full DB engine tuning | DBA/performance skills |
| Caching strategies | `caching-strategies` |
| Code quality baseline | `code-quality-standards` |

## What is N+1?

```text
Query 1: SELECT * FROM book
For each book:
  Query: SELECT * FROM author WHERE id = book.author_id
→ 1 + N queries
```

| Tool | Use |
| --- | --- |
| `select_related` | SQL JOIN for foreign key / one-to-one |
| `prefetch_related` | Separate query + Python join for M2M / reverse FK |
| `Prefetch(...)` | Customize queryset for prefetch |
| `only` / `defer` | Limit columns |
| `annotate` / `prefetch_related_objects` | Aggregates / manual prefetch |

## Workflow

### 1. Confirm scope and success criteria

1. Slow endpoints/templates/serializers identified.
2. Success: query count reduced to stable small N; p95 latency improved; tests guard regressions.
3. Baseline with production-like data volume in staging.

### 2. Measure

```python
# Django Debug Toolbar in dev
# or:
from django.db import connection, reset_queries
from django.conf import settings
settings.DEBUG = True  # dev only
reset_queries()
# ... call view ...
print(len(connection.queries))
```

```bash
# Logging
# settings: django.db.backends logging DEBUG in dev
```

1. Capture exact repeated SQL patterns.
2. Note whether relation is FK, reverse FK, or M2M.

### 3. Apply `select_related` / `prefetch_related`

```python
# FK / O2O
Book.objects.select_related("author", "publisher")

# reverse FK / M2M
Author.objects.prefetch_related("book_set", "groups")

# nested
Book.objects.select_related("author").prefetch_related("author__awards")

# customized prefetch
from django.db.models import Prefetch
Author.objects.prefetch_related(
    Prefetch(
        "book_set",
        queryset=Book.objects.filter(published=True).only("id", "title", "author_id"),
        to_attr="published_books",
    )
)
```

1. DRF: use `select_related`/`prefetch_related` in `get_queryset()`—not only in serializer.
2. Templates: same issue for `{{ book.author.name }}` in loops.

### 4. Avoid common mistakes

| Mistake | Fix |
| --- | --- |
| `select_related` on M2M | Use `prefetch_related` |
| Prefetch then filter in Python differently | Prefetch queryset should match usage |
| `iterator()` + prefetch | Prefetch may not apply as expected—know docs |
| Caching whole QS incorrectly | Evaluate carefully |
| Fixing N+1 with huge JOIN | May need denormalize/cache |

```python
# BAD: N+1 in serializer
class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    def get_author_name(self, obj):
        return obj.author.name  # if author not selected

# GOOD: queryset selects author; field = author.name source
```

### 5. only/defer, annotations, exists

```python
Book.objects.only("id", "title", "author_id").select_related("author")
# Count without loading objects
Author.objects.annotate(n=Count("book")).filter(n__gt=0)
# Existence
Book.objects.filter(author_id=aid).exists()
```

1. Avoid `len(qs)` if `qs.count()` suffices.
2. Pagination before expensive prefetch when possible.

### 6. Guard with tests

```python
from django.test import TestCase

class BookListTests(TestCase):
    def test_list_query_budget(self):
        # create fixtures...
        with self.assertNumQueries(5):  # tune to measured budget
            resp = self.client.get("/api/books/")
            self.assertEqual(resp.status_code, 200)
```

1. Use `assertNumQueries` on critical paths.
2. Revisit budget when features add intentional joins.

### 7. Verify and hand off

1. Re-measure toolbar/logs; confirm latency.
2. EXPLAIN slow remaining queries; add indexes if filtered columns warrant (`database` skills).
3. Document queryset helpers (custom managers) for reuse.
4. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| List API | `get_queryset` with select/prefetch | Default QS + nested access |
| M2M | `prefetch_related` | `select_related` misuse |
| Tests | `assertNumQueries` | Hope |
| Measure | Staging-scale data | 2 rows in dev only |
| Templates | Related in QS | Touch relations in loop |
| Async | Batch ORM in sync path | Per-field `sync_to_async` |

## Output Checklist

- [ ] Hot paths measured with query counts
- [ ] FK paths use `select_related`
- [ ] M2M/reverse use `prefetch_related` / `Prefetch`
- [ ] DRF `get_queryset` fixed
- [ ] Templates audited for relation access
- [ ] Query budget tests added
- [ ] Latency improved on staging evidence
- [ ] Indexes considered for remaining slow SQL
- [ ] Managers/helpers documented
- [ ] `code-quality-standards` applied

## Rules

- Measure before and after; do not guess.
- Prefer correct related loading over caching broken N+1.
- Keep query budget tests on critical endpoints.
- Production DEBUG SQL logging off.
- Owned apps only; topic is Django ORM N+1.
