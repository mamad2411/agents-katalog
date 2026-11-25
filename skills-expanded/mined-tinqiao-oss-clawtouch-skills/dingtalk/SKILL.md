---
name: dingtalk
description: Operate the DingTalk desktop client via simulated keyboard and mouse through clawtouch-mcp — messaging and file sharing (verified), plus docs/calendar surfaces that reuse the Feishu skill's patterns (not independently verified on DingTalk). Tested against DingTalk V7.x on Windows. Explicitly excludes attendance / check-in flows (打卡). Load when the user wants to message, share files, edit docs, or manage calendar events in DingTalk.
---

# Skill: DingTalk (钉钉)

For LLM agents driving **DingTalk desktop** through `clawtouch-mcp`.
DingTalk is one of the dominant B2B collaboration suites in China.
Very little LLM training data — this skill bridges the gap for
day-to-day office surfaces.

> **Tested against**: DingTalk desktop **V7.x** on Windows 10/11
> (zh-CN locale). Last verified 2026-05-26.
>
> ⚠️ DingTalk releases major UI revisions roughly yearly. If you are
> on a substantially newer version (V8+) and the sidebar layout,
> keyboard shortcuts, or menu paths described below don't match what
> you see, the skill may be out of date — please open an issue at
> [tinqiao-oss/clawtouch-skills](https://github.com/tinqiao-oss/clawtouch-skills/issues)
> so we can refresh it.

## Scope

This skill covers DingTalk's messaging, file sharing, docs, and
calendar surfaces — the low-risk daily-office workflows.

**Not covered** (intentionally out of scope):

- Check-in / attendance flows (打卡 / 补卡)
- Approval submit / approve / reject (审批同意 / 拒绝)
- Reimbursement sign-off, attendance adjustments, or any other
  action that creates a binding labor or financial record

These flows must be triggered by the user in person, not by an
unattended agent loop. They are deliberately omitted from this
skill — if your use case requires them, the user must drive the
relevant click in real time.

## When to use this skill

User is operating DingTalk desktop (`DingTalk.exe` on Windows,
`DingTalk.app` on macOS) for messaging, file sharing, or calendar /
docs interaction.

## App-wide navigation

- **Left sidebar** = section switcher: 消息 (Messages) / 文档 (Docs)
  / 日历 (Calendar) / 工作 (Work) / 通讯录 (Contacts)
- **Global search inside DingTalk**: `Ctrl+F`
- **Quick chat switcher**: `Ctrl+Alt+L`
- **Settings**: top-right avatar → 设置

## Messaging (消息)

| Task | Step sequence |
|------|---------------|
| Open a specific chat | `hid.key("ctrl+alt+l")` → type name → Enter |
| Send a message | Click input area → `hid.type("...")` → `Ctrl+Enter` (default — see send-key gotcha) |
| Reply to a specific message | Hover the message → click "回复" icon |
| @ mention | Type `@` then name → arrow keys + Enter |
| Send file | Click paperclip, or drag-drop |
| Voice message | Long-press the mic icon — **avoid this unless explicitly the task** |

### Send-key gotcha ⚠️

Same as Feishu — `Enter` vs `Ctrl+Enter` is user-configurable.
Default to `Ctrl+Enter`; switch only after observing a misfire.

## Docs and Calendar

DingTalk's docs and calendar are **assumed** to share Feishu's shape —
block-based docs (`/` opens the block menu, markdown shortcuts) and a
standard calendar grid — but the DingTalk-specific menu paths here are
**not independently verified** (only the messaging section above was).
Use the [Feishu skill](../feishu/SKILL.md) as the starting point and fall
back to screenshot-based reasoning if the menus differ. Contributions with
verified DingTalk Docs/Calendar steps are welcome.

## Known gotchas

- **Notification banners**: incoming messages produce screen-corner
  toasts that can intercept clicks. Wait or dismiss.
- **Update prompts**: DingTalk frequently prompts for updates with
  a modal — dismiss with `hid.key("escape")`.
- **Multi-org switching**: users in multiple organizations see an
  org-switcher at top. The operation context can change based on
  active org — verify the active org before doing org-specific
  lookups.
- **Login flow**: QR-code only on first install. **Don't try to
  type credentials.**
- **In-app mini-programs (工作 tab)**: companies install custom
  mini-programs whose UI is tenant-specific. **Not covered** by this
  skill — fall back to screenshot + LLM reasoning.

## When this skill doesn't help

- Custom enterprise mini-programs inside the "工作" tab — too varied
- Video meeting controls — real-time, prefer screenshot reasoning
- Admin console at admin.dingtalk.com — separate web app, not
  covered here
