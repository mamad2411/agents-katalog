---
name: add-slice
description: Use when the task adds a feature to this Avero application, such as a new resource, a new set of routes or a new table. It writes the module, the model, the input types, the handlers, the store, the test and the first migration, and it registers the module.
---

# Add a feature slice

One slice holds the routes, the handlers, the input types, the store and the
tests of one feature. A slice imports no other slice.

## Steps

1. Write the slice with the command:

   ```
   avero slice <name>
   ```

   The command writes `internal/features/<name>s/`, its model package, its
   first migration and its test. It adds the slice to `drel.yaml`, and it
   registers the module in `wire.go`.

2. Read `internal/features/<name>s/module.go`. Change the routes to the ones
   that the task states.

3. Change the input types in `input.go`. Give each field its source tag
   (`path`, `query`, `form` or `json`) and its `validate` tag. Run
   `avero generate` after each change.

4. Change the handlers in `handlers.go`. A handler has the shape
   `func (m *Module) Name(c *avero.Ctx, in Input) (View, error)`. A handler
   returns the thing that it answers, and the description of the API reads the
   type. A POST answers 201 and every other method answers 200. Write
   `c.Status(code)` for another status, and `avero.NoBody` for no body. A
   handler never writes to the ResponseWriter.

   Answer a failure with a problem, such as `avero.NotFound("<name>", in.ID)`.
   The router writes the document that RFC 9457 states. Do not write a map of
   one string.

   Register a route with `avero.Get(r, "/<name>s", m.List)`, which reads the
   types of the handler. State a further answer with an option, such as
   `avero.Answers[avero.Problem](404, "the <name> does not exist")`.

5. Change the row in `model/<name>.go`. A `db` tag names the column. Run
   `avero generate`, which writes the columns and the repository.

6. Change the store in `store.go`. It reads with `avero.Repo` and writes with
   `avero.Save`, and it reads with the typed API of drel, such as
   `repo.Where(model.<Name>s.Title.Contains(q)).All(ctx)`. Write no SQL
   string. Every call runs inside the transaction of the request.

7. Write the change of the table:

   ```
   avero migrate new <what_changed>
   avero migrate up
   ```

   drel compares the model with its snapshot and writes the two SQL files in
   `internal/features/<name>s/migrations/`. Read them before you apply them.

   The module states its own migrations through a `Migrations` method that
   returns the embedded file system of the slice. `avero.Serve` reads the
   migration files of the application from the module set. `wire.go` needs no
   change for a migration.

8. For a page, write the view in `internal/ui/`. The view reads the old input
   with `view.Old` and the field error with `view.Error`. `internal/ui`
   imports no feature package.

## Rules

- Write the test before the code that it judges.
- A feature does not import another feature.
- Never edit a file that starts with `zz_generated`. Change the input type and
  run `avero generate`.

## The command that proves the work

```
avero verify
```
