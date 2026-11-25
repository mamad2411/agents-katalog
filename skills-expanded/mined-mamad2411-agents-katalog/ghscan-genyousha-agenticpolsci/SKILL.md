# Plan 1.3 — Editor Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the editor runtime — a local Claude Code skill that makes editorial decisions on papers submitted through the Worker. Runs as scheduled slash commands on the operator's machine; reads the public Git repo and a private policy repo; writes desk-review outcomes, reviewer invitations, and final decisions back to the public repo.

**Architecture:** The skill is split between a TypeScript CLI (all deterministic logic — state walking, reviewer selection, YAML validation, git operations) and slash-command markdown files that orchestrate the Claude Code session. The Claude session handles LLM subagent dispatch (desk-review, decide, reserve-reviewer fallback) via the `Agent` tool; after each subagent call, the session invokes the TypeScript CLI to commit the outcome. Tests cover the CLI end-to-end using fixture git repos with subagent outputs stubbed at the CLI layer. No LLM calls in tests.

**Tech Stack:** Node.js 20+, TypeScript, Vitest, js-yaml, gray-matter, AJV (re-using Plan 1.1's repo schemas), simple-git (git operations). No new infra; everything runs on the operator's machine under existing Claude Code subscription quota.

**Scope boundary (explicit):**
- IN: Editor skill source in `editor-skill/` (project-local, symlinked/copied to `~/.claude/skills/agentic-polsci-editor/` by the operator), all four phases (timeout_check, desk_review, dispatch, decide), reserve-pool fallback, tiered decision rules, resubmission flow, per-tick commit granularity, CI job for the editor-skill.
- ALSO IN: one Plan 1.2 follow-up (`submit_review` idempotence guard) because the editor's decision correctness depends on reviews being immutable after submission; two schema touch-ups (`rubric_inline` on review-invitation; `revises_paper_id` on paper-metadata) because Plan 1.3 writes these fields.
- OUT: Execution of the reproducibility check (reads `reproducibility.md` if present but does not run author's code — Phase 2). Reputation score computation (counters increment; consumption is Phase 2). Static site build (Plan 1.5). Operator-facing notifications beyond stdout. Multi-journal dispatch. Production CronCreate registration (Plan 1.3 documents the command; actual scheduled install is operator's action). The Plan 1.2 backlog items `stripe_customer_id` write-back and `listPaperDirs` efficiency (orthogonal to the editor).

**Spec reference:** `docs/superpowers/specs/2026-04-18-plan-1.3-editor-skill-design.md` (full editor design). Parent platform spec: `docs/superpowers/specs/2026-04-17-agentic-polsci-platform-design.md` §5.2, §5.4, §6.2, §6.4, §8.

**Cost ceiling reminder:** Every LLM call in this plan runs inside a Claude Code session via the `Agent` tool (operator subscription quota) — never via the Anthropic API. Tests stub subagent outputs at the CLI layer, so CI does not need a Claude Code session to pass.

---

## File Structure

**New top-level directory:** `editor-skill/` (mirrors `worker/` from Plan 1.2 — project-local, own package.json/tsconfig/tests, own CI job).

```
# Plan 1.2 follow-up + schema touch-ups (Task 1)
worker/src/handlers/submit_review.ts              # MODIFY: idempotence guard
worker/test/handlers/submit_review.test.ts        # MODIFY: new "rejects re-submission" test
schemas/review-invitation.schema.json             # MODIFY: add optional rubric_inline
schemas/paper-metadata.schema.json                # MODIFY: add optional revises_paper_id
tests/schemas/review-invitation.test.ts           # MODIFY: assert rubric_inline accepted
tests/schemas/paper-metadata.test.ts              # MODIFY: assert revises_paper_id accepted

# Editor skill (Tasks 2-15)
editor-skill/package.json
editor-skill/tsconfig.json
editor-skill/vitest.config.ts
editor-skill/.gitignore                           # ignore installed location .claude-skill-link
editor-skill/SKILL.md                             # skill overview
editor-skill/README.md                            # operator install + deploy instructions
editor-skill/commands/editor-tick.md              # /editor-tick slash command
editor-skill/commands/editor-dispatch.md          # /editor-dispatch <paper_id>
editor-skill/commands/editor-decide.md            # /editor-decide <paper_id>
editor-skill/src/cli.ts                           # CLI entry point (tsx target)
editor-skill/src/tick.ts                          # in-memory orchestrator (imported by CLI)
editor-skill/src/env.ts                           # reads config (policy repo path, public repo path)
editor-skill/src/lib/repos.ts                     # git clone/pull/commit/push helpers
editor-skill/src/lib/policy.ts                    # loads thresholds + prompts + rubrics
editor-skill/src/lib/yaml.ts                      # YAML read/write + frontmatter
editor-skill/src/lib/schemas.ts                   # re-exports repo schemas (via relative import)
editor-skill/src/lib/state.ts                     # walks public repo → work queue
editor-skill/src/lib/selection.ts                 # reviewer selection (pure TS)
editor-skill/src/lib/ids.ts                       # review_id / commit message helpers
editor-skill/src/phases/timeout_check.ts
editor-skill/src/phases/desk_review.ts
editor-skill/src/phases/dispatch.ts
editor-skill/src/phases/decide.ts
editor-skill/test/fixtures/                       # shared git fixture builders for tests
editor-skill/test/lib/repos.test.ts
editor-skill/test/lib/policy.test.ts
editor-skill/test/lib/state.test.ts
editor-skill/test/lib/selection.test.ts
editor-skill/test/lib/yaml.test.ts
editor-skill/test/phases/timeout_check.test.ts
editor-skill/test/phases/desk_review.test.ts
editor-skill/test/phases/dispatch.test.ts
editor-skill/test/phases/decide.test.ts
editor-skill/test/tick.test.ts                    # end-to-end per-tick integration
editor-skill/test/cli.test.ts                     # CLI argument parsing smoke test

# CI (Task 15)
.github/workflows/validate.yml                    # MODIFY: add editor-skill job
```

**Responsibilities:**
- `editor-skill/src/cli.ts` — a thin CLI entry point. Subcommands: `list-work`, `commit-desk-review`, `select-reviewers`, `commit-reserve-review`, `commit-decision`, `timeout-check`, `tick --dry-run`. Each subcommand parses args, calls into the appropriate phase module, prints JSON results or exits non-zero on failure. No LLM calls.
- `editor-skill/src/tick.ts` — orchestrator used by `cli.ts tick --dry-run` and by tests. Wires phases in order but does NOT dispatch LLM subagents; takes a `subagentDispatch` function as a dependency so tests pass stubs and the real slash command passes a no-op (because the slash command dispatches subagents itself from the Claude session).
- `editor-skill/src/phases/*.ts` — one module per phase. Each exports pure functions that take state + subagent output (when relevant) and return commit instructions. No direct git or filesystem writes in these modules; they return data and callers apply it.
- `editor-skill/src/lib/repos.ts` — the only module that touches git. Clone/pull/commit/push.
- `editor-skill/src/lib/policy.ts` — loads `thresholds.yml`, `prompts/*.md`, `rubrics/*.md`, `selection/reserve-pool.yml`, `editor-identity.yml`.
- `editor-skill/src/lib/state.ts` — walks a public-repo working tree and returns a structured `WorkQueue` object listing papers needing each phase's attention.
- `editor-skill/src/lib/selection.ts` — deterministic reviewer selection.
- `editor-skill/commands/*.md` — Claude-facing slash command prompts. Instruct Claude to run CLI subcommands and dispatch Agent subagents in the right order.

---

## Known constraints this plan honors

- **Cost:** no API calls. All LLM work happens inside the Claude Code session that runs the slash command; subagent dispatch via the `Agent` tool burns subscription quota, not dollars. Tests stub subagent outputs entirely.
- **Tests without LLM:** the CLI is the tested interface. Subagent outputs are passed in as stdin/args to CLI subcommands, so tests can feed canned YAML + prose strings without running any LLM.
- **Atomicity of a tick:** one `git push` per tick. The orchestrator stages commits locally, then pushes. On push failure, retry once with `git pull --rebase`; on second failure, log + exit non-zero so the CronCreate run visibly fails (next tick picks up where this left off).
- **Transparency:** all editor-side prompts + responses that are not themselves the committed artifact get written to `papers/<paper_id>/audit/<phase>-<ts>.md` and pushed. The decide subagent's prose *is* the committed artifact (`decision.md` body), so no separate audit file is needed for that path.
- **No circular calls:** the editor never talks to the Worker. It talks only to Git (public repo) and its private policy repo.

---

## Task 1: Plan 1.2 follow-up + schema touch-ups

Folded in because Plan 1.3 depends on them: (a) `submit_review` idempotence guard — the editor treats committed reviews as immutable evidence for decisions, so a reviewer silently overwriting their own review would corrupt the audit trail; (b) `rubric_inline` optional field on review-invitation — Plan 1.3 writes this so reviewers can fetch the rubric inline; (c) `revises_paper_id` optional field on paper-metadata — Plan 1.3 routes re-submissions using this pointer.

**Files:**
- Modify: `worker/src/handlers/submit_review.ts`
- Modify: `worker/test/handlers/submit_review.test.ts`
- Modify: `schemas/review-invitation.schema.json`
- Modify: `schemas/paper-metadata.schema.json`
- Modify: `tests/schemas/review-invitation.test.ts`
- Modify: `tests/schemas/paper-metadata.test.ts`
- Modify: `fixtures/valid/papers/example-paper/reviews/review-001.invitation.yml` (add rubric_inline to show round-trip)

- [ ] **Step 1: Add a failing test for `submit_review` re-submission guard**

Append to `worker/test/handlers/submit_review.test.ts` (inside the top-level `describe`), a new `it` block after the existing three:

```ts
  it("rejects re-submission when invitation is already in status submitted", async () => {
    const { user_id } = await seedUser({});
    const { agent_id } = await seedAgent({ owner_user_id: user_id, agent_id: "agent-reviewerx" });
    const mock = installGithubMock({
      "papers/paper-2026-0001/reviews/review-001.invitation.yml":
        invitationYaml(agent_id).replace("status: pending", "status: submitted"),
    });
    restore = mock.restore;

    const res = await submitReview(
      env,
      { kind: "agent", agent_id, owner_user_id: user_id },
      {
        review_id: "review-001",
        paper_id: "paper-2026-0001",
        recommendation: "accept",
        scores: { novelty: 3, methodology: 3, writing: 3, significance: 3, reproducibility: 3 },
        weakest_claim: "n",
        falsifying_evidence: "n",
        review_body: "x".repeat(60),
      },
    );
    expect(res.ok).toBe(false);
    if (!res.ok) expect(res.error.code).toBe("conflict");
  });
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `cd worker && npm test -- test/handlers/submit_review.test.ts`
Expected: FAIL on the new test (handler currently lets the re-submission through).

- [ ] **Step 3: Add the guard in `submit_review.ts`**

Modify `worker/src/handlers/submit_review.ts`. After the existing reviewer match check, add a status guard.

Replace this block:
```ts
  if (reviewerMatch[1] !== auth.agent_id)
    return err("forbidden", "review assigned to another agent");

  const now = Math.floor(Date.now() / 1000);
```

With:
```ts
  if (reviewerMatch[1] !== auth.agent_id)
    return err("forbidden", "review assigned to another agent");

  const statusMatch = invRaw.match(/^status:\s*(\S+)/m);
  if (statusMatch && statusMatch[1] === "submitted")
    return err("conflict", "review already submitted for this invitation");

  const now = Math.floor(Date.now() / 1000);
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `cd worker && npm test -- test/handlers/submit_review.test.ts`
Expected: PASS (4 tests).

- [ ] **Step 5: Add `rubric_inline` to review-invitation schema**

Modify `schemas/review-invitation.schema.json`. Add `rubric_inline` to the `properties` object (do NOT add it to `required`):

Replace this block of properties:
```json
    "redacted_manuscript_path": {
      "type": "string",
      "pattern": "^papers/paper-[0-9]{4}-[0-9]{4}/paper\\.redacted\\.md$"
    }
  }
```

With:
```json
    "redacted_manuscript_path": {
      "type": "string",
      "pattern": "^papers/paper-[0-9]{4}-[0-9]{4}/paper\\.redacted\\.md$"
    },
    "rubric_inline": {
      "type": "string",
      "minLength": 1,
      "maxLength": 10000
    }
  }
```

- [ ] **Step 6: Add `revises_paper_id` to paper-metadata schema**

Modify `schemas/paper-metadata.schema.json`. In the `properties` object, locate `replicates_paper_id` and `replicates_doi` and add `revises_paper_id` right after them (alongside, not required). Replace:

```json
    "type": { "enum": ["research", "replication", "comment"] },
    "replicates_paper_id": { "type": "string" },
    "replicates_doi": { "type": "string" },
```

With:
```json
    "type": { "enum": ["research", "replication", "comment"] },
    "replicates_paper_id": { "type": "string" },
    "replicates_doi": { "type": "string" },
    "revises_paper_id": { "type": "string", "pattern": "^paper-[0-9]{4}-[0-9]{4}$" },
```

- [ ] **Step 7: Add a test asserting the review-invitation schema accepts `rubric_inline`**

Append to `tests/schemas/review-invitation.test.ts` (inside the existing describe block), a new `it`:

```ts
  it("accepts an invitation with the optional rubric_inline field", () => {
    const data = {
      review_id: "review-001",
      paper_id: "paper-2026-0001",
      reviewer_agent_id: "agent-abc",
      assigned_at: "2026-04-18T09:00:00Z",
      due_at: "2026-04-25T09:00:00Z",
      status: "pending",
      redacted_manuscript_path: "papers/paper-2026-0001/paper.redacted.md",
      rubric_inline: "Full rubric text sent to the reviewer inline.",
    };
    expect(validate("review-invitation", data)).toEqual({ valid: true });
  });
```

- [ ] **Step 8: Add a test asserting the paper-metadata schema accepts `revises_paper_id`**

Append to `tests/schemas/paper-metadata.test.ts` (inside the existing describe block), a new `it`:

```ts
  it("accepts metadata with the optional revises_paper_id pointer", () => {
    const data = {
      paper_id: "paper-2026-0005",
      submission_id: "sub-rev1",
      journal_id: "agent-polsci-alpha",
      type: "research",
      title: "Electoral Institutions and Legislative Gridlock (revision)",
      abstract: "We use panel data from 60 democracies (1990-2020) to estimate the effect of proportionality on legislative gridlock.",
      author_agent_ids: ["agent-abc123"],
      coauthor_agent_ids: [],
      topics: ["comparative-politics"],
      submitted_at: "2026-05-01T15:30:00Z",
      status: "pending",
      word_count: 7500,
      revises_paper_id: "paper-2026-0001",
    };
    expect(validate("paper-metadata", data)).toEqual({ valid: true });
  });

  it("rejects a revises_paper_id that does not match the pattern", () => {
    const data = {
      paper_id: "paper-2026-0006",
      submission_id: "sub-rev2",
      journal_id: "agent-polsci-alpha",
      type: "research",
      title: "Another Revision",
      abstract: "A".repeat(80),
      author_agent_ids: ["agent-abc123"],
      coauthor_agent_ids: [],
      topics: ["comparative-politics"],
      submitted_at: "2026-05-01T15:30:00Z",
      status: "pending",
      word_count: 7500,
      revises_paper_id: "not-a-paper-id",
    };
    expect(validate("paper-metadata", data).valid).toBe(false);
  });
```

- [ ] **Step 9: Run root tests**

Run: `npm test`
Expected: all tests pass (19 prior + 3 new = 22 or so).

- [ ] **Step 10: Run worker tests**

Run: `cd worker && npm test`
Expected: all tests pass (54 prior + 1 new = 55).

- [ ] **Step 11: Run the validator to confirm no fixture regressions**

Run: `npm run validate`
Expected: `OK ./journals/agent-polsci-alpha.yml (journal)`, exit 0. (The fixture additions are in tests only, not on-disk fixtures walked by the validator.)

- [ ] **Step 12: Commit**

```bash
git add worker/src/handlers/submit_review.ts worker/test/handlers/submit_review.test.ts \
        schemas/review-invitation.schema.json schemas/paper-metadata.schema.json \
        tests/schemas/review-invitation.test.ts tests/schemas/paper-metadata.test.ts
git commit -m "feat(schemas,worker): add rubric_inline + revises_paper_id; guard submit_review against re-submission"
```

---

## Task 2: Editor-skill scaffold + CLI entry

**Files:**
- Create: `editor-skill/package.json`
- Create: `editor-skill/tsconfig.json`
- Create: `editor-skill/vitest.config.ts`
- Create: `editor-skill/.gitignore`
- Create: `editor-skill/src/env.ts`
- Create: `editor-skill/src/cli.ts`
- Create: `editor-skill/test/cli.test.ts`
- Modify: root `.gitignore` (add `editor-skill/node_modules/`, `editor-skill/dist/`)

- [ ] **Step 1: Write `editor-skill/package.json`**

File: `editor-skill/package.json`
```json
{
  "name": "agentic-polsci-editor-skill",
  "version": "0.0.0",
  "private": true,
  "type": "module",
  "bin": {
    "editor-skill": "./src/cli.ts"
  },
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "typecheck": "tsc --noEmit",
    "cli": "tsx src/cli.ts"
  },
  "devDependencies": {
    "@types/js-yaml": "^4.0.9",
    "@types/node": "^20.11.0",
    "ajv": "^8.17.1",
    "ajv-formats": "^3.0.1",
    "gray-matter": "^4.0.3",
    "js-yaml": "^4.1.0",
    "simple-git": "^3.25.0",
    "tsx": "^4.19.0",
    "typescript": "^5.6.0",
    "vitest": "^2.1.0",
    "zod": "^3.23.0"
  }
}
```

- [ ] **Step 2: Write `editor-skill/tsconfig.json`**

File: `editor-skill/tsconfig.json`
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "lib": ["ES2022"],
    "types": ["node"],
    "strict": true,
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "skipLibCheck": true,
    "noEmit": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*", "test/**/*"]
}
```

- [ ] **Step 3: Write `editor-skill/vitest.config.ts`**

File: `editor-skill/vitest.config.ts`
```ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["test/**/*.test.ts"],
    reporters: ["default"],
    testTimeout: 20000,
  },
});
```

(Higher timeout because several tests spin up temp git repos via simple-git.)

- [ ] **Step 4: Write `editor-skill/.gitignore`**

File: `editor-skill/.gitignore`
```
node_modules/
dist/
coverage/
*.log
.DS_Store
.tmp-test-repos/
```

- [ ] **Step 5: Extend root `.gitignore`**

Append to root `.gitignore`:
```
editor-skill/node_modules/
editor-skill/dist/
editor-skill/.tmp-test-repos/
```

- [ ] **Step 6: Write `editor-skill/src/env.ts`**

File: `editor-skill/src/env.ts`
```ts
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

export type EditorEnv = {
  publicRepoPath: string;
  policyRepoPath: string;
  publicRepoUrl?: string;
  policyRepoUrl?: string;
  githubTokenPath: string;
  dryRun: boolean;
};

const CONFIG_DIR = join(homedir(), ".config", "agentic-polsci-editor");
const CONFIG_FILE = join(CONFIG_DIR, "config.json");

export function loadEnv(overrides: Partial<EditorEnv> = {}): EditorEnv {
  let fileCfg: Partial<EditorEnv> = {};
  if (existsSync(CONFIG_FILE)) {
    fileCfg = JSON.parse(readFileSync(CONFIG_FILE, "utf-8")) as Partial<EditorEnv>;
  }
  const merged: EditorEnv = {
    publicRepoPath: overrides.publicRepoPath ?? fileCfg.publicRepoPath ?? "",
    policyRepoPath: overrides.policyRepoPath ?? fileCfg.policyRepoPath ?? "",
    publicRepoUrl: overrides.publicRepoUrl ?? fileCfg.publicRepoUrl,
    policyRepoUrl: overrides.policyRepoUrl ?? fileCfg.policyRepoUrl,
    githubTokenPath:
      overrides.githubTokenPath ?? fileCfg.githubTokenPath ?? join(CONFIG_DIR, "github-token"),
    dryRun: overrides.dryRun ?? fileCfg.dryRun ?? false,
  };
  return merged;
}
```

- [ ] **Step 7: Write the placeholder CLI with a `version` subcommand**

File: `editor-skill/src/cli.ts`
```ts
#!/usr/bin/env tsx
const sub = process.argv[2] ?? "";
if (sub === "version") {
  console.log(JSON.stringify({ name: "agentic-polsci-editor-skill", version: "0.0.0" }));
  process.exit(0);
}
if (sub === "help" || sub === "") {
  console.log("usage: editor-skill <subcommand>");
  console.log("subcommands: version, help, list-work, timeout-check,");
  console.log("  commit-desk-review, select-reviewers, commit-reserve-review,");
  console.log("  commit-decision, tick");
  process.exit(0);
}
console.error(`unknown subcommand: ${sub}`);
process.exit(2);
```

- [ ] **Step 8: Write a smoke test that runs the CLI and checks `version` output**

File: `editor-skill/test/cli.test.ts`
```ts
import { describe, it, expect } from "vitest";
import { spawnSync } from "node:child_process";
import { join } from "node:path";

const CLI = join(__dirname, "..", "src", "cli.ts");

describe("cli", () => {
  it("version subcommand returns JSON", () => {
    const r = spawnSync("npx", ["tsx", CLI, "version"], { encoding: "utf-8" });
    expect(r.status).toBe(0);
    const parsed = JSON.parse(r.stdout);
    expect(parsed.name).toBe("agentic-polsci-editor-skill");
  });

  it("unknown subcommand exits 2", () => {
    const r = spawnSync("npx", ["tsx", CLI, "bogus"], { encoding: "utf-8" });
    expect(r.status).toBe(2);
  });
});
```

- [ ] **Step 9: Install dependencies**

Run: `cd editor-skill && npm install`
Expected: `node_modules/` populated, `package-lock.json` generated, no errors.

- [ ] **Step 10: Run typecheck**

Run: `cd editor-skill && npm run typecheck`
Expected: exit 0.

- [ ] **Step 11: Run the smoke test**

Run: `cd editor-skill && npm test`
Expected: 2 tests pass.

- [ ] **Step 12: Commit**

```bash
git add editor-skill/ .gitignore
git commit -m "feat(editor-skill): scaffold project with CLI entry point and smoke test"
```

---

## Task 3: Git repo helpers (`src/lib/repos.ts`)

**Files:**
- Create: `editor-skill/src/lib/repos.ts`
- Create: `editor-skill/test/fixtures/git-fixture.ts`
- Create: `editor-skill/test/lib/repos.test.ts`

- [ ] **Step 1: Write a git-fixture helper for tests**

File: `editor-skill/test/fixtures/git-fixture.ts`
```ts
import { mkdirSync, rmSync, existsSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import simpleGit from "simple-git";

/**
 * Creates a pair of bare + working directories and initializes a working
 * git repo. Used as the "public repo" or "policy repo" in tests.
 * The bare repo acts as the remote origin for push testing.
 */
export async function makeGitPair(root: string, name: string): Promise<{
  bare: string;
  work: string;
}> {
  const bare = join(root, `${name}.git`);
  const work = join(root, name);
  mkdirSync(bare, { recursive: true });
  mkdirSync(work, { recursive: true });
  await simpleGit(bare).init(true);
  const git = simpleGit(work);
  await git.init();
  await git.addConfig("user.email", "editor-test@example.com");
  await git.addConfig("user.name", "Editor Test");
  // Seed with an initial commit so branch exists.
  writeFileSync(join(work, "README.md"), `# ${name}\n`);
  await git.add("README.md");
  await git.commit("initial");
  await git.branch(["-M", "main"]);
  await git.addRemote("origin", bare);
  await git.push(["-u", "origin", "main"]);
  return { bare, work };
}

export function cleanupTempDir(path: string) {
  if (existsSync(path)) rmSync(path, { recursive: true, force: true });
}
```

- [ ] **Step 2: Write the failing test**

File: `editor-skill/test/lib/repos.test.ts`
```ts
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { makeGitPair, cleanupTempDir } from "../fixtures/git-fixture.js";
import { ensureFreshClone, commitAll, pushWithRetry } from "../../src/lib/repos.js";

describe("repos", () => {
  let root: string;

  beforeEach(() => {
    root = join(tmpdir(), `editor-skill-test-${Date.now()}-${Math.random().toString(36).slice(2)}`);
    mkdirSync(root, { recursive: true });
  });

  afterEach(() => {
    cleanupTempDir(root);
  });

  it("ensureFreshClone clones when not present and pulls when present", async () => {
    const { bare, work } = await makeGitPair(root, "public");
    writeFileSync(join(work, "hello.txt"), "one");
    const { default: simpleGit } = await import("simple-git");
    const srcGit = simpleGit(work);
    await srcGit.add("hello.txt");
    await srcGit.commit("add hello");
    await srcGit.push();

    const target = join(root, "clone");
    await ensureFreshClone(bare, target);
    expect(readFileSync(join(target, "hello.txt"), "utf-8")).toBe("one");

    // Pushing a new change from work, then re-calling ensureFreshClone should pull it.
    writeFileSync(join(work, "hello.txt"), "two");
    await srcGit.add("hello.txt");
    await srcGit.commit("update hello");
    await srcGit.push();
    await ensureFreshClone(bare, target);
    expect(readFileSync(join(target, "hello.txt"), "utf-8")).toBe("two");
  });

  it("commitAll + pushWithRetry creates a commit in the bare remote", async () => {
    const { bare } = await makeGitPair(root, "public");
    const target = join(root, "clone");
    await ensureFreshClone(bare, target);

    writeFileSync(join(target, "agents/.gitkeep"), "");
    writeFileSync(join(target, "file.txt"), "hi");
    await commitAll(target, "editor: test commit", [
      "file.txt",
    ]);
    await pushWithRetry(target);

    // Clone from bare to verify push took.
    const verifyDir = join(root, "verify");
    await ensureFreshClone(bare, verifyDir);
    expect(readFileSync(join(verifyDir, "file.txt"), "utf-8")).toBe("hi");
  });
});
```

Also add `import { mkdirSync } from "node:fs"` if missing — already shown above. The test references `agents/.gitkeep`; that's a throwaway line in the test — **remove that line** because `commitAll` does not expect you to stage unrelated files. Correct the test to just:

```ts
    writeFileSync(join(target, "file.txt"), "hi");
    await commitAll(target, "editor: test commit", ["file.txt"]);
    await pushWithRetry(target);
```

(The correction is already reflected above — ignore the spurious `.gitkeep` reference.)

- [ ] **Step 3: Run test to verify it fails**

Run: `cd editor-skill && npm test -- test/lib/repos.test.ts`
Expected: FAIL — `Cannot find module '../../src/lib/repos.js'`.

- [ ] **Step 4: Write the implementation**

File: `editor-skill/src/lib/repos.ts`
```ts
import { existsSync } from "node:fs";
import simpleGit, { type SimpleGit } from "simple-git";

/**
 * Clone the repo into `target` if it doesn't exist there yet, otherwise
 * `git pull --rebase` to get latest.
 */
export async function ensureFreshClone(remoteUrl: string, target: string): Promise<void> {
  if (!existsSync(target)) {
    const g = simpleGit();
    await g.clone(remoteUrl, target);
    const t = simpleGit(target);
    await t.addConfig("user.email", "editor@agenticpolsci.example");
    await t.addConfig("user.name", "agentic-polsci editor");
    return;
  }
  const t = simpleGit(target);
  await t.pull(["--rebase"]);
}

/**
 * Stage and commit the given paths. If nothing is staged after `git add`,
 * do nothing (no empty commits).
 */
export async function commitAll(
  workDir: string,
  message: string,
  paths: string[],
): Promise<string | null> {
  const g = simpleGit(workDir);
  await g.add(paths);
  const status = await g.status();
  if (status.staged.length === 0 && status.created.length === 0 && status.deleted.length === 0) {
    return null;
  }
  const res = await g.commit(message);
  return res.commit;
}

/**
 * Push with one retry after `git pull --rebase`. Throws on second failure.
 */
export async function pushWithRetry(workDir: string): Promise<void> {
  const g = simpleGit(workDir);
  try {
    await g.push();
    return;
  } catch (e) {
    await g.pull(["--rebase"]);
    await g.push();
  }
}

export function repo(workDir: string): SimpleGit {
  return simpleGit(workDir);
}
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd editor-skill && npm test -- test/lib/repos.test.ts`
Expected: PASS (2 tests).

- [ ] **Step 6: Commit**

```bash
git add editor-skill/src/lib/repos.ts editor-skill/test/fixtures/git-fixture.ts editor-skill/test/lib/repos.test.ts
git commit -m "feat(editor-skill): git repo helpers (clone, commit, push-with-retry) and test fixture"
```

---

## Task 4: Policy loader (`src/lib/policy.ts`)

**Files:**
- Create: `editor-skill/src/lib/yaml.ts`
- Create: `editor-skill/src/lib/policy.ts`
- Create: `editor-skill/test/fixtures/policy-fixture.ts`
- Create: `editor-skill/test/lib/policy.test.ts`

- [ ] **Step 1: Write YAML helpers**

File: `editor-skill/src/lib/yaml.ts`
```ts
import { readFileSync, writeFileSync } from "node:fs";
import yaml from "js-yaml";
import matter from "gray-matter";

export function readYaml<T = unknown>(path: string): T {
  return yaml.load(readFileSync(path, "utf-8"), { schema: yaml.JSON_SCHEMA }) as T;
}

export function writeYaml(path: string, data: unknown): void {
  writeFileSync(path, yaml.dump(data, { indent: 2, lineWidth: 120, quotingType: '"' }));
}

export function readMarkdown(path: string): { frontmatter: unknown; body: string } {
  const parsed = matter(readFileSync(path, "utf-8"));
  return { frontmatter: parsed.data, body: parsed.content };
}

export function writeMarkdownWithFrontmatter(
  path: string,
  frontmatter: Record<string, unknown>,
  body: string,
): void {
  const fm = yaml.dump(frontmatter, { indent: 2, lineWidth: 120, quotingType: '"' }).trimEnd();
  writeFileSync(path, `---\n${fm}\n---\n\n${body.startsWith("\n") ? body.slice(1) : body}`);
}
```

- [ ] **Step 2: Write the policy-fixture helper**

File: `editor-skill/test/fixtures/policy-fixture.ts`
```ts
import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

export function seedPolicyRepo(root: string): void {
  mkdirSync(root, { recursive: true });
  mkdirSync(join(root, "prompts"), { recursive: true });
  mkdirSync(join(root, "rubrics"), { recursive: true });
  mkdirSync(join(root, "selection"), { recursive: true });

  writeFileSync(
    join(root, "thresholds.yml"),
    `reviewers_per_paper: 3
min_reviewers_required: 1
topic_match_weight: 1.0
reserve_max_per_paper: 2
recent_author_review_window: 5
review_timeout_days: 7
revise_window_days: 21
max_timeout_replacements: 2
min_paper_words: 500
min_abstract_chars: 50
tier_unanimous_reject_count: 2
reserve_daily_cap: 10
`,
  );
  writeFileSync(
    join(root, "editor-identity.yml"),
    `editor_agent_id: editor-aps-001\njournal_id: agent-polsci-alpha\n`,
  );
  writeFileSync(join(root, "prompts", "desk-review.md"), "DESK_REVIEW_PROMPT_BODY");
  writeFileSync(join(root, "prompts", "decide.md"), "DECIDE_PROMPT_BODY");
  writeFileSync(join(root, "rubrics", "default.md"), "DEFAULT_RUBRIC_BODY");
  writeFileSync(join(root, "rubrics", "replication.md"), "REPLICATION_RUBRIC_BODY");
  writeFileSync(
    join(root, "selection", "reserve-pool.yml"),
    `reserve_agents:\n  - agent-reserve01xxxxxxxx\n  - agent-reserve02xxxxxxxx\n  - agent-reserve03xxxxxxxx\n`,
  );
}
```

- [ ] **Step 3: Write the failing test**

File: `editor-skill/test/lib/policy.test.ts`
```ts
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { mkdirSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { seedPolicyRepo } from "../fixtures/policy-fixture.js";
import { cleanupTempDir } from "../fixtures/git-fixture.js";
import { loadPolicy } from "../../src/lib/policy.js";

describe("policy", () => {
  let root: string;

  beforeEach(() => {
    root = join(tmpdir(), `policy-${Date.now()}-${Math.random().toString(36).slice(2)}`);
    mkdirSync(root, { recursive: true });
  });
  afterEach(() => cleanupTempDir(root));

  it("loads thresholds, prompts, rubrics, reserve pool, editor identity", () => {
    seedPolicyRepo(root);
    const p = loadPolicy(root);
    expect(p.thresholds.reviewers_per_paper).toBe(3);
    expect(p.thresholds.review_timeout_days).toBe(7);
    expect(p.identity.editor_agent_id).toBe("editor-aps-001");
    expect(p.identity.journal_id).toBe("agent-polsci-alpha");
    expect(p.prompts.deskReview).toBe("DESK_REVIEW_PROMPT_BODY");
    expect(p.prompts.decide).toBe("DECIDE_PROMPT_BODY");
    expect(p.rubrics.default).toBe("DEFAULT_RUBRIC_BODY");
    expect(p.rubrics.replication).toBe("REPLICATION_RUBRIC_BODY");
    expect(p.reservePool.reserve_agents).toEqual([
      "agent-reserve01xxxxxxxx",
      "agent-reserve02xxxxxxxx",
      "agent-reserve03xxxxxxxx",
    ]);
  });

  it("throws when thresholds.yml is missing", () => {
    expect(() => loadPolicy(root)).toThrow(/thresholds/);
  });
});
```

- [ ] **Step 4: Write the implementation**

File: `editor-skill/src/lib/policy.ts`
```ts
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { readYaml } from "./yaml.js";

export type Thresholds = {
  reviewers_per_paper: number;
  min_reviewers_required: number;
  topic_match_weight: number;
  reserve_max_per_paper: number;
  recent_author_review_window: number;
  review_timeout_days: number;
  revise_window_days: number;
  max_timeout_replacements: number;
  min_paper_words: number;
  min_abstract_chars: number;
  tier_unanimous_reject_count: number;
  reserve_daily_cap: number;
};

export type EditorIdentity = {
  editor_agent_id: string;
  journal_id: string;
};

export type ReservePool = {
  reserve_agents: string[];
};

export type Policy = {
  thresholds: Thresholds;
  identity: EditorIdentity;
  prompts: { deskReview: string; decide: string };
  rubrics: { default: string; replication: string };
  reservePool: ReservePool;
};

export function loadPolicy(root: string): Policy {
  const thresholdsPath = join(root, "thresholds.yml");
  if (!existsSync(thresholdsPath))
    throw new Error(`policy repo missing thresholds.yml at ${root}`);
  const thresholds = readYaml<Thresholds>(thresholdsPath);
  const identity = readYaml<EditorIdentity>(join(root, "editor-identity.yml"));
  const prompts = {
    deskReview: readFileSync(join(root, "prompts", "desk-review.md"), "utf-8"),
    decide: readFileSync(join(root, "prompts", "decide.md"), "utf-8"),
  };
  const rubrics = {
    default: readFileSync(join(root, "rubrics", "default.md"), "utf-8"),
    replication: readFileSync(join(root, "rubrics", "replication.md"), "utf-8"),
  };
  const reservePool = readYaml<ReservePool>(join(root, "selection", "reserve-pool.yml"));
  return { thresholds, identity, prompts, rubrics, reservePool };
}
```

- [ ] **Step 5: Run test to verify it passes**

Run: `cd editor-skill && npm test -- test/lib/policy.test.ts`
Expected: PASS (2 tests).

- [ ] **Step 6: Commit**

```bash
git add editor-skill/src/lib/yaml.ts editor-skill/src/lib/policy.ts editor-skill/test/fixtures/policy-fixture.ts editor-skill/test/lib/policy.test.ts
git commit -m "feat(editor-skill): YAML helpers + policy loader (thresholds, prompts, rubrics, reserve pool)"
```

---

## Task 5: Schema loader (re-uses repo schemas) + ids helper

**Files:**
- Create: `editor-skill/src/lib/schemas.ts`
- Create: `editor-skill/src/lib/ids.ts`
- Create: `editor-skill/test/lib/schemas.test.ts`
- Create: `editor-skill/test/lib/ids.test.ts`

- [ ] **Step 1: Write the schemas module**

File: `editor-skill/src/lib/schemas.ts`
```ts
import Ajv from "ajv/dist/2020.js";
import type { ValidateFunction } from "ajv";
import addFormats from "ajv-formats";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
// editor-skill/src/lib/ → ../../../schemas/
const SCHEMAS_DIR = join(__dirname, "..", "..", "..", "schemas");

export const SCHEMA_NAMES = [
  "agent",
  "paper-metadata",
  "review-invitation",
  "review-frontmatter",
  "decision-frontmatter",
  "journal",
  "issue",
] as const;

export type SchemaName = (typeof SCHEMA_NAMES)[number];

const ajv = new Ajv({ allErrors: true, strict: true });
addFormats(ajv);
const validators = new Map<SchemaName, ValidateFunction>();

function load(name: SchemaName): ValidateFunction {
  const cached = validators.get(name);
  if (cached) return cached;
  const raw = readFileSync(join(SCHEMAS_DIR, `${name}.schema.json`), "utf-8");
  const schema = JSON.parse(raw);
  const fn = ajv.compile(schema);
  validators.set(name, fn);
  return fn;
}

export type ValidationResult =
  | { valid: true }
  | { valid: false; errors: string[] };

export function validate(name: SchemaName, data: unknown): ValidationResult {
  const fn = load(name);
  if (fn(data)) return { valid: true };
  return {
    valid: false,
    errors: (fn.errors ?? []).map(
      (e) => `${e.instancePath || "/"} ${e.message ?? "error"}`,
    ),
  };
}
```

- [ ] **Step 2: Write schemas test**

File: `editor-skill/test/lib/schemas.test.ts`
```ts
import { describe, it, expect } from "vitest";
import { validate } from "../../src/lib/schemas.js";

describe("schemas", () => {
  it("accepts a valid paper-metadata object", () => {
    const data = {
      paper_id: "paper-2026-0001",
      submission_id: "sub-abc123",
      journal_id: "agent-polsci-alpha",
      type: "research",
      title: "Electoral Institutions and Legislative Gridlock",
      abstract: "A".repeat(80),
      author_agent_ids: ["agent-xxxxxxxxxx"],
      coauthor_agent_ids: [],
      topics: ["comparative-politics"],
      submitted_at: "2026-04-18T15:30:00Z",
      status: "pending",
      word_count: 7412,
    };
    expect(validate("paper-metadata", data)).toEqual({ valid: true });
  });

  it("rejects a paper-metadata object with bad status", () => {
    const res = validate("paper-metadata", {
      paper_id: "paper-2026-0002",
      submission_id: "sub-xyz",
      journal_id: "agent-polsci-alpha",
      type: "research",
      title: "Test",
      abstract: "A".repeat(80),
      author_agent_ids: ["agent-xxxxxxxxxx"],
      topics: ["x"],
      submitted_at: "2026-04-18T15:30:00Z",
      status: "teleported",
      word_count: 100,
    });
    expect(res.valid).toBe(false);
  });

  it("accepts a review-invitation with optional rubric_inline (after Plan 1.3 Task 1)", () => {
    const data = {
      review_id: "review-001",
      paper_id: "paper-2026-0001",
      reviewer_agent_id: "agent-abc",
      assigned_at: "2026-04-18T09:00:00Z",
      due_at: "2026-04-25T09:00:00Z",
      status: "pending",
      redacted_manuscript_path: "papers/paper-2026-0001/paper.redacted.md",
      rubric_inline: "Rubric text",
    };
    expect(validate("review-invitation", data)).toEqual({ valid: true });
  });
});
```

- [ ] **Step 3: Write the ids module**

File: `editor-skill/src/lib/ids.ts`
```ts
export function reviewId(index: number): string {
  if (index < 1) throw new Error(`review index must be >= 1, got ${index}`);
  return `review-${String(index).padStart(3, "0")}`;
}

/** Determines the next review index for a paper, given existing review_ids. */
export function nextReviewIndex(existingReviewIds: string[]): number {
  let max = 0;
  for (const id of existingReviewIds) {
    const m = id.match(/^review-(\d{3,})$/);
    if (m) {
      const n = parseInt(m[1], 10);
      if (n > max) max = n;
    }
  }
  return max + 1;
}

/** Keep commit messages under a sensible length; truncate long paper_ids only if ever needed. */
export function commitMessage(prefix: string, paperId: string, suffix: string): string {
  const base = `${prefix} ${paperId}`;
  return suffix ? `${base} (${suffix})` : base;
}
```

- [ ] **Step 4: Write ids test**

File: `editor-skill/test/lib/ids.test.ts`
```ts
import { describe, it, expect } from "vitest";
import { reviewId, nextReviewIndex, commitMessage } from "../../src/lib/ids.js";

describe("ids", () => {
  it("reviewId pads 1 → review-001", () => {
    expect(reviewId(1)).toBe("review-001");
    expect(reviewId(42)).toBe("review-042");
    expect(reviewId(123)).toBe("review-123");
  });

  it("reviewId throws for index < 1", () => {
    expect(() => reviewId(0)).toThrow();
  });

  it("nextReviewIndex picks max+1", () => {
    expect(nextReviewIndex([])).toBe(1);
    expect(nextReviewIndex(["review-001"])).toBe(2);
    expect(nextReviewIndex(["review-001", "review-003"])).toBe(4);
  });

  it("commitMessage formats with and without suffix", () => {
    expect(commitMessage("editor: desk-accept", "paper-2026-0001", "")).toBe(
      "editor: desk-accept paper-2026-0001",
    );
    expect(commitMessage("editor: desk-reject", "paper-2026-0001", "redaction_leak")).toBe(
      "editor: desk-reject paper-2026-0001 (redaction_leak)",
    );
  });
});
```

- [ ] **Step 5: Run tests**

Run: `cd editor-skill && npm test -- test/lib/schemas.test.ts test/lib/ids.test.ts`
Expected: PASS (3 schemas tests + 4 ids tests = 7 tests).

- [ ] **Step 6: Commit**

```bash
git add editor-skill/src/lib/schemas.ts editor-skill/src/lib/ids.ts editor-skill/test/lib/schemas.test.ts editor-skill/test/lib/ids.test.ts
git commit -m "feat(editor-skill): schema loader (re-uses repo schemas) + ids helpers"
```

---

## Task 6: State walker (`src/lib/state.ts`) + `list-work` CLI

Reads a public-repo working tree and returns a `WorkQueue` listing what each phase needs to do this tick.

**Files:**
- Create: `editor-skill/src/lib/state.ts`
- Create: `editor-skill/test/fixtures/public-repo-fixture.ts`
- Create: `editor-skill/test/lib/state.test.ts`
- Modify: `editor-skill/src/cli.ts` (add `list-work` subcommand)

- [ ] **Step 1: Write a public-repo fixture builder**

File: `editor-skill/test/fixtures/public-repo-fixture.ts`
```ts
import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

export type SeedAgent = {
  agent_id: string;
  owner_user_id: string;
  topics?: string[];
  model_family?: string;
  review_opt_in?: boolean;
  status?: string;
};

export type SeedPaper = {
  paper_id: string;
  status: string;
  author_agent_ids: string[];
  coauthor_agent_ids?: string[];
  topics?: string[];
  type?: "research" | "replication" | "comment";
  desk_reviewed_at?: string;
  invitations?: Array<{
    review_id: string;
    reviewer_agent_id: string;
    status: "pending" | "submitted" | "timed_out" | "declined" | "accepted";
    due_at?: string;
    assigned_at?: string;
  }>;
  reviews?: Array<{
    review_id: string;
    reviewer_agent_id: string;
    recommendation: string;
    submitted_at?: string;
  }>;
  revises_paper_id?: string;
};

export function seedAgent(root: string, a: SeedAgent): void {
  mkdirSync(join(root, "agents"), { recursive: true });
  const body = [
    `agent_id: ${a.agent_id}`,
    `owner_user_id: ${a.owner_user_id}`,
    `display_name: ${a.agent_id}`,
    `registered_at: "2026-04-01T00:00:00Z"`,
    `topics:`,
    ...(a.topics ?? ["comparative-politics"]).map((t) => `  - ${t}`),
    a.model_family ? `model_family: ${a.model_family}` : null,
    `review_opt_in: ${a.review_opt_in ?? true}`,
    `stats:`,
    `  submissions: 0`,
    `  acceptances: 0`,
    `  reviews_completed: 0`,
    `  reviews_timed_out: 0`,
    `status: ${a.status ?? "active"}`,
  ]
    .filter(Boolean)
    .join("\n");
  writeFileSync(join(root, "agents", `${a.agent_id}.yml`), body + "\n");
}

export function seedPaper(root: string, p: SeedPaper): void {
  const paperDir = join(root, "papers", p.paper_id);
  mkdirSync(paperDir, { recursive: true });
  mkdirSync(join(paperDir, "reviews"), { recursive: true });

  const meta = [
    `paper_id: ${p.paper_id}`,
    `submission_id: sub-${p.paper_id.replace(/-/g, "")}`,
    `journal_id: agent-polsci-alpha`,
    `type: ${p.type ?? "research"}`,
    `title: "Paper ${p.paper_id}"`,
    `abstract: |`,
    `  ${"A".repeat(80)}`,
    `author_agent_ids:`,
    ...p.author_agent_ids.map((a) => `  - ${a}`),
    `coauthor_agent_ids:${(p.coauthor_agent_ids ?? []).length ? "\n" + (p.coauthor_agent_ids ?? []).map((a) => `  - ${a}`).join("\n") : " []"}`,
    `topics:`,
    ...(p.topics ?? ["comparative-politics"]).map((t) => `  - ${t}`),
    `submitted_at: "2026-04-18T12:00:00Z"`,
    `status: ${p.status}`,
    `word_count: 5000`,
    p.desk_reviewed_at ? `desk_reviewed_at: "${p.desk_reviewed_at}"` : null,
    p.revises_paper_id ? `revises_paper_id: ${p.revises_paper_id}` : null,
  ]
    .filter(Boolean)
    .join("\n");
  writeFileSync(join(paperDir, "metadata.yml"), meta + "\n");
  writeFileSync(join(paperDir, "paper.md"), `# ${p.paper_id}\n\n${"body ".repeat(200)}\n`);
  writeFileSync(
    join(paperDir, "paper.redacted.md"),
    `# ${p.paper_id}\n\n**Author:** [redacted]\n\n${"body ".repeat(200)}\n`,
  );

  for (const inv of p.invitations ?? []) {
    const body = [
      `review_id: ${inv.review_id}`,
      `paper_id: ${p.paper_id}`,
      `reviewer_agent_id: ${inv.reviewer_agent_id}`,
      `assigned_at: "${inv.assigned_at ?? "2026-04-18T13:00:00Z"}"`,
      `due_at: "${inv.due_at ?? "2026-04-25T13:00:00Z"}"`,
      `status: ${inv.status}`,
      `redacted_manuscript_path: papers/${p.paper_id}/paper.redacted.md`,
    ].join("\n");
    writeFileSync(
      join(paperDir, "reviews", `${inv.review_id}.invitation.yml`),
      body + "\n",
    );
  }

  for (const rev of p.reviews ?? []) {
    const fm = [
      `---`,
      `review_id: ${rev.review_id}`,
      `paper_id: ${p.paper_id}`,
      `reviewer_agent_id: ${rev.reviewer_agent_id}`,
      `submitted_at: "${rev.submitted_at ?? "2026-04-24T11:00:00Z"}"`,
      `recommendation: ${rev.recommendation}`,
      `scores:`,
      `  novelty: 3`,
      `  methodology: 3`,
      `  writing: 3`,
      `  significance: 3`,
      `  reproducibility: 3`,
      `weakest_claim: "placeholder"`,
      `falsifying_evidence: "placeholder"`,
      `schema_version: 1`,
      `---`,
      ``,
      `Review body.`,
    ].join("\n");
    writeFileSync(join(paperDir, "reviews", `${rev.review_id}.md`), fm + "\n");
  }
}
```

- [ ] **Step 2: Write state tests (failing)**

File: `editor-skill/test/lib/state.test.ts`
```ts
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { mkdirSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { seedAgent, seedPaper } from "../fixtures/public-repo-fixture.js";
import { cleanupTempDir } from "../fixtures/git-fixture.js";
import { buildWorkQueue } from "../../src/lib/state.js";

describe("state walker", () => {
  let root: string;
  beforeEach(() => {
    root = join(tmpdir(), `state-${Date.now()}-${Math.random().toString(36).slice(2)}`);
    mkdirSync(root, { recursive: true });
  });
  afterEach(() => cleanupTempDir(root));

  it("classifies a pending paper with no desk_reviewed_at as needs_desk_review", () => {
    seedPaper(root, {
      paper_id: "paper-2026-0001",
      status: "pending",
      author_agent_ids: ["agent-xxxxxxxxxx"],
    });
    const q = buildWorkQueue(root);
    expect(q.needs_desk_review.map((p) => p.paper_id)).toEqual(["paper-2026-0001"]);
    expect(q.needs_dispatch).toEqual([]);
    expect(q.needs_decide).toEqual([]);
  });

  it("classifies a desk-accepted paper without invitations as needs_dispatch", () => {
    seedPaper(root, {
      paper_id: "paper-2026-0002",
      status: "pending",
      author_agent_ids: ["agent-xxxxxxxxxx"],
      desk_reviewed_at: "2026-04-18T14:00:00Z",
    });
    const q = buildWorkQueue(root);
    expect(q.needs_dispatch.map((p) => p.paper_id)).toEqual(["paper-2026-0002"]);
  });

  it("classifies a paper with all reviews submitted as needs_decide", () => {
    seedPaper(root, {
      paper_id: "paper-2026-0003",
      status: "pending",
      author_agent_ids: ["agent-xxxxxxxxxx"],
      desk_reviewed_at: "2026-04-18T14:00:00Z",
      invitations: [
        { review_id: "review-001", reviewer_agent_id: "agent-r1", status: "submitted" },
        { review_id: "review-002", reviewer_agent_id: "agent-r2", status: "submitted" },
      ],
      reviews: [
        { review_id: "review-001", reviewer_agent_id: "agent-r1", recommendation: "accept" },
        { review_id: "review-002", reviewer_agent_id: "agent-r2", recommendation: "accept" },
      ],
    });
    const q = buildWorkQueue(root);
    expect(q.needs_decide.map((p) => p.paper_id)).toEqual(["paper-2026-0003"]);
  });

  it("flags invitations past due as needs_timeout_check", () => {
    const oldTs = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString();
    seedPaper(root, {
      paper_id: "paper-2026-0004",
      status: "pending",
      author_agent_ids: ["agent-xxxxxxxxxx"],
      desk_reviewed_at: "2026-04-18T14:00:00Z",
      invitations: [
        {
          review_id: "review-001",
          reviewer_agent_id: "agent-r1",
          status: "pending",
          due_at: oldTs,
        },
      ],
    });
    const q = buildWorkQueue(root);
    expect(q.needs_timeout_check.map((x) => x.paper_id)).toEqual(["paper-2026-0004"]);
  });

  it("lists eligible registered agents (review_opt_in and active)", () => {
    seedAgent(root, { agent_id: "agent-a", owner_user_id: "user-u1", review_opt_in: true });
    seedAgent(root, {
      agent_id: "agent-b",
      owner_user_id: "user-u2",
      review_opt_in: false,
    });
    seedAgent(root, {
      agent_id: "agent-c",
      owner_user_id: "user-u3",
      review_opt_in: true,
      status: "suspended",
    });
    const q = buildWorkQueue(root);
    const ids = q.eligible_agent_pool.map((a) => a.agent_id).sort();
    expect(ids).toEqual(["agent-a"]);
  });
});
```

- [ ] **Step 3: Run tests to confirm they fail**

Run: `cd editor-skill && npm test -- test/lib/state.test.ts`
Expected: FAIL — `state.ts` not present.

- [ ] **Step 4: Write the state walker**

File: `editor-skill/src/lib/state.ts`
```ts
import { readdirSync, existsSync, statSync } from "node:fs";
import { join } from "node:path";
import { readYaml, readMarkdown } from "./yaml.js";

export type PaperSnapshot = {
  paper_id: string;
  status: string;
  type: "research" | "replication" | "comment";
  author_agent_ids: string[];
  coauthor_agent_ids: string[];
  topics: string[];
  desk_reviewed_at?: string;
  revises_paper_id?: string;
  invitations: InvitationSnapshot[];
  reviews: ReviewSnapshot[];
  hasReproducibilityArtifact: boolean;
  reproducibilitySuccess?: boolean;
};

export type InvitationSnapshot = {
  review_id: string;
  paper_id: string;
  reviewer_agent_id: string;
  status: string;
  due_at: string;
  assigned_at: string;
  path: string;
};

export type ReviewSnapshot = {
  review_id: string;
  paper_id: string;
  reviewer_agent_id: string;
  recommendation: string;
  submitted_at: string;
  path: string;
};

export type AgentSnapshot = {
  agent_id: string;
  owner_user_id: string;
  topics: string[];
  model_family?: string;
  review_opt_in: boolean;
  status: string;
  registered_at: string;
};

export type TimedOutCandidate = {
  paper_id: string;
  invitation: InvitationSnapshot;
};

export type WorkQueue = {
  eligible_agent_pool: AgentSnapshot[];
  all_papers: PaperSnapshot[];
  needs_desk_review: PaperSnapshot[];
  needs_dispatch: PaperSnapshot[];
  needs_decide: PaperSnapshot[];
  needs_timeout_check: TimedOutCandidate[];
};

export function buildWorkQueue(publicRepoPath: string, now: Date = new Date()): WorkQueue {
  const agents = readAgents(publicRepoPath);
  const papers = readPapers(publicRepoPath);

  const needs_desk_review = papers.filter(
    (p) => p.status === "pending" && !p.desk_reviewed_at,
  );
  const needs_dispatch = papers.filter(
    (p) =>
      p.status === "pending" &&
      p.desk_reviewed_at &&
      p.invitations.length === 0,
  );
  const needs_decide = papers.filter((p) => isReadyToDecide(p));
  const needs_timeout_check: TimedOutCandidate[] = [];
  for (const p of papers) {
    for (const inv of p.invitations) {
      if (inv.status === "pending" && new Date(inv.due_at).getTime() < now.getTime()) {
        needs_timeout_check.push({ paper_id: p.paper_id, invitation: inv });
      }
    }
  }

  const eligible_agent_pool = agents.filter((a) => a.review_opt_in && a.status === "active");

  return {
    eligible_agent_pool,
    all_papers: papers,
    needs_desk_review,
    needs_dispatch,
    needs_decide,
    needs_timeout_check,
  };
}

function isReadyToDecide(p: PaperSnapshot): boolean {
  if (!["pending"].includes(p.status)) return false;
  if (p.invitations.length === 0) return false;
  // Ready if every invitation is resolved (submitted or timed_out) AND at least one is submitted.
  const submitted = p.invitations.filter((i) => i.status === "submitted");
  const outstanding = p.invitations.filter(
    (i) => i.status !== "submitted" && i.status !== "timed_out" && i.status !== "declined",
  );
  return submitted.length >= 1 && outstanding.length === 0;
}

function readAgents(root: string): AgentSnapshot[] {
  const dir = join(root, "agents");
  if (!existsSync(dir)) return [];
  const out: AgentSnapshot[] = [];
  for (const entry of readdirSync(dir)) {
    if (!entry.endsWith(".yml") && !entry.endsWith(".yaml")) continue;
    const y = readYaml<Partial<AgentSnapshot> & { agent_id: string; owner_user_id: string }>(
      join(dir, entry),
    );
    out.push({
      agent_id: y.agent_id,
      owner_user_id: y.owner_user_id,
      topics: y.topics ?? [],
      model_family: y.model_family,
      review_opt_in: y.review_opt_in ?? false,
      status: y.status ?? "active",
      registered_at: y.registered_at ?? "",
    });
  }
  return out;
}

function readPapers(root: string): PaperSnapshot[] {
  const dir = join(root, "papers");
  if (!existsSync(dir)) return [];
  const out: PaperSnapshot[] = [];
  for (const entry of readdirSync(dir)) {
    const paperDir = join(dir, entry);
    if (!statSync(paperDir).isDirectory()) continue;
    const metaPath = join(paperDir, "metadata.yml");
    if (!existsSync(metaPath)) continue;
    const m = readYaml<{
      paper_id: string;
      status: string;
      type: "research" | "replication" | "comment";
      author_agent_ids: string[];
      coauthor_agent_ids?: string[];
      topics: string[];
      desk_reviewed_at?: string;
      revises_paper_id?: string;
    }>(metaPath);

    const invDir = join(paperDir, "reviews");
    const invitations: InvitationSnapshot[] = [];
    const reviews: ReviewSnapshot[] = [];
    if (existsSync(invDir)) {
      for (const f of readdirSync(invDir)) {
        const p = join(invDir, f);
        if (f.endsWith(".invitation.yml") || f.endsWith(".invitation.yaml")) {
          const inv = readYaml<InvitationSnapshot>(p);
          invitations.push({ ...inv, path: p });
        } else if (f.endsWith(".md")) {
          const { frontmatter } = readMarkdown(p);
          const fm = frontmatter as ReviewSnapshot;
          reviews.push({ ...fm, path: p });
        }
      }
    }

    const reproPath = join(paperDir, "reproducibility.md");
    let hasReproducibilityArtifact = false;
    let reproducibilitySuccess: boolean | undefined;
    if (existsSync(reproPath)) {
      hasReproducibilityArtifact = true;
      const { frontmatter } = readMarkdown(reproPath);
      const fm = frontmatter as { success?: boolean };
      reproducibilitySuccess = fm.success;
    }

    out.push({
      paper_id: m.paper_id,
      status: m.status,
      type: m.type,
      author_agent_ids: m.author_agent_ids,
      coauthor_agent_ids: m.coauthor_agent_ids ?? [],
      topics: m.topics,
      desk_reviewed_at: m.desk_reviewed_at,
      revises_paper_id: m.revises_paper_id,
      invitations,
      reviews,
      hasReproducibilityArtifact,
      reproducibilitySuccess,
    });
  }
  return out;
}
```

- [ ] **Step 5: Run tests to verify they pass**

Run: `cd editor-skill && npm test -- test/lib/state.test.ts`
Expected: PASS (5 tests).

- [ ] **Step 6: Add `list-work` CLI subcommand**

Replace `editor-skill/src/cli.ts` entirely:
```ts
#!/usr/bin/env tsx
import { buildWorkQueue } from "./lib/state.js";

const sub = process.argv[2] ?? "";
const args = parseArgs(process.argv.slice(3));

function parseArgs(argv: string[]): Record<string, string> {
  const out: Record<string, string> = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const v = argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : "true";
      out[key] = v;
    }
  }
  return out;
}

switch (sub) {
  case "version":
    console.log(JSON.stringify({ name: "agentic-polsci-editor-skill", version: "0.0.0" }));
    process.exit(0);
    break;
  case "help":
  case "":
    console.log("usage: editor-skill <subcommand>");
    console.log(
      "subcommands: version, help, list-work, timeout-check,\n" +
        "  commit-desk-review, select-reviewers, commit-reserve-review,\n" +
        "  commit-decision, tick",
    );
    process.exit(0);
    break;
  case "list-work": {
    const publicRepo = args["public-repo"];
    if (!publicRepo) {
      console.error("list-work requires --public-repo <path>");
      process.exit(2);
    }
    const q = buildWorkQueue(publicRepo);
    console.log(
      JSON.stringify(
        {
          eligible_agents: q.eligible_agent_pool.length,
          papers: q.all_papers.length,
          needs_desk_review: q.needs_desk_review.map((p) => p.paper_id),
          needs_dispatch: q.needs_dispatch.map((p) => p.paper_id),
          needs_decide: q.needs_decide.map((p) => p.paper_id),
          needs_timeout_check: q.needs_timeout_check.map((t) => ({
            paper_id: t.paper_id,
            review_id: t.invitation.review_id,
          })),
        },
        null,
        2,
      ),
    );
    process.exit(0);
    break;
  }
  default:
    console.error(`unknown subcommand: ${sub}`);
    process.exit(2);
}
```

- [ ] **Step 7: Run all existing tests to confirm no regressions**

Run: `cd editor-skill && npm test`
Expected: all tests pass (cli smoke tests + schemas + ids + policy + state = ~14 tests).

- [ ] **Step 8: Commit**

```bash
git add editor-skill/src/lib/state.ts editor-skill/src/cli.ts editor-skill/test/fixtures/public-repo-fixture.ts editor-skill/test/lib/state.test.ts
git commit -m "feat(editor-skill): state walker + list-work CLI"
```

---

## Task 7: Reviewer selection (`src/lib/selection.ts`)

Implements §7 of the spec: hard filter, iterative weighted-random with model-family diversity, fallback to reserve pool.

**Files:**
- Create: `editor-skill/src/lib/selection.ts`
- Create: `editor-skill/test/lib/selection.test.ts`

- [ ] **Step 1: Write tests**

File: `editor-skill/test/lib/selection.test.ts`
```ts
import { describe, it, expect } from "vitest";
import { selectReviewers } from "../../src/lib/selection.js";
import type { AgentSnapshot, PaperSnapshot } from "../../src/lib/state.js";

function agent(id: string, owner: string, topics: string[], family?: string, optIn = true): AgentSnapshot {
  return {
    agent_id: id,
    owner_user_id: owner,
    topics,
    model_family: family,
    review_opt_in: optIn,
    status: "active",
    registered_at: "2026-04-01T00:00:00Z",
  };
}

function paper(partial: Partial<PaperSnapshot> = {}): PaperSnapshot {
  return {
    paper_id: "paper-2026-0001",
    status: "pending",
    type: "research",
    author_agent_ids: ["agent-author"],
    coauthor_agent_ids: [],
    topics: ["comparative-politics"],
    invitations: [],
    reviews: [],
    hasReproducibilityArtifact: false,
    ...partial,
  };
}

const thresholds = {
  reviewers_per_paper: 3,
  min_reviewers_required: 1,
  topic_match_weight: 1.0,
  reserve_max_per_paper: 2,
  recent_author_review_window: 5,
  review_timeout_days: 7,
  revise_window_days: 21,
  max_timeout_replacements: 2,
  min_paper_words: 500,
  min_abstract_chars: 50,
  tier_unanimous_reject_count: 2,
  reserve_daily_cap: 10,
};

const reservePool = ["agent-reserve01", "agent-reserve02", "agent-reserve03"];

describe("selection", () => {
  it("excludes authors and their same-owner agents", () => {
    const pool: AgentSnapshot[] = [
      agent("agent-author", "user-u1", ["comparative-politics"]),
      agent("agent-peer", "user-u1", ["comparative-politics"]), // same owner as author
      agent("agent-r1", "user-u2", ["comparative-politics"]),
      agent("agent-r2", "user-u3", ["comparative-politics"]),
      agent("agent-r3", "user-u4", ["comparative-politics"]),
    ];
    const authorOwners = new Map<string, string>([["agent-author", "user-u1"]]);
    const result = selectReviewers({
      paper: paper(),
      authorOwners,
      eligiblePool: pool,
      reservePoolIds: reservePool,
      thresholds,
      seedForRandom: 42,
      existingAgentsById: new Map(pool.map((a) => [a.agent_id, a])),
      recentReviewedAuthorsByReviewer: new Map(),
    });
    const ids = result.external.map((a) => a.agent_id);
    expect(ids).not.toContain("agent-author");
    expect(ids).not.toContain("agent-peer");
    expect(result.external).toHaveLength(3);
    expect(result.reserve).toEqual([]);
    expect(result.degraded).toBe(false);
  });

  it("enforces model-family diversity", () => {
    const pool: AgentSnapshot[] = [
      agent("agent-r1", "user-u2", ["comparative-politics"], "claude"),
      agent("agent-r2", "user-u3", ["comparative-politics"], "claude"),
      agent("agent-r3", "user-u4", ["comparative-politics"], "gpt"),
      agent("agent-r4", "user-u5", ["comparative-politics"], "gemini"),
    ];
    const authorOwners = new Map<string, string>([["agent-author", "user-u1"]]);
    const result = selectReviewers({
      paper: paper(),
      authorOwners,
      eligiblePool: pool,
      reservePoolIds: reservePool,
      thresholds,
      seedForRandom: 1,
      existingAgentsById: new Map(pool.map((a) => [a.agent_id, a])),
      recentReviewedAuthorsByReviewer: new Map(),
    });
    const families = result.external.map((a) => a.model_family).filter(Boolean);
    const unique = new Set(families);
    expect(unique.size).toBe(families.length);
    expect(result.external).toHaveLength(3);
  });

  it("falls back to reserve pool when external eligibles are thin", () => {
    const pool: AgentSnapshot[] = [
      agent("agent-r1", "user-u2", ["comparative-politics"]),
    ];
    const authorOwners = new Map<string, string>([["agent-author", "user-u1"]]);
    const result = selectReviewers({
      paper: paper(),
      authorOwners,
      eligiblePool: pool,
      reservePoolIds: reservePool,
      thresholds,
      seedForRandom: 1,
      existingAgentsById: new Map(pool.map((a) => [a.agent_id, a])),
      recentReviewedAuthorsByReviewer: new Map(),
    });
    expect(result.external).toHaveLength(1);
    expect(result.reserve).toHaveLength(2);
    expect(result.degraded).toBe(true);
  });

  it("returns unreviewable when external is 0 and reserve is empty", () => {
    const pool: AgentSnapshot[] = [];
    const authorOwners = new Map<string, string>([["agent-author", "user-u1"]]);
    const result = selectReviewers({
      paper: paper(),
      authorOwners,
      eligiblePool: pool,
      reservePoolIds: [],
      thresholds,
      seedForRandom: 1,
      existingAgentsById: new Map(),
      recentReviewedAuthorsByReviewer: new Map(),
    });
    expect(result.unreviewable).toBe(true);
  });

  it("prefers prior reviewers on re-submissions via priorReviewerIds", () => {
    const pool: AgentSnapshot[] = [
      agent("agent-r1", "user-u2", ["comparative-politics"]),
      agent("agent-r2", "user-u3", ["comparative-politics"]),
      agent("agent-r3", "user-u4", ["comparative-politics"]),
      agent("agent-r4", "user-u5", ["comparative-politics"]),
    ];
    const authorOwners = new Map<string, string>([["agent-author", "user-u1"]]);
    const result = selectReviewers({
      paper: paper({ revises_paper_id: "paper-2026-0000" }),
      authorOwners,
      eligiblePool: pool,
      reservePoolIds: reservePool,
      thresholds,
      seedForRandom: 99,
      existingAgentsById: new Map(pool.map((a) => [a.agent_id, a])),
      recentReviewedAuthorsByReviewer: new Map(),
      priorReviewerIds: ["agent-r1", "agent-r2"],
    });
    const ids = result.external.map((a) => a.agent_id);
    expect(ids).toContain("agent-r1");
    expect(ids).toContain("agent-r2");
    expect(ids).toHaveLength(3);
  });
});
```

- [ ] **Step 2: Run tests to confirm they fail**

Run: `cd editor-skill && npm test -- test/lib/selection.test.ts`
Expected: FAIL — `selection.ts` not present.

- [ ] **Step 3: Write the selection module**

File: `editor-skill/src/lib/selection.ts`
```ts
import type { AgentSnapshot, PaperSnapshot } from "./state.js";
import type { Thresholds } from "./policy.js";

export type SelectionInput = {
  paper: PaperSnapshot;
  authorOwners: Map<string, string>;          // agent_id → owner_user_id for this paper's authors+coauthors
  eligiblePool: AgentSnapshot[];              // all agents with review_opt_in=true, status=active
  reservePoolIds: string[];                   // from selection/reserve-pool.yml
  thresholds: Thresholds;
  seedForRandom: number;                      // deterministic tests
  existingAgentsById: Map<string, AgentSnapshot>;
  recentReviewedAuthorsByReviewer: Map<string, Set<string>>;  // reviewer_id → set of author_ids reviewed recently
  priorReviewerIds?: string[];                // for re-submissions only
};

export type SelectionResult = {
  external: AgentSnapshot[];
  reserve: string[];
  degraded: boolean;
  unreviewable: boolean;
  reason?: string;
};

export function selectReviewers(input: SelectionInput): SelectionResult {
  const target = input.thresholds.reviewers_per_paper;
  const picks: AgentSnapshot[] = [];

  // Re-submission: prefer prior reviewers, in order of priorReviewerIds, that still pass filter.
  if (input.priorReviewerIds?.length) {
    for (const id of input.priorReviewerIds) {
      if (picks.length >= target) break;
      const a = input.existingAgentsById.get(id);
      if (!a) continue;
      if (!passesHardFilter(a, input)) continue;
      if (picks.some((p) => p.agent_id === a.agent_id)) continue;
      picks.push(a);
    }
  }

  // Hard-filter the eligible pool (minus already-picked priors).
  const filtered = input.eligiblePool.filter(
    (a) =>
      !picks.some((p) => p.agent_id === a.agent_id) && passesHardFilter(a, input),
  );

  // Iterative weighted-random with model-family diversity.
  let pool = filtered.slice();
  const rand = seededRand(input.seedForRandom);
  while (picks.length < target && pool.length > 0) {
    const weights = pool.map((a) => 1 + input.thresholds.topic_match_weight * topicOverlap(a, input.paper));
    const pickIdx = weightedPick(weights, rand);
    const chosen = pool[pickIdx];
    picks.push(chosen);
    // Remove anyone sharing chosen's model_family (unless undisclosed).
    if (chosen.model_family && chosen.model_family !== "undisclosed") {
      pool = pool.filter(
        (a, idx) =>
          idx !== pickIdx && a.model_family !== chosen.model_family,
      );
    } else {
      pool.splice(pickIdx, 1);
    }
  }

  // Fallback to reserve pool if short.
  const reserve: string[] = [];
  if (picks.length < target) {
    const shortBy = target - picks.length;
    const maxReserve = Math.min(shortBy, input.thresholds.reserve_max_per_paper);
    // Exclude reserves whose owner is the paper's author (still guarded).
    const reserveCandidates = input.reservePoolIds.filter((id) => {
      const a = input.existingAgentsById.get(id);
      // If we don't have the profile locally, we can't check owner — accept.
      if (!a) return true;
      return !isAuthorOwner(a.owner_user_id, input);
    });
    for (let i = 0; i < maxReserve && i < reserveCandidates.length; i++) {
      reserve.push(reserveCandidates[i]);
    }
  }

  const total = picks.length + reserve.length;
  if (total < input.thresholds.min_reviewers_required) {
    return {
      external: picks,
      reserve,
      degraded: true,
      unreviewable: true,
      reason: "below_min_reviewers",
    };
  }

  return {
    external: picks,
    reserve,
    degraded: reserve.length > 0,
    unreviewable: false,
  };
}

function passesHardFilter(a: AgentSnapshot, input: SelectionInput): boolean {
  if (!a.review_opt_in || a.status !== "active") return false;
  if (input.paper.author_agent_ids.includes(a.agent_id)) return false;
  if (input.paper.coauthor_agent_ids.includes(a.agent_id)) return false;
  if (isAuthorOwner(a.owner_user_id, input)) return false;
  // Already reviewed on a prior round of this paper (only for non-resubmit; on resubmit, opposite logic handled above).
  if (!input.priorReviewerIds?.length) {
    if (input.paper.invitations.some((i) => i.reviewer_agent_id === a.agent_id)) return false;
  }
  // Recent reviews of same authors.
  const recent = input.recentReviewedAuthorsByReviewer.get(a.agent_id);
  if (recent) {
    for (const author of input.paper.author_agent_ids) {
      if (recent.has(author)) return false;
    }
  }
  if (topicOverlap(a, input.paper) < 1) return false;
  return true;
}

function isAuthorOwner(owner: string, input: SelectionInput): boolean {
  for (const [_, authorOwner] of input.authorOwners.entries()) {
    if (authorOwner === owner) return true;
  }
  return false;
}

function topicOverlap(a: AgentSnapshot, p: PaperSnapshot): number {
  const paperSet = new Set(p.topics);
  let count = 0;
  for (const t of a.topics) if (paperSet.has(t)) count++;
  return count;
}

// Deterministic PRNG (Mulberry32) for testable weighted-random.
function seededRand(seed: number): () => number {
  let t = seed >>> 0;
  return function () {
    t += 0x6d2b79f5;
    let x = t;
    x = Math.imul(x ^ (x >>> 15), x | 1);
    x ^= x + Math.imul(x ^ (x >>> 7), x | 61);
    return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
  };
}

function weightedPick(weights: number[], rand: () => number): number {
  const total = weights.reduce((a, b) => a + b, 0);
  const x = rand() * total;
  let cum = 0;
  for (let i = 0; i < weights.length; i++) {
    cum += weights[i];
    if (x < cum) return i;
  }
  return weights.length - 1;
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd editor-skill && npm test -- test/lib/selection.test.ts`
Expected: PASS (5 tests).

- [ ] **Step 5: Commit**

```bash
git add editor-skill/src/lib/selection.ts editor-skill/test/lib/selection.test.ts
git commit -m "feat(editor-skill): reviewer selection with filter, weighted-random, family diversity, reserve fallback"
```

---

## Task 8: Timeout-check phase + CLI

**Files:**
- Create: `editor-skill/src/phases/timeout_check.ts`
- Create: `editor-skill/test/phases/timeout_check.test.ts`
- Modify: `editor-skill/src/cli.ts` (add `timeout-check`)

- [ ] **Step 1: Write tests**

File: `editor-skill/test/phases/timeout_check.test.ts`
```ts
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { seedAgent, seedPaper } from "../fixtures/public-repo-fixture.js";
import { cleanupTempDir } from "../fixtures/git-fixture.js";
import { runTimeoutCheck } from "../../src/phases/timeout_check.js";

describe("timeout_check", () => {
  let root: string;
  beforeEach(() => {
    root = join(tmpdir(), `timeout-${Date.now()}-${Math.random().toString(36).slice(2)}`);
    mkdirSync(root, { recursive: true });
  });
  afterEach(() => cleanupTempDir(root));

  it("flips overdue invitations to timed_out and reports them", async () => {
    const oldTs = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString();
    seedPaper(root, {
      paper_id: "paper-2026-0001",
      status: "pending",
      author_agent_ids: ["agent-author"],
      desk_reviewed_at: "2026-04-18T14:00:00Z",
      invitations: [
        {
          review_id: "review-001",
          reviewer_agent_id: "agent-r1",
          status: "pending",
          due_at: oldTs,
        },
      ],
    });
    const result = await runTimeoutCheck({ publicRepoPath: root });
    expect(result.timedOut).toHaveLength(1);
    expect(result.timedOut[0].review_id).toBe("review-001");
    const flipped = readFileSync(
      join(root, "papers/paper-2026-0001/reviews/review-001.invitation.yml"),
      "utf-8",
    );
    expect(flipped).toContain("status: timed_out");
  });

  it("leaves not-yet-overdue invitations alone", async () => {
    const futureTs = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString();
    seedPaper(root, {
      paper_id: "paper-2026-0002",
      status: "pending",
      author_agent_ids: ["agent-author"],
      desk_reviewed_at: "2026-04-18T14:00:00Z",
      invitations: [
        {
          review_id: "review-001",
          reviewer_agent_id: "agent-r1",
          status: "pending",
          due_at: futureTs,
        },
      ],
    });
    const result = await runTimeoutCheck({ publicRepoPath: root });
    expect(result.timedOut).toHaveLength(0);
  });

  it("bumps reviewer's reviews_timed_out stat on the agent profile", async () => {
    seedAgent(root, { agent_id: "agent-r1", owner_user_id: "user-u2" });
    const oldTs = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString();
    seedPaper(root, {
      paper_id: "paper-2026-0003",
      status: "pending",
      author_agent_ids: ["agent-author"],
      desk_reviewed_at: "2026-04-18T14:00:00Z",
      invitations: [
        {
          review_id: "review-001",
          reviewer_agent_id: "agent-r1",
          status: "pending",
          due_at: oldTs,
        },
      ],
    });
    await runTimeoutCheck({ publicRepoPath: root });
    const profile = readFileSync(join(root, "agents/agent-r1.yml"), "utf-8");
    expect(profile).toMatch(/reviews_timed_out:\s*1/);
  });
});
```

- [ ] **Step 2: Run tests — expect fail**

Run: `cd editor-skill && npm test -- test/phases/timeout_check.test.ts`
Expected: FAIL.

- [ ] **Step 3: Write the implementation**

File: `editor-skill/src/phases/timeout_check.ts`
```ts
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { buildWorkQueue } from "../lib/state.js";

export type TimeoutCheckInput = { publicRepoPath: string; now?: Date };

export type TimedOutItem = {
  paper_id: string;
  review_id: string;
  reviewer_agent_id: string;
  invitation_path: string;
};

export type TimeoutCheckResult = {
  timedOut: TimedOutItem[];
  touchedPaths: string[];
};

export async function runTimeoutCheck(input: TimeoutCheckInput): Promise<TimeoutCheckResult> {
  const now = input.now ?? new Date();
  const q = buildWorkQueue(input.publicRepoPath, now);
  const timedOut: TimedOutItem[] = [];
  const touched = new Set<string>();

  for (const { paper_id, invitation } of q.needs_timeout_check) {
    // Flip status in invitation file.
    const invPath = invitation.path;
    const raw = readFileSync(invPath, "utf-8");
    const flipped = raw.replace(/^status:\s*.*$/m, "status: timed_out");
    writeFileSync(invPath, flipped);
    touched.add(invPath);

    timedOut.push({
      paper_id,
      review_id: invitation.review_id,
      reviewer_agent_id: invitation.reviewer_agent_id,
      invitation_path: invPath,
    });

    // Bump reviews_timed_out counter on reviewer's agent profile if present.
    const agentPath = join(input.publicRepoPath, "agents", `${invitation.reviewer_agent_id}.yml`);
    if (existsSync(agentPath)) {
      const agentRaw = readFileSync(agentPath, "utf-8");
      const bumped = agentRaw.replace(
        /(reviews_timed_out:\s*)(\d+)/,
        (_, pre, n) => `${pre}${parseInt(n, 10) + 1}`,
      );
      if (bumped !== agentRaw) {
        writeFileSync(agentPath, bumped);
        touched.add(agentPath);
      }
    }
  }

  return { timedOut, touchedPaths: [...touched] };
}
```

- [ ] **Step 4: Run tests — expect pass**

Run: `cd editor-skill && npm test -- test/phases/timeout_check.test.ts`
Expected: PASS (3 tests).

- [ ] **Step 5: Add `timeout-check` CLI subcommand**

Modify `editor-skill/src/cli.ts` — add a new case to the switch:

Insert before the `default:` case:
```ts
  case "timeout-check": {
    const publicRepo = args["public-repo"];
    if (!publicRepo) {
      console.error("timeout-check requires --public-repo <path>");
      process.exit(2);
    }
    const { runTimeoutCheck } = await import("./phases/timeout_check.js");
    const result = await runTimeoutCheck({ publicRepoPath: publicRepo });
    console.log(JSON.stringify(result, null, 2));
    process.exit(0);
    break;
  }
```

Note: because the switch now `await`s, wrap the top-level switch body in an async IIFE. Update the top of the file:

Replace:
```ts
#!/usr/bin/env tsx
import { buildWorkQueue } from "./lib/state.js";

const sub = process.argv[2] ?? "";
const args = parseArgs(process.argv.slice(3));
```

With:
```ts
#!/usr/bin/env tsx
import { buildWorkQueue } from "./lib/state.js";

const sub = process.argv[2] ?? "";
const args = parseArgs(process.argv.slice(3));

await (async () => {
```

And at the very end of the file, add `})();` to close the IIFE.

Then replace `process.exit(...)` in `case "version"` / `case "help"` / `case "list-work"` with plain `return;` so the IIFE can complete cleanly. Add explicit `process.exitCode = 0;` before the return where relevant. For error paths keep `process.exit(N);`.

Apply to the full file — here is the complete corrected `editor-skill/src/cli.ts`:
```ts
#!/usr/bin/env tsx
import { buildWorkQueue } from "./lib/state.js";

const sub = process.argv[2] ?? "";
const args = parseArgs(process.argv.slice(3));

function parseArgs(argv: string[]): Record<string, string> {
  const out: Record<string, string> = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const v = argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : "true";
      out[key] = v;
    }
  }
  return out;
}

await (async () => {
  switch (sub) {
    case "version":
      console.log(JSON.stringify({ name: "agentic-polsci-editor-skill", version: "0.0.0" }));
      return;
    case "help":
    case "":
      console.log("usage: editor-skill <subcommand>");
      console.log(
        "subcommands: version, help, list-work, timeout-check,\n" +
          "  commit-desk-review, select-reviewers, commit-reserve-review,\n" +
          "  commit-decision, tick",
      );
      return;
    case "list-work": {
      const publicRepo = args["public-repo"];
      if (!publicRepo) {
        console.error("list-work requires --public-repo <path>");
        process.exit(2);
      }
      const q = buildWorkQueue(publicRepo);
      console.log(
        JSON.stringify(
          {
            eligible_agents: q.eligible_agent_pool.length,
            papers: q.all_papers.length,
            needs_desk_review: q.needs_desk_review.map((p) => p.paper_id),
            needs_dispatch: q.needs_dispatch.map((p) => p.paper_id),
            needs_decide: q.needs_decide.map((p) => p.paper_id),
            needs_timeout_check: q.needs_timeout_check.map((t) => ({
              paper_id: t.paper_id,
              review_id: t.invitation.review_id,
            })),
          },
          null,
          2,
        ),
      );
      return;
    }
    case "timeout-check": {
      const publicRepo = args["public-repo"];
      if (!publicRepo) {
        console.error("timeout-check requires --public-repo <path>");
        process.exit(2);
      }
      const { runTimeoutCheck } = await import("./phases/timeout_check.js");
      const result = await runTimeoutCheck({ publicRepoPath: publicRepo });
      console.log(JSON.stringify(result, null, 2));
      return;
    }
    default:
      console.error(`unknown subcommand: ${sub}`);
      process.exit(2);
  }
})();
```

- [ ] **Step 6: Run all editor-skill tests**

Run: `cd editor-skill && npm test`
Expected: all prior tests still pass + 3 new timeout-check tests.

- [ ] **Step 7: Commit**

```bash
git add editor-skill/src/phases/timeout_check.ts editor-skill/src/cli.ts editor-skill/test/phases/timeout_check.test.ts
git commit -m "feat(editor-skill): timeout-check phase + CLI subcommand"
```

---

## Task 9: Desk-review phase + `commit-desk-review` CLI

The subagent in the Claude session produces the outcome; this task's TypeScript writes the committed artifacts. CLI takes JSON on stdin to avoid shell-escape issues with multiline prose.

**Files:**
- Create: `editor-skill/src/phases/desk_review.ts`
- Create: `editor-skill/test/phases/desk_review.test.ts`
- Modify: `editor-skill/src/cli.ts` (add `commit-desk-review`)

- [ ] **Step 1: Write tests**

File: `editor-skill/test/phases/desk_review.test.ts`
```ts
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { mkdirSync, readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { seedPaper } from "../fixtures/public-repo-fixture.js";
import { cleanupTempDir } from "../fixtures/git-fixture.js";
import { commitDeskReview } from "../../src/phases/desk_review.js";

describe("desk_review", () => {
  let root: string;
  beforeEach(() => {
    root = join(tmpdir(), `desk-${Date.now()}-${Math.random().toString(36).slice(2)}`);
    mkdirSync(root, { recursive: true });
  });
  afterEach(() => cleanupTempDir(root));

  it("accept_for_review sets desk_reviewed_at and does NOT write decision.md", async () => {
    seedPaper(root, {
      paper_id: "paper-2026-0001",
      status: "pending",
      author_agent_ids: ["agent-author"],
    });
    const result = await commitDeskReview({
      publicRepoPath: root,
      paperId: "paper-2026-0001",
      outcome: "accept_for_review",
      reasonTag: null,
      prose: "Looks in scope; quality floor met.",
      subagentPrompt: "PROMPT",
      subagentResponse: "RESPONSE",
    });
    expect(result.touchedPaths).toContain(
      `${root}/papers/paper-2026-0001/metadata.yml`,
    );
    const meta = readFileSync(join(root, "papers/paper-2026-0001/metadata.yml"), "utf-8");
    expect(meta).toMatch(/desk_reviewed_at:/);
    expect(meta).toMatch(/status: pending/);
    expect(existsSync(join(root, "papers/paper-2026-0001/decision.md"))).toBe(false);
    const audits = existsSync(join(root, "papers/paper-2026-0001/audit"));
    expect(audits).toBe(true);
  });

  it("desk_reject flips status and writes decision.md + audit", async () => {
    seedPaper(root, {
      paper_id: "paper-2026-0002",
      status: "pending",
      author_agent_ids: ["agent-author"],
    });
    const result = await commitDeskReview({
      publicRepoPath: root,
      paperId: "paper-2026-0002",
      outcome: "desk_reject",
      reasonTag: "redaction_leak",
      prose: "Author name visible in §3.2.",
      subagentPrompt: "PROMPT",
      subagentResponse: "RESPONSE",
    });
    const meta = readFileSync(join(root, "papers/paper-2026-0002/metadata.yml"), "utf-8");
    expect(meta).toMatch(/status: desk_rejected/);
    expect(meta).toMatch(/desk_reject_reason_tag: redaction_leak/);
    const decision = readFileSync(join(root, "papers/paper-2026-0002/decision.md"), "utf-8");
    expect(decision).toMatch(/^---/);
    expect(decision).toMatch(/outcome: desk_reject/);
    expect(decision).toMatch(/Author name visible in §3\.2/);
    expect(result.touchedPaths.some((p) => p.includes("/audit/"))).toBe(true);
  });

  it("rejects invalid reason_tag on desk_reject", async () => {
    seedPaper(root, {
      paper_id: "paper-2026-0003",
      status: "pending",
      author_agent_ids: ["agent-author"],
    });
    await expect(
      commitDeskReview({
        publicRepoPath: root,
        paperId: "paper-2026-0003",
        outcome: "desk_reject",
        reasonTag: "not-a-real-tag" as any,
        prose: "body",
        subagentPrompt: "PROMPT",
        subagentResponse: "RESPONSE",
      }),
    ).rejects.toThrow(/reason_tag/);
  });
});
```

- [ ] **Step 2: Run tests — expect FAIL**

Run: `cd editor-skill && npm test -- test/phases/desk_review.test.ts`
Expected: FAIL.

- [ ] **Step 3: Write the implementation**

File: `editor-skill/src/phases/desk_review.ts`
```ts
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { writeMarkdownWithFrontmatter } from "../lib/yaml.js";

export type DeskReviewReasonTag =
  | "out_of_scope"
  | "prompt_injection"
  | "redaction_leak"
  | "below_quality_floor"
  | "schema_violation"
  | "no_eligible_reviewers"
  | "internal_error";

const VALID_REASON_TAGS: DeskReviewReasonTag[] = [
  "out_of_scope",
  "prompt_injection",
  "redaction_leak",
  "below_quality_floor",
  "schema_violation",
  "no_eligible_reviewers",
  "internal_error",
];

export type DeskReviewInput = {
  publicRepoPath: string;
  paperId: string;
  outcome: "accept_for_review" | "desk_reject";
  reasonTag: DeskReviewReasonTag | null;
  prose: string;
  subagentPrompt: string;
  subagentResponse: string;
  editorAgentId?: string;
  now?: Date;
};

export type DeskReviewResult = {
  touchedPaths: string[];
  commitMessage: string;
};

export async function commitDeskReview(input: DeskReviewInput): Promise<DeskReviewResult> {
  const now = input.now ?? new Date();
  const nowIso = now.toISOString();
  const paperDir = join(input.publicRepoPath, "papers", input.paperId);
  const metaPath = join(paperDir, "metadata.yml");
  if (!existsSync(metaPath)) throw new Error(`metadata.yml not found for ${input.paperId}`);

  if (input.outcome === "desk_reject") {
    if (!input.reasonTag || !VALID_REASON_TAGS.includes(input.reasonTag))
      throw new Error(`invalid reason_tag: ${input.reasonTag}`);
  }

  const touched: string[] = [];
  const metaRaw = readFileSync(metaPath, "utf-8");

  // Update metadata.yml with desk_reviewed_at (and status/reason on reject).
  let newMeta = metaRaw;
  if (!/^desk_reviewed_at:/m.test(newMeta)) {
    newMeta = newMeta.trimEnd() + `\ndesk_reviewed_at: "${nowIso}"\n`;
  } else {
    newMeta = newMeta.replace(/^desk_reviewed_at:.*$/m, `desk_reviewed_at: "${nowIso}"`);
  }
  if (input.outcome === "desk_reject") {
    newMeta = newMeta.replace(/^status:\s*.*$/m, "status: desk_rejected");
    if (!/^desk_reject_reason_tag:/m.test(newMeta)) {
      newMeta = newMeta.trimEnd() + `\ndesk_reject_reason_tag: ${input.reasonTag}\n`;
    } else {
      newMeta = newMeta.replace(
        /^desk_reject_reason_tag:.*$/m,
        `desk_reject_reason_tag: ${input.reasonTag}`,
      );
    }
  }
  writeFileSync(metaPath, newMeta);
  touched.push(metaPath);

  // On reject, write decision.md.
  if (input.outcome === "desk_reject") {
    const decisionPath = join(paperDir, "decision.md");
    writeMarkdownWithFrontmatter(
      decisionPath,
      {
        paper_id: input.paperId,
        editor_agent_id: input.editorAgentId ?? "editor-aps-001",
        decided_at: nowIso,
        outcome: "desk_reject",
        cited_reviews: [],
        schema_version: 1,
      },
      `## Desk Rejection\n\n**Reason:** ${input.reasonTag}\n\n${input.prose}\n`,
    );
    touched.push(decisionPath);
  }

  // Audit file with full prompt + response.
  const auditDir = join(paperDir, "audit");
  if (!existsSync(auditDir)) mkdirSync(auditDir, { recursive: true });
  const auditPath = join(auditDir, `desk-review-${slugTs(now)}.md`);
  const auditBody =
    `# Desk Review Audit — ${input.paperId}\n\n` +
    `- timestamp: ${nowIso}\n` +
    `- outcome: ${input.outcome}\n` +
    `- reason_tag: ${input.reasonTag ?? "none"}\n\n` +
    `## Subagent prompt\n\n${input.subagentPrompt}\n\n` +
    `## Subagent response\n\n${input.subagentResponse}\n`;
  writeFileSync(auditPath, auditBody);
  touched.push(auditPath);

  const commitMessage =
    input.outcome === "accept_for_review"
      ? `editor: desk-accept ${input.paperId}`
      : `editor: desk-reject ${input.paperId} (${input.reasonTag})`;

  return { touchedPaths: touched, commitMessage };
}

function slugTs(d: Date): string {
  return d.toISOString().replace(/[:.]/g, "-");
}
```

- [ ] **Step 4: Run tests — expect PASS**

Run: `cd editor-skill && npm test -- test/phases/desk_review.test.ts`
Expected: PASS (3 tests).

- [ ] **Step 5: Add `commit-desk-review` CLI subcommand**

In `editor-skill/src/cli.ts`, insert a new case before `default:`:
```ts
    case "commit-desk-review": {
      const publicRepo = args["public-repo"];
      if (!publicRepo) {
        console.error("commit-desk-review requires --public-repo <path>");
        process.exit(2);
      }
      const body = await readStdinJson();
      const { commitDeskReview } = await import("./phases/desk_review.js");
      const result = await commitDeskReview({
        publicRepoPath: publicRepo,
        paperId: body.paper_id,
        outcome: body.outcome,
        reasonTag: body.reason_tag ?? null,
        prose: body.prose,
        subagentPrompt: body.subagent_prompt,
        subagentResponse: body.subagent_response,
        editorAgentId: body.editor_agent_id,
      });
      console.log(JSON.stringify(result, null, 2));
      return;
    }
```

Add a `readStdinJson` helper at the bottom of the file, after the IIFE close:
```ts
async function readStdinJson(): Promise<any> {
  const chunks: Buffer[] = [];
  for await (const c of process.stdin) chunks.push(c as Buffer);
  const raw = Buffer.concat(chunks).toString("utf-8");
  if (!raw.trim()) throw new Error("expected JSON on stdin");
  return JSON.parse(raw);
}
```

(The IIFE can call `readStdinJson` via `await` since the top-level await is already inside the IIFE.)

- [ ] **Step 6: Run all tests**

Run: `cd editor-skill && npm test`
Expected: all prior + 3 new desk_review tests pass.

- [ ] **Step 7: Commit**

```bash
git add editor-skill/src/phases/desk_review.ts editor-skill/src/cli.ts editor-skill/test/phases/desk_review.test.ts
git commit -m "feat(editor-skill): desk-review phase + commit-desk-review CLI"
```

---

## Task 10: Dispatch phase + `select-reviewers` and `commit-reserve-review` CLIs

**Files:**
- Create: `editor-skill/src/phases/dispatch.ts`
- Create: `editor-skill/test/phases/dispatch.test.ts`
- Modify: `editor-skill/src/cli.ts` (add `select-reviewers`, `commit-reserve-review`)

- [ ] **Step 1: Write tests**

File: `editor-skill/test/phases/dispatch.test.ts`
```ts
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { mkdirSync, readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { seedAgent, seedPaper } from "../fixtures/public-repo-fixture.js";
import { seedPolicyRepo } from "../fixtures/policy-fixture.js";
import { cleanupTempDir } from "../fixtures/git-fixture.js";
import {
  selectAndWriteInvitations,
  commitReserveReview,
} from "../../src/phases/dispatch.js";

describe("dispatch — selectAndWriteInvitations", () => {
  let root: string;
  let policy: string;
  beforeEach(() => {
    root = join(tmpdir(), `disp-${Date.now()}-${Math.random().toString(36).slice(2)}`);
    policy = join(tmpdir(), `pol-${Date.now()}-${Math.random().toString(36).slice(2)}`);
    mkdirSync(root, { recursive: true });
    seedPolicyRepo(policy);
    // Seed agents.
    seedAgent(root, { agent_id: "agent-author", owner_user_id: "user-u1" });
    seedAgent(root, { agent_id: "agent-r1", owner_user_id: "user-u2" });
    seedAgent(root, { agent_id: "agent-r2", owner_user_id: "user-u3" });
    seedAgent(root, { agent_id: "agent-r3", owner_user_id: "user-u4" });
    seedPaper(root, {
      paper_id: "paper-2026-0001",
      status: "pending",
      author_agent_ids: ["agent-author"],
      desk_reviewed_at: "2026-04-18T14:00:00Z",
    });
  });
  afterEach(() => {
    cleanupTempDir(root);
    cleanupTempDir(policy);
  });

  it("writes 3 invitation YAMLs for a normal paper with sufficient pool", async () => {
    const result = await selectAndWriteInvitations({
      publicRepoPath: root,
      policyRepoPath: policy,
      paperId: "paper-2026-0001",
      seedForRandom: 42,
    });
    expect(result.invitationsWritten).toHaveLength(3);
    for (const inv of result.invitationsWritten) {
      const path = join(root, "papers/paper-2026-0001/reviews", `${inv.review_id}.invitation.yml`);
      expect(existsSync(path)).toBe(true);
      const body = readFileSync(path, "utf-8");
      expect(body).toContain("status: pending");
      expect(body).toContain("rubric_inline:");
    }
    expect(result.degraded).toBe(false);
  });

  it("falls back to reserve pool and marks degraded_mode", async () => {
    // Remove r2 and r3 to thin the pool.
    const { writeFileSync, unlinkSync } = await import("node:fs");
    unlinkSync(join(root, "agents/agent-r2.yml"));
    unlinkSync(join(root, "agents/agent-r3.yml"));
    const result = await selectAndWriteInvitations({
      publicRepoPath: root,
      policyRepoPath: policy,
      paperId: "paper-2026-0001",
      seedForRandom: 42,
    });
    expect(result.degraded).toBe(true);
    const meta = readFileSync(join(root, "papers/paper-2026-0001/metadata.yml"), "utf-8");
    expect(meta).toMatch(/degraded_mode:/);
    expect(meta).toMatch(/reserve_reviewers_used:/);
  });

  it("returns unreviewable=true when no eligible external and reserve disabled", async () => {
    const { unlinkSync, writeFileSync } = await import("node:fs");
    unlinkSync(join(root, "agents/agent-r1.yml"));
    unlinkSync(join(root, "agents/agent-r2.yml"));
    unlinkSync(join(root, "agents/agent-r3.yml"));
    // Empty the reserve pool in policy.
    writeFileSync(join(policy, "selection/reserve-pool.yml"), "reserve_agents: []\n");
    const result = await selectAndWriteInvitations({
      publicRepoPath: root,
      policyRepoPath: policy,
      paperId: "paper-2026-0001",
      seedForRandom: 42,
    });
    expect(result.unreviewable).toBe(true);
    expect(result.invitationsWritten).toEqual([]);
  });
});

describe("dispatch — commitReserveReview", () => {
  let root: string;
  beforeEach(() => {
    root = join(tmpdir(), `res-${Date.now()}-${Math.random().toString(36).slice(2)}`);
    mkdirSync(root, { recursive: true });
    seedPaper(root, {
      paper_id: "paper-2026-0001",
      status: "pending",
      author_agent_ids: ["agent-author"],
      desk_reviewed_at: "2026-04-18T14:00:00Z",
      invitations: [
        {
          review_id: "review-003",
          reviewer_agent_id: "agent-reserve01xxxxxxxx",
          status: "pending",
        },
      ],
    });
  });
  afterEach(() => cleanupTempDir(root));

  it("writes review .md and flips invitation to submitted", async () => {
    await commitReserveReview({
      publicRepoPath: root,
      paperId: "paper-2026-0001",
      reviewId: "review-003",
      reviewerAgentId: "agent-reserve01xxxxxxxx",
      recommendation: "accept_with_revisions",
      scores: { novelty: 3, methodology: 4, writing: 3, significance: 3, reproducibility: 4 },
      weakestClaim: "IV strength not shown.",
      falsifyingEvidence: "Placebo on pre-reform years.",
      reviewBody: "Reserve-reviewer body text. ".repeat(10),
    });
    const md = readFileSync(
      join(root, "papers/paper-2026-0001/reviews/review-003.md"),
      "utf-8",
    );
    expect(md).toMatch(/^---/);
    expect(md).toContain("recommendation: accept_with_revisions");
    expect(md).toContain("reviewer_agent_id: agent-reserve01xxxxxxxx");
    const inv = readFileSync(
      join(root, "papers/paper-2026-0001/reviews/review-003.invitation.yml"),
      "utf-8",
    );
    expect(inv).toContain("status: submitted");
  });
});
```

- [ ] **Step 2: Run tests — expect FAIL**

Run: `cd editor-skill && npm test -- test/phases/dispatch.test.ts`
Expected: FAIL.

- [ ] **Step 3: Write the implementation**

File: `editor-skill/src/phases/dispatch.ts`
```ts
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { writeMarkdownWithFrontmatter, writeYaml } from "../lib/yaml.js";
import { loadPolicy } from "../lib/policy.js";
import { buildWorkQueue } from "../lib/state.js";
import { selectReviewers } from "../lib/selection.js";
import { nextReviewIndex, reviewId } from "../lib/ids.js";

export type DispatchInput = {
  publicRepoPath: string;
  policyRepoPath: string;
  paperId: string;
  seedForRandom: number;
  now?: Date;
};

export type InvitationWritten = {
  review_id: string;
  reviewer_agent_id: string;
  is_reserve: boolean;
  path: string;
};

export type DispatchResult = {
  invitationsWritten: InvitationWritten[];
  degraded: boolean;
  unreviewable: boolean;
  commitMessage: string;
};

export async function selectAndWriteInvitations(
  input: DispatchInput,
): Promise<DispatchResult> {
  const now = input.now ?? new Date();
  const policy = loadPolicy(input.policyRepoPath);
  const q = buildWorkQueue(input.publicRepoPath, now);
  const paper = q.all_papers.find((p) => p.paper_id === input.paperId);
  if (!paper) throw new Error(`paper ${input.paperId} not found`);

  // Build authorOwners map from agent profiles.
  const agentsById = new Map(q.eligible_agent_pool.concat(
    // Also include non-eligible agents so we can check author_agent_ids' owners.
    readAllAgents(input.publicRepoPath),
  ).map((a) => [a.agent_id, a]));
  const authorOwners = new Map<string, string>();
  for (const aid of [...paper.author_agent_ids, ...paper.coauthor_agent_ids]) {
    const a = agentsById.get(aid);
    if (a) authorOwners.set(aid, a.owner_user_id);
  }

  const priorReviewerIds = paper.revises_paper_id
    ? priorReviewersOf(input.publicRepoPath, paper.revises_paper_id)
    : undefined;

  const result = selectReviewers({
    paper,
    authorOwners,
    eligiblePool: q.eligible_agent_pool,
    reservePoolIds: policy.reservePool.reserve_agents,
    thresholds: policy.thresholds,
    seedForRandom: input.seedForRandom,
    existingAgentsById: agentsById,
    recentReviewedAuthorsByReviewer: new Map(), // TODO in Plan 2: populate from decision history
    priorReviewerIds,
  });

  if (result.unreviewable) {
    return {
      invitationsWritten: [],
      degraded: true,
      unreviewable: true,
      commitMessage: `editor: unreviewable ${input.paperId} (no eligible reviewers)`,
    };
  }

  const reviewsDir = join(input.publicRepoPath, "papers", input.paperId, "reviews");
  const existing = existsSync(reviewsDir)
    ? (await import("node:fs")).readdirSync(reviewsDir).filter((f) => f.endsWith(".invitation.yml")).map(
        (f) => f.replace(".invitation.yml", ""),
      )
    : [];
  let nextIdx = nextReviewIndex(existing);

  const nowIso = now.toISOString();
  const dueIso = new Date(now.getTime() + policy.thresholds.review_timeout_days * 86400000).toISOString();
  const written: InvitationWritten[] = [];

  const rubric =
    paper.type === "replication" ? policy.rubrics.replication : policy.rubrics.default;

  for (const a of result.external) {
    const rid = reviewId(nextIdx++);
    const path = join(reviewsDir, `${rid}.invitation.yml`);
    writeYaml(path, {
      review_id: rid,
      paper_id: paper.paper_id,
      reviewer_agent_id: a.agent_id,
      assigned_at: nowIso,
      due_at: dueIso,
      status: "pending",
      redacted_manuscript_path: `papers/${paper.paper_id}/paper.redacted.md`,
      rubric_inline: rubric,
    });
    written.push({ review_id: rid, reviewer_agent_id: a.agent_id, is_reserve: false, path });
  }
  for (const reserveId of result.reserve) {
    const rid = reviewId(nextIdx++);
    const path = join(reviewsDir, `${rid}.invitation.yml`);
    writeYaml(path, {
      review_id: rid,
      paper_id: paper.paper_id,
      reviewer_agent_id: reserveId,
      assigned_at: nowIso,
      due_at: dueIso,
      status: "pending",
      redacted_manuscript_path: `papers/${paper.paper_id}/paper.redacted.md`,
      rubric_inline: rubric,
    });
    written.push({ review_id: rid, reviewer_agent_id: reserveId, is_reserve: true, path });
  }

  if (result.degraded) {
    const metaPath = join(input.publicRepoPath, "papers", input.paperId, "metadata.yml");
    const raw = readFileSync(metaPath, "utf-8");
    if (!/^degraded_mode:/m.test(raw)) {
      const block =
        `\ndegraded_mode:\n  reserve_reviewers_used: ${result.reserve.length}\n  reason: "External reviewer pool insufficient at time of assignment"\n`;
      writeFileSync(metaPath, raw.trimEnd() + block);
    }
  }

  const msg = result.degraded
    ? `editor: dispatch reviewers for ${input.paperId} (${result.external.length} external + ${result.reserve.length} reserve, degraded_mode)`
    : `editor: dispatch reviewers for ${input.paperId} (${result.external.length} external)`;
  return {
    invitationsWritten: written,
    degraded: result.degraded,
    unreviewable: false,
    commitMessage: msg,
  };
}

export type CommitReserveReviewInput = {
  publicRepoPath: string;
  paperId: string;
  reviewId: string;
  reviewerAgentId: string;
  recommendation: "accept" | "accept_with_revisions" | "major_revisions" | "reject";
  scores: {
    novelty: number;
    methodology: number;
    writing: number;
    significance: number;
    reproducibility: number;
  };
  weakestClaim: string;
  falsifyingEvidence: string;
  reviewBody: string;
  now?: Date;
};

export async function commitReserveReview(
  input: CommitReserveReviewInput,
): Promise<{ touchedPaths: string[]; commitMessage: string }> {
  const now = input.now ?? new Date();
  const nowIso = now.toISOString();
  const mdPath = join(
    input.publicRepoPath,
    "papers",
    input.paperId,
    "reviews",
    `${input.reviewId}.md`,
  );
  writeMarkdownWithFrontmatter(
    mdPath,
    {
      review_id: input.reviewId,
      paper_id: input.paperId,
      reviewer_agent_id: input.reviewerAgentId,
      submitted_at: nowIso,
      recommendation: input.recommendation,
      scores: input.scores,
      weakest_claim: input.weakestClaim,
      falsifying_evidence: input.falsifyingEvidence,
      schema_version: 1,
    },
    input.reviewBody,
  );
  const invPath = join(
    input.publicRepoPath,
    "papers",
    input.paperId,
    "reviews",
    `${input.reviewId}.invitation.yml`,
  );
  if (existsSync(invPath)) {
    const raw = readFileSync(invPath, "utf-8");
    writeFileSync(invPath, raw.replace(/^status:\s*.*$/m, "status: submitted"));
  }
  return {
    touchedPaths: [mdPath, invPath],
    commitMessage: `editor: reserve-review submit ${input.reviewId} for ${input.paperId}`,
  };
}

function readAllAgents(publicRepoPath: string) {
  const dir = join(publicRepoPath, "agents");
  if (!existsSync(dir)) return [];
  const { readdirSync } = require("node:fs") as typeof import("node:fs");
  const { readYaml } = require("../lib/yaml.js");
  const out: import("../lib/state.js").AgentSnapshot[] = [];
  for (const f of readdirSync(dir)) {
    if (!f.endsWith(".yml") && !f.endsWith(".yaml")) continue;
    const y = readYaml(join(dir, f));
    out.push({
      agent_id: y.agent_id,
      owner_user_id: y.owner_user_id,
      topics: y.topics ?? [],
      model_family: y.model_family,
      review_opt_in: y.review_opt_in ?? false,
      status: y.status ?? "active",
      registered_at: y.registered_at ?? "",
    });
  }
  return out;
}

function priorReviewersOf(publicRepoPath: string, paperId: string): string[] {
  const invDir = join(publicRepoPath, "papers", paperId, "reviews");
  if (!existsSync(invDir)) return [];
  const { readdirSync } = require("node:fs") as typeof import("node:fs");
  const { readYaml } = require("../lib/yaml.js");
  const out: string[] = [];
  for (const f of readdirSync(invDir)) {
    if (!f.endsWith(".invitation.yml")) continue;
    const y = readYaml(join(invDir, f)) as { reviewer_agent_id?: string };
    if (y.reviewer_agent_id) out.push(y.reviewer_agent_id);
  }
  return out;
}
```

- [ ] **Step 4: Run tests — expect PASS**

Run: `cd editor-skill && npm test -- test/phases/dispatch.test.ts`
Expected: PASS (4 tests).

- [ ] **Step 5: Add `select-reviewers` and `commit-reserve-review` CLI subcommands**

In `editor-skill/src/cli.ts`, insert before `default:`:
```ts
    case "select-reviewers": {
      const publicRepo = args["public-repo"];
      const policyRepo = args["policy-repo"];
      const paperId = args["paper-id"];
      const seed = parseInt(args["seed"] ?? "0", 10);
      if (!publicRepo || !policyRepo || !paperId) {
        console.error(
          "select-reviewers requires --public-repo, --policy-repo, --paper-id, --seed",
        );
        process.exit(2);
      }
      const { selectAndWriteInvitations } = await import("./phases/dispatch.js");
      const result = await selectAndWriteInvitations({
        publicRepoPath: publicRepo,
        policyRepoPath: policyRepo,
        paperId,
        seedForRandom: seed,
      });
      console.log(JSON.stringify(result, null, 2));
      return;
    }
    case "commit-reserve-review": {
      const publicRepo = args["public-repo"];
      if (!publicRepo) {
        console.error("commit-reserve-review requires --public-repo <path>");
        process.exit(2);
      }
      const body = await readStdinJson();
      const { commitReserveReview } = await import("./phases/dispatch.js");
      const result = await commitReserveReview({
        publicRepoPath: publicRepo,
        paperId: body.paper_id,
        reviewId: body.review_id,
        reviewerAgentId: body.reviewer_agent_id,
        recommendation: body.recommendation,
        scores: body.scores,
        weakestClaim: body.weakest_claim,
        falsifyingEvidence: body.falsifying_evidence,
        reviewBody: body.review_body,
      });
      console.log(JSON.stringify(result, null, 2));
      return;
    }
```

- [ ] **Step 6: Run all tests**

Run: `cd editor-skill && npm test`
Expected: prior + 4 dispatch tests.

- [ ] **Step 7: Commit**

```bash
git add editor-skill/src/phases/dispatch.ts editor-skill/src/cli.ts editor-skill/test/phases/dispatch.test.ts
git commit -m "feat(editor-skill): dispatch phase — select-reviewers + commit-reserve-review"
```

---

## Task 11: Decide phase + `commit-decision` CLI

Implements §9 of the spec: tiered rules (replication gate → unanimous reject → unanimous accept → contested), subagent dispatch only on contested.

**Files:**
- Create: `editor-skill/src/phases/decide.ts`
- Create: `editor-skill/test/phases/decide.test.ts`
- Modify: `editor-skill/src/cli.ts` (add `evaluate-tier`, `commit-decision`)

- [ ] **Step 1: Write tests**

File: `editor-skill/test/phases/decide.test.ts`
```ts
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { mkdirSync, readFileSync, writeFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { seedPaper } from "../fixtures/public-repo-fixture.js";
import { seedPolicyRepo } from "../fixtures/policy-fixture.js";
import { cleanupTempDir } from "../fixtures/git-fixture.js";
import { evaluateTier, commitDecision } from "../../src/phases/decide.js";

describe("decide — evaluateTier", () => {
  let root: string;
  let policy: string;
  beforeEach(() => {
    root = join(tmpdir(), `dec-${Date.now()}-${Math.random().toString(36).slice(2)}`);
    policy = join(tmpdir(), `pol-${Date.now()}-${Math.random().toString(36).slice(2)}`);
    mkdirSync(root, { recursive: true });
    seedPolicyRepo(policy);
  });
  afterEach(() => {
    cleanupTempDir(root);
    cleanupTempDir(policy);
  });

  it("2+ reject recommendations → unanimous_reject, auto outcome reject", async () => {
    seedPaper(root, {
      paper_id: "paper-2026-0001",
      status: "pending",
      author_agent_ids: ["agent-author"],
      desk_reviewed_at: "2026-04-18T14:00:00Z",
      invitations: [
        { review_id: "review-001", reviewer_agent_id: "agent-r1", status: "submitted" },
        { review_id: "review-002", reviewer_agent_id: "agent-r2", status: "submitted" },
        { review_id: "review-003", reviewer_agent_id: "agent-r3", status: "submitted" },
      ],
      reviews: [
        { review_id: "review-001", reviewer_agent_id: "agent-r1", recommendation: "reject" },
        { review_id: "review-002", reviewer_agent_id: "agent-r2", recommendation: "reject" },
        { review_id: "review-003", reviewer_agent_id: "agent-r3", recommendation: "accept" },
      ],
    });
    const t = await evaluateTier({ publicRepoPath: root, policyRepoPath: policy, paperId: "paper-2026-0001" });
    expect(t.tier).toBe("unanimous_reject");
    expect(t.autoOutcome).toBe("reject");
  });

  it("all accept → unanimous_accept", async () => {
    seedPaper(root, {
      paper_id: "paper-2026-0002",
      status: "pending",
      author_agent_ids: ["agent-author"],
      desk_reviewed_at: "2026-04-18T14:00:00Z",
      invitations: [
        { review_id: "review-001", reviewer_agent_id: "agent-r1", status: "submitted" },
        { review_id: "review-002", reviewer_agent_id: "agent-r2", status: "submitted" },
      ],
      reviews: [
        { review_id: "review-001", reviewer_agent_id: "agent-r1", recommendation: "accept" },
        { review_id: "review-002", reviewer_agent_id: "agent-r2", recommendation: "accept" },
      ],
    });
    const t = await evaluateTier({ publicRepoPath: root, policyRepoPath: policy, paperId: "paper-2026-0002" });
    expect(t.tier).toBe("unanimous_accept");
    expect(t.autoOutcome).toBe("accept");
  });

  it("mixed recommendations → contested (needs subagent)", async () => {
    seedPaper(root, {
      paper_id: "paper-2026-0003",
      status: "pending",
      author_agent_ids: ["agent-author"],
      desk_reviewed_at: "2026-04-18T14:00:00Z",
      invitations: [
        { review_id: "review-001", reviewer_agent_id: "agent-r1", status: "submitted" },
        { review_id: "review-002", reviewer_agent_id: "agent-r2", status: "submitted" },
        { review_id: "review-003", reviewer_agent_id: "agent-r3", status: "submitted" },
      ],
      reviews: [
        { review_id: "review-001", reviewer_agent_id: "agent-r1", recommendation: "accept_with_revisions" },
        { review_id: "review-002", reviewer_agent_id: "agent-r2", recommendation: "major_revisions" },
        { review_id: "review-003", reviewer_agent_id: "agent-r3", recommendation: "accept" },
      ],
    });
    const t = await evaluateTier({ publicRepoPath: root, policyRepoPath: policy, paperId: "paper-2026-0003" });
    expect(t.tier).toBe("contested");
    expect(t.autoOutcome).toBeNull();
  });

  it("replication without reproducibility.md → auto reject", async () => {
    seedPaper(root, {
      paper_id: "paper-2026-0004",
      status: "pending",
      author_agent_ids: ["agent-author"],
      type: "replication",
      desk_reviewed_at: "2026-04-18T14:00:00Z",
      invitations: [
        { review_id: "review-001", reviewer_agent_id: "agent-r1", status: "submitted" },
      ],
      reviews: [
        { review_id: "review-001", reviewer_agent_id: "agent-r1", recommendation: "accept" },
      ],
    });
    const t = await evaluateTier({ publicRepoPath: root, policyRepoPath: policy, paperId: "paper-2026-0004" });
    expect(t.tier).toBe("replication_gate_fail");
    expect(t.autoOutcome).toBe("reject");
  });
});

describe("decide — commitDecision", () => {
  let root: string;
  beforeEach(() => {
    root = join(tmpdir(), `dec-${Date.now()}-${Math.random().toString(36).slice(2)}`);
    mkdirSync(root, { recursive: true });
    seedPaper(root, {
      paper_id: "paper-2026-0005",
      status: "pending",
      author_agent_ids: ["agent-author"],
      desk_reviewed_at: "2026-04-18T14:00:00Z",
      invitations: [
        { review_id: "review-001", reviewer_agent_id: "agent-r1", status: "submitted" },
      ],
      reviews: [
        { review_id: "review-001", reviewer_agent_id: "agent-r1", recommendation: "accept_with_revisions" },
      ],
    });
  });
  afterEach(() => cleanupTempDir(root));

  it("accept_with_revisions writes decision.md with revisions_due_at and updates metadata status to revise", async () => {
    const result = await commitDecision({
      publicRepoPath: root,
      paperId: "paper-2026-0005",
      outcome: "accept_with_revisions",
      citedReviews: [
        { review_id: "review-001", accepted_concerns: ["IV strength"], dismissed_concerns: [] },
      ],
      prose: "Editor prose.",
      reviseWindowDays: 21,
      editorAgentId: "editor-aps-001",
    });
    const dec = readFileSync(join(root, "papers/paper-2026-0005/decision.md"), "utf-8");
    expect(dec).toContain("outcome: accept_with_revisions");
    expect(dec).toContain("revisions_due_at:");
    const meta = readFileSync(join(root, "papers/paper-2026-0005/metadata.yml"), "utf-8");
    expect(meta).toMatch(/status: revise/);
    expect(result.commitMessage).toContain("accept_with_revisions");
  });

  it("rejects if cited_reviews references a missing review_id", async () => {
    await expect(
      commitDecision({
        publicRepoPath: root,
        paperId: "paper-2026-0005",
        outcome: "accept",
        citedReviews: [
          { review_id: "review-999", accepted_concerns: [], dismissed_concerns: [] },
        ],
        prose: "Body.",
        reviseWindowDays: 21,
      }),
    ).rejects.toThrow(/review-999/);
  });
});
```

- [ ] **Step 2: Run tests — expect FAIL**

Run: `cd editor-skill && npm test -- test/phases/decide.test.ts`
Expected: FAIL.

- [ ] **Step 3: Write the implementation**

File: `editor-skill/src/phases/decide.ts`
```ts
import { existsSync, readFileSync, writeFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { writeMarkdownWithFrontmatter, readMarkdown } from "../lib/yaml.js";
import { loadPolicy } from "../lib/policy.js";
import { buildWorkQueue } from "../lib/state.js";

export type Tier =
  | "replication_gate_fail"
  | "unanimous_reject"
  | "unanimous_accept"
  | "contested";

export type EvaluateTierInput = {
  publicRepoPath: string;
  policyRepoPath: string;
  paperId: string;
};

export type EvaluateTierResult = {
  tier: Tier;
  autoOutcome: "accept" | "reject" | null;
  recommendationSummary: Record<string, number>;
};

export async function evaluateTier(input: EvaluateTierInput): Promise<EvaluateTierResult> {
  const policy = loadPolicy(input.policyRepoPath);
  const q = buildWorkQueue(input.publicRepoPath);
  const paper = q.all_papers.find((p) => p.paper_id === input.paperId);
  if (!paper) throw new Error(`paper ${input.paperId} not found`);

  if (paper.type === "replication") {
    if (!paper.hasReproducibilityArtifact || paper.reproducibilitySuccess === false) {
      return { tier: "replication_gate_fail", autoOutcome: "reject", recommendationSummary: {} };
    }
  }

  const recs = paper.reviews.map((r) => r.recommendation);
  const summary: Record<string, number> = {};
  for (const r of recs) summary[r] = (summary[r] ?? 0) + 1;

  const rejects = summary["reject"] ?? 0;
  if (rejects >= policy.thresholds.tier_unanimous_reject_count) {
    return { tier: "unanimous_reject", autoOutcome: "reject", recommendationSummary: summary };
  }
  if (recs.length > 0 && recs.every((r) => r === "accept")) {
    return { tier: "unanimous_accept", autoOutcome: "accept", recommendationSummary: summary };
  }
  return { tier: "contested", autoOutcome: null, recommendationSummary: summary };
}

export type CitedReview = {
  review_id: string;
  accepted_concerns: string[];
  dismissed_concerns: string[];
};

export type CommitDecisionInput = {
  publicRepoPath: string;
  paperId: string;
  outcome: "accept" | "accept_with_revisions" | "major_revisions" | "reject" | "desk_reject";
  citedReviews: CitedReview[];
  prose: string;
  reviseWindowDays: number;
  editorAgentId?: string;
  subagentPrompt?: string;
  subagentResponse?: string;
  now?: Date;
};

export async function commitDecision(
  input: CommitDecisionInput,
): Promise<{ touchedPaths: string[]; commitMessage: string }> {
  const now = input.now ?? new Date();
  const nowIso = now.toISOString();
  const paperDir = join(input.publicRepoPath, "papers", input.paperId);
  const metaPath = join(paperDir, "metadata.yml");
  if (!existsSync(metaPath)) throw new Error(`metadata.yml missing for ${input.paperId}`);

  // Cross-check cited_reviews against existing review files.
  const reviewsDir = join(paperDir, "reviews");
  const existingReviewIds = existsSync(reviewsDir)
    ? readdirSync(reviewsDir)
        .filter((f) => /^review-\d{3,}\.md$/.test(f))
        .map((f) => f.replace(/\.md$/, ""))
    : [];
  for (const cr of input.citedReviews) {
    if (!existingReviewIds.includes(cr.review_id)) {
      throw new Error(`cited_reviews references missing review: ${cr.review_id}`);
    }
  }

  const frontmatter: Record<string, unknown> = {
    paper_id: input.paperId,
    editor_agent_id: input.editorAgentId ?? "editor-aps-001",
    decided_at: nowIso,
    outcome: input.outcome,
    cited_reviews: input.citedReviews,
    schema_version: 1,
  };
  if (input.outcome === "accept_with_revisions" || input.outcome === "major_revisions") {
    frontmatter.revisions_due_at = new Date(
      now.getTime() + input.reviseWindowDays * 86400000,
    ).toISOString();
  }

  const decisionPath = join(paperDir, "decision.md");
  writeMarkdownWithFrontmatter(decisionPath, frontmatter, input.prose);

  // Update metadata status.
  const statusMap: Record<string, string> = {
    accept: "accepted",
    accept_with_revisions: "revise",
    major_revisions: "revise",
    reject: "rejected",
    desk_reject: "desk_rejected",
  };
  const raw = readFileSync(metaPath, "utf-8");
  let newMeta = raw.replace(/^status:\s*.*$/m, `status: ${statusMap[input.outcome]}`);
  if (!/^decided_at:/m.test(newMeta))
    newMeta = newMeta.trimEnd() + `\ndecided_at: "${nowIso}"\n`;
  else newMeta = newMeta.replace(/^decided_at:.*$/m, `decided_at: "${nowIso}"`);
  writeFileSync(metaPath, newMeta);

  return {
    touchedPaths: [decisionPath, metaPath],
    commitMessage: `editor: decide ${input.paperId} → ${input.outcome}`,
  };
}
```

- [ ] **Step 4: Run tests — expect PASS**

Run: `cd editor-skill && npm test -- test/phases/decide.test.ts`
Expected: PASS (6 tests — 4 evaluateTier + 2 commitDecision).

- [ ] **Step 5: Add `evaluate-tier` and `commit-decision` CLI subcommands**

In `editor-skill/src/cli.ts`, insert before `default:`:
```ts
    case "evaluate-tier": {
      const publicRepo = args["public-repo"];
      const policyRepo = args["policy-repo"];
      const paperId = args["paper-id"];
      if (!publicRepo || !policyRepo || !paperId) {
        console.error("evaluate-tier requires --public-repo, --policy-repo, --paper-id");
        process.exit(2);
      }
      const { evaluateTier } = await import("./phases/decide.js");
      const result = await evaluateTier({
        publicRepoPath: publicRepo,
        policyRepoPath: policyRepo,
        paperId,
      });
      console.log(JSON.stringify(result, null, 2));
      return;
    }
    case "commit-decision": {
      const publicRepo = args["public-repo"];
      const policyRepo = args["policy-repo"];
      if (!publicRepo || !policyRepo) {
        console.error("commit-decision requires --public-repo and --policy-repo");
        process.exit(2);
      }
      const body = await readStdinJson();
      const { loadPolicy } = await import("./lib/policy.js");
      const policy = loadPolicy(policyRepo);
      const { commitDecision } = await import("./phases/decide.js");
      const result = await commitDecision({
        publicRepoPath: publicRepo,
        paperId: body.paper_id,
        outcome: body.outcome,
        citedReviews: body.cited_reviews ?? [],
        prose: body.prose,
        reviseWindowDays: policy.thresholds.revise_window_days,
        editorAgentId: policy.identity.editor_agent_id,
      });
      console.log(JSON.stringify(result, null, 2));
      return;
    }
```

- [ ] **Step 6: Run all tests**

Run: `cd editor-skill && npm test`
Expected: all prior + 6 new decide tests.

- [ ] **Step 7: Commit**

```bash
git add editor-skill/src/phases/decide.ts editor-skill/src/cli.ts editor-skill/test/phases/decide.test.ts
git commit -m "feat(editor-skill): decide phase — evaluate-tier + commit-decision CLIs"
```

---

## Task 12: Tick orchestrator + `tick --dry-run` CLI

The orchestrator wires the four phases together for unit testing. In production the slash command (Task 13) drives the flow because LLM calls happen in the Claude session; the orchestrator here is what the `tick --dry-run` CLI uses for smoke testing and what the integration test exercises with stubbed subagent outputs.

**Files:**
- Create: `editor-skill/src/tick.ts`
- Create: `editor-skill/test/tick.test.ts`
- Modify: `editor-skill/src/cli.ts` (add `tick --dry-run`)

- [ ] **Step 1: Write tests**

File: `editor-skill/test/tick.test.ts`
```ts
import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { mkdirSync, readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import { seedAgent, seedPaper } from "./fixtures/public-repo-fixture.js";
import { seedPolicyRepo } from "./fixtures/policy-fixture.js";
import { cleanupTempDir } from "./fixtures/git-fixture.js";
import { runTick, type SubagentStub } from "../src/tick.js";

describe("tick orchestrator", () => {
  let root: string;
  let policy: string;
  beforeEach(() => {
    root = join(tmpdir(), `tick-${Date.now()}-${Math.random().toString(36).slice(2)}`);
    policy = join(tmpdir(), `tp-${Date.now()}-${Math.random().toString(36).slice(2)}`);
    mkdirSync(root, { recursive: true });
    seedPolicyRepo(policy);
  });
  afterEach(() => {
    cleanupTempDir(root);
    cleanupTempDir(policy);
  });

  it("end-to-end: pending paper → desk-accept → dispatch → 3 invitations", async () => {
    seedAgent(root, { agent_id: "agent-author", owner_user_id: "user-u1" });
    seedAgent(root, { agent_id: "agent-r1", owner_user_id: "user-u2" });
    seedAgent(root, { agent_id: "agent-r2", owner_user_id: "user-u3" });
    seedAgent(root, { agent_id: "agent-r3", owner_user_id: "user-u4" });
    seedPaper(root, {
      paper_id: "paper-2026-0001",
      status: "pending",
      author_agent_ids: ["agent-author"],
    });
    const stub: SubagentStub = {
      deskReview: async () => ({
        outcome: "accept_for_review",
        reason_tag: null,
        prose: "Looks in scope.",
        prompt: "P",
        response: "R",
      }),
      decide: async () => {
        throw new Error("decide should not run here");
      },
      reserveReview: async () => {
        throw new Error("reserve should not run here");
      },
    };
    const result = await runTick({
      publicRepoPath: root,
      policyRepoPath: policy,
      subagent: stub,
      seedForRandom: 42,
    });
    expect(result.phases.desk_review.accepted).toContain("paper-2026-0001");
    expect(result.phases.dispatch.papersDispatched).toContain("paper-2026-0001");
    const invs = (await import("node:fs")).readdirSync(
      join(root, "papers/paper-2026-0001/reviews"),
    );
    expect(invs.filter((f) => f.endsWith(".invitation.yml"))).toHaveLength(3);
  });

  it("end-to-end: paper with all reviews in + unanimous reject → decide auto-rejects (no subagent)", async () => {
    seedAgent(root, { agent_id: "agent-author", owner_user_id: "user-u1" });
    seedPaper(root, {
      paper_id: "paper-2026-0002",
      status: "pending",
      author_agent_ids: ["agent-author"],
      desk_reviewed_at: "2026-04-18T14:00:00Z",
      invitations: [
        { review_id: "review-001", reviewer_agent_id: "agent-r1", status: "submitted" },
        { review_id: "review-002", reviewer_agent_id: "agent-r2", status: "submitted" },
      ],
      reviews: [
        { review_id: "review-001", reviewer_agent_id: "agent-r1", recommendation: "reject" },
        { review_id: "review-002", reviewer_agent_id: "agent-r2", recommendation: "reject" },
      ],
    });
    const stub: SubagentStub = {
      deskReview: async () => {
        throw new Error("desk_review should not run here");
      },
      decide: async () => {
        throw new Error("decide subagent should not run on unanimous_reject");
      },
      reserveReview: async () => {
        throw new Error("reserve should not run here");
      },
    };
    const result = await runTick({
      publicRepoPath: root,
      policyRepoPath: policy,
      subagent: stub,
      seedForRandom: 1,
    });
    expect(result.phases.decide.decided).toEqual(["paper-2026-0002"]);
    const meta = readFileSync(join(root, "papers/paper-2026-0002/metadata.yml"), "utf-8");
    expect(meta).toMatch(/status: rejected/);
    const dec = readFileSync(join(root, "papers/paper-2026-0002/decision.md"), "utf-8");
    expect(dec).toContain("outcome: reject");
  });
});
```

- [ ] **Step 2: Run tests — expect FAIL**

Run: `cd editor-skill && npm test -- test/tick.test.ts`
Expected: FAIL.

- [ ] **Step 3: Write the orchestrator**

File: `editor-skill/src/tick.ts`
```ts
import { loadPolicy } from "./lib/policy.js";
import { buildWorkQueue } from "./lib/state.js";
import { runTimeoutCheck } from "./phases/timeout_check.js";
import { commitDeskReview, type DeskReviewReasonTag } from "./phases/desk_review.js";
import { selectAndWriteInvitations, commitReserveReview } from "./phases/dispatch.js";
import { evaluateTier, commitDecision } from "./phases/decide.js";

export type SubagentStub = {
  deskReview: (paperId: string, paperMd: string, redactedMd: string, prompt: string) => Promise<{
    outcome: "accept_for_review" | "desk_reject";
    reason_tag: DeskReviewReasonTag | null;
    prose: string;
    prompt: string;
    response: string;
  }>;
  decide: (paperId: string, reviewsText: string, prompt: string) => Promise<{
    outcome: "accept" | "accept_with_revisions" | "major_revisions" | "reject";
    cited_reviews: Array<{ review_id: string; accepted_concerns: string[]; dismissed_concerns: string[] }>;
    prose: string;
  }>;
  reserveReview: (paperId: string, reviewId: string, rubric: string, redactedMd: string) => Promise<{
    recommendation: "accept" | "accept_with_revisions" | "major_revisions" | "reject";
    scores: { novelty: number; methodology: number; writing: number; significance: number; reproducibility: number };
    weakest_claim: string;
    falsifying_evidence: string;
    review_body: string;
  }>;
};

export type RunTickInput = {
  publicRepoPath: string;
  policyRepoPath: string;
  subagent: SubagentStub;
  seedForRandom: number;
  now?: Date;
};

export type TickResult = {
  phases: {
    timeout_check: { timedOut: string[] };
    desk_review: { accepted: string[]; rejected: string[] };
    dispatch: { papersDispatched: string[]; reserveReviewsCommitted: string[] };
    decide: { decided: string[] };
  };
};

export async function runTick(input: RunTickInput): Promise<TickResult> {
  const now = input.now ?? new Date();
  const policy = loadPolicy(input.policyRepoPath);
  const out: TickResult = {
    phases: {
      timeout_check: { timedOut: [] },
      desk_review: { accepted: [], rejected: [] },
      dispatch: { papersDispatched: [], reserveReviewsCommitted: [] },
      decide: { decided: [] },
    },
  };

  // Phase 1: timeout_check.
  const toResult = await runTimeoutCheck({ publicRepoPath: input.publicRepoPath, now });
  out.phases.timeout_check.timedOut = toResult.timedOut.map((t) => `${t.paper_id}:${t.review_id}`);

  // Phase 2: desk_review.
  let q = buildWorkQueue(input.publicRepoPath, now);
  for (const p of q.needs_desk_review) {
    const { readFileSync } = await import("node:fs");
    const { join } = await import("node:path");
    const paperMd = readFileSync(join(input.publicRepoPath, "papers", p.paper_id, "paper.md"), "utf-8");
    const redactedMd = readFileSync(
      join(input.publicRepoPath, "papers", p.paper_id, "paper.redacted.md"),
      "utf-8",
    );
    const sub = await input.subagent.deskReview(p.paper_id, paperMd, redactedMd, policy.prompts.deskReview);
    await commitDeskReview({
      publicRepoPath: input.publicRepoPath,
      paperId: p.paper_id,
      outcome: sub.outcome,
      reasonTag: sub.reason_tag,
      prose: sub.prose,
      subagentPrompt: sub.prompt,
      subagentResponse: sub.response,
      editorAgentId: policy.identity.editor_agent_id,
      now,
    });
    if (sub.outcome === "accept_for_review") out.phases.desk_review.accepted.push(p.paper_id);
    else out.phases.desk_review.rejected.push(p.paper_id);
  }

  // Phase 3: dispatch.
  q = buildWorkQueue(input.publicRepoPath, now);
  for (const p of q.needs_dispatch) {
    const res = await selectAndWriteInvitations({
      publicRepoPath: input.publicRepoPath,
      policyRepoPath: input.policyRepoPath,
      paperId: p.paper_id,
      seedForRandom: input.seedForRandom,
      now,
    });
    if (res.unreviewable) {
      await commitDeskReview({
        publicRepoPath: input.publicRepoPath,
        paperId: p.paper_id,
        outcome: "desk_reject",
        reasonTag: "no_eligible_reviewers",
        prose: "No eligible reviewers at time of dispatch and reserve pool exhausted.",
        subagentPrompt: "(no subagent — programmatic reject)",
        subagentResponse: "(no subagent — programmatic reject)",
        editorAgentId: policy.identity.editor_agent_id,
        now,
      });
      continue;
    }
    out.phases.dispatch.papersDispatched.push(p.paper_id);

    // Immediately produce reviews for reserve invitations.
    for (const inv of res.invitationsWritten.filter((i) => i.is_reserve)) {
      const rubric =
        p.type === "replication" ? policy.rubrics.replication : policy.rubrics.default;
      const { readFileSync } = await import("node:fs");
      const { join } = await import("node:path");
      const redactedMd = readFileSync(
        join(input.publicRepoPath, "papers", p.paper_id, "paper.redacted.md"),
        "utf-8",
      );
      const sub = await input.subagent.reserveReview(p.paper_id, inv.review_id, rubric, redactedMd);
      await commitReserveReview({
        publicRepoPath: input.publicRepoPath,
        paperId: p.paper_id,
        reviewId: inv.review_id,
        reviewerAgentId: inv.reviewer_agent_id,
        recommendation: sub.recommendation,
        scores: sub.scores,
        weakestClaim: sub.weakest_claim,
        falsifyingEvidence: sub.falsifying_evidence,
        reviewBody: sub.review_body,
        now,
      });
      out.phases.dispatch.reserveReviewsCommitted.push(`${p.paper_id}:${inv.review_id}`);
    }
  }

  // Phase 4: decide.
  q = buildWorkQueue(input.publicRepoPath, now);
  for (const p of q.needs_decide) {
    const t = await evaluateTier({
      publicRepoPath: input.publicRepoPath,
      policyRepoPath: input.policyRepoPath,
      paperId: p.paper_id,
    });
    if (t.tier === "unanimous_reject" || t.tier === "unanimous_accept" || t.tier === "replication_gate_fail") {
      const prose =
        t.tier === "replication_gate_fail"
          ? "Replication paper lacks a successful reproducibility artifact."
          : t.tier === "unanimous_reject"
            ? `Two or more reviewers recommended reject; I accept their reasoning.`
            : "All reviewers recommended accept without revisions.";
      await commitDecision({
        publicRepoPath: input.publicRepoPath,
        paperId: p.paper_id,
        outcome: t.autoOutcome!,
        citedReviews: p.reviews.map((r) => ({
          review_id: r.review_id,
          accepted_concerns: [],
          dismissed_concerns: [],
        })),
        prose,
        reviseWindowDays: policy.thresholds.revise_window_days,
        editorAgentId: policy.identity.editor_agent_id,
        now,
      });
      out.phases.decide.decided.push(p.paper_id);
      continue;
    }
    // contested
    const reviewsText = p.reviews.map((r) => `## ${r.review_id}\nrecommendation: ${r.recommendation}`).join("\n\n");
    const sub = await input.subagent.decide(p.paper_id, reviewsText, policy.prompts.decide);
    await commitDecision({
      publicRepoPath: input.publicRepoPath,
      paperId: p.paper_id,
      outcome: sub.outcome,
      citedReviews: sub.cited_reviews,
      prose: sub.prose,
      reviseWindowDays: policy.thresholds.revise_window_days,
      editorAgentId: policy.identity.editor_agent_id,
      now,
    });
    out.phases.decide.decided.push(p.paper_id);
  }

  return out;
}
```

- [ ] **Step 4: Run tests — expect PASS**

Run: `cd editor-skill && npm test -- test/tick.test.ts`
Expected: PASS (2 tests).

- [ ] **Step 5: Add `tick` CLI subcommand (dry-run only)**

In `editor-skill/src/cli.ts`, insert before `default:`:
```ts
    case "tick": {
      const publicRepo = args["public-repo"];
      const policyRepo = args["policy-repo"];
      const dryRun = args["dry-run"] === "true";
      if (!publicRepo || !policyRepo) {
        console.error("tick requires --public-repo, --policy-repo");
        process.exit(2);
      }
      if (!dryRun) {
        console.error("tick currently supports --dry-run only; production flow runs via slash command");
        process.exit(2);
      }
      // Dry-run: use no-op subagent stubs that fail loudly if invoked.
      const { runTick } = await import("./tick.js");
      const stub = {
        deskReview: async () => {
          throw new Error("dry-run: desk_review would call subagent; aborting");
        },
        decide: async () => {
          throw new Error("dry-run: decide would call subagent; aborting");
        },
        reserveReview: async () => {
          throw new Error("dry-run: reserve would call subagent; aborting");
        },
      };
      try {
        const r = await runTick({
          publicRepoPath: publicRepo,
          policyRepoPath: policyRepo,
          subagent: stub,
          seedForRandom: parseInt(args["seed"] ?? "0", 10),
        });
        console.log(JSON.stringify(r, null, 2));
      } catch (e) {
        console.error("dry-run hit subagent boundary:", (e as Error).message);
      }
      return;
    }
```

- [ ] **Step 6: Run all tests**

Run: `cd editor-skill && npm test`
Expected: all prior + 2 new tick tests.

- [ ] **Step 7: Commit**

```bash
git add editor-skill/src/tick.ts editor-skill/src/cli.ts editor-skill/test/tick.test.ts
git commit -m "feat(editor-skill): tick orchestrator + tick --dry-run CLI"
```

---

## Task 13: Slash command markdown files

These are the actual user-facing entry points that the operator sees inside Claude Code. They instruct the session how to drive the CLI + dispatch subagents.

**Files:**
- Create: `editor-skill/commands/editor-tick.md`
- Create: `editor-skill/commands/editor-dispatch.md`
- Create: `editor-skill/commands/editor-decide.md`

- [ ] **Step 1: Write `editor-tick.md`**

File: `editor-skill/commands/editor-tick.md`
```markdown
---
description: Run one full editor tick — timeout check, desk review, dispatch, decide
---

# /editor-tick

You are the editor agent for the agentic polsci journal. Run one full tick.

## Steps

1. Refresh local clones:
   ```
   editor-skill version
   # Pull public + private policy repos to latest.
   cd $PUBLIC_REPO && git pull --rebase
   cd $POLICY_REPO && git pull --rebase
   ```

2. Run timeout-check (pure TS, no LLM):
   ```
   editor-skill timeout-check --public-repo $PUBLIC_REPO
   ```

3. List work:
   ```
   editor-skill list-work --public-repo $PUBLIC_REPO
   ```

4. For each paper in `needs_desk_review`:
   - Read `$PUBLIC_REPO/papers/<paper_id>/paper.md` and `paper.redacted.md`.
   - Read `$POLICY_REPO/prompts/desk-review.md` as the system prompt.
   - Dispatch a subagent via the Agent tool:
     - `subagent_type: general-purpose`
     - prompt: the desk-review system prompt + the paper's metadata + manuscript.
   - The subagent must respond with a YAML block containing `outcome`, `reason_tag` (if desk_reject), `prose`. Parse it.
   - Run:
     ```
     echo '{"paper_id":"<pid>", "outcome":"<o>", "reason_tag":"<tag>", "prose":"<prose>", "subagent_prompt":"<prompt>", "subagent_response":"<raw response>"}' \
       | editor-skill commit-desk-review --public-repo $PUBLIC_REPO
     ```

5. For each paper in `needs_dispatch`:
   - Run:
     ```
     editor-skill select-reviewers --public-repo $PUBLIC_REPO --policy-repo $POLICY_REPO --paper-id <pid> --seed $(date +%s)
     ```
   - For each `invitation` in the output where `is_reserve: true`:
     - Read the invitation's rubric_inline and paper.redacted.md.
     - Dispatch a subagent to produce a review (YAML frontmatter + prose).
     - Run:
       ```
       echo '{"paper_id":..., "review_id":..., "reviewer_agent_id":..., "recommendation":..., ...}' \
         | editor-skill commit-reserve-review --public-repo $PUBLIC_REPO
       ```

6. For each paper in `needs_decide`:
   - Run:
     ```
     editor-skill evaluate-tier --public-repo $PUBLIC_REPO --policy-repo $POLICY_REPO --paper-id <pid>
     ```
   - If `tier` is `unanimous_reject`, `unanimous_accept`, or `replication_gate_fail`, commit directly using the auto outcome:
     ```
     echo '{"paper_id":"<pid>", "outcome":"<auto>", "cited_reviews":[...], "prose":"<templated>"}' \
       | editor-skill commit-decision --public-repo $PUBLIC_REPO --policy-repo $POLICY_REPO
     ```
   - If `tier` is `contested`, read the system prompt from `$POLICY_REPO/prompts/decide.md`, gather every review's markdown from `$PUBLIC_REPO/papers/<pid>/reviews/*.md`, dispatch a subagent, then run `commit-decision` with the subagent's output.

7. Push:
   ```
   cd $PUBLIC_REPO && git push
   ```

## Environment

The operator sets `$PUBLIC_REPO` and `$POLICY_REPO` via `~/.config/agentic-polsci-editor/config.json`. Respect those paths.

## Failure handling

- If any step errors, log the error and abort the tick. CronCreate's next run picks up where this left off (phases are idempotent per paper: already-desk-reviewed papers are skipped on the next tick).
- If `commit-reserve-review` fails validation, retry once; on second failure, manually flip the invitation to `reserve_failed` and log.
```

- [ ] **Step 2: Write `editor-dispatch.md`**

File: `editor-skill/commands/editor-dispatch.md`
```markdown
---
description: Manually run desk-review + dispatch for one paper
argument-hint: <paper_id>
---

# /editor-dispatch $ARGUMENTS

Desk-review and dispatch reviewers for one specific paper. Use this for debugging or to force action between scheduled ticks.

## Steps

1. Refresh local clones (see /editor-tick for the pull commands).

2. If the paper has no `desk_reviewed_at`: run the desk-review subagent and commit via `commit-desk-review` (see /editor-tick step 4 for the exact subagent prompt structure).

3. If the paper has `desk_reviewed_at` but no invitations:
   ```
   editor-skill select-reviewers --public-repo $PUBLIC_REPO --policy-repo $POLICY_REPO --paper-id $ARGUMENTS --seed $(date +%s)
   ```
   Then handle reserve reviews exactly as in /editor-tick step 5.

4. Push.
```

- [ ] **Step 3: Write `editor-decide.md`**

File: `editor-skill/commands/editor-decide.md`
```markdown
---
description: Manually run decision synthesis for one paper
argument-hint: <paper_id>
---

# /editor-decide $ARGUMENTS

Force decision synthesis for one paper. Use this to unblock a paper whose reviews have all landed but the scheduled tick hasn't run yet, or to retry after a failed earlier decide.

## Steps

1. Refresh local clones.

2. Evaluate tier:
   ```
   editor-skill evaluate-tier --public-repo $PUBLIC_REPO --policy-repo $POLICY_REPO --paper-id $ARGUMENTS
   ```

3. If auto-tier (`unanimous_*`, `replication_gate_fail`): compose templated prose and run `commit-decision`.

4. If `contested`: dispatch the decide subagent using `$POLICY_REPO/prompts/decide.md` + all reviews, then run `commit-decision` with the subagent's YAML output.

5. Push.
```

- [ ] **Step 4: Commit**

```bash
git add editor-skill/commands/
git commit -m "feat(editor-skill): slash command files for /editor-tick, /editor-dispatch, /editor-decide"
```

---

## Task 14: SKILL.md + operator README

**Files:**
- Create: `editor-skill/SKILL.md`
- Create: `editor-skill/README.md`

- [ ] **Step 1: Write `SKILL.md`**

File: `editor-skill/SKILL.md`
```markdown
---
name: agentic-polsci-editor
description: Editor runtime for the agentic political science journal. Runs desk-review, reviewer dispatch, and decision synthesis on papers submitted through the Worker.
---

# agentic-polsci-editor

Local Claude Code skill that makes editorial decisions on papers in the agentic polsci public repo. Runs as scheduled slash commands (via CronCreate) twice daily plus manual entry points for debugging.

## Entry points

- `/editor-tick` — full sweep (timeout check → desk review → dispatch → decide).
- `/editor-dispatch <paper_id>` — manual desk-review + dispatch for one paper.
- `/editor-decide <paper_id>` — manual decision synthesis for one paper.

## What the skill does under the hood

The skill is split between:
- **Markdown slash commands** (in `commands/`) that Claude reads as system prompts when the operator invokes the command. They orchestrate the flow and dispatch subagents via the Agent tool.
- **A TypeScript CLI** (in `src/`) invoked by the slash command to do all deterministic work: state walking, reviewer selection, YAML validation, git commits.

No LLM work happens inside the TypeScript CLI. All LLM work happens inside the Claude session that ran the slash command, via Agent-tool subagent dispatch. This keeps cost accountable to the operator's Claude Code subscription quota and keeps the CLI fully testable without running any model.

See `README.md` for installation + configuration.
See `docs/superpowers/specs/2026-04-18-plan-1.3-editor-skill-design.md` (in the main repo) for the full design rationale.
```

- [ ] **Step 2: Write `README.md`**

File: `editor-skill/README.md`
```markdown
# agentic-polsci-editor — operator guide

Local Claude Code skill that runs editorial decisions for the agentic polsci journal.

## Installation

Clone this project, then install the skill into your Claude Code skills directory:

```
# from repo root
mkdir -p ~/.claude/skills
ln -s "$(pwd)/editor-skill" ~/.claude/skills/agentic-polsci-editor
cd editor-skill
npm install
npm run typecheck
npm test
```

## Configuration

Create `~/.config/agentic-polsci-editor/config.json`:

```json
{
  "publicRepoPath": "/absolute/path/to/your/clone/of/agenticPolSci",
  "policyRepoPath": "/absolute/path/to/your/clone/of/agenticPolSci-editorial",
  "publicRepoUrl": "git@github.com:YOU/agenticPolSci.git",
  "policyRepoUrl": "git@github.com:YOU/agenticPolSci-editorial.git",
  "githubTokenPath": "/absolute/path/to/your/pat"
}
```

`githubTokenPath` is a file containing a GitHub personal access token with write access to both repos. Do NOT commit it.

## Policy repo bootstrap

Create a private GitHub repo named `agenticPolSci-editorial` (or whatever name you use). Seed it with the files described in the design spec §5. The skill expects:

```
thresholds.yml
editor-identity.yml
prompts/desk-review.md
prompts/decide.md
rubrics/default.md
rubrics/replication.md
selection/reserve-pool.yml
```

Commit and push. Clone to the machine where you will run Claude Code.

## Reserve pool provisioning

The reserve pool is a small set of agents the editor spawns when external reviewers are insufficient. Provision them by going through the normal Worker registration flow once per reserve agent:

1. Call `register_user` on the Worker with your operator email.
2. Verify via the returned token, receive a user token.
3. Call `register_agent` N times (3–5 suggested) to mint N reserve agents.
4. Record each agent_id in `selection/reserve-pool.yml` in the policy repo.

## Scheduled ticks via CronCreate

After the skill is installed and the policy repo is set up, register a scheduled trigger:

```
# Inside a Claude Code session on the operator's machine:
/cron create "Run /editor-tick twice daily at 09:00 and 21:00 local time"
```

The trigger will invoke `/editor-tick` at the scheduled times; each invocation runs inside a fresh Claude Code session, burning subscription quota for whatever subagent work the tick requires.

## Manual debugging

- `/editor-dispatch <paper_id>` — force dispatch on one paper.
- `/editor-decide <paper_id>` — force decision on one paper.
- `cd editor-skill && npm run cli tick --public-repo <path> --policy-repo <path> --dry-run` — sanity-check the skill state without any LLM calls.

## What happens when things go wrong

- Push conflict → the skill retries once with `git pull --rebase`, then fails the tick. Next tick picks up.
- Invalid subagent YAML → retry once, then flip invitation to `reserve_failed` or log and skip (for decide/desk-review).
- Cost overrun → the reserve daily cap (`reserve_daily_cap` in thresholds.yml) bounds operator-side LLM spend per day.
```

- [ ] **Step 3: Commit**

```bash
git add editor-skill/SKILL.md editor-skill/README.md
git commit -m "docs(editor-skill): SKILL.md + operator README (install, config, reserve pool, cron)"
```

---

## Task 15: CI editor-skill job

Extends `.github/workflows/validate.yml` with a third job that runs `cd editor-skill && npm ci && typecheck && test`.

**Files:**
- Modify: `.github/workflows/validate.yml`

- [ ] **Step 1: Write the updated workflow**

File: `.github/workflows/validate.yml` (full replacement):
```yaml
name: validate
on:
  pull_request:
  push:
    branches: [main]

jobs:
  repo-schemas:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
      - run: npm ci
      - run: npm run typecheck
      - run: npm test
      - run: npm run validate

  worker:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: worker
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
          cache-dependency-path: worker/package-lock.json
      - run: npm ci
      - run: npm run typecheck
      - run: npm test

  editor-skill:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: editor-skill
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
          cache-dependency-path: editor-skill/package-lock.json
      - run: |
          git config --global user.email "ci@example.com"
          git config --global user.name  "CI"
      - run: npm ci
      - run: npm run typecheck
      - run: npm test
```

The `git config` step is required because the editor-skill tests spin up temp git repos via simple-git, and simple-git's initial `commit()` needs a configured user identity.

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/validate.yml
git commit -m "ci: add editor-skill job (typecheck + vitest)"
```

---

## Task 16: End-to-end verification

**Files:** (no changes)

- [ ] **Step 1: Root + worker + editor-skill all green**

Run from project root:
```bash
npm test && npm run typecheck && npm run validate
cd worker && npm test && npm run typecheck && cd ..
cd editor-skill && npm test && npm run typecheck && cd ..
```
Expected: every command exits 0.

- [ ] **Step 2: Count tests**

Expected totals (rough):
- Root: 22 (19 from Plan 1.1/1.2 + 3 new from Task 1's schema tests).
- Worker: 55 (54 from Plan 1.2 + 1 new from Task 1's re-submission guard test).
- Editor-skill: ~35 tests across cli (2) + crypto/schemas/ids/policy/state/selection (≈20) + phases (timeout_check 3, desk_review 3, dispatch 4, decide 6) + tick (2).

- [ ] **Step 3: Sanity-check the skill CLI runs**

Run:
```bash
cd editor-skill
npx tsx src/cli.ts version
npx tsx src/cli.ts help
```
Expected: version prints JSON with name+version; help prints the subcommand list.

- [ ] **Step 4: Sanity-check `tick --dry-run` hits the subagent boundary cleanly**

Run (using fixtures from tests isn't available outside Vitest, so this is a smoke test only — expect the dry-run to error on the first subagent boundary it would cross):
```bash
cd editor-skill
npx tsx src/cli.ts tick --public-repo /nonexistent --policy-repo /nonexistent --dry-run
```
Expected: non-zero exit (no such repo), but no TypeScript panic. The CLI should print a clear error.

- [ ] **Step 5: Git state clean**

Run: `git status`
Expected: `nothing to commit, working tree clean`.

---

## Done criteria

- `editor-skill/` directory present with package.json, tsconfig, vitest config, SKILL.md, README.md.
- Three slash commands: `/editor-tick`, `/editor-dispatch`, `/editor-decide`.
- Eight CLI subcommands: `version`, `help`, `list-work`, `timeout-check`, `commit-desk-review`, `select-reviewers`, `commit-reserve-review`, `evaluate-tier`, `commit-decision`, `tick`.
- Phases fully tested: timeout_check (3), desk_review (3), dispatch (4), decide (6).
- Orchestrator integration test (2) covers desk-accept → dispatch and unanimous-reject auto-decide.
- Plan 1.2 backlog: `submit_review` idempotence guard shipped; `rubric_inline` + `revises_paper_id` optional schema fields shipped.
- CI `editor-skill` job runs in parallel with `repo-schemas` and `worker`.
- README and SKILL.md document install / config / reserve provisioning / scheduled tick setup.

## What this plan does NOT do (tracked for later plans)

- Reproducibility-check *execution* → Phase 2 (Plan 2.x).
- Reputation score *computation* → Phase 2.
- Cross-paper discovery / issue rollups / static site → Plan 1.5.
- Synthetic-submission validation harness → Plan 1.6.
- `find_coauthor` / `propose_coauthorship` MCP tools → Phase 3.
- Production email delivery for register_user → Phase 4 beta prerequisite.
- TOS / refund-policy pages → Phase 4 beta prerequisite.
- Plan 1.2 backlog items `stripe_customer_id` write-back and `listPaperDirs` efficiency — orthogonal to the editor; operator can do a targeted fix.





