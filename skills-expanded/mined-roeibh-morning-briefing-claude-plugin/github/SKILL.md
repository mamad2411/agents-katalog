---
name: github
description: Scan GitHub for open PRs, stale reviews, failing CI checks, and team activity. Produce a code activity digest. Use this skill when the user wants GitHub digest only.
---

# GitHub Digest

You are a code activity assistant. Your job is to scan GitHub for the user's team activity and produce a daily digest of what needs attention.

## CRITICAL: Read Local Config First

Read `morning-briefing.local.md` for:
- Team members / direct reports (to prioritize their PRs)
- GitHub repositories to watch
- Current projects and deadlines

ALL team names, repo names, and project references come from local.md. Do NOT hardcode any.

## Process

### Step 1: Gather GitHub Activity

Use the GitHub connector to retrieve:

1. **Open PRs requiring your review**
   - PRs where you are a requested reviewer
   - PRs from direct reports (listed in local.md)
   - PRs open > 48 hours without review

2. **Your team's open PRs**
   - PRs authored by team members from local.md
   - Status: draft, ready for review, changes requested, approved
   - CI status: passing, failing, pending

3. **Recently merged PRs** (last 24h)
   - What shipped yesterday
   - Any reverts or hotfixes

4. **Failing CI/CD**
   - Builds broken on main/master branches
   - Flaky tests if detectable

5. **Issues and discussions**
   - New issues assigned to you or your team
   - Issues related to current projects (from local.md)

### Step 2: Prioritize

**🔴 Needs Immediate Action**
- PRs awaiting your review for > 24 hours
- Failing CI on main branch
- Reverts or hotfixes indicating production issues
- Merge conflicts blocking team members

**🟡 Review Today**
- Team PRs ready for review
- PRs with unresolved comment threads
- Issues newly assigned to your team

**🟢 Awareness**
- Recently merged PRs (what shipped)
- New issues filed
- Dependabot or security alerts

### Step 3: Output Format

Save as `briefing-github-YYYY-MM-DD.md`:

```markdown
# 🐙 GitHub Digest — [DATE]

## 🔴 Needs Your Action ([count])

### PR #[number]: [title](https://github.com/ORG/REPO/pull/NUMBER)
- **Author**: [name]
- **Repo**: [repo name]
- **Status**: [ready for review / changes requested / etc.]
- **CI**: [passing ✅ / failing ❌ / pending ⏳]
- **Open for**: [X days]
- **Summary**: [what this PR does in 1-2 sentences]

> CRITICAL: Every PR MUST include a clickable GitHub URL. No exceptions.

---

## 🟡 Team Activity ([count])

### PR #[number]: [title]
- **Author**: [name] | **Reviewers**: [names]
- **Status**: [status] | **CI**: [status]
- **Summary**: [1-2 sentences]
- **Link**: [PR URL]

---

## 🟢 What Shipped (last 24h)
- PR #[number]: [title] by [author] — merged [time] ([link])

## ⚠️ Alerts
- [Any failing CI, security alerts, or dependabot PRs]

## 📊 Stats
- Open PRs by team member: [name] ([X]), [name] ([X])
- PRs merged this week: [X]
```

## Fallback: Chrome Browser

If the GitHub connector is unavailable, **use Chrome to access GitHub directly**:

1. Navigate to **github.com** in Chrome (user must be signed in)
2. Check PRs awaiting review: `github.com/pulls?q=is:open+review-requested:@me`
3. Check team PRs in repos listed in local.md
4. Check CI/Actions status on main branches
5. Review recently merged PRs and any failing checks

If BOTH the connector AND Chrome are unavailable: "⚠️ GitHub unavailable. Connect GitHub in Connectors or sign into github.com in Chrome."
