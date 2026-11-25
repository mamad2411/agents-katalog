# Repo Ref
- source: https://github.com/jinhong270/ai-agent (path: Xiao-Q/skills/ppt-page-recognition/SKILL.md, branch: main)
- mined: 2026-11-24
- desc: 读取本地 PowerPoint `.pptx`，恢复页面结构与语义，并输出可用于后续生成的标准 JSON。在正式识别前，先检查是否存在同名 PDF；如果没有，必须明确提醒用户补充 PDF，或让用户确认接受仅用 PPT 继续识别的较低视觉覆盖率。默认使用当前 IDE 或智能体自身的视觉能力完成图片页补全；如果当前模型不支持视觉，必须先提醒用户切换到支持视觉的模型。
