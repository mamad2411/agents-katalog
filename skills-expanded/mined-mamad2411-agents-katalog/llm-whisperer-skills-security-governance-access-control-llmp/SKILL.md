# Access Control for LLMs

## Overview

Access control for LLM systems ensures that only authorized users and services can interact with models, data, and APIs. This includes role-based access control (RBAC), API key management, rate limiting, and fine-grained permissions for different model capabilities. Production systems need layered security that protects against both external attacks and internal misuse.

## Key Concepts

- **Role-based access control (RBAC)**: Assigning permissions through roles rather than individual users
- **API key management**: Secure generation, rotation, and revocation of API keys
- **Rate limiting**: Controlling request frequency per user/role to prevent abuse
- **Token-based authentication**: JWT/OAuth2 for stateless auth in distributed systems
- **Fine-grained permissions**: Controlling access to specific models, endpoints, and features
- **Audit logging**: Recording all access attempts for security monitoring

## Implementation Patterns

```python
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import hashlib
import secrets

class Permission(Enum):
    MODEL_READ = "model:read"
    MODEL_WRITE = "model:write"
    INFERENCE = "inference"
    ADMIN = "admin"

@dataclass
class Role:
    name: str
    permissions: set[Permission]
    rate_limit: int = 100  # requests per minute

@dataclass
class APIKey:
    key_hash: str
    user_id: str
    roles: list[str]
    created_at: str
    expires_at: str | None = None
    is_active: bool = True

class AccessControlManager:
    """Manage access control for LLM systems."""

    def __init__(self):
        self.roles: dict[str, Role] = {}
        self.api_keys: dict[str, APIKey] = {}
        self._setup_default_roles()

    def _setup_default_roles(self):
        self.roles["viewer"] = Role("viewer", {Permission.MODEL_READ}, rate_limit=50)
        self.roles["user"] = Role("user", {Permission.MODEL_READ, Permission.INFERENCE}, rate_limit=100)
        self.roles["admin"] = Role("admin", set(Permission), rate_limit=1000)

    def create_api_key(self, user_id: str, roles: list[str]) -> str:
        """Create a new API key for a user."""
        key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        self.api_keys[key_hash] = APIKey(
            key_hash=key_hash,
            user_id=user_id,
            roles=roles,
            created_at=datetime.utcnow().isoformat(),
        )
        return key

    def validate_access(self, api_key: str, required_permission: Permission) -> bool:
        """Validate API key and check permission."""
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        key = self.api_keys.get(key_hash)
        if not key or not key.is_active:
            return False
        if key.expires_at and key.expires_at < datetime.utcnow().isoformat():
            return False
        for role_name in key.roles:
            role = self.roles.get(role_name)
            if role and required_permission in role.permissions:
                return True
        return False

    def revoke_key(self, api_key: str):
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        if key_hash in self.api_keys:
            self.api_keys[key_hash].is_active = False
```

## Best Practices

1. Use short-lived tokens with refresh mechanisms for user sessions
2. Implement rate limiting per API key with sliding window counters
3. Hash API keys before storage — never store plaintext keys
4. Rotate API keys regularly with grace periods for old keys
5. Log all authentication and authorization events
6. Use separate keys for different environments (dev, staging, prod)
7. Implement IP allowlisting for production API keys
8. Use secrets managers (Vault, AWS Secrets Manager) for key storage

## Common Pitfalls

- Storing API keys in version control or environment variables
- Not implementing rate limiting, allowing abuse
- Using long-lived tokens without rotation
- Not logging failed authentication attempts
- Granting admin permissions by default

## References

- OWASP Authentication Cheat Sheet
- JWT Best Practices: https://datatracker.ietf.org/doc/html/rfc8725
- "API Security Best Practices" (OWASP, 2024)
