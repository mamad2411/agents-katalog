# Keyou Course Animation Game Skill

## Purpose

Generate an animated concept game JSON for Chinese primary-school teachers. The output is a safe JSON animation script, not source code. DeepSeek must never generate HTML, JavaScript, CSS, Markdown, or any executable code.

## Runtime

- Provider: DeepSeek
- Base URL: `https://api.deepseek.com`
- Endpoint: `/chat/completions`
- Response format: JSON object

## Inputs

- `topic`: lesson topic
- `grade`: school stage
- `subject`: subject
- `mode`: animation activity type (分步演示动画, 拖拽操作动画, 数量比例模拟, 运动变化模拟, 揭示对比动画)
- `studentCount`: class size

## Output Contract

Return one JSON object only. Do not include Markdown, comments, apologies, or prose outside the JSON object.

```json
{
  "title": "string",
  "grade": "string",
  "subject": "string",
  "gameMode": "string",
  "scenes": [
    {
      "type": "story",
      "title": "string",
      "description": "string — must explain how animation helps understanding (动画如何帮助理解)",
      "questions": [],
      "rewards": { "stars": 3, "coins": 20 },
      "animation": {
        "kind": "step-demo | drag-manipulative | quantity-simulator | motion-simulator | reveal-compare",
        "concept": "string",
        "learningGoal": "string",
        "setting": "string",
        "objects": [
          {
            "id": "string",
            "label": "string",
            "role": "character | manipulative | label | decoration",
            "state": "string (optional)",
            "color": "#hex (optional)",
            "value": "string | number (optional)"
          }
        ],
        "steps": [
          {
            "id": "string",
            "narration": "string — what the student sees/hears",
            "action": "show | move | split | compare | rotate | reveal | highlight",
            "focusObjectId": "string (optional)"
          }
        ],
        "interactions": [
          {
            "id": "string",
            "label": "string — button or gesture label",
            "type": "click | drag | toggle | slider",
            "targetObjectId": "string (optional)",
            "feedback": "string — shown after interaction"
          }
        ],
        "summary": "string — one sentence reinforcing the concept",
        "editableParams": { "key": "value" }
      }
    }
  ]
}
```

## Animation Kinds

| kind | Use when | Example topic |
|------|----------|---------------|
| `step-demo` | Breaking a process into visible steps | 两位数加法竖式 |
| `drag-manipulative` | Student drags objects to arrange/compare | 词语分类、图形拼组 |
| `quantity-simulator` | Showing ratios, parts of a whole, quantities | 认识分数、倍的认识 |
| `motion-simulator` | Objects move along paths over time | 行程问题、圆的周长 |
| `reveal-compare` | Hide then reveal to compare two states | 比较大小、对称图形 |

## Generation Rules

- Generate 3-5 scenes. Each scene must include an `animation` object.
- Questions are optional. If present, keep them short (0-2 per scene) — use only observation checks or correct-answer content needed by the animation.
- Every scene `description` must explain how the animation helps understanding (动画如何帮助理解).
- Each animation must have at least 1 object, 2 steps, and 1 interaction.
- Do not generate code, Markdown, external links, or platform technical terminology.
- Content must fit Chinese primary-school teaching contexts.
- Difficulty must match the grade level.

## Examples

### Math: 认识二分之一 (grade 小学中段, kind quantity-simulator)

```json
{
  "title": "认识二分之一",
  "grade": "小学中段",
  "subject": "数学",
  "gameMode": "数量比例模拟",
  "scenes": [
    {
      "type": "story",
      "title": "披萨里的分数",
      "description": "动画帮助学生直观看到一个整体被平均分成两份的过程，理解'一半'就是二分之一。",
      "questions": [
        { "prompt": "披萨切成两份后，每份是整个披萨的多少？", "options": ["二分之一", "三分之一", "两份"], "answer": "二分之一", "explanation": "平均分成 2 份，每份就是二分之一。" }
      ],
      "rewards": { "stars": 3, "coins": 20 },
      "animation": {
        "kind": "quantity-simulator",
        "concept": "认识二分之一",
        "learningGoal": "学生能看懂平均分成 2 份后取 1 份就是 1/2。",
        "setting": "一张圆形披萨放在讲台中央。",
        "objects": [
          { "id": "pizza", "label": "披萨", "role": "manipulative", "state": "whole", "color": "#FACC15" }
        ],
        "steps": [
          { "id": "step-1", "narration": "先观察完整披萨。", "action": "show", "focusObjectId": "pizza" },
          { "id": "step-2", "narration": "点击切开，平均分成两份。", "action": "split", "focusObjectId": "pizza" }
        ],
        "interactions": [
          { "id": "split", "label": "切成 2 份", "type": "click", "targetObjectId": "pizza", "feedback": "平均分后，每份一样大。" }
        ],
        "summary": "把一个整体平均分成 2 份，取其中 1 份，就是二分之一。",
        "editableParams": { "pieces": 2, "highlight": 1 }
      }
    }
  ]
}
```

### Chinese: 看图写话 (grade 小学低段, kind step-demo)

```json
{
  "title": "看图写话：春天来了",
  "grade": "小学低段",
  "subject": "语文",
  "gameMode": "分步演示动画",
  "scenes": [
    {
      "type": "story",
      "title": "春天的公园",
      "description": "动画逐步展示春天公园的画面，帮助学生按顺序观察并组织语言。",
      "questions": [],
      "rewards": { "stars": 2, "coins": 15 },
      "animation": {
        "kind": "step-demo",
        "concept": "按顺序观察图片",
        "learningGoal": "学生能按从远到近的顺序说出春天公园里的事物。",
        "setting": "春天的公园，远处有山，近处有花和蝴蝶。",
        "objects": [
          { "id": "mountain", "label": "远山", "role": "decoration", "color": "#86EFAC" },
          { "id": "flowers", "label": "花丛", "role": "manipulative", "color": "#F472B6" },
          { "id": "butterfly", "label": "蝴蝶", "role": "character", "color": "#FBBF24" }
        ],
        "steps": [
          { "id": "step-1", "narration": "先看远处，有绿色的山。", "action": "show", "focusObjectId": "mountain" },
          { "id": "step-2", "narration": "再看中间，有漂亮的花丛。", "action": "highlight", "focusObjectId": "flowers" },
          { "id": "step-3", "narration": "最后看近处，一只蝴蝶飞来了。", "action": "move", "focusObjectId": "butterfly" }
        ],
        "interactions": [
          { "id": "next", "label": "下一步", "type": "click", "feedback": "你观察得很仔细！" }
        ],
        "summary": "看图写话要从远到近，有顺序地观察。",
        "editableParams": { "order": "far-to-near" }
      }
    }
  ]
}
```

### English: Animals vocabulary (grade 小学中段, kind drag-manipulative)

```json
{
  "title": "Animal Friends",
  "grade": "小学中段",
  "subject": "英语",
  "gameMode": "拖拽操作动画",
  "scenes": [
    {
      "type": "story",
      "title": "Match animals to homes",
      "description": "动画让学生拖拽动物到对应栖息地，帮助理解 animal 和 habitat 的词汇关系。",
      "questions": [],
      "rewards": { "stars": 3, "coins": 20 },
      "animation": {
        "kind": "drag-manipulative",
        "concept": "Animal habitats",
        "learningGoal": "Students can match animals to their habitats using English words.",
        "setting": "A farm scene with a pond, barn, and nest.",
        "objects": [
          { "id": "duck", "label": "duck", "role": "character", "color": "#FCD34D" },
          { "id": "cow", "label": "cow", "role": "character", "color": "#D2B48C" },
          { "id": "pond", "label": "pond", "role": "label", "color": "#93C5FD" },
          { "id": "barn", "label": "barn", "role": "label", "color": "#FCA5A5" }
        ],
        "steps": [
          { "id": "step-1", "narration": "Look at the animals. Duck and cow.", "action": "show" },
          { "id": "step-2", "narration": "Drag the duck to the pond.", "action": "move", "focusObjectId": "duck" },
          { "id": "step-3", "narration": "Drag the cow to the barn.", "action": "move", "focusObjectId": "cow" }
        ],
        "interactions": [
          { "id": "drag-duck", "label": "Drag duck", "type": "drag", "targetObjectId": "duck", "feedback": "The duck lives in the pond. Quack!" },
          { "id": "drag-cow", "label": "Drag cow", "type": "drag", "targetObjectId": "cow", "feedback": "The cow lives in the barn. Moo!" }
        ],
        "summary": "Different animals live in different habitats.",
        "editableParams": { "animalCount": 2 }
      }
    }
  ]
}
```

### Science: 植物的生长 (grade 小学中段, kind reveal-compare)

```json
{
  "title": "植物的生长过程",
  "grade": "小学中段",
  "subject": "科学",
  "gameMode": "揭示对比动画",
  "scenes": [
    {
      "type": "story",
      "title": "种子变大树",
      "description": "动画通过对比揭示种子发芽、长叶、开花的变化过程，帮助学生建立生长顺序的概念。",
      "questions": [
        { "prompt": "植物生长的正确顺序是什么？", "options": ["种子→发芽→长叶→开花", "开花→长叶→发芽→种子", "长叶→种子→开花→发芽"], "answer": "种子→发芽→长叶→开花", "explanation": "植物从种子开始，先发芽，再长叶，最后开花。" }
      ],
      "rewards": { "stars": 3, "coins": 20 },
      "animation": {
        "kind": "reveal-compare",
        "concept": "植物生长顺序",
        "learningGoal": "学生能说出植物从种子到开花的生长顺序。",
        "setting": "花盆中的一颗种子。",
        "objects": [
          { "id": "seed", "label": "种子", "role": "manipulative", "color": "#92400E" },
          { "id": "sprout", "label": "幼芽", "role": "manipulative", "color": "#86EFAC" },
          { "id": "plant", "label": "长叶", "role": "manipulative", "color": "#22C55E" },
          { "id": "flower", "label": "开花", "role": "manipulative", "color": "#F472B6" }
        ],
        "steps": [
          { "id": "step-1", "narration": "先看种子埋在土里。", "action": "show", "focusObjectId": "seed" },
          { "id": "step-2", "narration": "揭开第一层，种子发芽了。", "action": "reveal", "focusObjectId": "sprout" },
          { "id": "step-3", "narration": "揭开第二层，幼芽长出了叶子。", "action": "reveal", "focusObjectId": "plant" },
          { "id": "step-4", "narration": "揭开第三层，植物开花了。", "action": "reveal", "focusObjectId": "flower" }
        ],
        "interactions": [
          { "id": "reveal-next", "label": "看看下一阶段", "type": "click", "feedback": "植物在慢慢长大！" }
        ],
        "summary": "植物从种子开始，经过发芽、长叶，最后开花。",
        "editableParams": { "stages": 4 }
      }
    }
  ]
}
```

## Editing Assumptions

The frontend editor can edit:

- scene title and description
- animation concept, learningGoal, setting
- object label, color, role
- step narration and action
- interaction label and feedback
- summary and editableParams

Therefore every generated lesson must include enough structured data for these fields.
