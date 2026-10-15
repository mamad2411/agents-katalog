---
name: gh-actions-build-trigger
description: GH Actions workflow triggering/monitoring gotchas for any repo with multiple workflows (e.g. APK + AAB builds). Use when a push to main did not seem to trigger a workflow, when only .github/** changed (paths filters skip it, needs manual dispatch), when parallel runs need one cancelled, when a build failed and the job log must be pulled, or when checking run status/artifacts. For the end-to-end Expo APK/AAB build flow use gh-actions-expo-apk-build instead.
---

# GH Actions build trigger

When a repo has several workflows (e.g. an APK workflow and an AAB workflow),
they **do not behave the same**. Know each one's auto-trigger and paths
filter before pushing:

| Workflow | Auto-trigger on push | Paths filter |
| --- | --- | --- |
| `build-apk.yml` (test APK) | ✅ every push to `main` | often none |
| `build-aab.yml` (store AAB) | ✅ push to `main` | often **only app source paths** (app/, components/, db/, hooks/, lib/, plugins/, types/, assets/, app.json, package*.json, patches/) — **NOT `.github/**`** |

Check the actual `paths:` / `paths-ignore:` in each workflow file — don't
assume.

## Steps

### 1. Decide which workflow(s) the request needs

APK for sideloading/testing, AAB for Play Store. If the user asks for one,
cancel the other — pushing to `main` may trigger **both** (the no-filter
workflow always runs). Never let a build the user did not ask for burn runner
time.

### 2. Check whether a push will trigger the workflow

A push that touches **only `.github/**`** (workflow files, etc.) does **NOT**
trigger a workflow whose paths filter omits `.github/**`. Pushing a
workflow-file-only commit will still trigger a workflow with **no** filter.
For the filtered workflow in that case, use a manual dispatch (step 3)
instead of expecting the push to fire it.

### 3. Trigger (manual dispatch when needed)

```bash
curl -s -o /dev/null -w "dispatch: HTTP %{http_code}\n" -X POST \
  -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/<owner>/<repo>/actions/workflows/<workflow-file>.yml/dispatches" \
  -d '{"ref":"main"}'
```

`204` = accepted. After dispatch (or a push), **runs can take several seconds
to appear in the API** — the first query right after a push may return an
empty list. Sleep ~5–10s and re-query before concluding "nothing triggered"
(a classic race).

### 4. Monitor the run

```bash
curl -s -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/<owner>/<repo>/actions/runs?per_page=5" \
  | node -e "const d=JSON.parse(require('fs').readFileSync(0,'utf8')); for (const r of d.workflow_runs||[]) console.log(r.id, r.name, r.head_sha.slice(0,7), r.status, r.conclusion, r.event)"
```

`conclusion: null` while running. If a run fails, pull the job log:

```bash
JOB_ID=$(curl -s -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/<owner>/<repo>/actions/runs/$RUN_ID/jobs" \
  | node -e "console.log(JSON.parse(require('fs').readFileSync(0,'utf8')).jobs[0].id)")
curl -sL -H "Authorization: Bearer $GH_TOKEN" \
  "https://api.github.com/repos/<owner>/<repo>/actions/jobs/$JOB_ID/logs" -o /tmp/job.log
```

Then grep the log for the failing step (e.g. `grep -B2 -A12 "error"` or look
for `##[error]` / `Process completed with exit code 1`).

### 5. Cancel an unneeded parallel run

```bash
curl -s -o /dev/null -w "cancel: HTTP %{http_code}\n" -X POST \
  -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/<owner>/<repo>/actions/runs/$RUN_ID/cancel"
```

`202` = accepted. Note: cancelling is async — the run may show as "cancelled"
only after the runner notices.

Completion criterion: the correct workflow(s) for the request are running on
the intended commit, unneeded parallel runs are cancelled, and you know the
run ID + URL to report. If a build failed, you can name the failing step and
the error.

## Reference

- Token: a `gh_token` is provided per session; export it as `GH_TOKEN` and
  never write it into files/commits.
- Artifacts are uploaded by `actions/upload-artifact@v4`; the artifact name
  and path are declared in the workflow's upload step.
- First build on a fresh runner takes ~15–25 min; cached ones are faster.
