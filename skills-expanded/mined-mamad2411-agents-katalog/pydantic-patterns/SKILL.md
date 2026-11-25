---
name: pydantic-patterns
description: "When to activate: Pydantic v2, data validation, serialization, settings management, pydantic-settings, field validators"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: python
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Pydantic v2 Patterns

## Model Configuration
```python
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from pydantic import AliasChoices, AliasPath

class UserModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,       # replaces orm_mode = True
        str_strip_whitespace=True,  # strip leading/trailing whitespace
        validate_default=True,      # validate default values
        frozen=True,                # immutable after creation
    )
    
    id: int
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(pattern=r"^[\w.+-]+@[\w-]+\.[\w.]+$")
    age: int = Field(gt=0, le=150)
    tags: list[str] = Field(default_factory=list)
```

## Field Validators (v2 API)
```python
from pydantic import field_validator, model_validator
from typing import Self

class SignupRequest(BaseModel):
    email: str
    password: str
    password_confirm: str
    
    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.lower().strip()
    
    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be ≥8 characters")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain a digit")
        return v
    
    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")
        return self
```

## Settings with pydantic-settings
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, PostgresDsn

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    database_url: PostgresDsn
    secret_key: SecretStr
    debug: bool = False
    cors_origins: list[str] = ["http://localhost:3000"]
    
    @property
    def db_url_str(self) -> str:
        return str(self.database_url)

settings = Settings()  # reads from env + .env file
```

## Custom Types
```python
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema
from typing import Annotated

class PositiveInt(int):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
        return core_schema.int_schema(gt=0)

class UserId(int):
    pass

# Use Annotated for reusable constraints
EmailStr = Annotated[str, Field(pattern=r"^[\w.+-]+@[\w-]+\.[\w.]+$")]
PositiveFloat = Annotated[float, Field(gt=0)]
```

## Serialization
```python
from pydantic import BaseModel, field_serializer
from datetime import datetime

class EventModel(BaseModel):
    name: str
    timestamp: datetime
    
    @field_serializer("timestamp")
    def serialize_timestamp(self, v: datetime) -> str:
        return v.isoformat()

event = EventModel(name="signup", timestamp=datetime.utcnow())
event.model_dump()           # → dict
event.model_dump_json()      # → JSON string
event.model_dump(mode="json")  # → dict suitable for JSON serialization
```

## Migration from v1 to v2
| v1 | v2 |
|---|---|
| `orm_mode = True` | `model_config = ConfigDict(from_attributes=True)` |
| `@validator` | `@field_validator` |
| `@root_validator` | `@model_validator` |
| `.dict()` | `.model_dump()` |
| `.json()` | `.model_dump_json()` |
| `Optional[T]` | `T \| None` |
| `Field(regex=...)` | `Field(pattern=...)` |
