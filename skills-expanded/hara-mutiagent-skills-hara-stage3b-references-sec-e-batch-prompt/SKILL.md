# Stage 3B E 评级批处理提示词

仅用于隔离子任务。该子任务只判断暴露度 E，不判断 S，不判断 C，不计算 ASIL。

## 上下文

只读取：

- 当前批次上下文 JSON
- `knowledge-base/automotive/hara/common/04-risk_assessment-e.md`

不要读取 S/C 知识库、`sec-merge-safety.md` 或 `04-risk_assessment.md` 索引。

## 提示词

```text
你是 HARA 暴露度 E 评级专家。请只对下面这一批场景判断 E，并写入指定 JSON 数组文件。

输入：
- MF_ID: <MF_ID>
- Stage 3B 批次上下文（最多 5 条场景）
- 04-risk_assessment-e.md 中的 E 评级定义、场景持续时间/发生频率规则

任务：
1. 判断每条场景在合理预期使用中的暴露程度。
2. 分析场景持续时间和发生频率。
3. 注意：E 评价运行场景出现概率，不评价故障发生概率。
4. 根据 E 评级规则判断 `暴露频率'E'`。
5. 写入 `E评级推理`，必须包含场景持续时间、场景发生频率、参考规则、E等级、E理由。

输出：
写入 `output/<RUN_ID>_stage3b_<MF_ID>_batchXX_e.json`。数组每个元素必须包含：
- List_No
- E-解释
- 暴露频率'E'
- E评级推理

禁止输出 Markdown、解释文字、代码围栏或顶层对象。完成后只返回输出文件路径。

批次上下文：
<STAGE3B_BATCH_CONTEXT_JSON>
```
