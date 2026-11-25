---
name: game-save-system
description: "Design, version and repair a game's save files so player progress survives every future patch. Names the compatibility promise first — how many builds back a save has to load, and what happens outside that window — then picks the format from the promise rather than the other way round, version-tags the schema with one migration step per bump, makes the write atomic so an interrupted save is not a corrupt one, checksums and rotates backups, and settles cloud-save conflicts by lineage rather than last-write-wins. Use this skill whenever someone is building or changing a save system, or says \"the patch broke everyone's saves\", \"how do I version my save format\", \"players lose progress syncing between two devices\", or \"the save file is corrupt\". Not for a server database schema change (db-migration), an account or inventory service (api-design), or building the game itself (game-builder)."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(git:*), Bash(python:*)
---

# Game Save System

A save system is right when a player who last opened the game two years and eleven patches ago installs the current build, loads their file, and loses nothing they would notice — and when a save interrupted by a power cut still loads.

Two failure modes account for almost every ruined save, and both are decided early. The first is choosing the format before choosing the promise: JSON was already in the project, or the engine had a one-line serialiser, so the file shape was fixed by convenience, and the question of whether a save written by build 1.0 has to load in build 1.4 was answered eighteen months later by a patch that could not be shipped. Serialisers that embed class identity make this worse, because the file is then tied to the code layout and a rename breaks every save on disk. The second is treating the write as a write. A save is not one operation; it is serialise, write, flush and replace, and a machine that loses power between any two of those steps leaves a file that is half old and half new, which parses far enough to look loadable. That is the common corruption, not bit rot and not tampering. Everything below is ordered so the expensive decisions are made while they are still cheap.

## Scope

Use for: designing a save system, versioning a save schema, writing or reviewing a migration, diagnosing corrupt or unloadable saves, choosing the write and backup policy, resolving cloud-save conflicts between devices, deciding what belongs in a save at all, and building a corpus of old saves to test migrations against.

Do not use for: a schema change to a live relational database on a server — that is `db-migration`, and none of the atomicity or cloud-conflict work here applies to it. A player-account, inventory or leaderboard service reached over HTTP is `api-design`. Building the game, including where autosaves sit in the loop for feel, is `game-builder`. Replicating state between a server and a client during play is `game-netcode`. Tuning the numbers a save happens to store is `game-balance`. Getting save behaviour through platform certification is `game-certification`.

## Scale and game type

Scale here means what the work requires rather than a headcount or a budget: indie/A is one small team wearing every hat; AA adds specialised roles, several platforms and a publisher's milestones; AAA adds many specialised disciplines, external studios and a simultaneous multi-platform launch.

| | Indie/A | AA | AAA |
| --- | --- | --- | --- |
| Promise (step 1) | Fine only before the first external playtest — the promise table fits "saves do not survive an update" to closed testing and jam entries; a shipped indie game needs the last N versions or better | The last N versions load, matching a publisher's patch cadence | Every save ever written loads — a live economy cannot break a save on any patch |
| Cloud sync (step 7) | Often skipped — one device, no sync | Cross-device sync for the platforms shipped | Cross-device and cross-platform sync, with lineage resolution tested |
| Certification interplay | The same person who writes the save code checks the platform's write-timing rules | `game-certification`'s save-data messaging row is a separate sign-off | The same, across every platform in a simultaneous launch |

Open world and large 3D games carry the most risk here, because a large persistent world needs the migration-chain discipline in step 3 from the first save file, and whether the game is save-anywhere or checkpoint-only is the cadence decided at step 4 — this skill owns what the write costs, and `game-builder` owns where autosaves sit for feel. Any game with a traded economy or a leaderboard needs step 10's server-authoritative case from day one, which is most often competitive multiplayer and live-service titles.

## Workflow

### 1. Name the compatibility promise before anything else

Answer these three in a sentence each and write the answers into the repository, next to the save code. They are the input to every decision below, and recovering them later means recovering them from shipped files in players' hands.

- **Backward compatibility.** Can the current build load a save written by an older build, and how many versions back? This is the promise players think they have by default.
- **Forward compatibility.** Can an older build load a save written by a newer one? It sounds exotic until two devices sit on different patch levels, or a console build is stuck behind a cert queue while the PC build ships, or a platform rolls a release back.
- **What happens outside the window.** Refuse and say why, load with stated loss, or convert silently. Pick one now; the default is a parse exception in front of the player.

| Promise | What it costs | Fits |
| --- | --- | --- |
| Every save ever written loads | One migration step kept forever, and a test corpus that only grows | Long-lived games, anything with a paid or traded economy |
| The last N versions load | The same, bounded, plus a refusal path real players will hit — so it needs a message and a support answer | Live games that patch often and can afford to draw a line |
| Saves do not survive an update | Nothing, until the first person outside the team plays | Closed playtests and jam entries, and nothing that has shipped |
| Old builds load new saves too | Unknown fields preserved rather than dropped on read, and no field may ever change meaning | Cloud saves across devices, staggered platform releases |

The promise is the gate because the format follows from it. A serialiser that cannot represent a field it does not recognise cannot keep a forward-compatibility promise at all, and no amount of care downstream adds the capability. A struct written straight out of memory cannot keep a backward one past the first field reorder. Choosing the format first means discovering which promise you accidentally made.

### 2. Choose the format from the promise

| Format | Backward | Forward | Notes |
| --- | --- | --- | --- |
| JSON, optionally compressed | Good — unknown fields are visible and skippable | Good if the reader keeps unknown keys instead of dropping them | Readable in a bug report, which is worth more than it sounds. Verbose; compression removes most of that |
| MessagePack or CBOR | As JSON | As JSON | JSON's shape without JSON's size, at the cost of not being readable by eye |
| Protocol buffers or FlatBuffers | Strong, if field numbers are never reused | Strong — unknown fields are preserved by design in proto | A schema you have to maintain and ship; the best fit for a strict promise |
| SQLite | Strong, with the same migration discipline as any database | Weak | Earns its place for a large, partially loaded world; overkill for a slot of player state |
| Engine-native or reflection-based serialiser | Weak — the file follows your class layout | None | The convenient one. See below before choosing it |

Two disqualifiers are independent of taste. A serialiser that embeds type or class identity in the file ties every existing save to the current code layout, so renaming a class or moving it between namespaces invalidates saves on disk; it is also a code-execution surface the moment such a file arrives from a cloud sync or a friend. C# `BinaryFormatter` is obsolete and removed from recent .NET, Java's built-in serialization and Python's `pickle` are the same shape of hazard, and Godot's `FileAccess.store_var` takes `full_objects` for exactly this reason — leave it false. The second disqualifier is a format with no room for a field the reader does not know: it forecloses forward compatibility permanently.

Separate the save's schema from the runtime classes whatever you choose. A save record that is its own type, converted to and from the live objects, is the thing that lets you refactor the game without touching the file format. `references/formats-and-layout.md` has the per-format detail, the header layout and the save-record pattern; read it at this step.

### 3. Version the schema, and write one migration step per bump

- Put a format version in a fixed-size header that can be read without parsing the body, so a save from the future can be refused rather than half-parsed. Add a magic number beside it; a file whose first bytes are wrong is a different file, not a corrupt one.
- Version the save format, not the game build. A patch that changes no persisted shape does not bump it, and a version that tracks the build number produces migration steps that do nothing and hide the ones that do.
- Migrate as a chain of single-step functions — v3 to v4, v4 to v5 — applied in order until the save reaches the current version. The alternative, one function that converts any version to the present, grows a combinatorial tangle of conditionals and is where migration bugs live.
- Each step takes the previous representation and returns the next, touches nothing else, and is not edited after it ships. Editing a released step changes what old saves become, retroactively, and the change is invisible until a player reports a number that is wrong.
- Never renumber and never reuse a version number, including one that only reached a beta branch.
- Additive fields with a sensible default need no step. Renames, retypes, splits, merges, unit changes and meaning changes all need one, and a meaning change with no rename is the one that gets missed.

### 4. Make the write atomic, because the common corruption is an interrupted write

Write to a new file and replace, in this order:

1. Serialise completely, into memory or a temporary buffer, before touching anything on disk. A serialisation exception should cost nothing.
2. Write the bytes to a temporary file in the same directory as the destination, so the replace stays on one filesystem.
3. Flush the file and fsync it. The bytes are not durable because `write` returned.
4. Rename the temporary file over the destination. This is the one step that is atomic; a reader sees the old file or the new one.
5. Fsync the containing directory where the platform supports it, so the rename itself survives a power loss.

Skipping step 3 is the subtle one: on several filesystems a rename that is durable before its data produces a file of the right name and the wrong or zero length, which is the corrupt save that arrives without a crash to blame.

Consoles usually mediate saves through a platform API rather than raw file writes, and that API supplies the atomicity — use it. The same platforms require a visible saving indicator and forbid certain writes around suspend; those are certification items and belong to `game-certification`.

Decide the save cadence here too. Autosaving every frame multiplies every cost above and puts the write in the middle of play, where the interruption is; autosave on a boundary the player understands, plus a bounded timer, and coalesce rapid triggers. `references/durability-and-corruption.md` carries the per-platform write sequence and the interruption test rig; read it at this step and step 5.

### 5. Detect a bad save before you trust it

Store a checksum over the payload, with the field holding it excluded from its own computation. It catches truncation, a partial write that survived, bit rot on failing storage, and a sync that copied half a file — which is every corruption you can actually do something about.

A checksum is not tamper-proofing, and treating it as such is how teams talk themselves into an expensive design. Anyone editing a save recomputes it, and an HMAC whose key ships inside the client is recovered soon after release. Whether that matters is step 8.

Validate again after parsing. A file can be structurally perfect and semantically impossible after a patch: an item id that no longer exists, a quest pointing at a removed node, a currency past a new cap. Clamp and drop rather than crash, but log what was clamped, because a rising count there is a migration bug reporting itself.

On a failed load, fall back in order — most recent backup, then the next — and if nothing loads, refuse with a message naming the file and its location. Keep the bad file, renamed rather than deleted. It is the only evidence of the defect, and deleting it converts a recoverable support case into a lost account.

### 6. Keep backups, and decide how many

- Rotate a small fixed number of previous saves per slot. Three covers the realistic case, which is one bad write plus the panic re-save that follows it.
- Keep the last known-good save outside the rotation, so a run of corrupt writes cannot push the only working file off the end.
- Take a backup before running a migration, tagged with the version it came from, and keep it until the player has played and saved successfully on the new version.
- Size the rotation against the platform's save quota rather than the disk. Console save quotas are measured in megabytes, and backups count against them.

### 7. Resolve cloud conflicts with lineage, not with a timestamp

Last-write-wins loses progress, and players notice, because the situation that produces a conflict is exactly the one where both copies contain real play. Clocks make it worse: an offline device's clock can be wrong by days, so the newest timestamp can be the copy with less in it.

- Give every save a counter that increments on each write, alongside a device identifier and accumulated playtime. A counter does not go backwards when a clock does.
- Record enough lineage to tell a stale copy from a divergence — which save each write descended from. If neither side descends from the other, it is a conflict, and treating it as staleness is what silently deletes an evening's play.
- On a genuine conflict, ask the player, and show the facts a decision can be made from: playtime, chapter or area, currency, completion, and the device each came from. "Local or cloud" is not a question anyone can answer.
- Keep the copy that loses, as a slot or a recoverable backup.
- Prefer avoidance: save and upload on quit and on suspend, and resolve pending uploads before the next session can start. A conflict never created beats a conflict resolved well.

`references/cloud-sync.md` covers the per-platform sync models, the lineage scheme, and the resolution prompt; read it when a game syncs saves at all.

### 8. Keep machine-specific and order-dependent data out of the file

Anything in this list turns into a broken save on someone else's machine or after some later edit:

- **Absolute paths.** They break on a different machine, a different OS user, a moved install, and a different platform.
- **Hardware or machine identifiers used as keys.** They change on reinstall and on hardware replacement, and the player loses the save while looking at it.
- **Unversioned enum ordinals.** Inserting a value in the middle re-points every existing save silently. Persist a stable string name, or treat the numbers as permanent and never reorder or reuse them.
- **Object references, pointers and engine instance ids.** They mean nothing in the next process.
- **Large derived data.** It doubles the file, and it goes stale the moment the formula changes; recompute on load.
- **Entitlements and anything the client should not be authoritative over.** A save that grants purchases is an economy exploit with a save-file interface.
- **Unbounded history.** An event log or telemetry buffer that only grows eventually exceeds the platform's save quota, which fails as a write error in front of the player.

Store a unit with any quantity whose unit is currently implied by the code. Seconds became milliseconds in a patch somewhere in every long-lived codebase, and the save is where that becomes permanent.

### 9. Test migrations against real old saves

A save synthesised by the current writer with an old version number in the header carries today's assumptions, so it passes migrations that fail on the real thing. Keep the real ones.

- Maintain a corpus of saves captured from actual play on each shipped version, committed with the tests. Include the awkward ones: near-complete, mid-cutscene, full inventory, and any file written by a build with a known bug.
- Load each corpus file, run the full chain to the current version, and assert invariants — currency totals, completion count, item identity, position within the world — rather than field-by-field equality, which breaks on every legitimate change.
- Test corruption on purpose. Truncate copies at many offsets, flip bytes, and zero the file, then assert the loader refuses cleanly and falls back:

```bash
size=$(wc -c < save.dat)
for offset in $(seq 1024 1024 "$size"); do
  head -c "$offset" save.dat > "truncated-$offset.dat"
done
```

- Test the write path under interruption: kill the process repeatedly at random moments during a save, and assert that every resulting on-disk state loads, as either the old save or the new one.

`references/compatibility-and-migration.md` has the migration chain pattern, the corpus layout, the invariant assertions and the retirement procedure for a version that falls out of the window. Read it at steps 3 and 9.

### 10. Handle save-scumming and anti-cheat only where they change the design

Most of this debate changes nothing you would build. Three cases do:

- **A leaderboard, a traded economy or anything competitive reads the save.** Then the authoritative copy lives on a server and the local file is a cache, which is a service decision rather than a file-format one — `api-design` owns the service. No client-side format defends this.
- **Single-player with achievements.** Saves are editable; obfuscation buys days and costs you the ability to read a player's file when they report a bug. Decide that trade explicitly rather than by reflex.
- **Deletion is a mechanic**, as in permadeath. Then the save is part of the rules, and the atomic write and the backup rotation are what stop a crash from being read as a death — keep both, and keep the backups somewhere the player has to make an effort to reach.

Encrypting saves also means you cannot diagnose a player's file from a bug report, and a key that changes bricks every save written before it.

## Anti-patterns

**Choosing the format before the promise.** The format decides which promises remain available, so this order silently picks the promise for you, usually the weakest one.

**A serialiser that embeds class identity.** The first class rename invalidates every save on disk, and the file becomes a code-execution surface when it arrives from a sync.

**Writing over the live save in place.** A crash mid-write leaves one file that is half of each, and there is no backup because the backup was the file you overwrote.

**A save version that tracks the build number.** It produces migration steps that do nothing, which trains everyone to skip writing the ones that matter.

**One migration function with a ladder of version conditionals.** Every new version multiplies the paths through it, and the paths nobody runs are the ones that ship broken.

**Editing a migration step after it has shipped.** It rewrites history for saves that have not been loaded yet, and the resulting wrong number arrives with no change to blame.

**Persisting enum ordinals and then inserting a value.** Every existing save quietly means something else, and it usually surfaces as an unrelated bug report weeks later.

**Calling a checksum anti-tamper.** It detects damage, which is the useful job; sold as security it justifies work that buys nothing.

**Last-write-wins on a cloud conflict.** The conflict case is the one where both copies matter, so the cheap rule deletes progress precisely when progress exists.

**Deleting a save that failed to load.** It destroys the only evidence and converts a recoverable case into a lost account.

**Testing migrations on synthesised saves.** They encode the current writer's assumptions, so they pass the migrations that real old files fail.

## References

- `references/compatibility-and-migration.md` — read at steps 3 and 9: the version header, the migration chain, defaults and field retirement, the real-save corpus, invariant assertions, and how to retire a version from the window.
- `references/formats-and-layout.md` — read at step 2: format by format against the promise, the header layout, the save-record pattern that keeps the file independent of runtime classes, and the serialisers to avoid with the reason each.
- `references/durability-and-corruption.md` — read at steps 4 and 5: the atomic write sequence per platform, checksum choice and placement, the fallback order on a failed load, backup rotation and quotas, and the interruption test rig.
- `references/cloud-sync.md` — read at step 7 when saves sync at all: the platform sync models, the counter and lineage scheme, divergence detection, the conflict prompt, and the avoidance work that removes most conflicts.
