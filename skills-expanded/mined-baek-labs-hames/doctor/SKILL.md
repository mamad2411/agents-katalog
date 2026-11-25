---
name: doctor
description: Diagnose a Hames installation without changing it when the user invokes /doctor.
---

# Doctor

Inspect the plugin and project configuration in read-only mode and report actionable recovery options.

Check config parsing and schema, required `.hames/` paths, entry boundary blocks, contract hashes, progress, review and knowledge linkage, evidence linkage, session ownership, four skills, and hook files.

Separate configured state, observed runtime behavior, and checks that have not been run. A file's presence does not prove host discovery or hook execution. Do not modify, clear, recover, or select anything. Show a failed check's impact and only recovery actions the bundled runtime supports.

Run the bundled `runtime/doctor.js` against the current project root and report its check results without treating warnings or unreadable output as a pass.

Report configured hook handlers, local execution observations, and unverified host trust separately. Inspect index pending markers and queued updates without clearing them. Warn about stale owners and require an explicit recovery choice before changing a lock. `/index` owns inventory and file-rule auditing. An unconfigured root should be offered `/setup` without changing files.
