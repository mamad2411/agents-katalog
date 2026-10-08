---
name: extension-oql
description: Make a canister's data queryable by the Caffeine Data Intelligence agent. Use whenever an app stores structured data (Maps/Lists/arrays of records) that should be answerable in natural language — "top customers", "revenue by region", "active projects". Adds a discoverable `schema()` and a JSON `execute()` query endpoint via the `caffeineai-oql` mops package's `Expose` mixin.
version: 0.6.2
compatibility:
  mops:
    caffeineai-oql: "~0.6.1"
caffeineai-subscription: [none]
---

# OQL — Object Query Layer

Go over the actor's fields (non-transient) and, for each collection worth querying,
consider how its data maps to a **table** in a database (an *entity*). You only
declare one entity per table — the `Expose` mixin makes them queryable.

# Backend

Each entity carries an authorization level; the default `.controllerOnly()` is
safe (private to users, still readable by the Data Intelligence agent). Model
your entities first, then pick a level per entity — see `## Auth`.

## Setup

Run `mops add caffeineai-oql@0.6.1` in the **same write batch** as your first
`mo:caffeineai-oql/...` import. Auto-derivation requires `moc >= 1.11` (the
generated-app template already satisfies this).

### Build flags

`--default-persistent-actors` is mandatory. `--implicit-package=core` is
optional convenience; every snippet and source file must import the `mo:core`
modules it uses. If the app uses `OQL.Table` and needs more than 4 GiB of
`Region`, add `--max-stable-pages 1638400` as well; a dependency's own flags are
not applied to the project that depends on it, so it has to be set in the app's
own build.

### Imports — one per resolver module

`.toEntity`, the builder chain (`.sample` / `.build` / `.public_` / …), and record
`_toRow` derivation are resolved from modules **imported top-level in the file
that declares entities** — the resolver does not walk submodules, so importing
only `mo:caffeineai-oql` is not enough. Import exactly the resolver modules your
code uses:

- `mo:caffeineai-oql/Entity` — always (the `.sample` / `.build` / `.edge` /
  `.ownedBy` / auth-level builder chain, and `.payload` / `.flatten` in manual mode).
- the collection module for each `.toEntity` / `.toEntityManual` receiver —
  `MapEntity`, `SetEntity`, `ListEntity`, `ArrayEntity`, or `VarArrayEntity`.
- for each **auto-derived** (`.toEntity`) record: `RecordValue`, plus one
  `<Type>Value` per primitive field type present — `NatValue`, `TextValue`,
  `PrincipalValue`, `BoolValue`, `IntValue`, `FloatValue`, the sized `Nat`/`Int`
  widths, `BlobValue`. Manual `.payload` return types need their `<Type>Value`
  too; manual-only entities need no `RecordValue`.

When a collection module is missing the compiler names it — *"field toEntity does
not exist … Did you mean to import mo:caffeineai-oql/MapEntity?"* — add the named
import. A missing `Entity` import gets no such hint: it surfaces as a bare
*"field payload does not exist in type Builder<…>"* (M0072). Treat any
`field <builderMethod> does not exist` error as a missing top-level import from
this list, never as a wrong package version.

## Declare entities and install

`.toEntity(name, typeName, primaryKey)` turns a collection of records into a
queryable entity; the compiler auto-derives the fields. Each entity sets its own
authorization level (see `## Auth`); the example below shows one table per level.
`Expose` adds only the OQL query methods (`schema` / `execute`) — your existing
state, types, and `shared` methods are untouched.

- Always call `.sample({...})` on every `.toEntity` / `Entity.manual` chain; dummy values are fine. Empty collection + no sample → empty schema (`fields: []` / `"record { }"`).

<!-- motoko-check:skip -->
```motoko filepath=src/backend/sample_required.mo
include Expose({ entities = [tasks.toEntity("task", "Task", "id").sample({ id = 0; title = "" }).public_().build()] })
```

```motoko filepath=src/backend/main.mo
import Map       "mo:core/Map";
import Nat       "mo:core/Nat";
import Principal "mo:core/Principal";
import OQL       "mo:caffeineai-oql";
import Expose    "mo:caffeineai-oql/Expose";
// Resolver modules, imported top-level (see "Imports" above). This app derives
// Map entities over records of Nat / Text / Principal fields:
import MapEntity      "mo:caffeineai-oql/MapEntity";
import Entity         "mo:caffeineai-oql/Entity";
import RecordValue    "mo:caffeineai-oql/RecordValue";
import NatValue       "mo:caffeineai-oql/NatValue";
import TextValue      "mo:caffeineai-oql/TextValue";
import PrincipalValue "mo:caffeineai-oql/PrincipalValue";

actor {
  type Product  = { id : Nat; name : Text; priceUsd : Nat };
  type Vendor   = { id : Nat; name : Text };
  type AuditLog = { id : Nat; action : Text; atNs : Nat };
  type Note     = { id : Nat; user : Principal; body : Text };
  type Document = { id : Nat; owner : Principal; title : Text; ciphertext : Text };
  type User     = { id : Principal; isAdmin : Bool };

  let products  : Map.Map<Nat, Product>;
  let vendors   : Map.Map<Nat, Vendor>;
  let supplies  : Map.Map<Product, Vendor>;
  let auditLogs : Map.Map<Nat, AuditLog>;
  let notes     : Map.Map<Nat, Note>;
  let documents : Map.Map<Nat, Document>;
  // not all collections need to be exposed if there is no need — `users` backs
  // auth only, so it is intentionally never turned into an entity below
  let users     : Map.Map<Principal, User>;

  transient let anyP = Principal.fromText("aaaaa-aa");   // sample owner; the value is ignored

  // Look up whether a caller is an admin.
  func isAdmin(p : Principal) : Bool =
    switch (users.get(p)) { case (?u) u.isAdmin; case null false };

  // A custom .ownedByWith rule: admins see every document, everyone else only
  // their own. `owner` is the field's Value — a Principal column arrives as #text.
  func canSeeDocument(caller : Principal, owner : OQL.Value) : Bool =
    isAdmin(caller) or owner == #text(caller.toText());

  include Expose({
    entities = [
      // #public_ — anyone, incl. anonymous, reads the whole catalogue
      products.toEntity("product", "Product", "id")
        .sample({ id = 0; name = ""; priceUsd = 0 })
        .public_()
        .build(),
      vendors.toEntity("vendor", "Vendor", "id")
        .sample({ id = 0; name = "" })
        .public_()
        .build(),
      // `supplies : Map<Product, Vendor>` — a map between two non-primitive types.
      // The identity lives in the key/value records, not a field, so iterate
      // .entries() in manual mode, promote each side's id, and .edge both — a
      // query can then traverse "product.name" and "vendor.name".
      OQL.Entity.manual<(Product, Vendor)>("supply", func () = supplies.entries(), "Supply", "key")
        .sample(({ id = 0; name = ""; priceUsd = 0 }, { id = 0; name = "" }))
        .payload("key",     func ((p, v)) = p.id.toText() # ":" # v.id.toText())
        .payload("product", func ((p, _)) = p.id) .edge("product", "product")
        .payload("vendor",  func ((_, v)) = v.id) .edge("vendor",  "vendor")
        .controllerOnly()
        .build(),
      // #controllerOnly (the default, shown explicitly) — only the platform reads
      auditLogs.toEntity("auditLog", "AuditLog", "id")
        .sample({ id = 0; action = ""; atNs = 0 })
        .controllerOnly()
        .build(),
      // #scopedPerUser — each signed-in user reads only their own rows
      notes.toEntity("note", "Note", "id")
        .sample({ id = 0; user = anyP; body = "" })
        .ownedBy("user")
        .scopedPerUser()
        .build(),
      // #controllerOrScoped — controller reads all; scoped reads use canSeeDocument.
      // `.hidden` — opaque column absent from schema + default projection
      documents.toEntity("document", "Document", "id")
        .sample({ id = 0; owner = anyP; title = ""; ciphertext = "" })
        .hidden("ciphertext")
        .ownedByWith("owner", canSeeDocument)
        .controllerOrScoped()
        .build(),
    ];
  });
}
```

The migration chain head:

```motoko filepath=src/backend/migrations/00000000_000000.mo
import Map "mo:core/Map";

module {
  type Product  = { id : Nat; name : Text; priceUsd : Nat };
  type Vendor   = { id : Nat; name : Text };
  type AuditLog = { id : Nat; action : Text; atNs : Nat };
  type Note     = { id : Nat; user : Principal; body : Text };
  type Document = { id : Nat; owner : Principal; title : Text; ciphertext : Text };
  type User     = { id : Principal; isAdmin : Bool };

  type NewActor = {
    products  : Map.Map<Nat, Product>;
    vendors   : Map.Map<Nat, Vendor>;
    supplies  : Map.Map<Product, Vendor>;
    auditLogs : Map.Map<Nat, AuditLog>;
    notes     : Map.Map<Nat, Note>;
    documents : Map.Map<Nat, Document>;
    users     : Map.Map<Principal, User>;
  };

  public func migration(_old : {}) : NewActor {
    {
      products  = Map.empty<Nat, Product>();
      vendors   = Map.empty<Nat, Vendor>();
      supplies  = Map.empty<Product, Vendor>();
      auditLogs = Map.empty<Nat, AuditLog>();
      notes     = Map.empty<Nat, Note>();
      documents = Map.empty<Nat, Document>();
      users     = Map.empty<Principal, User>();
    };
  };
};
```

## Auth

Authorization is **per entity** — each builder declares a level, and `schema()`
and `execute()` both run the check against the live `caller`. No app-wide config,
no tokens. The default when none is set is `#controllerOnly`.

| Builder call | Who reads | Rows returned |
|---|---|---|
| `.public_()` | anyone (incl. anonymous) | all |
| `.controllerOnly()` *(default)* | controllers only | all |
| `.scopedPerUser()` | any signed-in caller | only the caller's own |
| `.controllerOrScoped()` | controllers + signed-in callers | controller: all; user: own |

### Choosing a level

Pick per entity by who should read its rows — when in doubt, keep the default.

- **`.controllerOnly()`** *(default)* — private app data the agent should answer
  over, but no end user reads directly (orders, metrics, audit logs, config). The
  agent calls as the controller, so it reads everything while the data stays
  private to users.
- **`.public_()`** — world-readable data, including logged-out visitors (public
  catalogue, published content, leaderboards).
- **`.controllerOrScoped()`** — per-user data where each user reads only their own
  rows, but the agent must still answer aggregate questions (profiles, a user's
  orders). Requires an owner column.
- **`.scopedPerUser()`** — strictly private per-user data: each user reads only
  their own, and the agent is scoped too, so it **cannot** answer over this table
  (DMs, private journals). Requires an owner column — prefer
  `.controllerOrScoped()` unless the agent must be blind to it.

The user may override per entity; if a request implies per-user data but is
ambiguous, ask.

### Per-user (row-level) scoping

Scoped levels (`.scopedPerUser()`, `.controllerOrScoped()`) need a way to know
which rows belong to the caller — an **owner column** or a subject-honouring
source. `.build()` traps if a scoped entity has neither, and also traps if a
`.public_()` entity declares an owner (the check would never run). This is the
guardrail against the common data-leak footgun.

**When to tag:** a `Principal` field is the signal.

- `.ownedBy(field)` — the field *is* the owner; visibility is identity equality.
- `.ownedByWith(field, canSee)` — custom visibility (teams, admins, sharing).
  `canSee : (caller : Principal, owner : Value) -> Bool` decides per row; `field`
  need not be a `Principal`, and the closure can read actor state.

A scoped caller sees only its owned rows — both as the query target and through a
join — so traversal can never leak another owner's rows.

```mo
// Per-user notes: each signed-in user reads only their own rows.
notes.toEntity("note", "Note", "id")
  .sample({ id = 0; owner = Principal.fromText("aaaaa-aa") /* any principal */; body = "" })
  .ownedBy("owner")
  .scopedPerUser()
  .build()

// .ownedByWith custom rule: the owner sees their own docs, listed admins see
// everyone's, and the platform controller sees all (#controllerOrScoped).
// `owner` is the field's Value — a Principal column arrives as #text(principal).
docs.toEntity("doc", "Doc", "id")
  .sample({ id = 0; owner = Principal.fromText("aaaaa-aa"); title = "" })
  .ownedByWith("owner", func (caller, owner) =
    admins.get(caller) != null or owner == #text(caller.toText()))
  .controllerOrScoped()
  .build()
```

Where ownership decides **which** rows a scoped caller sees, `.viewWith(view)`
decides what **shape** it sees them in — a per-subject redaction that runs only
on rows the ownership check already admitted:

```mo
// Everyone sees their own bookings; exact amounts only on their own rows is
// not needed here — but coarsen the contact field for non-owners of a shared
// calendar, say:
bookings.toEntity("booking", "Booking", "id")
  .sample({ id = 0; calendarId = 0; contact = "" })
  .ownedByWith("calendarId", canSeeCalendar)
  .viewWith(func (subject, b) = if (isOwner(subject, b)) b else { b with contact = "" })
  .scopedPerUser()
  .build()
```

`view : (subject : Principal, row : T) -> T` reshapes the typed row; the whole
query pipeline (filters included) evaluates the VIEWED row, so a predicate can
never probe a value the view hides. Views run for scoped subjects only —
pairing `.viewWith` with `.public_()` traps at `.build()` (unrestricted reads
always see raw rows).

`.ownedBy(f)` is exactly `.ownedByWith(f, OQL.Entity.ownerIsCaller)`. At most one
owner column; it must be a real field, not also `.edge` / `.hidden`. For
owner-keyed storage (`Map<Principal, List<T>>`) use
`OQL.Entity.newScoped(name, scopedIter, typeName, primaryKey)` so the scan is
O(user rows): `scopedIter(?p)` returns only `p`'s rows, `scopedIter(null)` all
(schema seeding).

## Entity builder

Two modes, picked by the row type `T`.

### Auto-derivation — `.toEntity`

For records whose fields are all primitives with a built-in `_toRow` (`Nat`,
`Int`, `Float`, `Text`, `Bool`, the sized `Nat`/`Int` widths, `Principal`):

```mo
customers.toEntity(name, typeName, primaryKey)
  .sample(template)              // REQUIRED — empty collection + no sample → empty schema
  .edge(field, targetEntity)     // tag an existing field as a foreign key
  .ownedBy(field)                // (or .ownedByWith(field, canSee)) per-user scoping
  .scopedPerUser()               // auth level: .public_ / .controllerOnly (default) / .scopedPerUser / .controllerOrScoped
  .hidden(field)                 // opaque/sensitive — drop from schema + default projection
  .build()
```

- `.toEntity` is sugar for `OQL.Entity.new<T>(name, func () = coll.values(), …)`;
  it exists on `Map`, `Set`, `List`, `[T]`, and `[var T]`. It iterates **values
  only** — if a row's identity (PK or owner) lives in the *Map key*, it is not a
  field: promote it via manual mode over `.entries()`, or `OQL.Entity.newScoped`
  when it's the owner.
- `primaryKey`, and any `.edge` / `.ownedBy` field, must name a real,
  non-`.hidden` column of the row.
- `.edge(name, target)` tags an **existing** field (it does not add one) as an FK,
  enabling dotted-path traversal `"name.targetField"` in queries. FK/PK types
  must be `Text`, `Nat`/`Int`, or `Bool` (`Float` keys are rejected), and the
  target's primary key must not be `.hidden`.
- **The edge target must be an entity registered in THIS canister's `Expose`.**
  An edge to an absent entity (a typo, or an FK into another canister) silently
  drops the whole field from `schema()` — the column still stores and filters,
  but no schema-driven client can discover it. A cross-canister FK belongs as a
  plain payload field, not an `.edge`.
- `.sample(template)` seeds schema discovery. Always call it; without it an
  empty collection yields an empty schema (`fields: []`). Only the shape
  matters, not the values.
- `.hidden(name)` drops a derivable field from schema + default projection; it
  does **not** skip `_toRow` — unsupported field types still need manual mode or
  a `<Type>Value`.

Schema fields are listed in **lexicographic order** (the `__record` combiner's
canonical form); sort client-side if display order matters.

### Manual mode — `.toEntityManual` / `OQL.Entity.manual`

For non-record `T`, computed fields, or records with nested / variant / option /
collection fields:

```mo
// REQUIRED, top-level in this file — `.payload` / `.flatten` are Entity
// functions reached by receiver notation, not fields of the builder:
import Entity "mo:caffeineai-oql/Entity";

authors.toEntityManual<Author>("author", "Author", "id")
  .sample({ id = 0; name = ""; address = { street = ""; city = "" }; tags = [] })
  .payload("name", func a = a.name)        // one field; extract returns a _toRow value
  .flatten(func a = a.address)             // splice a nested record's fields as columns
  .payload("tagCount", func a = a.tags.size())
  // .edge tags a declared column; .hidden drops one you already added via
  // `.payload` / `.flatten` — omit fields by not adding them
  .build()
```

**`field payload does not exist in type Builder<…>` (M0072) means the `Entity`
import above is missing — it is never a package-version problem.** `.payload`
and `.flatten` have been `Entity` functions since 0.1.0; `mops add`-ing a
different `caffeineai-oql` version will not fix this error. Importing only
`mo:caffeineai-oql` is not enough, and neither is reaching the module through
the `OQL.Entity.…` re-export: receiver notation resolves against **top-level
imports** only, so a file that calls `OQL.Entity.manual(...).payload(...)`
still needs its own `import Entity "mo:caffeineai-oql/Entity";`. Unlike
`.toEntity`, this failure carries no "Did you mean to import …?" hint.

- `.payload(name, extract)` — `name` must not contain `.`. Prefer
  `func r = r.field` (let Motoko infer; avoid redundant annotations). For
  options/variants, return `Text`/`Nat` with a sentinel (see below).
- `.flatten(extract : T -> S)` — `S` must be flat; each of its fields becomes a
  top-level column. Drop unwanted ones with `.hidden`. Name collisions get
  `__1`, `__2` suffixes (nothing is dropped).
- `OQL.Entity.manual<T>(name, iter, typeName, primaryKey)` for arbitrary row
  sources (custom flatteners, filtered iterators). Always chain `.sample(...)`
  with one dummy row of type `T`. The qualified call resolves through the
  `OQL` import, but any `.payload` / `.flatten` chained onto its result still
  needs the top-level `Entity` import.

`OQL.Value` is `{ #null_; #bool; #nat; #int; #float; #text }`. Numeric variants
compare across each other, so a JSON integer threshold matches a `Float` value.

| Row type `T` | Mode |
|---|---|
| All-primitive record | `.toEntity` |
| Record with `?` / variant / nested field | `.toEntity` once you ship `<Type>Value.mo` (below); else manual |
| Record with a collection field | manual — `.size()` or `Text.join` into a payload |
| Tuple / primitive / computed | manual |

## Converting non-primitive fields

To keep a record on the auto-derive path, give each non-primitive field type a
`_toRow : T -> OQL.Value`: one file per type named `<TypeName>Value.mo`, a single
`public func _toRow`, imported **top-level** in the file that declares entities —
the same top-level rule as the built-in value modules (see `## Setup` → Imports);
the resolver does not walk submodules. Parent records then ride `.toEntity(...)`
with no per-field `.payload`.

```mo
// OptTextValue.mo — option → sentinel
module { public func _toRow(self : ?Text) : OQL.Value =
  switch self { case null { #text("") }; case (?t) { #text(t) } }; };

// StatusValue.mo — variant → tag text
module { public func _toRow(self : Status) : OQL.Value =
  #text(switch self { case (#draft) "draft"; case (#published) "published" }); };

// DepartmentValue.mo — nested record → child PK (then .edge the field)
module { public func _toRow(self : Department) : OQL.Value = #text(self.name); };
```

**Always return ONE `Value` variant**, even for null (sentinel `""` / `0` /
`false`) — a `_toRow` that sometimes returns `#null_` makes the reported schema
type flip-flop by row order. Sentinels keep the field queryable (`eq value ""`
matches the nulls). For a one-off field, inline the same conversion in a
`.payload` instead of a module; lift to a module only when 2+ entities need it.
A record used both as an entity and as a nested field just ships its
`<Type>Value.mo` — the structural `Row` derivation and your `Value` collapse are
distinct types and coexist.

## Entity patterns beyond one-row-per-record

The same storage can back several entities — pick what the client should see:

- **reshaped** — flatten `Map<K1, Map<K2, V>>` into rows; have the flattener emit
  a flat **record** (not a tuple) so it still auto-derives, then `.edge` the
  promoted keys.
- **enumerated** — derive an entity from index keys (`Map<Author, …>.keys()`) via
  `OQL.Entity.manual`; entries with no rows simply don't appear.
- **synthetic** — project a junction from an array field to make a many-to-many
  queryable from both sides:

```mo
OQL.Entity.manual<(Article, Text)>("articleTag", func () = flattenTags(articles), "Pair", "pair")
  .sample(({ id = 0 }, ""))
  .payload("article", func ((a, _)) = a.id) .edge("article", "article")
  .payload("tag",     func ((_, t)) = t)    .edge("tag", "tag")
  .build()
```

## Larger data — `OQL.Table`

For a table expected to grow large (tens of thousands of rows and up — events,
transactions, logs, imported datasets), store it in an `OQL.Table`. It scales
far past what heap collections hold; rows are keyed by their append position.

Declaring one is three decisions — **columns, indexes, row function**:

```motoko filepath=src/backend/tables_demo.mo
import OQL    "mo:caffeineai-oql";
import Expose "mo:caffeineai-oql/Expose";
import Entity "mo:caffeineai-oql/Entity";   // the builder chain — always import
import Table  "mo:caffeineai-oql/Table";

actor {
  type Event = { kind : Nat; amount : Nat; note : Text };

  // decisions 1 + 2 (columns, indexes) are fixed where `Table.new` runs —
  // the migration chain entry below
  let events : Table.Table;

  // 3. Row function: your record → one (name, Value) per column, names matching.
  func eventRow(e : Event) : [(Text, OQL.Value)] =
    [("kind", #nat(e.kind)), ("amount", #nat(e.amount)), ("note", #text(e.note))];

  // Writes: the returned position is the row's primary key.
  // A modify is delete + append.
  public func addEvent(e : Event) : async Nat {
    Table.append(events, e, eventRow);
  };

  // REQUIRED: register the table's entity in the Expose mixin — schema() and
  // execute() only see what Expose registers; a Table that is not in this list
  // exists but is invisible to every query. Same list, same auth levels, and
  // FK edges to other entities, as for any entity. `entity` defaults the type
  // name to the entity name and the primary key to "id";
  // `entityWith(events, "event", "Event", "id")` overrides either.
  include Expose({
    entities = [
      Table.entity(events, "event").public_().build(),
      // ... the app's other entities ...
    ];
  });
};
```

`Table.new` runs in the migration chain entry that introduces the table:

<!-- motoko-check:skip -->
```motoko
import Table "mo:caffeineai-oql/Table";

module {
  public func migration(_old : {}) : { events : Table.Table } {
    {
      // 1. Columns: (name, type) pairs. Order matters and the set is FIXED for
      //    the table's life. Types: #nat / #int / #float / #bool (64-bit cells) + #text.
      // 2. Indexes: the columns queries will filter or order by —
      //    #hash for equality, #ordered for ranges / orderBy.
      events = Table.new(
        [("kind", #nat), ("amount", #nat), ("note", #text)],   // columns
        [("kind", #hash), ("amount", #ordered)],               // indexes
      );
    };
  };
};
```

Rules that matter:

- **The schema is fixed once data is flushed** — no adding, dropping, or
  retyping columns; a different shape means a new table.
- **A value's kind must equal its column's type** — a mismatch traps loudly at
  `append` rather than storing corrupt cells; numeric cells are 64-bit.
- **A table that will be bulk-loaded is declared with NO indexes** — index
  after the load (next section).
- **A `Table` is queryable only through its entity in `Expose`** — declaring
  the table alone stores data but exposes nothing; `schema()` / `execute()`
  see exactly the `entities` list.

Beyond what the index serves, a `Table` answers whole-column **`sum` / `avg`
straight from segment stats** — flat in table size — and reads only the columns
a query touches.

## Bulk upload (`ImportData`) — load existing data into a `Table`

When the user's data already exists (a CSV export from a spreadsheet or the
system the app replaces), don't trickle it through `append` — include the
`ImportData` mixin and load it as pre-built **segment images**: the loader lays
rows out off-chain in exactly a flushed segment's byte layout and the canister
validates and copies the bytes, so one message costs O(columns) instead of
O(rows), and the heap stays flat throughout.

```motoko filepath=src/backend/bulk_load_demo.mo
import Expose     "mo:caffeineai-oql/Expose";
import Entity     "mo:caffeineai-oql/Entity";   // the builder chain — always import
import Table      "mo:caffeineai-oql/Table";
import ImportData "mo:caffeineai-oql/ImportData";

actor {
  // Declare the table INDEX-FREE for the load — loadSegment traps on a table
  // that declares an index (a ready index missing the loaded rows would
  // silently under-fetch). The index is built after the load, in the background.
  // Constructed in the migration chain entry that introduces it:
  //   events = Table.new([("kind", #nat), ("amount", #nat), ("note", #text)], []);
  let events : Table.Table;

  include Expose({
    entities = [
      Table.entity(events, "event").public_().build(),
      // ... the app's other entities ...
    ];
  });
  include ImportData([ events.importTarget("event") ]);
};
```

The mixin adds **controller-only** endpoints (`layout`, `rows`, `putSegment`,
`importFlush`, `buildIndex`, `indexStatus`) — the image's stats are trusted
answers, so the load surface belongs to the principal that could install code
anyway.

**Running the loader.** The tool ships with this skill in `scripts/` — plain
Node (≥ 20) with **no dependencies to install**; every call goes through
`icp canister call`, so icp-cli must be set up:

```bash
node <this skill's directory>/scripts/ingest.mjs \
  --canister <canister-id> --target event --file events.csv \
  -e ic --index kind:hash
```

- `--target` is the `importTarget` name declared in the canister; the canister's
  `layout()` is the schema authority — the CSV header is matched to the columns
  **by name**, so file column order never matters (extra CSV columns are
  ignored; a declared column missing from the file is an error).
- Connection flags pass through to icp-cli, the same way every other canister
  call works: `-e <environment>` (`-e ic` for the deployed app), `-n <network>`,
  `--identity <name>` (default: your current one). The endpoints are
  controller-only, so the identity must be a **controller** of the canister.
  With none of them, your icp defaults apply — a canister NAME then resolves
  against the project's default environment, so run the tool from the app's
  project directory.
- `--index col:kind` (repeatable, `kind` = `hash`) builds and uploads that
  column's index off-chain after the rows. For anything it can't build
  (`#ordered`, composites), build on-chain instead through the mixin's
  endpoint: `icp canister call <id> buildIndex '("event", vec {"kind"},
  variant {hash})'` — queries scan (correctly, just slower) until the build
  completes, then the index serves; `indexStatus '("event")'` reports progress.
- Verify a load the same way clients will read it:
  `icp canister call <id> execute '("{\"start\":\"event\",\"aggregate\":[{\"fn\":\"count\"}]}")' --query`
  must return the CSV's row count.
- CSV cells decode by declared type. An unquoted empty field is a **null**
  cell; a quoted `""` in a `#text` column is the empty string; a `#bytes(w)`
  column's field is **base64** and must decode to exactly `w` bytes.
- **Re-running the same command resumes**: rows the table already holds are
  skipped, and `putSegment`'s expect-first-row guard turns any double-send into
  a loud trap instead of duplicated rows.

**Operating rules** (violations refuse loudly rather than corrupt):

1. **Finish the first load completely — data and indexes — before the app
   starts writing.** If writes land mid-load, a re-run cannot finish the index;
   rebuild it in-canister with `buildIndex` (slower, always works).
2. **After that, load and write in turns.** Between loads the app writes
   freely; the next run of the same command picks up the growth as a delta
   load, nothing to prepare.
3. **Never both at once** — the canister refuses, it does not mis-answer.
4. **Queries keep working throughout**, including mid-load; a column whose
   index is still uploading scans until it finishes.

## Checklist

- [ ] `mops add caffeineai-oql@0.6.1` in the same batch as the first import
- [ ] Resolver modules imported top-level (see `## Setup` → Imports): `Entity`
      (**always** — every builder method including `.payload` / `.flatten`
      resolves through it), the collection module(s) (`MapEntity` / …), and
      `RecordValue` + a `<Type>Value` per primitive field type of each
      auto-derived record
- [ ] Each entity: row iterator exists; `.toEntity` (all-primitive) or
      `.toEntityManual` / `OQL.Entity.manual` otherwise
- [ ] `<Type>Value.mo` for every non-primitive field reused across entities,
      imported top-level
- [ ] `.sample(template)` on every `.toEntity` / `Entity.manual` chain (dummy values are fine)
- [ ] FK fields `.edge(name, target)`; opaque/sensitive auto-derived fields
      `.hidden(name)` (manual: omit via no `.payload`, or `.hidden` only columns
      you did add)
- [ ] Every sentinel conversion returns ONE `Value` variant
- [ ] Per-user entities use `.ownedBy` / `.ownedByWith` **and** a scoped level
      (`.scopedPerUser()` / `.controllerOrScoped()`) — never bare
      `.controllerOnly()`
- [ ] Large, append-mostly table → `OQL.Table`; keep the handle in a persistent
      field and thread it through migrations
- [ ] Existing dataset to import → declare the `Table` **index-free**, add
      `ImportData([t.importTarget(name)])`, load with `scripts/ingest.mjs`,
      index after the load (`--index` or `buildIndex`) — data and indexes done
      **before** the app starts writing
