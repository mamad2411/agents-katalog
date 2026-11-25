---
name: linkfox-walmart-wmtwin
description: 沃师傅(沃尔玛WMTwin)自动化登录与竞品搜索工具。当用户提到沃师傅、wmtwin、www.wmtwin.com、沃尔玛工具、搜竞品、或需要访问沃师傅网站功能时触发此技能。提供自动登录、API调用和竞品搜索功能（支持关键词搜索、WFS筛选、销量范围筛选），所有数据自动解码。
---

# 沃师傅(WMTwin) 自动化登录与竞品搜索

This skill provides automated login, API calling and competitor search capabilities for WMTwin (沃师傅), a Walmart seller tool platform. It handles authentication flow and competitor product search with automatic data decoding.

## Core Concepts

沃师傅(WMTwin) 是沃尔玛卖家工具平台。本技能提供自动化登录、API调用和竞品搜索功能，包括：

### 登录与认证

- **自动登录管理**: 检测登录状态，自动执行登录流程
- **图形验证码**: 需要人工识别，系统会展示图片给用户
- **短信验证码**: 自动发送，用户提供验证码完成登录
- **Session持久化**: 登录成功后保存session，避免重复登录
- **多账号支持**: 每个手机号独立管理session

### 竞品搜索

- **关键词搜索**: 按关键词搜索沃尔玛平台竞品
- **WFS筛选**: 只搜索 Walmart Fulfillment Services 商品
- **销量范围**: 按最小/最大销量筛选产品
- **分页查询**: 支持大量数据的分页获取
- **自动解码**: 所有编码字符自动转换为真实数据
- **自动登录**: 检测登录状态，未登录时自动引导用户登录
- **Session管理**: 自动保存和加载登录状态，支持多账号

## Authentication Flow

```
1. 尝试密码登录
   ├─ 成功 → 保存session，完成
   └─ 失败 (code: 1101) → 需要验证码登录

2. 获取图形验证码
   └─ 展示图片给用户，等待人工识别

3. 发送短信验证码
   └─ 使用图形验证码答案调用发送API

4. 短信验证码登录
   └─ 用户提供短信验证码，完成登录

5. 保存Session
   └─ Session保存在 /tmp/linkfox_wmtwin_sessions/{phone}.json
```

## Important API Rules

### Response Format

沃师傅的API响应格式特殊，需要注意：

**成功响应**:
```json
{
  "code": 1,           // 注意：1表示成功，不是0！
  "msg": "成功",
  "data": {...}
}
```

**失败响应**:
```json
{
  "code": 1101,        // 其他code表示失败
  "msg": "错误信息",
  "data": null
}
```

**判断成功的条件**:
```python
def is_success(result):
    return result.get('code') in [0, 1] and result.get('msg') in ['成功', '操作成功']
```

### Common Error Codes

| Code | 含义 | 处理方式 |
|------|------|---------|
| 1 | 成功 | 正常处理 |
| 1101 | 环境异常，需要验证码登录 | 执行短信登录流程 |
| 1008 | 验证码错误 | 重新获取验证码 |
| 1020 | 短信验证码错误 | 检查验证码或重新发送 |

## API Endpoints

### Authentication APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/login` | POST | 密码登录 |
| `/api/v1/auth/captcha` | GET | 获取图形验证码 |
| `/api/v1/auth/sms-code` | POST | 发送短信验证码 |
| `/api/v1/auth/sms-login` | POST | 短信验证码登录 |

See `references/api.md` for detailed API documentation.

## Usage

### Step-by-Step Login

```python
# 步骤1: 开始登录，获取验证码
python3 scripts/wmtwin_login.py login 13699998888 111111

# 系统会保存验证码图片: /tmp/linkfox_wmtwin_captcha.png
# 用户查看图片并提供答案（例如：24）

# 步骤2: 提供验证码，发送短信
python3 scripts/wmtwin_login.py continue 24

# 系统发送短信到用户手机
# 用户提供短信验证码（例如：123456）

# 步骤3: 完成登录
python3 scripts/wmtwin_login.py continue sms 123456

# 登录成功，session保存在:
# /tmp/linkfox_wmtwin_sessions/13699998888.json
```

### Check Login Status

```python
python3 scripts/wmtwin_login.py check 13699998888
```

### Call API

```python
# GET请求
python3 scripts/wmtwin_login.py api 13699998888 /user/info

# POST请求
python3 scripts/wmtwin_login.py api 13699998888 /order/create POST '{"item":"test"}'
```

## Working with Session

### Session Storage

- **Location**: `/tmp/linkfox_wmtwin_sessions/{phone}.json`
- **Format**: JSON containing cookies, headers, and timestamp
- **Auto-load**: Automatically loaded when calling APIs

### Session Structure

```json
{
  "cookies": {
    "wal": "encoded_session_token"
  },
  "headers": {
    "User-Agent": "...",
    "Content-Type": "application/json"
  },
  "saved_at": "2024-04-28T16:28:08.987745"
}
```

### Cookie Handling

**Important**: 沃师傅返回重复的cookie名称，需要特殊处理：

```python
# 正确方式：避免重复cookie错误
cookies_dict = {}
for cookie in session.cookies:
    cookies_dict[cookie.name] = cookie.value  # 自动覆盖重复项
```

## Password Encryption

密码使用RSA加密传输：

- **Algorithm**: RSA 1024-bit + PKCS1 v1.5 padding
- **Encoding**: Base64
- **Transport**: HTTPS

```python
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDEICVdtxqOCBwHN9a/+YxeXz/B
ZGfduADPfV9dUTW+hGVpIcXU6kBkUdlhVPPdO6n7irK7dxD56m1xG1EmV2RICsvy
W2Y7JVyRRVhun92urbw7TtBcMCCB5SzLI+x1LBUr98SMkMNRQxcnYPkrPj0qGI4v
MC52dJ7z3n6aMf3XoQIDAQAB
-----END PUBLIC KEY-----"""

def encrypt_password(password):
    public_key = RSA.import_key(PUBLIC_KEY)
    cipher = PKCS1_v1_5.new(public_key)
    encrypted_bytes = cipher.encrypt(password.encode('utf-8'))
    return base64.b64encode(encrypted_bytes).decode('utf-8')
```

## Data Decoding

沃师傅API返回的数据使用了Unicode字符编码来混淆数据。本技能提供完整的解码器支持所有编码范围。

### Encoding Ranges

沃师傅使用了4个编码范围，支持两套不同的编码方案：

| 编码范围 | Unicode | 映射 | 用途 | 方案 |
|---------|---------|------|------|------|
| **323** | 单字符 | 小数点 `.` | 价格小数点 | 通用 |
| **324-333** | 10字符 | 数字 0-9 | 简单数字（评论数等） | API方案 |
| **334-385** | 52字符 | A-Z, a-z | 卖家名称、公司名 | API方案 |
| **528** | 单字符 | 小数点 `.` | 价格小数点 | 文档方案 |
| **529-538** | 10字符 | 数字 0-9 | 数字 | 文档方案 |
| **539-564** | 26字符 | 大写 A-Z | 大写字母 | 文档方案 |
| **565-590** | 26字符 | 小写 a-z | 小写字母 | 文档方案 |

### Decoding Examples

```python
# 编码示例
'ņ' (326) → '2'                    # 评论数 (324-333)
'ŒşŖŐ-ŒťŝşŒŠŠ' → 'ERIC-EXPRESS'      # 卖家名 (334-385)
'$ņŅŅńŃňŲ+' → '$2110.4k+'           # 销售额 (323+324-333)
'ȓ' (531) → '2'                    # 数字 (529-538)
'ȟȬȣȝ-ȟȲȪȬȟȭȭ' → 'ERIC-EXPRESS'    # 卖家名 (539-564)
'$ȓȒȒȑȐȕȿ+' → '$2110.4k+'          # 销售额 (528-590)
```

### Using the Decoder

**完整解码器**: `scripts/wmtwin_complete_decoder.py`

```bash
# 解码JSON文件
python3 scripts/wmtwin_complete_decoder.py input.json -o output.json

# 从标准输入解码
cat input.json | python3 scripts/wmtwin_complete_decoder.py - -o output.json
```

**在代码中使用**:

```python
from scripts.wmtwin_complete_decoder import decode_json, decode_json_file

# 方法1: 解码JSON对象
import json
with open('input.json') as f:
    data = json.load(f)
decoded_data = decode_json(data)

# 方法2: 直接解码文件
decoded_data = decode_json_file('input.json', 'output.json')
```

### Decoded Fields

解码器会递归解码JSON中的所有字符串字段，包括：

**基本字段**:
- `number_of_reviews`: 评论数
- `additional_offer_count`: 供应商数
- `sales_volume`: 销量
- `sales_amount`: 销售额

**卖家字段** (`sellers`):
- `display_name`: 卖家显示名称
- `name`: 公司名称
- `seller_reviews`: 卖家评论数
- `seller_rating`: 卖家评分

**销售趋势** (`sales_trends`):
- `sales_amount.label`: 销售额标签（如 `$2110.4k+`）
- `sales_volume.label`: 销量标签（如 `197.0k+`）
- `month_sales_growth`: 月增长
- `gross_profit`: 毛利
- `gross_profit_margin`: 毛利率

### Data Sources

不同数据源可能使用不同的编码方案：

- **API实时数据**: 使用 323-385 范围（方案A）
- **参考文件**: 使用 528-590 范围（方案B）
- **解码器支持**: 同时支持两套方案

### Verification

验证解码是否完整：

```python
# 检查是否还有编码字符
encoded_ranges = [(323, 323), (324, 333), (334, 385), (528, 590)]

def has_encoded_chars(text):
    if not isinstance(text, str):
        return False
    for char in text:
        code = ord(char)
        for start, end in encoded_ranges:
            if start <= code <= end:
                return True
    return False

# 检查解码后的数据
import json
with open('decoded.json') as f:
    data = json.load(f)

# 递归检查所有字符串字段
def check_decoded(obj):
    if isinstance(obj, dict):
        return all(check_decoded(v) for v in obj.values())
    elif isinstance(obj, list):
        return all(check_decoded(item) for item in obj)
    elif isinstance(obj, str):
        return not has_encoded_chars(obj)
    return True

is_fully_decoded = check_decoded(data)
print(f"完全解码: {is_fully_decoded}")
```

## In Conversation Usage

When the user mentions 沃师傅 or related keywords, this skill is automatically triggered. Follow these steps:

1. **Check login status**:
   ```python
   from scripts.wmtwin_login import load_session
   session = load_session(phone)
   ```

2. **If not logged in, guide the user**:
   - Start login process
   - Display CAPTCHA image to user
   - Ask user for CAPTCHA answer
   - Send SMS code
   - Ask user for SMS code
   - Complete login

3. **Call API with session**:
   ```python
   from scripts.wmtwin_login import call_api
   result = call_api(phone, endpoint, method, data)
   ```

## Best Practices

1. **Always check login before API calls** - Avoid 401/403 errors
2. **Show CAPTCHA image to user** - Human input required for graphical CAPTCHA
3. **Clear error messages** - Guide user through each step
4. **Session reuse** - Don't login repeatedly if session exists
5. **Multi-account support** - Each phone number has independent session

## Debugging

### View CAPTCHA

```bash
# macOS
open /tmp/linkfox_wmtwin_captcha.png

# Or in conversation
"帮我查看验证码图片"
```

### View Session

```bash
cat /tmp/linkfox_wmtwin_sessions/13699998888.json | python3 -m json.tool
```

### Clear Session

```bash
rm /tmp/linkfox_wmtwin_sessions/13699998888.json
```

## Security

- ✅ Password encrypted with RSA before transmission
- ✅ HTTPS communication only
- ✅ No plaintext password storage
- ✅ Local session storage
- ✅ Support for session cleanup

## Performance

| Operation | Time |
|-----------|------|
| Password login attempt | < 2s |
| Get CAPTCHA | < 1s |
| Send SMS code | < 2s |
| SMS login | < 2s |
| API call (logged in) | < 2s |

## Limitations

- **CAPTCHA recognition**: Requires human input (no auto-recognition yet)
- **SMS verification**: User must manually provide SMS code
- **Session expiry**: Session may expire, requiring re-login

## Competitor Search

### Usage

搜索沃尔玛竞品，支持多种筛选条件。**集成自动登录功能**，无需手动管理登录状态。

#### ✨ 自动分页功能

**新功能**：当请求的数据量大于API单页限制（50条）时，脚本会自动查询多页并合并结果：

```bash
# 自动获取100条数据（自动查询2页）
python3 scripts/wmtwin_search_competitors.py \
    --keyword "iphone case" \
    --phone 15625238480 \
    --page-size 100 \
    -o results.json
```

**特性：**
- ✅ 自动检测请求数量是否超过单页限制（50条）
- ✅ 自动查询多页直到达到目标数量
- ✅ 自动合并多页结果为单个JSON文件
- ✅ 显示实时查询进度（已获取/目标总数）
- ✅ 支持所有筛选条件

#### 自动登录流程

调用搜索 API 时会自动：
1. 检查是否有有效的登录 session
2. 如果没有 session，引导用户登录
3. 登录成功后自动保存 session
4. 下次自动加载已保存的 session
5. 如果 session 过期，自动重新登录

#### Python 代码

```python
from scripts.wmtwin_search_competitors import WMTwinCompetitorSearch

# 创建搜索客户端（提供手机号会自动加载已有登录）
client = WMTwinCompetitorSearch(phone="13699998888")

# 方法1: 使用参数字典（自动检查登录）
params = {
    "keyword": "iphone case",
    "is_wfs": True,
    "min_sales_volume": 200,
    "max_sales_volume": 800,
    "min_sales_amount": 200,
    "max_sales_amount": 800,
    "min_number_of_reviews": 50,
    "max_number_of_reviews": 100,
    "min_average_rating": 1.0,
    "max_average_rating": 5.0,
    "min_price": 1.0,
    "max_price": 10.0,
    "seller_name": "ERIC-EXPRESS",
    "brand": "Simyoung",
    "page": 1,
    "pageSize": 10
}
results = client.search_from_params(params)

# 方法2: 直接调用（自动检查登录）
results = client.search_competitors(
    keyword="iphone case",
    is_wfs=True,
    min_sales_volume=200,
    max_sales_volume=800,
    min_sales_amount=200,
    max_sales_amount=800,
    min_number_of_reviews=50,
    max_number_of_reviews=100,
    min_average_rating=1.0,
    max_average_rating=5.0,
    min_price=1.0,
    max_price=10.0,
    seller_name="ERIC-EXPRESS",
    brand="Simyoung",
    page=1,
    page_size=10
)

# 方法3: 提供登录信息（首次登录）
results = client.search_competitors(
    keyword="iphone",
    phone="13699998888",
    password="your_password",  # 可选，不提供会提示输入
    is_wfs=True
)

# 方法4: 自动分页获取大量数据（推荐）
results = client.search_multiple_pages(
    total_count=100,  # 自动查询多页直到获取100条
    keyword="iphone case",
    phone="15625238480",
    is_wfs=True,
    min_sales_volume=200
)
print(f"共获取 {len(results['data']['list'])} 条数据")

# 使用解码后的数据
for product in results['data']['list']:
    print(f"产品: {product['title']}")
    print(f"价格: {product['price']}")
    print(f"卖家: {product['sellers'][0]['display_name']}")
    print(f"销量: {product['sales_trends'][0]['sales_volume']['label']}")
```

#### 命令行

```bash
# 基本搜索（会自动检查登录，需要时提示登录）
python3 scripts/wmtwin_search_competitors.py --keyword "iphone"

# 提供手机号（自动加载已有登录）
python3 scripts/wmtwin_search_competitors.py --keyword "iphone" --phone 13699998888

# 完整参数（自动管理登录）
python3 scripts/wmtwin_search_competitors.py \
    --keyword "iphone case" \
    --phone 13699998888 \
    --seller-name "ERIC-EXPRESS" \
    --brand "Simyoung" \
    --is-wfs \
    --min-sales 200 \
    --max-sales 800 \
    --min-sales-amount 200 \
    --max-sales-amount 800 \
    --min-reviews 50 \
    --max-reviews 100 \
    --min-rating 1.0 \
    --max-rating 5.0 \
    --min-price 1.0 \
    --max-price 10.0 \
    --page 1 \
    --page-size 10

# 模拟模式（无需登录，用于测试）
python3 scripts/wmtwin_search_competitors.py --keyword "iphone" --mock

# 从 JSON 文件读取参数
python3 scripts/wmtwin_search_competitors.py --from-json params.json --phone 13699998888

# 保存结果（自动保存原始和解码两个文件）
python3 scripts/wmtwin_search_competitors.py --keyword "iphone" --phone 13699998888 -o results.json
# 这将保存：
#   - results_raw.json (原始编码数据)
#   - results.json (解码后的数据)
```

**重要说明**：
- 当使用 `-o` 参数保存文件时，会自动保存两个文件：
  - `<filename>_raw.json` - 原始编码数据（API直接返回的数据）
  - `<filename>.json` - 解码后的数据（所有字符已解码）
- 后续操作始终使用解码后的文件
- 解码过程自动进行，无需手动操作

### 搜索参数

| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| keyword | string | 是 | 搜索关键词 | "iphone" |
| is_wfs | boolean | 否 | 只搜索 WFS 商品 | true |
| min_sales_volume | integer | 否 | 最小销量 | 4000 |
| max_sales_volume | integer | 否 | 最大销量 | 90000 |
| min_sales_amount | integer | 否 | 最小销售额 | 200 |
| max_sales_amount | integer | 否 | 最大销售额 | 800 |
| min_number_of_reviews | integer | 否 | 最小评论数 | 50 |
| max_number_of_reviews | integer | 否 | 最大评论数 | 100 |
| min_average_rating | float | 否 | 最低评分（1-5） | 1.0 |
| max_average_rating | float | 否 | 最高评分（1-5） | 5.0 |
| min_price | float | 否 | 最低价格 | 1.0 |
| max_price | float | 否 | 最高价格 | 10.0 |
| seller_name | string | 否 | 卖家名称 | "ERIC-EXPRESS" |
| brand | string | 否 | 品牌 | "Simyoung" |
| page | integer | 否 | 页码（从1开始） | 1 |
| pageSize | integer | 否 | 每页数量 | 10 |

### 返回数据结构

返回的数据结构与登录后调用其他 API 相同，包含产品列表、卖家信息、销售数据等。所有编码字符会自动解码。

详细数据结构和字段说明见 `references/competitor_search.md`。

### 自动解码

沃师傅使用 Unicode 字符编码数据，本工具会自动解码：

| 编码示例 | 解码结果 | 类型 |
|---------|---------|------|
| ȟȬȣȝ-ȟȲȪȬȟȭȭ | ERIC-EXPRESS | 卖家名称 |
| $ȒȓȐȔȘ | $12.37 | 价格 |
| ȓȑȑ+ | 200+ | 数量 |
| $ȓȒȒȑȐȕȿ+ | $2110.4k+ | 销售额 |

### 常见用法示例

```python
# 1. 搜索高销量产品
results = client.search_competitors(
    keyword="phone case",
    min_sales_volume=10000,
    page_size=50
)

# 2. 只搜索 WFS 商品
results = client.search_competitors(
    keyword="iphone",
    is_wfs=True
)

# 3. 特定销量区间
results = client.search_competitors(
    keyword="charger",
    min_sales_volume=5000,
    max_sales_volume=50000
)

# 4. 按评论数和评分筛选
results = client.search_competitors(
    keyword="iphone case",
    min_number_of_reviews=50,
    max_number_of_reviews=100,
    min_average_rating=4.0,
    max_average_rating=5.0
)

# 5. 按价格范围筛选
results = client.search_competitors(
    keyword="phone charger",
    min_price=5.0,
    max_price=20.0
)

# 6. 按卖家和品牌筛选
results = client.search_competitors(
    keyword="iphone case",
    seller_name="ERIC-EXPRESS",
    brand="Simyoung"
)

# 7. 综合筛选（多条件组合）
results = client.search_competitors(
    keyword="iphone case",
    is_wfs=True,
    min_sales_volume=200,
    max_sales_volume=800,
    min_price=1.0,
    max_price=10.0,
    min_number_of_reviews=50,
    max_number_of_reviews=100,
    min_average_rating=1.0,
    max_average_rating=5.0,
    seller_name="ERIC-EXPRESS",
    brand="Simyoung",
    page=1,
    page_size=10
)

# 8. 分页获取所有数据
all_products = []
page = 1
while True:
    results = client.search_competitors(
        keyword="iphone",
        page=page,
        page_size=50
    )
    products = results['data']['list']
    if not products:
        break
    all_products.extend(products)
    page += 1
```

### 命令行用法示例

```bash
# 基本搜索
python3 scripts/wmtwin_search_competitors.py --keyword "iphone case" --phone 15625238480

# 多条件筛选
python3 scripts/wmtwin_search_competitors.py \
    --keyword "iphone case" \
    --phone 15625238480 \
    --seller-name "ERIC-EXPRESS" \
    --brand "Simyoung" \
    --is-wfs \
    --min-sales 200 \
    --max-sales 800 \
    --min-sales-amount 200 \
    --max-sales-amount 800 \
    --min-reviews 50 \
    --max-reviews 100 \
    --min-rating 1.0 \
    --max-rating 5.0 \
    --min-price 1.0 \
    --max-price 10.0 \
    --page 1 \
    --page-size 10 \
    -o results.json
```

## References

- **API Documentation**: See `references/api.md`
- **Competitor Search API**: See `references/competitor_search.md`
- **Auto Login Guide**: See `AUTO_LOGIN.md`
- **Competitor Search Quick Start**: See `COMPETITOR_SEARCH.md`
- **Login Script**: See `scripts/wmtwin_login.py`
- **Search Script (with Auto Login)**: See `scripts/wmtwin_search_competitors.py`
- **Decoder**: See `scripts/decode_api_json.py`
- **Quick Start**: See `QUICKSTART.md`
- **Complete Guide**: See `README.md`
