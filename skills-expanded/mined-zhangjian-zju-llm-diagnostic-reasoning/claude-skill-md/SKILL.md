# 🤖 Claude Skill 使用指南

> **⚡ 这是一个专为 Claude Code 设计的强大诊断推理 Skill**

## 🎯 什么是 Claude Skill？

Claude Skill 是扩展 Claude Code 能力的官方方式。这个 Skill 让 Claude 能够：

- 🧠 **像专家一样思考** - 执行多步骤诊断推理
- 🎨 **可视化推理过程** - 生成精美的因果图和贝叶斯网络
- 🌍 **跨领域诊断** - 医疗、HVAC、工业、汽车等
- 📊 **量化置信度** - 给出概率化的诊断结果
- ⚡ **一键调用** - `/diagnose` 命令即可启动

## 🚀 快速开始

### 1. 安装 Skill

```bash
# 克隆项目
git clone https://github.com/Zhangjian-zju/llm-diagnostic-reasoning.git
cd llm-diagnostic-reasoning

# 安装依赖
pip install -r requirements.txt
```

### 2. 在 Claude Code 中使用

打开 Claude Code，直接在对话中输入：

```bash
/diagnose --demo hvac
```

就这么简单！Claude 会自动：
1. ✅ 分析症状
2. ✅ 生成诊断假设
3. ✅ 构建推理链路
4. ✅ 生成可视化图表
5. ✅ 给出诊断结论和建议

## 📖 完整命令参考

### 基础用法

```bash
# 运行演示案例
/diagnose --demo hvac          # HVAC 空调诊断演示
/diagnose --demo medical       # 医疗诊断演示
/diagnose --demo industrial    # 工业设备诊断演示
```

### 自定义诊断

```bash
# 指定症状和领域
/diagnose --symptoms "空调送风温度偏高,区域温度偏高" --domain hvac

# 指定诊断方法
/diagnose --symptoms "发热,咳嗽" --method chain      # 推理链路法
/diagnose --symptoms "发热,咳嗽" --method symptom   # 症状驱动法
/diagnose --symptoms "发热,咳嗽" --method bayesian  # 贝叶斯网络法
```

### 高级选项

```bash
# 输出详细日志
/diagnose --demo hvac --verbose

# 指定输出格式
/diagnose --demo hvac --output json        # JSON 格式
/diagnose --demo hvac --output markdown    # Markdown 报告
/diagnose --demo hvac --output html        # 交互式 HTML

# 保存可视化图表
/diagnose --demo hvac --save-viz reasoning_chain.png
```

## 🎨 三种诊断方法详解

### 方法一：多步骤推理链路 (`--method chain`)

**适用场景：**
- ✅ 需要详细的推理过程
- ✅ 验证诊断结果的合理性
- ✅ 学习和教学场景

**示例：**
```bash
/diagnose --symptoms "空调送风温度偏高" --method chain
```

**输出：**
```
🔍 诊断推理中...

Step 1: 故障假设生成
├─ 假设1: 冷却盘管阀门卡死 (92%)
├─ 假设2: 冷却盘管泄漏 (65%)
└─ 假设3: 送风机转速过低 (45%)

Step 2: 推理链路构建
故障源: 冷却盘管阀门卡死
   ↓ (冷却不足)
送风温度升高 (+2.3°C)
   ↓ (热空气传递)
区域温度升高 (+1.8°C)

Step 3: 验证分析
✅ 症状匹配率: 89%
✅ 逻辑一致性: 高

🎉 诊断结论: 冷却盘管阀门卡死 (置信度: 92%)
```

### 方法二：症状驱动诊断 (`--method symptom`)

**适用场景：**
- ✅ 未知故障类型
- ✅ 真实诊断场景
- ✅ 需要逆向推理

**示例：**
```bash
/diagnose --symptoms "发热,咳嗽,呼吸困难" --method symptom --domain medical
```

**特点：**
- 🔍 从症状出发，逆向推理
- 📚 动态查询知识库
- 🎯 更符合实际诊断流程

### 方法三：贝叶斯网络 (`--method bayesian`)

**适用场景：**
- ✅ 有历史数据支持
- ✅ 需要快速诊断
- ✅ 概率推理场景

**示例：**
```bash
/diagnose --symptoms "电机温度过高,振动异常" --method bayesian --domain industrial
```

**特点：**
- ⚡ 推理速度快 (<0.1s)
- 📊 概率量化
- 🔄 可持续学习

## 🌍 支持的领域

### 🏢 HVAC（空调系统）

```bash
/diagnose --symptoms "送风温度偏高,区域温度偏高,冷却阀门固定75%" --domain hvac
```

**常见诊断：**
- 冷却盘管阀门卡死
- 冷却盘管泄漏
- 送风机故障
- 传感器故障

### 🏥 医疗诊断

```bash
/diagnose --symptoms "发热38.5℃,干咳,呼吸困难,胸部CT磨玻璃影" --domain medical
```

**常见诊断：**
- 呼吸道感染
- 肺炎
- 心血管疾病
- （仅供参考，请咨询专业医生）

### 🏭 工业设备

```bash
/diagnose --symptoms "电机温度85℃,振动频率120Hz,电流15A" --domain industrial
```

**常见诊断：**
- 轴承磨损
- 电机过载
- 传动系统故障
- 冷却系统失效

### 🚗 汽车故障

```bash
/diagnose --symptoms "发动机抖动,加速无力,油耗增加" --domain automotive
```

**常见诊断：**
- 点火系统故障
- 燃油系统问题
- 进气系统堵塞
- 传感器故障

## 💡 最佳实践

### 1️⃣ 提供准确的症状描述

```bash
# ❌ 不够具体
/diagnose --symptoms "空调坏了"

# ✅ 详细准确
/diagnose --symptoms "送风温度比设定值高2.3°C,区域温度高1.8°C,冷却阀门固定在75%"
```

### 2️⃣ 选择合适的方法

| 场景 | 推荐方法 |
|------|---------|
| 需要详细解释 | `--method chain` |
| 未知故障类型 | `--method symptom` |
| 快速诊断 | `--method bayesian` |
| 学习研究 | `--method chain` |

### 3️⃣ 结合可视化

```bash
# 生成可视化图表
/diagnose --demo hvac --save-viz my_diagnosis.png

# 生成交互式 HTML
/diagnose --demo hvac --output html
```

### 4️⃣ 批量诊断

```python
# 在 Python 中批量处理
from llm_diagnostic import BatchDiagnostic

batch = BatchDiagnostic(method="chain")
results = batch.diagnose_from_csv("test_cases.csv")
```

## 🎓 学习资源

- 📖 [完整文档](README.md)
- 🔬 [方法论详解](docs/METHODOLOGY.md)
- 🎨 [可视化指南](docs/VISUALIZATION.md)
- 💡 [最佳实践](docs/BEST_PRACTICES.md)

## 🤝 贡献

这个 Skill 是开源的！欢迎：

- 🐛 报告 Bug
- 💡 提出新功能
- 🌍 添加新的诊断领域
- 📝 改进文档
- ⭐ 给项目点 Star

## 📞 获取帮助

- 💬 [GitHub Discussions](https://github.com/Zhangjian-zju/llm-diagnostic-reasoning/discussions)
- 🐛 [Issue Tracker](https://github.com/Zhangjian-zju/llm-diagnostic-reasoning/issues)
- 📖 [完整文档](README.md)

---

<div align="center">

**🤖 Built with ❤️ using Claude Code**

[⬆ 回到主页](README.md)

</div>
