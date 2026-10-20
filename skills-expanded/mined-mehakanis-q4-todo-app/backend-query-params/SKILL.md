# Backend Query Parameters Skill

**Purpose**: Guidance for handling query parameters for filtering, sorting, search, and pagination.

## Overview

Query parameters MUST support filtering (status, priority, due_date, tags), sorting (created, title, updated, priority, due_date), search (title, description), and pagination (page, limit). All parameters are optional with sensible defaults.

## Key Patterns

### 1. Query Parameter Definition

**Pattern**: Define query parameters with validation

```python
from fastapi import Query
from typing import Optional

@router.get("/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    status: Optional[str] = Query(
        None,
        regex="^(all|pending|completed)$",
        description="Filter by completion status"
    ),
    sort: Optional[str] = Query(
        None,
        regex="^(created|title|updated|priority|due_date)$",
        description="Sort by field"
    ),
    search: Optional[str] = Query(
        None,
        max_length=200,
        description="Search in title and description"
    ),
    priority: Optional[str] = Query(
        None,
        regex="^(low|medium|high)$",
        description="Filter by priority"
    ),
    due_date: Optional[str] = Query(
        None,
        regex="^\\d{4}-\\d{2}-\\d{2}$",
        description="Filter by due date (YYYY-MM-DD)"
    ),
    tags: Optional[str] = Query(
        None,
        description="Comma-separated tags"
    ),
    page: Optional[int] = Query(
        1,
        ge=1,
        description="Page number (starts at 1)"
    ),
    limit: Optional[int] = Query(
        20,
        ge=1,
        le=100,
        description="Items per page (max 100)"
    ),
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_jwt_token)
):
    # Implementation
    pass
```

**Pattern Rules**:
- Use `Query()` for all query parameters
- Use `regex` for enum validation
- Use `ge`, `le` for numeric range validation
- Use `max_length` for string length limits
- Provide default values (page=1, limit=20)
- Add descriptions for OpenAPI documentation

### 2. Status Filtering

**Pattern**: Filter tasks by completion status

```python
from sqlmodel import select

def apply_status_filter(statement, status: Optional[str]):
    """Apply status filter to query"""
    if status == "pending":
        return statement.where(Task.completed == False)
    elif status == "completed":
        return statement.where(Task.completed == True)
    # "all" or None means no filter
    return statement
```

**Pattern Rules**:
- "all" or None = no filter (show all)
- "pending" = completed == False
- "completed" = completed == True
- Always apply after user_id filter

### 3. Priority Filtering

**Pattern**: Filter tasks by priority

```python
def apply_priority_filter(statement, priority: Optional[str]):
    """Apply priority filter to query"""
    if priority:
        return statement.where(Task.priority == priority)
    return statement
```

**Pattern Rules**:
- Filter by exact priority match
- Values: "low", "medium", "high"
- Optional parameter (no filter if None)

### 4. Due Date Filtering

**Pattern**: Filter tasks by due date

```python
from datetime import datetime

def apply_due_date_filter(statement, due_date: Optional[str]):
    """Apply due date filter to query"""
    if due_date:
        # Parse date string (YYYY-MM-DD)
        due_date_obj = datetime.fromisoformat(due_date).date()
        return statement.where(Task.due_date == due_date_obj)
    return statement
```

**Pattern Rules**:
- Parse date string to datetime object
- Use exact date match
- Format: YYYY-MM-DD
- Optional parameter

### 5. Tags Filtering

**Pattern**: Filter tasks by tags (JSON array contains)

```python
def apply_tags_filter(statement, tags: Optional[str]):
    """Apply tags filter to query"""
    if tags:
        # Parse comma-separated tags
        tag_list = [tag.strip() for tag in tags.split(",")]
        
        # PostgreSQL JSONB contains operator
        for tag in tag_list:
            statement = statement.where(Task.tags.contains([tag]))
    
    return statement
```

**Pattern Rules**:
- Parse comma-separated tags string
- Use PostgreSQL `contains()` for JSON array
- Filter by each tag (AND condition)
- Optional parameter

### 6. Search Functionality

**Pattern**: Full-text search on title and description

```python
from sqlmodel import or_

def apply_search_filter(statement, search: Optional[str]):
    """Apply search filter to query"""
    if search:
        # Case-insensitive partial match
        search_term = f"%{search}%"
        return statement.where(
            or_(
                Task.title.ilike(search_term),
                Task.description.ilike(search_term)
            )
        )
    return statement
```

**Pattern Rules**:
- Use `ilike()` for case-insensitive search
- Use `%` wildcards for partial matching
- Search in both title and description
- Use `or_()` for multiple conditions

### 7. Full-Text Search (Advanced)

**Pattern**: PostgreSQL full-text search with ranking

```python
from sqlalchemy import func, text

def apply_fulltext_search(statement, search: Optional[str]):
    """Apply PostgreSQL full-text search"""
    if search:
        # PostgreSQL full-text search
        return statement.where(
            or_(
                func.to_tsvector('english', Task.title).match(search),
                func.to_tsvector('english', Task.description).match(search)
            )
        ).order_by(
            func.ts_rank_cd(
                func.to_tsvector('english', Task.title),
                func.plainto_tsquery('english', search)
            ).desc()
        )
    return statement
```

**Pattern Rules**:
- Use `to_tsvector()` and `match()` for full-text search
- Use `ts_rank_cd()` for relevance ranking
- Order by relevance score
- More advanced than simple ilike

### 8. Sorting

**Pattern**: Sort tasks by various fields

```python
from sqlalchemy import case

def apply_sorting(statement, sort: Optional[str]):
    """Apply sorting to query"""
    if sort == "created":
        return statement.order_by(Task.created_at.desc())
    elif sort == "title":
        return statement.order_by(Task.title.asc())
    elif sort == "updated":
        return statement.order_by(Task.updated_at.desc())
    elif sort == "priority":
        # Custom priority ordering: high > medium > low
        priority_order = case(
            (Task.priority == "high", 1),
            (Task.priority == "medium", 2),
            (Task.priority == "low", 3)
        )
        return statement.order_by(priority_order)
    elif sort == "due_date":
        # Ascending, with nulls last
        return statement.order_by(Task.due_date.asc().nulls_last())
    else:
        # Default: created_at desc
        return statement.order_by(Task.created_at.desc())
```

**Pattern Rules**:
- "created" = created_at desc (newest first)
- "title" = title asc (alphabetical)
- "updated" = updated_at desc (recently updated first)
- "priority" = custom order (high > medium > low)
- "due_date" = due_date asc (earliest first, nulls last)
- Default = created_at desc

### 9. Pagination

**Pattern**: Implement pagination with page and limit

```python
from sqlmodel import select, func

def get_tasks_paginated(
    db: Session,
    user_id: str,
    page: int = 1,
    limit: int = 20,
    **filters
):
    """Get tasks with pagination"""
    # Base query with user isolation
    statement = select(Task).where(Task.user_id == user_id)
    
    # Apply filters
    statement = apply_filters(statement, **filters)
    
    # Get total count BEFORE pagination
    count_statement = select(func.count()).select_from(statement.subquery())
    total = db.exec(count_statement).one()
    
    # Apply sorting
    statement = apply_sorting(statement, filters.get("sort"))
    
    # Apply pagination
    offset = (page - 1) * limit
    statement = statement.offset(offset).limit(limit)
    
    # Execute query
    tasks = db.exec(statement).all()
    
    # Calculate total pages
    total_pages = (total + limit - 1) // limit
    
    return {
        "data": tasks,
        "meta": {
            "total": total,
            "page": page,
            "limit": limit,
            "totalPages": total_pages
        }
    }
```

**Pattern Rules**:
- Get total count before applying limit
- Calculate offset: (page - 1) * limit
- Apply limit after sorting
- Return pagination metadata
- Default: page=1, limit=20
- Max limit: 100

### 10. Complete Query Builder

**Pattern**: Combine all query parameters

```python
from sqlmodel import Session, select, or_, func
from typing import Optional, List
from datetime import datetime

def get_tasks_with_query_params(
    db: Session,
    user_id: str,
    status: Optional[str] = None,
    sort: Optional[str] = None,
    search: Optional[str] = None,
    priority: Optional[str] = None,
    due_date: Optional[str] = None,
    tags: Optional[str] = None,
    page: int = 1,
    limit: int = 20
):
    """Complete query builder with all parameters"""
    # Base query with user isolation
    statement = select(Task).where(Task.user_id == user_id)
    
    # Apply status filter
    if status == "pending":
        statement = statement.where(Task.completed == False)
    elif status == "completed":
        statement = statement.where(Task.completed == True)
    
    # Apply priority filter
    if priority:
        statement = statement.where(Task.priority == priority)
    
    # Apply due_date filter
    if due_date:
        due_date_obj = datetime.fromisoformat(due_date).date()
        statement = statement.where(Task.due_date == due_date_obj)
    
    # Apply tags filter
    if tags:
        tag_list = [tag.strip() for tag in tags.split(",")]
        for tag in tag_list:
            statement = statement.where(Task.tags.contains([tag]))
    
    # Apply search filter
    if search:
        search_term = f"%{search}%"
        statement = statement.where(
            or_(
                Task.title.ilike(search_term),
                Task.description.ilike(search_term)
            )
        )
    
    # Get total count
    count_statement = select(func.count()).select_from(statement.subquery())
    total = db.exec(count_statement).one()
    
    # Apply sorting
    if sort == "created":
        statement = statement.order_by(Task.created_at.desc())
    elif sort == "title":
        statement = statement.order_by(Task.title.asc())
    elif sort == "updated":
        statement = statement.order_by(Task.updated_at.desc())
    elif sort == "priority":
        from sqlalchemy import case
        priority_order = case(
            (Task.priority == "high", 1),
            (Task.priority == "medium", 2),
            (Task.priority == "low", 3)
        )
        statement = statement.order_by(priority_order)
    elif sort == "due_date":
        statement = statement.order_by(Task.due_date.asc().nulls_last())
    else:
        statement = statement.order_by(Task.created_at.desc())
    
    # Apply pagination
    offset = (page - 1) * limit
    statement = statement.offset(offset).limit(limit)
    
    # Execute query
    tasks = db.exec(statement).all()
    
    # Calculate metadata
    total_pages = (total + limit - 1) // limit
    
    return {
        "data": tasks,
        "meta": {
            "total": total,
            "page": page,
            "limit": limit,
            "totalPages": total_pages
        }
    }
```

**Pattern Rules**:
- Always start with user_id filter
- Apply filters in logical order
- Get total count before pagination
- Apply sorting before pagination
- Return data and metadata

## Steps for Adding Query Parameters

1. **Define Parameters in Route**
   - Use `Query()` with validation
   - Add descriptions for OpenAPI
   - Provide default values

2. **Apply Filters in Service**
   - Build query dynamically
   - Apply user_id filter first
   - Apply other filters conditionally

3. **Apply Sorting**
   - Apply after filters
   - Before pagination

4. **Apply Pagination**
   - Get total count first
   - Apply offset and limit
   - Calculate total pages

5. **Return Results**
   - Return data array
   - Return pagination metadata

## Common Patterns Summary

- ✅ All query parameters are optional
- ✅ Use Query() with validation (regex, ge, le)
- ✅ Provide default values (page=1, limit=20)
- ✅ Always filter by user_id first
- ✅ Apply filters before counting
- ✅ Apply sorting before pagination
- ✅ Get total count before limit
- ✅ Return pagination metadata
- ✅ Support multiple filters simultaneously
- ✅ Use case-insensitive search

