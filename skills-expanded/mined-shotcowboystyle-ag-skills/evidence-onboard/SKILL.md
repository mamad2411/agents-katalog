---
name: evidence-onboard
description: Use when running for the first time or on a new machine — checks the environment, offers to install what is missing, configures a storage destination, and ends by showing the shortest working pipeline for this host. Triggers - "set up evidence-ops", "first run", "get me started with evidence handling".
allowed-tools: Bash(command *), Bash(mkdir *), Bash(test *), Read, Write
---

# Onboard

Get this pipeline working on a machine for the first time, and finish by showing the
shortest sequence that actually runs here.

## When to use

- First run, on a new machine.
- After an operating system upgrade that may have removed tooling.
- When handing the setup to someone else.

## Procedure

### 1. Check the environment

Run environment-check. Report which stages are available and which are blocked, and by
what.

### 2. Offer to install what is missing

Present the list and let the user choose. Nothing here is mandatory — the pipeline
degrades in a defined way:

| Missing | Consequence |
| --- | --- |
| SHA-256 tool | nothing works; this one is required |
| `exiftool`, `mediainfo` | metadata inspection unavailable |
| `single-file` | web capture unavailable |
| `ots` | no independent time anchoring |
| `bagit.py` | no standard packaging for handover |
| `rclone`, `aws` | local only, no offsite replication |
| `b3sum`, `mat2` | optional, no effect on the core pipeline |

Run evidence-install-deps only for what was accepted. Stop at the first refusal and continue with
the remaining stages.

### 3. Configure a destination

Offer setup-storage. Skip it if the collection is local-only for now, and record that
choice so it is a decision rather than an oversight.

### 4. Create or find a store

If the working directory has no evidence tree, offer init-evidence-store. If it already
has one, report its path and record count instead.

### 5. Show the working pipeline

End by printing the sequence that runs on this host given what is installed, with the
unavailable steps named and marked. For example:

```
capture-web  →  log-custody  →  timestamp-evidence  →  verify-bundle
                                (unavailable: ots not installed)
```

Give one concrete next command the user can run immediately.

## Output

- A configured host, a storage decision on the record, and possibly an evidence store.
- A printed pipeline showing exactly what works here.

## Notes

- Do not install anything without agreement, and do not treat silence as agreement.
- A partial setup is a legitimate outcome. Record what was skipped so the gap is
  visible later.
