---
name: distill-shield
description: "Distill Shield：为个人移交资料包生成 Canary 与可选加固策略，提高未授权蒸馏成本；仅适用于有权处置的数据。"
license: MIT
metadata: {"emoji": "🛡️", "ecosystem": "immortal-skill"}
---

## 复制给 AI

- **本 Skill 唯一入口**：当前文件 `SKILL.md`。
- **生成脚本**：

```bash
python3 kit/shield_gen.py --output ./handover-bundle --label "我的移交包"
```

# Distill Shield

## 语言

根据用户**第一条消息**的语言，全程使用同一语言。

## 何时激活

- 用户要「防蒸馏」「加固资料包」「移交前埋 Canary」。
- 用户运行 `kit/shield_gen.py` 后需要根据输出做伦理与可读性检查。

## 伦理红线

- **仅**对本人或已获授权的数据使用；**禁止**对他人资料恶意投毒。
- 不承诺数学上不可攻破；承诺 **可检测性、审计成本、部分管线干扰**。

## 操作顺序

### Phase 0：威胁模型

- 蒸馏场景：一次性 LLM 蒸馏 vs 批量训练 vs 仅人类阅读？
- 接收方：家人 / 律师 / 公司？（决定策略强度）

### Phase 1：材料盘点

- 格式、是否分块检索、是否经 OCR。

### Phase 2：策略选择（准则）

| 策略 | 对人 | 对自动化管线 | 可被绕过 |
|------|------|--------------|----------|
| Canary 唯一字符串 | 低影响（可放附录） | 泄露时可检索 | 剔除后丢失 |
| 提示注入段 | 需标注阅读区 | 可能干扰单次 LLM 蒸馏 | 预处理可剥离 |
| 矛盾样本 | 可能困惑读者 | 污染蒸馏一致性 | 人工可识别 |

### Phase 3：生成

```bash
python3 kit/shield_gen.py --output ./handover-bundle --label "我的移交包"
```

将生成的 `CANARY.txt` 与说明合并进实际交付目录。

### Phase 4：自检清单

- [ ] 第三方隐私已脱敏
- [ ] Canary 已记录在安全处（便于日后比对）
- [ ] 人类读者能看懂「附录为技术性标记」

### Phase 5：（可选）给接收方的一页说明

解释「附录含技术性标记，用于完整性校验，非正文内容」。

### Phase 6：搭配蒸馏协议

建议同时使用 [蒸馏协议](https://github.com/agenmod/distill-protocol-skill) 生成许可文件，防蒸馏负责技术标记，协议负责权利表达。

## 不做的事

- 不提供针对具体模型的对抗样本保证。
- 不帮助绕过合法安全控制。
