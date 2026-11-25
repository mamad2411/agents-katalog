---
name: mes-progress-update
description: Use before committing or handing off AI-MES Copilot work to update COLLABORATION.md with concise progress, module status, validation results, next step, risks, or AI-assisted development notes.
---

# MES Progress Update

## Purpose

Keep project progress readable for community contributors. Updates should be short, useful, and tied to actual work. Public credits use GitHub usernames, not real names or private email addresses.

## When to Update

Update when:

- a feature or slice is completed;
- module status changes;
- API or database contract changes;
- a meaningful bug is fixed;
- validation result matters to others;
- a risk or handoff note exists.

## How to Update

1. Follow the current `COLLABORATION.md` structure: append a dated section describing the change.
2. State the affected module or documents, completed work, and verification scope.
3. Keep the entry concise; do not introduce a progress table when the file has none.
4. If a module status changed, describe the new state in the same entry.
5. Mention if validation was not run and why.

## Example Entry

```text
YYYY-MM-DD 文档维护：更新当前项目说明与有效文档入口；检查链接和项目名称。仅修改说明文件，未运行业务回归。
```

## Must Not

- Do not write vague rows like "优化代码" without module and result.
- Do not mark "已完成" without validation.
- Do not remove previous progress history unless explicitly requested.
