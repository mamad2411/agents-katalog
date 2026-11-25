# Skill: Frank-RAG方案设计工具

## Profile
- **Author**: Frank
- **Version**: 1.0.0
- **Language**: 中文
- **Category**: 维度7 - AI项目专精
- **Description**: 生成企业知识库RAG方案，含分块/嵌入/检索/重排/生成全流程

---

## When to Use
AI项目中需要设计RAG知识库方案

---

## Input Requirements
- 知识库规模
- 文档类型
- 检索精度要求

---

## Workflow
1. 设计文档处理流程：加载→清洗→分块→元数据标注
2. 选择嵌入模型：开源(BGE/M3E) vs 商业(OpenAI)
3. 设计向量数据库方案：Milvus/Pinecone/Weaviate
4. 规划检索策略：稠密检索+稀疏检索+混合检索
5. 设计重排序方案：Cross-encoder/Cohere Rerank
6. 设计生成方案：Prompt模板+上下文组装+答案生成
7. 制定评估方案：检索准确率+生成质量+端到端评估
8. 输出RAG方案设计文档

---

## Output Format
RAG方案设计文档（含全流程设计+技术选型+评估方案）

---

## Output Template
```
RAG环节 | 技术方案 | 选型理由 | 参数配置 | 性能指标 | 备选方案
```

---

## Example
| 字段 | 内容 |
|------|------|
| 分块策略 | 语义分块(512 token) | 保持语义完整性 | chunk_size=512, overlap=50 | 召回率85% | 固定长度分块 |

---

## Constraints
- 技术选型有对比分析
- 评估方案可量化
- 方案可落地

---

## Quality Criteria
- [ ] 全流程覆盖
- [ ] 技术选型合理
- [ ] 评估方案科学

---

## Applicable Scenarios
- **G端政府项目**: 部分适用
- **B端企业项目**: 部分适用
- **AI智能项目**: 适用

---

## Usage
### 方式1：Claude Code / Cursor / Codex
将本SKILL.md内容复制到Agent技能配置区，通过技能名触发。

### 方式2：飞书妙搭 / 扣子
将SKILL.md内容粘贴到Agent提示词配置区，设置触发词为技能名。

### 方式3：独立使用
直接复制本文件内容到AI对话中，按Workflow步骤执行。

---

> **Frank专属售前技能** | 维度7: AI项目专精 | 编号: 077
> 基于"Frank售前解决方案Skills工具集 v1.0"与实操提示词融合优化生成
