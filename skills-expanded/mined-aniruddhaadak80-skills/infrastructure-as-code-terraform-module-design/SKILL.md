---
name: infrastructure-as-code-terraform-module-design
description: "Composable modules with typed variables, sensible defaults, and outputs that compose upward."
---
# Design Terraform modules people reuse

> Composable modules with typed variables, sensible defaults, and outputs that compose upward.

**Track:** ☁️ DevOps & Cloud · **Domain:** Infrastructure as Code · **Level:** intermediate · **~40 min**

**Who this is for:** DevOps Engineers, SREs, Cloud Architects, Platform Engineers

## When to Use This Skill

Composable modules with typed variables, sensible defaults, and outputs that compose upward.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. One module = one architectural decision (a network, a service, a store)
2. Type every variable; constrain with validation blocks
3. Defaults for 80% cases; no secret values as defaults ever
4. Outputs expose only what callers genuinely consume
5. Tag resources uniformly: env, owner, repo, cost-center
6. Version modules semver; changelog breaking moves loudly

## Common Pitfalls

- Copy-pasted 800-line root modules nobody dares touch
- count vs for_each migrations destroying remote state

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill infrastructure-as-code-terraform-module-design
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill infrastructure-as-code-terraform-module-design -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills