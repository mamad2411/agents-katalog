---
name: pagination-design
description: Design pagination for large datasets with cursor-based, offset-based, and keyset strategies. Outputs performance trade-offs and implementation patterns.
argument-hint: [dataset size, ordering requirements, client type]
allowed-tools: Read, Write, Bash
---

# Pagination Design

Design efficient pagination that scales to millions of records without performance degradation. Not just "LIMIT/OFFSET" — cursor-based, keyset, and seek methods with deep linking, filters, and sorting.

## Process

1. **Assess dataset size.** < 10k rows (offset OK), > 100k rows (cursor/keyset required).
2. **Choose strategy.** Offset (simple), cursor (opaque), keyset (transparent, fastest).
3. **Handle sorting.** Single column, multiple columns, custom ordering.
4. **Support filters.** WHERE conditions must preserve pagination.
5. **Add metadata.** Total count, page info, has_next/has_previous.
6. **Design URLs.** RESTful, shareable, bookmarkable.
7. **Optimize queries.** Indexes on sort columns, avoid COUNT(*) for large tables.

## Output Format

### Pagination Strategy: [API/Dataset Name]

**Dataset Size:** 5 million records  
**Strategy:** Cursor-based (Keyset)  
**Page Size:** 50 records  
**Sort:** created_at DESC, id DESC  
**Total Count:** Omitted (performance)

---

## Strategy Comparison

| Strategy | Performance | Deep Links | Complexity | Best For |
|----------|-------------|------------|------------|----------|
| Offset | O(n) | ✅ Yes | Low | < 10k rows |
| Cursor (Opaque) | O(log n) | ❌ No | Medium | Unknown sort order |
| Keyset (Seek) | O(log n) | ✅ Yes | High | > 100k rows, known sort |

---

## Offset-Based (Simple, Slow at Scale)

### How It Works
```sql
SELECT * FROM orders
ORDER BY created_at DESC
LIMIT 50 OFFSET 100;  -- Page 3 (skip first 100)
```

### REST API
```
GET /api/orders?page=3&page_size=50

Response:
{
  "data": [...],
  "pagination": {
    "page": 3,
    "page_size": 50,
    "total_pages": 1000,
    "total_count": 50000
  },
  "links": {
    "first": "/api/orders?page=1&page_size=50",
    "prev": "/api/orders?page=2&page_size=50",
    "next": "/api/orders?page=4&page_size=50",
    "last": "/api/orders?page=1000&page_size=50"
  }
}
```

### Implementation (Python + SQLAlchemy)
```python
from sqlalchemy import func

def get_orders_offset(page: int, page_size: int):
    offset = (page - 1) * page_size
    
    # Get data
    orders = db.query(Order)\
        .order_by(Order.created_at.desc())\
        .limit(page_size)\
        .offset(offset)\
        .all()
    
    # Get total count
    total = db.query(func.count(Order.id)).scalar()
    
    return {
        'data': [o.to_dict() for o in orders],
        'pagination': {
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size,
            'total_count': total
        }
    }
```

**Pros:**  
- Simple to implement
- Supports deep linking (page numbers)
- Easy to jump to any page

**Cons:**  
- O(n) performance — `OFFSET 100000` scans 100k rows
- Inconsistent results if data changes between pages
- Expensive COUNT(*) queries on large tables

**When to Use:** Tables < 10,000 rows

---

## Cursor-Based (Opaque, Fast)

### How It Works
- Encode last record's position as opaque cursor
- Client passes cursor to get next page
- Server decodes cursor and fetches next records

### REST API
```
GET /api/orders?limit=50

Response:
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJjcmVhdGVkX2F0IjogIjIwMjQtMDEtMTUiLCAiaWQiOiAxMjM0NX0=",
    "has_next": true,
    "page_size": 50
  }
}

GET /api/orders?limit=50&cursor=eyJjcmVhdGVkX2F0IjogIjIwMjQtMDEtMTUiLCAiaWQiOiAxMjM0NX0=
```

### Cursor Encoding
```python
import base64
import json

def encode_cursor(last_record):
    """Encode last record position as base64 JSON"""
    cursor_data = {
        'created_at': last_record.created_at.isoformat(),
        'id': last_record.id
    }
    json_str = json.dumps(cursor_data)
    return base64.b64encode(json_str.encode()).decode()

def decode_cursor(cursor: str):
    """Decode cursor to extract position"""
    json_str = base64.b64decode(cursor).decode()
    return json.loads(json_str)
```

### Implementation
```python
def get_orders_cursor(cursor: str = None, limit: int = 50):
    query = db.query(Order).order_by(Order.created_at.desc(), Order.id.desc())
    
    if cursor:
        # Decode cursor
        position = decode_cursor(cursor)
        created_at = datetime.fromisoformat(position['created_at'])
        last_id = position['id']
        
        # Seek to position
        query = query.filter(
            (Order.created_at < created_at) |
            ((Order.created_at == created_at) & (Order.id < last_id))
        )
    
    # Fetch limit + 1 to check if more pages exist
    orders = query.limit(limit + 1).all()
    
    has_next = len(orders) > limit
    orders = orders[:limit]
    
    next_cursor = None
    if has_next and orders:
        next_cursor = encode_cursor(orders[-1])
    
    return {
        'data': [o.to_dict() for o in orders],
        'pagination': {
            'next_cursor': next_cursor,
            'has_next': has_next,
            'page_size': limit
        }
    }
```

**SQL Generated:**
```sql
-- First page
SELECT * FROM orders
ORDER BY created_at DESC, id DESC
LIMIT 51;

-- Second page (cursor points to last record of page 1)
SELECT * FROM orders
WHERE (created_at < '2024-01-15' OR (created_at = '2024-01-15' AND id < 12345))
ORDER BY created_at DESC, id DESC
LIMIT 51;
```

**Pros:**  
- O(log n) performance with indexes
- Consistent results (no skipped/duplicate records)
- No expensive COUNT(*)

**Cons:**  
- No deep linking (cursors are opaque)
- Cannot jump to arbitrary pages
- Cannot display "Page 5 of 100"

**When to Use:** Large tables (100k+ rows), mobile apps, infinite scroll

---

## Keyset Pagination (Transparent, Fastest)

### How It Works
- Use actual column values as pagination keys
- Client passes last seen values
- Transparent (URLs are shareable)

### REST API
```
GET /api/orders?limit=50

Response:
{
  "data": [...],
  "pagination": {
    "next": "/api/orders?limit=50&before_created_at=2024-01-15T10:30:00Z&before_id=12345",
    "has_next": true
  }
}
```

### Implementation
```python
from datetime import datetime

def get_orders_keyset(
    limit: int = 50,
    before_created_at: str = None,
    before_id: int = None
):
    query = db.query(Order).order_by(Order.created_at.desc(), Order.id.desc())
    
    if before_created_at and before_id:
        created_at = datetime.fromisoformat(before_created_at)
        
        query = query.filter(
            (Order.created_at < created_at) |
            ((Order.created_at == created_at) & (Order.id < before_id))
        )
    
    orders = query.limit(limit + 1).all()
    has_next = len(orders) > limit
    orders = orders[:limit]
    
    next_url = None
    if has_next and orders:
        last = orders[-1]
        next_url = f"/api/orders?limit={limit}&before_created_at={last.created_at.isoformat()}&before_id={last.id}"
    
    return {
        'data': [o.to_dict() for o in orders],
        'pagination': {
            'next': next_url,
            'has_next': has_next
        }
    }
```

**Required Index:**
```sql
CREATE INDEX idx_orders_pagination ON orders(created_at DESC, id DESC);
```

**Pros:**  
- O(log n) performance
- Transparent URLs (shareable, bookmarkable)
- Most efficient at scale

**Cons:**  
- More complex than offset
- Requires unique sort column combination
- Cannot jump to arbitrary pages

**When to Use:** Very large tables (millions of rows), need shareable URLs

---

## Bidirectional Pagination

```python
def get_orders_bidirectional(
    limit: int = 50,
    after_cursor: str = None,
    before_cursor: str = None
):
    """Support both next and previous pages"""
    
    query = db.query(Order).order_by(Order.created_at.desc(), Order.id.desc())
    
    if after_cursor:
        # Going forward
        position = decode_cursor(after_cursor)
        query = query.filter(
            (Order.created_at < position['created_at']) |
            ((Order.created_at == position['created_at']) & (Order.id < position['id']))
        )
        
    elif before_cursor:
        # Going backward
        position = decode_cursor(before_cursor)
        query = query.filter(
            (Order.created_at > position['created_at']) |
            ((Order.created_at == position['created_at']) & (Order.id > position['id']))
        ).order_by(Order.created_at.asc(), Order.id.asc())
        # Reverse results after fetching
    
    orders = query.limit(limit + 1).all()
    
    if before_cursor:
        orders = list(reversed(orders))
    
    has_next = len(orders) > limit
    has_prev = bool(after_cursor or before_cursor)
    
    orders = orders[:limit]
    
    return {
        'data': [o.to_dict() for o in orders],
        'pagination': {
            'next_cursor': encode_cursor(orders[-1]) if has_next else None,
            'prev_cursor': encode_cursor(orders[0]) if has_prev else None,
            'has_next': has_next,
            'has_prev': has_prev
        }
    }
```

---

## Filtering + Pagination

```python
def get_orders_filtered(
    limit: int = 50,
    cursor: str = None,
    status: str = None,
    min_amount: float = None
):
    query = db.query(Order).order_by(Order.created_at.desc(), Order.id.desc())
    
    # Apply filters
    if status:
        query = query.filter(Order.status == status)
    if min_amount:
        query = query.filter(Order.amount >= min_amount)
    
    # Apply cursor
    if cursor:
        position = decode_cursor(cursor)
        query = query.filter(
            (Order.created_at < position['created_at']) |
            ((Order.created_at == position['created_at']) & (Order.id < position['id']))
        )
    
    orders = query.limit(limit + 1).all()
    # ... rest of pagination logic
```

**Index Required:**
```sql
-- Composite index for filtered pagination
CREATE INDEX idx_orders_status_pagination 
ON orders(status, created_at DESC, id DESC);
```

---

## Avoiding COUNT(*) for Large Tables

```python
# Bad: Expensive on large tables
total = db.query(func.count(Order.id)).scalar()

# Good: Use approximate count
total_approx = db.execute(
    "SELECT reltuples::bigint FROM pg_class WHERE relname = 'orders'"
).scalar()

# Good: Omit total count entirely
return {
    'data': [...],
    'pagination': {
        'next_cursor': '...',
        'has_next': True
        # No total_count, total_pages
    }
}

# Good: Cache count (update hourly)
@cache(ttl=3600)
def get_approximate_order_count():
    return db.query(func.count(Order.id)).scalar()
```

---

## GraphQL Connections Spec

```graphql
type Query {
  orders(first: Int, after: String, last: Int, before: String): OrderConnection
}

type OrderConnection {
  edges: [OrderEdge]
  pageInfo: PageInfo!
  totalCount: Int  # Optional, expensive
}

type OrderEdge {
  node: Order
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

---

## Mobile App Pattern (Infinite Scroll)

```javascript
// React Query example
const { data, fetchNextPage, hasNextPage, isFetchingNextPage } = useInfiniteQuery(
  ['orders'],
  ({ pageParam }) => fetch(`/api/orders?cursor=${pageParam || ''}`).then(r => r.json()),
  {
    getNextPageParam: (lastPage) => lastPage.pagination.next_cursor
  }
);

// Render
<FlatList
  data={data?.pages.flatMap(p => p.data)}
  onEndReached={() => hasNextPage && fetchNextPage()}
  onEndReachedThreshold={0.5}
/>
```

---

## Performance Benchmarks

**Dataset:** 1 million orders

| Strategy | Page 1 | Page 100 | Page 10000 |
|----------|--------|----------|------------|
| Offset | 5ms | 50ms | 2000ms ❌ |
| Cursor | 5ms | 8ms | 12ms ✅ |
| Keyset | 3ms | 5ms | 8ms ✅ |

---

## Testing

```python
def test_cursor_pagination_consistency():
    """Ensure no records skipped or duplicated"""
    all_ids = set()
    cursor = None
    
    while True:
        response = get_orders_cursor(cursor=cursor, limit=10)
        
        # Track IDs
        page_ids = [o['id'] for o in response['data']]
        assert len(page_ids) == len(set(page_ids)), "Duplicates in page"
        assert all_ids.isdisjoint(page_ids), "Duplicate across pages"
        all_ids.update(page_ids)
        
        if not response['pagination']['has_next']:
            break
        
        cursor = response['pagination']['next_cursor']
    
    # Verify all records fetched
    expected_count = db.query(func.count(Order.id)).scalar()
    assert len(all_ids) == expected_count
```

## Rules

- Cursor-based or keyset pagination required for tables > 100k rows — offset pagination O(n) degrades severely.
- Sort columns must have index covering all pagination keys (created_at, id) for O(log n) performance.
- Always include tiebreaker column (id) in sort even if sorting by another column — prevents non-deterministic ordering.
- Fetch limit + 1 records to determine has_next without separate query.
- Avoid COUNT(*) on large tables — omit total_count or use approximate/cached values.
- Cursors must encode all sort column values to handle equality cases correctly.
- Filter columns must be part of composite index before pagination columns.
- URLs must be shareable/bookmarkable if users need deep linking — use keyset, not opaque cursors.
- Default page size 50-100 records — smaller for mobile, larger for exports.
- Pagination must be stable even if records inserted/deleted between pages — cursor/keyset prevent this.
