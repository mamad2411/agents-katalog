---
name: feat-issue
description: Plan a OpenDirector feature and publish a concise, actionable GitHub Issue through gh CLI. Use when the user invokes feat-issue or requests feature planning with issue creation, not for implementation or discussion of the skill itself.
---

# Feat Issue

Turn a feature request into a focused specification stored as a remote
GitHub Issue. Keep the feature document in memory and publish through gh
CLI; do not save it as a local Markdown file, including a temporary file.
The skill's own files remain repository-local.

## Invocation and scope

- Explicit invocation authorizes planning and creating the feature Issue.
  Use the feature details supplied in the current conversation. If no
  feature can be identified, ask what to plan before creating anything.
- A request to create or edit this skill, discuss its design, or draft a
  document without publishing does not authorize an Issue. Honor explicit
  preview-only or no-publish instructions.
- An implicitly selected skill may publish when the request includes Issue
  creation. Do not silently expand a planning-only request into publishing.
- Once publication is authorized and the target is clear, create the Issue
  without another confirmation round. Normal execution permissions apply.
- This workflow does not implement code, stage files, commit, create a
  branch or PR, or change existing Issues unless separately requested.

## Plan the feature

Read the user's request and inspect the relevant code with targeted searches.
Distinguish existing behavior from proposed behavior. For OpenDirector, keep
browser interactions, business rules, Agent decisions, durable execution,
and media processing in their proper modules.

Record confirmed requirements directly. Mark inferred choices as suggested
defaults, not user-approved decisions. Ask only when missing information
blocks a meaningful plan; otherwise list important unresolved decisions in
an optional section. Do not ask about routine implementation choices.

Write the title and body in Chinese by default, preserving code identifiers;
follow the user's language preference when specified. Use a short title
such as `[feat] settings: 支持设置菜单与浅深色主题切换`. Choose a scope that
identifies the feature or subsystem, not a generic task label.

For an ordinary small feature, aim for roughly 300–600 Chinese characters in
the body, without treating this as a hard limit. Retain essential constraints
for complex features. Avoid repeated background, generic architecture text,
code listings, and exhaustive file inventories. Keep each requirement in
one place. Acceptance items describe observable results and remain unchecked.

Use these four sections, plus the optional fifth:

```markdown
## 目标与范围

说明用户要解决的问题、本次交付内容，以及必要的范围限制。

## 用户流程与关键规则

- 描述主要操作路径、默认行为与状态变化。
- 补充影响实现的异常、边界或输入方式规则。

## 实现影响

- 列出相关模块或少量关键文件，以及需要调整的职责。
- 说明必要的数据、接口或已有行为兼容要求。

## 验收标准

- [ ] 描述可以直接验证的用户行为。
- [ ] 覆盖关键异常、边界或兼容性要求。
```

Append `## 待确认` only for important open decisions. Do not leave empty
sections or template instructions in the published body. Include keyboard,
touch, layout, persistence, startup, migrations, cost, or permissions only
when relevant, inside the existing sections. Describe proposed new files as
proposals; do not imply unimplemented modules exist. Link relevant existing
Issues or documents rather than duplicating their content. Repository-file
links must target content available remotely, not local absolute paths.

## Resolve the publishing target

1. Confirm gh CLI is available and authenticated with `gh auth status`.
   Never request token output or change authentication automatically.
2. Prefer a repository explicitly named by the user. Otherwise resolve the
   current repository with `gh repo view --json nameWithOwner,url,isArchived,hasIssuesEnabled`.
   Honor an explicit target even when it differs from the current repo.
   If multiple candidates remain ambiguous, ask which repository to use.
3. Confirm the repository is accessible, not archived, and permits Issues.
   Preserve its host for enterprise repositories. Use an explicit `--repo`
   value for every later Issue command so remote defaults cannot redirect it.
4. Search existing Issues for the same request before publishing, using
   `gh issue list --repo ... --state all --search ... --json number,title,body,url,createdAt`.
   Compare content, not just titles. If the request is already represented,
   report its URL rather than creating a duplicate; distinguish an open
   plan from a closed Issue when explaining the match. Related but distinct
   work is not automatically a duplicate. Do not edit or reopen an existing
   Issue unless requested.

If CLI, authentication, repository access, or necessary user input is missing,
report the concrete blocker. Return any useful plan in the chat; do not save
it locally or claim an Issue was created.

## Publish through gh

Call gh directly from the shell, without a Python or other wrapper. Pass
the completed body through standard input using a quoted heredoc, preserving
real newlines. For example (replace all example values before running):

```bash
gh issue create \
  --repo 'github.com/OWNER/REPO' \
  --title '[feat] scope: 简短的特性目标' \
  --body-file - <<'ISSUE_BODY'
## 目标与范围

在此写入按上述结构整理好的完整特性说明。
ISSUE_BODY
```

Keep the heredoc delimiter quoted so Markdown backticks, dollar signs, and
command substitutions in the body remain literal. Choose a delimiter that
does not appear as a standalone line in the body. Shell-quote the repository
and title separately; correctly escape embedded quotes when constructing
these arguments. Do not use eval, an unquoted heredoc, or an echo pipeline
that interprets the document as shell code.

Do not use local feature documents, editor mode, or browser creation mode.
Apply labels, assignees, milestones, and projects only when requested and
available. Do not create labels or change repository settings automatically.

Check the command result and retain the returned Issue URL. If submission
fails with an unclear outcome, perform a read-only lookup in that same repo
for a matching recent title and body. A search miss alone does not prove the
create request was never accepted. Do not blindly retry an ambiguous create;
report uncertainty if the outcome cannot be established. Stop on a concrete
failure and explain it without substituting a local file for publication.

After success, return the Issue URL and a one-sentence scope summary. Keep
the full document on the Issue instead of repeating it in the final answer.
