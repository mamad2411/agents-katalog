---
name: realm-policy-authoring
description: 'Use when writing, linking, or debugging a realm policy — "let teachers read their own classrooms", "let anyone signed in create a ticket", "why does this grant admit nobody", "point this realm at a policy", "anyone may read", "a public form", "why was this caller refused", "should I grant update", "is snapshot ok here". The reference for a `RealmPolicy` card: rules and grants, the create lane, file and source-read grants, `where` in the `policy` BXL profile, which `query` grants compile to a search filter, `snapshot: true`, every issue code, `validate` and `explain`, anonymous callers and rate limits, the refusals a caller sees, and the judgment calls. Activates on `RealmPolicy`, `PolicyRule`, `OperationGrant`, `"policy"` in `realm.json`, `where`, `actor()`, `nonGrantable`, `readSource`, `operation-not-permitted`, `policy-not-filterable`, `module-not-granted`, `partial-match`, `unsnapshotted-policy-read`, `explain`, `explainDraft`, `policy-not-in-force`, `actingUser`, `blocklist`, `rateLimitRequests`, `rate-limited`.'
boxel:
  kind: skill
---

# Authoring a realm policy

A realm's permissions say who may read it and who may write it, realm-wide. A
**policy** lets a caller those permissions turn away do particular things to
particular cards: a teacher with no permission on the school's realm may read
the classrooms that list them as a teacher, and rename those classrooms, and
nothing else.

A policy is a card. The realm's `realm.json` names it, and its rules grant
operations on card types, each grant optionally conditioned on a BXL predicate
over the card:

```json
{
  "data": {
    "type": "card",
    "attributes": {
      "rules": [
        {
          "targetType": {
            "module": "https://school.example/education/classroom",
            "name": "Classroom"
          },
          "grants": [
            { "operation": "read", "where": ".teacherIds | any(. == actor())" },
            { "operation": "rename", "where": ".teacherIds | any(. == actor())" },
            { "operation": "query", "where": ".teacherIds | any(. == actor())" }
          ]
        }
      ]
    },
    "meta": {
      "adoptsFrom": {
        "module": "@cardstack/catalog/realm-policy/realm-policy",
        "name": "RealmPolicy"
      }
    }
  }
}
```

Most of what goes wrong with a policy does not throw. A grant the realm cannot
apply is recorded as an issue and left out, and the rest of the policy applies
without it, so the symptom is a caller who is refused for no visible reason.
Check the policy's issues (§9) after every edit.

The operations a grant names are the ones `card-operations-authoring` covers:
the base operations every card carries and the named ones a card type
declares.

## What a policy does not do

Read these before relying on a policy for anything that matters. Each is
deliberate, and each is the kind a reader learns about only when it bites.

- **It only widens.** Nothing in a policy takes away what the realm's
  permissions grant. A realm reader reads every card and a realm writer writes
  every card, whatever the policy says (§3).
- **Any writer of the realm controls it.** The pointer is a field on
  `realm.json`, which realm write (not owner) can change, and it may name a
  policy card in a realm the writer can't read (§1).
- **Search is not a prompt revocation boundary.** A direct read judges the card
  as stored and refuses on the next request. A search answers from the index and
  keeps listing the card until it is reindexed. To revoke urgently, change what
  the grant reads on the card: a direct read refuses at once, and a search once
  the card is reindexed. A policy-card edit reaches both only once the policy
  card is reindexed (§3, §7).
- **A `snapshot: true` predicate is a window.** It decides on indexed values,
  so taking someone off a roster a computed value reads from doesn't revoke
  them until the card is reindexed (§8, §14).
- **A write is judged on the card before it.** A grant that admits a caller
  because of a field doesn't stop that caller writing the field (§11, §14).
- **A grant reaches what the card carries.** Linked cards, query-backed
  results, rendered formats and computed values derived from other cards come
  with a granted card, whether or not anything grants them (§3, §9).
- **A card's raw `.json` is the whole card.** A `readSource` grant, or a
  card+json write grant, shows everything a narrower `read` leaves out (§3, §5).
- **Timing is not concealed.** A caller who can't read the realm gets the same
  bytes for a card a grant refused as for one that isn't there, but a refusal
  that evaluated a predicate takes measurably longer (§13).
- **A subtype that declares a compared field differently is left out of a
  `query` grant's search** (as a computed or query-backed field, another type, a
  list, or not at all), though a direct read may still admit its cards (§7).
- **A caller who can't read the realm doesn't name their cards.** The realm
  mints the id of every card they create (§4).
- **An archived realm tells a caller only the policy admits that it is
  archived where a grant would admit them**, and tells every signed-in caller
  on the routes that serve stored bytes (§13).

## 1. Linking a policy

The pointer is the `policy` string on the realm's `RealmConfig` card —
`realm.json`, `data.attributes.policy`:

```json
{
  "data": {
    "type": "card",
    "attributes": {
      "cardInfo": { "name": "Education" },
      "policy": "https://school.example/org/policies/education"
    },
    "meta": {
      "adoptsFrom": { "module": "@cardstack/base/realm-config", "name": "RealmConfig" }
    }
  }
}
```

| `policy` holds                                         | The realm                                                                                   |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| Nothing, `null`, or a blank string                      | Names no policy. Its permissions alone decide every request                                 |
| An absolute `http(s)` card URL                          | Is governed by that card                                                                    |
| A prefix-form id (`@cardstack/catalog/policies/…`)      | Is governed by that card, for a prefix the server maps to a realm                           |
| A relative path, an unmapped prefix, a non-`http(s)` URL, or a non-string | **Names no policy.** The value is dropped and the realm serves on its permissions alone |
| A well-formed id of a card that is missing, errored, or not a `RealmPolicy` | **Refuses every caller its permissions decline**: a 500 for a signed-in caller, the 401 `actor-required` for one who isn't (§9, §12) |

The last two rows are the trap. A typo in the *shape* of the pointer silently
removes the policy. A well-formed pointer to the wrong card fails closed.

- **The policy card may live in another realm**, including one nobody the
  governed realm serves can read. The realm reads it from the server's index
  on its own authority, so the card must be indexed on the same server, without
  error. A pointer into a realm the server doesn't serve reads as
  `policy-card-missing`.
- **Repointing takes effect at once.** The pointer is read from `realm.json` on
  disk. Settings a predicate reads with `realmConfig()` follow the index pass of
  `realm.json`, so they can trail a direct file edit briefly.
- **A published realm names no policy.** Publishing strips `policy` from the
  published copy of `realm.json`; the published realm answers on its own
  permissions. The source realm keeps its pointer.

**Any writer of the realm can repoint it** — at another policy, at none, or at
a policy card in a realm they cannot read. The realm applies whatever it names
on the server's authority. So the policy constrains callers the realm's
permissions decline; it does not constrain the realm's own writers, and a
realm writer can learn whether a compiling policy sits at a URL (a 500 against
an ordinary refusal) and exercise its grants against cards they control. A
policy's rules are not secret from the writers of other realms on the server.
**Never put a value that must stay secret in a predicate.**

## 2. The card shape

The definitions live in the catalog realm:

```
RealmPolicy   (CardDef)   rules     = containsMany(PolicyRule)
PolicyRule    (FieldDef)  targetType = contains(CodeRefField)
                          grants    = containsMany(OperationGrant)
OperationGrant(FieldDef)  operation              = contains(StringField)
                          where                  = contains(PolicyPredicateField)
                          actingUser             = contains(StringField)
                          blocklist              = contains(StringField)
                          rateLimitRequests      = contains(StringField)
                          rateLimitWindowSeconds = contains(StringField)
```

An instance adopts from `@cardstack/catalog/realm-policy/realm-policy`, name
`RealmPolicy`. Write it as JSON. A rule is a field holding a `containsMany` of
grants, and the card API renders no editor for a `containsMany` nested inside a
field, so the card's edit view can't reach a rule's grants.

**`targetType`** is a code ref, `{ "module", "name" }`. The module is an
absolute URL, a prefix form (`@cardstack/base/card-api`), or a path relative to
the policy card's own URL — `../classroom` for a policy card at
`policies/education` in the realm that holds `classroom.gts`. A module that
re-exports the type works too.

**`operation`** is the name a caller invokes — a base operation (`read`,
`update`, `query`, …) or a named operation the type declares (`rename`).

**`where`** takes three forms:

| `where`                                   | Means                                                                 |
| ----------------------------------------- | --------------------------------------------------------------------- |
| absent or `null`                          | Unconditional — the grant admits every card the rule matches           |
| `".teacherIds \| any(. == actor())"`      | A BXL predicate over the card's stored values                         |
| `{ "bxl": ".headTeacher == actor()", "snapshot": true }` | A predicate that may read computed values and searchable links (§8) |

`""` (or whitespace) is not "no condition"; it records `invalid-predicate`.
Leave `where` out for an unconditional grant.

**`actingUser`**, **`blocklist`**, **`rateLimitRequests`** and
**`rateLimitWindowSeconds`** are BXL expressions, each a string, that say how a
grant treats callers who aren't signed in: the user such a caller's write is
made as, the addresses the grant refuses, and how many requests one address
may make through it (§12). A grant admits such a caller only when its `where`
names them (`actor() == "anonymous"`). Leave all four out for a grant that
admits signed-in callers only.

**Any other shape breaks the whole card, not just the grant.** An object with a
key besides `bxl` and `snapshot`, a `bxl` that isn't a string, or a `snapshot`
that isn't a boolean (`"yes"`) fails the card when it is indexed. The realm then
records `policy-card-unloadable` and the whole policy is out of force: every
signed-in caller the realm's permissions decline gets 500, and every caller who
isn't signed in gets 401 `actor-required` (§9).

The card also carries operations no grant can reach: `validate`, on the
`validate` base, which answers what the policy compiles to (§9), and `explain`,
on the `explain` base, with its draft, search and listing forms, which answer
what it decides for one caller, card and operation (§10). Its isolated view
runs both.

## 3. What a grant admits

**A policy only widens access.** A request the realm's permissions allow never
reaches the policy — a realm writer's write and a realm reader's read evaluate
no predicate. The policy is consulted only for what the permissions declined:
everything, for a caller with no permission on the realm; writes, for a caller
who may read it. A caller who isn't signed in reaches it only through a grant
that opts in (§12). The two exceptions are the policy's own tools: an `explain`
runs the predicates for the actor it names, and a `validate` compiles the
policy (§9, §10). A route that needs the realm's owner, such as
`_permissions`, answers on the permissions alone, and no grant reaches it.

**Taking a realm permission away doesn't revoke a caller a grant admits.** It
sends their next request to the policy, which may admit it. To take access
away at once, change what the grant's predicate reads on the card (take their
id off `teacherIds`), or change the policy. The direct lane sees a card edit on
the next request, and a search sees it once the card is reindexed (§7). Both
lanes see a policy-card edit once the policy card is reindexed (§9).

**Grants union.** A request is admitted when any grant in any rule that
matches holds. Order changes nothing, and nothing in a policy denies. Two rules
on the same type are two sets of grants, either of which can admit.

**A rule covers its type and every subtype, never an ancestor.** A rule on
`Classroom` covers a `Homeroom extends Classroom`; a rule on `Homeroom` does not
cover a plain `Classroom`.

**Name the root type to mean everything:**

| You mean            | `targetType`                                                       |
| ------------------- | ------------------------------------------------------------------ |
| every card          | `{ "module": "@cardstack/base/card-api", "name": "CardDef" }`        |
| every file          | `{ "module": "@cardstack/base/file-api", "name": "FileDef" }`        |

**Never `BaseDef`.** A rule on `BaseDef`, or on any field definition, compiles
to no grants: the realm records each grant on it as `unknown-operation` ("BaseDef
has no `read` operation…"), whatever operation it names. The message blames the
operation; the cause is the type.

**A named operation is grantable only on the type that declares it, or a
subtype.** A rule on `CardDef` naming `rename` records `unknown-operation` even
though `Classroom` declares `rename`, and that grant is inactive. Put the grant
on a rule for `Classroom`.

**A grant on a named operation never grants its base.** Granting `rename` (a
`transform`) does not grant `transform`; granting `appendActivity` (a `create`)
does not grant a plain `create` of the card type it mints. That is the point of
a named operation: the grant admits the one narrow write the declaration
expresses.

**What each target carries.** A card carries `read`, `readSource`, `create`,
`update`, `delete`, `query`, `transform` and `appendContainsMany`, plus its
named operations. On a **file**, a grant only ever admits `readSource` (§5).
`explain` and `validate` are never granted (§11).

**A `query` grant only scopes search.** It never admits a direct read of a
card, and a `read` grant never puts a card in anyone's search results. To let a
teacher both open and list their classrooms, grant both (§7).

**The card+json verbs reach the built-in behavior only.** A granted `update`,
`delete` or `create` admits `PATCH`, `DELETE` and `POST` on the card+json
routes — unless the type redeclares that operation, in which case the verb is
refused to a caller the permissions declined, and the grant is used only
through `_operations`. A card+json write that side-loads cards in `included` is
refused to such a caller too, whatever the grants say. **A granted card+json
write answers with the whole card.** A `POST` or `PATCH` answers with the
card's indexed document without running the type's `read`, so no `output` a
`read` declares narrows it, and a `PATCH` that changes nothing still answers
with it. Grant a card+json write only where the caller may see the whole card.

**A granted `read` serves the card's whole representation**, as the type's own
`read` declaration shapes it for every caller: under the default `links:
'full'`, the linked cards and the results of query-backed fields arrive in
`included`, even when the caller holds no grant on those cards' types and a
direct read of one would be refused. Under `links: 'ids'` the relationships name
their targets and nothing is assembled. The realm records
`grant-reaches-ungranted-type` against such a grant as a warning (§9). **A
declaration applies uniformly**: the response shape never depends on how the
caller was authorized, so a grant can't be given a narrower representation than
a realm reader gets — narrow the declaration itself (`card-operations-authoring`
§2).

## 4. The create lane

A create has no stored card to test, so it is matched and judged differently.

- **It is judged by the resolved type**, never by the type the payload claims.
  A payload whose `adoptsFrom` names a module that re-exports `Bulletin` is a
  `Bulletin` create; one whose class is *called* `Bulletin` but resolves to
  `Classroom` is a `Classroom` create.
- **A `CardDef` rule granting `create` covers every create.** A rule on a type
  covers creates of its subtypes.
- **Only a `create` grant admits a create.** `read`, `update` and `delete` grants
  never do, on any type.
- **A `where` on a create reads the card being minted** — its attributes as the
  payload leaves them after staging. A named create anchored on an existing
  card (`appendActivity` invoked on a classroom) is judged by that card instead.
- **A create grant cannot use a snapshot read.** The new card is not in the
  index yet; a `create` grant with a `snapshot` predicate that reads a computed
  or linked value records `unsnapshotted-policy-read` (§8).
- **`adoptsFrom` must name an absolute or prefix-form module.** A create whose
  type is `{ "module": "./bulletin" }` is refused with 400 `invalid-params`
  through `_operations` for every caller, realm owner included, and through a
  card+json `POST` for every caller the realm's permissions decline: a card
  that isn't stored yet has no location for a relative module to resolve
  against.
- **For a caller who cannot read the realm, the realm chooses the new card's
  id.** It lands under the type's directory (`…/Bulletin/<minted>`). A `lid`
  still links the cards of one batch to each other, but names no file. Their
  card+json `POST` targets the realm root; a `POST` to a subdirectory answers
  404, or 401 `actor-required` to a caller who isn't signed in (§12).

## 5. Files and source

`readSource` is the read of a path's stored bytes: a data file's bytes, a
module's source, or a card's raw `.json`. It is the one operation a grant
admits on a file, and it is judged differently from every other read, because
it is matched on what is stored at the path rather than on an index row.

### How a file resolves to a type

A card's `.json` is matched on the card's type. Every other stored file is
matched on the `FileDef` subclass its **extension** names, and nothing else:
not its bytes, not its index row. **Renaming a file changes which rule matches
it, and whoever can write a file chooses its name.** A realm writer who saves
a document as `notes.png` puts it under every grant on `PngDef` and `ImageDef`.

A rule matches through ancestry (§3), so a rule on an intermediate class
covers every extension beneath it:

| Name                                        | Resolves to                                  | Also matched by a rule on        |
| ------------------------------------------- | -------------------------------------------- | -------------------------------- |
| `logo.png`                                  | `PngDef`                                     | `RasterImageDef`, `ImageDef`, `FileDef` |
| `photo.jpg`, `photo.jpeg`                   | `JpgDef`                                     | `RasterImageDef`, `ImageDef`, `FileDef` |
| `icon.svg`                                  | `SvgDef`                                     | `ImageDef`, `FileDef` — not `RasterImageDef` |
| `notes.md`, `notes.markdown`                | `MarkdownDef`                                | `FileDef`                        |
| `readme.txt`                                | `TextFileDef`                                | `FileDef`                        |
| `build.log`                                 | `LogFile`                                    | `TextFileDef`, `FileDef`         |
| `grades.csv`                                | `CsvFileDef`                                 | `FileDef`                        |
| `syllabus.pdf`                              | `PdfDef`                                     | `FileDef`                        |
| `song.mp3`                                  | `Mp3Def`                                     | `AudioDef`, `FileDef`            |
| `song.mid`                                  | `MidiDef`                                    | `FileDef` — not `AudioDef`       |
| `clip.mp4`                                  | `Mp4Def`                                     | `VideoDef`, `FileDef`            |
| `data.json` whose bytes are not a card document | `JsonFileDef`                            | `FileDef`                        |
| `Classroom/1.json` holding a card document  | The card's type, from its `adoptsFrom`       | That type's ancestors, up to `CardDef` |
| `theme.css`, `site.yml`, `LICENSE`, `.gitignore`, `bundle.mjs` | `FileDef` itself          | —                                |
| `util.ts`, `app.js`                         | `TsFileDef`: module source (see below)       | Nothing else — not `FileDef`     |
| `classroom.gts`, `app.gjs`                  | `GtsFileDef`: module source (see below)      | `TsFileDef` — not `FileDef`      |

- **The extension is the last dot of the file name, in any case.** `photo.PNG`
  is a `PngDef`; `backup.tar.gz` is a `.gz`, which no def covers, so `FileDef`.
- **An extension no def is written for, or none, resolves to `FileDef`
  itself.** So does a dot-file: `.gitignore` has no extension. A rule on a
  narrower type never matches one.
- **A `.json` is a card's source only if its bytes are a card document.** It is
  then matched on the type the document names, judged from the stored bytes,
  never from the index, so a card written a moment ago and not yet
  indexed is matched on its new type. A card whose type doesn't resolve is
  matched by nothing, not read as a data file. Any other `.json` is a
  `JsonFileDef`.
- **A path with nothing stored at it is matched by nothing**, so a grant
  answers "not found" for it as for a file it refuses.

Name a narrower type in `targetType` the way §2 names any type —
`{ "module": "@cardstack/base/image-file-def", "name": "ImageDef" }`.

### What a `readSource` grant serves

- **A grant on a card type serves that card's raw `.json`**, and a subtype's. A
  rule on `CardDef` granting `readSource` serves every card's raw source except
  the realm's config card and policy cards, which no grant reaches (§11).
- **A card's `.json` is its whole stored document**, including every field the
  type's `read` declaration leaves out of a read. A `readSource` grant beside a
  narrower `read` hands the caller everything that `read` was written to
  withhold. Grant `readSource` on a card type only where the caller may see all
  of it. It is not a superset of a read either: a default `read` carries the
  linked cards in `included`, and the stored document holds only their ids.
- **A rule on `FileDef` serves every stored file that isn't module source**:
  every data file, every dot-file (`.gitignore` and the like), and files of
  types nobody has written a def for. A rule on `FileDef` is a catch-all; to
  keep dot-files out, grant a narrower type (`ImageDef`, `PdfDef`, …), which a
  dot-file never matches.
- **No grant reaches a path the realm ignores**: anything in a `.git` or
  `node_modules` directory at any depth, and whatever the `.gitignore` at the
  realm's root names. A caller reaching the realm only through grants is told such a path
  holds nothing. The `.gitignore` itself is served by a rule on `FileDef`
  unless its own patterns name it.

### Over HTTP

A `readSource` grant is honored on the routes that serve a path's bytes: the
`card+source` read, the realm's raw file serve, and the module serve a
browser's `import` reaches, `GET` and `HEAD`. For a caller the realm's
permissions decline:

- **The `card+source` read takes the name exactly as given: no extension
  fallback and no redirect.** Ask for `Classroom/1.json`, not `Classroom/1`;
  `room.v2` is not redirected to `room.v2.json`, and `classroom` is not
  `classroom.gts`.
- **The module serve resolves an import name as it does for a reader.**
  `./classroom` reaches `classroom.gts`, and the gate judges the module the
  name resolved to, so a grant on `GtsFileDef` serves it by either name.
- **The gate decides before any cache answers**, so a refused caller's answer
  never depends on what a reader's requests cached. A caller it admits to a
  module is served from the module caches a reader is, and a module compiled
  for them fills those caches for whoever asks next. Source they read on
  `card+source` or the raw file serve isn't cached.
- **A granted response is always `Cache-Control: private`.**
- **`If-None-Match` and the other validators count only after the gate has
  admitted the read**, so a refused caller can't probe a file's content with an
  `ETag`.
- **A refused `GET` is a 404 identical to a missing path**, and a refused
  `HEAD` gets the realm's discovery answer, as for any path such a caller can't
  read (§13).

### Predicates on a file

A file has no document to read. A `where` on a file rule sees the file's URL,
through `instance("id")`, the caller, through `actor()`, and the realm's
settings, through `realmConfig()`. `.` holds no fields and `instance()` no
other key, so write the predicate on those:

```json
{
  "operation": "readSource",
  "where": "instance(\"id\") | startswith(\"https://school.example/education/handouts/\")"
}
```

The path is a name a writer chose, so a path predicate inherits the rename
caveat above: anyone who can write into `handouts/` decides what it serves.

### Code is a file a grant can name

Module source is matched like any other file, on the type its extension names,
but only on the part of that type's chain that is code:

- **A rule on `TsFileDef` covers every module**: `.ts`, `.gts`, `.js` and
  `.gjs`. A rule on `GtsFileDef` covers the ones with templates, `.gts` and
  `.gjs`. `GtsFileDef` extends `TsFileDef`, so a `.gts` is matched by either.
  Other script extensions (`.mjs`, `.cjs`) are not module source to the realm:
  they are data files a `FileDef` rule serves.
- **A rule on `FileDef` does not reach code.** A module's chain stops short of
  `FileDef`, so the catch-all written for a realm's data files never serves
  the modules that render them. Only a rule naming a code type does.
- **A `readSource` grant on a code type serves the modules it covers** to the
  callers its `where` admits: their source on `card+source`, and the
  transpiled module a browser imports, by path or by import name (see
  [Over HTTP](#over-http)).
- **Its `where` reads what a data file's does**: `actor()`, `instance("id")`
  and `realmConfig()` (see [Predicates on a file](#predicates-on-a-file)).
- **A granted module is served `Cache-Control: private`**, from the same
  module caches a caller with the realm's own read is served from, once the
  gate has admitted the read (see [Over HTTP](#over-http)), so serving it to a
  granted caller costs no more than serving it to a reader. A shared cache in
  front of the realm (a CDN or a proxy) never stores a granted module, because
  it would answer without the gate: past each grant's blocklist and rate
  limit, and after a grant is narrowed or removed. Put modules that need to be
  CDN-cacheable in a realm with a `*: read` permission.
- **A code grant can open modules to callers who aren't signed in**, as any
  file grant can, when its `where` names them (§12). A card opened to visitors
  needs its module opened to them too, or the card reads and fails to render.
  Each module served to a visitor, a 304 included, counts against the grant's
  rate limit, and a browser imports several modules for one card.
- **A module no grant reaches is refused as any file is:** a signed-in caller's
  `GET` gets a 404 identical to a missing path, a `HEAD` gets the realm's
  discovery answer, and a caller who isn't signed in gets 401
  `actor-required` (§12, §13).

So **code and data can live in one realm.** A caller who reaches the realm only
through grants needs the module behind every card they are granted, or the card
reads and fails to render. Grant the code to the same people as the cards. A
project realm lets the reviewers its `realm.json` lists read and find its
plans, and load the code that renders them:

```json
{
  "rules": [
    {
      "targetType": { "module": "../plans/project-plan", "name": "ProjectPlan" },
      "grants": [
        { "operation": "read",  "where": "realmConfig(\"reviewers\") | any(. == actor())" },
        { "operation": "query", "where": "realmConfig(\"reviewers\") | any(. == actor())" }
      ]
    },
    {
      "targetType": { "module": "@cardstack/base/ts-file-def", "name": "TsFileDef" },
      "grants": [
        { "operation": "readSource", "where": "realmConfig(\"reviewers\") | any(. == actor())" }
      ]
    }
  ]
}
```

All three grants read one list, the realm's `config`
(`"reviewers": ["@reviewer:example.org", …]`), so adding or removing a
reviewer is one edit to `realm.json`. The `query` grant's `where` reads nothing
of the card, so a search settles it once for its caller (§7). To let different
people see different plans, keep the list on each plan instead
(`.reviewerIds | any(. == actor())`), which compiles to a filter, and keep the
code grant's list a superset of every plan's.

**`validate` warns when the code grant is missing.** A `read` or `query` grant
on a type the realm defines, in a policy with no `readSource` grant on
`TsFileDef` or `GtsFileDef`, records `module-not-granted` (§9). A rule on
`CardDef` counts too, by the realm's own types it holds cards of. A code grant
covers only the kinds of caller it can admit: one whose `where` is
`actor() == "anonymous"` serves visitors, not the signed-in callers a read
grant names. Beyond that, the check never evaluates the code grant's `where`,
so a reviewer listed on a plan but missing from the code grant's list reads the
plan and can't render it, with no warning, and a code grant narrowed by path
(below) silences the warning even for cards whose module lies outside it. Nor
can it tell a module's extension, so a grant on `GtsFileDef` alone silences the
warning while cards whose type is defined in, or descends from, a `.ts` module
still fail to render. Grant the code on `TsFileDef`. A grant never implies
another, so the read grant can't carry the code with it.

A rule on `TsFileDef` serves every module in the realm, including ones no
granted card uses. To serve fewer, narrow the predicate by path
(`instance("id") | startswith(…)`), as for any file. Module source is
readable code, so grant it only where the caller may read all of what it
covers.

Keeping the definitions in a separate realm everyone can read, as the school
example does with `school-code` (§10), is another arrangement, not a
requirement.

### What needs the realm's own read

A grant reaches files, never the realm's file tree or the routes that analyze
its code:

- **The directory listing.** A caller who reaches the realm only through grants
  is told a directory holds nothing.
- **Code mode's routes**: `_dependencies`, `_card-dependencies` and `_lint`.
- **A shimmed module**, which the host serves from its own bundle rather than
  from the realm's files.

So **code mode needs the realm's own read permission** — browsing the file tree
does, whatever the grants say about the files in it. The host doesn't offer
code mode to a caller without it: the submode switcher, a card's error and an
attached file offer no way in, and the assistant's tools that open code mode
refuse. That is a courtesy, not the boundary; the endpoints are. A shared link
can still land a grant-reached caller in code mode, where the file tree is
refused and only a file a grant reaches opens — and a card's `.json` granted
by `readSource` can show there beside a preview its missing `read` refuses.
Anyone who authors code in a realm needs the realm's own read permission, and
its write permission to save.

## 6. Writing `where`

A predicate is BXL validated against the **`policy` profile**. It must evaluate
to exactly `true`; anything else — `false`, `null`, a string — does not hold.
`bxl-authoring` covers the language; this section covers what the profile
changes.

### What `.` is

`.` is the card's **stored** values, projected the way a card operation sees
them:

| Read                                   | Gets                                                             |
| -------------------------------------- | ---------------------------------------------------------------- |
| `.title`, `.address.city`              | Stored scalars and contained values                               |
| `.id`                                  | The card's own URL                                                |
| `.lead.id`                             | The absolute URL a `linksTo` names (relative links are resolved)  |
| `.lead == null`                        | An unset `linksTo`                                                |
| `.teachers \| any(.id == "https://…")` | A `linksToMany`, as a list of `{ id }`                            |

There is no `.attributes` or `.relationships`. A computed field's value and a
linked card's fields are **not** in `.` — reading one needs `snapshot: true`
(§8).

### The calls

| Call                 | Gives                                                                         |
| -------------------- | ----------------------------------------------------------------------------- |
| `actor()`            | The caller's Matrix user id, `"@teacher:school.example"` — only that. For a caller who isn't signed in, `"anonymous"`, which only a grant whose `where` names it admits (§12) |
| `instance("key")`    | One of the card's raw stored attributes; `instance("id")` is its URL          |
| `realmConfig("key")` | A setting from the governed realm's `config` object on `realm.json`            |
| `policy("field")`    | A stored field of the policy card itself. `RealmPolicy` declares only `rules` beside what every card carries, so a value of your own needs a `RealmPolicy` subtype that declares the field (§12) |

`params()` is refused (`invalid-predicate`): a grant decides whether a caller
may invoke, never what they sent. `NOW()`, `TODAY()` and the random functions
are refused too — a predicate gives one answer for one card and one caller.

```json
{ "operation": "approve", "where": "realmConfig(\"approver\") == actor()" }
```

with the governed realm's `realm.json` holding
`"config": { "approver": "@principal:school.example" }`.

### Membership: `any(. == actor())`

Spell "the caller is in this list" as:

```
.teacherIds | any(. == actor())
```

- `actor() in .teacherIds` compiles and **throws** on every card.
- `contains` is a **substring** match: `.teacherIds | contains([actor()])` holds
  for `@bob:school.example` against a list holding `@bob:school.example.org`. The
  realm refuses it — see below.

### Partial-match builtins are refused

Any call that can hold for a value it matches only in part records
`partial-match`, and the grant is inactive. The call is refused wherever it
appears in the predicate, not only next to `actor()`:

| Kind                         | Refused                                                                       |
| ---------------------------- | ----------------------------------------------------------------------------- |
| Substring                    | `contains`, `inside`, `index`, `rindex`, `indices`, `FIND`, `SEARCH`, `isIn`  |
| Pattern                      | `test`, `match`, `capture`, `scan`, `matches`, `like`                          |
| Nearest-value lookup         | `MATCH`, `LOOKUP`, `LOOKUP_BY`, `VLOOKUP`, `VLOOKUP_BY`, `HLOOKUP`, `XLOOKUP`, `bsearch` |
| Internal helpers             | any call whose name starts with `_`                                            |
| Anchored at a variable value | `startswith`, `endswith`, `ltrimstr`, `rtrimstr`, `trimstr` — unless their one argument is a fixed string literal |

Compare strings with `==`. A fixed prefix or suffix is allowed, and the realm
cannot check where the literal ends, so end a prefix at a delimiter and start a
suffix at one:

```
actor() | endswith(":school.example")
```

`":school.example"` cannot be satisfied by `@eve:evilschool.example`;
`"school.example"` can.

### Parenthesize every membership test in a compound predicate

`|` binds more loosely than `or` and `and`, so an unwrapped second test joins
the first pipeline and the predicate throws:

```
(.teacherIds | any(. == actor())) or (.leadTeacherIds | any(. == actor()))
```

### Other refusals

All of these record `invalid-predicate`, whose message names the rule broken:

- **Single quotes.** `.status == 'open'` doesn't tokenize. Use double quotes —
  escaped inside JSON: `".status == \"open\""`.
- **Aggregates** — `SUM`, `COUNT`, `MAX`, jq `max`/`min`, and the rest.
- **Error masking** — `try`, `IFERROR`, `ISERROR` and kin. A predicate that
  fails must fail visibly.
- **Structure** — `def`, `reduce`/`foreach`, `..`, assignment, `label`/`break`,
  `@base64` and the other formats.

Bindings (`. as $c`), `IF(…)`, `has(…)`, `length`, `tonumber`, case folding and
`split` are fine.

### A predicate that throws

A predicate that throws on a card — `(.title | tonumber) > 0` on a title that
isn't a number — **denies**, unless another grant holds. When none does, the
caller gets 500 `policy-predicate-failed` if they may read the realm, and the
same 404 as any refusal if not; explaining the decision answers
`predicate-threw` (§10). A throw
is a bug in the policy, not a refusal: guard the value (`.title != null and
…`) rather than relying on it.

## 7. `query` grants and search

A `query` grant is never evaluated card by card. Its predicate is compiled into
a search filter, and every ad-hoc search by a caller the realm's permissions
decline — the realm's `_search` and `_federated-search` — is narrowed by it.

**A grant on a named query is a different grant.** A grant whose `operation`
names a `query` operation the type declares (`listMySchedules`) compiles its
`where` the same way, and its filter narrows only that saved search, invoked by
name. It never admits an ad-hoc search, and a grant on `query` never admits the
saved one: granting a saved search is not granting the freedom to write any
filter over its type. Prefer the named form when the type's `query`
declaration narrows what each row carries (its `links`), since an ad-hoc search
serves every row with its whole link closure. A predicate the filter compiler can't express records
`policy-not-filterable`, and the grant admits nothing.

What compiles:

| Predicate reads                       | Compiles when                                                          |
| ------------------------------------- | ---------------------------------------------------------------------- |
| A text field                          | `==` / `!=` against a string or `actor()`, on a field whose type is exactly `StringField`, `TextAreaField`, `MarkdownField` or `ReadOnlyField` |
| A number field                        | `==`, `!=`, `<`, `<=`, `>`, `>=` against a number literal, on exactly `NumberField` |
| A `containsMany` of text              | Membership only: `.teacherIds \| any(. == actor())`                     |
| A `linksTo`                           | `.lead.id == "<absolute URL>"`                                           |
| A `linksToMany`                       | `.teachers \| any(.id == "<absolute URL>")`                              |
| A computed field                      | Only with `snapshot: true`, under the same rules as a stored field      |
| No condition                          | Always — every card of the type and its subtypes                        |
| Nothing of the card                   | Settled once per search: every card or none (below)                     |

Combine with `and`, `or` and `not` — except that a membership test or an id
comparison can't sit under `not` or `!=`.

**A predicate that reads nothing of the card is settled once per search.** One
that reads only `actor()`, `realmConfig()`, `policy()` and fixed values, such as
`realmConfig("reviewers") | any(. == actor())`, has the same value for every
card. A search runs it once for its caller, before anything is composed: where
it holds, the grant admits every card of its type and subtypes, as a grant with
no condition does; where it doesn't hold, or throws, the grant adds nothing. No
row is judged. A change to `realm.json` reaches the next search once the realm
has indexed it. Any read of the card at all takes the predicate down the
filter path instead. So does any variable binding (`realmConfig("x") as $list |
…`), whatever it binds, and any builtin called at the top of the predicate,
where its input is the card (`IN(…)`, `IF(…)`): start from the setting and pipe
it on, as `realmConfig("reviewers") | any(. == actor())` does. So a predicate
that mixes the two,
`(realmConfig("reviewers") | any(. == actor())) and .status == "open"`, records
`policy-not-filterable`. To scope by both, either list the reviewers on each
card (`(.reviewerIds | any(. == actor())) and .status == "open"` compiles), or
grant the listed reviewers a named query whose own filter does the narrowing:
`listOpenPlans`, declared with `eq: { status: 'open' }`, granted with
`realmConfig("reviewers") | any(. == actor())`.

What doesn't compile, and records `policy-not-filterable`:

- `realmConfig()` or `policy()` beside a read of the card, and string functions
  — `startswith`, `ascii_downcase`, even where the gate would accept them.
- A link's id compared with `actor()`, a relative URL, or a prefix-form id. A
  link is a card, never a person; compare `actor()` with a text field that holds
  user ids.
- A link compared as a whole, `.lead == null` included — only its `.id` is
  comparable. The gate accepts `.lead == null`; a search filter doesn't.
- Any field of a linked card (`.lead.name`), even with `snapshot: true`.
- A query-backed field, in any form.
- Bindings (`. as $c`) and variables, though the gate accepts them.
- `true`/`false` literals, fields of any other type (`BooleanField`, `DateField`,
  custom fields), a whole list (`.teacherIds == […]`), a list position
  (`.teacherIds[0]`), lists of numbers, arithmetic, `//`, `if`, and one field
  compared with another.

How a filter and its predicate can differ:

- **The filter can be narrower.** A comparison BXL holds for an unset value
  doesn't list a card that has none: `.roomNumber < 200` holds in BXL for a
  classroom with no room number (`null < 200`), and `.providerId != actor()`
  for one with no provider, and the filter lists neither. Say `== null` when
  you mean those cards — `.providerId == null` compiles.
- **A subtype that redeclares a field the filter compares is kept out of that
  comparison**, so its cards aren't judged by a field that means something else
  there. A subtype in the governed realm that declares the compared field as a
  computed field, a query-backed one, another type, or a list, or doesn't
  declare it, never comes back from a search through a grant resting on that
  comparison alone, though a direct read, which runs the predicate against the
  card itself, may still admit it. Under `snapshot: true` a computed
  redeclaration reads alike and is judged as usual, and a link compared by its
  `.id` reads the same whatever it links to. A subtype that declares the field
  back as the rule's type does is judged as usual. No issue is recorded; an
  explain of the search shows the exclusion in `search.fragment`, as a `not`
  of the subtype beside the comparison (§10). If the realm can't name such a
  subtype in a filter, the grant records `policy-not-filterable`.
- **A caller's filter and a grant that test the same path into a list must
  be satisfied by one element of it.** The search runs the caller's filter and
  the grants as one query, so where both test the list itself, or the same
  field of the cards it links to, one element has to meet both conditions.
  With the grant `.teacherIds | any(. == actor())`, a teacher who searches
  `teacherIds` for themselves finds every classroom they teach, and a search of
  `teacherIds` for a colleague finds none of those classrooms, not even one
  that lists them both. A classroom another of their `query` grants admits,
  such as one they own, is still found. Write such a search against another
  field. Conditions on
  different fields of a list's items are each met by any element, not
  necessarily the same one. A saved search's own filter is composed the same
  way. The limit only ever removes rows, never adds one.

A `query` grant compiles only on a card type, so a caller a grant reaches never
searches file rows. The config card and every policy card are left out of
every policy-scoped search, so even an unconditional `query` grant on `CardDef`
does not list them.

## 8. `snapshot: true`

A predicate reads the card's stored source by default. Stored source holds a
link as a reference and holds no computed value at all, so a grant that needs
either opts into a **snapshot**: the realm lays the card's indexed values under
its stored ones before evaluating.

| Predicate reads                                         | Needs                                              |
| ------------------------------------------------------- | -------------------------------------------------- |
| Stored fields, `.lead.id`, `.teachers \| any(.id == …)` | Nothing                                            |
| A computed field (`.headTeacher`)                       | `snapshot: true`                                   |
| A field of a `linksTo` marked `searchable` (`.lead.handle`) | `snapshot: true`                               |
| Fields behind a `linksToMany`, a non-`searchable` link, a link inside a contained value or a linked card, a computed value inside a list, a query-backed field, or `instance()` of a computed field | **Unreadable** — no snapshot holds them |

```json
{ "operation": "read", "where": { "bxl": ".headTeacher == actor()", "snapshot": true } }
```

A predicate that reads a value from the second or third row without the
annotation, or a value from the last row in any form, records
`unsnapshotted-policy-read`, and the grant is inactive in both lanes. An
annotated predicate that reads only stored values compiles as an ordinary one.

What a snapshot read costs:

- **It is as fresh as the index.** The indexed values trail a write until that
  write is indexed. A card that is not indexed, or whose index row is an error,
  admits nothing through a snapshot grant.
- **Computed values always come from the index**, even when the stored JSON holds
  a value under the same key.
- **A linked card's fields count only while the stored link still names the
  card the index expanded.**
- **No create** — §4.

Each decision a snapshot grant makes at the gate or under the write lock is
logged as `policy-snapshot-read` on the realm's `boxel:operations` channel,
naming the grant and the rule's type, so an operator can count how often a
realm leans on index-time values. A capability check logs nothing, and an
explain logs its decisions marked `hypothetical`.

Whether a given grant may rest on index-time values is a judgment about how
stale a decision may be. Make it per grant (§14).

## 9. When a policy is wrong

**The policy fails closed.** A policy the realm can't compile refuses every
caller its permissions decline. There is no fallback to an earlier version.

**An issue takes out the part it names.** A grant with an issue is inactive and
the rest of its rule applies; a rule with an issue is dropped and the other
rules apply. Each issue has a `code`, a `path` at the author's position
(`rules[1].grants[0].where`, or `""` for the whole card), a plain-language
`message`, and a `severity`:

| Code                                  | Severity | Part     | Means                                                                 |
| ------------------------------------- | -------- | -------- | --------------------------------------------------------------------- |
| `policy-card-missing`                 | inactive | card     | The index holds no card at the pointer                                 |
| `policy-card-unloadable`              | inactive | card     | The card's index row is an error, or its last visit failed            |
| `not-a-policy`                        | inactive | card     | The card isn't a `RealmPolicy`                                         |
| `invalid-rule` (at `rules`)           | inactive | card     | `rules` is present and isn't a list. A card with no `rules` compiles to a policy that grants nothing |
| `invalid-rule`                        | inactive | rule     | `targetType` lacks `module`/`name`, or `grants` isn't a list           |
| `unresolved-type`                     | inactive | rule     | The `targetType` resolves to no exported type                          |
| `invalid-grant`                       | inactive | grant    | The grant names no `operation`, or its `where` is neither a string nor `{ bxl, snapshot }` |
| `unknown-operation`                   | inactive | grant    | The type has no such operation (and every grant on `BaseDef`)          |
| `grants-invalid-operation`            | inactive | grant    | The operation is declared but failed to lower                          |
| `grants-authorization-infrastructure` | inactive | grant    | The operation is `nonGrantable`, or the rule's type is a `RealmPolicy` (§11) |
| `unresolved-type` (at `.operation`)   | inactive | grant    | An ancestor of the type has no readable definition, so whether it marks the operation `nonGrantable` can't be told |
| `invalid-predicate`                   | inactive | grant    | `where` is empty, doesn't parse, or breaks the `policy` profile (§6)   |
| `partial-match`                       | inactive | grant    | `where` calls a partial-match builtin (§6)                             |
| `unsnapshotted-policy-read`           | inactive | grant    | `where` reads a value its form can't (§8)                              |
| `policy-not-filterable`               | inactive | grant    | A `query` grant's `where` can't compile to a search filter (§7)        |
| `anonymous-not-base-operation`        | inactive | grant    | A `where` names `"anonymous"` on a named query, or on an operation whose base isn't eligible (§12). Recorded at `.where`; the grant is out for signed-in callers too |
| `invalid-grant-expression`            | inactive | grant    | An `actingUser`, `blocklist`, `rateLimitRequests` or `rateLimitWindowSeconds` that isn't a string, is empty, doesn't parse, or breaks the `policy` profile (§12) |
| `grant-expression-reads-target`       | inactive | grant    | A `blocklist` or rate-limit expression reads `instance()`, or any of the four reads `actor()` (§12) |
| `anonymous-write-without-acting-user` | warning  | grant    | A write grant whose `where` names `"anonymous"` has no `actingUser`, so it admits no visitor's write; it still admits signed-in callers (§12) |
| `anonymous-grant-reads-actor`         | warning  | grant    | A grant whose `where` names `"anonymous"` is on an operation whose program, template or output reads `actor()`, so it admits no visitor (§12). Recorded at `.operation` |
| `anonymous-grant-user-key`            | warning  | grant    | A grant whose `where` names `"anonymous"` is on a `callApi` that sends the caller's own key (`{{userKey}}`), which a visitor doesn't have, so it admits no visitor (§12). Recorded at `.operation` |
| `acting-user-never-used`              | warning  | grant    | An `actingUser` on a grant whose `where` never names `"anonymous"`, or on an operation that doesn't write (§12) |
| `grant-expression-wrong-type`         | warning  | grant    | An expression that is a single value of the wrong kind, such as `actingUser: "42"` or `rateLimitRequests: "\"lots\""` (§12) |
| `acting-user-from-submitted-card`     | warning  | grant    | A `create` grant whose `where` names `"anonymous"` has an `actingUser` that reads `instance()`, which on a create is the card the visitor sends, so the visitor picks who the card is created as (§12). Recorded at `.actingUser` |
| `grant-reaches-ungranted-type`        | warning  | grant    | A `read` or `query` answer carries cards of a type no rule grants a read of (§3) |
| `render-reaches-ungranted-type`       | warning  | grant    | A `query` grant's rendered rows draw on such a type                    |
| `module-not-granted`                  | warning  | grant    | A `read` or `query` grant on a type the realm defines, in a policy with no `readSource` grant on `TsFileDef` or `GtsFileDef` for the same kind of caller, so its callers can't load the code that renders the cards (§5). Also such a grant open to visitors when no code grant is open to visitors (§12), and one for signed-in callers where the only code grant is open to visitors alone |

A card-level issue makes the whole policy uncompilable, and every signed-in
caller the realm's permissions decline gets 500 (§13). A caller who isn't
signed in gets 401 `actor-required` instead (§12). The nine warnings keep their grant
live; every other code takes its part out.

### The reach warnings

A grant on a row covers the row's whole returned representation, and nothing
fails when that reaches further than the rule reads. The two reach warnings are
what say so. They are recorded where the policy compiles, from the definitions
of the types the closure crosses, so they cost no index pass and read no card;
a link added to one of those types is found the next time the policy
revalidates.

**`grant-reaches-ungranted-type`** is recorded against a `read` or `query`
grant whose document, under the `links` strategy that governs it, carries cards
of a type no rule lets a caller read. Its `path` is the grant's, and its
`message` names the **reaching type** (the rule's), the **reached type**, and
the **field path** the closure took (`lead.office`). Each reached type gets its
own issue.

- **The strategy that governs it.** A grant on a `read`-based operation is
  served under that operation's declaration — the type's own `read` unless it
  names another; a named query grant under that query's `links`.
  An ad-hoc `query` grant has no declaration, so it is always `full`. Only
  `full` assembles anything, so only a `full` document is walked.
- **What counts as granted.** A reached type is readable when a rule on it, or
  on an ancestor, keeps a `read`, a `readSource`, or a `query` that compiled a
  filter. A rule that only lets a caller write or delete the type doesn't count,
  and neither does a `query` grant that admits nothing. The config card and
  every policy card never count, even under a catch-all `CardDef` rule.
- **The grant stays live.** Plenty of realms reach across a link on purpose;
  the warning tells you the reach is there.

The fix goes on the **granted** side:

| The grant is                | To send only the links                                                    |
| --------------------------- | ------------------------------------------------------------------------- |
| `read`-based                | `links: 'ids'` on the granted operation's declaration                     |
| A named query               | `links: 'ids'` (or `'none'`) on that query                                |
| The ad-hoc `query`          | Grant a named query that declares `links: 'ids'` instead — the ad-hoc search can't be narrowed |

Or, to share the reached cards on purpose, add a rule that lets callers read the
reached type (never offered for a policy card, the config card, or a type
every card descends from). **A declaration on the reached type never helps**: a
card carried through a link is carried whatever its own type declares. Nor
does a narrower `where` on the grant: every card it does admit still carries
its closure.

**`render-reaches-ungranted-type`** is the same check over a `query` grant's
**rendered** rows. A search row carries its prerendered HTML, and a render
draws the card's links whatever `links` says, so `links: 'ids'` doesn't clear
it. Mark every format `unshareable` in the named query's `html`
(`card-operations-authoring` §2) — the check can't tell which formats draw the
link, so one left shareable keeps the warning — or grant such a named query in
place of the ad-hoc `query`, or change the type's templates so they don't draw
the linked cards. A `read` grant serves no rendering and never records it.

**Nothing warns about a computed value.** A computed field is part of the card's
own attributes, served under every `links` strategy, and it can derive from
linked cards no rule grants: a computed `headTeacherEmail` publishes a field of
a roster card to everyone who reads the classroom. A `read` declaration's
`output` can leave it out of that read, but it still reaches the caller in a
search row and in rendered HTML. Keep such a value off any type a grant reaches,
or accept that it is published with the card.

### Seeing the issues

- **The policy card's isolated view** validates the policy as the realm compiles
  it: a "not in force" alert when it won't compile, an "inactive" mark on each
  rule and grant an issue takes out, a warning mark on a grant that stays live,
  and an issues list. It re-checks after each index pass of the realms the
  policy reads. Embedded and fitted views don't.
- **The realm's config card** shows whether the policy its pointer names is in
  force, beside the `policy` field. It is the only place the pointer problems
  (`policy-card-missing`, `not-a-policy`) appear for a card that isn't there.
  Only a caller who can read the realm the pointer names, and every realm the
  compile read, sees it.
- **`validate`**, invoked on the policy card (or `validatePolicy` on the realm's
  config card), answers the same thing as data:

  ```json
  POST <policy card's realm>/_operations
  X-HTTP-Method-Override: QUERY
  Content-Type: application/vnd.api+json;ext="https://boxel.ai/ext/operations"
  Accept: application/vnd.api+json;ext="https://boxel.ai/ext/operations"

  { "boxel:operations": [
      { "op": "invoke", "boxel:name": "validate", "href": "https://school.example/org/policies/education" }
  ] }
  ```

  Its result lists `issues`, and `rules` — the rules and grants in force, each a
  `path`. A rule or grant missing from `rules` is inactive; a grant carrying
  `admitsNothing: "unfilterable"` is kept but admits nothing. Only a caller who
  can read the policy card's realm, and every realm the compile read, may ask.
- **That gate covers the answers, not the realm's behavior.** Any writer of a
  realm may point it at a policy card in a realm they cannot read, and the
  realm then loads and applies that card on the server's own authority. Asking
  as a signed-in caller the realm declines, that writer can tell whether a
  compiling policy sits at the URL (a 500 against an ordinary refusal), and can
  exercise its grants against cards they control. So a policy's rules are not
  secret from other realms' writers, and §1 says what follows from that.

**An edit reaches the gate within seconds.** The compiled policy is
revalidated when the index of the policy card, or of a type its rules read,
moves, and at least every 5 s. Validate after each edit, then explain the
grant for a caller it should admit and one it shouldn't (§10).

## 10. Explaining a decision

A policy narrower than you meant produces refusals someone has to report. A
policy wider than you meant produces nothing at all. **`explain`** asks the
realm directly: for one caller, one card and one operation, it runs the target
realm's gate the way that invocation would, stops at the decision, and reports
how the gate reached it. Nothing is invoked, so explaining a `delete` deletes
nothing.

### Asking

Every policy card carries six explain operations, all built on base `explain`.
Each is a separate declaration because a declared param is always required:

| Operation             | Asks about                                      | Params beyond the question |
| --------------------- | ----------------------------------------------- | -------------------------- |
| `explain`             | One card or file                                | —                          |
| `explainDraft`        | One card or file, against a draft               | `draft`                    |
| `explainSearch`       | What a search returns to the caller             | `search`                   |
| `explainDraftSearch`  | The same, against a draft                       | `search`, `draft`          |
| `explainListing`      | Each card on one page of a realm                | `list`                     |
| `explainDraftListing` | The same, against a draft                       | `list`, `draft`            |

The question is three strings:

| Param       | Holds                                                                                   |
| ----------- | --------------------------------------------------------------------------------------- |
| `actor`     | The caller's Matrix user id, or `""` for a caller who isn't signed in                    |
| `target`    | The URL of a card or file. For a search or a listing, the URL of the realm it runs in   |
| `operation` | The name the invocation would invoke: `read`, `rename`, `listMine`, …                    |

**Invoke it on the policy card the target's realm names**, in the policy card's
realm. The explain asks the gate of the realm that holds the target, so the
policy card and the cards it governs can sit in different realms.

The calls below are made against the school example realms, which ship in the
boxel repository at `packages/school-example-realm`: `school-org` holds the
roster and the policy card, and `school-education` holds the classrooms. Each
deployment links `school-education`'s `realm.json` to that policy card and fills
in the roster's Matrix ids, since both differ by environment. They are shown
mounted at `https://school.example/it-admin/`, which is a different place from
the illustrative realms the earlier sections use, with a different policy. Alice
teaches Room 204 and leads Room 205; Room 206 is Ben's alone. Why can't Alice
read Room 206?

```ts
import { operations } from '@cardstack/base/operations';
import { RealmPolicy } from '@cardstack/catalog/realm-policy/realm-policy';

let explanation = await operations<typeof RealmPolicy>(policy).explain({
  actor: '@alice:school.example',
  target:
    'https://school.example/it-admin/school-education/classrooms/room-206',
  operation: 'read',
});
```

Over the wire it is an entry in an `_operations` request to the policy card's
realm, sent as `QUERY` the way `validate` is (§9), and its answer is that
entry's result:

```json
POST https://school.example/it-admin/school-org/_operations
X-HTTP-Method-Override: QUERY
Content-Type: application/vnd.api+json;ext="https://boxel.ai/ext/operations"
Accept: application/vnd.api+json;ext="https://boxel.ai/ext/operations"

{ "boxel:operations": [
    { "op": "invoke", "boxel:name": "explain",
      "href": "https://school.example/it-admin/school-org/policies/education",
      "data": {
        "actor": "@alice:school.example",
        "target": "https://school.example/it-admin/school-education/classrooms/room-206",
        "operation": "read"
      } }
] }
```

Asked by the IT admin, who reads both realms, the realm answers:

```json
{ "atomic:results": [ {
    "actor": "@alice:school.example",
    "target": "https://school.example/it-admin/school-education/classrooms/room-206",
    "operation": "read",
    "acl": { "read": false, "write": false },
    "decision": "denied",
    "reason": "predicate-false",
    "refusal": { "status": 404, "code": "target-not-found" },
    "rules": [
      { "targetType": { "module": "https://school.example/it-admin/school-code/classroom", "name": "Classroom" },
        "path": "rules[0]",
        "grants": [
          { "path": "rules[0].grants[0]",
            "where": "(.teacherIds | any(. == actor())) or (.leadTeacherIds | any(. == actor()))",
            "tier": "stored", "outcome": "did-not-hold" }
        ] }
    ]
} ] }
```

Only the `read` grant is listed: a rule's `grants` holds the grants that name
the operation asked about, so the rule's `appendActivity` grant doesn't appear.
The same question about Room 204, whose `teacherIds` list Alice, answers
`allowed`, `granted`, the grant's `outcome` as `held`, no `refusal`, and
`"admittedBy": { "rule": 0, "grant": 0 }`.

The policy card's isolated view asks the same questions from its **Explain a
decision** panel: one card, a search, or every card in a realm, each optionally
against a draft.

**The target is a card or a file, never a type.** A plain `create` mints from a
type and has no stored card to name, so it can't be explained. A named create
invoked on an existing card (`appendActivity` on a classroom) can be, since its
target is that card.

### Who may ask

- **The caller needs read on both realms**: the policy card's and the target's.
  Read is the whole requirement, not ownership. A reader of both may explain any
  actor, themselves included, and learns that actor's standing in the target
  realm's permissions (`acl`), which the realm's permissions listing shows only
  to its owners.
- **The caller is judged by their own session.** A revoked session, or one
  delegated to the policy card's realm alone, asks as nobody.
- **No grant reaches it.** Every explain operation is `nonGrantable` (§11). A
  grant naming `explain` on a `RealmPolicy` rule records
  `grants-authorization-infrastructure`. On a rule for any other type,
  `CardDef` included, it records `unknown-operation`, because only a policy
  card declares `explain`. Either way the grant is inactive, so a caller who
  reaches the policy card's realm only through a grant can't explain anything,
  their own access included.

How each refusal reads:

| Situation                                                                 | Answer                                         |
| ------------------------------------------------------------------------- | ---------------------------------------------- |
| The caller can't read the policy card's realm | That realm's own refusal before explain runs: 404 `target-not-found` where the policy card's realm names a policy of its own, its permissions' 403 where it doesn't. Either way the same bytes whatever the question asks about |
| The caller can't read the target's realm, the session is revoked or delegated, the target doesn't exist, its realm isn't served here, or its realm is archived | 404 `target-not-found`, the same bytes in every case |
| The request sends no credentials                                          | 401 before explain runs (`actor-required` where the policy card's realm names a policy) |
| The target's realm doesn't name this policy card                          | 422 `policy-not-in-force`                      |
| A draft names a type in a realm the caller can't read                     | 403 `operation-not-permitted`, refused whole   |
| The question is malformed, or asks about more than 100 decisions          | 400 `invalid-params`                           |

A caller who can't read the target's realm learns nothing from an explain about
which cards exist there.

### What it answers

The answer is a `PolicyExplanation`, the object `explain(…)` resolves to:

| Field        | Holds                                                                                    |
| ------------ | ---------------------------------------------------------------------------------------- |
| `actor`, `target`, `operation` | The question as the realm read it. `actor` is `null` for `""`          |
| `acl`        | `{ read, write }`: what the target realm's own permissions allow the actor               |
| `decision`   | `allowed`, `denied`, or `failed` (deciding faults, and the invocation would answer 500)  |
| `reason`     | Why, from the table below                                                                 |
| `refusal`    | `{ status, code }` exactly as the actor would receive it. Absent when allowed            |
| `rules`      | Every rule whose `targetType` is the target's type or an ancestor, in policy order: `targetType`, `path`, and `grants`, the rule's grants that name the operation. A rule governing the type with no grant for the operation is listed with `grants: []` |
| `admittedBy` | `{ rule, grant }`: the grant that admitted it, where one did                              |
| `draft`      | `{ issues }`, when answered against a draft                                              |
| `search`     | What the policy composes into a search, when a search was asked about                   |
| `anonymous`  | For `actor: ""`: `platformLimit` (`{ requests, windowSeconds }`), the rate limit a grant counts visitors against where it sets none (§12). Each grant's own limit and blocklist are on the grant |

**`admittedBy` indexes the explanation, not the policy.** `{ "rule": 0,
"grant": 0 }` is the first grant listed in the explanation's first rule. That
grant's `path` (`rules[2].grants[1]`) is where it sits in the policy card, in
the same form a policy issue's `path` takes.

**`refusal` is what the actor sees, not what the asker sees.** An actor who
can't read the target's realm is refused with 404 `target-not-found` whatever
the reason; `reason` still says why. Over a card+json route, the actor sees only
the status (§13).

Each listed grant carries its `path`, its `where` as written (absent for an
unconditional grant), the `tier` its predicate reads (`stored`, or `snapshot`
for one marked `snapshot: true`, which is checked against the index's copy of
the card, §8), and an `outcome`. For `actor: ""`, a grant whose `where` names
`"anonymous"` also carries `anonymous`, each of its expressions as written and
what it produced (one whose named operation reads `actor()` opens nothing, so
it carries only its issue):

| `anonymous.…` | Holds                                                                     |
| ------------- | ------------------------------------------------------------------------- |
| `actingUser`  | Write grants only. `expression`, and either the `user` it resolves to or a `failure`: `expression-failed`, `not-a-matrix-id` or `no-write`. An expression that reads `instance()` shows only `expression` where the gate didn't get as far as the card |
| `blocklist`   | `expression`, and the `entries` it produced, or `invalid` (what isn't an address or range) or `failed` (why it produced nothing). Either of those closes the grant to every visitor, and the gate leaves it out |
| `rateLimit`   | `requests` and `windowSeconds` the grant counts visitors against, `requestsFrom` and `windowSecondsFrom` (`grant` or `platform`), and `requestsExpression` / `windowSecondsExpression` where it has them |

A grant also carries `issues`, the policy issues recorded at its path, such as
`anonymous-grant-reads-actor` (§9). A grant an issue made inactive isn't
listed at all. Its `outcome`:

| `outcome`       | Means                                                                          |
| --------------- | ------------------------------------------------------------------------------ |
| `unconditional` | No `where`; the grant admits outright                                          |
| `held`          | The predicate evaluated to `true`                                              |
| `did-not-hold`  | It evaluated to anything else                                                  |
| `threw`         | It threw (§6)                                                                  |
| `not-evaluated` | The gate decided without it: an earlier grant admitted, or a refusal came first. On a search, every grant whose `where` reads the card |

| `reason`                       | Means                                                                       |
| ------------------------------ | --------------------------------------------------------------------------- |
| `acl`                          | The realm's own permissions allow this, so the policy isn't consulted and `rules` is empty |
| `granted`                      | A grant admits it                                                           |
| `no-grant`                     | No rule for the target's type grants this operation                          |
| `predicate-false`              | Grants for the operation matched, and none of their predicates held          |
| `predicate-threw`              | A predicate threw and no other grant held (`decision: failed`)               |
| `non-grantable`                | The operation is `nonGrantable` on the type or an ancestor, or is an explain or a validate |
| `query-lane`                   | The operation is built on `query`; see below                                  |
| `authorization-infrastructure` | The target is the realm's config card or its policy card, or the operation reads, writes or mints a policy card (§11) |
| `unmatchable-target`           | No rule can match: a card whose index row is an error, a file for anything but `readSource`, a path that holds nothing, or a path the realm ignores |
| `not-resolved`                 | The target doesn't carry the operation; `refusal` says how it's refused      |
| `actor-required`               | `actor` is `""`, the permissions don't let an anonymous caller in, and no grant whose `where` names `"anonymous"` opens the operation: 401 (§12) |
| `reads-actor`                  | `actor` is `""`, and the operation, as the target's type declares it, reads `actor()`, so no anonymous grant applies: 401 (§12) |
| `policy-unloadable`            | The realm can't load its policy (`decision: failed`)                         |

**An operation built on `query`, explained on a card, answers `query-lane`**,
with no rules: a query isn't invoked on a card, and its grants are judged by
the search it's named in. Explain the search instead, with `explainSearch`. A
query that is `nonGrantable` on the type or any ancestor answers
`non-grantable`, even where a subtype redeclares it without the flag. A caller
who can read the realm answers `acl`.

The answer doesn't say what to change. A `draft.issues` entry has the same
shape as a policy issue; §9 says what each code means.

### Explaining a search

`search` names the search the way its request would, and `target` is the realm
it runs in:

| The search            | `operation`             | `search`                                  |
| --------------------- | ----------------------- | ----------------------------------------- |
| A named query         | Its name (`listMine`)   | `{ "on": <type that declares it>, "params": { … } }`, `params` optional |
| An ad-hoc search      | `query`                 | `{ "filter": <the filter it sends> }`     |

A search refuses nobody it can run for; it returns rows, or none. So `denied`
on a search means the search has no rows, and carries a `refusal` only where
the search itself would be refused:

| `decision` / `reason`        | The search                                                                |
| ---------------------------- | ------------------------------------------------------------------------- |
| `allowed` / `acl`            | Runs unscoped: the actor can read the realm                               |
| `allowed` / `granted`        | Runs narrowed by the grants that admit it                                 |
| `denied` / `no-grant`        | Returns nothing: no grant on its operation compiled a filter, or each one settled for the actor didn't hold |
| `denied` / `non-grantable`   | Returns nothing: a grant compiled, and a declaration keeps the query out of every policy |
| `denied` / `not-resolved`    | Is refused as sent: no such named query, or a filter the search grammar rejects. `refusal` is the search's own |
| `denied` / `actor-required`  | Is refused 401: `actor` is `""`, the realm's permissions want someone, and the policy opens the search's operation to no visitor |
| `failed` / `policy-unloadable` | Fails: the realm can't load its policy                                  |

The answer's `search` holds `operation`; `types`, the types whose rules count
(the declaring type, or each type the filter anchors to; empty when the filter
anchors to none, so nothing can grant it); `filter`, the search's own filter as
the realm runs it; `fragment`, what the policy adds, so the search runs
`{ "every": [filter, fragment] }`; and `index`. Each listed grant carries
`filterable: true` or `false`. A grant with `filterable: false` is one that
records `policy-not-filterable` (§7). A grant whose `where` reads nothing of the
card was settled for the actor, and carries that `outcome` (`held`,
`did-not-hold` or `threw`); every other grant with a `where` is
`not-evaluated`.

**A search is as fresh as the index.** `index.pending` counts the index passes
yet to land, and `index.oldestPendingMs` how long the oldest has waited. Until
they land, the search answers from the cards as they were, while an explain of
the same card answers from it as stored. `{ "pending": 0 }` means the index has
caught up.

### Explaining every card on a page

`list` is `{ "on"?: <type>, "page"?: { "number"?, "size"? } }`, and `target` is
the realm. It explains each card on one page of the realm's cards, of `on` and
its subtypes or of every type, ordered by URL, each as its own question. The
answer is `{ explanations, page: { number, size, total } }`, plus `draft` once
when answered against a draft. A card deleted while the page is read is left
out.

**One request explains at most 100 decisions.** `size` defaults to 100 and may
not exceed it. The cap counts every explain in a batch together: a listing
counts its `size`, and any other explain counts one. So a hundred single
explains pass, and two listings of 60, or a full page and one more explain, are
refused whole with 400 `invalid-params` before anything is explained. Page
through the rest with `page.number`.

### Against a draft

The `draft` param is a policy document: an object holding the `rules` a
`RealmPolicy` card holds, as in its `data.attributes`. A whole card document
(`{ "data": … }`) is refused with 400 `invalid-params`.

- **The draft is compiled in memory, for this answer alone**, in place of the
  card the target's realm names. Nothing caches it or serves it, the policy in
  force doesn't change, and a predicate that throws in it isn't logged as the
  realm's fault. A relative `targetType` module resolves against the card in
  force.
- **It rides the explain of the card in force.** Invoke `explainDraft` (or its
  search and listing forms) on the policy card the target's realm names. A
  separate draft card that no realm names answers 422 `policy-not-in-force`
  for its own explain, draft or not.
- **The answer carries `draft.issues`**: what compiling the draft recorded, in
  the shape of the policy's own issues (§9). An empty list means it compiled
  cleanly. A grant an issue takes out is missing from `rules`, and a draft with
  a card-level issue answers `failed` / `policy-unloadable` for every question
  the policy would decide; an actor the realm's permissions admit still gets
  `allowed` / `acl`, and an operation that doesn't resolve still gets
  `not-resolved`.

**Before widening a rule, explain the draft.** Edit the rules as a draft,
explain the cases you care about — a caller the change should admit, one it
shouldn't, and the searches and listings it touches — then save the rules onto
the card in force, or onto a new card and repoint the realm at it (§1). The
panel's draft starts from the card's own rules.

## 11. Authorization infrastructure

Some cards decide who may do what. No grant reaches them:

- **The realm's config card** (`realm.json`) and **the card its `policy` names**:
  no grant reads, writes, or source-reads them, under any operation name.
- **Every `RealmPolicy` card, and every subtype's**, whether or not any realm
  names it: no grant reads, writes or creates one. Every grant on a rule whose
  type is `RealmPolicy` (or a subtype), `query` included, records
  `grants-authorization-infrastructure`.
- **Every policy-scoped search** leaves out the config card and every policy
  card.
- **An operation declared `nonGrantable`** — on the type or anywhere up its
  chain — can't be granted; a grant naming it records
  `grants-authorization-infrastructure`. A subtype that redeclares it without
  the flag doesn't make it grantable. A flag on a *subtype* is different: a
  grant on the supertype records nothing, and the realm refuses the operation
  invoked on one of the subtype's cards. A search through the supertype is
  judged by the supertype and its ancestors, so the subtype's cards can still
  come back in it. `explain` and `validate` are always
  `nonGrantable`. Mark a card's own operation this way when the card holds
  authorization — a field a predicate reads to decide access:

  ```ts
  @operation static addTeacher = {
    base: 'transform',
    params: { teacherId: StringField },
    append: { to: 'teacherIds', value: params('teacherId') },
    nonGrantable: true,
  } satisfies OperationDeclaration;
  ```

**These refusals cover an operation invoked on one of these cards, not a card
carried inside another's answer.** A granted `read`, or a row a `query` grant
admits, is served with its whole link closure. If a granted type links to the
config card or a policy card, every caller the grant admits receives that card
— the policy's whole rule list — in `included`. The realm records
`grant-reaches-ungranted-type` against such a grant (§9). Don't link to these
cards from a granted type, or declare a narrower `links` on the read or the
named query that serves it.

Only the realm's own writers can change these cards. **Keep the field a
predicate reads out of reach of the grant it authorizes**: a grant that lets a
teacher `update` a classroom whose `teacherIds` admits them lets them add
anyone to it. Grant a named operation that writes only what the caller should
change, and mark the authorization-bearing write `nonGrantable` (§14).

## 12. Callers who aren't signed in

A grant admits only signed-in callers unless its `where` names the caller who
isn't: "anyone may read the published articles", "anyone may submit
feedback". For such a visitor, `actor()` is `"anonymous"`.

### Opting a grant in

```json
{ "operation": "read", "where": "actor() == \"anonymous\" and .status == \"published\"" }
```

- **Off by default.** A grant whose `where` never names `"anonymous"` never
  admits a visitor: one with no `where`, one with `where: "true"`, and one
  whose `where` would hold for anybody (`.status == "published"`) included. So
  a grant written for signed-in callers never starts admitting everyone.
- **Naming is comparing `actor()` with `"anonymous"`** in a way that can hold
  for a visitor: `actor() == "anonymous"`, `"anonymous" == actor()` or
  `NOT(actor() != "anonymous")`. A card field compared with that text
  (`.status == "anonymous"`) names no caller, and `actor() != "anonymous"` only
  ever keeps visitors out, so neither opens the grant. Write the text in double
  quotes, as every BXL string is.
- **The grant still admits signed-in callers** the realm's permissions decline,
  evaluated with their own `actor()`, for whom `actor() == "anonymous"` is
  false. `OR(actor() == "anonymous", .ownerId == actor())` admits visitors and
  the card's owner.
- **Admitting everyone is two grants**, one naming `"anonymous"` and one for
  signed-in callers:

  ```json
  { "operation": "read", "where": "actor() == \"anonymous\" and .status == \"published\"" },
  { "operation": "read", "where": ".status == \"published\"" }
  ```
- **Eligible: an operation whose base is `read`, `readSource`, `create`,
  `update`, `delete`, `transform`, `appendContainsMany` or `appendLine`**,
  under its own name or a named one the type declares (`rename`,
  `submitFeedback`), plus the ad-hoc `query`. A `where` naming `"anonymous"`
  on a named query (`listMine`) records `anonymous-not-base-operation`, and
  the grant is inactive for signed-in callers too.
- **A `callApi` is eligible when it sends no key or only shared ones**
  (`{{apiKey}}`). The grant decides where visitors can use a shared key; a
  shared key serves them only where its owner also allows anonymous use on
  the key itself (when adding it, or from the key's page), and visitors are
  then limited by address and, where the key's owner set them, by the key's
  daily or monthly anonymous cap ([`api-integrations`](../api-integrations/SKILL.md) §2).
  Sharing or swapping a key into the workspace makes no choice: with the
  grant in place, visitors will use any key shared there, so a key that
  doesn't allow anonymous use isn't shared or swapped in. A key already
  shared when the grant is saved serves visitors if it allows anonymous use,
  and otherwise they are asked to sign in, so saving such a grant asks first:
  see [Saving a grant that opens shared keys](#saving-a-grant-that-opens-shared-keys). One with a
  `{{userKey}}` slot sends the caller's own key, which a visitor doesn't
  have: a grant naming `"anonymous"` on it records `anonymous-grant-user-key`
  and admits no visitor, and still applies to signed-in callers.
- **Prefer a named operation for a visitor's write.** It states exactly what a
  visitor may do, such as "submit this form", where a raw `update` lets them
  write any field (§14). A named operation is one invocation of its base: one
  write, counted once, made as the grant's acting user. Visitors reach it
  through `_operations`; the card+json verbs run only the built-in behavior.
- **An anonymous `query` grant must compile a filter** (§7). One that records
  `policy-not-filterable` opens search to nobody. It compiles twice: once with
  `actor() == "anonymous"` false, for signed-in callers, and once with
  `actor()` as `"anonymous"`, for visitors.

Beside `where`, a grant carries four BXL expressions that only a visitor's
request uses (below): `actingUser`, `blocklist`, `rateLimitRequests` and
`rateLimitWindowSeconds`. Each is a string of BXL, parsed under the `policy`
profile (§6), and may read the governed realm's settings
(`realmConfig("key")`), a field of the policy card (`policy("field")`), or be
written out as a constant.

### Saving a grant that opens shared keys

A save that opens a `callApi` with a shared key to visitors, where keys are
already shared into the governed workspace and approved there for use when a
card is opened, needs confirming. That is a save of the policy card a
workspace names (including creating the card a workspace already names), or
of the workspace's `realm.json` pointing at another one, from any surface: the
card editor, the code editor, the AI assistant, `boxel file write` or `boxel
realm push`/`sync`. The realm refuses it with 409
`policy-opens-shares-to-anonymous`, listing each such share: whether its key
allows anonymous use, and the operations. Someone who writes the workspace is
also shown each key's label and owner; someone who only writes the policy card
(it can live in another workspace) is shown how many keys, not which.

- **In Boxel**, the save opens a dialog listing the keys visitors will start
  using, and the keys that will refuse them until their owners allow it.
  **Save** saves it; **Don't save** leaves the policy as it was, the save
  reports as failed, and the next save of the change asks again.
- **From the CLI**, the list is printed and a terminal is asked;
  `--confirm-shared-keys` saves after printing it, and without a terminal the
  write is refused, naming the flag.
- **The confirmation covers exactly the list shown.** A share bound, or a
  key's setting changed, before the save lands makes a new list, which is asked
  about again.
- **Each listed key's owner hears about it** on their keys page the next time
  they open it. The owner of a key that already allows anonymous use is told
  that visitors now use it in the workspace. The owner of a key that doesn't
  is asked to approve anonymous use: they can allow it for the key and set an
  optional cap, or decline. Declining leaves the key refusing visitors there,
  and the same request isn't made again.

A save that opens nothing new to visitors, or opens only operations no share
is approved for when a card is opened, saves as any other.

**As the AI assistant**, write the policy as asked; Boxel shows the person the
dialog, and only they confirm it. Say in your reply which shared keys the
change lets visitors use now, and that the owners of the others will be asked
to approve anonymous use on their keys page. When a write fails because the person chose **Don't save**,
report that the policy wasn't saved; if they then ask you to save it, write it
again and Boxel asks them again.

### Scoping an anonymous grant

A named operation whose program, template or output reads `actor()` can't be
run by a visitor. A grant naming `"anonymous"` on one records
`anonymous-grant-reads-actor` as a warning at its `operation`, opens nothing to
visitors, and stays live for signed-in callers. A subtype that redeclares an
opened operation so that it reads `actor()` admits no visitor to the subtype's
cards, while the grant still serves the parent type's cards. Explaining that
subtype's refusal with `actor: ""` answers reason `reads-actor`. Where the
rule's own type reads `actor()`, the policy opens the operation to no visitor,
and the reason is `actor-required`. Scope an anonymous grant by what the card
holds:

| Means                              | `where`                                             |
| ---------------------------------- | --------------------------------------------------- |
| Published articles only            | `actor() == "anonymous" and .status == "published"` |
| Open tickets only, on an `update`  | `actor() == "anonymous" and .status == "open"`      |
| Every card the rule's type covers  | `actor() == "anonymous"`                            |

A visitor-wide grant on `CardDef` opens every card in the realm. Name the
narrowest type, and scope by the card wherever one card differs from another.

**A visitor receives everything a granted row carries** (§3, §9): a granted
`read` or a row a `query` grant admits arrives with its whole link closure in
`included`, and a search row with its prerendered HTML, which draws the linked
cards too. So opening a type to visitors also shows them every card its rows
link to, including cards no anonymous grant opens. Heed the reach warnings on
an anonymous grant. A named query with a narrower `links` can't be opened to
visitors, so for search the fix is the type itself: open only types whose
links are safe to show, or declare `links: 'ids'` on the type's `read` for a
direct read.

### Acting users for writes

Every anonymous write, through a base operation or a named one built on a
write, is made **on behalf of the user the grant's `actingUser` names**. It is
a BXL expression that produces a Matrix user id:

| Source                          | `actingUser`                     |
| ------------------------------- | -------------------------------- |
| A setting in the realm's `config` | `realmConfig("submitter")`     |
| Written out                     | `"@writer:example.com"`          |
| A field of the policy card      | `policy("writer")`               |
| A user the target card names    | `instance().owner` (never on a `create`) |

```json
{ "operation": "create", "where": "actor() == \"anonymous\"", "actingUser": "realmConfig(\"submitter\")" }
```

```json
"config": { "submitter": "@feedback-bot:school.example" }
```

- **Only a visitor's write uses it.** A signed-in caller's writes are made as
  themselves, and reads never use it. An `actingUser` on a grant whose `where`
  never names `"anonymous"`, or on an operation that doesn't write, records
  `acting-user-never-used` as a warning.
- **A write grant naming `"anonymous"` with no `actingUser` records
  `anonymous-write-without-acting-user`** as a warning. The grant stays live
  for signed-in callers and admits no visitor's write. One expression per grant
  is enough: an invocation writes only its one target, or the one card a create
  mints.
- **It is evaluated at every write.** It must produce a Matrix user id, and
  that user must hold write on the realm's own permissions. When it doesn't,
  the grant admits no visitor's write, and the visitor gets the 401 unless
  another grant admits it. The failure is one of:

  | Failure             | Means                                                                 |
  | ------------------- | --------------------------------------------------------------------- |
  | `expression-failed` | The expression produced no value, such as a `realmConfig` key the realm doesn't set |
  | `not-a-matrix-id`   | It produced something that isn't a Matrix user id, `"anonymous"` included |
  | `no-write`          | The user it names may not write the realm                              |

  Changing the setting or field it reads, or taking the user's write, takes
  effect on the next write, with no edit to the grant.
- **`instance()` is the card being written**: the stored card for an `update`
  or `delete`, the card being minted for a `create`. `instance().owner` makes
  a visitor's edit as the user the card names, so that user must hold write on
  the realm. On a `create`, that card is the one the visitor sends, so the
  visitor fills in `owner` and picks any of the realm's writers to write as.
  An `actingUser` that reads `instance()` on a grant that admits a visitor's
  `create` records `acting-user-from-submitted-card` as a warning; read the
  user from `realmConfig` or the policy card instead.
- **A constant of the wrong kind** (`"actingUser": "42"`) records
  `grant-expression-wrong-type` as a warning, and admits no visitor's write.
- **The write carries the acting user's identity**, wherever the realm records
  who wrote. It never brings realm-owner authority: `realm.json` and policy
  cards stay out of reach (§11), and no grant writes module source.
- **`actor()` is still `"anonymous"`, never the acting user.** A grant
  `where .ownerId == actor()` never lets a visitor edit the acting user's own
  cards.
- **A visitor writes through the card+json routes (`POST`, `PATCH`,
  `DELETE`) and `_operations`.** The `card+source` write and `_atomic` stay
  closed to visitors, whatever the grants say.
- **Name a dedicated account, not a person who edits the realm.** A visitor's
  write is indexed as the acting user's own, and that user's reads wait for
  visitors' writes to index as they wait for their own. A busy public form
  would slow its editor down.
- **Different grants can write as different users**: feedback as
  `realmConfig("feedbackWriter")`, sign-ups as `realmConfig("signupWriter")`.
  Each write in a batch is checked against its own grant's user, but the
  batch's index pass is credited to the first entry's.

**Where the user comes from decides who chooses it.** The acting user must
already hold write on the realm, so an `actingUser` can only hand visitors'
writes to one of the realm's writers. Who picks which writer differs by
source: a `realmConfig` setting is chosen by the realm's own writers, since
changing `realm.json` takes write on the realm; a constant or a `policy()`
field is chosen by whoever writes the policy card, which can live in another
realm (§1); and an `instance()` field is chosen by whoever wrote the card. On
an `update` or `delete` that is whoever last wrote the field, and on a
`create` it is the visitor. When the policy card's writers aren't the realm's,
read the user from `realmConfig`, and never read it from `instance()` on a
grant that admits a visitor's `create`.

A write grant's `where` is judged as every write's is: on the stored card
before the write, for an `update` or `delete`, and on the card being minted, for
a `create` (§4).

### Blocklists and rate limits

Each grant that names `"anonymous"` limits and blocks visitors by address,
with expressions of its own:

```json
{
  "operation": "read",
  "where": "actor() == \"anonymous\" and .status == \"published\"",
  "blocklist": "realmConfig(\"blockedIps\")",
  "rateLimitRequests": "realmConfig(\"visitorRequests\")",
  "rateLimitWindowSeconds": "60"
}
```

with the governed realm's `realm.json` holding:

```json
"config": { "blockedIps": "192.0.2.1, 10.0.0.0/8", "visitorRequests": 30 }
```

- **`blocklist`** produces the IP addresses and CIDR ranges the grant refuses:
  a comma-separated string (`"192.0.2.1, 10.0.0.0/8"`) or a list. Read it from
  a setting, `realmConfig("blockedIps")`; from the policy card,
  `policy("blockedIps")`; or write it out, as the JSON value
  `"\"192.0.2.7, 198.51.100.0/24, 2001:db8::/32\""`. Blank entries are
  dropped, so `""` blocks nothing. A range whose address has bits set below
  its prefix (`192.0.2.1/24`) isn't a range.
- **A blocklist fails closed.** An entry that isn't an address or a range, a
  value that is neither a string nor a list, or an expression that produces
  nothing (a `realmConfig` key the realm doesn't set) closes the grant to every
  visitor until it is fixed, since dropping it would let in the caller its
  author meant to keep out. Keep the setting in place, set to `""`, for a
  grant that blocks nobody.
- **`rateLimitRequests` and `rateLimitWindowSeconds`** produce whole numbers:
  how many requests one address may make through the grant in a window of
  that many seconds, `requests` from 1 to 1,000,000 and `windowSeconds` from 1
  to 86,400. Each one left out, or producing anything else (a number outside
  those bounds, a fraction, a string such as a `config` value written as
  `"30"`), is the platform's default for that half: 300 requests per 60
  seconds unless the server is configured otherwise. A grant's views show the
  limit it counts against, defaults included. A constant of the wrong kind
  (`"rateLimitRequests": "\"lots\""`) records `grant-expression-wrong-type` as
  a warning.
- **Each grant counts on its own**, per address; an IPv6 caller is counted by
  the `/64` their address is in. Two grants in a realm don't share a count. A
  request is charged to the grant that admitted it.
- **Only an admitted request counts.** A refused one costs the visitor nothing,
  and neither does a scoped stylesheet served with a card's markup.
- **A capability check counts once per pair it asks about**, charged before
  anything is checked, from the same budget as the visitor's reads. A check
  that doesn't fit in what's left of the window gets 429 whole, and answers
  nothing; one asking about more pairs than `requests` always does.
- **The address is the one the platform's proxy reports**, never a header the
  visitor sends. A visitor whose address can't be determined is refused.
- **Signed-in callers are never limited or blocked** by these expressions, and
  neither are the platform's own services, such as a prerender of your cards.
  Their requests are counted, not refused.

**A blocklist or rate limit can't read the target card, and no expression
reads `actor()`.** A `blocklist` or rate-limit expression calling `instance()`,
or any of the four calling `actor()`, records `grant-expression-reads-target`,
and the grant is inactive. They are settled once per request, before the card
it names is read:

- a blocked or over-limit address gets the same 401 or 429 whatever card it
  names, so the answer says nothing about whether a card exists or what it
  holds;
- a refusal costs the realm no card load;
- a search is checked and charged once, not once per card it finds.

`actor()` would always be `"anonymous"` there, so it would tell an expression
nothing. `actingUser` is settled for a write, once the card is known, so it
alone may read `instance()`.

**How a request is admitted.** The realm takes the grants that open what the
request runs to visitors, in policy order, and settles each one's blocklist
and limit for the visitor's address. Grants whose blocklist names the address,
or fails, drop out; with none left, the visitor gets the 401. For a request
that counts, grants whose budget for the address is used up drop out next;
with none left, the visitor gets 429. Only the grants left may admit the
request, judged by their `where` as any grant is.

An expression that doesn't parse, is empty, isn't a string, or breaks the
`policy` profile records `invalid-grant-expression`, and the grant is
inactive.

**`policy("field")` reads the policy card's own stored fields.** `RealmPolicy`
declares only `rules`, so a blocklist or acting user kept on the policy card
needs a subtype that declares the field, and the policy card adopts from it:

```gts
import { field, contains } from '@cardstack/base/card-api';
import StringField from '@cardstack/base/string';
import NumberField from '@cardstack/base/number';
import { RealmPolicy } from '@cardstack/catalog/realm-policy/realm-policy';

export class SitePolicy extends RealmPolicy {
  @field writer = contains(StringField);
  @field blockedIps = contains(StringField);
  @field visitorRequests = contains(NumberField);
}
```

A rate limit read from a field needs a `NumberField`: a `StringField` holding
`"30"` produces a string, and the platform's default applies.

### What visitors see

| Situation                                                   | Answer                                              |
| ----------------------------------------------------------- | --------------------------------------------------- |
| No anonymous grant admits the request, a matching grant's `where` doesn't hold, or the card is missing | 401 `actor-required`, the same bytes in every case |
| Every grant that would admit it blocks the visitor's address, or has a blocklist that fails | 401 `actor-required`, as above |
| The policy won't compile                                    | 401 `actor-required`, as above: a policy that won't compile opens nothing to visitors. Check its issues (§9) |
| The visitor is over the limit of every grant that would admit it | 429 `rate-limited`, with `Retry-After` in seconds; nothing is done |
| The limit can't be counted right now                        | 503 `rate-limit-unavailable`, with `Retry-After`; nothing is done |
| An anonymous create is admitted                             | The realm chooses the new card's id (§4)            |
| The realm is archived, and a grant admits the visitor      | 403 `archived`, as a signed-in caller is told; a visitor no grant admits still gets the 401 |
| A batch has an entry no grant admits                        | 401 `actor-required` for the whole batch; nothing is written |
| A batch would take the visitor over the limit               | 429 `rate-limited` for the whole batch; nothing is written |

**A write counts once, and a batch once per entry**, after the whole batch is
admitted and before anything is written, so a refused write costs nothing. A
batch is charged to the grant that admitted its first entry, and one with more
entries than that grant's `requests` is refused with 429 however long the
visitor waits, so set `rateLimitRequests` above the largest batch a visitor's
page sends.

A visitor never learns whether a card exists from a refusal: wherever a caller
who can't read the realm would get a 404, a visitor gets the 401 above, so a
card no grant admits, a missing card and a path the realm refuses all answer
alike, for reads and writes.

**Search.** An anonymous `query` grant narrows a visitor's ad-hoc `_search`
and `_federated-search` the way it narrows a signed-in caller's (§7). Only
grants whose `where` names `"anonymous"`, and whose blocklist and limit let the
visitor in, are composed, each with `actor()` read as `"anonymous"`. A named
query is never opened to visitors.

- **A search counts once**, in each realm it is scoped in. A search no grant
  scopes costs the visitor nothing.
- **A realm's own `_search`** answers 429 once the visitor's budget is spent
  through every `query` grant that would admit them.
- **In `_federated-search`**, each realm named answers for itself: one whose
  policy opens `query` to visitors serves the rows its grants admit, one whose
  policy doesn't, or whose grants all block the visitor, serves no rows, and
  one whose limits the visitor has used up is counted failed
  (`meta.incomplete: true`) while the others still answer. When none of the
  realms named that the visitor can't otherwise read admits them, blocked
  everywhere included, the whole search is 401, even if a public realm named
  beside them would have answered. A visitor's federated search may name only a few private realms (two by
  default); one naming more is 401. Archived realms are never asked.
- **A named query is 401 to a visitor** in a realm whose permissions don't
  already let anyone read, on its own `_search` too.

**Hiding a control that won't work.** `@context.canInvoke` answers for a
visitor too, so a public page can hide its submit button when `canInvoke`
answers `false`. Hide on `false`, never on `undefined` (`card-operations-authoring`
§3): a prerender, a pending check and a failed one all answer `undefined`, and a
page that gates on `true` serves visitors no button. In a realm whose
permissions don't already let anyone read, every pair a page asks about counts
against the visitor's limit, so a public page that gates thirty
controls spends thirty of it on each load. Ask only about the controls a
visitor can act on, and set `rateLimitRequests` with those checks in mind.

**A realm whose permissions already let anyone read** (`"*": ["read"]`)
answers anonymous reads on its permissions alone, without the policy or any
grant's limit or blocklist. A policy only widens (§3). A visitor's writes
there still need an anonymous grant, and are limited and blocked by it like
any other realm's.

**Explain a visitor's request** with `actor: ""` (§10). Where the policy opens
the operation to visitors, the gate judges the question against the grants
whose `where` names `"anonymous"`, and a write against the same acting-user
check the write itself gets. So does `canInvoke` for a visitor's write. A
question names no address, so a blocklist leaves a grant out only when it
can't be read, not because it lists addresses. The answer says what a visitor meets that a signed-in caller doesn't
(§10): `anonymous.platformLimit`, and on each grant naming `"anonymous"`,
`anonymous.actingUser` (the user a write grant's expression resolves to, or
`expression-failed`, `not-a-matrix-id` or `no-write`), `anonymous.blocklist`
(the entries it produced, or why it closes the grant) and `anonymous.rateLimit`
(the limit and where each half comes from). A visitor every grant turns away
for its acting user or blocklist answers `no-grant`. The policy card's
**Explain a decision** panel shows the same; leave the person empty to ask
about a visitor.

### Worked examples

**Published articles are public.** Visitors may open and list published
articles, and nothing else:

```json
{
  "targetType": { "module": "../article", "name": "Article" },
  "grants": [
    { "operation": "read",  "where": "actor() == \"anonymous\" and .status == \"published\"" },
    { "operation": "query", "where": "actor() == \"anonymous\" and .status == \"published\"" }
  ]
}
```

Both grants: a `read` grant puts nothing in search results, and a `query`
grant opens no card (§3). `status` must be a `StringField` for the `query`
grant to compile (§7). Check what a published article's `read` carries in
`included` (`grant-reaches-ungranted-type`, §9): a visitor receives all of it.
Signed-in callers the realm's permissions decline get neither grant; add a
`read` and a `query` without `actor() == "anonymous"` for them. Visitors also
need the code that renders an article: add a rule on `TsFileDef` granting
`readSource` with a `where` that names them (§5), or `validate` records
`module-not-granted` (§9).

**A public feedback form.** Visitors may submit `Feedback` cards, written as a
dedicated user, at a tighter rate than the platform's, from any address the
realm doesn't list:

```json
{
  "targetType": { "module": "../feedback", "name": "Feedback" },
  "grants": [
    {
      "operation": "create",
      "where": "actor() == \"anonymous\"",
      "actingUser": "realmConfig(\"submitter\")",
      "blocklist": "realmConfig(\"blockedIps\")",
      "rateLimitRequests": "5",
      "rateLimitWindowSeconds": "300"
    }
  ]
}
```

with the governed realm's `realm.json` holding:

```json
"config": { "submitter": "@feedback-bot:school.example", "blockedIps": "" }
```

and `@feedback-bot:school.example` holding write on the realm. Visitors can't
read what they submitted, since no grant opens `read`. The form's card hides its
submit button when `@context.canInvoke('create', Feedback, { realm })` answers
`false`, naming the realm because a visitor has no default writable realm.

## 13. Refusals a caller sees

How the realm refuses depends on whether the caller may read the realm:

| Situation                                   | Caller who may read the realm                     | Caller who may not                     |
| ------------------------------------------- | ------------------------------------------------- | -------------------------------------- |
| No grant holds                              | 403 `operation-not-permitted`                     | 404, identical to "not found"           |
| The type doesn't carry the operation        | 405 `operation-not-allowed`                       | 404, identical to "not found"           |
| A predicate threw and no other grant held   | 500 `policy-predicate-failed`                     | 404, identical to "not found"           |
| The policy won't compile                    | 500 `internal-error`, "Policy unavailable" (on writes) | 500 `internal-error`, "Policy unavailable"; 401 `actor-required` for a caller who isn't signed in |
| Nobody signed in, and no anonymous grant admits it | —                                          | 401 `actor-required`                    |
| Nobody signed in, over each admitting grant's limit | —                                        | 429 `rate-limited`, with `Retry-After` (§12) |

The codes are the `code` on an `_operations` error, and on a search. A card+json
route answers with the same status and a title, and its body carries no `code`,
so over those routes the status is the whole answer. The routes that serve
stored bytes answer "Policy unavailable" with a code of `500`.

A caller who may not read the realm learns nothing about what exists from the
answer: a card that isn't there and a card a grant refuses answer the same
bytes. **Timing is not concealed.** A card that isn't there is refused before
any grant is matched, while a card refused because a matching grant's
predicate didn't hold had that predicate evaluated against it, so a caller who
measures carefully can tell the two apart. The realm doesn't pad either
answer. A realm with no policy answers with its permissions' own 401 and 403.
For the rest of an operation's refusals, see `card-operations-authoring` §5.

**An archived realm** answers with its seal, a 403 with code `archived`:

- A caller the realm's permissions allow meets the seal everywhere, whatever
  the policy grants them.
- A caller only the policy admits meets it only where a grant would admit them.
  Everywhere else they get the answer the realm gives while it is active, so
  the seal tells them nothing a grant doesn't.
- On the routes that serve stored bytes (the `card+source` read, and the file
  and module serve of a file or a card's `.json`), every signed-in caller of an
  archived, private realm with a policy meets the seal on a `GET`, whether or
  not a grant reaches the file. A `HEAD` from a caller who can't read the realm
  gets the realm's discovery answer. The scoped-CSS serve shows the seal only
  where it would serve a stylesheet, so a hash it doesn't hold is not found,
  archived or not.

## 14. Choosing what to grant

The realm accepts a policy that compiles, and it compiles plenty of policies
that let a caller widen their own access. The engine can't tell a grant you
meant from one that hands over the keys. The calls below are yours to make, and
each one has a counterpart in the school example realms (§10):

```json
{ "targetType": { "module": "../../school-code/classroom", "name": "Classroom" },
  "grants": [
    { "operation": "read",
      "where": "(.teacherIds | any(. == actor())) or (.leadTeacherIds | any(. == actor()))" },
    { "operation": "appendActivity", "where": ".teacherIds | any(. == actor())" }
  ] },
{ "targetType": { "module": "../../school-code/service-plan-schedule", "name": "ServicePlanSchedule" },
  "grants": [
    { "operation": "read", "where": ".providerId == actor()" },
    { "operation": "listMySchedules", "where": ".providerId == actor()" }
  ] }
```

### A named operation, not a raw base

**Prefer a named operation to a raw `update` wherever a grant rests on a
field.** A write's predicate is judged against the card as it stands before the
write (`card-operations-authoring` §6). So a teacher granted `update` because
`teacherIds` lists them may send a `teacherIds` of their own in the same
request. The grant holds, because the old list admitted them, and the new list
says whatever they wrote. They can add a colleague, remove the lead teacher, or
take the classroom for themselves. Nothing in the policy can stop it: a
predicate never sees what the caller sent (`params()` is refused, §6).

A named operation constrains what it writes. `Classroom.appendActivity` mints a
`ClassroomActivity` and fills it with values the caller can't forge:

```ts
@operation static appendActivity = {
  base: 'create',
  of: ClassroomActivity,
  params: { note: StringField },
  fill: {
    note: params('note'),
    author: actor(),
    classroom: instance('id'),
  },
} satisfies OperationDeclaration;
```

The caller chooses the note and nothing else. `author` is always the caller,
`classroom` is always the card it was invoked on, and nothing about it can
reach `teacherIds`. The predicate's inputs stay outside the caller's reach, so
whether the grant holds tomorrow doesn't depend on anything the caller does
today. **The policy decides whether; the operation decides what.**

That is why **a grant on a named operation never grants its base** (§3). If
granting `appendActivity` granted `create`, the caller could mint a
`ClassroomActivity` with any `author` they liked. If granting `rename` granted
`transform`, they could run any program over the classroom. The narrowness is
the whole reason to declare the operation.

**A field one grant reads must be out of reach of every grant, not just its
own.** In a batch, each entry is judged against what the entries before it in
a serial run left, or, in a parallel group, against what the group started
from (`card-operations-authoring` §3). So a granted `update` of `status`,
followed in the same batch by a `delete` whose grant reads `.status == "draft"`,
deletes a card the caller could never have deleted on its own. Check each
grant's predicate against everything every other grant on the type can write.

A named operation is only as narrow as its declaration. One that writes a
caller-supplied `params` value into the field a grant reads is a raw `update`
under another name. The `addTeacher` in §11 is one, so it is `nonGrantable`.
Check what each granted declaration's `fill`, `set` and `append` write, and
whether any of it comes from `params`.

In the school example, Alice teaches Room 204 and may log activities there. A
raw `update` of Room 204's `teacherIds`, sent as Alice, is refused with the 404
she gets for anything the policy doesn't grant, and the stored list is
unchanged. Explaining it answers `no-grant`, with the `Classroom` rule listed
and its `grants: []`.

### Keep authorization-bearing fields out of reach

**Never grant raw `update`, `transform`, `appendContainsMany` or `delete` on
a type whose predicate reads a field those operations can change, unless every
caller who passes the predicate is trusted with the consequence.** `update` and
`transform` rewrite the field. A raw `appendContainsMany` lets the caller name
the field and the items, so it adds anyone to `teacherIds`. `delete` removes
the field along with the card, so any caller the predicate admits decides alone
whether the card and its roster go on existing.

Sometimes the consequence is fine. Take a draft whose `ownerId` admits its
owner to `update`: they can hand the draft to someone else, and that's an
ordinary part of owning a draft. It is not fine when the field is a roster
someone else maintains. A teacher should never edit the list of who teaches.

Where the people who change the authorizing data and the people it authorizes
are different audiences, **keep the authorizing data where no grant writes
it**:

- **On a different card, in a realm the policy grants nothing in.** The school
  keeps its staff roster in `school-org`, which no grant reaches. The working
  data, the classrooms and schedules, is in `school-education`.
- **On the governed card, written only by the realm's own writers.** A predicate
  reads the card it judges, and a stored link is only a URL, so a classroom also
  stores its teachers' Matrix ids in `teacherIds`, mirrored from the roster
  links. The policy grants no write that reaches `teacherIds`: a
  raw `update` would write the mirror like any other field, so none is
  granted. The IT admin syncs the mirror with an ordinary `update` the realm's write permission
  admits.
- **Behind a `nonGrantable` operation**, where the card itself declares the
  write (§11).

An anonymous write grant needs the same care. Every visitor's `actor()` is
`"anonymous"`, so its predicate tells one visitor from another only by the
card, and every visitor who satisfies it gets the write. The write is made as
the grant's acting user (§12), which never widens
what the grant reaches. Never open a raw write to visitors on a type whose
predicate reads a field that write can change. Open a named operation that
writes only what a visitor should change instead.

A mirror decides on what it holds, not on the roster it copies. Until someone
syncs it, a teacher removed from the roster still reads their old classroom.
That gap is a human step. Give the people who keep the mirror a way to see when
it disagrees with its source: the school's classroom page warns when the two
differ.

### When `snapshot: true` is acceptable

A snapshot grant reads the card's stored fields as they are now, and its
computed values and `searchable` linked cards' fields as the index last saw
them (§8). Those indexed values open a time-of-check gap the length of the
index's delay. Suppose a classroom has a computed `headTeacher`, or a
`searchable` link to its coordinator's roster card that the predicate reads
the coordinator's Matrix id through. Change the computed value's inputs, or
the id on the roster card, and the grant keeps deciding on the old value until
the classroom is indexed again. Re-pointing the link revokes at once, because the
indexed fields count only while the stored link still names the card the index
expanded (§8). A grant that should hold through the new link's target waits for
the reindex, and admits nothing until then. The delay is usually short, but it grows while the realm's
index is busy. The gap applies to writes too: the write lock judges a snapshot
grant against the same indexed copy.

The annotation is acceptable when **a removed person keeping access a little
longer harms nobody**:

- A `read` of information they recently had anyway, such as a schedule they
  provided last week.
- A value that changes rarely and is never revoked under pressure.
- A `query` grant: every search is already as fresh as the index (§7), so the
  snapshot adds no new gap to that lane.

It isn't acceptable when **revocation has to be immediate**:

- A grant that writes or deletes, where the removed person is the one racing the
  change.
- Access that is withdrawn for cause, such as someone leaving, a safeguarding
  concern, or a compromised account.
- Any grant whose consequence you'd have to undo by hand.

For those, put the value the predicate reads in a stored field, as the school
does with `teacherIds` and `providerId` in place of reading through the roster
links. A stored predicate decides on the card as it is stored at the moment of
the request, so a change to the classroom takes effect on its next request.
The gap moves to whatever keeps the stored field current, which you control.

A snapshot grant also admits nothing for a card the index hasn't seen, or whose
index row is an error. A card created a moment ago is refused through such a
grant until it is indexed. That direction fails closed, but a caller may report
it as a refusal.

### `read` and `query` are separate grants

**A `read` grant never lists a card, and a `query` grant never opens one**
(§3, §7). A schedule's provider can read it and list it because the rule
grants both, `read` and the named `listMySchedules`, each with
`.providerId == actor()`. In the school example, a provider who sends an ad-hoc
search over schedules finds nothing: no grant names `query`, and the `read`
grant contributes nothing to a search.

Writing the same predicate twice is **the cost of the separation, not a smell**.
Each grant states one lane's condition, and the lanes differ:

- **They are judged differently.** A `read` predicate is evaluated against the
  card as stored. A `query` predicate is compiled to a filter over the index,
  so it must stay inside what compiles (§7). The gate accepts some predicates,
  `realmConfig()` beside a read of the card and string functions among them,
  that no filter can express.
- **They can mean different things.** Being allowed to open a card you were
  sent a link to is different from being allowed to enumerate every card like
  it.
- **Each can change without the other.** Narrowing who may list a type
  shouldn't silently narrow who may open a card they were already given.

When the two are meant to match, write them identically and change them
together. Explain both after an edit: `explain` for the read and
`explainSearch` for the listing.

### Reading an explanation

`explain` answers what the policy decides (§10). What to make of the answer:

1. **Read `acl` first.** `"acl": { "read": true }` with `reason: "acl"` means
   the policy was never consulted. The actor gets in through the realm's own
   permissions, and no edit to the policy changes that. If they shouldn't get
   in, change the realm's permissions. For `actor: ""`, read `reason`:
   `actor-required` means the policy opens the operation to no visitor,
   `reads-actor` that the operation depends on who asks, and `no-grant` with
   grants listed that each grant naming `"anonymous"` was turned away: read
   its `anonymous.blocklist` and `anonymous.actingUser` (§12).
2. **Read `reason` for the cause and `refusal` for the experience.** The two
   differ on purpose. Alice's read of Room 206 answers `predicate-false`, but
   she sees 404 `target-not-found`, the same as for a classroom that doesn't
   exist. A report that "the card isn't there" from someone without realm read
   is a refusal until an explain says otherwise.
3. **`no-grant` and `predicate-false` point at different edits.**
   - `no-grant` with no rules listed means no rule governs the target's type.
     Check the `targetType` and whether the rule names an ancestor of the card's
     type, not a subtype.
   - `no-grant` with a rule listed and `grants: []` means the rule governs the
     type but no live grant names this operation. Either nothing grants it, as
     with a raw `update` beside a granted named operation, or the grant has an
     issue that takes it out. Run `validate` (§9).
   - `predicate-false` means the right grant was found and its condition didn't
     hold for this card and actor. Look at the card's data before the
     predicate: a stale mirror is the usual cause.
4. **Check each grant's `tier` before you trust its `outcome`.** A `stored`
   outcome reflects the card as it is now. A `snapshot` outcome
   reflects the index's copy of the card's computed and linked values (§8), so
   a `did-not-hold` just after an edit to one of those can be the index
   catching up. Explain again once it has. Every `query` grant's outcome comes
   from the index too: `index.pending` on a search explanation says whether
   that index has caught up.
5. **`threw` is a bug in the policy, not a refusal.** When no other grant
   held, the answer is `decision: "failed"` and the invocation would answer
   500 to a realm reader. When another grant held, the explanation can
   be `allowed` with a `threw` grant inside it. The bug is still there, and it
   refuses the first card that only the throwing grant could admit. Guard the value the predicate
   assumed (§6).
6. **An unexpected `allowed` is the case to chase.** Follow `admittedBy` into
   the explanation's `rules`, then that grant's `path` into the policy card, and
   read the predicate that held. A policy wider than you meant produces no
   reports, so look for this one deliberately.

**The loop around an edit:** explain the draft before you save it, and the live
policy after. Before saving, `explainDraft` the cases the change is meant to
affect: a caller it should admit, one it shouldn't, and an operation it must
still refuse, such as the raw `update` beside a named one. Add `explainSearch`
for any listing it touches. Check that `draft.issues` is empty. Once the edit
has reached the gate (§9), explain the same cases against the live policy and
compare the answers.

## 15. Before calling a policy done

- The policy card's issues list is empty, or holds only warnings you mean to keep.
- Every membership test is `any(. == actor())`, parenthesized inside `or`/`and`.
- Every grant that needs a computed or linked value says `snapshot: true`, and
  no `create` grant does.
- Every `query` grant compiled a filter or reads nothing of the card (no
  `policy-not-filterable`), and every card a teacher should open also has a
  `read` grant.
- Every `read` or `query` grant has a `readSource` grant on `TsFileDef` for the
  same kind of caller (no `module-not-granted`, §5).
- Every caller a `read` or `query` grant admits is also admitted by the code
  grant's `where`: where the two read different lists, the code grant's is a
  superset of every card's, and a code grant narrowed by path still covers
  every granted card's module. `validate` compares only kinds of caller, signed
  in or visitor, and never evaluates the code grant's `where`.
- Every `readSource` grant on a card type is meant to reveal the whole stored
  document, and every file rule names the narrowest `FileDef` that fits.
- No grant can write the field its own predicate reads. Every write grant that
  rests on a field names a named operation, not a raw `update`, `transform`,
  `appendContainsMany` or `delete`, unless everyone it admits is trusted with
  that write (§14).
- Every `snapshot: true` grant can tolerate a removed person keeping access
  until the card is indexed again (§14).
- Every grant whose `where` names `"anonymous"` is on an eligible operation
  (no named query), preferably a named one for writes, scoped by what the card
  holds, and meant to reach every visitor; every grant that doesn't name it is
  meant for signed-in callers only. Every anonymous write grant has an
  `actingUser` that resolves to a user with write on the realm, chosen by
  whoever should choose it. Each grant's `blocklist` reads (an unset setting
  closes the grant), and its `rateLimitRequests` suits what a visitor may do
  through it.
- You explained each grant for a caller it should admit and one it shouldn't
  (§10), and explained a draft before widening any rule.
