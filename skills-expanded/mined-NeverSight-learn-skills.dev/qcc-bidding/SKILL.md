---
name: qcc-bidding
description: "企业招投标全维度尽调。当用户明确要求「尽调XX公司」「查招投标」「供应商评估」「找投标机会」「投标合规核查」「查竞争对手」时使用。Node.js 直连企查查 API，覆盖工商、司法风险、经营罗盘、知识产权、董监高、历史存档 6 大维度 70 个招投标核心工具。"
---

# 企查查招投标尽调

> 调用链：`node scripts/qcc_client.js` → `agent.qcc.com/mcp/<server>/stream` → JSON 数据。每次独立调用，不依赖 MCP 代理。

## 首次使用：设置 API Key

本 Skill 通过 **`.env` 文件**管理 API Key。用户将 Key 告诉你后，你必须自动写入。

**Agent 自动设置流程（当用户说"我的Key是xxx"时执行）：**

```
1. 识别用户提供的 Key 字符串
2. 将 Key 写入 qcc-bidding/.env 文件（替换 your_key_here）：
   QCC_API_KEY=用户提供的Key
3. 验证：node scripts/qcc_client.js company get_company_profile "华为" 应返回正常数据
```

> Key 未设置时提示用户：去 https://agent.qcc.com 注册获取 Key，然后直接告诉 Agent "我的Key是xxx"，Agent 会自动写入 .env 文件。
> Key 独立计费。Key 过期后重新申请并告诉 Agent 新 Key 即可。
> 脚本读取顺序：系统环境变量 → .env 文件

---

## API 端点

| Server | 端点 | 工具数 | 用途 |
|--------|------|--------|------|
| 企业工商 | `agent.qcc.com/mcp/company/stream` | 13 | 注册信息、股东、实控人、财务、年报 |
| 司法风险 | `agent.qcc.com/mcp/risk/stream` | 23 | 失信、被执行、裁判文书、行政处罚、欠税 |
| 经营罗盘 | `agent.qcc.com/mcp/operation/stream` | 17 | 招投标、资质、信用、纳税、舆情、荣誉 |
| 知识产权 | `agent.qcc.com/mcp/ipr/stream` | 7 | 商标、专利、软著、企业标准 |
| 董监高 | `agent.qcc.com/mcp/executive/stream` | 7 | 董监高任职、关联企业、风险扫描 |
| 历史存档 | `agent.qcc.com/mcp/history/stream` | 3 | 历史工商/股东/失信（需企业认证） |

---

## 通用调用模板

所有场景使用独立脚本 `scripts/qcc_client.js`：

```bash
# 通用格式
node scripts/qcc_client.js <SERVER> <TOOL_NAME> "公司全称"

# SERVER: company | risk | operation | ipr | executive | history
# TOOL_NAME: 见下方工具列表
```

### 招投标专用格式化

```bash
node scripts/qcc_bidding_fmt.js "公司全称"
```

自动以表格输出招投标 TOP 15 记录。

### 财务数据格式化

```bash
node scripts/qcc_client.js company get_financial_data "公司全称"
```

输出 JSON 后按需提取：营收、利润、资产、净利率、负债率、营收增速。

> **原则**：能用格式化脚本的就用；其余工具走通用 `scripts/qcc_client.js` 输出 JSON。

---

## 招投标尽调工具集（按维度分组）

### 工商基础 (company)
| 工具 | 招投标用途 |
|------|-----------|
| `get_company_by_query` | 模糊搜索锁定公司全称 |
| `get_company_registration_info` | 工商注册：名称/代码/法人/资本/成立/状态/地址 |
| `get_company_profile` | 企业概况摘要 |
| `get_actual_controller` | 实际控制人穿透 |
| `get_beneficial_owners` | 最终受益人（UBO） |
| `get_shareholder_info` | 股东出资结构 |
| `get_key_personnel` | 主要人员 |
| `get_external_investments` | 对外投资 |
| `get_branches` | 分支机构 |
| `get_change_records` | 工商变更记录 |
| `get_annual_reports` | 企业年报 |
| `get_financial_data` | 财务数据：营收/利润/资产/净利率/负债率/增速 |
| `verify_company_accuracy` | 核验工商信息准确性 |

### 风险扫描 (risk)
| 工具 | 招投标用途 |
|------|-----------|
| `get_company_risk_scan` | **一键综合风险扫描**（投标前必查） |
| `get_dishonest_info` | 失信被执行人 |
| `get_high_consumption_restriction` | 限制高消费 |
| `get_business_exception` | 经营异常 |
| `get_serious_violation` | 严重违法失信 |
| `get_administrative_penalty` | 行政处罚 |
| `get_tax_violation` | 税收违法 |
| `get_tax_arrears_notice` | 欠税公告 |
| `get_default_info` | 违约事项/票据违约 |
| `get_judicial_documents` | 裁判文书 |
| `get_court_notice` | 开庭公告 |
| `get_equity_freeze` | 股权冻结 |
| `get_stock_pledge_info` | 股权质押 |
| `get_equity_pledge_info` | 股权出质 |
| `get_terminated_cases` | 终本案件 |
| `get_case_filing_info` | 立案信息 |
| `get_environmental_penalty` | 环保处罚 |

### 一票否决类风险 (risk)
| 工具 | 招投标用途 |
|------|-----------|
| `get_bankruptcy_reorganization` | **破产重整**（投标资格一票否决） |
| `get_guarantee_info` | **对外担保**（或有负债风险） |
| `get_chattel_mortgage_info` | **动产抵押**（资产受限） |
| `get_judicial_auction` | 司法拍卖 |
| `get_exit_restriction` | 限制出境 |
| `get_valuation_inquiry` | 评估询价 |

### 经营实力 (operation)
| 工具 | 招投标用途 |
|------|-----------|
| `get_bidding_info` | **招投标记录**（累计/中标/项目明细） |
| `get_qualifications` | **资质证书**（ISO/CMMI/行业资质） |
| `get_credit_evaluation` | 信用评价 |
| `get_taxpayer_qualification` | 纳税信用等级 |
| `get_honor_info` | 荣誉信息/获奖 |
| `get_government_announcement` | 政府公告（招投标相关） |
| `get_government_interview` | 政府约谈（风险信号） |
| `get_news_sentiment` | 新闻舆情 |
| `get_administrative_license` | 行政许可 |
| `get_ranking_list_info` | 行业排名 |
| `get_recruitment_info` | 招聘信息（经营活跃度） |

### 投标机会 (operation)
| 工具 | 招投标用途 |
|------|-----------|
| `get_land_grant_info` | **土地出让**（工程建设标来源） |
| `get_land_transfer_info` | 土地转让 |
| `get_property_rights_transaction` | **产权交易**（国有资产标来源） |
| `get_asset_auction` | 资产拍卖 |
| `get_financing_records` | 融资记录（企业扩张信号） |
| `get_company_announcement` | 企业公告 |

### 知识产权 (ipr)
| 工具 | 招投标用途 |
|------|-----------|
| `get_trademark_info` | 商标 |
| `get_patent_info` | 专利 |
| `get_international_patent` | 国际专利 |
| `get_software_copyright_info` | 软件著作权 |
| `get_copyright_work_info` | 作品著作权 |
| `get_standard_info` | **企业标准**（投标加分项） |
| `get_ipr_pledge` | 知识产权质押 |

### 董监高 (executive)
| 工具 | 招投标用途 |
|------|-----------|
| `get_executive_risk_scan` | **董监高综合风险扫描** |
| `get_executive_positions` | 董监高任职 |
| `get_executive_related_companies` | 关联企业 |
| `get_executive_controlled_companies` | 控制企业 |
| `get_executive_dishonest` | 董监高失信 |
| `get_executive_high_consumption_ban` | 董监高限高 |
| `get_executive_historical_dishonest` | 董监高历史失信 |

### 历史追溯 (history)
| 工具 | 招投标用途 |
|------|-----------|
| `get_historical_company_info` | 历史工商（洗白核查） |
| `get_historical_shareholder_info` | 历史股东 |
| `get_historical_dishonest_info` | 历史失信 |

> **注意**：history Server 需企业认证。未认证时跳过历史维度，不影响主流程。

---

## 场景一：快速查公司

先模糊搜索锁定全称 → 再并行查工商+失信+招投标：

```
步骤1：node scripts/qcc_client.js company get_company_by_query "关键词"
步骤2（并行）：
  node scripts/qcc_client.js company get_company_registration_info "全称"
  node scripts/qcc_client.js risk get_dishonest_info "全称"
  node scripts/qcc_bidding_fmt.js "全称"
```

输出：**企业概览** + **风险速览** + **招投标 TOP 15**。

---

## 场景二：供应商全面尽调（核心场景）

用户说「尽调 XX 公司」，**分 4 批并行执行**：

### 第 1 批：基础画像 (4 条)
```
node scripts/qcc_client.js company get_company_registration_info "全称"
node scripts/qcc_client.js company get_actual_controller "全称"
node scripts/qcc_client.js company get_shareholder_info "全称"
node scripts/qcc_client.js company get_company_profile "全称"
```

### 第 2 批：一键风险 + 一票否决 (5 条)
```
node scripts/qcc_client.js risk get_company_risk_scan "全称"
node scripts/qcc_client.js risk get_bankruptcy_reorganization "全称"
node scripts/qcc_client.js risk get_guarantee_info "全称"
node scripts/qcc_client.js risk get_chattel_mortgage_info "全称"
node scripts/qcc_client.js executive get_executive_risk_scan "全称"
```

### 第 3 批：经营实力 (5 条)
```
node scripts/qcc_bidding_fmt.js "全称"
node scripts/qcc_client.js operation get_qualifications "全称"
node scripts/qcc_client.js operation get_credit_evaluation "全称"
node scripts/qcc_client.js operation get_taxpayer_qualification "全称"
node scripts/qcc_client.js company get_financial_data "全称"
```

### 第 4 批：深度维度 (5 条，按需)
```
node scripts/qcc_client.js operation get_news_sentiment "全称"
node scripts/qcc_client.js operation get_honor_info "全称"
node scripts/qcc_client.js ipr get_patent_info "全称"
node scripts/qcc_client.js ipr get_standard_info "全称"
node scripts/qcc_client.js executive get_executive_related_companies "全称"
```

### 汇总报告结构

```
## 供应商尽调报告：XX 公司

### 一、企业画像
- 工商信息、实控人、股东结构

### 二、风险评级（A/B/C/D）
- 综合风险扫描结果
- 失信/被执行/违约/限高/经营异常/欠税/行政处罚
- 破产重整/对外担保/动产抵押（一票否决项）
- 董监高风险

### 三、经营实力
- 招投标 TOP 10（日期/金额/项目/中标单位）
- 资质证书清单
- 信用评价 / 纳税等级 / 行业排名
- 财务 3 年对比（营收/利润/资产/净利率/负债率）

### 四、加分项
- 荣誉/获奖、企业标准、专利/软著

### 五、关联关系
- 董监高关联企业

### 六、综合结论
- 风险评级 + 是否建议合作 + 关注事项
```

---

## 场景三：招投标专项

```
node scripts/qcc_bidding_fmt.js "全称"
node scripts/qcc_client.js operation get_qualifications "全称"
node scripts/qcc_client.js operation get_honor_info "全称"
node scripts/qcc_client.js ipr get_standard_info "全称"
node scripts/qcc_client.js company get_financial_data "全称"
```

---

## 场景四：关联关系穿透

```
node scripts/qcc_client.js company get_actual_controller "全称"
node scripts/qcc_client.js company get_shareholder_info "全称"
node scripts/qcc_client.js executive get_executive_positions "全称"
node scripts/qcc_client.js executive get_executive_controlled_companies "全称"
node scripts/qcc_client.js executive get_executive_related_companies "全称"
```

---

## 场景五：投标合规核查

重点关注招标文件中的禁止性条款：

```
node scripts/qcc_client.js risk get_company_risk_scan "全称"
node scripts/qcc_client.js risk get_bankruptcy_reorganization "全称"
node scripts/qcc_client.js risk get_serious_violation "全称"
node scripts/qcc_client.js risk get_dishonest_info "全称"
node scripts/qcc_client.js risk get_tax_arrears_notice "全称"
node scripts/qcc_client.js risk get_high_consumption_restriction "全称"
node scripts/qcc_client.js risk get_guarantee_info "全称"
node scripts/qcc_client.js risk get_chattel_mortgage_info "全称"
node scripts/qcc_client.js operation get_government_interview "全称"
```

---

## 场景六：投标机会发现

用户说「找标」「有什么可投的」时，从经营罗盘中挖掘机会：

```
node scripts/qcc_client.js operation get_land_grant_info "地区或关键词"
node scripts/qcc_client.js operation get_property_rights_transaction "地区或关键词"
node scripts/qcc_client.js operation get_asset_auction "地区或关键词"
node scripts/qcc_client.js operation get_government_announcement "关键词"
node scripts/qcc_client.js operation get_company_announcement "关键词"
```

> `searchKey` 可以填地区名（如"苏州"）、行业关键词（如"市政工程"）或留空。
