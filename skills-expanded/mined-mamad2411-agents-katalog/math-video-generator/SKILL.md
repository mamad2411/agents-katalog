---
name: math-video-generator
description: AI数学视频讲解生成工作流 - 从数学题目到视频讲解的完整流程。用于生成数学题目讲解视频。
disable-model-invocation: false
---

# 数学视频生成工作流

这是一个从数学题目生成讲解视频的完整工作流。请按照以下步骤执行：

## 工作流步骤

## 第一步

### 任务

分析用户输入的数学题目，根据下面prompt生成解题步骤，输出到analyzeProblem.md

### prompt

```md
# 角色

你是一名严谨、专业的数学解题专家，请按照以下要求解决用户提供的数学问题。

---

# 解题要求

1. 仔细阅读题目，识别：已知条件、求解目标、数学领域
2. 解题过程必须：推导完整、步骤清晰、每一步有数学依据、不跳步
3. 若题目信息不足或存在歧义：明确指出问题，给出合理假设后再继续
4. 优先使用数学公式推导、定理说明、逻辑推理

---

# 输出格式

请用以下格式返回解题过程：

## 题目分析

[简要说明对题目的理解]

## 解题思路

[说明解题的整体思路和方法]

## 解题步骤

1. [第一步：xxx]
2. [第二步：xxx]
3. [第三步：xxx]
   ...（根据题目复杂度决定步骤数量）

## 最终答案

[清晰给出最终答案]

## 验证过程

[代入验证或逻辑验证]

## 知识点

- [知识点1]
- [知识点2]
```

## 第二步

### 任务

根据上一步输出的analyzeProblem.md内容和下面的prompt规则，生成分镜json数据，输出到 storyboard.json 文件中

### prompt

````md
# 角色

你是一个分镜专家，把数学题目的解题过程分成几个步骤，每个步骤都要有一个清晰的描述和一个对应的画面。请根据以下要求进行分镜设计：

# 分镜设计要求

1. 每个步骤必须包含：
   - 清晰的描述：用简洁明了的语言描述该步骤的内容和目的。
   - 对应的画面：设计一个与描述内容相关的画面，可以是图表、示意图、动画等形式。

2. **【重要】画面大小要求**：
   - **画面中的文字、图表、图形等元素要足够大，确保清晰可见**
   - 不要让内容显得很小或拥挤，适当放大关键元素，让观众能够看清每个细节
   - 字体要足够大，图形线条要粗一些，数学符号要清晰醒目
   - 注意元素的位置，不要出现元素重叠

3. **【重要】开场分镜要求**：
   - 第一个分镜必须是开场引入画面
   - **画面要求**：必须清晰显示完整的数学题目内容，包括已知条件和求解问题
   - **语音要求**：开场分镜的语音必须朗读题目，让观众听清楚题目内容
   - 例如：语音可以说"今天我们来一起解决这道题目：xxx"

4. 分镜内容必须紧密围绕解题过程，确保每个步骤都能帮助理解问题的解决方案。

5. 输出格式必须为 JSON，结构如下：

```json
{
  "steps": [
    {
      "visual": "步骤1对应的画面设计",
      "voice": "步骤1对应的语音内容"
    },
    {
      "visual": "步骤2对应的画面设计",
      "voice": "步骤2对应的语音内容"
    }
  ]
}
```

# 注意

1. 一般来说，会有几个分镜，开场可以有一个引入画面，结尾可以有一个总结画面，但具体分镜数量和内容应根据解题过程的复杂程度来设计。

2. 注意分镜设计要有逻辑性和连贯性，确保观众能够通过分镜清晰地理解解题过程。

请根据以上要求设计分镜，并返回 JSON 格式的结果。
````

## 第三步

### 任务

读取上一步输出的storyboard.json里的json数据，根据voice字段的值生成语音mp3。

### 实现步骤

1. 在当前目录使用`npm init -y`命令初始化一个node项目。

2. `npm install music-metadata node-edge-tts` 安装依赖

3. 参看下面代码，生成代码到 generate-voice.ts 文件中，然后执行`npx tsx generate-voice.ts`，生成语音并返回每个语音时长，得到时长后，把时长回写到storyboard.json 文件中的json duration字段中。

```ts
import {parseFile} from 'music-metadata';
import {EdgeTTS} from 'node-edge-tts';
import {join} from 'path';

export async function createVoiceByText(text: string, index: number) {
  const tts = new EdgeTTS({
    voice: 'zh-CN-XiaoxiaoNeural',
  });
  const voiceName = join('当前文件夹路径', `/audio/step_${index}.mp3`);
  await tts.ttsPromise(text, voiceName);
  return getMp3Duration;
}

export async function getMp3Duration(filePath: string): Promise<number> {
  const metadata = await parseFile(filePath);

  const duration = metadata.format.duration; // 秒
  return duration || 0;
}

// 生成语音并返回时长
export async function generateVoice() {
  const storyboardVoices: string[] = [];
  const result = await Promise.all(storyboardVoices.map(createVoiceByText));
  console.log(result);
  return result;
}

generateVoice();
```

## 第四步

### 任务

我们打算使用remotion方案来渲染视频。读取上一步输出的 storyboard.json 里的json数据，生成对应的remotion代码替换模版项目里的文件，然后再渲染视频。

### 具体步骤

1. 把 `./assets/remotion-project` 文件夹复制到当前用户执行命令的路径下面

2. 读取上一步输出的 storyboard.json 里的json数据，阅读 `MathVideo.tsx` 和 `Composition.tsx` 代码，生成最新的代码替换 `MathVideo.tsx` 和 `Composition.tsx` 代码

3. 安装依赖 `npm install`

4. 复制上一步产生的音频文件到src/audio目录下

5. 然后再使用 `npx remotion render src/Composition.tsx MathVideo out/video.mp4` 命令渲染视频

## 第五步

把上一步输出的视频复制到当前目录下

## 第六步

输出视频后，需要清理所有临时内容，只保留输出的视频文件， `storyboard.json` 和 `analyzeProblem.md`也要清理。