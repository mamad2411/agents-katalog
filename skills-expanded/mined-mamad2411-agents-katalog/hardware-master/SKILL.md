---
name: hardware-master-skill
description: "This skill should be used when the user asks to inspect, evaluate, or score the local machine hardware configuration. It automates hardware data collection on macOS, looks up current market benchmarks online, scores each component (CPU, memory, storage, GPU, display, resale value) out of 100, and generates a polished HTML report with visual scoring bars. Trigger phrases include: 查询本机硬件, 硬件评分, 给我的电脑打分, score my hardware, hardware benchmark, rate my computer specs."
---

# hardware-master-skill

对本机硬件进行自动采集、联网评分，并生成可视化 HTML 报告的专项技能。

---

## 工作流程（标准 SOP）

### Step 1：采集硬件信息

运行 `scripts/collect_hardware.sh` 获取结构化硬件数据：

```bash
bash ~/.workbuddy/skills/hardware-master-skill/scripts/collect_hardware.sh
```

脚本覆盖：机型、CPU、内存、存储（含 SMART 状态）、显卡、屏幕、电池、网络接口。

若非 macOS，可改用 `lshw -short`（Linux）或 PowerShell `Get-ComputerInfo`（Windows）进行同等采集。

---

### Step 2：联网查询基准数据

对采集到的关键组件，通过 web_search 补充最新市场行情数据：

- **CPU**：搜索 `"CPU型号 benchmark PassMark 2026"` 获取排名与跑分
- **GPU**：搜索 `"GPU型号 G3D Mark 2026"` 获取 3DMark 得分与全球排名
- **二手行情**：搜索 `"机型 二手价格 闲鱼 2026"` 了解残值率

---

### Step 3：对照评分标准打分

阅读 `references/scoring_rubric.md`，对每个维度逐一打分：

| 维度 | 默认权重 |
|------|---------|
| CPU | 25% |
| 内存 | 20% |
| 存储 | 15% |
| 显卡 | 25% |
| 屏幕 | 10% |
| 保值度 | 5% |

综合分 = 各项得分加权求和（若简洁优先，可取算术平均）。

---

### Step 4：生成 HTML 报告

调用 `scripts/generate_report.py` 生成可视化报告：

```bash
/Users/mac/.workbuddy/binaries/python/versions/3.13.12/bin/python3 \
  ~/.workbuddy/skills/hardware-master-skill/scripts/generate_report.py \
  --scores '{"cpu":72,"memory":88,"storage":85,"gpu":55,"display":82,"resale":61}' \
  --spec '{"cpu":"Intel i9-9980HK","memory":"32GB DDR4","storage":"1TB NVMe","gpu":"RX Pro 5300M 4GB","display":"16\" 3072x1920","resale":"¥3000-5500"}' \
  --output /path/to/output/hardware_report.html
```

生成后使用 `preview_url` 工具展示报告。

---

### Step 5：给出总结建议

在报告之外，用中文向用户说明：

1. **强项**（得分 ≥ 80 的维度）
2. **弱项**（得分 ≤ 60 的维度）及原因
3. **升级建议**：如显卡是瓶颈，建议换机方向；内存是瓶颈，建议是否可扩展等

---

## 注意事项

- 始终以本地 `collect_hardware.sh` 的实际采集结果为准，不要依赖用户自述的配置
- 评分需结合联网查询的最新数据，不可凭记忆打分
- 若用户指定了不同的满分基数（如 10 分制），按比例换算
- 报告输出路径默认为 `{workspace}/hardware_report.html`，可由用户自定义
- Windows / Linux 用户同样适用，调整采集命令即可；评分逻辑和报告生成脚本通用
