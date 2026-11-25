---
name: dependency-audit
description: Audits package.json dependencies for outdated packages, security vulnerabilities, unnecessary deps, and version issues. Use when the user says "audit my dependencies", "check my packages", "what deps should I update", "clean up package.json", "are there security issues in my deps", or pastes a package.json.
---

# Dependency Audit

Audits `package.json` across four dimensions: security vulnerabilities,
outdated packages, unnecessary dependencies, and version hygiene. Produces
a prioritized action list with exact upgrade commands.

---

## Required Details

| Detail | Example |
|---|---|
| **package.json content** | Paste full file or deps section |
| **Runtime** | Node.js / browser / both |
| **Framework** | Next.js, Express, React, etc. |
| **Node.js version** | `20`, `22`, etc. |

---

## Instructions

### Step 1 — Classify every dependency

For each package, evaluate:

| Question | Why it matters |
|---|---|
| Is it in the right section? | `devDependencies` vs `dependencies` affects bundle size |
| Is it still used? | Unused deps add attack surface and noise |
| Is it actively maintained? | Unmaintained = no security patches |
| Does it have a better alternative? | Many legacy packages have modern replacements |
| Is the version pinned too tightly? | `"1.2.3"` vs `"^1.2.3"` — prevents getting patches |

### Step 2 — Flag known problematic patterns

**Security risks**
- Packages with known CVEs (reference common ones: `node-fetch` < 3, `lodash` < 4.17.21, `axios` < 1.6.0)
- Packages abandoned with unpatched vulnerabilities
- Overly broad version ranges (`*`, `>= 0.0.0`)

**Wrong section**
```json
// ❌ Build tools in dependencies — shipped to production
"dependencies": {
  "typescript": "^5.0.0",    // should be devDependencies
  "eslint": "^8.0.0",        // should be devDependencies
  "@types/node": "^20.0.0"   // should be devDependencies
}
```

**Redundant or replaceable packages**
| Legacy | Modern replacement |
|---|---|
| `moment` | `date-fns` or `Temporal` |
| `request` | native `fetch` or `axios` |
| `uuid` | `crypto.randomUUID()` (native) |
| `lodash` | native array/object methods |
| `node-fetch` | native `fetch` (Node 18+) |
| `cross-env` | not needed in Node 20+ scripts |

**Version hygiene**
- Prefer `^` (minor+patch updates) over exact versions for non-critical deps
- Prefer exact versions for critical deps (`next`, `react`) to avoid surprise upgrades
- `"*"` is never acceptable

### Step 3 — Generate action list with commands

```bash
# Security — fix immediately
npm audit fix

# Move to devDependencies
npm uninstall typescript && npm install -D typescript

# Upgrade specific package
npm install axios@latest

# Remove unused package
npm uninstall moment
```

---

## Non-Negotiable Acceptance Criteria

- [ ] Every flagged package has a reason and a concrete action
- [ ] Security issues are listed first and marked 🔴
- [ ] Wrong-section packages include the correct `npm install` command to move them
- [ ] Recommended replacements include migration notes if the API changed
- [ ] Output includes a ready-to-run command block for all fixes

---

## Output Format

~~~
## Dependency Audit

### Summary
[X dependencies reviewed. Y security issues, Z outdated, W misplaced.]

### 🔴 Security Issues
[packages with CVEs or unpatched vulnerabilities]

### 🟠 Wrong Section (devDeps in deps or vice versa)
[packages in the wrong section]

### 🟡 Outdated / Unmaintained
[packages that should be upgraded or replaced]

### 🔵 Cleanup Suggestions
[unused, redundant, or replaceable packages]

### Action Commands
```bash
[all fix commands in one block, ready to copy-paste]
```
~~~