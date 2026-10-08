# Pydantic Error Handling

Pydantic validation errors and how to raise errors in validators.

## ValidationError Structure

When validation fails, Pydantic raises `ValidationError` with structured error data:

```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    name: str
    age: int

try:
    User(name="Alice", age="not-a-number")
except ValidationError as e:
    print(e.errors())
```

Each error contains:

| Field | Description | Example |
|-------|-------------|---------|
| `type` | Error type identifier | `"int_parsing"` |
| `loc` | Location as tuple | `("age",)` |
| `msg` | Human-readable message | `"Input should be a valid integer"` |
| `input` | The invalid input value | `"not-a-number"` |
| `ctx` | Context for the error | `{"error": ...}` |
| `url` | Link to error docs | `"https://errors.pydantic.dev/..."` |

## Raising Errors in Validators

### Use ValueError, Not ValidationError

**Important**: In validators, raise `ValueError` or `AssertionError`, not `ValidationError` directly.

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    password: str
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v
```

### PydanticCustomError for Rich Errors

Use `PydanticCustomError` to provide custom error types and context:

```python
from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError

class User(BaseModel):
    password: str
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise PydanticCustomError(
                "password_too_short",  # Custom error type
                "Password must be at least {min_length} characters",
                {"min_length": 8}  # Context for message formatting
            )
        if not any(c.isupper() for c in v):
            raise PydanticCustomError(
                "password_no_uppercase",
                "Password must contain at least one uppercase letter",
                {}
            )
        return v
```

### model_validator for Cross-Field Validation

```python
from pydantic import BaseModel, model_validator

class UserCreate(BaseModel):
    password: str
    confirm_password: str
    
    @model_validator(mode="after")
    def passwords_match(self) -> "UserCreate":
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
```

## Customizing Error Messages

### Error Type Mapping

Map error types to custom messages:

```python
from pydantic import ValidationError

CUSTOM_MESSAGES = {
    "int_parsing": "This field must be a number",
    "string_too_short": "This field is too short",
    "missing": "This field is required",
    "password_too_short": "Password is too weak",
}

def format_errors(exc: ValidationError) -> list[dict]:
    errors = []
    for error in exc.errors():
        error_type = error["type"]
        message = CUSTOM_MESSAGES.get(error_type, error["msg"])
        
        # Format with context if available
        if ctx := error.get("ctx"):
            message = message.format(**ctx)
        
        errors.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": message,
        })
    return errors
```

### In FastAPI Exception Handler

```python
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        loc = error["loc"]
        # Skip first element ("body", "query", "path")
        field = ".".join(str(x) for x in loc[1:]) if len(loc) > 1 else str(loc[0])
        errors.append({
            "field": field,
            "message": CUSTOM_MESSAGES.get(error["type"], error["msg"]),
        })
    
    return JSONResponse(
        status_code=422,
        content={"error": {"code": "validation_error", "errors": errors}}
    )
```

## Error Location Format Conversion

Convert location tuple to dot notation:

```python
def loc_to_dot(loc: tuple) -> str:
    """Convert ('items', 0, 'name') to 'items[0].name'"""
    parts = []
    for item in loc:
        if isinstance(item, int):
            parts.append(f"[{item}]")
        elif parts:
            parts.append(f".{item}")
        else:
            parts.append(item)
    return "".join(parts)

# Example usage
error_loc = ("items", 1, "price")
print(loc_to_dot(error_loc))  # "items[1].price"
```

## Common Patterns

### Conditional Validation

```python
from pydantic import BaseModel, model_validator

class Order(BaseModel):
    order_type: str
    shipping_address: str | None = None
    
    @model_validator(mode="after")
    def validate_shipping(self) -> "Order":
        if self.order_type == "physical" and not self.shipping_address:
            raise ValueError("Shipping address required for physical orders")
        return self
```

### Validation with External Data

```python
from pydantic import BaseModel, field_validator

VALID_COUNTRIES = {"US", "CA", "UK", "DE", "FR"}

class Address(BaseModel):
    country: str
    
    @field_validator("country")
    @classmethod
    def validate_country(cls, v: str) -> str:
        if v.upper() not in VALID_COUNTRIES:
            raise ValueError(f"Country must be one of: {', '.join(VALID_COUNTRIES)}")
        return v.upper()
```

## Anti-Patterns

### Don't Raise ValidationError Directly

```python
from pydantic import BaseModel, field_validator, ValidationError

class User(BaseModel):
    email: str
    
    # BAD - Don't raise ValidationError in validators
    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValidationError(...)  # Wrong!
        return v
    
    # GOOD - Raise ValueError
    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v
```

### Don't Silently Fix Invalid Data

```python
class User(BaseModel):
    age: int
    
    # BAD - Silently changes data
    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v < 0:
            return 0  # Silently fixes - user doesn't know
        return v
    
    # GOOD - Reject invalid data
    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Age cannot be negative")
        return v
```

### Be Careful with Coercion

```python
from pydantic import BaseModel

class Config(BaseModel):
    enabled: bool

# Pydantic coerces these to bool - may be unexpected
config = Config(enabled="false")  # enabled = True (non-empty string is truthy)
config = Config(enabled="0")      # enabled = True
config = Config(enabled=0)        # enabled = False

# Use strict mode if needed
from pydantic import ConfigDict

class StrictConfig(BaseModel):
    model_config = ConfigDict(strict=True)
    enabled: bool

StrictConfig(enabled="false")  # Raises ValidationError
```

## Integration with FastAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel, field_validator

app = FastAPI()

class UserCreate(BaseModel):
    username: str
    password: str
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v.lower()

@app.post("/users")
async def create_user(user: UserCreate):
    # Validation happens automatically
    # Errors handled by global RequestValidationError handler
    return {"username": user.username}
```
