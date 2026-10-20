# Controller Rules — Python Examples

**Framework basis:** Python 3.11+, FastAPI 0.100+, Pydantic v2.
The rules themselves are framework-agnostic — these examples only show one
concrete stack.
**Translation hints:** Flask → blueprints + marshmallow/manual validation;
Django REST Framework → ViewSets = controllers, Serializers = DTOs +
validation; "controller" here = FastAPI router/endpoint functions.
**Version-sensitive:** Pydantic v2 shown (`model_validate`, `Field`) — v1
uses `parse_obj`/`validator`. FastAPI 0.100+ pairs with Pydantic v2; older
FastAPI requires v1 models.

## Rule 1 — Translate, don't think
Violation:
```python
@router.post("/registrations")
def register(body: RegistrationRequest, svc=Depends(get_svc)):
    student = svc.get_student(body.student_id)
    if student.credits >= 30 and not student.has_hold():   # business decision
        return svc.register(body.student_id, body.course_id)
    raise HTTPException(400)
```
Correct:
```python
@router.post("/registrations", status_code=201)
def register(body: RegistrationRequest, svc=Depends(get_svc)):
    result = svc.register(RegisterStudent(body.student_id, body.course_id))
    return RegistrationResponse.model_validate(result)     # translate only
```

## Rule 2 — One controller per resource
Violation:
```python
router = APIRouter()                      # grab-bag router
@router.get("/students/{id}") ...
@router.post("/courses") ...              # different resource
@router.get("/reports/enrollment") ...    # and another
```
Correct:
```python
students = APIRouter(prefix="/students")  # one resource each
courses = APIRouter(prefix="/courses")
reports = APIRouter(prefix="/reports")
```

## Rule 3 — Thin handlers
Violation:
```python
@router.post("/students")
def create(body: dict):                   # 40 lines of parsing, checks,
    ...                                   # loops, and formatting
```
Correct:
```python
@router.post("/students", status_code=201)
def create(body: CreateStudentRequest, svc=Depends(get_svc)):
    student = svc.create(body.to_command())
    return StudentResponse.model_validate(student)   # 3 lines: translate
```

## Rule 4 — Validate shape declaratively
Violation:
```python
@router.post("/students")
def create(body: dict):
    if "@" not in body.get("email", ""):             # hand-rolled, in body
        raise HTTPException(400, "bad email")
```
Correct:
```python
class CreateStudentRequest(BaseModel):
    email: EmailStr                                   # declarative shape
    year: int = Field(ge=1, le=6)
# handler receives an already-valid model; existence checks stay in service
```

## Rule 5 — DTOs in, DTOs out
Violation:
```python
@router.get("/students/{id}", response_model=StudentEntity)   # ORM model out
def get(id: int, db=Depends(get_db)):
    return db.get(StudentEntity, id)
```
Correct:
```python
@router.get("/students/{id}", response_model=StudentResponse)  # DTO out
def get(id: int, svc=Depends(get_svc)):
    return StudentResponse.model_validate(svc.get(StudentId(id)))
```

## Rule 6 — No business-error handling
Violation:
```python
@router.post("/registrations")
def register(body: RegistrationRequest, svc=Depends(get_svc)):
    try:
        return svc.register(body.to_command())
    except CourseFullError:                          # domain error caught here
        raise HTTPException(409, "course full")
```
Correct:
```python
@router.post("/registrations", status_code=201)
def register(body: RegistrationRequest, svc=Depends(get_svc)):
    return svc.register(body.to_command())
# app-level exception handler maps CourseFullError → 409 (exception-warden)
```

## Rule 7 — No persistence access
Violation:
```python
@router.get("/students")
def list_students(db: Session = Depends(get_db)):
    return db.query(StudentEntity).all()             # "just a simple read"
```
Correct:
```python
@router.get("/students")
def list_students(svc=Depends(get_svc), page: PageParams = Depends()):
    return [StudentResponse.model_validate(s) for s in svc.list(page)]
```

## Rule 8 — Explicit status codes
Violation:
```python
@router.post("/students")                 # defaults to 200 on create
def create(...): ...
@router.delete("/students/{id}")          # returns 200 with a body
def delete(...): return {"deleted": True}
```
Correct:
```python
@router.post("/students", status_code=201)
def create(...): ...                      # + Location or id in response
@router.delete("/students/{id}", status_code=204)
def delete(...): ...                      # no body
```

## Rule 9 — Declarative security
Violation:
```python
@router.delete("/students/{id}", status_code=204)
def delete(id: int, svc=Depends(get_svc)):           # who may call this?
    svc.delete(StudentId(id))
```
Correct:
```python
@router.delete("/students/{id}", status_code=204,
               dependencies=[Depends(require_role("ADMIN"))])
def delete(id: int, svc=Depends(get_svc)):           # policy visible here
    svc.delete(StudentId(id))
# per-record ownership checks live in the service
```

## Rule 10 — Stateless controllers
Violation:
```python
class StudentRoutes:
    current_user = None                    # shared across requests
    def set_user(self, u): self.current_user = u
```
Correct:
```python
@router.get("/students/me")
def me(user: User = Depends(current_user)):   # per-request via injection
    ...
```

## Rule 11 — HTTP semantics
Violation:
```python
@router.get("/students/{id}/delete")       # GET that mutates
@router.post("/getStudentList")            # verb in path, wrong method
```
Correct:
```python
@router.delete("/students/{id}", status_code=204)
@router.get("/students")                   # nouns + methods carry the verb
```

## Rule 12 — Cap and allowlist collection params
Violation:
```python
@router.get("/students")
def list_students(size: int = 20, sort: str = "id"):
    return svc.list(size=size, sort=sort)  # ?size=10**6, ?sort=password_hash
```
Correct:
```python
SORTABLE = {"id", "last_name", "enrolled_at"}
@router.get("/students")
def list_students(size: int = Query(20, ge=1, le=100),
                  sort: str = Query("id")):
    if sort not in SORTABLE:
        raise RequestValidationError(...)   # boundary concern: allowed here
    return svc.list(size=size, sort=sort)
```

## Rule 13 — Version and document
Violation:
```python
app.include_router(students)               # no version; endpoint undocumented
```
Correct:
```python
app.include_router(students, prefix="/v1")
@router.get("/students/{id}", response_model=StudentResponse,
            summary="Get a student by id",
            responses={404: {"description": "Student not found"}})
```

## Rule 14 — Test the mapping only
Violation:
```python
def test_register_rejects_when_course_full(client):   # business behavior
    ...                                                # re-tested via HTTP
```
Correct:
```python
def test_post_registrations_returns_201(client_with_fake_svc): ...
def test_malformed_email_returns_422(client_with_fake_svc): ...
def test_delete_requires_admin_role(client_with_fake_svc): ...
# course-full behavior is a service test (test-warden's territory)
```
