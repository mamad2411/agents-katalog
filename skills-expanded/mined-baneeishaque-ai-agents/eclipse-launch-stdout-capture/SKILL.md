---
name: eclipse-launch-stdout-capture
description: Patch an Eclipse PDE `.launch` configuration so the runtime JVM's stdout
    and stderr are captured to a file adjacent to the `.launch` file, surfacing
    telemetry / lifecycle output (e.g., `[telemetry ...]` lines) that bypasses
    application-managed log appenders.
category: Eclipse
---

# Eclipse Launch Stdout Capture Skill (v1)

This skill patches an Eclipse PDE / Tycho `.launch` file (a project-shared launch configuration of type
`org.eclipse.pde.ui.RuntimeWorkbench` or `org.eclipse.jdt.launching.localJavaApplication`) so that the
launched JVM's `System.out` and `System.err` are teed to a file on disk. The captured file is the **only**
sink that surfaces output written before application loggers attach, written after they detach, or written
to streams the application logger has deliberately bypassed (e.g., a telemetry exporter holding a saved
reference to the original `PrintStream` so its lines survive a `System.setOut(...)` swap).

***

## 1. When to Use

Apply this skill when **all** of the following are true:

1. The workflow targets an Eclipse PDE / Tycho `.launch` file checked into the project (not a workspace-local
   launch stored under `.metadata/`).
2. The hosted application emits diagnostic or telemetry lines to `System.out` / `System.err` that do **not**
   appear in the application's own log files (because those files are written by a separate logging
   appender that does not see the original stdout stream).
3. The user needs the captured output as a permanent artifact — for verification, audit, regression analysis,
   or to feed into a downstream parser.

Typical trigger: a telemetry library following the resilience pattern in
[`eclipse-pde-telemetry-resilience`](../eclipse-pde-telemetry-resilience/SKILL.md) emits `[<tag> <ts>] ...`
lifecycle lines, but they are not in `tool.log` / `<host>.log` / `workspace.log` etc. because those files
are written by a different appender. The lines exist only in the Eclipse Console view's in-memory buffer
and vanish when the run ends.

***

## 2. The Minimum Viable Patch

Add exactly **one** attribute to the `.launch` XML inside the `<launchConfiguration>` root element:

```xml
<stringAttribute key="org.eclipse.debug.ui.ATTR_CAPTURE_IN_FILE"
                 value="${workspace_loc:/<project-name>}/<launch-basename>.log"/>
```

Eclipse infers the rest:

- `capture_output` defaults to `true` whenever `ATTR_CAPTURE_IN_FILE` is present.
- `ATTR_APPEND_TO_FILE` defaults to `false` (each run overwrites the previous log).

If overwrite-vs-append needs to be explicit, add the optional sibling:

```xml
<booleanAttribute key="org.eclipse.debug.ui.ATTR_APPEND_TO_FILE" value="false"/>
```

### Placement inside the XML

Insert the attribute in **alphabetical order by key prefix** to match Eclipse's canonical serialization.
The relevant ordering points:

1. `org.eclipse.debug.core.*` attributes (e.g., `preferred_launchers`).
2. `org.eclipse.debug.ui.ATTR_APPEND_TO_FILE` (if present).
3. `org.eclipse.debug.ui.ATTR_CAPTURE_IN_FILE`.
4. `org.eclipse.jdt.launching.*` attributes.

A correctly placed example from a `RuntimeWorkbench` launch:

```xml
<stringAttribute key="location" value="${workspace_loc}/runtime-<product>.product"/>
<booleanAttribute key="org.eclipse.debug.core.ATTR_FORCE_SYSTEM_CONSOLE_ENCODING" value="false"/>
<mapAttribute key="org.eclipse.debug.core.preferred_launchers">
    <mapEntry key="[run]" value="org.eclipse.pde.ui.RuntimeWorkbench"/>
</mapAttribute>
<stringAttribute key="org.eclipse.debug.ui.ATTR_CAPTURE_IN_FILE"
                 value="${workspace_loc:/<project-name>}/<launch-basename>.log"/>
<stringAttribute key="org.eclipse.jdt.launching.JRE_CONTAINER" value="..."/>
```

***

## 3. Attribute Reference & Common Mistakes

| Attribute key | Package | Purpose |
|---|---|---|
| `org.eclipse.debug.ui.ATTR_CAPTURE_IN_FILE` | **`.ui.`** | Absolute path or workspace-variable path where stdout+stderr are teed. |
| `org.eclipse.debug.ui.ATTR_APPEND_TO_FILE` | **`.ui.`** | `true` = append across runs, `false` = overwrite. Defaults to `false`. |
| `org.eclipse.debug.core.capture_output` | `.core.` | Master switch. Implicit `true` when `ATTR_CAPTURE_IN_FILE` is set. |

**Common authoring mistakes** (encountered live):

- ❌ Writing `org.eclipse.debug.core.ATTR_CAPTURE_IN_FILE` — the file attrs live in **`.ui.`**, not `.core.`.
  Eclipse silently ignores the wrong-package keys; the *Common* tab's Output File field stays empty.
- ❌ Setting only `capture_output=true` with no file path — output goes to the Console view only, not to disk.
- ❌ Wrapping the path in `<stringAttribute>` with the workspace variable malformed — Eclipse falls back to
  literal-path resolution. Use `${workspace_loc:/<project>}` (with the colon-and-leading-slash form).

***

## 4. Path Naming Convention

The captured log MUST land **adjacent to the `.launch` file** with the same basename + `.log` extension:

- `ice_dcg_ats.product.launch` → `ice_dcg_ats.product.log`
- `myapp_debug.launch` → `myapp_debug.log`

This makes the capture file trivially discoverable, automatically scoped to the launch it documents, and
keeps multiple coexisting launchers from clobbering each other's output.

The canonical path expression:

```text
${workspace_loc:/<containing-project-name>}/<launch-file-basename>.log
```

`<containing-project-name>` MUST be the Eclipse project that hosts the `.launch` file, not the launched
product or workspace root.

***

## 5. Patching Protocol

### 5.1 Edit-on-disk approach (preferred for automation)

1. Read the target `.launch` file and locate the `<mapAttribute key="org.eclipse.debug.core.preferred_launchers">`
   block (every PDE/JDT launch has one).
2. Insert the `ATTR_CAPTURE_IN_FILE` `<stringAttribute>` element on the line immediately **after** the closing
   `</mapAttribute>` tag.
3. Save the file.
4. **Refresh in Eclipse** — see §5.3.
5. Verify the Common tab — see §6.

### 5.2 UI-driven approach (when Eclipse normalizes the file aggressively)

Some Eclipse builds normalize `.launch` files on save and prune attributes they don't recognize at parse
time. If the edit-on-disk approach does not surface in the Common tab after a refresh, use the UI:

1. **Run → Run Configurations…**
2. Select the target launch in the left tree.
3. Click the **Common** tab.
4. Scroll to **Standard Input and Output** (near the bottom).
5. Tick the **Output File** checkbox.
6. Click **Workspace…**, navigate to the containing project, type the filename as `<launch-basename>.log`,
   click OK. The field will show `${workspace_loc:/<project>/<launch-basename>.log}` (Eclipse's preferred
   alternate path syntax — semantically equivalent).
7. Leave **Append** unchecked unless explicit append behaviour is required.
8. Click **Apply**, then **Close**.

### 5.3 Refreshing Eclipse's in-memory cache

Eclipse loads `.launch` files into its `LaunchManager` at startup and on workspace refresh; it does **not**
re-read disk edits while the IDE is open. After an edit-on-disk patch:

1. **F5** on the containing project in the Project Explorer.
2. **Close** any open Run Configurations dialog without clicking **Apply** — see §7.
3. Re-open Run → Run Configurations… → Common tab to verify.

If the Common tab is still blank after F5, restart Eclipse (`File → Restart`). Do **not** click *Apply* in
the Run Configurations dialog beforehand.

***

## 6. Verification

After patching and refreshing:

1. **UI check**: Run → Run Configurations… → target launch → Common tab → *Standard Input and Output* →
   confirm:
    - ☑ **Output File** is ticked and shows the workspace-variable path.
    - ☐ **Append** is unchecked (or ticked if explicitly requested).
2. **Functional check**: Run the launch. After completion, F5 the containing project. The `.log` file MUST
   appear adjacent to the `.launch` file.
3. **Content check**: Open the `.log` file. It MUST contain the same lines that were visible in the
   Eclipse Console view, including any pre-init banner, lifecycle, and post-shutdown output from
   `System.out` / `System.err`. For a telemetry-resilience host, grep for the configured marker
   (e.g., `[telemetry `, `[OTEL `, `[telemetry `) and verify the lifecycle catalogue documented by the
   upstream skill (e.g.,
   [`eclipse-pde-telemetry-resilience/SKILL.md §6.1`](../eclipse-pde-telemetry-resilience/SKILL.md#61-lifecycle-event-catalogue))
   appears end-to-end.

***

## 7. Pitfalls & Gotchas

| Hazard | Symptom | Mitigation |
|---|---|---|
| Wrong package on `ATTR_CAPTURE_IN_FILE` (`.core.` vs `.ui.`) | Common tab Output File stays blank after refresh | Use `org.eclipse.debug.ui.ATTR_CAPTURE_IN_FILE`. |
| Apply-overwrites-edit | Disk edit lost; Common tab reverts to blank | Never click *Apply* in Run Configurations after an external disk edit until the dialog has been re-opened and shows the new state. **Close** the dialog (Don't Save) to discard the stale in-memory copy. |
| In-flight run not picking up edit | New launch attribute absent from current run's log | Eclipse snapshots launch attributes at JVM start. Edits during a run apply only to the **next** launch. |
| "Delete" on a local-shared `.launch` deletes the file | File missing from disk; revert via `git checkout` | In Eclipse, *Delete* on a launch stored as a project file (project-shared launch) physically removes the file. The "re-discovered on refresh" behaviour applies only to workspace-local launches under `.metadata/.plugins/org.eclipse.debug.core/.launches/`. |
| Wrong launcher patched | Captured log appears but with content from a different run; or no log appears for the run the user expects | Confirm which `.launch` file the user actually invokes — the filename in the Run Configurations tree may differ from the launch the user assumes. Audit with `grep -l 'ATTR_CAPTURE_IN_FILE' *.launch` to see all patched candidates. |
| Filename mismatch after refactor | Captured log lands at a stale name (e.g., the old launcher's name) | The path is a literal string in the XML — renaming the `.launch` file does NOT update `ATTR_CAPTURE_IN_FILE`. Re-patch the path manually. |
| Application closes stdout (rare) | Log file is created but empty after the first few lines | The application's logger has called `System.out.close()`. The telemetry library must hold a saved reference to the original `PrintStream` (see [`eclipse-pde-telemetry-resilience`](../eclipse-pde-telemetry-resilience/SKILL.md) §4) and call `flush()` explicitly after each line. |

***

## 8. Related Skills

- [`eclipse-pde-telemetry-resilience`](../eclipse-pde-telemetry-resilience/SKILL.md) — Generates the
  `[telemetry <ts>] ...` lifecycle lines that this skill captures. Without that resilience pattern (saved-stream
  reference + explicit flush), the lines may not reach the captured file even when capture is configured
  correctly.
- [`eclipse-pde-jdk-migration`](../eclipse-pde-jdk-migration/SKILL.md) — Sibling Eclipse PDE skill covering
  JDK-version migration of `.classpath` / `MANIFEST.MF` / `*.launch` / `pom.xml`. The `.launch` JRE pin
  (`org.eclipse.jdt.launching.JRE_CONTAINER`) lives in the same file modified by this skill.

***

## 9. Composition by Higher-Level Skills

This skill is currently atomic (single-step XML patch). No higher-level skills compose it as of v1. If a
future workflow needs to patch many `.launch` files in bulk (e.g., enable capture for every launcher in a
product project), wrap this skill inside a discovery composer following the Layered Composition Mandate.

***

## 10. Environment & Dependencies

No external tools required. The skill is a pure XML / filesystem edit. The Agent MUST verify only:

1. The target file exists and matches one of the Eclipse launch XML types:
    - `<launchConfiguration type="org.eclipse.pde.ui.RuntimeWorkbench">` (PDE Eclipse-Application launches).
    - `<launchConfiguration type="org.eclipse.jdt.launching.localJavaApplication">` (plain Java Application launches).
2. The containing Eclipse project name is known (used in `${workspace_loc:/<project>}`).
3. The user has confirmed which `.launch` file is in scope when multiple exist in the same project.
