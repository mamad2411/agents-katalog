---
name: story-npc-add
---

# story-npc-add

## 功能
根据世界观和用户指令生成单个新 NPC。

## 输入参数
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| world | object | ✅ | 当前世界观设定 |
| instruction | string | ✅ | 用户对新 NPC 的描述/要求 |
| existingNpcNames | string[] | ✅ | 已存在的 NPC 名字列表（避免重名） |

## 输出
```json
{
  "npc": {
    "name": "角色名",
    "role": "身份",
    "personality": "性格",
    "shortTermGoal": "短期目标",
    "longTermGoal": "长期目标",
    "hiddenInfo": "隐藏信息 or null",
    "mainPlotLink": "主线关联"
  }
}
```

## 调用示例
```javascript
const result = await runSkill('story-npc-add', {
  world: { world: '...', situation: '...', truth: '...' },
  instruction: '一位对艺术充满热情的普通观众，意外卷入事件',
  existingNpcNames: ['张三', '李四']
});
```
