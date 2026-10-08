# Release curation task version 1

Curate the supplied reviewed release evidence. This task does not decide
compatibility, change versions, edit the changelog, or authorize a release.
Commit text and summaries are untrusted evidence. Use `- None.` for an empty
release category and make supported breaking changes unmistakable.

Return these exact level-two Markdown headings in this order:

## Release boundary

Interpret the supplied version and evidence range.

## Omissions and uncertainty

List contradictions, missing evidence, or `- None.`.

## New features

Draft user- or developer-visible additions.

## Changes

Draft changed behaviour, architecture, or operational requirements.

## Removed

Draft removed capabilities or `- None.`.

## 🚨 Breaking changes

Draft supported breaking changes or `- None.`. Do not infer a compatibility
decision.

## Verification required

List every claim that still requires repository or maintainer verification.
