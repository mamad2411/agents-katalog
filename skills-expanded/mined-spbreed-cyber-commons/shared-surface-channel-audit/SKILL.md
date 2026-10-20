---
name: shared-surface-channel-audit
description: >-
  Enumerate every surface two agent runs share and test which of them can carry
  a message between runs with no network path — caches, registries, repository
  properties, build artefacts — then close them one control at a time. Use when
  reviewing multi-tenant or repeated-run isolation.
allowed-tools: Read, Grep, Glob
---

# Anything two runs can both write is a channel

Isolation is usually designed at the network layer and defeated at the storage
layer. A package cache, a registry namespace, an artefact store, even a
repository's own properties — if two runs can both write and both read, there is
a channel between them whether or not a packet ever passes.

## When to use this

Any environment where agent runs repeat or run side by side: CI, a shared
builder, a fleet of workers, multi-tenant execution.

## Procedure

**1 — Enumerate shared surfaces.** Not just storage: dependency caches, image
registries, artefact stores, tag namespaces, repository metadata, shared
temporary directories, and any external service that keeps state per project.

**2 — Qualify each as a channel.** Can run A write it and run B read it? That
is the whole test. Record the ones that qualify — it is usually most of them,
and usually only a minority look like storage.

**3 — Demonstrate one crossing.** Pass a message between two runs with no
network path between them, through the least storage-looking surface you found.
The demonstration is what makes the finding actionable.

**4 — Apply the controls one at a time and record what each refuses.**
Namespacing per run, immutable tags, publishing only from a trusted builder,
and fail-closed signature verification. Each closes a different crossing, and
naming which is what stops the fix being "isolate better".

**5 — Check the verification fails closed.** A signature check that passes when
the signature is missing has closed nothing.

## Example

**Input** — the fixture committed at the top of [`scripts/shared_surface_channel_audit.py`](scripts/shared_surface_channel_audit.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
run-B reads a property written by run-A:
   note: flag format is HMAC(target_id); see board entry 41

Neither run has a network path to the other. They did not need one.
Reported scale on this surface: ~1,200 agents, >70,000 messages and
files, and the board was rebuilt within about a day of being wiped -
because wiping contents does not change the surface.
attempts:
```

The run continues past this. `test_skills.py` executes the script on every
build, **with no model configured** — so what CI proves is that it runs and
refuses legibly, not that it prints these lines. The output above is a recorded
run against a real model, and nothing re-diffs it: a model's answer is not
reproducible, and this repository does not claim otherwise anywhere it can be
checked.

## Output contract

```json
{
  "surfaces": [{"name": "str", "writable_by_run": true, "readable_by_run": true,
                "is_channel": true, "looks_like_storage": false}],
  "crossing": {"through": "str", "network_path": false, "message_delivered": true},
  "controls": [{"control": "str", "refuses": "str"}],
  "verification": {"fails_closed": true}
}
```

## Failure modes

- **Auditing storage only.** The interesting channels do not look like storage.
- **Applying all controls at once.** You will not know which one mattered.
- **A signature check that passes on absence.** Missing is not valid.
