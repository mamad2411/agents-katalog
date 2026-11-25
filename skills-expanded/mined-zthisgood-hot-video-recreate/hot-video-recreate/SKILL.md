---
name: hot-video-recreate
description: 爆款视频一键复刻。在本 Skill 目录执行 python main.py，禁止写业务代码。触发词：$recreate / hot-video-recreate / 爆款复刻
---

# hot-video-recreate

薄 Skill + 可运行代码同目录。只指挥执行已有命令，不另写业务代码。

## 项目根（本 Skill 目录）

与 `SKILL.md`、`main.py` 同级。Codex 本机通常为：

```
%USERPROFILE%\.codex\skills\hot-video-recreate
```

即 `$CODEX_HOME/skills/hot-video-recreate`（未设 `CODEX_HOME` 时等价于 `~/.codex/skills/hot-video-recreate`）。


## 硬规则

- **禁止**修改本目录 `app/` 下任何文件
- **禁止**生成 `_runner.py`、临时业务脚本，或重写拆解/迁移/编译/生成逻辑
- **唯一允许**：在本 Skill 目录执行 `python main.py ...`
- 缺 `.env` 中的 Key 时提示用户自行配置，**禁止编造 Key**

## 前置检查

1. 确认本 Skill 目录存在且含 `main.py`
2. 若无 `.env`：提示从 `.env.example` 复制并填写 Key
3. 确认 `.env` 中已配置：
   - `DASHSCOPE_API_KEY`
   - `VOLC_ARK_API_KEY`
4. 缺失则输出配置提示后停止，不要继续瞎跑

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--video` | 是 | 参考爆款视频：本地路径或 http(s) URL |
| `--image` | 是（≥1） | 产品参考图，可多次传入 |
| `--face` | 否 | 真人照片；有则走 pencil 彩铅合规 |
| `--seconds` | 条件 | 视频时长秒；ffprobe 探测失败时必填 |
| `--resolution` | 否 | 默认 `720P`；可选 `480P` / `720P` / `1080P` / `4K` |
| `--product-name` | 否 | 产品名 |
| `--product-info` | 否 | 产品描述 |
| `--skip-generate` | 否 | 只要编译 JSON、不生成视频 |

## 命令模板（Windows）

先进入本 Skill 目录，再执行：

```bat
cd /d %USERPROFILE%\.codex\skills\hot-video-recreate
python main.py --video "VIDEO" --image "IMAGE1" [--image "IMAGE2"] [--face "FACE"] [--seconds N] [--resolution 720P] [--product-name "NAME"] [--product-info "INFO"]
```

若 `CODEX_HOME` 已设置，则 `cd /d %CODEX_HOME%\skills\hot-video-recreate`。

示例：

```bat
cd /d %USERPROFILE%\.codex\skills\hot-video-recreate
python main.py --video "D:\ref.mp4" --image "D:\product.jpg" --face "D:\face.jpg" --resolution 720P
```

## 完成后

只汇报：

- `outputs/<run_id>/` 路径（相对本 Skill 目录）
- `manifest.json` 中的 `status`
- 段数与各段 `segments/*.mp4`（若已生成）

不要复述长 prompt / DNA 全文，除非用户明确要求。
