---
name: iada
description: Rank the parts of a system by how many parties must change when each part changes (Identifiers, then API, then Data, then Architecture) and catch inversions where a cheap-to-change layer has leaked into an expensive one. Use when designing or reviewing identifiers, REST or package APIs, schemas, storage, or a data model; when someone says "/iada" or asks whether a change is safe or a name is stable; or when a design question turns on "what would this cost to change later".
---

# IADA: what is hard to change comes first

A doctrine I worked under for years, restated from memory and in my own
words. Four layers, ordered by the cost of changing them. The cost is
measured in *parties*, not lines: how many people or systems outside this
repo would have to act if this changed.

| layer | what it holds | who must change if it changes |
|---|---|---|
| **Identifiers** | names others store: ids, URIs, paths, enum values, relation names | nobody can; they are permanent |
| **API** | contracts others call: endpoints, package exports, schemas *as published*, CLI flags | every consumer, but they can be told |
| **Data** | the shape you persist: tables, documents, fixture files, internal schemas | this repo and its migrations |
| **Architecture** | how the work gets done: engine, services, libraries, storage choice | this repo only |

The doctrine is the ordering and one rule that follows from it:

> Nothing from a lower layer may appear in a higher one.

A storage key or region inside an identifier, a table shape inside an
API, a version segment inside a name, a modelling choice you are still
revising inside an id: each is an inversion. Inversions are how systems become brittle. The
lower layer can no longer change without dragging the higher one, and the
higher one was the part that was never supposed to move.

## The consequences

1. **Effort tracks the ranking.** Identifiers get the most care and the
   slowest review; architecture gets the least. Spend design time at the
   top, and change freely at the bottom.
2. **A minted identifier cannot change, ever.** It outlives the system
   that minted it, the API that operated on it, and the team that knew
   what it meant. It ends up in spreadsheets, emails, printed documents,
   other people's databases, places nobody imagined. You never get to
   delete the old ones. At best you keep a table mapping old to new, and
   you keep it forever. Design every identifier as if it will be dug up as
   archaeology.
3. **Identifiers are opaque strings.** Consumers compare them for equality
   and store them; they never parse, split, sort, or infer from them. A
   prefix or namespace saying *who minted it* is allowed and useful, since
   it lets ids from different owners share one space without colliding.
   Anything about the *content* is not. The canonical trap is a location
   in the id read as "where the record lives": the home moves, the record
   gets replicated or migrated, and one day the authoritative copy sits
   somewhere the id says it doesn't. The moment anyone interprets an id,
   every fact it happens to encode becomes a contract that rule 2 then
   makes permanent. Bend this knowingly and write down that you did.
4. **Decide what counts as an identifier, on purpose.** Whether a field
   name, a query key, or an enum value is an identifier or part of the API
   is a labelling choice, and the label sets the change cost. Make it
   explicitly, in the identifiers doc, before anyone stores the value.
5. **Additive changes are cheap at every layer.** Renames and removals in
   the top two layers need a version, an adapter, or a deprecation path.
   Never silently.
6. **When two layers pull in different directions, the higher wins.** A
   worse table for a stable id is the right trade every time.
7. **"It was reviewed" is a reason to protect the top two layers, not the
   bottom two.** Caution spent on preserving a data-layer choice is caution
   in the wrong place.

## How to apply it

When invoked on a design question, do this and nothing more:

1. List the elements under discussion and assign each a layer. Say which
   parties would have to act if it changed. Where the layer is arguable,
   say why and pick one.
2. Name any inversion: a lower-layer fact living in a higher layer. Quote
   the offending element.
3. State what the change actually costs, by layer. Most questions resolve
   here: either the change is in a lower layer and is cheap, or it touches
   an identifier or contract and needs a path for existing holders.
4. Give one recommendation. Do not produce a menu.

Do not turn this into a style guide. UUIDs, contract-first, JSON Schema:
all sometimes right, none a consequence of the ordering. Opacity is the
exception: it is the doctrine's own rule for the top layer, not a style.
Below that, the doctrine says nothing about *how* to build a layer, only
about which layers must not leak into which.

## Where it does not apply

Firmware with no external consumer, dotfiles, formal specifications, and
one-off scripts have no top two layers worth the ceremony. Do not invoke it
there. Projects that publish something others store (a data package, a
plugin's paths, a service's URLs) are where it earns its keep; those
projects may point at this skill with one line in their CLAUDE.md.
