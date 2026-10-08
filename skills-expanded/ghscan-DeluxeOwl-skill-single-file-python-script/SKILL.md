---
name: single-file-python-script
description: Use this when you need to run a self-contained python script
---

# Single-File Python App

Everything — backend, frontend, database — lives in **one `.py` file**. No project scaffold, no `package.json`, no build step. Just `uv run main.py`.

Reference implementation: `todos.py` adjanced to this file.

---

## 1. File Header & Dependencies

Every file starts with the uv script header. This is how dependencies are declared — uv resolves and installs them automatically on first run.

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "click",
#     "fastapi",
#     "pydantic",
#     "uvicorn",
#     "pytest",
# ]
# ///
```

**Rules:**
- Add dependencies here, not via pip/requirements.txt.
- Use Python's standard library when possible (e.g. `sqlite3` needs no dependency).
- The shebang lets you run the file directly: `chmod +x main.py && ./main.py`.
- Always include `pytest` in dependencies for inline tests (see §6).

---

## 2. Backend Architecture

Organize the Python code in this order, using section comments:

```
# ── Domain ────────────
# ── Repository ────────
# ── Schemas ───────────
# ── API ───────────────
# ── App ───────────────
# ── Inline Tests ──────
# ── CLI ───────────────
```

### 2.1 Domain Model

Plain classes. No framework imports. Business logic only.

```python
class Todo:
    def __init__(self, description: str) -> None:
        self.description = description
        self.done = False

    def toggle_done(self) -> None:
        self.done = not self.done
```

**Rules:**
- Initialize with the minimum required data.
- Only expose public methods that represent domain operations.
- No Pydantic, no SQLAlchemy — keep the domain framework-free.

### 2.2 Repository (Abstract Base Class + Implementation)

Define an ABC contract, then implement it. This keeps the domain decoupled from storage.

```python
from abc import ABC, abstractmethod

class TodoRepository(ABC):
    @abstractmethod
    def add(self, todo: Todo) -> None: ...

    @abstractmethod
    def list_all(self) -> list[Todo]: ...

    @abstractmethod
    def get_by_index(self, index: int) -> Todo: ...
```

**Use `sqlite3`** (standard library) for persistence. No ORM needed for single-file apps.

```python
import sqlite3

class SqliteTodoRepository(TodoRepository):
    def __init__(self, db_path: str = "todos.db") -> None:
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS todos ("
            "  id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "  description TEXT NOT NULL,"
            "  done INTEGER NOT NULL DEFAULT 0"
            ")"
        )
        self._conn.commit()

    def add(self, todo: Todo) -> None:
        cur = self._conn.execute(
            "INSERT INTO todos (description, done) VALUES (?, ?)",
            (todo.description, int(todo.done)),
        )
        self._conn.commit()
        todo._rowid = cur.lastrowid

    def list_all(self) -> list[Todo]:
        rows = self._conn.execute(
            "SELECT id, description, done FROM todos ORDER BY id"
        ).fetchall()
        todos: list[Todo] = []
        for rowid, description, done in rows:
            todo = Todo(description)
            todo.done = bool(done)
            todo._rowid = rowid
            todos.append(todo)
        return todos

    def get_by_index(self, index: int) -> Todo:
        row = self._conn.execute(
            "SELECT id, description, done FROM todos ORDER BY id LIMIT 1 OFFSET ?",
            (index,),
        ).fetchone()
        if row is None:
            raise IndexError(f"No todo at index {index}")
        rowid, description, done = row
        todo = Todo(description)
        todo.done = bool(done)
        todo._rowid = rowid
        return todo

    def save(self, todo: Todo) -> None:
        self._conn.execute(
            "UPDATE todos SET done = ? WHERE id = ?",
            (int(todo.done), todo._rowid),
        )
        self._conn.commit()
```

**Rules:**
- Always use `PRAGMA journal_mode=WAL` for concurrent reads.
- Create tables with `IF NOT EXISTS` in `__init__` — the app bootstraps itself.
- Reconstruct domain objects from rows; don't return raw tuples from the repository.
- Add a `save()` method when mutations need to be persisted back.

### 2.3 Scaling Up: Service Layer

For simple entities like a Todo, endpoints can call the repository directly. But when business logic grows (e.g. validation across multiple entities, side effects, notifications), introduce a **service** that depends on the repository:

```python
class TodoService:
    def __init__(self, repo: TodoRepository) -> None:
        self._repo = repo

    def add(self, description: str) -> Todo:
        # business logic, validation, side effects...
        todo = Todo(description)
        self._repo.add(todo)
        return todo

    def toggle(self, index: int) -> Todo:
        todo = self._repo.get_by_index(index)
        todo.toggle_done()
        self._repo.save(todo)
        return todo
```

The endpoint then calls the service instead of the repo:

```python
service = TodoService(repo)

@api.patch("/todos/{index}/toggle", response_model=TodoResponse)
async def toggle_todo_done(index: int):
    todo = service.toggle(index)
    ...
```

**When to add a service:**
- An endpoint does more than fetch → mutate → save.
- Multiple endpoints share the same business logic.
- You need to coordinate across multiple repositories.

**When you don't need one:** a simple CRUD entity where the endpoint is just glue between schema and repo (like our Todo).

### 2.4 Pydantic Schemas (API Layer)

Separate request and response models. These are the API contract — never return domain objects directly.

```python
from pydantic import BaseModel

class AddTodoRequest(BaseModel):
    description: str

class TodoResponse(BaseModel):
    index: int
    description: str
    done: bool
```

**Rules:**
- Request models contain only what the user provides (e.g. `AddTodoRequest` has only `description`).
- Response models contain what the client needs (including computed fields like `index`).
- These Pydantic models define the shape that the frontend TypeScript types must mirror.

### 2.4 FastAPI Endpoints (APIRouter with `/api` prefix)

Put all endpoints on an `APIRouter` with `prefix="/api"`. This keeps API routes separate from the frontend SPA routes (handled by wouter on the client). The router is included into the app in the App section.

```python
from fastapi import APIRouter, FastAPI, HTTPException

api = APIRouter(prefix="/api")
repo = SqliteTodoRepository()

@api.post("/todos", response_model=TodoResponse, status_code=201)
async def add_todo(body: AddTodoRequest):
    todo = Todo(body.description)
    repo.add(todo)
    index = len(repo.list_all()) - 1
    return TodoResponse(index=index, description=todo.description, done=todo.done)

@api.get("/todos", response_model=list[TodoResponse])
async def list_todos():
    return [
        TodoResponse(index=i, description=t.description, done=t.done)
        for i, t in enumerate(repo.list_all())
    ]

@api.patch("/todos/{index}/toggle", response_model=TodoResponse)
async def toggle_todo_done(index: int):
    try:
        todo = repo.get_by_index(index)
    except IndexError:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.toggle_done()
    repo.save(todo)
    return TodoResponse(index=index, description=todo.description, done=todo.done)
```

**Rules:**
- Always use `APIRouter(prefix="/api")` — never mount endpoints at the root. This avoids conflicts with the SPA catch-all route.
- Endpoints define paths relative to the prefix (e.g. `"/todos"` becomes `/api/todos`).
- Always set `response_model` — it documents the API and validates output.
- Use `status_code=201` for creation endpoints.
- Raise `HTTPException` with a `detail` string — the frontend error handler parses this.
- The flow is: parse request → create/fetch domain object → call domain method → persist → return response.

### 2.5 App & SPA Catch-All

Include the API router, then add a catch-all route that serves the HTML for any non-API path. This lets wouter handle client-side routing — refreshing `/active` or `/done` still works because the server returns the same HTML and wouter picks up the path.

```python
app = FastAPI()
app.include_router(api)

@app.get("/{path:path}", response_class=HTMLResponse)
async def spa(path: str):
    return HTML
```

**Rules:**
- `include_router(api)` must come before the catch-all, so `/api/*` routes are matched first.
- The catch-all `"/{path:path}"` serves the HTML for every other path — wouter reads `window.location` and renders the correct page.

### 2.6 CLI Entrypoint

Use Click for CLI options. The `if __name__` block routes to pytest when the first argument is `test`, otherwise runs the app.

```python
import click
import uvicorn

@click.command()
@click.option("--host", default="0.0.0.0", show_default=True, help="Bind host")
@click.option("--port", default=8765, type=int, help="Bind port")
def main(host: str, port: int | None):
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        import pytest
        sys.exit(pytest.main([__file__] + sys.argv[2:]))
    main()
```

---

## 3. Frontend (Inline HTML)

The entire frontend is a single HTML string assigned to a `HTML` variable in the Python file. It uses CDN-loaded libraries — no bundler, no node_modules.

### 3.1 CDN Stack

All libraries are loaded via `esm.sh` in an import map. Pin React-dependent libraries with `?deps=react@19` to avoid duplicate React instances.

```html
<script type="importmap">
{
  "imports": {
    "react": "https://esm.sh/react@19",
    "react/jsx-runtime": "https://esm.sh/react@19/jsx-runtime",
    "react/jsx-dev-runtime": "https://esm.sh/react@19/jsx-dev-runtime",
    "react-dom": "https://esm.sh/react-dom@19",
    "react-dom/client": "https://esm.sh/react-dom@19/client",
    "shadcn": "https://esm.sh/shadcn-ui-bundled/standalone",
    "@tanstack/react-query": "https://esm.sh/@tanstack/react-query@5?deps=react@19",
    "react-error-boundary": "https://esm.sh/react-error-boundary?deps=react@19",
    "ky": "https://esm.sh/ky",
    "react-hook-form": "https://esm.sh/react-hook-form?deps=react@19",
    "wouter": "https://esm.sh/wouter?deps=react@19"
  }
}
</script>
```

**Libraries and their roles:**
| Library | Purpose |
|---|---|
| React 19 + ReactDOM | UI framework |
| Tailwind CSS v4 | Styling (browser runtime via `<script>` tag) |
| shadcn-ui-bundled/standalone | Pre-built UI components |
| @tanstack/react-query v5 | Server state (`useSuspenseQuery`, `useMutation`) |
| react-error-boundary | Error boundaries for Suspense |
| ky | HTTP client (replaces fetch boilerplate) |
| react-hook-form | Form state & validation |
| wouter | Lightweight client-side routing |
| Babel standalone | In-browser TSX compilation |

**Rules:**
- Always pin `?deps=react@19` on libraries that peer-depend on React.
- `ky` has no React dependency, so no `deps` param needed.
- To add a new library, add it to the import map pointing to `esm.sh`.

### 3.2 Babel TSX Setup

Babel compiles TSX in the browser. This preset block is required:

```html
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<script>
  Babel.registerPreset("tsx-auto", {
    presets: [
      [Babel.availablePresets["react"], { runtime: "automatic" }],
      [Babel.availablePresets["typescript"], { isTSX: true, allExtensions: true }],
    ],
  });
</script>
```

All app code goes in:
```html
<script type="text/babel" data-type="module" data-presets="tsx-auto">
  // your TSX here
</script>
```

### 3.3 Tailwind + shadcn Theme

The `<style type="text/tailwindcss">` block maps Tailwind utilities to CSS custom properties. The `@theme inline` block is **required** for shadcn components to render correctly. See `main.py` for the full theme block.

Available shadcn components (import from `"shadcn"`):
```
Accordion, Alert, AlertDialog, AspectRatio, Avatar, Badge, Breadcrumb,
Button, Calendar, Card, Carousel, Chart, Checkbox, Collapsible, Combobox,
Command, ContextMenu, Dialog, Drawer, DropdownMenu, Empty, Field,
HoverCard, Input, InputGroup, InputOTP, Item, Kbd, Label, Menubar,
NativeSelect, NavigationMenu, Pagination, Popover, Progress, RadioGroup,
Resizable, ScrollArea, Select, Separator, Sheet, Sidebar, Skeleton,
Slider, Spinner, Switch, Table, Tabs, Textarea, Toggle, ToggleGroup,
Tooltip, Toaster
```

---

## 4. Frontend Patterns

Organize the TSX code in this order:

```
// ── Types ──────────
// ── Query keys ─────
// ── API client ─────
// ── Error handling ─
// ── Components ─────
// ── Pages ──────────
// ── App ────────────
```

### 4.1 TypeScript Types (Mirror Pydantic Schemas)

Create TypeScript interfaces that match the Pydantic response models exactly.

```typescript
// Pydantic: TodoResponse(index: int, description: str, done: bool)
interface Todo {
  index: number;
  description: string;
  done: boolean;
}
```

**Rule:** Every Pydantic response model gets a corresponding TS interface. Keep the names aligned.

### 4.2 Query Keys (`as const` Object)

Centralize all TanStack Query cache keys in one object. Provides autocomplete, refactor safety, and a clear inventory.

```typescript
const todoKeys = {
  all: ["todos"] as const,
} as const;
```

Extend as needed: `detail: (id: number) => ["todos", id] as const`.

### 4.3 API Client (ky with prefix)

Create a ky instance with `prefix: "/api"` to match the backend's `APIRouter(prefix="/api")`. Then group all API calls in a single `const` object. ky auto-throws on non-2xx and auto-parses JSON.

```typescript
import ky from "ky";

const api = ky.create({ prefix: "/api" });

const todoClient = {
  list: () => api.get("todos").json<Todo[]>(),
  add: (description: string) =>
    api.post("todos", { json: { description } }).json<Todo>(),
  toggleDone: (index: number) =>
    api.patch(`todos/${index}/toggle`).json<Todo>(),
} as const;
```

**Rules:**
- Always create a ky instance with `prefix: "/api"` — keeps the prefix in one place.
- Client methods use relative paths (e.g. `"todos"` not `"/api/todos"`).
- One client object per domain entity.
- Type the `.json<T>()` call with the matching TS interface.
- Never use raw `fetch` — ky removes all the `res.ok` / `res.json()` boilerplate.

### 4.4 Standardized Error Handling

All backend errors flow through ky's `HTTPError`, which carries the `Response`. FastAPI always returns `{"detail": "..."}` on errors. Build one hook + one component to handle everything.

```typescript
import ky, { HTTPError } from "ky";

function useErrorMessage(error: Error | null): string | null {
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!error) { setMessage(null); return; }

    if (error instanceof HTTPError) {
      error.response
        .json()
        .then((body: any) => setMessage(body?.detail ?? error.message))
        .catch(() => setMessage(error.message));
    } else {
      setMessage(error.message);
    }
  }, [error]);

  return message;
}

function AppErrorMessage({ error, retry }: { error: Error | null; retry?: () => void }) {
  const message = useErrorMessage(error);
  if (!message) return null;

  if (retry) {
    return (
      <Alert variant="destructive" className="my-4">
        <AlertDescription className="flex items-center justify-between">
          <span>{message}</span>
          <Button variant="outline" size="sm" onClick={retry}>Retry</Button>
        </AlertDescription>
      </Alert>
    );
  }

  return <p className="text-sm text-destructive">{message}</p>;
}
```

**Two modes:**
- **With `retry`** → Alert box with retry button. Used as the `ErrorBoundary` fallback for queries.
- **Without `retry`** → Inline destructive text. Used under forms and mutation triggers.

### 4.5 Data Fetching (useSuspenseQuery + Suspense + ErrorBoundary)

Wrap data-fetching components in `<Suspense>` + `<ErrorBoundary>`. Use `useSuspenseQuery` — it suspends until data is ready, so `data` is never `undefined`.

```tsx
import { useSuspenseQuery, useQueryClient } from "@tanstack/react-query";
import { ErrorBoundary } from "react-error-boundary";

function TodoList() {
  const { data: todos } = useSuspenseQuery({
    queryKey: todoKeys.all,
    queryFn: todoClient.list,
  });
  // data is always Todo[] here, never undefined
  return ( /* render todos */ );
}

function ErrorFallback({ error, resetErrorBoundary }) {
  return <AppErrorMessage error={error} retry={resetErrorBoundary} />;
}

// In the parent:
<ErrorBoundary FallbackComponent={ErrorFallback}>
  <Suspense fallback={<LoadingFallback />}>
    <TodoList />
  </Suspense>
</ErrorBoundary>
```

### 4.6 Mutations (useMutation + Error Display)

Every mutation invalidates the relevant query key on success and displays errors via `AppErrorMessage`.

```tsx
import { useMutation } from "@tanstack/react-query";

function TodoItem({ todo }: { todo: Todo }) {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: () => todoClient.toggleDone(todo.index),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: todoKeys.all });
    },
  });

  return (
    <div>
      <Checkbox
        checked={todo.done}
        disabled={mutation.isPending}
        onCheckedChange={() => mutation.mutate()}
      />
      <span>{todo.description}</span>
      <AppErrorMessage error={mutation.error} />
    </div>
  );
}
```

**Rules:**
- Always invalidate queries on success — don't manually update the cache in simple apps.
- Always render `<AppErrorMessage error={mutation.error} />` near the trigger.
- Disable the trigger while `mutation.isPending`.

### 4.7 Forms (react-hook-form)

Use `useForm` for form state. Combine with `useMutation` for submission.

```tsx
import { useForm } from "react-hook-form";

interface AddTodoFields {
  description: string;
}

function AddTodoForm() {
  const { register, handleSubmit, reset, formState: { isValid } } = useForm<AddTodoFields>({
    defaultValues: { description: "" },
  });
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: todoClient.add,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: todoKeys.all });
      reset();
    },
  });

  const onSubmit = ({ description }: AddTodoFields) => {
    mutation.mutate(description.trim());
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Input
        {...register("description", { required: true, validate: (v) => v.trim().length > 0 })}
        disabled={mutation.isPending}
      />
      <Button type="submit" disabled={mutation.isPending || !isValid}>
        {mutation.isPending ? "Adding…" : "Add"}
      </Button>
      <AppErrorMessage error={mutation.error} />
    </form>
  );
}
```

**Rules:**
- Define an interface for form fields (mirrors the request body shape).
- Use `register` with validation rules — don't manually manage `onChange`/`useState`.
- Call `reset()` on mutation success.
- Disable inputs while `mutation.isPending`.

### 4.8 Client-Side Routing (wouter)

Use wouter for lightweight client-side routing. Import `Switch` as `RouteSwitch` to avoid conflicts with other components.

```tsx
import { Switch as RouteSwitch, Route, Link, useLocation } from "wouter";
```

**Pages** are components that compose the shared layout with route-specific content:

```tsx
function TodoPage({ filter }: { filter: "all" | "active" | "done" }) {
  return (
    <div className="flex flex-col gap-4">
      <AddTodoForm />
      <Separator />
      <NavBar />
      <ErrorBoundary FallbackComponent={ErrorFallback}>
        <Suspense fallback={<LoadingFallback />}>
          <TodoList filter={filter} />
        </Suspense>
      </ErrorBoundary>
    </div>
  );
}

function NotFound() {
  const [, navigate] = useLocation();
  return (
    <div className="flex flex-col items-center gap-4 py-8">
      <p className="text-4xl font-bold">404</p>
      <p className="text-muted-foreground">Page not found</p>
      <Button variant="outline" onClick={() => navigate("/")}>Go home</Button>
    </div>
  );
}
```

**Navigation** uses `Link` and `useLocation` for active state:

```tsx
function NavBar() {
  const [location] = useLocation();

  const links = [
    { href: "/", label: "All" },
    { href: "/active", label: "Active" },
    { href: "/done", label: "Done" },
  ] as const;

  return (
    <nav className="flex gap-2">
      {links.map(({ href, label }) => (
        <Link key={href} href={href}>
          <Badge
            variant={location === href ? "default" : "outline"}
            className="cursor-pointer"
          >
            {label}
          </Badge>
        </Link>
      ))}
    </nav>
  );
}
```

**Rules:**
- Define pages in a `// ── Pages ──` section, between Components and App.
- Each route renders a page component — don't inline complex JSX in `<Route>`.
- Always include a catch-all `<Route>` for 404.
- Navigation state (active link) comes from `useLocation()`, not manual state.

### 4.9 App Shell (QueryClientProvider + Router)

Wrap the root in `QueryClientProvider`. Routes go inside the layout shell. wouter doesn't need a provider — it uses `window.location` by default.

```tsx
const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1 },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen flex items-center justify-center p-4">
        <Card className="w-full max-w-lg">
          <CardHeader>
            <CardTitle>Todos</CardTitle>
            <CardDescription>A simple todo list backed by FastAPI</CardDescription>
          </CardHeader>
          <CardContent>
            <RouteSwitch>
              <Route path="/">{() => <TodoPage filter="all" />}</Route>
              <Route path="/active">{() => <TodoPage filter="active" />}</Route>
              <Route path="/done">{() => <TodoPage filter="done" />}</Route>
              <Route><NotFound /></Route>
            </RouteSwitch>
          </CardContent>
        </Card>
      </div>
    </QueryClientProvider>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
```

**Rules:**
- `RouteSwitch` renders only the first matching route (like a switch statement).
- The catch-all `<Route>` (no path) must be last — it handles 404s.
- The backend's SPA catch-all (`/{path:path}`) ensures refreshing any route serves the HTML, and wouter picks up the path client-side.

---

## 5. Running

```bash
uv run main.py                  # starts on 0.0.0.0:8765
uv run main.py --port 3000      # custom port
```

No install step. uv handles everything.

---

## 6. Inline Tests

Every single-file app includes inline tests. Because `uv run pytest main.py` ignores inline metadata, the test runner is built into the script itself — pytest is listed in the script's dependencies and invoked via a CLI argument.

### 6.1 Pattern

Add `pytest` to the inline dependencies, write `test_*` functions alongside your code, and route to pytest from the `__main__` block:

```python
# /// script
# dependencies = [
#   "requests",
#   "pytest",
# ]
# ///
import requests

def fetch_data():
    return requests.get("https://httpbin.org/ip").status_code

# ── Inline Tests ──────────────────────────────────────────────────

def test_fetch_data():
    assert fetch_data() == 200

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        import pytest
        sys.exit(pytest.main([__file__] + sys.argv[2:]))
    print(f"Status: {fetch_data()}")
```

Run them:

```bash
uv run main.py test             # run all inline tests
uv run main.py test -v          # verbose output
uv run main.py test -k toggle   # run only tests matching "toggle"
```

### 6.2 What to Test

- **Domain logic** — business rules, state transitions (e.g. `Todo.toggle_done()`).
- **Repository** — CRUD operations using `:memory:` SQLite so tests are instant and isolated.
- **Pure functions** — any utility/helper functions.

```python
# ── Inline Tests ──────────────────────────────────────────────────

def test_todo_toggle():
    todo = Todo("Buy milk")
    assert not todo.done
    todo.toggle_done()
    assert todo.done

def test_repo_add_and_list():
    repo = SqliteTodoRepository(db_path=":memory:")
    repo.add(Todo("First"))
    repo.add(Todo("Second"))
    assert len(repo.list_all()) == 2

def test_repo_toggle_and_save():
    repo = SqliteTodoRepository(db_path=":memory:")
    repo.add(Todo("Task"))
    todo = repo.get_by_index(0)
    todo.toggle_done()
    repo.save(todo)
    assert repo.get_by_index(0).done
```

**Rules:**
- Place tests in a `# ── Inline Tests ──` section, between the App section and the CLI entrypoint.
- Use `:memory:` for SQLite repos in tests — no cleanup needed, fully isolated.
- Keep `pytest` as a lazy import inside the `__main__` block so it's not loaded during normal app startup.
- Always add at least domain + repository tests when creating a new app.
