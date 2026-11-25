---
name: replace-so-oss-repos-10
description: The "10 GitHub repos so good they shouldn't be free" carousel from @replace.so (Echo-Music, Graft, HydraDB, Anydoc, Img2threejs, Openworker, Open-kritt, Crm, Editor; the tenth did not appear in the upload) with each repo's owner, licence and what to watch, from clones read on 5 October 2026 - including an unofficial YouTube Music client, two AGPL projects and an unidentified Editor. Use when considering any of these repos, or checking which are safe to use commercially.
---

# 10 repos "so good they shouldn't be free" (9 seen)

Source: @replace.so carousel, 9 repo slides plus a cover; the tenth repo's slide was not in the upload. Slides name repos without owners, so owners were found by web search and licences read from clones. Star counts on slides are unverified.

| Repo | Slide says | Owner found | Licence | Watch |
|---|---|---|---|---|
| Echo-Music | Android YouTube Music client: ad-free streaming, offline, synced lyrics, podcasts | EchoMusicApp/Echo-Music | GPL-3.0 | An unofficial client that removes ads from YouTube Music: likely against YouTube's terms, and the site funds itself with ads. Personal use at your own risk [Likely] |
| Graft | Open-source context layer: linked code graph for large codebases | NanoNets/Graft | MIT | The graph is linked markdown files in `graft/`; summaries need a model key; the speed and cost claims are the vendor's |
| HydraDB | Rust distributed graph DB on S3-compatible storage, OpenCypher, GraphBLAS, Bolt | hydra-db/hydradb | **AGPL-3.0** | Network copyleft; needs Rust 1.91+; young project |
| Anydoc | Word, PowerPoint, Excel, OpenDocument, RTF, EPUB, CSV, PDF to GitHub-Flavored Markdown (Rust, Node, Python) | firecrawl/anydoc | MIT | Useful for feeding documents to models; check output on your own files |
| Img2threejs | Reference image to code-only procedural Three.js model | several forks found (hoainho, others) | not read | Owner and licence not confirmed; not cloned |
| Openworker | Local-first AI coworker across files and tools, approvals, audit logs | andrewyng/openworker | MIT | Holds connector tokens and model keys locally; read its permission modes before connecting mail or Slack |
| Open-kritt | Self-hosted platform running AI agents to find and validate vulnerabilities | Kritt-ai/open-kritt | **AGPL-3.0** | Runs agents against code with API keys; use only on code you own or are authorised to test |
| Crm | Open-source CRM built for AI agents (research contacts, evidence-based updates) | trycompai/crm | MIT | Enriches people with outside data: a GDPR question for any EU contact |
| Editor | Open-source video editor where agents change timeline and canvas | not identified (candidates: OpenChatCut, AGPL-3.0) | unknown | The slide did not name an owner; do not assume |

## Rule

For commercial use, AGPL items (HydraDB, Open-kritt) need a licence decision first; GPL (Echo-Music) forces its own terms on anything you distribute with it. Use `/repo-licence-check`.
