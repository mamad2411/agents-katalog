---
name: inkdiary-next
description: 当用户要求继续优化、升级、排错或迭代 InkDiary 安卓墨水屏手写 AI 日记项目时使用。适合处理 ROADMAP 中的流式回复、显示开关、SurfaceView、记忆召回等任务。
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TaskCreate, TaskUpdate
---

# InkDiary 迭代技能

使用本技能时，按以下流程工作：

1. 先读这些文件，确认当前边界：
   - `README.md`
   - `docs/ROADMAP.md`
   - `docs/ARCHITECTURE.md`
   - `.codebuddy/CODEBUDDY.md`
2. 把用户目标映射到 ROADMAP 里程碑；如果不在路线图里，先说明应插入哪个里程碑。
3. 只做一个最小可验证改动，列出将修改的文件。
4. 改动时遵守 `.codebuddy/rules/android-ink.md` 与 `.codebuddy/rules/security.md`。
5. 完成后做能力范围内的检查：XML 解析、包名一致、关键类引用、ZIP 重新打包。
6. 如果不能编译，必须明确说“未编译验证”，并给出用户本机 Android Studio 的下一步操作。
7. 最后更新 README 或相关 docs，让用户能继续按步骤操作。

默认交付口径：

- 说明改了什么、为什么、影响哪些文件。
- 给出下一步建议，按 P0/P1/P2 排序。
- 若产生可下载结果，重新生成 `/workspace/InkDiary.zip`。
