---
name: jayt-workbuddy-petdex
description: 为 macOS 官方 WorkBuddy 浏览、安装、切换、运行、诊断、暂停或移除 Petdex 动画桌面宠物，并让宠物显示当前对话、多任务和完成状态，全程不依赖 Codex。用户提到桌面宠物、Petdex、动画伙伴、任务状态宠物、推荐宠物、从 petdex.dev 链接或名称安装宠物、切换宠物、修复宠物或卸载宠物运行组件时使用。
---

# JayT-workbuddy-petdex

Give beginners a complete WorkBuddy pet experience using community pets from [Petdex](https://petdex.dev/zh). Do not involve Codex, modify the WorkBuddy app bundle, or change the WorkBuddy skin.

## Beginner-first rule

Assume the user has never used a terminal, Petdex, a Skill, or a spritesheet. Use short Chinese sentences, explain one decision at a time, and run bundled scripts for them. Never ask them to type a shell command.

When the user has not supplied a pet link, copied Petdex command, or name, reproduce the following Chinese guide faithfully. Keep the link clickable and do not paraphrase it into a longer answer:

> 选宠物只要四步：
> 1. 打开 **[Petdex 中文宠物站](https://petdex.dev/zh)**。
> 2. 点击一只喜欢的宠物。可以直接浏览，也可以用搜索框或标签筛选。
> 3. 复制浏览器地址栏里的详情链接，例如 `https://petdex.dev/pets/boba`。如果你点了页面上的“复制安装命令”也没关系。
> 4. 回到这里粘贴，并说“帮我安装这只宠物”。剩下的交给我，不用打开终端。

Immediately after the guide, say exactly: `浏览和安装 Petdex 官方收录的宠物不需要注册账号，也不需要手动下载文件。` Do not add a second explanation unless the user asks.

If the user asks for recommendations, ask for at most one preference such as “可爱 / 搞怪 / 安静 / 酷” and then direct them to the gallery. Keep the choice with the user; do not install a pet merely because it is popular.

## Installation workflow

When the user supplies a Petdex detail URL, a copied command such as `npx petdex install boba`, or a simple pet slug/name:

1. Read `references/petdex-package.md` and `references/security.md`.
2. Desktop pet activation needs permission to start a local background app. If the current WorkBuddy task is not already in **允许完全访问**, stop before downloading and reproduce this beginner guide faithfully:

   > 安装桌面宠物前，需要给本次任务一次“允许完全访问”：
   > 1. 点击输入框下方的“默认权限”。
   > 2. 点击“允许完全访问”。
   > 3. 勾选“我已了解风险，并愿意继续”，再确认“允许完全访问”。
   > 4. 完成后回复“继续安装”。
   > 这个权限用于把宠物保存到你的个人目录并启动本地宠物，不会修改 WorkBuddy.app。

   Do not claim that a restart can replace this permission. Do not try to change the user's permission yourself.
3. Pass the user's full message to the local resolver. It accepts an exact HTTPS `petdex.dev` detail URL embedded in a sentence, the copied Petdex install command as inert text, or a safe slug. It rejects lookalike domains and never executes the copied command.
4. Run:

   ```bash
   ./scripts/install-pet.sh "<the exact user input>"
   ```

   Use this exact command without `--no-start` in a normal user flow. Do not stop after downloading or describe the pet as “待激活” when the command has not asked for a restart. The installer already attempts safe, no-restart activation.
5. If the command reports that the pet appeared and connected, immediately run `./scripts/doctor.sh`. When the doctor passes, report success and never ask for a restart.
6. If the command says `宠物宿主没有成功启动` or the doctor says the bridge/pet is not running, the task lacks effective Full Access. Show the four permission steps above and ask the user to reply `继续激活宠物`; after that, run `./scripts/start-runtime.sh` and `./scripts/doctor.sh`. Never diagnose this as a restart problem.
   If the installer instead reports that Apple build tools are missing or mismatched, tell the user to open **系统设置 → 通用 → 软件更新** and install the available developer-tools update, or update Xcode from the App Store. Never ask a beginner to open Terminal, run `sudo`, delete `/Library/Developer/CommandLineTools`, or reinstall tools with shell commands.
   If the local error instead says another WorkBuddy desktop pet is running, name the conflict if it is visible, ask the user for permission to pause the old pet, and only continue after consent. Never kill an unrelated pet silently.
7. Only when the exact installer command explicitly says the running WorkBuddy lacks the verified local state connection and requests `scripts/start-runtime.sh --restart`, ask exactly one question: `为了让宠物读取 WorkBuddy 的任务状态，需要重启一次 WorkBuddy。现在可以重启吗？` Never infer that a restart is needed merely because this is the first installed pet.
   Never work around this result with `nohup`, a background shell job, `open` commands, or a direct invocation of `workbuddy-pet`. Those paths can show a window while bypassing lifecycle ownership or the verified state bridge. Only bundled scripts may start the pet runtime.
8. For every other download or network failure, stop and quote the short local error. Do not use WebFetch, DNS-over-HTTPS, a hard-coded IP, `--resolve`, `--connect-to`, disabled certificate checks, a proxy bypass other than the bundled script, or manual installation steps. Ask the user to check their network and try again.
9. Only after the user explicitly agrees, run:

   ```bash
   ./scripts/start-runtime.sh --restart
   ```

10. Run `./scripts/doctor.sh` and report the installed pet name, Petdex source link, and successful state connection.
    A passing doctor also proves that both processes are owned by macOS `launchd`, recover after an unexpected crash while WorkBuddy is open, and do not depend on Codex or the current WorkBuddy task. They are not login-started; if WorkBuddy is closed, the pet is allowed to stop.
    After the user has approved one `--restart`, the local supervisor preserves the state-enabled WorkBuddy launch on later ordinary app opens. Do not ask the user to repeat terminal steps or manually start the pet after each restart.
    If the doctor says `状态桥正在后台等待 WorkBuddy 状态端口` or `scripts/start-runtime.sh --restart`, report that the pet is already stable but current task text cannot update until WorkBuddy is reopened with its local status port. Ask exactly one question: `宠物已经稳定运行。为了让它显示当前对话和任务状态，需要重启一次 WorkBuddy。现在可以重启吗？` If the user agrees, run `./scripts/start-runtime.sh --restart` and then `./scripts/doctor.sh`.
    If doctor instead reports `9441 端口已被其它进程占用`, `untrusted_cdp`, `renderer_not_found`, `inspection_failed`, or `invalid_renderer_state`, do not restart repeatedly. Report the exact diagnosis in Chinese and ask the user to share that doctor result with the Skill maintainer. Never replace these failures with a direct pet-binary command.
11. Explain the controls:
   - Drag the pet anywhere, including outside WorkBuddy.
   - Click it to wave and show/hide the task panel.
   - Right-click for reset, jump, task panel, or quit.
   - It reacts automatically to running, waiting, review, failed, and completed tasks.

Never execute the remote shell returned by Petdex. The bundled installer only extracts allowlisted `https://assets.petdex.dev/` asset URLs, validates the package, and installs it into the WorkBuddy-specific local library.

## Current conversation and multi-task behavior

The native task bubble may show:

- the latest visible user instruction, truncated to 60 characters;
- the current assistant lead/status, truncated to 96 characters;
- up to five WorkBuddy task titles and states;
- an eight-second completion notice.

Never collect a full assistant response, older turns, attachments, filenames, account data, or artifact contents. Read `references/workbuddy-state-bridge.md` when diagnosing task text or animations.

## Manage installed pets

- List local pets: `./scripts/list-pets.sh`
- Switch without downloading: `./scripts/switch-pet.sh "<slug>"`
- Pause pet and bridge: `./scripts/stop-pet.sh`
- Wake the selected pet: `./scripts/start-runtime.sh`
- Diagnose: `./scripts/doctor.sh`
- Remove a non-active pet: `./scripts/remove-pet.sh "<slug>"`
- Uninstall runtime but keep downloads: `./scripts/uninstall-runtime.sh`
- Uninstall runtime and all downloads only after explicit confirmation: `./scripts/uninstall-runtime.sh --remove-pets`

Do not delete pets or the runtime from vague requests such as “换一只” or “先不要这个”. Interpret those as switch/pause, not destructive deletion.

## Boundaries

- Support the official macOS WorkBuddy app only.
- Never modify, unpack, replace, re-sign, or write into `WorkBuddy.app` or `app.asar`.
- Never invoke `$HOME/.workbuddy/jayt-workbuddy-petdex/bin/workbuddy-pet` directly. Always use the bundled lifecycle scripts so the pet, pause marker, bridge, and WorkBuddy status port remain consistent.
- Never install Codex, write Codex hooks, open Codex Settings, or require `~/.codex/pets`.
- Never add theme CSS, background images, skin colors, or page styling. Route those requests to the separate skin Skill.
- Keep Petdex creator attribution and source URLs in local metadata.
- Petdex pets are community submissions and may be fan works. Tell users to check rights before public or commercial use.
- Do not restart WorkBuddy without explicit permission.
