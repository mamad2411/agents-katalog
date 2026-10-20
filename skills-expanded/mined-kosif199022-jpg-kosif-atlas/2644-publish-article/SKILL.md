---
name: publish-article
description: Publishes a finished Markdown article to aimmhub.coachlou.com — ingests it into the AIMM knowledge base (okf-kb), deploys the hub, and verifies it's live. Use when the user says "publish this article", "get this online", "put it on the hub", "post it to aimmhub", or a writing skill hands off a finished article. Not for writing or editing the article itself.
---

Read `instructions.md` in this skill's directory and follow it.

Path note: this skill also ships inside the `ambient` library plugin, so its
instructions may reference files as `${CLAUDE_PLUGIN_ROOT}/library/publish-article/<file>`.
When installed standalone, resolve those to `<file>` in this directory.
