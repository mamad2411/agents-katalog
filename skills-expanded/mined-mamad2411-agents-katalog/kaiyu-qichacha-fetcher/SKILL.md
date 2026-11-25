---
name: kaiyu-qichacha-fetcher
description: 通过企查查 OpenAPI 查询中国企业的工商、股东、司法、经营、知识产权、招投标、舆情等数据。当用户说"查 XX 公司"、"看 XX 的工商/股东/有没有官司/有没有被执行/有没有商标专利/有没有经营异常"、"XX 是不是空壳"、"XX 法人是谁"、"XX 注册资本"、"查企查查"、"查企业"等任何企业信息查询需求时，使用此技能。已注册 45 个商业接口（用户需自行在企查查后台逐个申请开通）。零依赖纯 Python，跨平台 Mac/Windows/Linux。
---

# 企查查 OpenAPI 数据查询

企查查 API 工具。**用户用自然语言提需求，AI 在后台调脚本——用户不需要打命令**。

## 你（AI）的工作方式

用户说的话 → 你识别意图 → 你调脚本 → 你把结果用人话回给用户。

| 用户说的 | 你该做的 |
|---|---|
| "查一下腾讯的工商信息" | 调 410（工商基本）；如果用户后续问"详细一点" 再叠 735 |
| "腾讯的法人是谁 / 注册资本多少" | 调 410，从 `OperName` / `RegistCapi` 字段答 |
| "腾讯股东有哪些" | 调 731 |
| "腾讯有没有官司 / 被起诉 / 被执行" | 司法风险全套：740（失信）+741（被执行）+887（裁判文书）+888（开庭）+889（立案），按风险层级答 |
| "腾讯经营异常吗 / 有没有处罚 / 有没有质押" | 经营风险：739（经营异常）+748（严重违法）+865（行政处罚）+751/753（股权质押）|
| "腾讯有什么商标 / 专利" | 231（商标）+ 514（专利）|
| "腾讯最近有什么新闻 / 融资" | 701（舆情）+ 950（融资）|
| "XX 是不是真的（合同对方核验）" | 855（二要素）或 856（三要素，需要法人）|
| "XX 这个公司是空壳吗" | 410 工商 + 884 对外投资 + 732 主要人员，综合判断 |

**自然语言里没说明企业全称时**：先用 886（模糊搜索，0.10 元）拿到完整工商全称，再调具体接口。别让用户打全称。

**金额提醒原则**（默认推荐口径，可调整）：单次调用超 1 元的接口（735/731/213/271/884/758/988/1024/980/958）多个叠用前，先口头说"这几项加起来约 X 元，跑吗"；2 元以下随便跑不用问。

## 资源位置

| 资源 | Mac / Linux | Windows |
|---|---|---|
| Skill 目录 | `~/.claude/skills/kaiyu-qichacha-fetcher/` | `%USERPROFILE%\.claude\skills\kaiyu-qichacha-fetcher\` |
| 凭证文件 | `~/.config/qichacha/credentials.json` | `%USERPROFILE%\.config\qichacha\credentials.json` |
| 缓存目录 | `~/.cache/qichacha/<MD5(企业名)[:16]>/` | `%USERPROFILE%\.cache\qichacha\<MD5(企业名)[:16]>\` |

- 接口注册表: `scripts/api_registry.py`（45 个接口，默认 `opened: False`）
- 官方文档: https://openapi.qcc.com/dataApi
- 控制台: https://openapi.qcc.com/console
- 首次配置: 见 `SETUP.md`（用 `python setup.py` 一键完成）
- 排错手册: `TROUBLESHOOTING.md`

## setup.py 管理命令（用户管理 skill 状态的入口）

**用户不需要手编辑任何文件**。所有维护操作都通过这些命令完成——当用户问相关问题时，**你（AI）应主动跑这些命令**：

| 用户说的 | 你跑的命令 |
|---|---|
| "帮我配置 / 第一次用 / 还没设置" | `python3 setup.py`（交互式录入凭证） |
| "我到底装到哪一步了 / 查一下状态 / 能用了吗" | `python3 setup.py diagnose` |
| "帮我标记 410/740/... 已经开通了" | `python3 setup.py mark-opened 410 740 ...` |
| "取消 XX 的开通标记 / 我退订了 XX 接口" | `python3 setup.py mark-closed 410` |
| "看下我开了哪些接口" | `python3 setup.py list-opened` |
| "测一下凭证对不对 / 跑一次真实请求验证" | `python3 setup.py probe`（扣 ¥0.1） |
| "重新来 / 重置 / 清掉重新配" | `python3 setup.py reset`（需确认） |

`mark-opened` 会修改 `scripts/api_registry.py` 中的 `opened` 字段；写入前会做 Python 语法校验，失败拒绝写入。**用户不应该手编辑这个文件**——出问题都用 `mark-opened` / `mark-closed`。

## 你怎么调脚本（内部实现）

**Python 内联**（推荐，避免子进程开销）：

```python
import os, sys
# 用 expanduser 自动展开 ~ / %USERPROFILE%，跨平台
sys.path.insert(0, os.path.expanduser("~/.claude/skills/kaiyu-qichacha-fetcher/scripts"))
from client import fetch, check_account, QccError

r = fetch("410", keyword="腾讯科技（深圳）有限公司")
if r.ok:
    data = r.data  # 工商详情字典
    # 用 r.data 里的字段写自然语言回复
elif r.status == "":
    pass  # QccError 已经被抛
else:
    # r.ok==False 但没抛——通常是无结果
    pass
```

**Bash / CMD 调 CLI**（备用，输出 JSON 自己解析）：

```bash
# Mac/Linux
python3 ~/.claude/skills/kaiyu-qichacha-fetcher/scripts/qcc.py fetch 410 "腾讯科技（深圳）有限公司"
python3 ~/.claude/skills/kaiyu-qichacha-fetcher/scripts/qcc.py check-account
python3 ~/.claude/skills/kaiyu-qichacha-fetcher/scripts/qcc.py list --opened --md
```

```cmd
:: Windows
python %USERPROFILE%\.claude\skills\kaiyu-qichacha-fetcher\scripts\qcc.py fetch 410 "腾讯科技（深圳）有限公司"
python %USERPROFILE%\.claude\skills\kaiyu-qichacha-fetcher\scripts\qcc.py check-account
```

## 自然语言意图 → ApiCode 映射

按"用户最可能怎么说"组织。多个接口可叠加。

> **注意**：用户必须先在企查查后台 https://openapi.qcc.com/dataApi 逐个申请开通对应接口，开通后跑 `python setup.py mark-opened <code1> <code2> ...` 告诉 skill（**不要让用户手编辑 `api_registry.py`**）。未开通的接口调用会返回 `not_opened` 错误。

### 工商基础（最高频）

| 意图关键词 | ApiCode | 单价 | 该字段在哪 |
|---|---|---|---|
| "工商 / 注册 / 注册资本 / 法人 / 经营范围 / 成立时间" | 410 | 0.20 | `RegistCapi / OperName / Scope / StartDate` |
| "工商详情 / 完整工商 / 实缴 / 参保人数 / 国标行业" | 735 | 2.00 | 比 410 多 30+ 字段 |
| "股东 / 出资 / 持股" | 731 | 2.00 | `Result.[].StockName/StockType/StockPercent` |
| "高管 / 董事 / 监事 / 法人 / 主要人员" | 732 | 0.50 | `Result.[].Name/Job` |
| "分公司 / 分支机构 / 子公司（注：子公司是 884）" | 733 | 0.50 | `Result.[].Name/Address` |
| "变更 / 改过名 / 法人变过吗 / 经营范围改过吗" | 734 | 1.00 | `Result.[].ProjectName/BeforeContent/AfterContent` |
| "年报 / 历年营收 / 历年员工数" | 213 | 1.00 | 按年份列表 |
| "开票 / 税号" | 271 | 1.00 | `TaxpayerNo / RegisterAddress` |
| "二要素 / 名称统一社会信用代码对吗" | 855 | 0.10 | `Result == "一致"` |
| "三要素 / 名称+信用代码+法人对吗" | 856 | 0.20 | 同上 |
| "模糊搜 / 不知道全称 / XX 这家公司" | 886 | 0.10 | `Result.[].Name/KeyNo` |

### 关联族谱

| 意图关键词 | ApiCode | 单价 |
|---|---|---|
| "对外投资 / 投了哪些公司 / 子公司（投资关系）" | 884 | 1.00 |

实控人、股权穿透、企业图谱、控制企业、受益所有人——**这些都是企查查面议类接口**，需联系企查查商务（400-088-8275）单独开通。

### 司法风险（信贷尽调必查）

| 意图关键词 | ApiCode | 单价 |
|---|---|---|
| "失信被执行 / 老赖" | 740 | 0.30 |
| "被执行" | 741 | 0.30 |
| "限高 / 限制高消费" | 742 | 0.50 |
| "股权冻结" | 752 | 0.50 |
| "破产 / 重整" | 761 | 0.50 |
| "判决 / 裁判文书 / 打过官司 / 被起诉" | 887 | 0.30 |
| "开庭" | 888 | 0.50 |
| "立案" | 889 | 0.50 |
| "终本 / 执行不能" | 758 | 1.00 |
| "限制出境" | 988 | 1.00 |
| "法院公告" | 882 | 0.50 |
| "司法拍卖" | 744 | 0.50 |

**推荐预设——信贷尽调司法包**：用户说"看 XX 司法风险"时，**默认跑 740+741+742+752+887+888+889**（共约 3.0 元，前提是这些接口已开通），高级别尽调再加 761+758+988+882+744。

### 经营风险

| 意图关键词 | ApiCode | 单价 |
|---|---|---|
| "经营异常 / 列入异常名录" | 739 | 0.50 |
| "严重违法 / 黑名单" | 748 | 0.50 |
| "行政处罚" | 865 | 0.50 |
| "动产抵押" | 747 | 0.50 |
| "土地抵押" | 745 | 0.50 |
| "股权出质" | 751 | 0.50 |
| "股权质押" | 753 | 0.50 |
| "税收违法" | 756 | 0.50 |
| "欠税" | 757 | 0.50 |
| "对外担保" | 1024 | 1.00 |
| "清算 / 注销中" | 980 | 1.00 |

### 知识产权

| 意图关键词 | ApiCode | 单价 |
|---|---|---|
| "商标" | 231 | 0.30 |
| "专利" | 514 | 0.30 |
| "软著 / 著作权" | 233 | 0.50 |
| "网站备案 / ICP" | 515 | 0.50 |

### 经营信息

| 意图关键词 | ApiCode | 单价 |
|---|---|---|
| "招投标 / 中标" | 958 | 1.00 |
| "资质 / 证书" | 255 | 0.30 |
| "税务信用 / 纳税评级" | 691 | 0.50 |
| "行政许可 / 资质审批" | 892 | 0.50 |

### 企业发展

| 意图关键词 | ApiCode | 单价 |
|---|---|---|
| "新闻 / 舆情 / 最近报道 / 出过事吗" | 701 | 0.50 |
| "融资 / 估值 / 投资人" | 950 | 0.50 |

## 高阶用法：一键批量尽调取数

`scripts/duediligence.py` 是批量编排器——输入企业名，自动跑全部"已开通"的接口，输出 markdown 原料包 + JSON 原始数据 + 调用日志。

```python
import os, sys
sys.path.insert(0, os.path.expanduser("~/.claude/skills/kaiyu-qichacha-fetcher/scripts"))
from duediligence import run_full_dd, render_markdown

report = run_full_dd("腾讯科技（深圳）有限公司")
print(render_markdown(report))
# 或直接 CLI：python3 ~/.claude/skills/kaiyu-qichacha-fetcher/scripts/duediligence.py "企业名" --out ./output
```

**成本预估**（接口全开通的话）：
- 全套约 ¥27（45 个接口，886 + 410 在 build_context 阶段已调）
- 缓存命中后第二次跑：约 ¥0
- 单家全套耗时：约 50 秒

**风险信号汇总口径**（写在 `_build_risk_summary()` 里）：

- **🔴 极高**：740 失信 / 988 限制出境 / 748 严重违法 / 980 清算（任一命中）
- **🟠 高**：741 被执行 / 742 限高 / 752 股权冻结 / 761 破产 / 758 终本 / 739 经营异常
- **🟡 中**：865 行政处罚 / 756 税收违法 / 757 欠税 / 745/747 抵押 / 751/753 股权质押 / 1024 对外担保；**或** 887 裁判文书"被告 ≥3 且 被告比 ≥70%"
- **⚪ 信号**：882 法院公告 / 744 司法拍卖 / 888 开庭 / 889 立案（提示性，不直接定级）

> 这是一个"信贷/担保业务"视角的保守口径。其他业务场景（投前、合规筛查、供应商背调）可能需要自定义评级表——直接改 `_build_risk_summary()` 即可。

## 签名规则（已封装到 client.py，不用手算）

- Header `Token` = `MD5(appkey + Timespan + SecretKey).upper()`（32 位大写）
- Header `Timespan` = Unix 秒
- Query `key` = appkey
- 全部 GET

## 缓存策略

- 默认开启；TTL 按数据时效分级（工商 30-60 天 / 司法 7 天 / 舆情 3 天）
- 同一企业的同一接口在 TTL 内**第二次起免费**
- 用户说"重新查 / 拉最新 / 不要缓存"时用 `use_cache=False`
- 负结果（关键词无匹配）**不写缓存**，避免长期缓存"没查到"

## 错误归类（`QccError.kind`）

捕获到 QccError 后**优先用 `e.friendly()`** ——会返回带中文 label + 行动建议的字符串，可直接转给用户：

```python
try:
    r = fetch("741", keyword="腾讯")
except QccError as e:
    user_message = e.friendly()  # 例如：
    # [接口未开通] [741 被执行人核查] Status=403 接口未开通
    # → 这个接口在企查查后台还没申请开通。去 https://openapi.qcc.com/dataApi/741
    #   点'申请开通'，通过后跑 `python setup.py mark-opened 741`。
```

| kind | 含义 | 友好建议方向 |
|---|---|---|
| `creds` | 凭证错/签名错/必填参数缺 | 跑 `python setup.py` 重新录入 |
| `not_opened` | ApiCode 在 appkey 下没开通 | 申请开通后跑 `python setup.py mark-opened <code>` |
| `no_result` | 关键词无匹配（业务正常） | 用 886 模糊搜索拿全称；或用统一社会信用代码 |
| `rate_limit` | 限流 | 等 1-2 分钟；高频联系企查查商务提升 QPS |
| `network` | DNS/超时/代理 | 详见 TROUBLESHOOTING.md |
| `unknown` | 其他 | 把 `r.raw` 贴给用户 + 引导看 TROUBLESHOOTING.md |

## 注意事项

1. **企业全称要精确**：模糊匹配在不同接口表现不同，先用 886 拿 `KeyNo` 或完整全称再调其他接口
2. **统一社会信用代码兜底**：企业名含全角括号等特殊字符匹配不稳时，用信用代码代替 `keyword`
3. **缓存哈希不可逆**：目录名是 MD5 截断，反查不到企业名；按企业清缓存得自己记录映射
4. **面议类接口**：实控人/股权穿透/企业图谱/受益所有人/财税数据等需联系 400-088-8275 单独议价
5. **接口开通是逐个申请的**：企查查不是开通就能用全部 45 个接口——每个接口要在 openapi.qcc.com/dataApi/{code} 点"申请开通"，可能涉及二次审核或加价。开通后用 `python setup.py mark-opened <code>` 告诉 skill
6. **跨平台**：脚本零第三方依赖，拷贝整个 skill 目录 + 凭证文件即可在 Mac/Windows/Linux 跑

