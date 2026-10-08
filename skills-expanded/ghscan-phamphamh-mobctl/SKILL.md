# Example: driving mobctl from an AI coding agent

This is the template I give my coding agent (Claude Code) as a "skill" so it can operate the
physical iPhone autonomously. The key idea: **the deliverable is not "I changed the code" —
it's a screenshot of the working result.** The agent codes, drives the phone to verify, keeps
iterating until it's right, and always ends with a capture.

Adapt the bundle id, scheme and testID conventions to your own app.

---

## The proof loop

When asked to build or fix a visible UI change:

1. **Code** the change (put a `testID` / accessibility id on every interactive element).
2. **Preflight:** `./scripts/up.sh` — make sure the dev build on the device is current.
3. **Navigate** to the screen you touched: `mobctl launch --fresh`, then
   `mobctl deeplink myapp://<route>` or `mobctl tap` / `mobctl scrollto` until you're on it.
4. **Capture + judge:** `mobctl observe --shot`, then read the screenshot. Does it match the
   request? Crash? Broken layout? For animations, take 2–3 quick captures.
5. **Iterate** if it's off: each mismatch is a finding → re-code → back to step 3.
6. **Post the proof:** show the validated screenshot with one clear sentence.

**Guardrails:** cap at ~3–4 rounds, then stop and report the blocker with the last capture
(no infinite loops). Two consecutive WDA session failures → stop and explain. If you added a
native dependency, warn about the rebuild before doing it.

**Red flags you're cheating:** "it should work" without a capture; "done" before you've
actually looked at an image; a screenshot taken without navigating to the changed screen.

## Driving verbs

```bash
./bin/mobctl launch --fresh          # always before observe
./bin/mobctl observe                 # compact UI tree: "Type #testID \"label\" =value @cx,cy"
./bin/mobctl observe --shot          # + screenshot (read it to actually "see")
./bin/mobctl tap --id <testID>       # tap by testID (most reliable)
./bin/mobctl tap --text "LABEL"      # tap by text (substring, case-insensitive)
./bin/mobctl type "value" --id <field> --enter
./bin/mobctl swipe up --dist medium  # direction = finger movement
./bin/mobctl scrollto --id <testID>  # scroll until visible
./bin/mobctl deeplink myapp://route  # direct navigation
./bin/mobctl assert --id <testID>    # verify presence (--absent for inverse)
```

Pattern: `launch` → `observe` → act on a `#testID` seen in `observe` → `observe` to verify.
Prefer `observe` (light) over screenshots; screenshot only for visual checks (layout/colors).

## Blocked on a physical gesture — ask, then poll

Some steps need a hardware gesture automation can't do: Face ID / Touch ID, unlocking,
side-button double-click, plugging a cable. Rule: **do 100% of the rest yourself; the human
only does the minimal gesture.** Don't give up at the first block, don't fall back to the
simulator.

1. Bring the UI up to the blocking point.
2. Ask for the exact gesture in one sentence ("rest your finger on the sensor to confirm").
3. Poll every ~30 s to detect it's done (e.g. `mobctl assert --id <target-screen>` or a
   successful `mobctl raw "mobile: launchApp" ...`), then resume automatically.
4. Guardrail: ~10 min of polling max, then stop and ask once more.
