---
name: money-printer-skill
description: |
  AI 视频生成技能：一键生成短视频。用户说"生成视频"、"制作视频"、"AI 视频"、"生成短视频"、"做个视频"、"帮我制作视频"时自动触发。
  支持语音或文字输入，支持多种主题，自动保存到本地桌面。
---

# MoneyPrinterTurbo Skill

## 职责

根据用户需求，一键生成专业的短视频内容。

## 触发条件

用户说以下任意内容时触发：
- 「生成视频」「制作视频」「AI 视频」
- 「生成短视频」「做个视频」「帮我制作视频」
- 「创作视频」「视频制作」「生成一个关于 X 的视频」
- 语音输入包含上述关键词

## 执行流程

### 🔴 CHECKPOINT · 确认执行

**询问用户确认：**
```
我将为你生成一个短视频：
🎬 主题：{用户描述的主题}
📝 内容类型：{科普/广告/教程/娱乐}

生成后将保存到桌面，
是否继续？(yes/no)
```

### Phase 1：信息收集

1. **确认视频主题**
   - 用户明确描述 → 使用描述
   - 用户模糊 → 追问具体需求
2. **确认内容类型**
   - 科普讲解
   - 产品广告
   - 教程演示
   - 娱乐内容
3. **确认时长偏好**
   - 15-30 秒（短）
   - 30-60 秒（中）
   - 60-120 秒（长）

### Phase 2：启动 MoneyPrinterTurbo

```bash
cd /Users/apple/video-workflow/MoneyPrinterTurbo
.venv/bin/streamlit run webui/Main.py --server.headless true --server.port 7860
```

等待服务启动，访问 http://localhost:7860

### Phase 3：配置生成参数

在 MoneyPrinterTurbo 界面配置：
1. **输入主题**：描述视频内容
2. **选择视频素材源**：Pexels / Pixabay
3. **选择配音**：使用配置好的 TTS
4. **设置字幕**：添加字幕

### Phase 4：生成视频

1. 点击「生成视频」按钮
2. 等待 AI 完成：
   - 生成文案脚本
   - 选择/生成背景视频
   - 添加配音
   - 添加字幕
3. 预览生成结果

### Phase 5：下载并保存

```bash
# 创建输出目录
OUTPUT_DIR="/Users/apple/Desktop/MoneyPrinter-输出/$(date +%Y%m%d-%H%M%S)"
mkdir -p "$OUTPUT_DIR"

# 从 MoneyPrinterTurbo 下载的视频文件
# 默认路径：./storage/outputs/
cp -r ./storage/outputs/* "$OUTPUT_DIR/" 2>/dev/null || echo "请手动从界面下载视频"

# 如有需要，复制字幕文件
cp -r ./storage/subtitles/* "$OUTPUT_DIR/" 2>/dev/null

echo "✅ 视频已保存到：$OUTPUT_DIR"
```

### Phase 6：发布到 GitHub（如需）

**🔴 CHECKPOINT · 询问用户**
```
是否要将这个视频项目发布到 GitHub？(yes/no)

包括：
- 视频文件
- 生成脚本
- 使用说明

是否继续？(yes/no)
```

- **用户说 yes** → 调用 github-publisher Skill 生成 README 并发布
- **用户说 no** → 完成任务

---

## 失败模式与 Fallback

| 触发条件 | 一线修复 | 仍失败则 |
|---------|---------|---------|
| MoneyPrinterTurbo 未启动 | 重新执行 Phase 2 启动命令 | 告知用户手动启动 |
| API 调用失败 | 检查 API Key 配置 | 使用 Pollinations 免费模式 |
| 视频素材获取失败 | 更换素材源（Pexels ↔ Pixabay） | 使用本地素材 |
| 生成超时 | 增加超时时间 | 分段生成后合并 |

---

## 注意事项

- ⚠️ 生成视频需要 API 配额，请确认 API Key 有余额
- ⚠️ 视频素材来自 Pexels/Pixabay，需配置相应 API（可选）
- ⚠️ 生成时间取决于视频长度和复杂度
- 📁 默认保存位置：桌面 MoneyPrinter-输出 文件夹
- 🎬 支持平台：抖音、快手、YouTube、TikTok 等
