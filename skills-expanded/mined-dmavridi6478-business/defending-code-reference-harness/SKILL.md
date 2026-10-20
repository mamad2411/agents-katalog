# Defending Code Reference Harness

Reference implementation for autonomous vulnerability discovery and remediation with Claude. Covers the full recon → find → verify → dedupe → report → patch pipeline, plus a detection & response (D&R) track for hunting attackers already in logs.

**Source:** `anthropics/defending-code-reference-harness` (public; not maintained, not accepting contributions)
**Local clone:** `/home/user/anthropics/defending-code-reference-harness`
**Blog post:** [Using LLMs to Secure Source Code](https://claude.com/blog/using-llms-to-secure-source-code)
**Managed option:** [Claude Security](https://claude.com/product/claude-security) (hosted product)

---

## Two tracks

| Track | Purpose | Key skills | Autonomous pipeline |
|-------|---------|-----------|-------------------|
| **Vulnerability discovery** | Find and fix bugs before attackers do | `/quickstart`, `/threat-model`, `/vuln-scan`, `/triage`, `/patch`, `/customize` | `bin/vp-sandboxed run` |
| **Detection & response** | Hunt an attacker already in the logs | `/dnr-hunt`, `/dnr-respond` | `bin/vp-sandboxed dnr-pipeline run` |

---

## Built-in Claude Code skills (`.claude/skills/`)

| Skill | What it does | Safe unsandboxed? |
|-------|-------------|-------------------|
| `/quickstart` | 30-sec intro + guided first run on the canary target | yes |
| `/threat-model` | Scope the attack surface before scanning | yes |
| `/vuln-scan` | Static scan scoped by the threat model | yes |
| `/triage` | Verify, dedupe, and rank findings; cross-run aggregation | yes |
| `/patch` | Generate and validate candidate fixes | yes (on static findings) |
| `/customize` | Port the pipeline to your language/detector/vuln class | yes |
| `/dnr-hunt` | Hunt a log corpus for attacker activity (no alert needed) | yes |
| `/dnr-respond` | Verdict + blast radius + response plan from a lead | yes |
| `/verify` | Re-verify a specific finding in isolation | yes |

> ⚠️ The autonomous pipelines (`vuln-pipeline`, `dnr-pipeline`, and `/patch` on pipeline results) **execute target code** — they refuse to run outside a gVisor sandbox unless explicitly overridden.

---

## Setup

```bash
# Interactive skills only (no sandbox needed)
git clone https://github.com/anthropics/defending-code-reference-harness
cd defending-code-reference-harness
export ANTHROPIC_API_KEY=sk-ant-...
claude
> /quickstart
```

```bash
# Autonomous pipeline (requires Docker + gVisor)
python3 -m venv .venv && .venv/bin/pip install -e .
./scripts/setup_sandbox.sh          # installs gVisor, builds agent images, verifies isolation
export ANTHROPIC_API_KEY=sk-ant-...
bin/vp-sandboxed run drlibs --model <model-id> --runs 3 --parallel --stream --auto-focus
```

---

## Recommended ramp-up (5-day plan)

### Day 1 — Static scan end-to-end (no sandbox)

```bash
export CLAUDE_CODE_SUBAGENT_MODEL=<model-id>
claude
> /quickstart
> /threat-model bootstrap targets/canary
> /vuln-scan targets/canary
> /triage targets/canary/VULN-FINDINGS.json
> /patch ./TRIAGE.json --repo targets/canary
```

Produces: `THREAT_MODEL.md`, `VULN-FINDINGS.{json,md}`, `TRIAGE.{json,md}`, `PATCHES/`

### Day 2 — Reference pipeline on a C/C++ library (sandbox required)

```bash
bin/vp-sandboxed run drlibs --model <model-id> --runs 3 --parallel --stream --auto-focus
bin/vp-sandboxed patch results/drlibs/<timestamp>/ --model <model-id>
```

### Days 3–5 — Customize for your target

```bash
claude
> /quickstart how do I customize this for ~/code/my-service?
> /threat-model bootstrap-then-interview ~/code/my-service
> /vuln-scan ~/code/my-service
> /customize use ~/code/my-service/{THREAT_MODEL.md,VULN-FINDINGS.json} and ./TRIAGE.md
bin/vp-sandboxed run my-service --model <model-id> --runs 1   # smoke test
```

### Week 2 — Scale autonomous scanning

```bash
bin/vp-sandboxed run my-service --model <model-id> --runs 5 --parallel --stream --auto-focus
> /triage results/my-service/ --repo ~/code/my-service --auto --votes 5
> /patch results/my-service/<timestamp>/ --model <model-id>
```

---

## Pipeline stages (vuln track)

| Stage | What happens |
|-------|-------------|
| **Build** | Compiles target into Docker image with ASAN |
| **Recon** | Lightweight agent partitions the codebase into N attack surfaces |
| **Find** | N parallel agents craft malformed inputs; each confirms a crash 3/3 |
| **Verify** | Separate grader reproduces each crash in a clean container |
| **Dedupe** | Judge agent compares crashes against known bugs; skips duplicates |
| **Report** | Report agent writes exploitability analysis (primitive, reachability, severity) |
| **Patch** | Patch agent fixes the bug; grader confirms PoC no longer crashes, tests still pass, fresh find agent can't bypass |

---

## Detection & response (Step 5 / optional)

Demo target: `targets/dnrcanary` — a deliberately vulnerable web app with a planted attack campaign in one week of generated logs.

```bash
pip install flask pyyaml
python3 targets/dnrcanary/generate_logs.py --seed 42   # generate logs first

# Interactive
> /dnr-hunt                          # no alert: hunt the corpus
> /dnr-respond INC-1                 # lead in hand: verdict + blast radius + response plan

# Autonomous
bin/vp-sandboxed dnr-pipeline run targets/dnrcanary --model <model-id>

# Self-score against ground truth
python3 targets/dnrcanary/grade.py results/dnrcanary/<ts>/INCIDENTS.json
```

---

## Customization: porting to a new stack

| Question | C/C++ reference | Your target |
|----------|----------------|-------------|
| What signals a finding? | ASAN crash signature | exception / canary file / DNS callback |
| What does a PoC look like? | crashing input file | HTTP request / tx list / test harness |
| How is the target built? | `Dockerfile` (clang + ASAN) | your language's build in a container |

Run `/customize` after pointing the static skills at your codebase. It modifies the harness and creates `targets/<your-service>/`.

---

## Key docs

| Doc | Topic |
|-----|-------|
| `docs/pipeline.md` | Full pipeline diagram and CLI flags |
| `docs/security.md` | Sandboxing, what not to mount |
| `docs/agent-sandbox.md` | gVisor isolation + egress allowlist |
| `docs/best-practices.md` | Verification, severity, iteration, large codebases |
| `docs/prompting.md` | Prompting for defensive security tasks |
| `docs/threat-model.md` | Why a threat model cuts false positives |
| `docs/detection-response.md` | D&R skills and pipeline deep-dive |
| `docs/customizing.md` | Porting guide |
| `docs/patching.md` | Fix generation and validation |
| `docs/other-use-cases.md` | Binary analysis, embedded, bug chains, threat intel |
| `docs/troubleshooting.md` | Duplicates, rate limits, subagent model pinning |

---

## Prompts

### Run the interactive skills on a codebase

```
Open /home/user/anthropics/defending-code-reference-harness in Claude Code.
Run these skills in order on [target path]:
  /threat-model bootstrap [target]
  /vuln-scan [target]
  /triage [target]/VULN-FINDINGS.json
Report: threat model summary, finding count by severity, top 3 findings.
```

### Port the pipeline to a new language

```
Using /home/user/anthropics/defending-code-reference-harness:
Run /customize to port the vuln pipeline to [language/framework].
Input artifacts: [THREAT_MODEL.md, VULN-FINDINGS.json, TRIAGE.md].
Produce: targets/<service>/ ready for a smoke run.
```

### Hunt for attacker activity in logs

```
Using /home/user/anthropics/defending-code-reference-harness:
Generate demo logs: python3 targets/dnrcanary/generate_logs.py --seed 42
Run /dnr-hunt to find the planted campaign.
Then run /dnr-respond on each incident found.
Score results: python3 targets/dnrcanary/grade.py results/dnrcanary/<ts>/INCIDENTS.json
```

### Scale autonomous scanning

```
Using /home/user/anthropics/defending-code-reference-harness:
Run 5 parallel pipeline scans against [target] with --auto-focus.
Cross-run triage with /triage results/[target]/ --auto --votes 5.
Patch the top 3 findings by severity.
Report: total unique bugs, severity distribution, patch validation results.
```
