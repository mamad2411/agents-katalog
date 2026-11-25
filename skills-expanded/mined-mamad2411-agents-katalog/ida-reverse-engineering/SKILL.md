---
name: ida-reverse-engineering
description: >
  Drive IDA Pro through the IDA Pro MCP like a senior reverse engineer: don't just narrate
  decompiler output, transform the database. Use this whenever the user is reverse engineering,
  analyzing malware, working a crackme or CTF, or doing binary/firmware analysis with IDA Pro
  over an MCP connection (mrexodia/ida-pro-mcp or idalib-mcp) — and especially when the agent
  keeps guessing at raw pseudocode instead of renaming functions and variables, defining structs,
  fixing types, and adding comments. Covers the iterative cleanup loop, anti-hallucination rules
  (always use int_convert; read real bytes/strings/xrefs), a triage/deobfuscation/library-resolution
  pre-pass, a definition-of-done, game-binary reversing (Unity/IL2CPP, Unreal, RTTI, anti-cheat/DRM),
  and bundled IDAPython scripts. Trigger even if the user only says
  "reverse engineer this binary", "clean up this IDB", "make this pseudocode readable", "dump the
  Unity/Unreal SDK", "reverse this game", or names IDA tools, without saying the word "skill".
---

# Senior Reverse Engineering with IDA Pro (MCP)

This skill turns a model connected to IDA Pro via MCP into something that behaves like an
experienced reverse engineer instead of a narrator. The single biggest failure mode of an
MCP-driven RE agent is treating decompiler output as an *answer to explain* rather than *raw
material to transform*. A junior reads `sub_401000`, says "this looks like it validates a
license," and moves on. A senior renames the function to `validate_license`, names every
variable, defines the struct behind `*(a1 + 0x10)`, fixes the argument types, comments the
algorithm, re-decompiles to confirm the output got cleaner, and only then moves on — leaving
the database permanently better than they found it.

Your job is to do the second thing, on every function, using the MCP write tools.

You are a capable model. Use that: reason from evidence, form hypotheses and test them against
the binary, and decide *where to spend effort*. The structure below is a reliable default, not a
cage — adapt it when the binary calls for it, but never skip the parts that exist because models
specifically fail at them (base conversion, struct recovery, writing findings back).

> **Scope and ethics.** This skill supports legitimate reverse engineering: malware *analysis*
> and triage, vulnerability research, interoperability, firmware/protocol analysis, CTFs, and
> crackmes. It is about *understanding* and *documenting* binaries. Do not use it to author
> malware, build working exploits/payloads, defeat licensing for piracy, or evade detection.
> Analyzing how a sample works is fine; weaponizing it is not.

---

## When this skill triggers: first three moves

Before any deep work, orient. Skipping this is how analyses go wrong from the start.

1. **Confirm the live tool surface.** Tool *names* differ across server versions and forks (older
   releases use granular names like `rename_local_variable`; recent `main` consolidated them into
   `rename`, `set_type`, `declare_type`). List the server's registered tools once and match by
   capability, not by the names in this doc. Full mapping and legacy↔current table:
   `references/tool_reference.md`.
2. **Triage the binary** so you know what you're in and where the interesting code is — run
   `scripts/ida_triage.py` (see "Binary-level workflow" below).
3. **Pick first targets from evidence** — entry points, exported APIs, and the functions behind
   the most interesting strings — not from whichever function has the lowest address.

**Reversing a game?** Stop and read `references/game_re.md` before the manual loop. Games carry
metadata (IL2CPP `global-metadata.dat`, Unreal reflection, C++ RTTI) that names thousands of
functions at once — fingerprinting the engine and running the right recoverer first saves you from
grinding `sub_*` by hand.

---

## Prime directive: write findings back, don't just describe them

Every conclusion you reach about the code must be persisted into the IDB with a tool call.
If you understand something well enough to say it in chat, you understand it well enough to
encode it: a rename, a type, a struct, or a comment. Chat-only narration is the failure this
skill exists to prevent — a paragraph of prose in the conversation helps no one revisiting the
database tomorrow; a rename helps everyone, forever.

So: prefer **acting** over **reporting**. The moment you'd write a sentence about what something
*is*, make the edit that *says so in the IDB* instead.

| When you catch yourself writing… | Do this instead |
|---|---|
| "v3 is probably a loop counter." | `rename` v3 to `i` / `index`. |
| "This dereferences offset 0x10, maybe a length field." | `declare_type` the struct, `set_type` it onto the var so Hex-Rays shows `obj->length`. |
| "a1 is likely a pointer to a config struct." | Fix the prototype with `set_type`; re-decompile. |
| "This function seems to decrypt a string." | `rename` to `decrypt_string`, `set_comments` on the algorithm, document key/IV. |
| "0x6C616D is some constant." | `int_convert` it — it's an ASCII tag — then comment it. |

---

## The core loop (run per function until "done")

Work one function at a time. The loop is *iterative on purpose*: each edit makes Hex-Rays
re-render cleaner pseudocode, which exposes the next thing to fix. Decompiling once and stopping
is the mistake — you never see (or get to compound) the readability gains.

1. **Decompile.** `decompile(addr)` to get current pseudocode. Read it as a *hypothesis to test*, not a transcript.
2. **Orient with ground truth, not guesses.** Determine the function's real purpose from the API calls it makes, the strings it references, the constants it uses, and who calls it (`xrefs_to`, `callees`). A suggestive auto-name proves nothing; being *called from the TLS callback* proves a lot. Resolve any numeric value with `int_convert`.
3. **Rename for meaning.** `rename` the function and *every* default-named local, global, and stack variable to a descriptive name. No `vN`, `aN`, `sub_*`, `dword_*`, `loc_*` should survive in code you've analyzed. A slightly-wrong name you fix later beats `v14` forever.
4. **Recover types and structs — the highest-leverage step.** Wherever you see `*(x + offset)` arithmetic, define the structure with `declare_type` and apply it with `set_type` (use `infer_types` as a starting point). Hex-Rays will rewrite the offset math into `x->field_name` across the whole function at once. Fix pointer/array/signedness mistakes the decompiler made. This single habit accounts for most of the difference between sludge and readable code — this is the step to slow down and think on.
5. **Comment the non-obvious.** `set_comments` on the algorithm, the *why* behind tricky branches, decoded constants, and anything that took effort to understand. Comments land in both disassembly and pseudocode. Don't comment the obvious — comment what the next analyst would otherwise have to re-derive.
6. **Re-decompile and verify.** Decompile again. Confirm your edits took effect and the output is genuinely more readable. If a type made things worse, revert it. Then move to the next function.

### Definition of done (per function)

A function is "done" when:
- it has a descriptive name reflecting its actual purpose (not `sub_*`);
- zero default-named identifiers remain (`vN`/`aN`/`dword_*`/etc.);
- pointer-offset arithmetic has been replaced by struct field access wherever a struct fits;
- argument and return types are correct;
- the core logic and any non-obvious behavior are commented.

Use `scripts/re_progress.py` to measure this across the whole database and find what's left.

---

## Anti-hallucination: the operations you are worst at

Be honest about where models fail. RE depends heavily on exactly the operations you are *least*
reliable at — base conversion, byte order, pointer arithmetic — and you will produce confident,
fluent, wrong answers if you do them in your head. The fix is not "try harder"; it's "don't do
them in your head at all."

**Self-check:** before you state any numeric fact, address, offset, decoded constant, or byte
interpretation, ask — *did I read or convert this with a tool, or did I compute it mentally?* If
mentally, stop and route it through a tool before it enters your analysis. One transposed nibble
silently invalidates everything downstream.

- **Never convert number bases by hand.** Always use `int_convert` for hex ↔ decimal ↔ bytes ↔ ASCII ↔ binary. If math beyond conversion is needed, say so explicitly rather than computing it inline (consider a math MCP for heavy arithmetic).
- **Read real data instead of assuming it.** Use `get_bytes`, `get_int` (with explicit width/endianness like `u32le`), `get_string`, `read_struct`, and `get_global_value` to read what's actually in the binary. Do not invent values.
- **Derive purpose from evidence.** Base claims on `xrefs_to`, `callees`, imports, and strings — not on an auto-generated name.
- **Trust the binary over old comments.** Stale or wrong pre-existing comments are common; verify against the actual code before relying on them.

---

## Binary-level workflow (the phases around the loop)

Don't start renaming function #1 blindly. Orient, remove noise, then go deep. Full detail and
worked patterns live in `references/methodology.md`; the short version:

1. **Recon / triage.** Run `scripts/ida_triage.py` (or read its sections via `py_eval`) to inventory entry points, segments and their entropy, imports (with commonly-abused APIs flagged), strings, and anti-analysis indicators. This tells you what kind of binary you're in and where the interesting code is.
2. **Deobfuscation pre-pass.** You perform *badly* on obfuscated code and will narrate nonsense with full confidence — so neutralize string encryption, import/API hashing, control-flow flattening, and anti-decompilation tricks *before* deep analysis. If the binary is heavily obfuscated, fix that first; everything downstream depends on it.
3. **Resolve library code.** Apply FLIRT signatures (and/or Lumina) so the C runtime, STL, and known library functions are identified automatically. This stops you from wasting effort renaming `std::vector` internals and sharply improves accuracy on the code that's actually the author's.
4. **Systematic cleanup.** Now run the core loop in a sensible order: start from entry points, exported/imported API usage, and string cross-references, then follow `xrefs_to` outward. Analyzing callees before their callers often lets you name the parent correctly. Let the database's improving state guide what to tackle next.
5. **Document.** Maintain a running `report.md` (or `RE/*.md`) capturing what each major function does, recovered structures, the overall control/data flow, and any IOCs. When you finish, the report plus the cleaned IDB *are* the deliverable.

---

## MCP tool quick-map

Confirm names against the live tool list (see "first three moves"). Grouped by what you reach for:

- **Read code:** `decompile`, `disasm`, `analyze_funcs`, `basic_blocks`, `callgraph`
- **Find things:** `lookup_funcs`, `list_funcs`, `list_globals`, `imports`, `xrefs_to`, `xrefs_to_field`, `callees`, `find_regex`, `find_bytes`, `find_insns`, `search_structs`
- **Read data (ground truth):** `get_bytes`, `get_int`, `get_string`, `get_global_value`, `read_struct`, `int_convert`
- **Write (the important part):** `rename` (funcs/locals/globals/stack), `set_type` / `infer_types`, `declare_type`, `set_comments`, `define_func`, `define_code`, `undefine`, `declare_stack` / `delete_stack`, `patch_asm`
- **Dynamic (extension, enable with `?ext=dbg`):** `dbg_start`, `dbg_run_to`, `dbg_step_*`, breakpoints, registers, `dbg_read`/`dbg_write`, `dbg_stacktrace`
- **Escape hatch:** `py_eval(code)` runs arbitrary IDAPython in IDA's context — use it for anything the dedicated tools don't cover, including running the bundled scripts.

Full mapping, batch payload shapes, and the legacy↔current name table: `references/tool_reference.md`.

---

## Operating the MCP tools well

Knowing *which* tool to call isn't enough; most wasted effort comes from mis-operating the tools
themselves. These habits compound — getting them right makes every loop faster and your "done"
checks actually trustworthy.

- **Batch your writes.** The API is batch-first: `rename` takes all four namespaces (func/data/local/stack) in one call, and `set_type` / `set_comments` take lists. Collect every edit for a function, then send *one* batch per tool — not twenty calls for twenty variables. It's faster and keeps your context clean.
- **Check the per-item `error` field, then retry.** A batch returns a parallel list where each item is `{..., "error": null | "message"}`. A call that "succeeded" can still have half its items rejected (invalid type, Hex-Rays refused a prototype). Read every item's error, fix the cause, and re-send the failures. Don't mark anything done off a return you didn't inspect.
- **Verify the write actually landed — don't trust the return.** `set_type` can be silently rejected or only partly applied. The proof is the re-decompile: after applying a struct, confirm `*(a1 + 0x10)` actually became `a1->length`. If it didn't, the type didn't take — fix it rather than moving on.
- **Follow pagination to completeness.** Search/listing tools (`xrefs_to`, `list_funcs`, `find_*`) paginate via a cursor (`{next: offset}` until `{done: true}`). Stopping at page one gives you a *subset* of xrefs — and "called from one place" when it's actually forty leads to a wrong parent name. Drain the cursor before drawing conclusions about callers or references.
- **Spend context wisely.** For orientation, `analyze_funcs` bundles decompile + asm + xrefs + callees + strings + constants in a single call — cheaper than six separate ones. For pure read-only state (segments, structs, imports), read the MCP **resources** (`ida://idb/segments`, `ida://structs`, `ida://import/{name}`) instead of issuing tool calls.
- **Treat any prior decompile as stale after a write.** A `rename` or `set_type` changes the pseudocode. If you keep reasoning over the listing already in your context, you'll reference names that no longer exist. Re-decompile before the next analytical step, not just at loop's end.
- **Declare dependent types in order.** `declare_type` parses C — a struct that references another type needs that type (or a forward declaration) first; pad fields you don't understand yet with `char field_N[size];` so offsets stay aligned. Nested structs and vtables fail to parse otherwise.
- **Use `py_eval` as a last resort, and capture its value.** Prefer the typed, dedicated tools (they're safer and validated). Reach for `py_eval` only for bulk operations or APIs with no wrapper, and remember it returns the *last expression's* value — return it explicitly rather than relying on `stdout`.
- **In headless `idalib`, target the right database.** With multiple DBs open, pass `database=` (session id / path) on each call. Omitting it writes your renames into whatever DB is current — a silent, painful mix-up.

### A worked pass (what the tool calls actually look like)

Cleaning one function `sub_401000` that decrypts a config blob:

1. `lookup_funcs(["sub_401000"])` → resolve the address.
2. `analyze_funcs(["0x401000"])` → one call for pseudocode + xrefs + callees + strings + constants.
3. See `*(a1 + 0x10)` and a constant `0x6C616D66`. `int_convert(["0x6C616D66"])` → it's the ASCII tag `"flam"` (never decode this in your head).
4. `declare_type` the layout: `struct Config { unsigned int magic; char* name; unsigned int length; };`
5. `set_type([{func:"0x401000", local:"a1", type:"Config*"}])`.
6. `decompile("0x401000")` again → **verify** `*(a1+0x10)` is now `a1->length`. (If not, the type was rejected — fix and repeat.)
7. One batched `rename`: func → `decrypt_config`, plus the `local`/`stack` vars; one `set_comments` for the algorithm and the decoded tag.
8. Check each returned item's `error`; re-send any that failed. Move to the next function.

---

## When to drop to disassembly or dynamic analysis

The decompiler is the default lens; reach lower when it's lying or missing:

- **Disassembly (`disasm`)** when the decompiler output looks wrong, the function involves heavy SIMD/intrinsics, calling conventions are non-standard, or you need exact instruction-level behavior (flags, alignment, jump tables).
- **Dynamic analysis (debugger extension)** when static analysis stalls: self-modifying or packed code, runtime-computed values, encrypted strings decrypted in memory, or you simply want to confirm a hypothesis by watching it run. Enable `?ext=dbg`, set breakpoints at the interesting addresses, read memory/registers — then feed what you learn *back* into renames, types, and comments. Run untrusted samples only in an isolated, disposable VM.

---

## Bundled scripts

Run these inside IDA (File ▸ Script file) or paste their bodies into `py_eval`. They are
analysis/cleanup aids — they read and report, or help you build structures; none changes program
behavior. See each script's header for usage and its heuristics/limits.

**Recon & finding the interesting code (do these early):**
- **`scripts/ida_triage.py`** — The recon pass; run first on any new sample. Metadata, segments with Shannon entropy (flags packed/encrypted regions), imports with commonly-abused APIs highlighted, notable strings, and anti-analysis indicators.
- **`scripts/function_capabilities.py`** — Lightweight capa-style ranking: attributes imported APIs to the functions that call them and ranks functions by how many behavior categories (net/crypto/inject/persist/anti/…) they touch, so you know where to start.
- **`scripts/string_xref_map.py`** — The "follow the strings" pivot: maps notable strings (URLs/IPs/paths/registry/mutexes) to the functions that reference them.
- **`scripts/crypto_const_scan.py`** — Findcrypt-style scan for known crypto constants (AES S-box, SHA/MD5 tables, Blowfish P-array, CRC32 table, Base64 alphabets, ChaCha sigma) and the functions that use them. Won't catch table-less ciphers like RC4 — find those behaviorally.

**Deobfuscation pre-pass:**
- **`scripts/stackstring_recover.py`** — Reconstructs strings built on the stack via immediate stores (a common way to hide strings from `strings`), so you can comment the real literals.

**Type recovery (step 4 of the loop):**
- **`scripts/struct_recovery.py`** — For a chosen function, collects `[base + displacement]` accesses, infers field widths, and emits a C `struct` skeleton to hand to `declare_type` and then `set_type` onto the base pointer.

**Progress & documentation:**
- **`scripts/re_progress.py`** — Operationalizes the definition-of-done: percentage of functions still auto-named, functions lacking comments, and (with `DEEP = True`) the functions with the most default-named variables. Keeps you honest about what's left.
- **`scripts/export_report.py`** — Harvests renamed functions, their comments, and declared structs/enums and writes a `report.md` skeleton in the `methodology.md` template, with TODO placeholders for the prose.

**Comparison & dynamic analysis (situational):**
- **`scripts/function_fingerprint.py`** — Exports relocation-independent per-function fingerprints (normalized mnemonics + operand types) to JSON; run in two databases to diff samples/versions/patches, or to spot duplicated code within one binary.
- **`scripts/dump_region.py`** — Debugger helper to dump a memory region or segment to disk (e.g. an unpacked payload after a breakpoint) and report its entropy. Needs the debugger extension (`?ext=dbg`); run untrusted samples only in an isolated VM.

---

## References

- **`references/tool_reference.md`** — Complete MCP tool → RE-action mapping, batch payload formats, and the legacy↔current name table. Read this when you need exact tool names/arguments.
- **`references/methodology.md`** — The deeper playbook: triage checklist, naming conventions, struct/type recovery technique, calling-convention cheats, common code patterns (loops, switch tables, crypto, string ops), and per-platform notes (Windows/Linux/macOS/embedded). Read this when you want the "how a senior actually thinks" detail.
- **`references/game_re.md`** — The game-binary playbook. Read this *first* whenever the target is a game: fingerprinting the engine (Unity/IL2CPP, Unreal, Source, etc.) and middleware, recovering names wholesale via IL2CPP dumpers / Unreal SDK generators / RTTI, typing math+SIMD and the entity struct, recognizing DRM/anti-cheat, and building update-resilient signatures. Games reverse very differently from malware — metadata names the world before you touch the manual loop.
- **`references/reading_list.md`** — Curated RE books (with what each is good for) plus high-quality online references, practice sites, and primary architecture/ABI documentation. Point the user here when they ask how to get better at RE.

---

## Common pitfalls (the short list)

Most reduce to one of these. If you're stuck or producing confident sludge, check here first:

- **Narrating instead of editing** — the cardinal sin. Prose without tool calls means nothing landed in the IDB. Write it back.
- **Skipping struct recovery** — leaving `*(a1 + N)` everywhere is the fastest way to keep pseudocode unreadable.
- **Mental hex math** — guaranteed to eventually corrupt an analysis. Route through `int_convert`.
- **Trusting auto-names and stale comments** — `sub_*` and old comments are leads, not facts.
- **Turning the model loose on obfuscated or unsignatured binaries** — deobfuscate and apply FLIRT/Lumina first, or expect confident garbage.
