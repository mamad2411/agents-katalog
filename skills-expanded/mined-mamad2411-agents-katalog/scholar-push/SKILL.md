# Scholar Push - Google Scholar 文献推送 + 粗读

从 Gmail 获取 Google Scholar 推送的文献，进行精确期刊查询和学术粗读。

## 功能

- 📧 获取 Gmail 中 Google Scholar 推送的新文章
- 🎯 通过 DOI/CrossRef API 查询精确期刊/会议信息
- 📖 **学术粗读**：提取研究背景、核心方法、结果贡献、关键词
- 📋 按统一格式输出

## 使用方法

```bash
# 获取最近推送（仅列表）
python3 skill.py list
python3 skill.py list days 7

# 获取推送 + 粗读（默认）
python3 skill.py read
python3 skill.py read days 3

# 仅粗读指定论文（需要 DOI 或 URL）
python3 skill.py fetch https://doi.org/xxx
```

## 输出格式

```
📬 Google Scholar 文献推送 (共X篇)

---

【1】论文标题（加粗）
作者：第一作者 + et al.（单位）
期刊/会议：精确期刊名
推送时间：YYYY.MM.DD

研究背景：（2-3句话，介绍研究动机、问题、现有方案不足）

核心方法：（2-3句话，描述核心技术路线和创新点）

结果与贡献：（2-3句话，总结关键成果、量化指标、意义影响）

关键词：关键词1、关键词2、关键词3

---
```

## 粗读模板

```
研究背景：（2-3句话）
- 研究动机和问题
- 现有方案不足
- 技术挑战

核心方法：（2-3句话）
- 技术路线
- 创新点

结果与贡献：（2-3句话）
- 关键成果
- 量化指标
- 意义影响
```

## 技术细节

- **Gmail API**: 获取 scholaralerts-noreply@google.com 发送的邮件
- **CrossRef API**: 通过 DOI 查询精确期刊/会议信息
- **Semantic Scholar API**: 获取论文摘要、作者单位等信息辅助粗读

## Zotero 分类结构

用户 Zotero 使用层级分类，保存论文时需要识别最佳分类：

```
01-Material & Mechanism（材料与机理）
├── 01-Switching Mechanism（开关机理）
├── 02-Selector & Neuron（选通器与神经元）
├── 03-2D Materials（二维材料）
└── 04-PCM & Other Mem（PCM与其他存储器）

02-Device & Array（器件与阵列）
├── 01-Device Modeling（器件建模）
├── 02-3D Integration（三维集成）
└── 03-Peripheral Circuits（外围电路）

03-Architecture & Logic（架构与逻辑）
├── 01-Analog Computing（模拟计算）
├── 02-Digital & Logic（数字与逻辑）
└── 03-Heterogeneous（异质集成）

04-System & Application（系统与应用）
├── 01-Neural Networks（神经网络）
├── 02-Security（安全）
├── 03-Robotics & SLAM（机器人与SLAM）
└── 04-In sensor computing（传感器计算）

05-Reference（参考资料）
├── 01-Review（综述）
├── 02-Top Conferences（顶级会议）
└── 03-Background（背景）
```

### 分类识别规则

| 论文主题 | 推荐分类 |
|----------|----------|
| 铁电/忆阻器/PCM/存储器 | 01-Material & Mechanism > 04-PCM & Other Mem |
| 器件制备/阵列/工艺 | 02-Device & Array |
| 模拟计算/存算一体/CIM | 03-Architecture & Logic > 01-Analog Computing |
| 神经网络/AI芯片 | 04-System & Application > 01-Neural Networks |
| 安全硬件/PUF | 04-System & Application > 02-Security |
