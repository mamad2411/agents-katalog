---
name: containers-dockerfile-production
description: "Multi-stage builds, slim bases, layer-order discipline, and non-root runtime for small secure images."
---
# Write production-grade Dockerfiles

> Multi-stage builds, slim bases, layer-order discipline, and non-root runtime for small secure images.

**Track:** ☁️ DevOps & Cloud · **Domain:** Containers · **Level:** intermediate · **~30 min**

**Who this is for:** DevOps Engineers, SREs, Cloud Architects, Platform Engineers

## When to Use This Skill

Multi-stage builds, slim bases, layer-order discipline, and non-root runtime for small secure images.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Start from slim/distroless variants pinned by digest, not :latest
2. Order layers least-to-most volatile; lock dependency manifests first
3. Multi-stage: build artifacts in builder, copy ONLY runtime needs
4. Run as non-root USER; expose no debug ports by default
5. Add HEALTHCHECK matching your orchestration's probe
6. Scan images in CI; fail on critical CVEs with a waiver process

## Common Pitfalls

- Copying node_modules across stages including dev deps
- apt-get upgrade layers busting cache every build

## Success Signals

- Image size under 200MB typical service
- Zero critical CVEs shipped

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill containers-dockerfile-production
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill containers-dockerfile-production -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills