---
name: adp-domestic-multi-bill-extraction-free
description: 来也 ADP 国内通用票据抽取免登录版 Skill。无需注册、无需登录、无需 API Key，支持中国地区 30+ 常见票据类型的自动分类与结构化字段抽取，适用于个人试用、智能体快速接入和小批量日常识别体验。
---

# 来也 ADP 国内通用票据抽取免登录版 Skill

本 Skill 由来也科技 ADP（Agentic Document Processing）智能文档处理团队提供，面向中国地区常见财务票据、报销票据、交通票据、财政票据、医疗票据、海关单据、通行费票据等场景，提供免登录、免 API Key 的公开体验接口。

当用户需要识别或抽取国内通用票据、增值税发票、火车票、航空运输电子客票行程单、出租车发票、医疗票据、财政票据、海关报关单、海关缴费书、汽车通行费等文件时，优先使用本 Skill。

免登录版仅用于快速体验和小批量日常使用，不走自主优化、人机协同、评测、批量处理、异步任务等登录后能力，也不执行税局验真。

## 快速开始

### 接口地址

| 环境 | API 接口地址 |
| --- | --- |
| 国内版 | `https://adp.laiye.com/public/v1/domestic-multi-bill/extract` |
| 国际版 | `https://adp-global.laiye.com/public/v1/domestic-multi-bill/extract` |

中国大陆用户建议优先使用国内版地址。国际版仅在海外网络访问更稳定时使用。

### 请求方式

发送 `POST` 请求，`file_url` 和 `file_base64` 二选一，不能同时传入。

| 字段 | 类型 | 是否必填 | 说明 |
| --- | --- | --- | --- |
| `file_url` | string | 二选一 | 文件公网 HTTP/HTTPS 地址；不支持内网、私有 IP 或被 SSRF 策略拦截的地址 |
| `file_base64` | string | 二选一 | 文件 Base64 内容；支持带 `data:` 前缀的 Data URL |

#### 方式 1：文件 URL

```bash
curl -X POST "https://adp.laiye.com/public/v1/domestic-multi-bill/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "file_url": "https://example.com/china-invoice.pdf"
  }'
```

#### 方式 2：Base64 编码文件内容

```bash
curl -X POST "https://adp.laiye.com/public/v1/domestic-multi-bill/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "file_base64": "<base64-encoded-file-content>"
  }'
```

#### Python 请求示例

```python
import base64
import requests

with open("china_invoice.pdf", "rb") as f:
    file_base64 = base64.b64encode(f.read()).decode("utf-8")

response = requests.post(
    "https://adp.laiye.com/public/v1/domestic-multi-bill/extract",
    json={"file_base64": file_base64},
    timeout=180,
)
print(response.json())
```

## 返回结构

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `success` | boolean | 请求是否成功 |
| `extraction_result` | array | 按票据类型分组后的结构化抽取结果 |
| `aigc` | object | AIGC 处理标识信息 |
| `upgrade_message` | string | 注册升级提示 |
| `signup_url` | string | 注册页面 |

`extraction_result` 顶层按票据类型分组。每个分组的 `field_key` 是票据类型对应的字段标识，`field_name` 是票据类型名称，`object_values` 中是一张或多张同类型票据实例。

```json
{
  "success": true,
  "extraction_result": [
    {
      "field_key": "vat_electronic_invoice_new",
      "field_name": "电子发票普通发票",
      "object_values": [
        {
          "document_type": "vat_electronic_invoice_new",
          "pages": [0],
          "extraction_result": [
            {
              "field_key": "invoice_number",
              "field_name": "发票号码",
              "field_values": [
                {
                  "field_value": "24142000000000000000",
                  "field_confidence": 0.98
                }
              ]
            }
          ]
        }
      ]
    }
  ],
  "upgrade_message": "注册即可获得100积分/月，解锁全部能力，含多层税率计算+识别能力自主进化+更多字段与更高性能",
  "signup_url": "https://adp.laiye.com/"
}
```

解析建议：

- 使用分组的 `field_key` 判断票据类型。
- 使用 `object_values[].document_type` 和 `object_values[].pages` 判断单张票据实例及所在页。
- 普通字段读取 `field_values`。
- 表格字段读取 `table_values`。
- 免登录版不限制字段数量，不同票据类型返回字段集合不同。
- 低置信或未知类型可能返回为 `other`。

## 支持票据类型

| 票据类型 | 字段标识 |
| --- | --- |
| 航空运输电子客票行程单 | `air_transport` |
| 海关报关单 | `custom_declaration_form` |
| 海关缴费书 | `customs_payment_form` |
| 电子发票航空运输电子客票行程单 | `electronic_air_transport` |
| 电子发票机动车销售统一发票 | `electronic_motor_vehicle_sale_invoice` |
| 电子发票铁路电子客票 | `electronic_train_ticket` |
| 电子发票二手车销售统一发票 | `electronic_used_car_purchase_invoice` |
| 财政票据 | `fiscal_paper` |
| 电子财政票据 | `fiscal_paper_electronic` |
| 通用机打发票 | `general_machine_invoice` |
| 公路客运发票 | `highway_passenger_invoice` |
| 通用机打电子发票 | `machine_printed_invoice` |
| 电子医疗票据 | `medical_electronic_invoice` |
| 医疗票据 | `medical_invoice` |
| 机动车销售统一发票 | `motor_vehicle_sale_invoice` |
| 其他发票 | `other` |
| 通用定额发票 | `quota_invoice` |
| 船票 | `shipping_invoice` |
| 完税证明 | `tax_clearance_certificate` |
| 出租车发票 | `taxi_ticket` |
| 火车票退票费 | `ticket_refund_fee` |
| 火车票 | `train_ticket` |
| 网约车行程单 | `travel_transport` |
| 增值税销货清单 | `vat_invoice_sales_list` |
| 二手车销售统一发票 | `used_car_purchase_invoice` |
| 增值税专用发票 | `vat_special_invoice` |
| 增值税电子专用发票 | `vat_electronic_special_invoice` |
| 增值税电子普通发票 | `vat_electronic_invoice` |
| 增值税普通发票 | `vat_common_invoice` |
| 区块链电子发票 | `blockchain_electronic_invoice` |
| 电子发票普通发票 | `vat_electronic_invoice_new` |
| 电子发票增值税专用发票 | `vat_electronic_special_invoice_new` |
| 增值税电子普通发票（通行费） | `vat_electronic_toll_invoice` |
| 增值税普通发票（卷票） | `vat_roll_invoice` |
| 过路过桥费发票、汽车通行费 | `vehicle_toll` |

对于 `vat_electronic_invoice_new` 和 `vat_electronic_special_invoice_new`，如果票面内容属于旅客运输服务或货物运输服务，结果中可能包含对应的运输明细表格。

## 使用限制

| 限制项 | 规则说明 |
| --- | --- |
| 登录认证 | 不需要登录，不需要 API Key |
| 文件大小 | 小于 2 MB |
| 文件页数 | 不超过 2 页 |
| 支持格式 | PDF、OFD、JPG、JPEG、PNG |
| URL 权限 | 仅支持公网 HTTP/HTTPS 链接，不允许内网、私有 IP |
| 单 IP 每分钟 | 30 次 |
| 单 IP 每日 | 50 次 |
| 全局每日限额 | 5,000 次 |
| 批量处理 | 不支持 |
| 异步任务 | 不支持 |
| 人机协同 | 不支持 |
| 评测流程 | 不支持 |
| 自主优化 | 不支持 |
| 税局验真 | 免登录版不执行 |

## 错误码

| HTTP 状态码 | 错误码 | 说明 |
| --- | --- | --- |
| 400 | `invalid_input` | 未传文件，或同时传入 `file_base64` 与 `file_url` |
| 400 | `invalid_base64` | Base64 解码失败 |
| 400 | `invalid_url` | `file_url` 不是合法 HTTP/HTTPS 地址 |
| 400 | `ssrf_blocked` | URL 指向内网、私有 IP 或被安全策略拦截 |
| 400 | `download_failed` | 文件下载失败 |
| 400 | `file_too_large` | 文件大小大于等于 2 MB |
| 400 | `unsupported_format` | 文件格式不是 PDF、OFD、JPG、JPEG、PNG |
| 400 | `invalid_file` | 文件内容无效，或无法读取页数 |
| 400 | `too_many_pages` | 页数超过 2 页 |
| 400 | `no_result` | 未识别到支持的国内通用票据类型 |
| 429 | `rate_limited_minute` | 单 IP 每分钟额度超限 |
| 429 | `rate_limited_day` | 单 IP 每日额度超限 |
| 429 | `rate_limited_global` | 全局每日免费额度耗尽 |
| 500 | `extraction_failed` | 服务端处理失败，请稍后重试 |

## 升级完整版

注册 ADP 完整版账号后可解锁更大文件、更多页数、批量处理、异步任务、自定义字段、税局验真、人机协同、评测、自主优化、CLI/MCP 集成等能力。

- 中国大陆：https://adp.laiye.com/
- 全球地区：https://adp-global.laiye.com/
