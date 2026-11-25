---
name: byte-deliver
description: Package final Your ByteDance / Byte OS delivery artifacts. Use when the product has been built and reviewed, or when the user asks to ship, hand off, summarize, package, or produce final delivery instructions.
---

# Byte Deliver

Deliver creates the final handoff for the built product. It should make the result usable by a human who was not present during the session.

## Inputs

Read:

```text
.byte-os/BYTE.md
.byte-os/OKRS.md
.byte-os/PRODUCT_SPEC.md
.byte-os/ROADMAP.md
.byte-os/plans/*.plan.md
.byte-os/BUILD_LOG.md
.byte-os/reviews/*.md
.byte-os/iterations/*.md
.byte-os/users/*.md
```

Inspect the actual repository or deliverable files.

## Delivery Checks

Verify:

- Product goal is clear.
- MVP scope is complete or known gaps are documented.
- Build or artifact exists.
- Run instructions are accurate.
- Tests or manual verification are recorded.
- Review verdict allows delivery, or risks are explicitly accepted.
- Real user feedback is not claimed unless `byte-users` ran on real evidence.
- Objective and Key Results status are summarized honestly.

For a web app or app requiring a server, start the dev server when appropriate and provide the local URL. If opening a static HTML file is enough, provide the absolute file path.

## Artifact

Write:

```text
.byte-os/DELIVERY.md
```

Include:

```text
# Product

# What Was Delivered

# How To Run

# How To Test

# Key Files

# Verification

# OKR Status

# Review And Iteration Summary

# Known Gaps

# Recommended Next Steps

# Real User Feedback Status
```

Update `STATUS.md`:

```text
Stage: delivered
Next recommended command: byte-users when real feedback exists, otherwise byte-iterate for planned improvements
```

## Completion Criteria

Delivery is complete when the user can run or inspect the result and understands what is complete, what is risky, and what to do next.
