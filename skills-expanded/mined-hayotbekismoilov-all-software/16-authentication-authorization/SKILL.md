---
name: authentication-authorization
description: |
  Authentication and authorization implementation patterns. Apply for login/register flows,
  JWT handling, role-based access control, OAuth integration, and session management.
  Covers httpOnly cookies, refresh token rotation, RBAC, and permission decorators.
---

# Authentication & Authorization

## JWT with httpOnly Cookies
```python
# core/security.py
import jwt
from datetime import datetime, timedelta

def create_tokens(user_id: str) -> tuple[str, str]:
    access_payload = {
        "sub": user_id,
        "type": "access",
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(minutes=15),
    }
    refresh_payload = {
        "sub": user_id,
        "type": "refresh",
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(days=7),
    }
    access = jwt.encode(access_payload, settings.SECRET_KEY, algorithm="HS256")
    refresh = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")
    return access, refresh

def set_auth_cookies(response: Response, access: str, refresh: str):
    response.set_cookie("access_token", access, httponly=True, secure=True,
                        samesite="lax", max_age=900)
    response.set_cookie("refresh_token", refresh, httponly=True, secure=True,
                        samesite="lax", max_age=604800, path="/api/v1/auth/refresh")
```

## RBAC (Role-Based Access Control)
```python
# models.py
class UserRole(str, Enum):
    GUEST = "guest"
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    SUPERADMIN = "superadmin"

ROLE_HIERARCHY = {
    UserRole.GUEST: 0,
    UserRole.USER: 1,
    UserRole.MODERATOR: 2,
    UserRole.ADMIN: 3,
    UserRole.SUPERADMIN: 4,
}

def require_role(minimum_role: UserRole):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            if ROLE_HIERARCHY[current_user.role] < ROLE_HIERARCHY[minimum_role]:
                raise HTTPException(403, "Insufficient permissions")
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

# Usage
@router.delete("/users/{user_id}")
@require_role(UserRole.ADMIN)
async def delete_user(user_id: str, current_user: User = Depends(get_current_user)):
    ...
```

## Refresh Token Rotation
```python
@router.post("/auth/refresh")
async def refresh_tokens(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(401, "Refresh token missing")
    
    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("type") != "refresh":
            raise HTTPException(401, "Invalid token type")
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Refresh token expired — please login again")
    
    # Rotate: invalidate old refresh token, issue new pair
    user_id = payload["sub"]
    await invalidate_refresh_token(db, refresh_token)  # Add to blocklist
    
    access, refresh = create_tokens(user_id)
    set_auth_cookies(response, access, refresh)
    return {"success": True, "data": {"access_token": access}}
```

## Frontend Auth State (Zustand)
```typescript
interface AuthStore {
  user: CurrentUser | null;
  isAuthenticated: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => Promise<void>;
  refreshAuth: () => Promise<void>;
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  isAuthenticated: false,

  login: async (credentials) => {
    const data = await api.auth.login(credentials);
    set({ user: data.user, isAuthenticated: true });
  },

  logout: async () => {
    await api.auth.logout();
    set({ user: null, isAuthenticated: false });
    queryClient.clear();
  },

  refreshAuth: async () => {
    try {
      const data = await api.auth.me();
      set({ user: data, isAuthenticated: true });
    } catch {
      set({ user: null, isAuthenticated: false });
    }
  },
}));
```
