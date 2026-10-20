# Security Rules — Python Examples

**Framework basis:** Python 3.11+, FastAPI + Pydantic v2, SQLAlchemy 2.x,
`passlib`/`bcrypt`. The rules themselves are framework-agnostic — these examples
only show one concrete stack.
**Translation hints:** Django → `@login_required`/permissions, the ORM's
parameter binding, template auto-escaping; Flask → an auth decorator +
`SQLAlchemy`/`parameterized` queries. **Version-sensitive:** Pydantic v2 uses
`model_validator`/`Field`; v1 uses `@validator`. SQLAlchemy 2.x uses `select()`.

## Rule 1 — Authenticate then authorize, deny by default
Violation:
```python
@router.get("/admin/report")               # no dependency, open to anyone
def report():
    return svc.build()
```
Correct:
```python
@router.get("/admin/report", dependencies=[Depends(require_role("admin"))])
def report():                              # explicit grant; closed by default
    return svc.build()
```

## Rule 2 — Object-level authorization (IDOR/BOLA)
Violation:
```python
@router.get("/accounts/{account_id}")
def get(account_id: int):
    return repo.get(account_id)            # any logged-in user reads any account
```
Correct:
```python
@router.get("/accounts/{account_id}")
def get(account_id: int, me: User = Depends(current_user)):
    acct = repo.get_for_owner(account_id, me.id)   # scoped to caller
    if acct is None:
        raise AccountNotFound(account_id)
    return acct
```

## Rule 3 — Validate untrusted input at the boundary
Violation:
```python
@router.post("/rename")
def rename(body: dict):                    # untyped, unbounded
    name = body["name"]
```
Correct:
```python
class RenameRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)

@router.post("/rename")
def rename(req: RenameRequest):            # validated by Pydantic at the edge
    ...
```

## Rule 4 — Make injection structurally impossible
Violation:
```python
db.execute(f"SELECT * FROM txn WHERE note = '{note}'")   # SQL injection
os.system(f"convert {user_path}")                        # command injection
```
Correct:
```python
db.execute(select(Txn).where(Txn.note == note))          # bound via ORM
subprocess.run(["convert", user_path], check=True)       # arg list, no shell
```

## Rule 5 — Encode output for its sink (XSS)
Violation:
```python
return HTMLResponse(f"<div>{user_comment}</div>")        # raw interpolation
# Jinja: {{ comment | safe }}                             # disables escaping
```
Correct:
```python
# Jinja auto-escapes by default:
return templates.TemplateResponse("c.html", {"comment": user_comment})  # {{ comment }}
```

## Rule 6 — No secrets in source
Violation:
```python
API_KEY = "sk_live_5f3a..."                # credential literal
```
Correct:
```python
API_KEY = settings.rates_api_key           # from config (config-warden)
```

## Rule 7 — Never leak sensitive data outward
Violation:
```python
return JSONResponse(status_code=500, content={"error": traceback.format_exc()})
logger.info("login user=%s pwd=%s", email, raw_password)   # secret in logs
```
Correct:
```python
return JSONResponse(status_code=500, content={"code": "INTERNAL", "message": "Unexpected error"})
logger.info("login attempt", extra={"user": email})       # no secret
```

## Rule 8 — Store credentials safely
Violation:
```python
user.password = hashlib.md5(raw.encode()).hexdigest()      # fast, unsalted
if token == stored: ...                                     # non-constant-time
```
Correct:
```python
user.password = pwd_context.hash(raw)                       # bcrypt/argon2 via passlib
hmac.compare_digest(token, stored)                          # constant time
```

## Rule 9 — Secure cookies, sessions, CORS
Violation:
```python
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True)  # forbidden combo
response.set_cookie("session", sid)                         # not HttpOnly/Secure/SameSite
```
Correct:
```python
app.add_middleware(CORSMiddleware, allow_origins=["https://app.example.com"],
                   allow_credentials=True)                  # explicit allow-list
response.set_cookie("session", sid, httponly=True, secure=True, samesite="lax")
```

## Rule 10 — Third-party responses are untrusted too
Violation:
```python
html = rates_client.fetch_widget()          # remote HTML
return HTMLResponse(html)                    # reflected verbatim
```
Correct:
```python
dto = rates_client.fetch_rate()              # validated model at the seam
if dto.rate is None:
    raise RatesUnavailable()
return {"rate": dto.rate}                     # only validated scalar used
```
