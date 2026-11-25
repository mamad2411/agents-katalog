---
name: oss-pr-landing
description: "A merge-rate-first contribution workflow: issue selection, minimal diffs, review follow-through. Use when contributing to someone else's repo, opening PRs upstream, or reviving stalled pull requests."
---
# Land merged PRs in large OSS repositories

> A merge-rate-first contribution workflow: issue selection, minimal diffs, review follow-through. Use when contributing to someone else's repo, opening PRs upstream, or reviving stalled pull requests.

**Track:** 🧭 Engineering Leadership · **Domain:** Open Source Stewardship · **Level:** intermediate · **~30 min**

**Who this is for:** Engineering Managers, Tech Leads, Staff Engineers, CTOs

## When to Use This Skill

A merge-rate-first contribution workflow: issue selection, minimal diffs, review follow-through. Use when contributing to someone else's repo, opening PRs upstream, or reviving stalled pull requests.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Pick labeled issues with recent maintainer activity; claim in a comment
2. Read CONTRIBUTING.md, AGENTS.md, and ten recent merged commits first
3. Branch per issue; one logical change per PR
4. Include tests matching repo conventions; keep diff reviewable in one sitting
5. Open with Fixes #n, proof of behavior before/after, test output
6. Answer every review comment same-day; ping politely once after two silent weeks

## Common Pitfalls

- Unrequested feature PRs to roadmap items
- Drive-by reformatting bloating diffs

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill oss-pr-landing
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill oss-pr-landing -g
```

**Find good first issues**
```bash
gh search issues --repo <owner>/<repo> "good first issue" --state open
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills