# Persistence Rules — Python Examples

**Framework basis:** the legacy backend (`backend/app.py`): a single-file Flask
app with a hand-written data-access layer over raw `sqlite3` — no ORM. A fresh
connection per request (`get_connection`), `sqlite3.Row` row factory,
`init_db()` as the schema/migration path (`CREATE TABLE IF NOT EXISTS` +
`PRAGMA table_info` → `ALTER TABLE ... ADD COLUMN`), and `row_to_dict()` as the
snake_case→camelCase boundary. The rules are stack-agnostic — these examples show
the raw-SQL DAO shape; the ORM shape is in the Java file.
**Translation hints:** SQLAlchemy Core/ORM → sessions + mapped classes replace
manual cursors, same scoping/bounding/migration rules; Django ORM → models +
migrations, `Model.objects` querysets; the injection, owner-scoping, and
additive-migration rules are identical everywhere.
**Version-sensitive:** stdlib `sqlite3`; `PRAGMA foreign_keys` is OFF by default,
so declared `FOREIGN KEY`s are NOT enforced and deletes never cascade — the
existing schema relies on this (documents reference a student loosely).

## Rule 1 — Map to the real schema, exactly
Violation:
```python
def row_to_dict(row):
    return {"firstName": row["firstname"]}   # column is `first_name`: KeyError,
                                             # or a silent guess at the wrong name
```
Correct:
```python
def row_to_dict(row):                        # explicit snake_case → camelCase map
    return {
        "id": row["id"],
        "firstName": row["first_name"],      # names the real column exactly
        "registeredAt": row["registered_at"],
    }
```

## Rule 2 — Data-access code only fetches and persists
Violation:
```python
def insert_student(conn, data):
    data["registered_at"] = utc_now_seconds()        # rule/clock decision here
    if conn.execute("SELECT 1 FROM students WHERE email = ?", (data["email"],)).fetchone():
        raise ValueError("duplicate")                # business rule in the DAO
    conn.execute("INSERT INTO students (...) VALUES (...)", ...)
```
Correct:
```python
def insert_student(conn, student):           # just persists what it's handed
    cur = conn.execute(
        "INSERT INTO students (first_name, last_name, email, program, address, "
        "phone, registered_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (student.first_name, ..., student.registered_at),
    )
    return cur.lastrowid
# duplicate check + registered_at timing live in the service/route layer
```

## Rule 3 — Persistence rows stay in the persistence layer
Violation:
```python
row = conn.execute("SELECT * FROM students WHERE id = ?", (sid,)).fetchone()
return jsonify(dict(row))                     # raw snake_case row straight onto the wire
```
Correct:
```python
row = conn.execute("SELECT * FROM students WHERE id = ?", (sid,)).fetchone()
return jsonify(row_to_dict(row))              # mapped to the camelCase wire shape
```

## Rule 4 — Transaction boundary is the caller's
Violation:
```python
def save_document(conn, doc):
    conn.execute("INSERT INTO documents (...) VALUES (...)", ...)
    conn.commit()                             # DAO commits mid-operation; a later
                                              # failure can't roll this back
```
Correct:
```python
def save_document(conn, doc):
    conn.execute("INSERT INTO documents (...) VALUES (...)", ...)  # no commit here
# the request handler owns the unit of work: do all writes, then conn.commit() once
```

## Rule 5 — Scope every query to its owner
Violation:
```python
doc = conn.execute("SELECT * FROM documents WHERE id = ?", (doc_id,)).fetchone()  # any student's
```
Correct:
```python
doc = conn.execute(
    "SELECT * FROM documents WHERE id = ? AND student_id = ?",   # owner-scoped
    (doc_id, student_id),
).fetchone()
```

## Rule 6 — Bound every read; avoid N+1
Violation:
```python
rows = conn.execute("SELECT * FROM students").fetchall()         # whole table...
count = len([r for r in rows if r["program"] == program])        # ...to count in Python
for r in rows:                                                   # N+1
    conn.execute("SELECT * FROM documents WHERE student_id = ?", (r["id"],)).fetchall()
```
Correct:
```python
count = conn.execute(
    "SELECT COUNT(*) FROM students WHERE program = ?", (program,)).fetchone()[0]  # in the DB
rows = conn.execute(
    "SELECT * FROM students ORDER BY id LIMIT ? OFFSET ?", (50, offset)).fetchall()  # bounded
```

## Rule 7 — Keep raw queries parameterized
Violation:
```python
conn.execute(f"SELECT * FROM students WHERE email = '{email}'")   # SQL injection
```
Correct:
```python
conn.execute("SELECT * FROM students WHERE email = ?", (email,))  # bound parameter
```

## Rule 8 — Model relationships deliberately; match existing semantics
Violation:
```python
# turning on enforcement/cascade the app was never written for:
conn.execute("PRAGMA foreign_keys = ON")
conn.execute("DELETE FROM students WHERE id = ?", (sid,))   # now orphan-deletes docs
```                                                         # + on-disk files leak
Correct:
```python
# the schema declares FOREIGN KEY(student_id) but enforcement stays OFF by design;
# documents are a loose reference and are cleaned up explicitly by the app, not by
# cascade. Changing that is a deliberate, called-out migration — not a drive-by.
```

## Rule 9 — Schema changes are additive and non-destructive
Violation:
```python
conn.execute("DROP TABLE students")                          # data loss
conn.execute("CREATE TABLE students (... phone TEXT NOT NULL ...)")  # no default
```
Correct:
```python
cols = [r["name"] for r in conn.execute("PRAGMA table_info(students)")]
if "nickname" not in cols:                                   # add only if missing
    conn.execute("ALTER TABLE students ADD COLUMN nickname TEXT")  # nullable → safe
# existing rows keep their data; no DROP, no RENAME, no NOT-NULL-without-default
```

## Rule 10 — Identity is stable; let the DB assign keys
Violation:
```python
conn.execute("INSERT INTO students (id, ...) VALUES (?, ...)", (chosen_id, ...))  # caller picks PK
```
Correct:
```python
cur = conn.execute("INSERT INTO students (first_name, ...) VALUES (?, ...)", (...,))
new_id = cur.lastrowid          # AUTOINCREMENT assigns it; read it back, don't set it
```

## Rule 11 — Respect the datastore's concurrency limits
Violation:
```python
# many threads writing the same SQLite file → "database is locked" (SQLITE_BUSY)
```
Correct:
```python
conn = sqlite3.connect(DB_PATH)   # a short-lived connection per request, one writer
# keep write transactions short; don't fan out concurrent writers against one file
```

## Rule 12 — Isolate persistence behind a seam
Violation:
```python
@app.route("/api/students")
def list_students():
    conn = sqlite3.connect(DB_PATH)          # driver wiring inline in the handler
    conn.row_factory = sqlite3.Row
    ...
```
Correct:
```python
@app.route("/api/students")
def list_students():
    conn = get_connection()                  # connection concerns behind one helper
    rows = conn.execute("SELECT * FROM students ORDER BY id").fetchall()
    return jsonify([row_to_dict(r) for r in rows])
```
