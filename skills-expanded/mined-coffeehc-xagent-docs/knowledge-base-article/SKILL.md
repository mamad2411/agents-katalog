---
name: knowledge-base-article
description: Use when creating, rewriting, organizing, or reviewing knowledge base articles, help center content, internal wiki pages, SOP articles, troubleshooting guides, FAQ entries, onboarding docs, or support macros. Prefer this Skill when the task needs reader task flow, searchable structure, prerequisites, steps, warnings, examples, and maintenance notes. Do not use for publishing, product truth invention, or policy approval.
meta:
  version: 1
  display_name: 知识库文章
---

# Knowledge Base Article

## Purpose

Create task-oriented knowledge content that helps readers solve a specific problem quickly and accurately.

## Use When

Use for:

- help center articles
- internal wiki pages
- SOP articles
- troubleshooting guides
- FAQs
- support macros
- onboarding docs
- maintenance notes

Prefer `blog-writing-workflow` for blog posts, thought leadership, research-backed articles, technical blogs, or newsletter-style articles. Use this Skill only when the content is task-oriented support or operational knowledge.

## Material Gate

Identify:

- target reader, task, prerequisite, product area, and source truth
- current behavior, steps, screenshots or examples if available
- warnings, edge cases, permissions, and escalation path
- whether content is customer-facing or internal

Do not invent product behavior, policy, screenshots, permissions, or support commitments.

## Workflow

1. Define the reader task and success outcome.
2. Put prerequisites and scope before steps.
3. Write steps in action order with expected results.
4. Add warnings, troubleshooting, examples, and escalation when needed.
5. Separate internal notes from public article copy.
6. Add maintenance owner, review trigger, or source link when useful.
7. Use `html-report-builder` for documentation audits or knowledge base reports.

## Checks

- Article answers one primary task.
- Steps are ordered and testable.
- Reader can tell whether the article applies to them.
- Warnings and edge cases are visible.
- Source truth is not invented.
- Blog-style opinion, marketing positioning, or SEO ranking promises are kept out of task articles.
- If product behavior is not verified, mark it as `待确认` / `Not verified`.

## Outputs

- help article
- internal wiki page
- SOP article
- troubleshooting guide
- FAQ entry
- support macro
- documentation audit

## Boundary

This Skill owns knowledge article structure, reader task flow, clarity, and maintenance framing. It does not own product truth, policy approval, CMS publishing, screenshots, account actions, or support system updates.

It must not run shell, Python, Node, npm, curl, MCP, CMS, helpdesk, wiki, product analytics, browser automation, package install, publish, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
