# RB3 vtable Slash-Command Skill — Design Plan

Adapt DC3's `/vtable` skill to RB3 (Wii / MetroWorks CodeWarrior / PowerPC).
DC3's implementation reads MSVC PowerPC COFF `.obj` files, parses `??_7…@@6B…`
mangled vtable symbols, and consults `??_R4` RTTI Complete Object Locators to
resolve sub-object offsets. None of that maps onto RB3:

- Object format is ELF, not COFF.
- Vtable mangling is `__vt__N<classname>` (MetroWorks), not `??_7…@@6B…`.
- There are no `??_R4` COL records; MWCC emits `__RTTI__N<classname>` pointers
  inline at the start of each sub-object vtable and uses `@<delta>@` thunk
  symbols for `this`-pointer adjustment.
- MWCC on Gekko does **not** do COMDAT folding / ICF in the MSVC sense, so the
  "disambiguate ICF-merged slots" mechanism DC3 needs is unnecessary here.
- The debug ELF carries full DWARF v2 with class hierarchy and `DW_AT_inheritance`.

This document covers the design only. No implementation code is produced.

## 1. Data source decision

Three plausible sources for vtable layout. Comparing each against RB3:

### (a) Build `.o` relocations via `pyelftools`  — RECOMMENDED

Read `build/SZBE69_B8/obj/<path>.o`, find the `__vt__N<classname>` symbol in
`.symtab`, look at its `.data` section, walk `.rela.data` entries whose offset
falls inside `[sym.value, sym.value + sym.size)`. Each relocation is an
`R_PPC_ADDR32` (type 1) pointing at either an `__RTTI__*` symbol (slot boundary
marker) or a function symbol (a virtual function pointer).

Confirmed empirically against `build/SZBE69_B8/obj/system/char/Character.o`:

- `__vt__9Character` is a single 628-byte object in `.data`.
- The first relocation inside that range points at `__RTTI__9Character` (this
  is the start of the primary sub-object vtable).
- Subsequent relocations point at function symbols for slot 0..N.
- A second `__RTTI__9Character` reloc appears mid-vtable; that marks the
  beginning of the next sub-object vtable. The thunks immediately following it
  are named `@<delta>@Method__9CharacterFv` where `<delta>` (decimal) is the
  byte offset from the primary `this` pointer to the sub-object `this`.

This is the cleanest mapping for the RB3 toolchain: it uses the same artifacts
already produced by `ninja`, requires no live service, and gives byte-exact
slot order for the version we're matching (`SZBE69_B8`). pyelftools is **not
installed** in the project's Python env (verified 2026-05-12: `import
pyelftools` raises `ModuleNotFoundError`; an earlier draft of this plan
incorrectly claimed `0.32` was already available). Neither `requirements.txt`
(only `pcpp`) nor `requirements-orchestrator.txt` declares it. Add
`pyelftools>=0.32` to `requirements.txt` and install before any implementation.

Pros:
- Authoritative for the build target (the actual `.o` we diff against).
- No service dependency; works offline / in CI.
- Symbol names are the mangled MWCC form, directly comparable to objdiff
  output and `band_r_wii.map`.
- Sub-object boundaries are visible (RTTI marker + `@N@` thunk prefix).

Cons:
- No demangled output for free — we need a demangler (objdiff-cli embeds
  `cwdemangle`; we can shell out, or call the Rust `tools/upstream/batch-demangle`
  binary if we build it). For our needs the mangled names are already
  unambiguous, so demangling is a nicety.
- No direct inheritance graph; we can derive "primary vs secondary base" only
  from offset boundaries and `@N@` thunk prefixes, not from class names.
- Slow if we want to enumerate every vtable in the project — fine for the
  one-class-at-a-time slash command, less great for bulk operations.

### (b) Ghidra MCP (`tools/ghidra/mcp_client.py`)

Ghidra has loaded `band_r_wii.elf` with DWARF imports. We could:
- `search_symbols("__vt__9Character")` → get the vtable address.
- `read_bytes(addr, size)` → read raw bytes, byteswap, look up each pointer.
- Resolve each pointer to a function symbol via another `search_symbols` or
  `list_xrefs` call.

Pros:
- Could give richer demangled names and resolved type info if Ghidra has done
  the work already.
- Single tool already wired up for `/struct-check`.

Cons:
- The version mismatch is fatal. The Ghidra-loaded ELF is **Bank 5 (Debug)**;
  our build target is **Bank 8 (Release SZBE69_B8)**. I observed
  `__vt__9Character` is 628 bytes in `build/SZBE69_B8/obj/.../Character.o`
  versus 604 bytes in the debug ELF. Vtable layouts shifted between banks.
  Using Ghidra would silently return the wrong slot for any class that
  changed between banks, and we'd have no easy way to know which ones did.
- Requires the `pyghidra-service.sh` daemon running; brittle in CI.
- O(N) MCP calls to resolve N pointer slots; latency adds up.

### (c) `readelf` / `nm` on `band_r_wii.elf` or `.o` files

Shell out to `readelf -W -s` and `readelf -W -r`, parse the text. This is
basically (a) with a different data layer.

Pros:
- No Python deps beyond stdlib.

Cons:
- Fragile text parsing of multi-format readelf output.
- Same version-mismatch caveat as (b) if we use the debug ELF, OR same as (a)
  but uglier if we parse `.o` files.

### Decision

**Use (a):** parse `.o` files from `build/SZBE69_B8/obj/` with pyelftools.
Add pyelftools to `requirements.txt` to make the dependency explicit.

For the `band_r_wii.elf` debug ELF, optionally use it as a *secondary* source
for class hierarchy enrichment (read `.debug_info` DIEs for the class, follow
`DW_TAG_inheritance` chains, label each sub-object vtable with the actual base
class name). This is gravy, not required — the `@<delta>@` thunk prefix and
the offset-of-the-second-`__RTTI__`-symbol already tell us most of what we
need. Flag this as a phase-2 enhancement.

> One thing DWARF v2 from MWCC explicitly does **not** give us: an
> `DW_AT_vtable_elem_location` attribute per virtual subprogram. I verified
> the abbrev table in `band_r_wii.elf` — only `DW_AT_virtuality` and
> `DW_AT_containing_type` are emitted, and the `virtuality=1 (virtual)` we
> see is consistently on `DW_TAG_inheritance` (virtual *base*), not on
> `DW_TAG_subprogram`. So DWARF cannot replace the `.o` relocation walk for
> slot assignment.

## 2. Output shape

Per-slot record:

| field          | example                                               | notes |
|----------------|-------------------------------------------------------|-------|
| `slot`         | `18`                                                  | 0-based, within its sub-object table |
| `offset`       | `0x48`                                                | byte offset from start of sub-object vtable (`slot * 4`) |
| `vtable_offset`| `0x80`                                                | offset of this sub-object vtable from `__vt__` symbol start; primary is 0 |
| `symbol`       | `Handle__9CharacterFP9DataArrayb`                     | mangled function symbol pointed to by this slot |
| `demangled`    | `Character::Handle(DataArray*, bool)`                 | optional; depends on demangler availability |
| `defining_class`| `Character`                                          | parsed from the symbol's mangled class-length prefix |
| `is_thunk`     | `false`                                               | `true` if symbol starts with `@N@` |
| `thunk_delta`  | `null` or `128`                                       | byte adjustment from `@N@`-prefixed thunks |
| `is_override`  | `true`                                                | inferred by comparing `defining_class` to "expected base class" along the chain |
| `sub_object`   | `{ "offset": 0, "base": "primary" }`                  | which sub-object vtable this slot lives in |

Whole-vtable dump record:

```json
{
  "class": "Character",
  "vtable_symbol": "__vt__9Character",
  "obj_file": "build/SZBE69_B8/obj/system/char/Character.o",
  "total_size_bytes": 628,
  "sub_objects": [
    {
      "offset": 0,
      "base": "primary",
      "slots": [ /* SlotRecord, SlotRecord, ... */ ]
    },
    {
      "offset": 128,
      "base": "<inferred-base-or-unknown>",
      "slots": [ /* ... */ ]
    }
  ]
}
```

Notes / simplifications:

- **No ICF disambiguation needed.** MWCC 4.3 on Gekko does not fold
  identical-body functions across virtuals; each `OnlyReturns`-style empty
  vtable slot has its own unique symbol. Drop the `ICF_HINTS`, `classify_icf`,
  and `confidence` machinery from DC3's script — they have no analogue here.
- **No `??_R4` COL parsing.** The `__RTTI__N<class>` symbol pointed to from
  each sub-object vtable header is just an 8-byte structure; the sub-object
  offset is *not* encoded there. Instead, we recover the offset by either
  (a) looking at the offset of the second/third `__RTTI__` reloc within the
  `__vt__` symbol's range, or (b) parsing the `@<delta>@` prefix from the
  first thunk in each sub-object section. Both should agree; mismatch is a
  red flag worth printing as a warning.
- **Demangling is optional.** The mangled MWCC names are already unambiguous
  ("Handle__9CharacterFP9DataArrayb"). If demangling is wanted, options are:
  build `tools/upstream/batch-demangle` (already has `cwdemangle` as a dep), shell out
  to it; OR call `objdiff-cli` indirectly; OR ship a tiny pure-Python parser
  that handles only the cases we hit (class-length + method-name extraction,
  similar to `_demangle_itanium_to_qualified` in
  `scripts/orchestrator/mcp_server.py:86`).

## 3. CLI surface

```
scripts/dump_vtable.py CLASS [--obj PATH] [--offset HEX]
                       [--unit UNIT] [--json] [--demangle] [--all-subobjects]
```

Mirroring DC3 where it makes sense, dropping `resolve` subcommand-vs-flag
duplication. Single command, two modes by presence of `--offset`:

- `dump_vtable.py Character`
  → Print full vtable dump (all sub-objects, all slots).
- `dump_vtable.py Character --offset 0x48`
  → Print the single matching slot (primary sub-object by default).
- `dump_vtable.py Character --offset 0x48 --sub-offset 0x80`
  → Print the slot from the sub-object at byte offset 0x80 within the vtable.

Auto-detection rules for `--obj`:

1. If `--unit UNIT` is given, use `build/SZBE69_B8/obj/<UNIT>.o`. UNIT format
   mirrors objdiff (`system/char/Character` or `main/system/char/Character`).
2. Else look up the class in `decomp.db`:
   `SELECT DISTINCT unit FROM functions WHERE symbol LIKE '__dt__N<class>Fv'`
   then `unit LIKE 'Handle__N<class>%'` and similar — anything that reliably
   sits in the same `.o` as the vtable. Confirmed `__dt__9CharacterFv` resolves
   to `main/system/char/Character` in `decomp.db`.
3. Else fall back to globbing `build/SZBE69_B8/obj/**/<Class>.o` (with the
   "strip Rnd/Ham prefix" heuristic borrowed from DC3 — RB3 has the same
   convention for things like `RndFontBase` living in `FontBase.cpp`).
4. If all of the above miss, error out with a list of `__vt__*` symbols seen
   in the most likely candidate `.o` files.

Class lookup by demangled name is supported by *inverting* the mangling:
`Character` → search for `__vt__9Character` (compute length prefix). This
covers the common case. If the user passes a mangled symbol directly
(`__vt__9Character`), accept that too.

Mangled-form fallback: accept `__vt__9Character` verbatim as the argument.

`--json` mode emits the per-slot record format from §2 for tooling
integration (orchestrator, future MCP tool, batch jobs).

## 4. Multiple-inheritance / sub-object vtables

MWCC's layout for multiply-inherited classes differs from MSVC's. Empirical
observation from `Character.o` (Character inherits from `ObjectDir`,
`RndDrawable`, `CharPollable`, plus a couple of templated `ObjPtr*` mixins):

- A single `__vt__9Character` symbol covers the entire 628-byte object.
- Inside that object, sub-object vtables are laid out **contiguously**, each
  one starting with a relocation pointing at `__RTTI__9Character` (same
  symbol; the RTTI block itself is per-class, not per-sub-object).
- The primary base (`ObjectDir`'s vtable slot layout) starts at offset 0.
- The next sub-object table starts at offset 128 (0x80); methods within it
  that override the primary's are emitted as thunks named
  `@128@MethodName__9CharacterFv`. The `128` is the byte delta from
  primary-`this` to this sub-object's `this`.
- Slots in sub-object tables that are NOT overridden by the derived class
  point directly at the base's implementation (e.g. slot points at
  `RefOwner__Q23Hmx6ObjectFv` — not a thunk).
- For `OnlyReturns`-style empty Object virtuals that DC3 had to disambiguate
  via ICF, MWCC emits unique per-class symbols. No special handling required.

What's verified vs guessed:

- Verified by inspection of `Character.o`: the "single `__vt__` symbol with
  multiple `__RTTI__` markers inside it" pattern.
- **Verified 2026-05-12 across the whole build:** no class anywhere in
  `build/SZBE69_B8/obj/**/*.o` has more than one `__vt__N<class>` symbol.
  Sweep:
  ```bash
  setopt globstar  # zsh; bash users: shopt -s globstar
  for f in build/SZBE69_B8/obj/**/*.o; do
      nm -g "$f" 2>/dev/null | awk -v file="$f" '/__vt__/ {print file, $3}'
  done | sort -k2 | uniq -c -f1 | awk '$1 > 1' | head
  ```
  Returned no rows. Top vtable-density files: Game.o (19), NetSync.o (17),
  VocalTrackDir.o (14), GemTrackDir.o (14). Single-symbol path is the only
  path needed for v1. The multi-symbol fallback (enumerate `__vt__*`,
  group by sub-object offset) stays a future-proofing note — implement on
  the first counter-example, not pre-emptively.

Virtual inheritance (`DW_AT_virtuality = 1` on `DW_TAG_inheritance`) **is**
present in some classes. **Locked test target: `RndDrawable`** (verified to
have a `DW_TAG_inheritance` of `RndHighlightable` at offset 0 with
`DW_AT_virtuality: 1`, plus a separate `DW_TAG_member` of type
`RndHighlightable` at offset 96 — see
[resolve-vcall-skill.md § 6](resolve-vcall-skill.md#6-worked-example-resolve-vcall-rnddrawable-0-5)).
The `--offset 0` (vtable load lands here) vs offset-96 (member-access
storage) distinction is the case the implementation must handle correctly.
Don't substitute "an SDK / NW4R / STL class TBD" — RndDrawable is the
regression target.

## 5. Integration with the decomp workflow

Typical trigger: objdiff shows a pair of `lwz` instructions on `r12` with an
offset mismatch. Concrete example from `build/SZBE69_B8/asm/system/char/Character.s`:

```
lwz   r12, 0x4(r3)       # load vptr from this+4 (a sub-object vtable!)
lwz   r12, 0x1a0(r12)    # call slot 0x1a0/4 = 104
```

Workflow when this is failing to match:

- The agent sees that our source calls `obj->SomeMethod()` but the diff shows
  a different vtable slot. They invoke `/vtable Character` to enumerate
  every slot. The `lwz r12, 0x4(r3)` tells them it's the sub-object at
  vtable_offset != 0, so they look at the sub-object table whose `@N@` thunks
  use offset 4. They scan the slot list, find slot 104 = e.g.
  `@4@DrawShowing__9CharacterFv`, and now they know the source needs to call
  `DrawShowing()` (qualified as a `RndDrawable` virtual, since this is
  RndDrawable's sub-object) rather than whatever they had.
- Reverse direction: when the agent's source calls `obj->X()` and the diff
  picks slot 0x50 but target uses 0x48, both `/vtable Class --offset 0x48`
  and `/vtable Class --offset 0x50` give the answer in one line each. Plug
  the right method into the source.
- For `/refactor-staff` and `/struct-check`-style verification passes: a
  batch mode (`--all-subobjects --json`) can dump every sub-object table for
  a class, which makes it easy to verify a header's virtual function order
  against the compiled binary.

## 6. Implementation effort estimate

Rough size:
- `scripts/dump_vtable.py`: ~250-350 lines (vs DC3's 577) — much smaller
  because we drop COFF parsing, RTTI COL parsing, and ICF logic, and we get
  ELF parsing for free from pyelftools.
- `.claude/skills/vtable/SKILL.md`: ~60-80 lines, mostly adapted from
  DC3's version.
- Optional class-hierarchy enrichment from DWARF: another ~150-250 lines
  if/when we want it. Keep this in a separate phase / module.

Dependencies:
- pyelftools: **not installed** in the project env (verified 2026-05-12 —
  `python3 -c "import pyelftools"` raises `ModuleNotFoundError`). Add
  `pyelftools>=0.32` to `requirements.txt` and install before Step 1.3
  in [tooling-roadmap.md](tooling-roadmap.md). Earlier draft of this doc
  claimed it was already installed; that was wrong.
- No new Rust deps. If we want demangled output, either (a) build the
  existing `tools/upstream/batch-demangle` crate (which already pulls in
  `cwdemangle`) and shell out, or (b) implement a minimal pure-Python
  cwdemangle that handles only the cases we hit. Option (b) is probably
  ~50 lines and avoids the build dep.

Skill/MCP wiring:
- Slash command following the `.claude/skills/<name>/SKILL.md` convention
  (single file with frontmatter — see `analyze-function/SKILL.md` and
  `struct-check/struct-check.md` as templates).
- The orchestrator MCP server (`scripts/orchestrator/mcp_server.py`) does
  not need a new tool for v1; adding `mcp__orchestrator__lookup_vtable`
  later is an obvious enhancement once the script stabilizes, since the
  orchestrator already opens `decomp.db`.

Total: ~half a day to a day, including testing against a handful of
multi-inheritance classes (Character, anything in `system/bandobj/`, an
NW4R class with virtual inheritance).

## 7. Open questions

1. **Orchestrator integration scope.** Should this ship as just a Python
   script + slash-command skill, or also as an `mcp__orchestrator__` tool
   alongside `query_functions` etc.? An MCP tool would let the agent
   request "what's at slot 0x48 of Character" mid-objdiff-analysis without
   spawning a subprocess. Question is whether it's worth the API surface;
   defer to v2.

2. **Single-vs-multi `__vt__` symbol invariant.** ~~I verified Character
   (multi-base, MI via `ObjectDir`+`RndDrawable`+`CharPollable`) emits one
   `__vt__9Character` symbol covering all sub-object vtables. Whether
   every MWCC-emitted class follows that invariant is unverified — would
   require a sweep across `build/SZBE69_B8/obj/**/*.o`.~~ **Resolved
   2026-05-12.** Whole-build sweep confirms no class has more than one
   `__vt__N<class>` symbol (see § 4). Single-symbol path is the only path
   needed for v1; multi-symbol fallback is documented but not implemented
   until a counter-example appears.

3. **Demangler choice.** Pure-Python mini-demangler vs shelling out to a
   built `tools/upstream/batch-demangle` vs invoking `objdiff-cli`. None is hard;
   the right answer depends on whether we ever want to run this without
   the Rust toolchain (e.g. in a stripped-down CI image). Default to
   "mangled output by default, pure-Python pretty-print of class+method
   when `--demangle` is passed; full demangle is an opt-in via
   `--demangle-full` shelling out to batch-demangle".

4. **Bank version handling.** This plan targets `SZBE69_B8`. Other Wii
   banks (1/2/5/6) and the 360/PS3 ports use different builds with their
   own `.o` directories. Currently the script will hard-code
   `build/SZBE69_B8/obj/`. Either read the version from `objdiff.json` or
   accept a `--version` flag — `configure.py --version SZBE69_B8 --map`
   suggests that's the project's convention. Keep simple for v1, parametrize
   when a second target is needed.
