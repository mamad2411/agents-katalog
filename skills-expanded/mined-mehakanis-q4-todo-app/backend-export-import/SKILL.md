# Backend Export/Import Skill

**Purpose**: Guidance for implementing CSV and JSON export/import functionality for tasks.

## Overview

Export functionality MUST support CSV and JSON formats. Import functionality MUST validate data, handle errors gracefully, and report import statistics. All operations MUST enforce user isolation.

## Key Patterns

### 1. Export Endpoint

**Pattern**: Export tasks to CSV or JSON file

```python
from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlmodel import Session, select
from backend.db import get_db
from backend.middleware.jwt import verify_jwt_token

router = APIRouter(prefix="/api", tags=["tasks"])

@router.get("/{user_id}/tasks/export")
async def export_tasks(
    user_id: str,
    format: str = Query(..., regex="^(csv|json)$", description="Export format"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_jwt_token)
):
    """Export tasks to CSV or JSON format"""
    # Verify user_id
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="User ID mismatch")
    
    # Get all tasks for user
    tasks = db.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
    
    # Export based on format
    if format == "csv":
        file_content = export_to_csv(tasks)
        content_type = "text/csv"
        filename = "tasks_export.csv"
    else:  # json
        file_content = export_to_json(tasks)
        content_type = "application/json"
        filename = "tasks_export.json"
    
    return Response(
        content=file_content,
        media_type=content_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
```

**Pattern Rules**:
- Validate format parameter (csv or json)
- Verify user_id matches JWT token
- Get all tasks for user (no pagination for export)
- Return Response with appropriate content type
- Set Content-Disposition header for file download

### 2. CSV Export

**Pattern**: Export tasks to CSV format

```python
import csv
from io import StringIO
from typing import List
from backend.models import Task

def export_to_csv(tasks: List[Task]) -> bytes:
    """Export tasks to CSV format"""
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=[
        "id",
        "title",
        "description",
        "priority",
        "due_date",
        "tags",
        "completed",
        "created_at",
        "updated_at"
    ])
    
    writer.writeheader()
    
    for task in tasks:
        writer.writerow({
            "id": task.id,
            "title": task.title,
            "description": task.description or "",
            "priority": task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else "",
            "tags": ",".join(task.tags) if task.tags else "",
            "completed": str(task.completed).lower(),
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        })
    
    return output.getvalue().encode("utf-8")
```

**Pattern Rules**:
- Use csv.DictWriter for structured output
- Include all task fields in CSV
- Convert datetime to ISO format string
- Convert tags array to comma-separated string
- Convert boolean to lowercase string
- Handle None values (empty string)
- Encode to UTF-8 bytes

### 3. JSON Export

**Pattern**: Export tasks to JSON format

```python
import json
from typing import List
from backend.models import Task

def export_to_json(tasks: List[Task]) -> bytes:
    """Export tasks to JSON format"""
    tasks_data = []
    
    for task in tasks:
        task_dict = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "tags": task.tags or [],
            "completed": task.completed,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }
        tasks_data.append(task_dict)
    
    # Pretty print with indent
    json_str = json.dumps(tasks_data, indent=2, default=str)
    return json_str.encode("utf-8")
```

**Pattern Rules**:
- Convert tasks to list of dictionaries
- Use ISO format for datetime objects
- Keep tags as array (not comma-separated)
- Use `default=str` for datetime serialization
- Pretty print with indent=2
- Encode to UTF-8 bytes

### 4. Import Endpoint

**Pattern**: Import tasks from CSV or JSON file

```python
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlmodel import Session
from backend.db import get_db
from backend.middleware.jwt import verify_jwt_token

@router.post("/{user_id}/tasks/import")
async def import_tasks(
    user_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_jwt_token)
):
    """Import tasks from CSV or JSON file"""
    # Verify user_id
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="User ID mismatch")
    
    # Validate file type
    if file.content_type not in ["text/csv", "application/json"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only CSV and JSON are supported"
        )
    
    # Read file content
    content = await file.read()
    
    # Determine format from filename or content type
    format = "csv" if file.filename.endswith(".csv") or file.content_type == "text/csv" else "json"
    
    # Import tasks
    result = import_tasks_from_file(db, user_id, content, format)
    
    return {
        "success": True,
        "data": {
            "imported": result["imported"],
            "errors": result["errors"],
            "errors_list": result.get("errors_list")
        }
    }
```

**Pattern Rules**:
- Validate file content type
- Read file content as bytes
- Determine format from filename or content type
- Delegate to import function
- Return import statistics

### 5. CSV Import

**Pattern**: Import tasks from CSV file

```python
import csv
from io import StringIO
from datetime import datetime
from typing import Dict, List
from sqlmodel import Session
from backend.models import Task

def import_from_csv(
    db: Session,
    user_id: str,
    content: bytes
) -> Dict:
    """Import tasks from CSV file"""
    imported = 0
    errors = 0
    errors_list = []
    
    # Decode content
    csv_content = content.decode("utf-8")
    reader = csv.DictReader(StringIO(csv_content))
    
    for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
        try:
            # Parse and validate data
            task = Task(
                user_id=user_id,  # Always set from authenticated user
                title=row["title"],
                description=row.get("description") or None,
                priority=row.get("priority", "medium"),
                due_date=datetime.fromisoformat(row["due_date"]) if row.get("due_date") else None,
                tags=row["tags"].split(",") if row.get("tags") else [],
                completed=row.get("completed", "false").lower() == "true",
            )
            
            # Validate task data
            if len(task.title) > 200:
                raise ValueError("Title exceeds 200 characters")
            if task.description and len(task.description) > 1000:
                raise ValueError("Description exceeds 1000 characters")
            if task.priority not in ["low", "medium", "high"]:
                raise ValueError("Invalid priority value")
            
            db.add(task)
            imported += 1
        
        except Exception as e:
            errors += 1
            errors_list.append(f"Row {row_num}: {str(e)}")
    
    # Commit all successful imports
    db.commit()
    
    return {
        "imported": imported,
        "errors": errors,
        "errors_list": errors_list if errors > 0 else None
    }
```

**Pattern Rules**:
- Decode content from UTF-8
- Use csv.DictReader for structured parsing
- Track row numbers for error reporting
- Validate each row before adding
- Set user_id from authenticated user (not from file)
- Parse dates, booleans, and arrays correctly
- Commit all successful imports in one transaction
- Report errors with row numbers

### 6. JSON Import

**Pattern**: Import tasks from JSON file

```python
import json
from typing import Dict, List
from datetime import datetime
from sqlmodel import Session
from backend.models import Task

def import_from_json(
    db: Session,
    user_id: str,
    content: bytes
) -> Dict:
    """Import tasks from JSON file"""
    imported = 0
    errors = 0
    errors_list = []
    
    # Parse JSON
    try:
        tasks_data = json.loads(content.decode("utf-8"))
    except json.JSONDecodeError as e:
        return {
            "imported": 0,
            "errors": 1,
            "errors_list": [f"Invalid JSON format: {str(e)}"]
        }
    
    # Validate it's a list
    if not isinstance(tasks_data, list):
        return {
            "imported": 0,
            "errors": 1,
            "errors_list": ["JSON must be an array of task objects"]
        }
    
    # Import each task
    for idx, task_data in enumerate(tasks_data):
        try:
            # Parse and validate data
            task = Task(
                user_id=user_id,  # Always set from authenticated user
                title=task_data["title"],
                description=task_data.get("description"),
                priority=task_data.get("priority", "medium"),
                due_date=datetime.fromisoformat(task_data["due_date"]) if task_data.get("due_date") else None,
                tags=task_data.get("tags", []),
                completed=task_data.get("completed", False)
            )
            
            # Validate task data
            if len(task.title) > 200:
                raise ValueError("Title exceeds 200 characters")
            if task.description and len(task.description) > 1000:
                raise ValueError("Description exceeds 1000 characters")
            if task.priority not in ["low", "medium", "high"]:
                raise ValueError("Invalid priority value")
            
            db.add(task)
            imported += 1
        
        except KeyError as e:
            errors += 1
            errors_list.append(f"Item {idx + 1}: Missing required field {str(e)}")
        except Exception as e:
            errors += 1
            errors_list.append(f"Item {idx + 1}: {str(e)}")
    
    # Commit all successful imports
    db.commit()
    
    return {
        "imported": imported,
        "errors": errors,
        "errors_list": errors_list if errors > 0 else None
    }
```

**Pattern Rules**:
- Parse JSON and handle decode errors
- Validate JSON structure (must be array)
- Track item indices for error reporting
- Validate each task before adding
- Set user_id from authenticated user
- Handle missing fields gracefully
- Commit all successful imports in one transaction
- Report errors with item numbers

### 7. Import Validation

**Pattern**: Validate imported task data

```python
def validate_imported_task(task_data: dict) -> tuple[bool, Optional[str]]:
    """
    Validate imported task data.
    
    Returns:
        tuple: (is_valid, error_message)
    """
    # Check required fields
    if "title" not in task_data:
        return False, "Missing required field: title"
    
    # Validate title length
    if len(task_data["title"]) > 200:
        return False, "Title exceeds 200 characters"
    
    # Validate description length
    if task_data.get("description") and len(task_data["description"]) > 1000:
        return False, "Description exceeds 1000 characters"
    
    # Validate priority
    if task_data.get("priority") not in [None, "low", "medium", "high"]:
        return False, "Invalid priority value. Must be low, medium, or high"
    
    # Validate due_date format
    if task_data.get("due_date"):
        try:
            datetime.fromisoformat(task_data["due_date"])
        except ValueError:
            return False, "Invalid due_date format. Use ISO format (YYYY-MM-DD)"
    
    # Validate tags is array
    if task_data.get("tags") and not isinstance(task_data["tags"], list):
        return False, "Tags must be an array"
    
    return True, None
```

**Pattern Rules**:
- Validate required fields
- Validate field lengths
- Validate enum values (priority)
- Validate date formats
- Validate data types (tags array)
- Return clear error messages

### 8. Error Handling in Import

**Pattern**: Handle import errors gracefully

```python
def import_tasks_from_file(
    db: Session,
    user_id: str,
    content: bytes,
    format: str
) -> Dict:
    """Import tasks with error handling"""
    try:
        if format == "csv":
            return import_from_csv(db, user_id, content)
        elif format == "json":
            return import_from_json(db, user_id, content)
        else:
            return {
                "imported": 0,
                "errors": 1,
                "errors_list": [f"Unsupported format: {format}"]
            }
    except Exception as e:
        # Rollback on unexpected errors
        db.rollback()
        return {
            "imported": 0,
            "errors": 1,
            "errors_list": [f"Import failed: {str(e)}"]
        }
```

**Pattern Rules**:
- Handle format errors
- Rollback on unexpected errors
- Return error statistics
- Don't expose internal error details

### 9. Service Layer Integration

**Pattern**: Implement export/import in service layer

```python
from backend.services.task_service import TaskService

class TaskService:
    def export_tasks(
        self,
        db: Session,
        user_id: str,
        format: str
    ) -> bytes:
        """Export tasks to CSV or JSON"""
        tasks = db.exec(
            select(Task).where(Task.user_id == user_id)
        ).all()
        
        if format == "csv":
            return self._export_to_csv(tasks)
        else:
            return self._export_to_json(tasks)
    
    def import_tasks(
        self,
        db: Session,
        user_id: str,
        content: bytes,
        filename: str
    ) -> Dict:
        """Import tasks from file"""
        format = "csv" if filename.endswith(".csv") else "json"
        
        if format == "csv":
            return self._import_from_csv(db, user_id, content)
        else:
            return self._import_from_json(db, user_id, content)
```

**Pattern Rules**:
- Delegate to service layer
- Get all tasks for user (no pagination)
- Determine format from filename
- Return bytes for export, dict for import

## Steps for Adding Export/Import

1. **Create Export Endpoint**
   - Validate format parameter
   - Verify user_id
   - Get all tasks for user
   - Generate file content
   - Return Response with file

2. **Create Import Endpoint**
   - Validate file type
   - Verify user_id
   - Read file content
   - Determine format
   - Import tasks
   - Return statistics

3. **Implement Export Functions**
   - CSV: Use csv.DictWriter
   - JSON: Use json.dumps
   - Handle datetime serialization
   - Encode to UTF-8 bytes

4. **Implement Import Functions**
   - CSV: Use csv.DictReader
   - JSON: Use json.loads
   - Validate each item
   - Track errors
   - Commit in transaction

5. **Add Validation**
   - Validate required fields
   - Validate field lengths
   - Validate enum values
   - Validate date formats

## Common Patterns Summary

- ✅ Support CSV and JSON formats
- ✅ Enforce user isolation (user_id from JWT)
- ✅ Validate file types
- ✅ Handle encoding (UTF-8)
- ✅ Validate imported data
- ✅ Report import statistics
- ✅ Handle errors gracefully
- ✅ Use transactions for atomic import
- ✅ Return file download for export
- ✅ Return import results for import

