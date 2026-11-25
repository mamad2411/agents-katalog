# Backend Service Layer Skill

**Purpose**: Guidance for implementing business logic in service layer, separated from route handlers.

## Overview

Service layer contains business logic, database operations, and validation. Routes delegate to services, keeping HTTP concerns separate from business logic.

## Key Patterns

### 1. Service Class Structure

**File Location**: `/backend/services/task_service.py`, `/backend/services/auth_service.py`

**Pattern**: Create service classes with methods for business operations

```python
from sqlmodel import Session, select
from typing import Optional, List, Dict
from backend.models import Task, User
from backend.schemas.requests import TaskCreateRequest, TaskUpdateRequest

class TaskService:
    """Service for task-related business logic"""
    
    def create_task(
        self,
        db: Session,
        user_id: str,
        task_data: TaskCreateRequest
    ) -> Task:
        """
        Create a new task for user.
        
        Args:
            db: Database session
            user_id: User ID (from JWT token)
            task_data: Task creation data
        
        Returns:
            Task: Created task object
        
        Raises:
            ValueError: If validation fails
        """
        # Validate task data
        self._validate_task_data(task_data)
        
        # Create task
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority or "medium",
            due_date=task_data.due_date,
            tags=task_data.tags or []
        )
        
        db.add(task)
        db.commit()
        db.refresh(task)
        
        return task
    
    def get_tasks(
        self,
        db: Session,
        user_id: str,
        filters: Optional[Dict] = None,
        pagination: Optional[Dict] = None
    ) -> tuple[List[Task], int]:
        """
        Get tasks for user with filtering and pagination.
        
        Returns:
            tuple: (tasks list, total count)
        """
        # Build query with user isolation
        statement = select(Task).where(Task.user_id == user_id)
        
        # Apply filters
        if filters:
            statement = self._apply_filters(statement, filters)
        
        # Get total count
        count_statement = select(func.count()).select_from(statement.subquery())
        total = db.exec(count_statement).one()
        
        # Apply sorting and pagination
        statement = self._apply_sorting(statement, filters.get("sort"))
        if pagination:
            statement = statement.offset(
                (pagination["page"] - 1) * pagination["limit"]
            ).limit(pagination["limit"])
        
        tasks = db.exec(statement).all()
        return tasks, total
    
    def _validate_task_data(self, task_data: TaskCreateRequest):
        """Validate task data"""
        if len(task_data.title) > 200:
            raise ValueError("Title must be 200 characters or less")
        if task_data.description and len(task_data.description) > 1000:
            raise ValueError("Description must be 1000 characters or less")
        if task_data.priority not in ["low", "medium", "high", None]:
            raise ValueError("Priority must be low, medium, or high")
    
    def _apply_filters(self, statement, filters: Dict):
        """Apply filters to query"""
        # Implementation
        return statement
    
    def _apply_sorting(self, statement, sort: Optional[str]):
        """Apply sorting to query"""
        # Implementation
        return statement
```

**Pattern Rules**:
- Create service classes for each domain (TaskService, AuthService)
- Methods take `db: Session` and `user_id` as first parameters
- Methods return domain objects (Task, User) not response models
- Use private methods (`_method`) for internal logic
- Raise `ValueError` for validation errors
- Always filter by user_id for user isolation

### 2. Authentication Service

**Pattern**: Service for user authentication and management

```python
from sqlmodel import Session, select
from backend.models import User
from backend.middleware.jwt import hash_password, verify_password

class AuthService:
    """Service for authentication-related business logic"""
    
    def create_user(
        self,
        db: Session,
        email: str,
        password: str,
        name: str
    ) -> User:
        """
        Create new user account.
        
        Raises:
            ValueError: If email already exists or validation fails
        """
        # Check if email already exists
        existing_user = db.exec(
            select(User).where(User.email == email)
        ).first()
        
        if existing_user:
            raise ValueError("Email already registered")
        
        # Validate email format
        if not self._validate_email(email):
            raise ValueError("Invalid email format")
        
        # Validate password strength
        if not self._validate_password_strength(password):
            raise ValueError("Password does not meet strength requirements")
        
        # Hash password
        password_hash = hash_password(password)
        
        # Create user
        user = User(
            email=email,
            password_hash=password_hash,
            name=name
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    def authenticate_user(
        self,
        db: Session,
        email: str,
        password: str
    ) -> Optional[User]:
        """
        Authenticate user with email and password.
        
        Returns:
            User if authentication successful, None otherwise
        """
        # Find user by email
        user = db.exec(
            select(User).where(User.email == email)
        ).first()
        
        if not user:
            return None
        
        # Verify password
        if not verify_password(password, user.password_hash):
            return None
        
        return user
    
    def _validate_email(self, email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _validate_password_strength(self, password: str) -> bool:
        """Validate password strength"""
        if len(password) < 8:
            return False
        # Add more validation rules as needed
        return True
```

**Pattern Rules**:
- Check email uniqueness before creating user
- Validate email format and password strength
- Hash passwords before storing
- Return None for failed authentication (not raise exception)
- Use private methods for validation logic

### 3. Task Service with Query Parameters

**Pattern**: Service methods for complex queries with filtering, sorting, search

```python
from sqlmodel import Session, select, or_, func
from typing import Optional, List, Dict
from datetime import datetime

class TaskService:
    def get_tasks(
        self,
        db: Session,
        user_id: str,
        status: Optional[str] = None,
        sort: Optional[str] = None,
        search: Optional[str] = None,
        priority: Optional[str] = None,
        due_date: Optional[str] = None,
        tags: Optional[List[str]] = None,
        page: int = 1,
        limit: int = 20
    ) -> Dict:
        """
        Get tasks with comprehensive filtering, sorting, search, and pagination.
        
        Returns:
            dict: {
                "data": List[Task],
                "meta": {
                    "total": int,
                    "page": int,
                    "limit": int,
                    "totalPages": int
                }
            }
        """
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
            due_date_obj = datetime.fromisoformat(due_date)
            statement = statement.where(Task.due_date == due_date_obj)
        
        # Apply tags filter
        if tags:
            for tag in tags:
                statement = statement.where(Task.tags.contains([tag]))
        
        # Apply search filter (full-text search)
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
        statement = self._apply_sorting(statement, sort)
        
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
    
    def _apply_sorting(self, statement, sort: Optional[str]):
        """Apply sorting to query"""
        if sort == "created":
            return statement.order_by(Task.created_at.desc())
        elif sort == "title":
            return statement.order_by(Task.title.asc())
        elif sort == "updated":
            return statement.order_by(Task.updated_at.desc())
        elif sort == "priority":
            from sqlalchemy import case
            priority_order = case(
                (Task.priority == "high", 1),
                (Task.priority == "medium", 2),
                (Task.priority == "low", 3)
            )
            return statement.order_by(priority_order)
        elif sort == "due_date":
            return statement.order_by(Task.due_date.asc().nulls_last())
        else:
            # Default: created_at desc
            return statement.order_by(Task.created_at.desc())
```

**Pattern Rules**:
- Build queries dynamically based on filters
- Always start with user_id filter
- Apply filters before counting
- Apply sorting before pagination
- Return pagination metadata
- Use helper methods for complex logic

### 4. Bulk Operations Service

**Pattern**: Service methods for bulk operations with transactions

```python
from sqlmodel import Session, select
from typing import List

class TaskService:
    def bulk_operations(
        self,
        db: Session,
        user_id: str,
        action: str,
        task_ids: List[int],
        **kwargs
    ) -> int:
        """
        Perform bulk operations on tasks.
        
        Args:
            action: 'delete'|'complete'|'pending'|'priority'
            task_ids: List of task IDs
            **kwargs: Additional parameters (e.g., priority for priority action)
        
        Returns:
            int: Number of affected tasks
        """
        # Get all tasks for user
        tasks = db.exec(
            select(Task).where(
                Task.id.in_(task_ids),
                Task.user_id == user_id  # User isolation
            )
        ).all()
        
        if len(tasks) != len(task_ids):
            raise ValueError("Some tasks not found or don't belong to user")
        
        # Perform action
        if action == "delete":
            for task in tasks:
                db.delete(task)
        elif action == "complete":
            for task in tasks:
                task.completed = True
                db.add(task)
        elif action == "pending":
            for task in tasks:
                task.completed = False
                db.add(task)
        elif action == "priority":
            priority = kwargs.get("priority")
            if priority not in ["low", "medium", "high"]:
                raise ValueError("Invalid priority value")
            for task in tasks:
                task.priority = priority
                db.add(task)
        else:
            raise ValueError(f"Invalid action: {action}")
        
        # Commit all changes atomically
        db.commit()
        
        return len(tasks)
```

**Pattern Rules**:
- Verify all tasks belong to user before bulk operation
- Use transactions for atomic operations
- Validate action parameter
- Return count of affected items
- Raise ValueError for invalid operations

### 5. Statistics Service

**Pattern**: Service methods for aggregations and statistics

```python
from sqlmodel import Session, select, func
from datetime import datetime

class TaskService:
    def get_statistics(
        self,
        db: Session,
        user_id: str
    ) -> Dict:
        """
        Get task statistics for user.
        
        Returns:
            dict: {
                "total": int,
                "completed": int,
                "pending": int,
                "overdue": int
            }
        """
        # Base query with user isolation
        base_statement = select(Task).where(Task.user_id == user_id)
        
        # Total count
        total = db.exec(
            select(func.count()).select_from(base_statement.subquery())
        ).one()
        
        # Completed count
        completed = db.exec(
            select(func.count()).select_from(
                base_statement.where(Task.completed == True).subquery()
            )
        ).one()
        
        # Pending count
        pending = db.exec(
            select(func.count()).select_from(
                base_statement.where(Task.completed == False).subquery()
            )
        ).one()
        
        # Overdue count (pending tasks with due_date < today)
        today = datetime.utcnow().date()
        overdue = db.exec(
            select(func.count()).select_from(
                base_statement.where(
                    Task.completed == False,
                    Task.due_date < today
                ).subquery()
            )
        ).one()
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "overdue": overdue
        }
```

**Pattern Rules**:
- Use aggregate functions (count) for statistics
- Always filter by user_id
- Use subqueries for complex aggregations
- Return structured dictionary

### 6. Export/Import Service

**Pattern**: Service methods for export and import functionality

```python
import csv
import json
from io import StringIO, BytesIO
from typing import List

class TaskService:
    def export_tasks(
        self,
        db: Session,
        user_id: str,
        format: str
    ) -> bytes:
        """
        Export tasks to CSV or JSON format.
        
        Args:
            format: 'csv' or 'json'
        
        Returns:
            bytes: File content
        """
        # Get all tasks for user
        tasks = db.exec(
            select(Task).where(Task.user_id == user_id)
        ).all()
        
        if format == "csv":
            return self._export_to_csv(tasks)
        elif format == "json":
            return self._export_to_json(tasks)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _export_to_csv(self, tasks: List[Task]) -> bytes:
        """Export tasks to CSV format"""
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            "id", "title", "description", "priority", "due_date",
            "tags", "completed", "created_at", "updated_at"
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
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            })
        
        return output.getvalue().encode("utf-8")
    
    def _export_to_json(self, tasks: List[Task]) -> bytes:
        """Export tasks to JSON format"""
        tasks_data = [task.dict() for task in tasks]
        return json.dumps(tasks_data, indent=2, default=str).encode("utf-8")
    
    def import_tasks(
        self,
        db: Session,
        user_id: str,
        file_content: bytes,
        filename: str
    ) -> Dict:
        """
        Import tasks from CSV or JSON file.
        
        Returns:
            dict: {
                "imported": int,
                "errors": int,
                "errors_list": List[str]
            }
        """
        format = "csv" if filename.endswith(".csv") else "json"
        
        if format == "csv":
            return self._import_from_csv(db, user_id, file_content)
        else:
            return self._import_from_json(db, user_id, file_content)
    
    def _import_from_csv(self, db: Session, user_id: str, content: bytes) -> Dict:
        """Import tasks from CSV"""
        imported = 0
        errors = 0
        errors_list = []
        
        csv_content = content.decode("utf-8")
        reader = csv.DictReader(StringIO(csv_content))
        
        for row in reader:
            try:
                # Validate and create task
                task = Task(
                    user_id=user_id,
                    title=row["title"],
                    description=row.get("description") or None,
                    priority=row.get("priority", "medium"),
                    due_date=datetime.fromisoformat(row["due_date"]) if row.get("due_date") else None,
                    tags=row["tags"].split(",") if row.get("tags") else [],
                    completed=row.get("completed", "false").lower() == "true"
                )
                
                db.add(task)
                imported += 1
            except Exception as e:
                errors += 1
                errors_list.append(f"Row {reader.line_num}: {str(e)}")
        
        db.commit()
        
        return {
            "imported": imported,
            "errors": errors,
            "errors_list": errors_list if errors > 0 else None
        }
    
    def _import_from_json(self, db: Session, user_id: str, content: bytes) -> Dict:
        """Import tasks from JSON"""
        imported = 0
        errors = 0
        errors_list = []
        
        tasks_data = json.loads(content.decode("utf-8"))
        
        for idx, task_data in enumerate(tasks_data):
            try:
                task = Task(
                    user_id=user_id,
                    title=task_data["title"],
                    description=task_data.get("description"),
                    priority=task_data.get("priority", "medium"),
                    due_date=datetime.fromisoformat(task_data["due_date"]) if task_data.get("due_date") else None,
                    tags=task_data.get("tags", []),
                    completed=task_data.get("completed", False)
                )
                
                db.add(task)
                imported += 1
            except Exception as e:
                errors += 1
                errors_list.append(f"Item {idx}: {str(e)}")
        
        db.commit()
        
        return {
            "imported": imported,
            "errors": errors,
            "errors_list": errors_list if errors > 0 else None
        }
```

**Pattern Rules**:
- Support CSV and JSON formats
- Handle encoding (UTF-8)
- Validate imported data
- Report errors with line/item numbers
- Use transactions for atomic import
- Return import statistics

## Steps for Adding New Service Method

1. **Define Method Signature**
   - Take `db: Session` and `user_id: str` as first parameters
   - Add type hints for all parameters
   - Add return type hint
   - Add docstring

2. **Implement Business Logic**
   - Validate inputs
   - Perform database operations
   - Handle errors appropriately
   - Return domain objects

3. **Add Validation**
   - Validate user_id (always filter by user_id)
   - Validate input data
   - Raise ValueError for validation errors

4. **Add Tests**
   - Test successful cases
   - Test validation errors
   - Test user isolation

## Common Patterns Summary

- ✅ Separate business logic from HTTP concerns
- ✅ Always filter by user_id for user isolation
- ✅ Use type hints throughout
- ✅ Raise ValueError for validation errors
- ✅ Return domain objects, not response models
- ✅ Use transactions for atomic operations
- ✅ Use private methods for internal logic
- ✅ Add comprehensive docstrings
- ✅ Handle errors gracefully

