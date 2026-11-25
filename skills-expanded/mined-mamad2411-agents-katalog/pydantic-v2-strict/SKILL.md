---
name: pydantic-v2-strict
version: "1.0"
description: >
  Pydantic V2 data modeling with strict mode enforcement for type safety.
  PROACTIVELY activate for: (1) Creating data models or schemas, (2) Validating API request/response types,
  (3) Building configuration classes, (4) Defining data contracts, (5) Implementing DTOs.
  Triggers: "pydantic", "BaseModel", "ConfigDict", "Field", "validator", "model_dump", "strict mode", "data model"
core-integration:
  techniques:
    primary: ["completeness_verification"]
    secondary: ["structured_decomposition"]
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# Pydantic V2 Strict Mode Data Modeling

## Core Principles

Pydantic V2 is a complete rewrite with a Rust core for maximum performance. **All models in the Vibekit ecosystem MUST use strict mode** to ensure type safety and eliminate implicit type coercion.

## BaseModel with ConfigDict (Required Pattern)

The modern way to configure Pydantic models uses `ConfigDict`:

```python
from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated

# ✅ REQUIRED: Use ConfigDict for all model configuration
class User(BaseModel):
    model_config = ConfigDict(
        strict=True,              # MANDATORY: No type coercion
        frozen=True,              # Immutable after creation
        extra='forbid',           # Reject unknown fields
        validate_assignment=True  # Validate on field updates
    )

    id: int
    email: str
    username: str
    is_active: bool = True

# ✅ REQUIRED: Use Field() for constraints and metadata
class Product(BaseModel):
    model_config = ConfigDict(strict=True, frozen=True)

    id: int = Field(gt=0, description="Product ID must be positive")
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0.0, description="Price must be positive")
    tags: list[str] = Field(default_factory=list)

# ❌ FORBIDDEN: Legacy V1 Config class
class LegacyUser(BaseModel):
    class Config:  # DO NOT USE THIS
        frozen = True
        extra = 'forbid'
```

## Strict Mode: No Implicit Coercion

Strict mode is **mandatory** for all Vibekit Python code. It prevents silent bugs from type coercion:

```python
from pydantic import BaseModel, ConfigDict, ValidationError

class StrictModel(BaseModel):
    model_config = ConfigDict(strict=True)

    age: int
    score: float
    is_active: bool

# ✅ With strict=True, only exact types are accepted
try:
    StrictModel(age=25, score=95.5, is_active=True)  # ✅ Works
    StrictModel(age="25", score=95.5, is_active=True)  # ❌ Raises ValidationError
except ValidationError as e:
    print(e)
    # Input should be a valid integer, got str

# Without strict mode (DO NOT USE):
class LooseModel(BaseModel):
    # NO model_config - defaults to strict=False
    age: int

# This silently converts "25" to 25 - DANGEROUS!
m = LooseModel(age="25")  # Works but shouldn't
print(m.age)  # 25 (int)
```

## Nested Models and Composition

Build complex data structures by nesting models:

```python
from pydantic import BaseModel, ConfigDict, Field

class Address(BaseModel):
    model_config = ConfigDict(strict=True, frozen=True)

    street: str
    city: str
    country: str
    postal_code: str

class Company(BaseModel):
    model_config = ConfigDict(strict=True, frozen=True)

    name: str
    headquarters: Address

class Employee(BaseModel):
    model_config = ConfigDict(strict=True, frozen=True)

    id: int
    name: str
    email: str
    company: Company
    home_address: Address | None = None

# Usage
employee = Employee(
    id=1,
    name="Alice",
    email="alice@example.com",
    company=Company(
        name="TechCorp",
        headquarters=Address(
            street="123 Tech St",
            city="San Francisco",
            country="USA",
            postal_code="94105"
        )
    )
)
```

## Field Aliasing for External Data

Map model fields to different keys in JSON/external data:

```python
from pydantic import BaseModel, ConfigDict, Field

class APIResponse(BaseModel):
    model_config = ConfigDict(strict=True)

    # Map camelCase API to snake_case Python
    user_id: int = Field(validation_alias='userId', serialization_alias='userId')
    first_name: str = Field(validation_alias='firstName', serialization_alias='firstName')
    last_name: str = Field(validation_alias='lastName', serialization_alias='lastName')
    created_at: str = Field(validation_alias='createdAt', serialization_alias='createdAt')

# Input from API (camelCase)
api_data = {
    'userId': 123,
    'firstName': 'John',
    'lastName': 'Doe',
    'createdAt': '2025-01-01T00:00:00Z'
}

response = APIResponse.model_validate(api_data)
print(response.user_id)  # 123 (Python snake_case)

# Serialize back to camelCase
output = response.model_dump(by_alias=True)
# {'userId': 123, 'firstName': 'John', ...}
```

## Validators (V2 Syntax)

Pydantic V2 uses new decorator syntax for validators:

```python
from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from typing import Self

class UserRegistration(BaseModel):
    model_config = ConfigDict(strict=True)

    email: str
    password: str
    confirm_password: str
    age: int

    # ✅ REQUIRED: Use @field_validator for field-level validation
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if '@' not in v:
            raise ValueError('Invalid email address')
        return v.lower()  # Normalize to lowercase

    @field_validator('age')
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v < 18:
            raise ValueError('Must be 18 or older')
        return v

    # ✅ REQUIRED: Use @model_validator for cross-field validation
    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self

# ❌ FORBIDDEN: V1 validator syntax
class LegacyModel(BaseModel):
    email: str

    @validator('email')  # Old V1 decorator - DO NOT USE
    def validate_email(cls, v):
        pass
```

## Serialization with model_dump()

Control how models are serialized:

```python
from pydantic import BaseModel, ConfigDict, Field

class User(BaseModel):
    model_config = ConfigDict(strict=True)

    id: int
    email: str
    password_hash: str
    is_admin: bool = False
    metadata: dict[str, any] = Field(default_factory=dict)

user = User(
    id=1,
    email="user@example.com",
    password_hash="hashed_secret",
    is_admin=True
)

# ✅ REQUIRED: Use model_dump() (not dict())
user_dict = user.model_dump()
# {'id': 1, 'email': 'user@example.com', 'password_hash': 'hashed_secret', ...}

# Exclude sensitive fields
public_data = user.model_dump(exclude={'password_hash'})
# {'id': 1, 'email': 'user@example.com', 'is_admin': True, ...}

# Include only specific fields
minimal = user.model_dump(include={'id', 'email'})
# {'id': 1, 'email': 'user@example.com'}

# ✅ REQUIRED: Use model_dump_json() for JSON strings
json_string = user.model_dump_json(exclude={'password_hash'})

# ❌ FORBIDDEN: V1 methods
user.dict()  # DO NOT USE - deprecated
user.json()  # DO NOT USE - deprecated
```

## Loading Data with model_validate()

Parse and validate external data:

```python
from pydantic import BaseModel, ConfigDict, ValidationError

class Config(BaseModel):
    model_config = ConfigDict(strict=True)

    api_key: str
    timeout: int
    debug: bool

# ✅ REQUIRED: Use model_validate() for dicts
config_data = {"api_key": "secret", "timeout": 30, "debug": True}
config = Config.model_validate(config_data)

# ✅ REQUIRED: Use model_validate_json() for JSON strings
json_str = '{"api_key": "secret", "timeout": 30, "debug": true}'
config = Config.model_validate_json(json_str)

# Error handling
try:
    bad_data = {"api_key": "secret", "timeout": "not_an_int", "debug": True}
    Config.model_validate(bad_data)
except ValidationError as e:
    print(e.errors())
    # [{'type': 'int_type', 'loc': ('timeout',), 'msg': 'Input should be a valid integer', ...}]

# ❌ FORBIDDEN: V1 methods
Config.parse_obj(config_data)  # DO NOT USE
Config.parse_raw(json_str)     # DO NOT USE
```

## Anti-Patterns to Avoid

### Not Using strict=True
```python
# BAD: Allows silent type coercion
class LooseModel(BaseModel):
    age: int

m = LooseModel(age="25")  # Silently converts string to int

# GOOD: Strict mode prevents this
class StrictModel(BaseModel):
    model_config = ConfigDict(strict=True)
    age: int

# Raises ValidationError on string input
```

### Using V1 Config Class
```python
# BAD: Legacy V1 syntax
class OldModel(BaseModel):
    class Config:
        frozen = True

# GOOD: V2 ConfigDict
class NewModel(BaseModel):
    model_config = ConfigDict(frozen=True)
```

### Using V1 Validator Decorators
```python
# BAD: V1 @validator
class OldValidation(BaseModel):
    email: str

    @validator('email')
    def check_email(cls, v):
        pass

# GOOD: V2 @field_validator
class NewValidation(BaseModel):
    email: str

    @field_validator('email')
    @classmethod
    def check_email(cls, v: str) -> str:
        pass
```

## When to Use This Skill

Activate this skill when:
- Creating new Pydantic models or schemas
- Validating API request/response data
- Building configuration management systems
- Defining data contracts between services
- Implementing data transfer objects (DTOs)
- Migrating Pydantic V1 code to V2

## Integration Points

This skill is a **required dependency** for:
- `agentient-rag-engine/data-ingestion-schemas` - RAG data models
- `agentient-frontend-bff/api-contracts` - API schemas
- `agentient-adk-agents/agent-tool-schemas` - ADK tool definitions

## Related Resources

For advanced patterns, see:
- Official Pydantic V2 Migration Guide: https://docs.pydantic.dev/latest/migration/
- Type Hints Best Practices: See `type-hints-best-practices` skill
