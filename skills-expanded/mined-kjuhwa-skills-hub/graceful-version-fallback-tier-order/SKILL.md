---
name: graceful-version-fallback-tier-order
description: Four-tier resolution order when a CLI is asked to install `name@version` against a git-tag-based registry and the expected tag does not exist. Replaces "tag-or-bust" with tag → frontmatter match → no-tags-yet hint → other-tags list, plus an explicit `--force-main` escape hatch.
category: cli
tags: [cli-design, versioning, git-tags, semver, pinned-install, graceful-degradation]
triggers:
  - "name@version resolution"
  - "install tag missing"
  - "version fallback order"
  - "--force-main escape hatch"
  - "pinned install friendly error"
source_project: skills-hub-v2.6.3
version: 0.1.0-draft
---
