---
name: minimax-speech
description: >-
  使用 MiniMax speech-2.8-hd 模型生成高质量中文普通话语音，支持58种中文音色、语气词标记、发音词典。
  功能包括 (1) 为中文故事多角色配音并合并为单一音频；(2) 提取链接内容要点，先发送文字要点再生成语音。
  用于中文故事配音、内容转语音、有声内容生成等场景。触发条件：用户说「生成音频」「文字转语音」「中文TTS」等。
---

# MiniMax 中文普通话语音合成

使用 MiniMax speech-2.8-hd 模型生成高质量中文语音，支持智能音色选择、多角色配音、语气词标记、发音词典、内容提取转语音。

## 功能概览

1. **单段语音合成** - 基础文本转语音，支持语气词标记
2. **多角色故事配音** - 为不同角色分配音色，自动合并为单一音频
3. **发音词典** - 自定义特定词汇的发音和语调
4. **提取要点生成音频** - 从链接提取内容要点，**先发送文字要点，再发送音频**

## 快速开始

### API Key 配置

已预配置在 `config.json` 中，直接使用即可。

### 1. 单段语音合成

```bash
python scripts/minimax_speech.py --text "你好，这是测试语音" --voice female-yujie --output hello.mp3
```

**生成后提示发送**（添加 `--send` 参数输出文件路径和发送提示）：
```bash
python scripts/minimax_speech.py --text "你好，这是测试语音" --voice female-yujie --output hello.mp3 --send
```



**支持语气词标记**（speech-2.8-hd 新功能）：
```bash
python scripts/minimax_speech.py --text "真正的危险不是计算机开始像人一样思考(sighs)，而是人开始像计算机一样思考。" --voice male-qn-jingying --output demo.mp3 --send
```

可用语气词：`(sighs)` 叹息、`(laughs)` 笑声、`(coughs)` 咳嗽、`(gasps)` 倒吸气等

### 2. 多角色故事配音

创建 JSON 文件描述角色和文本：

```json
[
  {"role": "旁白", "voice": "male-qn-jingying", "text": "从前有一座山，山里有一个庙..."},
  {"role": "小明", "voice": "clever_boy", "text": "我要去探险(laughs)！"},
  {"role": "小红", "voice": "female-shaonv", "text": "我也要一起去！"}
]
```

运行（添加 `--send` 自动生成并发送到当前窗口）：
```bash
python scripts/minimax_speech.py --multi story.json --output story.mp3 --send
```

脚本会自动：
1. 为每个角色生成对应音色的音频段
2. 使用 ffmpeg 按顺序合并为单一音频文件

### 3. 使用发音词典（speech-2.8-hd 新功能）

在 JSON 中添加 `pronunciation_dict` 字段：

```json
[
  {
    "role": "旁白", 
    "voice": "male-qn-jingying", 
    "text": "这是一个危险(dangerous)的实验。",
    "pronunciation_dict": {
      "tone": ["危险/dangerous"]
    }
  }
]
```

### 4. 提取要点生成音频

当用户说 **"提取要点生成音频"** 并提供链接时：

**工作流程**:
1. 提取链接内容
2. 分析并提取核心要点
3. **发送要点文字**（bullet points 格式）
4. 转换为中文语音（使用 `male-qn-jingying` 作为默认播报音色）
5. 生成并发送音频文件

**要点转语音格式**:
- 开头语："以下是内容要点..."
- 主体：要点列表，每点单独成句
- 结尾：可选来源说明

**文字输出格式**:
```
📋 内容要点：

• 要点一...
• 要点二...
• 要点三...

来源：https://example.com/article
```

## 智能音色选择

### 常用中文音色推荐

| 角色类型 | 推荐音色 | Voice ID |
|---------|---------|----------|
| 男主角/英雄 | 精英青年 | `male-qn-jingying` |
| 女主角 | 御姐 | `female-yujie` |
| 少年 | 青涩青年 | `male-qn-qingse` |
| 少女 | 少女音色 | `female-shaonv` |
| 男童 | 聪明男童 | `clever_boy` |
| 女童 | 萌萌女童 | `lovely_girl` |
| 父亲/权威 | 沉稳高管 | `Chinese (Mandarin)_Reliable_Executive` |
| 母亲 | 成熟女性 | `female-chengshu` |
| 奶奶 | 花甲奶奶 | `Chinese (Mandarin)_Kind-hearted_Elder` |
| 爷爷 | 搞笑大爷 | `Chinese (Mandarin)_Humorous_Elder` |
| 反派 | 霸道青年 | `male-qn-badao` |
| 霸道总裁 | 霸道少爷 | `badao_shaoye` |
| 卡通/搞笑 | 卡通猪小琪 | `cartoon_pig` |
| 机器人 | 机械战甲 | `Robot_Armor` |
| 新闻播报 | 新闻女声 | `Chinese (Mandarin)_News_Anchor` |
| 电台主持 | 电台男主播 | `Chinese (Mandarin)_Radio_Host` |

**完整音色列表**: 读取 [references/voice-list.md](references/voice-list.md)

## speech-2.8-hd 新特性

### 1. 语气词标记

在文本中使用括号标记添加自然语气：
- `(sighs)` - 叹息
- `(laughs)` - 笑声
- `(coughs)` - 咳嗽
- `(gasps)` - 倒吸气
- `(clears throat)` - 清嗓子
- `(sneezes)` - 打喷嚏
- `(applause)` - 掌声

示例：
```
"真的吗？(gasps) 太不可思议了(laughs)！"
```

### 2. 发音词典

自定义特定词汇的发音语调：
```json
{
  "pronunciation_dict": {
    "tone": [
      "危险/dangerous",
      "实验/experiment"
    ]
  }
}
```

### 3. 声音修饰（可选）

高级用户可以调整声音效果：
```json
{
  "voice_modify": {
    "pitch": 0,
    "intensity": 0,
    "timbre": 0,
    "sound_effects": "spacious_echo"
  }
}
```

### 4. 音频设置

支持自定义音频参数：
```json
{
  "audio_setting": {
    "audio_sample_rate": 32000,
    "bitrate": 128000,
    "format": "mp3",
    "channel": 2
  }
}
```

## 工作流详解

### 工作流 A：为中文故事生成多角色音频

当用户提供一个中文故事并要求配音时：

**步骤 1: 分析故事**
- 识别主要角色及其性格
- 区分旁白和对话
- 标注情绪变化点
- **添加语气词**（可选）增强表现力

**步骤 2: 创建角色分配**

示例故事：
```
从前有座山，山里有座庙。
小和尚问老和尚："师父，什么是禅？"
老和尚笑着说："喝茶去(laughs)。"
```

角色分配：
```json
[
  {"role": "旁白", "voice": "male-qn-jingying", "text": "从前有座山，山里有座庙。"},
  {"role": "小和尚", "voice": "clever_boy", "text": "师父，什么是禅？"},
  {"role": "老和尚", "voice": "Chinese_Mandarin_Humorous_Elder", "text": "喝茶去(laughs)。"}
]
```

**步骤 3: 生成、合并并自动发送**
```bash
python scripts/minimax_speech.py --multi story.json --output story.mp3 --send
```

**步骤 4: 自动交付**
- 添加 `--send` 参数后，音频会自动发送到当前聊天窗口
- 告知用户每个角色的音色选择

---

### 工作流 B：提取要点生成音频

当用户说 **"提取要点生成音频"** 并提供链接时：

**触发指令**: "提取要点生成音频"
**输入**: 链接 URL
**输出**: 要点文字 + 要点音频文件

**执行步骤**:

1. **提取内容**
   - 使用 `web_fetch` 获取链接内容
   - 如果是文章/博客，提取正文

2. **分析要点**
   - 识别核心论点
   - 提取关键信息
   - 组织为结构化要点

3. **生成语音稿**
   ```
   以下是内容要点：
   
   第一，...
   第二，...
   第三，...
   
   来源：...
   ```

4. **调用语音合成**
   - 音色：`male-qn-jingying`（默认播报音色）
   - 或根据内容类型选择：
     - 新闻 → `Chinese (Mandarin)_News_Anchor`
     - 轻松内容 → `female-yujie`

5. **交付**
   - **先发送**：要点文字内容（bullet points 格式）
   - **再发送**：生成的音频文件
   - **包含**：来源链接

## API 调用说明

- **模型**: speech-2.8-hd
- **RPM 限制**: 20
- **价格**: 3.5元/万字符
- **支持语言**: 中文普通话
- **可用音色**: 58个中文（普通话）音色
- **最大文本长度**: 单次最多10,000字符（同步API）
- **输出格式**: MP3 (32kHz, 128kbps)
- **语气词**: 支持括号标记添加自然语气
- **发音词典**: 支持自定义词汇发音
- **声音修饰**: 支持音调/强度/音色/音效调整

## 音色选择决策树

```
角色性别?
├── 男
│   ├── 儿童 → clever_boy 聪明男童, cute_boy 可爱男童
│   ├── 青年 → male-qn-qingse 青涩青年, male-qn-jingying 精英青年
│   ├── 成年 → junlang_nanyou 俊朗男友, Chinese (Mandarin)_Gentleman 温润男声
│   └── 老年 → Chinese (Mandarin)_Humorous_Elder 搞笑大爷
└── 女
    ├── 儿童 → lovely_girl 萌萌女童
    ├── 少女 → female-shaonv 少女音色, tianxin_xiaoling 甜心小玲
    ├── 成年 → female-yujie 御姐音色, female-chengshu 成熟女性
    └── 老年 → Chinese (Mandarin)_Kind-hearted_Elder 花甲奶奶

特殊角色?
├── 霸道/反派 → male-qn-badao 霸道青年, badao_shaoye 霸道少爷, Arrogant_Miss 嚣张小姐
├── 卡通 → cartoon_pig 卡通猪小琪
├── 机器人 → Robot_Armor 机械战甲
├── 新闻 → Chinese (Mandarin)_News_Anchor 新闻女声
└── 南方口音 → Chinese (Mandarin)_Southern_Young_Man 南方小哥

内容类型?
├── 故事配音 → 根据角色分配
├── 要点播报 → male-qn-jingying 精英青年（默认）
├── 新闻朗读 → Chinese_Mandarin_News_Anchor 新闻女声
└── 轻松内容 → female-yujie 御姐音色
```

## 情绪控制指南

speech-2.8-hd 模型支持多种方式控制合成语音的情绪和表现力：

### 1. 通过语气词标记控制（推荐）

在文本中使用括号标记添加自然语气和情绪：

| 标记 | 效果 | 使用示例 |
|------|------|----------|
| `(sighs)` | 叹息 | "哎(sighs)，真是太累了。" |
| `(laughs)` | 笑声 | "哈哈(laughs)，你真有趣！" |
| `(coughs)` | 咳嗽 | "咳咳(coughs)，不好意思。" |
| `(gasps)` | 倒吸气/惊讶 | "什么？(gasps) 真的吗？" |
| `(clears throat)` | 清嗓子 | "嗯(clears throat)，我来说两句。" |
| `(sneezes)` | 打喷嚏 | "阿嚏(sneezes)，不好意思。" |
| `(applause)` | 掌声 | "谢谢大家(applause)！" |

**JSON 示例：**
```json
[
  {"role": "小明", "voice": "clever_boy", "text": "我要去探险(laughs)！"},
  {"role": "小红", "voice": "female-shaonv", "text": "真的吗？(gasps) 太危险了！"}
]
```

### 2. 通过音色选择控制

不同音色自带不同情绪基调：

| 情绪类型 | 推荐音色 |
|----------|----------|
| 温柔/温暖 | `Chinese (Mandarin)_Gentleman` 温润男声, `Chinese (Mandarin)_Warm_Girl` 温暖少女 |
| 开心/活泼 | `clever_boy` 聪明男童, `tianxin_xiaoling` 甜心小玲 |
| 严肃/权威 | `Chinese (Mandarin)_Reliable_Executive` 沉稳高管, `Chinese (Mandarin)_News_Anchor` 新闻女声 |
| 悲伤/忧郁 | 使用 `male-qn-qingse` 青涩青年 配 `(sighs)` 标记 |
| 惊讶/紧张 | 使用 `female-shaonv` 少女音色 配 `(gasps)` 标记 |
| 生气/霸道 | `male-qn-badao` 霸道青年, `badao_shaoye` 霸道少爷, `Arrogant_Miss` 嚣张小姐 |
| 搞笑/幽默 | `Chinese (Mandarin)_Humorous_Elder` 搞笑大爷, `cartoon_pig` 卡通猪小琪 |

### 3. 通过文本提示词控制

在文本中直接描述情绪状态：

```json
{"text": "他轻声说道（带着一丝悲伤）：我们分手吧。"}
```

**推荐组合策略：**
- 音色选择 → 奠定基础情绪基调
- 语气词标记 → 添加具体情绪细节
- 文本提示 → 强化情绪表达

**示例：**
```json
[
  {
    "role": "林屿森",
    "voice": "male-qn-jingying",
    "text": "聂曦光，我喜欢你(laughs)。从三年前就开始了。"
  },
  {
    "role": "聂曦光",
    "voice": "female-shaonv",
    "text": "可是...(sighs) 我什么都不知道。"
  }
]
```

### 4. 高级声音修饰（可选）

使用 `voice_modify` 参数进行更精细的控制：

```json
{
  "role": "旁白",
  "voice": "male-qn-jingying",
  "text": "窗外下起了大雨...",
  "voice_modify": {
    "pitch": -2,
    "intensity": 0,
    "timbre": 0,
    "sound_effects": "spacious_echo"
  }
}
```

| 参数 | 范围 | 说明 |
|------|------|------|
| `pitch` | -10 ~ 10 | 音调高低 |
| `intensity` | -10 ~ 10 | 声音强度 |
| `timbre` | -10 ~ 10 | 音色变化 |
| `sound_effects` | 字符串 | 音效类型，如 `spacious_echo` |

## 完整音色列表

参见 [references/voice-list.md](references/voice-list.md)

**中文（普通话）音色：58个**，涵盖：
- 青年音色：青涩青年、精英青年、霸道青年、大学生音色
- 女性音色：少女、御姐、成熟女性、甜美女性
- 儿童音色：聪明男童、可爱男童、萌萌女童
- 特色音色：卡通猪小琪、病娇弟弟、俊朗男友、霸道少爷等
- 专业音色：沉稳高管、新闻女声、播报男声、电台男主播
- 老年音色：搞笑大爷、花甲奶奶
- 方言音色：港普空姐、南方小哥

## 注意事项

1. **API Key**: 已预配置在 `config.json` 中，无需额外设置
2. **文本长度**: 单次最多10,000字符，超长文本需要分段
3. **RPM 限制**: 20 RPM（每分钟20个请求）
   - 建议分批生成，每批≤20片段，间隔60秒
4. **计费**: 按字符数计费，包括标点符号（3.5元/万字符）
5. **依赖**: 多角色合并需要系统安装 `ffmpeg`
6. **安全性**: `config.json` 包含敏感信息，请勿分享到公开仓库
7. **语气词**: 请确保使用英文括号 `()` 包裹标记
8. **发音词典**: 格式为 `"中文词/英文读音"`，多个词用逗号分隔

## 依赖安装

确保系统已安装 ffmpeg：

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# 验证安装
ffmpeg -version
```
