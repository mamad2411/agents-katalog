---
name: startup-optimization
description: JVM startup tuning for JavaFX desktop apps — CDS, AppCDS, AOT, lazy init, module trimming
license: MIT
compatibility:
  - claude-code
  - cursor
  - codex
  - opencode
  - aider
  - hermes
metadata:
  version: "1.0.0"
  domain: performance
  layer: infrastructure
tags: [java, jvm, startup, performance, javafx, cds, appcds, aot]
---

# Startup Optimization

JavaFX desktop app startup tuning — reduce cold start from seconds to sub-second.

## Key Techniques

1. **CDS/AppCDS** — archive class metadata for faster loading
2. **AOT compilation** — native-image where applicable
3. **Lazy initialization** — defer non-critical module loading
4. **Module trimming** — `--limit-modules` to reduce boot modules
5. **JavaFX pulse tuning** — defer first scene render

## Quick Reference

```bash
# Generate CDS archive
java -Xshare:dump -XX:SharedArchiveFile=app.jsa -cp app.jar

# Use CDS archive
java -XX:SharedArchiveFile=app.jsa -jar app.jar

# AppCDS (class loading archive)
java -Xshare:on -XX:SharedArchiveFile=app.jsa -jar app.jar

# Limit modules
java --limit-modules java.base,java.desktop,javafx.controls,javafx.fxml -jar app.jar
```

## When to Use
- Apps deployed to end-user machines with varying hardware
- Apps where cold start > 2s is unacceptable
- Installer-packaged apps (jpackage) where startup is first impression

## References

→ [references/quick-reference.md](references/quick-reference.md)
