---
name: autobot-health-check
description: Check an installed AutoBot workspace with its read-only doctor and focused runtime diagnostics. Use for installation health, capability readiness or a requested health report; a check alone does not authorize repairs.
---

# AutoBot health check

Resolve the intended installed project and receipt before running commands. Do not select a different installation or treat a release-source checkout as an installed workspace. Read `docs/CLI-REFERENCE.md` and `docs/TROUBLESHOOTING.md` from that installation when needed for interpretation.

Run from the verified installation root:

```sh
./runtime/bin/autoassist version
./runtime/bin/autoassist doctor
```

The installation doctor is read-only and does not need sign-in or Node. Separate installation integrity from optional capabilities. When Node 22 or newer is available, use the supported read-only core commands:

```sh
./runtime/bin/autoassist core status < /dev/null
./runtime/bin/autoassist core capabilities < /dev/null
./runtime/bin/autoassist core heartbeat < /dev/null
./runtime/bin/autoassist core orphans < /dev/null
```

Scope any further inspection to the reported subsystem or requested root. Do not export private memory, dump whole task records, search personal stores, run `tick`, enable a service, change settings, perform a send or launch UI/permission probes as part of this check. Never run the release privacy scanner on a populated personal installation.

Report installation integrity, runtime availability and any actionable diagnostic separately. A missing optional integration is not proof the installation failed. Native Voice, Goals, Computer Use and schedules require actual native capability evidence; a local marker does not prove they work. Monitoring with no fresh observation is unknown, not proof of a stalled task.

For each relevant failure, give the observed code, affected capability and smallest next diagnostic or repair. Do not copy sensitive payloads into the report. Reuse an existing issue when appropriate. Run only the smallest focused check needed to resolve ambiguity, and stop once the affected contract is established.

Immediately before reporting changing runtime health, take one final bounded read of the authoritative result. State what was actually checked. A request to diagnose or report health does not authorize production repair; carry out a repair only when the user's request includes it.
