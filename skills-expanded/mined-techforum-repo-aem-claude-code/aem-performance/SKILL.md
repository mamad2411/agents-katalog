---
name: aem-performance
description: AEM performance review — JCR queries, traversal, resolver lifecycle, PostConstruct overhead
allowed-tools: Read, Grep, Glob
argument-hint: "[file or class path]"
---

Review `$ARGUMENTS` for AEM performance issues. Report each finding as **Blocking** / **Warning** / **Suggestion**.

- **JCR query without an Oak index or without a result limit** — Blocking
- **Query executed inside a loop** — Blocking
- **`Thread.sleep()` in servlet, job, scheduler, or workflow step** — Blocking
- **Request-scoped state (resolver, session, request) stored in an OSGi singleton field** — Blocking
- **Expensive query or broad tree traversal in `@PostConstruct` on a frequently rendered Sling Model** — Warning
- **`ResourceResolver` or `Session` held open longer than needed** — Warning
- **Lazy initialization missing where data is not always needed** — Suggestion
