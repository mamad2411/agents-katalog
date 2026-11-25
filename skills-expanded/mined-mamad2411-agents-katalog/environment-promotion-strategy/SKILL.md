---
name: environment-promotion-strategy
description: >
  Designs how a build/release is promoted through environments (dev,
  staging/QA, production, and optionally per-region or per-tenant tiers)
  with consistent gates, approvals, and configuration-per-environment
  handling. Use when the user asks to "design a promotion pipeline
  between environments," "add an approval gate before production," "keep
  dev/staging/prod config in sync without duplicating it," or "decide
  what has to pass before something reaches production."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: devops
  maturity: stable
---

# Environment Promotion Strategy

## Purpose

Most organizations run more than one environment (at minimum dev,
staging, production), and the central operational question is not "how do
we deploy" but "under what conditions does a given build move from one
environment to the next, and who/what decides." Without an explicit
promotion strategy, teams either promote too loosely (untested changes
reach production) or too rigidly (every environment requires a full manual
process, so releases queue up and batch into large, risky changes). This
skill covers designing the gates, approvals, and configuration handling
that make promotion both safe and fast enough to not become the
bottleneck.

## When to use

- Designing the environment topology and promotion flow for a new service
  or system (how many environments, what gates between each).
- Adding or tightening an approval gate before production (who approves,
  what evidence they see).
- Environment configuration (URLs, feature flags, resource sizing) is
  drifting or duplicated inconsistently across dev/staging/prod.
- Deciding whether the *same build artifact* should be promoted unchanged
  across environments, versus rebuilding per environment (it should
  almost always be the former).
- A production incident traces back to "it wasn't caught in staging" and
  the team needs to close that gap.
- Coordinating promotion across multiple services that must move through
  environments together (a release train) vs. independently.

## Prerequisites & environment

- A CI/CD pipeline capable of producing one immutable, versioned artifact
  per change (see
  [ci-cd-pipeline-design](../ci-cd-pipeline-design/SKILL.md) and
  [container-build-and-release](../container-build-and-release/SKILL.md))
  — promotion strategy assumes you're moving the *same* build forward,
  not rebuilding per environment (which reintroduces "works in staging,
  different bits in prod" risk).
- Defined environments with distinct purposes: at minimum, an environment
  for automated verification (dev/integration) and one that mirrors
  production closely enough to catch real issues (staging), before
  production itself. Extra tiers (per-region, per-tenant, canary-only)
  are added based on actual risk/scale needs, not by default.
- A configuration strategy that separates environment-specific values
  (URLs, resource limits, feature flags) from the artifact itself —
  environment variables, a config service, or per-environment
  `values.yaml`/`.tfvars` overlays, so the same build works unmodified in
  every environment.
- Platform support for approval gates: GitHub Environments (protection
  rules with required reviewers), GitLab `environment:` + manual jobs, or
  the GitOps operator's manual-sync setting (see
  [gitops-workflow](../gitops-workflow/SKILL.md)).

## Step-by-step guidance

1. **Define what each environment is for, explicitly**, and size gates
   accordingly:
   - **Dev/integration**: automated only, deploys on every merge to a
     shared branch, no approval — optimized for fast feedback, tolerant
     of instability.
   - **Staging/QA**: automated deploy, but gated on the full test suite
     (including integration/E2E) passing; may add manual exploratory
     testing or a stakeholder sign-off for higher-risk changes.
   - **Production**: gated on staging soak time, an explicit approval
     (human or automated canary analysis — see
     [blue-green-canary-deployments](../blue-green-canary-deployments/SKILL.md)),
     and typically a narrower deploy window/change process.

2. **Promote the artifact, not the source.** The same container
   image/package built once should flow through every environment
   unmodified; only configuration changes per environment. Concretely:
   version bump PRs (in a GitOps config repo) reference the same image
   digest/tag across `overlays/staging` and `overlays/prod` — only the
   overlay's environment-specific values differ.
   ```yaml
   # overlays/staging/kustomization.yaml
   images:
     - name: payments-api
       newTag: "1.4.2"
   configMapGenerator:
     - name: payments-api-config
       literals:
         - LOG_LEVEL=debug
         - EXTERNAL_API_URL=https://api.staging.example.com

   # overlays/prod/kustomization.yaml
   images:
     - name: payments-api
       newTag: "1.4.2"          # same tag as staging — same artifact
   configMapGenerator:
     - name: payments-api-config
       literals:
         - LOG_LEVEL=info
         - EXTERNAL_API_URL=https://api.example.com
   ```

3. **Define promotion criteria per gate explicitly**, not implicitly.
   Example criteria for staging → production promotion: all CI checks
   green, minimum soak time in staging (e.g., 24 hours or N business
   transactions observed with no new error-rate anomalies), no open
   Sev1/Sev2 incidents referencing the version, and required-reviewer
   approval recorded.

4. **Implement the gate mechanically**, don't rely on process memory.
   GitHub Actions example using environment protection + a required
   reviewer, chained after staging deploy:
   ```yaml
   deploy-staging:
     runs-on: ubuntu-latest
     environment: { name: staging }
     steps: [ ... ]

   deploy-production:
     needs: deploy-staging
     runs-on: ubuntu-latest
     environment:
       name: production      # configured in repo settings: required reviewers
     steps:
       - run: ./deploy.sh prod ${{ needs.deploy-staging.outputs.version }}
   ```
   The `production` GitHub Environment is configured (Settings →
   Environments → production → required reviewers) so the job literally
   cannot proceed without an approval click — the gate is enforced by the
   platform, not by a runbook step someone might skip.

5. **For multi-service releases, decide train vs. independent promotion
   explicitly.** If services must move together (tightly coupled API
   contracts), define a release train: a fixed cadence (e.g., weekly)
   where all participating services' latest verified builds promote
   together, with a clear cutoff for what makes the train. If services
   are independently deployable (preferred where contracts allow it),
   let each promote on its own schedule — this is almost always faster
   overall, since one slow/blocked service doesn't hold up others.

6. **Make promotion status visible.** A dashboard or simple report
   showing, per service, "what version is in each environment right now"
   avoids the common failure mode of nobody being sure whether staging
   and production have drifted apart. GitOps repos make this
   straightforward to derive (diff `overlays/staging` vs.
   `overlays/prod` image tags directly).

7. **Roll back by demoting**, using the same mechanism as promotion, not
   a special-case process — reverting the prod overlay's tag to the
   previous verified version and letting the ordinary deploy path apply
   it is more reliable than a bespoke "rollback script" maintained
   separately from the promotion path.

## Best practices

- Never let a hotfix skip environments "just this once" without an
  explicit, documented exception process — repeated exceptions quietly
  become the norm and erode the gate's value; if hotfixes routinely need
  to bypass staging, that's a signal staging's gate is too slow, not that
  bypassing is fine.
- Keep environment-specific configuration in overlays/config, not in
  conditional logic inside the application code (`if (env === 'prod')`)
  — the latter means you're never really testing the same code path that
  runs in production.
- Track lead time from "merged to main" to "in production" as a health
  metric for the promotion pipeline itself — if it's growing, find out
  which gate is the bottleneck rather than adding more gates on top.
- Require staging to be a reasonably faithful mirror of production
  (similar data shape/volume, same downstream service versions where
  feasible) — a staging environment too unlike production catches
  nothing and just adds latency for no safety benefit.
- Automate the "soak time" and metric-based promotion criteria where
  possible (canary analysis, automated smoke tests) rather than a fixed
  human "looks fine to me" check, which doesn't scale and is inconsistent
  across reviewers.
- Document the promotion policy itself (which gates exist, why, and who
  can override them) somewhere durable — a policy that lives only in
  institutional memory disappears with team turnover.

## Common pitfalls

- **Symptom:** A change passes staging cleanly but breaks in production.
  **Fix:** Audit for drift between staging and production beyond intended
  config differences — mismatched downstream service versions, different
  data volume/shape, or a feature flag that's off in staging but on in
  production (or vice versa) are common causes; close the specific gap
  found rather than generically "testing more."

- **Symptom:** Production and staging are running different versions and
  nobody can say for certain which, without checking manually.
  **Fix:** Adopt a GitOps config repo (see
  [gitops-workflow](../gitops-workflow/SKILL.md)) where each environment's
  deployed version is declared in a file, and build a simple report/diff
  across environment overlays rather than relying on tribal knowledge or
  `kubectl` spelunking.

- **Symptom:** Releases queue up because production approval is a
  scarce, slow human bottleneck (one person, infrequently available).
  **Fix:** Either widen the approver pool (multiple people/teams
  authorized to approve production promotions) or replace part of the
  manual gate with automated canary analysis so routine, low-risk changes
  don't require a human at all, reserving manual approval for
  higher-risk changes.

- **Symptom:** A hotfix was rebuilt directly against production
  configuration to "save time," bypassing the normal artifact-promotion
  path, and it later turns out staging never actually validated what's
  running in prod.
  **Fix:** Even for urgent fixes, build once and promote the same
  artifact through whatever gates can be compressed (fast-tracked review,
  shortened soak time) rather than skipping the pipeline and building a
  one-off artifact that was never validated anywhere else.

- **Symptom:** A multi-service release train regularly slips because one
  lagging service blocks the rest.
  **Fix:** Re-examine whether all services in the train genuinely need to
  move together — if their API contracts are versioned and
  backward-compatible, decouple them into independent promotion instead
  of a synchronized train.

## Worked example

**Scenario:** `payments-api` version `1.4.2` needs to move from a merge on
`main` to production, through dev → staging → production, with a release
train not required (this service promotes independently).

1. Merge to `main` triggers CI (per
   [ci-cd-pipeline-design](../ci-cd-pipeline-design/SKILL.md)): build,
   test, containerize, push `ghcr.io/example/payments-api:1.4.2`.
2. A pipeline job automatically bumps the `dev` overlay's tag to `1.4.2`
   and pushes; the GitOps operator deploys it within minutes — no
   approval required.
3. After dev smoke tests pass (automated), the same job opens a PR
   bumping the `staging` overlay to `1.4.2`. This PR is auto-merged since
   staging promotion criteria are "CI green" only.
4. `1.4.2` soaks in staging for the defined window (e.g., overnight);
   automated synthetic transactions and error-rate monitors confirm no
   regression.
5. A PR bumping the `prod` overlay to `1.4.2` is opened, referencing the
   staging soak evidence (linked dashboard) in its description. The
   `production` GitHub Environment requires one reviewer from the
   on-call rotation; they review the change, confirm the staging
   evidence, and approve.
6. Merging the PR triggers the GitOps operator (manual-sync mode for
   prod) to require an explicit `argocd app sync payments-api-prod`,
   executed by the same approver as a deliberate final step — completing
   promotion to production for the exact artifact that was built once in
   step 1 and never rebuilt.
7. If a regression appears post-promotion, rollback is a revert of the
   `prod` overlay bump PR (per
   [gitops-workflow](../gitops-workflow/SKILL.md)), demoting production
   back to `1.4.1` through the identical mechanism used to promote it.

## Cross-references

- [gitops-workflow](../gitops-workflow/SKILL.md)
- [ci-cd-pipeline-design](../ci-cd-pipeline-design/SKILL.md)
- [blue-green-canary-deployments](../blue-green-canary-deployments/SKILL.md)
