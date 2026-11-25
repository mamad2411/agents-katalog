---
name: ghidra-scripting-java
description: >
  Ghidra Java scripting and extension-style automation: GhidraScript lifecycle,
  Program API, analyzers vs scripts, FlatProgramAPI, classpath/extensions, and
  headless postScripts in Java. Use for authorized binaries and internal tooling.
---

# Ghidra Scripting (Java)

## Scope And Authorization

- **In scope:** Java GhidraScript development for owned/authorized binaries and internal RE tooling.
- **Out of scope:** Building crackme keygens for commercial products you do not own;
  distributing decompiled sources against license/ROE.
- Java scripts run with Ghidra privileges on the local project — treat as trusted code.
- Use isolated projects for experimental analyzers.

## When To Use

- Need stronger typing / IDE support than Jython for large automations.
- Writing reusable analyzers or complex CFG walks.
- Integrating with Java-only Ghidra APIs or extension points.
- Team standardizes on Java for Ghidra CI scripts.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Simple exports / learning API | `ghidra-scripting-basics` |
| Headless CLI orchestration | `ghidra-headless-analyze` |
| Runtime debug printers | `gdb-python-pretty-printers` |
| Product Java style guide | `java-style-and-javadoc` |
| Implementation quality | `code-quality-standards` |

## Concepts

| Piece | Role |
| --- | --- |
| `GhidraScript` | Base class; `run()` entry |
| `FlatProgramAPI` | Inherited helpers (`toAddr`, `getFunctionAt`, …) |
| `Analyzer` | Plugin analysis phase (extension) vs one-shot script |
| `TaskMonitor` | Progress / cancel |
| `Console` | `println` output |
| Headless | Same scripts via `-postScript Foo.java` |
| Extension | Proper module with `extension.properties` for complex tools |

### Script vs analyzer

| | Script | Analyzer |
| --- | --- | --- |
| Trigger | Manual / headless | Auto-analysis schedule |
| State | One-shot | Should be re-runnable carefully |
| Packaging | `.java` in script dirs | Ghidra extension module |

## Workflow

### 1. Setup IDE (optional but recommended)

1. Use GhidraDev Eclipse instructions for your Ghidra version **or** IntelliJ community setups maintained by the community — match Ghidra release.
2. Point classpath at Ghidra installation jars.
3. Success: script compiles; `run()` lists functions.

### 2. Minimal GhidraScript

```java
// ExportFunctionCount.java
//@category Lab
//@menupath Tools.Lab.FunctionCount

import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;

public class ExportFunctionCount extends GhidraScript {
    @Override
    public void run() throws Exception {
        int count = 0;
        FunctionIterator it = currentProgram.getFunctionManager().getFunctions(true);
        while (it.hasNext()) {
            monitor.checkCancelled();
            Function f = it.next();
            println(String.format("%s %s", f.getEntryPoint(), f.getName()));
            count++;
        }
        println("Total: " + count);
    }
}
```

### 3. Common Program API tasks

```java
// Xrefs to an address
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.address.Address;

Address target = toAddr(0x401000);
for (Reference ref : getReferencesTo(target)) {
    println("from " + ref.getFromAddress());
}
```

```java
// Rename with user-defined source
import ghidra.program.model.symbol.SourceType;

Function f = getFunctionAt(currentAddress);
if (f != null) {
    f.setName("AUTO_interesting", SourceType.USER_DEFINED);
}
```

Always `monitor.checkCancelled()` in loops.

### 4. Script arguments (headless)

```java
String[] args = getScriptArgs();
if (args.length < 1) {
    printerr("Usage: Export.java <outPath>");
    return;
}
java.nio.file.Path out = java.nio.file.Paths.get(args[0]);
// write files...
```

```bash
analyzeHeadless PROJECT_DIR Proj \
  -process bin.elf \
  -postScript ExportFunctionCount.java /out/funcs.txt
```

### 5. Transactions for mutations

```java
int tx = currentProgram.startTransaction("Bulk rename");
boolean commit = false;
try {
    // mutations...
    commit = true;
} finally {
    currentProgram.endTransaction(tx, commit);
}
```

### 6. Packaging and script paths

| Method | Use |
| --- | --- |
| Script directories in UI | Quick labs |
| `-scriptPath` | Headless CI |
| Full extension | Shared analyzers, multi-class tools |

For extensions: follow Ghidra skeleton (`build.gradle`, `extension.properties`), build zip, install via File → Install Extensions.

### 7. Testing

1. Unit-style: small sample binary with known function count.
2. Headless CI job asserting output file line count.
3. Negative: cancel monitor mid-loop (manual).
4. Re-run idempotency for renames (`AUTO_` prefix).

### 8. Performance tips

- Avoid decompiling every function unless needed (`DecompInterface` is expensive).
- Narrow address sets before heavy analysis.
- Cache `Listing`, `FunctionManager` references outside tight inner loops when safe.
- Log progress every N items via `monitor.setMessage`.

## API quick table

| Task | API |
| --- | --- |
| Functions | `FunctionManager` |
| Memory | `Memory` / `getByte` |
| Symbols | `SymbolTable` |
| Refs | `ReferenceManager` |
| Data types | `DataTypeManager` |
| Decompiler | `DecompInterface` (use sparingly) |
| Bookmarks | `BookmarkManager` |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Structure | Small classes, clear `run()` | God-script 3k lines |
| Cancel | `checkCancelled` | Uninterruptible loops |
| Mutations | Transactions | Partial rename on exception |
| Decompile | Targeted | Decompile entire firmware in script |
| Secrets | No sample exfil in script output | Upload binaries to public gist from script |

## Output Checklist

- [ ] Ghidra version + Java toolchain recorded
- [ ] Authorization for samples noted
- [ ] Script compiles and runs in Script Manager
- [ ] Headless invocation documented if used
- [ ] Mutations wrapped in transactions
- [ ] monitor cancellation handled
- [ ] Output paths parameterized
- [ ] Idempotency considered
- [ ] Extension packaging decided if multi-class
- [ ] `code-quality-standards` / Java style applied

## Rules

- Authorized analysis only.
- Prefer scripts for one-shot; analyzers for productized passes.
- Do not decompile/export proprietary code into public logs.
- Check cancellation and use transactions.
- Simple tasks may belong in `ghidra-scripting-basics` instead.
