---
name: plugin-upgrade
description: Migrate a DeepSeek Harness plugin repo across one of the three closed corridors this package carries. A zero-dependency seam scanner reads the target repo's declared band and routes to the matching corridor, then you walk the fix-and-verify loop. Corridor `legAB` (`0.1.3-alpha.1 -> 0.1.5-rc.1`, 20 seams) holds leg A (V3 session format, assistant/message.stream, SessionHandleReadResult, ctx.agent, Inbox, SubprocessHandle.pid, SystemPrompt persona, PTC rename, EpochHeader.system, and the tsconfig stale-path false green) plus leg B (the removed bare `conversation` client slot, the sidebar textpreview -> documentpreview package rename, the stale-type-line false green, the new global main-panel model and usePanelInfo standard prop, the new `present` tool key, two new session event types, and the peer-range trap). Corridor `legC` (`0.1.5-rc.2 -> 0.1.6-alpha.2`, 5 seams `E1`-`E5`) holds the `agent/created` listener-throw chain, the post-`await` apply race, the removed `settings.plugin.item` slot and `SessionListState.current`, the removed `sessions.open/openSubagent/clear` client API, and the removed model literals. Corridor `legD` (`0.1.6-alpha.2 / 0.1.7 -> 0.2.x`, 5 seams `D1`-`D5`) holds the install-time `<0.2.0` peer-band rejection, the deleted settings register/installSection/SettingsScope surface, the deleted invariants package/service/subpath exports, the removed `conversation.session.header.leading` slot, and the workspace-files Remote rename (`readAll`/`readRelated` -> `readBytes`, `changes()` -> `changes(path)`); its advisory section lists the V4 session-format, message-source, composition-row and other seams it deliberately does not scan.
whenToUse: Use when a DSH plugin must reach the DeepSeek Harness 0.2.x line (corridor `legD`, `0.1.6-alpha.2 / 0.1.7 -> 0.2.x`: the measured host is 0.2.2-alpha.2 / guide baseline 0.2.1-alpha.2), the 0.1.6-alpha.2 line (corridor `legC`), or the 0.1.5-rc.1 line (supported entry line: >=0.1.6-alpha.2; pre-0.1.6 lines are not covered), while keeping the older peer band working. The supported entry line is 0.1.6-alpha.2 for the older cards; read leg C. Legs A/B are historical reference for a repo already measured on 0.1.5 and are not a pre-0.1.6 activation promise. A repo on the 0.2 generation reads leg D, whose advisory section names the seams it does not scan. Not for 0.1.1 -> 0.1.2 migrations (use the community convergence skill) and not for the DSH user-facing upgrade/repair path. A hop past every corridor carried here is a new corridor, not a wider card.
metadata:
  corridors: "legAB `0.1.3-alpha.1 -> 0.1.5-rc.1` (leg A S1-S10 + M1 · leg B C1, C2, C4, C5, H1-H4, P1; leg B's C3 is leg A's M1) · legC `0.1.5-rc.2 -> 0.1.6-alpha.2` (E1-E5, all error) · legD `0.1.6-alpha.2 / 0.1.7 -> 0.2.x` (D1-D5, all error; advisory seams are not scanned)"
  host-baseline: "0.1.5-rc.1 (tag dsh-v0.1.5-rc.1 = 183f08e9c6dde7e36cd2318eaee70b0da08fb35e) for legAB; 0.1.6-alpha.2 (tag dsh-v0.1.6-alpha.2) for legC; 0.2.2-alpha.2 (harness checkout ce7073d512; guide baseline d743267 = dsh-v0.2.1-alpha.2) for legD. leg A baseline 0.1.5-alpha.1 (tag dsh-v0.1.5-alpha.1 = 5dda764ed3aa172535a7967b06ff95d9cbfe536a, checkout 19d2e38480)"
  evidence: "leg A: 2026-09-09 wave over 40 plugin repos · leg B: tag-range diff + public slot/service catalogs re-read 2026-09-10; family workspace sweep (15 repos with a client half, 8 slot keys) · leg C: 2026-09-19 sweep, dsh-v0.1.6-alpha.2 · leg D: 2026-11-01 re-read of harness ce7073d512 (0.2.2-alpha.2) + dsh-plugin-guide migration-0.2.md. All recorded in docs/EVIDENCE.md (sections A, 1-11 and 12)"
  status: "published"
  supersedes: "the retired version-locked packages dsh-plugin-upgrade (leg A) and dsh-plugin-upgrade-rc1 (leg B), plus the never-published dsh-plugin-upgrade-016 corridor now folded in as leg C; the two published retired names stay on the registry, deprecated"
user-invocable: true
---

# Plugin upgrade · one package, one corridor index (three closed corridors)

You are migrating **one plugin repository** across one closed DSH corridor. The goal is not "make typecheck pass" — it is "prove the plugin still works on the target host". Local gates are necessary but not sufficient, and two classes of failure survive a green gate: **stale-type false green** (the local gate compiles an old type line) and **silent non-mount** (the host drops a contribution with no error, no log line and no failed build). The corridor index in `lib/route.mjs` picks the card from your declared peer band; each corridor keeps its **own** scanner catalog, so read only the leg you were routed to.

## 1. Locate your leg first

| Your situation | Read |
|---|---|
| Target host is `0.1.5-alpha.1`, or your peer band is below `0.1.5-alpha.1`, or you are bringing a repo up from the `0.1.3-alpha.1` line | **Leg A** — card §1, seams `S1`–`S10` + `M1` |
| Target host is `0.1.5-rc.1`, or the repo has a client/browser half (legacy leg B; the package does not cover pre-0.1.6 activation) | **Leg B** — card §2, seams `C1`, `C2`, `C4`, `C5`, `H1`–`H4`, `P1` |
| A full `0.1.3-alpha.1 → 0.1.5-rc.1` upgrade | both legs, **A first then B**; card §1 then §2 |
| Your peer band is below `0.1.6-alpha.2` | **Not covered by this package.** Fix activation on the older line first; do not stretch leg A/B beyond their measured span. |
| Target is a hop after `0.1.5-rc.1` | **Leg C** — `./references/v0.1.5-rc.2-to-v0.1.6-alpha.2.md`, seams `E1`–`E5` |
| Target is the `0.2.x` generation, or your band declares `0.1.7` | **Leg D** — `./references/v0.1.6-alpha.2-to-v0.2.x.md`, seams `D1`–`D5` + the advisory (not scanned) section |

**One package, one corridor index (owner decision, 2026-09-19).** The earlier rule "a hop after 0.1.5-rc.1 is a new package" is superseded: this package carries a corridor index (`lib/route.mjs`) and the CLI routes to the matching corridor automatically. It reads the target repository's declared dsh band (`engines.dsh`, the `@deepseek-ai/dsh*` ranges) and `--span legAB|legC|legD` overrides the guess; an undeclared band falls back to the older corridor. Each corridor keeps its **own** catalog and evidence — the seam arrays are never merged, so every card claim stays traceable to its measurement.

**Before you pick a corridor, establish which line is newest.** That lookup is yours, not the scanner's: it is read-only, dependency-free and offline by contract. Read the harness's published line (npm `@deepseek-ai/dsh` dist-tags, or the repository's releases/tags), compare it with the target band, and state the target line in your plan. If the newest line is past every corridor here, say so plainly rather than stretching a card.

The card is `./references/v0.1.3-alpha.1-to-v0.1.5-rc.1.md`. It is one document: a preamble with the corridor and how to read it, **§1 = Leg A's full card**, **§2 = Leg B's full card**, **§3 = the merged 20-seam index**. Each leg keeps its own evidence, `path:line` citations, fixtures and rollback path, so one leg can be rolled back without touching the other.

**`C3` no longer exists as a seam.** Leg B's card spelled the stale-type-line false green `C3`; it is the same defect as leg A's `M1` and is folded into it, so `M1` now carries both causes (a stale `0.1.5-alpha.*` dev/test pin and an unresolvable `tsconfig` `paths` alias). The card records the old spelling where it applies. Do not pass `C3` to `--seams`.

### Routing hints carried over from the two legs' frontmatter

Both legs' frontmatter `whenToUse` were routing hints; they cannot both live in one frontmatter, so they are preserved verbatim here — they are still the sharpest statement of each leg's boundary.

- **Leg A** (`0.1.3-alpha.1 → 0.1.5-alpha.1`): historical hint only. This package now supports the measured `>=0.1.6-alpha.2` entry line; pre-0.1.6 activation is outside its scope.
- **Leg B** (`0.1.5-alpha.1 → 0.1.5-rc.1`): "Use when a DSH plugin must support the 0.1.5-rc.1 host line (supported entry line: >=0.1.6-alpha.2; pre-0.1.6 lines are not covered) while keeping the older peer band working, especially when the plugin has a client/browser half. Not for 0.1.3-alpha.1 -> 0.1.5-alpha.1 migrations (use the sibling corridor dsh-plugin-upgrade) and not for the DSH user-facing upgrade/repair path."
  - **Merged-world correction:** the "sibling corridor dsh-plugin-upgrade" that hint points at is now **this same package's Leg A** — read card §1. There is no second package to install.

## 2. Hard rules

1. **Run the scanner first.** `node ./scripts/scan-0.1.5.mjs --repo <repo>` — it prints `file:line` facts. Clear `M1` (stale type line) and `P1` (peer band) before trusting anything else: a fake green and a mis-edited peer range make every later signal meaningless.
2. **`M1` is a blocker, not a warning.** Two independent causes, either one enough: a `tsconfig` `paths` alias that resolves to a missing directory (TypeScript silently falls back to the published types), or dev/test types pinned at `0.1.5-alpha.*` (the local gate compiles the old slot catalog). Fix the paths and the pin, then re-run — new red is real signal.
3. **`P1` is a blocker.** Never collapse the peer range to `>=0.1.2-rc.1 <0.2.0`: under npm semver's prerelease-tuple rule it rejects `0.1.5-rc.1` (measured `false` on semver 7.8.5). rc.1 adaptation does **not** change the peer range.
4. **`C1` is an error, never a warning.** The bare `conversation` client slot was deleted with no alias, and `ctx.slots.inject()` only runs its callback when the declaration exists — the plugin's UI disappears with no error, no log line and no failed build.
5. **On leg D, `D1` is an install blocker, not a warning.** The host compares the runtime version to your declared `engines.dsh` / dsh peer ranges and refuses the install or restart when it does not match (`packages/boot/app-boot/src/plugin-compatibility.ts`). A band that still ends at `<0.2.0` is not "old but working": it cannot be installed on the 0.2.x host at all. Fix `D1` before reading any other legD hit.
6. **Only adapt what the card says changed.** Do not refactor beyond the card, and do not re-litigate the other leg: on leg B the session-format seams (`assistant/message.stream`, `SessionHandleReadResult`, `EpochHeader.system`, `ctx.agent`, `Inbox`, `SystemPrompt.persona`, the V3 log generation) are unchanged in that hop and belong to leg A; on leg A the repo must still boot on `0.1.2-rc.1`, so keep the old peer band working.
7. **A client half needs a browser assertion.** `conversation`'s removal is not detectable at build time. For every `C1` / `C2` / `C5` / `H2` hit, confirm in a real page that the plugin's UI actually appears. A clean scan and a green `typecheck` are **not** evidence.
8. **Behavior change ⇒ test change ⇒ docs change, in one commit.** Five-language READMEs and CHANGELOG move with the code.
9. **Real-host smoke is the exit criterion.** Temp `DSH_HOME` (mkdtemp) + target CLI + `dsh plugin --profile web add <tarball>` + `--dump-config`. Never touch the user's real `~/.dsh`. Leg A adds a **resume round-trip** for anything that writes session logs (`S3`); leg B adds the **real browser assertion** for a client half.

## 3. Loop (both legs)

1. **Identify** — record: repo, current version, peer band, target host tag, node/pnpm, and whether the repo has a client half / tracked `lib/`.
2. **Baseline** — run the repo's own gate chain and *record pre-existing failures*; never let them be counted as migration regressions.
3. **Scan** — run `./scripts/scan-0.1.5.mjs`; load only the version-card facts that hit. **Locate the leg** (§1 above) before planning: a leg-A-only repo must not be planned against leg B's catalog, and vice versa.
4. **Plan** — group by the leg's own axes — leg A: session log / host vocabulary / config / distribution; leg B: client slot / package rename / type line / host vocabulary / config — list files, why they change, tests, rollback point. Get confirmation before editing.
5. **Adapt + verify per module** — fix, run the module's tests, keep commits conventional and independently revertable.
6. **Prove** — full gate chain + real-host smoke + (leg A) the resume round-trip for log writers + (leg B) a real browser assertion for a client half. Report done / not-hit / pre-existing / unverified / rollback, and say **which leg** each finding came from.

## 4. Leg-specific guidance

**Leg A (`0.1.3-alpha.1 → 0.1.5-alpha.1`, seams `S1`–`S10` + `M1`)**

- The four seams no community PR covered are the high-value ones: `S3` (an `assistant/message` written without the V3 required `stream` field), `S8` (`SessionHandle.read()` now returns `{ eventState, events }`), `S9` (`SystemPrompt` `persona` → `personaPrefix` / `personaSuffix`), and `M1`.
- `S3`'s failure shape is worse than a red gate: the log write succeeds and `Session.fromRestore` then refuses to resume the session.
- `S9`: do **not** substitute `includeHarnessIdentity: false` — it deletes the harness identity block, which is not equivalent.
- `S7` / `S1` / `S2` / `S10` are advisory leads for manual review; they have legitimate matches.
- The exit criterion is a temp-`DSH_HOME` smoke plus the `S3` resume round-trip where applicable.

**Leg D (`0.1.6-alpha.2 / 0.1.7 → 0.2.x`, seams `D1`–`D5`)**

- `D1` first: the install-time peer check is the only seam that fails loudly, and a stale `<0.2.0` band means the plugin never loads on a 0.2.x host. Add a 0.2 clause (one per prerelease tuple) before anything else.
- `D2`/`D3` are deletions with no alias: `settings.register`/`installSection`/`SettingsScope` and the whole invariants package/service/subpath surface. `D4`/`D5` are client-side and silent: the old header slot never mounts, and the old Remote methods fail at call time.
- Read the card's **advisory (not scanned)** section before declaring the migration done: V4 session logs, `{kind:'plugin'}` message sources, deleted composition rows, `dsh.client.inject` shape, `stats` → `activity`/`usage`, `mode: 'both'`, and `L1`–`L19` are real 0.2 changes this scanner deliberately does not detect.
- Exit criterion: the install probe on a 0.2.x host, `--dump-config` with no `patch: entry … not found`/`name mismatch`, and a real browser assertion for `D4`/`D5`.

**Leg B (`0.1.5-alpha.1 → 0.1.5-rc.1`, seams `C1`, `C2`, `C4`, `C5`, `H1`–`H4`, `P1`)**

- Rewrite `inject('conversation')` to `main.conversation` (the conversation content seat) or to `main` with your own `key` (a global central panel); card §2 §3.4 has the full recipe. Do **not** "rename to the nearest key" (`conversation.session` and its siblings are different seats).
- `C2` is a package rename with no shim: `@deepseek-ai/dsh-client-ui-sidebar-textpreview` → `…-sidebar-documentpreview`.
- `C4` / `C5` / `H1` / `H2` / `H4` are advisory leads; `H3` is card-only and deliberately has no detector.
- `P1` is about `package.json` peers **only**. `dshWorkshop.compatibility.dshVersions` is a different field: there, replace `0.1.5-alpha.1` with the line you target — do not append.
- Honest sizing: the family's own client halves use 8 slot keys that all survive rc.1, so for them this leg is latent breakage. Third-party halves that targeted the bare `conversation` key are the ones that break, and they break quietly.

## 5. Reference

- `./references/v0.1.3-alpha.1-to-v0.1.5-rc.1.md` — the `legAB` version card: preamble, **§1 Leg A** (10 seams with host path + commit + minimal fix + regression, and the 4 that no community PR covers yet), **§2 Leg B** (the from→to mapping, the `conversation` → `main.conversation` rewrite recipe, the boundary list), **§3 the 20-seam merged index**.
- `./references/v0.1.5-rc.2-to-v0.1.6-alpha.2.md` — the `legC` version card: what breaks across `0.1.5-rc.2 → 0.1.6-alpha.2` (all silent or runtime-only), the five-seam index `E1`–`E5` with evidence and fix/verify recipes, and the family-side facts. `CARD_ONLY = []` there: every `legC` seam has a detector.
- `./references/v0.1.6-alpha.2-to-v0.2.x.md` — the `legD` version card: what breaks across `0.1.6-alpha.2 / 0.1.7 → 0.2.x` (install-time rejection + silent deletions + runtime API renames), the five-seam index `D1`–`D5` with evidence and fix/verify recipes, and an explicit **advisory (not scanned)** section for the V4 session format, `{kind:'plugin'}` message sources, deleted composition rows, `dsh.client.inject` shape, the `stats` → `activity`/`usage` split, `mode: 'both'`, and the guide's `L1`–`L19`. `CARD_ONLY = []`: every catalog seam has a detector; the advisory items are not catalog seams.
- `./scripts/scan-0.1.5.mjs` — the router plus detector: it resolves the corridor through `lib/route.mjs` (declared band, or `--span legAB|legC|legD|span`) and hands the same argv (minus `--span`) to that corridor's own catalog `main()` — `lib/scan.mjs` for `legAB`, `lib/scan-0.1.6.mjs` for `legC`, `lib/scan-0.2.mjs` for `legD`. Zero dependency, `file:line` output, exit `1` on error-severity hits, `--seams` to filter. The file name is historical; it ships inside the skill directory so relative paths resolve.
- The package's own test suite (`node --test`) — synthetic bad/good fixtures **for each corridor** (`fixtures/leg-a-*` for leg A, `fixtures/bad-repo` / `fixtures/good-repo` for leg B, `fixtures/leg-c-*` for leg C, `fixtures/leg-d-*` for leg D), a card↔catalog id-and-severity parity gate **for each corridor**, and a live negative on a family repo.
- `docs/EVIDENCE.md` — the command→output record behind every card claim: §A is leg A's provenance, §1–§10 the leg-B records, §11 the `legC` records.
