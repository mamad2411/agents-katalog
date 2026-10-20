---
name: wp-code-performance-review
description: Reviews WordPress PHP and asset code for likely performance risks and runs a conservative read-only static scanner before runtime confirmation.
---

# WordPress code performance review

Use this skill to inspect custom plugins, themes, must-use plugins, blocks, or integrations after the audit plan defines scope.

## Review priorities

- unbounded queries and missing pagination;
- N+1 option, metadata, taxonomy, user, or database access;
- broad work on hot hooks;
- synchronous remote requests in user-facing paths;
- cron scheduling and repeated background registration;
- cache key, scope, invalidation, and flush behavior;
- repeated filesystem or serialization work;
- oversized committed assets or profiling artifacts;
- work performed for every request when a narrower condition is possible.

## Scanner

Run:

```powershell
$Scanner = ".agents\plugins\wp-performance-audit\skills\wp-code-performance-review\scripts\scan-wordpress-performance.py"
python $Scanner --help
python $Scanner C:\path\to\project
```

The scanner is heuristic. Read [code-performance-review-checklist.md](resources/code-performance-review-checklist.md), inspect each reported location, and confirm important issues with runtime evidence.

The file [risky-performance-patterns.php](examples/risky-performance-patterns.php) is intentionally unsafe example code for scanner and review training. Never copy it into production.

Run [review-wordpress-code-performance-workflow.md](workflows/review-wordpress-code-performance-workflow.md).
