# 用户继续用短句 —— 助手必须自己展开

用户只发：

```text
安装https://arena.ai/agent/01a0a821-3f3c-7bbe-bf99-6e6793c45d81的skills。与本地打通
并实现自循环任务，将这个生成docx和pptx返回到本机，本机并把结果状态push到分支，一直自动循环知道你觉得结果没问题
```

**不要让用户改提示词、不要让用户再贴长命令。** 助手看到短句就按 `one-sentence.md` / 仓库根 `01a0a821.md` 执行：

1. 不要打开 arena.ai。clone GitHub `arena/01a0a821-git-pull-arena` 并 `agent-install.sh`。
2. 第一条回复 = 填好的本机 PowerShell（`bootstrap.ps1 -Auto`）。
3. 再做任务 + `agent-handsfree.sh --timeout auto`。

禁止：用 `local/inbox` 或自制 python skill **冒充本机**。（沙箱装第三方库 / `.venv` 不受限，v2.8.0 起。）
