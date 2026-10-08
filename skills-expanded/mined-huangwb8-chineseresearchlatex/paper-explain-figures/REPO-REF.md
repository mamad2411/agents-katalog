# Repo Ref
- source: https://github.com/huangwb8/chineseresearchlatex (path: skills/paper-explain-figures/SKILL.md, branch: main)
- mined: 2026-09-20
- desc: 解读论文 Figure 的含义并输出一份“教会人类如何读图”的高可读性 Markdown 报告；支持输入 1 个或多个 figure 文件绝对路径与人工解读，自动尝试从图附近检索生成该图的源代码，并采用类似 parallel-vibe 的方式通过 `codex exec`/`claude -p` 以进程级隔离解读每张图（并发上限默认 3，可在 config.yaml 调整）。⚠️ 不适用：用户只是
