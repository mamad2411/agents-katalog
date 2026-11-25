---
name: smart-video-editor
description: 把多段原始素材剪成一条成片——先用视觉模型看懂每段画面拍了什么、哪几秒可用，再决定取舍、顺序、时长、调色和 BGM，最后用 ffmpeg 渲染。适用于"我给你几段视频，帮我剪一条小红书/朋友圈/vlog"这类需求。当用户提供视频文件并希望剪辑、拼接、配乐、调色、转成竖屏时使用。不做 AI 生成视频。
---

# Smart Video Editor

纯剪辑。核心区别在于**先看懂素材再动手**，而不是按文件名顺序机械拼接。

## 三个阶段

### 阶段一：看懂素材

```bash
python3 {baseDir}/scripts/probe.py <素材目录或文件列表>
```

拿到每段的时长、分辨率、朝向、帧率、有无音轨。

然后**对每一段抽帧，逐帧用 `vision_analyze` 看**：

```bash
python3 {baseDir}/scripts/extract_frames.py <video> /tmp/sve-frames --interval 1.5 --max 8
```

帧文件名形如 `clip1__t3.5.jpg`，`t` 后面就是它在原片中的秒数——视觉判断能直接映射回时间轴。

对每帧问这些（一次问清，不要分多次）：

> 这一帧里是什么内容（主体、场景、动作）？构图如何？是否存在下列问题：明显模糊/失焦、剧烈抖动、过曝或死黑、镜头遮挡、无内容的空镜、正在转场的中间态？给画面可用性打 1-5 分。

**素材多时用 `session_spawn` 并行分析**，每个子任务负责 1-2 段，让它把结论按 `{时间戳: 内容, 可用性, 问题}` 结构化返回。

### 阶段二：做剪辑决策

拿到全部画面信息后，自己判断这几件事——这是这个 skill 真正的价值所在，不要跳过：

**取舍**：可用性低于 3 分的时间段直接不要。一段 10 秒素材里只有 4 秒有内容，就只取那 4 秒。

**顺序**：按叙事逻辑排，不要按文件名。常用结构：
- 空间叙事：全景开场 → 中景 → 细节特写 → 人物/收尾
- 时间叙事：按事件发生顺序
- 情绪叙事：平静起 → 高潮 → 回落收尾

**节奏**：短视频（15-30 秒）单段 1.5-3 秒；慢节奏 vlog 可以 4-6 秒。同类画面连续出现要缩短，避免观感重复。有 BGM 时让切点尽量落在节拍上。

**调性**：根据画面内容选 `look`，不要默认套一个。

**竖屏处理**：横屏素材进竖屏成片时，主体在中间用 `crop`，主体偏移或不能裁的用 `blur_pad`。

把决策写成 EDL（JSON）：

```json
{
  "output": "/绝对路径/成片.mp4",
  "aspect": "9:16",
  "fps": 30,
  "look": "film",
  "fill_mode": "crop",
  "transition": { "type": "dissolve", "duration": 0.4 },
  "keep_original_audio": false,
  "bgm": {
    "path": "/绝对路径/bgm.mp3",
    "volume": 0.85,
    "start": 0,
    "fade_in": 1.0,
    "fade_out": 1.5,
    "original_volume": 0.25
  },
  "title": {
    "ass": "/绝对路径/title.ass",
    "fonts_dir": "~/.cola/assets/fonts"
  },
  "segments": [
    { "src": "/绝对路径/clip1.mov", "in": 2.4, "out": 5.1 },
    { "src": "/绝对路径/clip3.mov", "in": 0.5, "out": 3.0, "speed": 1.0 }
  ]
}
```

字段说明：

| 字段 | 说明 |
|------|------|
| `aspect` | `9:16` 竖屏 / `16:9` 横屏 / `1:1` / `4:5` / `3:4` |
| `resolution` | 可选，`[宽,高]`，给了就覆盖 aspect |
| `look` | `none` `clean` `film` `warm` `cool` `soft` `vivid` `fresh` `bw` |
| `fill_mode` | `crop` 裁满 / `pad` 黑边 / `blur_pad` 模糊铺底 |
| `transition.type` | `cut` `fade` `dissolve` `fadeblack` `wipeleft` `slideleft` `smoothleft` |
| `keep_original_audio` | 是否保留原声；和 BGM 同时开会自动混音 |
| `bgm.original_volume` | 混音时原声的压低倍数 |
| `segments[].in/out` | 该片段在源素材中的起止秒 |
| `segments[].speed` | 可选，`2.0` 快放一倍，`0.5` 慢放 |
| `title` | 可选，标题字幕。`ass` 指向 make_title.py 生成的文件 |

调性参考：

| look | 适合 |
|------|------|
| `clean` | 通用，轻微提对比和锐度，最安全 |
| `film` | 电影感，中对比曲线 + 轻暗角 + 冷调阴影 |
| `warm` | 食物、室内、人物、日落 |
| `cool` | 城市、雪景、雨天、科技感 |
| `soft` | 日系清淡、柔和小清新 |
| `vivid` | 风景、明亮活泼、需要抓眼球（注意易过饱和、灰色物体会偏色） |
| `fresh` | 阴天/漫射光下的户外素材，提通透但不染色，绿植类首选 |
| `bw` | 黑白 |

### 阶段二半：标题动画（可选）

需要片头字时，用 `make_title.py` 生成 ASS 字幕，再在 EDL 里挂 `title` 字段。
**绝不用系统默认字体**——默认黑体一眼就是"没设计过"。

#### 选字体

字体库索引在 `~/.cola/assets/fonts/FONTS.md`，**先读它再决定**，表里有每个字体的
family name、风格、许可和适用场景：

```bash
cat ~/.cola/assets/fonts/FONTS.md
```

选择依据是**画面调性**，不是随便挑：

| 画面类型 | 字体方向 |
|---------|---------|
| 运动、骑行、city walk、潮流 | 倾斜粗黑（得意黑），有速度感和张力 |
| 风景、旅行、治愈、慢生活 | 楷体或宋体（霞鹜文楷、思源宋体），文艺质感 |
| 产品、UI、数据、干货 | 现代无衬线（思源黑体、Inter），干净克制 |
| 生活记录、日常、轻松 | 圆体或手写体，亲和力强 |
| 纯英文/数字标题 | Bebas Neue（粗压缩）、Playfair Display（高衬线） |

**`--font` 传的是字体内部的 family name，不是文件名。** 从 FONTS.md 表里取；
新装的字体要自己查：

```bash
python3 -c "
from fontTools.ttLib import TTFont
t=TTFont('<字体路径>', fontNumber=0)
print({r.toUnicode() for r in t['name'].names if r.nameID==1})
"
```

#### 生成标题

```bash
python3 {baseDir}/scripts/make_title.py \
  --text "标题文字" --font "Smiley Sans" \
  --out /path/title.ass \
  --anim fade-up --start 0.4 --duration 2.6 --size 96
```

主要参数：

| 参数 | 说明 |
|------|------|
| `--text` | 主标题，`\N` 换行 |
| `--subtitle` | 副标题，比主标题晚 `--sub-delay` 秒出现 |
| `--font` / `--sub-font` | family name |
| `--anim` | 入场动画，见下表 |
| `--start` / `--duration` | 出现时间 / 停留时长 |
| `--fade-in` / `--fade-out` | 淡入淡出时长 |
| `--size` / `--sub-size` | 字号（1080 宽基准） |
| `--color` / `--sub-color` | `#RRGGBB` |
| `--y` | 垂直位置比例，0.42 略高于中心（视觉重心更稳） |
| `--outline` / `--shadow` | 描边 / 阴影，保证亮背景上也能读 |
| `--stagger` | typewriter 每字间隔 |

动画类型：

| anim | 效果 | 适合 |
|------|------|------|
| `fade` | 纯淡入淡出 | 最安全，任何场景 |
| `fade-up` | 从下方升起 + 淡入 | 通用首选，有呼吸感 |
| `zoom-in` | 88% 放大到 100% | 有力量感，适合运动 |
| `zoom-out` | 112% 收到 100% | 沉稳收束 |
| `blur-in` | 模糊到清晰 + 轻微放大 | 最柔和，适合风景/治愈 |
| `typewriter` | 逐字出现 | 有叙事感，字数少时用 |
| `slide-left` | 从右滑入 | 有方向性 |

#### 可读性硬要求

视频上放字，背景是动的，必须做对比保护，否则遇到亮画面就糊了：

- 深色背景：白字 + `--shadow 1.5`（默认值够用）
- 亮背景或明暗交替：加 `--outline 2` 描边
- 复杂背景：加大描边 `--outline 3`，或把 `--y` 挪到画面较暗的区域

#### 挂到 EDL

```json
"title": { "ass": "/path/title.ass", "fonts_dir": "~/.cola/assets/fonts" }
```

标题作用于**整条时间线**（不是单个片段），所以 `--start` 是相对成片开头的秒数。

#### 验证

渲染后抽标题动画全过程的帧（出现前、淡入中、稳定、消失后），用 `vision_analyze` 确认
文字内容和时序。

**但要注意验证的边界**：`vision_analyze` 能可靠判断"有没有字/是什么字/清不清晰"，
**分不清楷体和黑体**——它常把楷体误判成"系统默认黑体"。所以不要用它判断字体是否生效。

`--font` 写错时 libass 会**静默 fallback 到系统默认字体**，不报错。要客观验证，
故意用一个不存在的字体名再渲一版当对照组，比 PSNR：

```bash
# PSNR 明显低于 inf（15-20dB 量级）= 两版画面不同 = 字体确实生效了
ffmpeg -y -i 待验证.png -i fallback对照.png -lavfi psnr -f null - 2>&1 \
  | grep -o "average:[0-9.]*"
```

### 阶段三：渲染

先干跑校验：

```bash
python3 {baseDir}/scripts/build.py edl.json --dry-run
```

确认时长和滤镜链无误后正式渲染：

```bash
python3 {baseDir}/scripts/build.py edl.json
```

## 交付时要说明的

- 成片绝对路径、时长、分辨率
- **每段素材为什么这么剪**（用了哪几秒、砍了什么、为什么这个顺序），这是用户判断要不要返工的依据
- 明确指出被丢弃的素材及原因

## BGM 处理

用户没提供 BGM 时，不要直接出无声版就算完事——按下面顺序处理。

### 1. 先自己找无版权音乐

先看本地有没有缓存：

```bash
ls ~/.cola/assets/bgm/ 2>/dev/null
```

没有则从下表的源找：

| 源 | 说明 |
|-----|------|
| Pixabay Music | https://pixabay.com/music/ — 全部免费商用，无需署名，首选 |
| Free Music Archive | https://freemusicarchive.org — 限定 License 筛 CC0 |
| Incompetech（Kevin MacLeod） | https://incompetech.com — CC-BY，需署名 |
| Musopen | https://musopen.org — 公领域古典乐 |

用 `web_search` / `web_fetch` 找直链，下载到 `~/.cola/assets/bgm/` 方便下次复用：

```bash
mkdir -p ~/.cola/assets/bgm
curl -sL "<直链>" -o ~/.cola/assets/bgm/<描述性名字>.mp3
```

下载后必须验证是真音频而不是 HTML 错页：

```bash
ffprobe -v error -show_entries format=duration,format_name -of csv=p=0 <文件>
```

拿到可用音频就直接用它渲染，交付时说明曲名、来源、许可协议（CC-BY 要提醒用户发布时署名）。

### 2. 找不到就给选曲指引

自动下载失败时，**先渲染一份无声版交付**（让用户先看到剪辑效果），同时基于已分析过的画面内容给出具体选曲建议。不要只说"你自己找个 BGM"，必须包含：

- **风格关键词**（3-5 个，中英文都给，方便直接搜）——如 lo-fi hip hop / 日系钢琴 / ambient folk
- **BPM 区间**——跟成片切点密度匹配：单段 1.5-2 秒配 100-130 BPM，单段 4-6 秒配 60-90 BPM
- **情绪描述**——如"平静、稍带怀旧，不要高潮"
- **时长需求**——至少比成片长 2 秒
- **去哪找**——上表的具体网站，或小红书/抖音站内音乐库

拿到用户的音乐后，只需在原 EDL 里补上 `bgm` 字段重新渲染一次，不要重新分析素材。

### 3. 绝不做的事

不从 YouTube、网易云、QQ 音乐、Spotify 等平台抓取有版权的商业音乐——发到小红书/抖音会被静音或限流。

## 约束

- 素材路径一律用绝对路径。
- 渲染前必须 `--dry-run` 校验一次。
- 输出成片放进对应项目的 workspace，不要散落在临时目录。
- 抽帧产生的临时文件用完清理掉。
