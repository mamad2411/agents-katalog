---
name: drawio-aws
version: 1.0.0
description: Use when the user asks for an AWS architecture diagram — VPC/networking, event-driven, landing zone, multi-AZ, serverless pipeline, or any diagram built with AWS service icons. Builds with the declarative layout engine using ground-truth mxgraph.aws4 stencils, validates (stencils/colors/nesting/geometry), runs a render-based vision self-check. Default output is .drawio; PNG/SVG only on request.
license: MIT
---

# Draw.io AWS

Produce correct AWS architecture diagrams in draw.io. This skill is a thin
frontend; the deterministic engine, validator, and rules live in the
`drawio-ai-kit` package, reached via the `drawio-ai` CLI.

## 0. Preflight — the CLI must be installed

```bash
command -v drawio-ai >/dev/null 2>&1 || echo "Install the Kit first:  npm i -g github:sparklabx/drawio-ai-kit"
```

If `drawio-ai` is **not** on PATH, stop and tell the user to run
`npm i -g github:sparklabx/drawio-ai-kit`. **Never run `npm i -g` yourself** — nothing mutates the
user's global environment without their say-so.

## 1. Shared Workflow

```bash
drawio-ai workflow
```

Prints the build → validate → render → write-to-project-path loop every diagram
follows. Read it; it is the source of truth for the process.

## 2. Domain rules

```bash
drawio-ai principles --mode aws
```

Returns the AWS rules + shared principles + catalog categories.

## 3. Build with the engine, then validate + render

Resolve the Kit's install dir, then `import` the engine by absolute path (the
Shared Workflow shows the exact pattern):

```bash
ROOT="$(drawio-ai root)"     # absolute path to the installed Kit
```

Build with the declarative layout engine (NO hand-written coordinates), then:
`drawio-ai validate <file>` → `drawio-ai render <file> -o <file>.png` (`Read`
the PNG for the vision self-check) → write the `.drawio` to an **absolute path
under the user's project** (never the Kit, never `cwd`).

## Domain notes

Container nesting order: `AWS Cloud → Region → VPC → AZ → Subnet → SG`.
Managed/global services (IAM, CloudFront, Route 53, S3, DynamoDB, SQS/SNS)
sit **outside** the VPC — they are not subnet-resident. Category colors from the
catalog are authoritative; **never recolor AWS icons**.

## Self-check (before delivering)
- [ ] Built with the layout engine — no hand-written coordinates.
- [ ] `drawio-ai validate` → ok, no warnings, no advice.
- [ ] Every icon came from `drawio-ai search` (category colors intact).
- [ ] `drawio-ai render` vision self-check passed.
- [ ] Output written under the user's project, not the Kit.
