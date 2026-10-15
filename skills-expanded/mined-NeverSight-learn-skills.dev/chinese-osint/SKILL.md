---
name: chinese-osint
description: Search for individuals on Chinese internet using limited info (name, phone, QQ). Covers QQ profile extraction, social media search, cross-verification, and platform-specific pitfalls.
version: 2.0.0
author: Open Source Community
license: MIT
---

# Chinese OSINT — 国内人员数字足迹搜索

根据有限信息（姓名、手机号、QQ号、昵称等）在中国互联网上查找特定人员的公开信息。

> **适用场景**：安全研究、失联人员寻找、防诈骗核实、社交媒体调查。
> **前置要求**：Python 3.8+，见 [requirements.txt](requirements.txt) 和各脚本头部的安装说明。

## 工具优先级（从高效到低效）

### Tier 1：直接API（最快，无需浏览器）

| 目标 | 方法 | 注意事项 |
|------|------|----------|
| QQ头像 | `https://q1.qlogo.cn/g?b=qq&nk={QQ号}&s=640` | 直接返回JPEG，Last-Modified可见更新时间 |
| QQ昵称 | `https://r.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?uins={QQ号}` | **2026年4月起全部要求登录**，已无法匿名获取 |
| QQ空间头像 | `https://qlogo3.store.qq.com/qzone/{QQ号}/{QQ号}/640` | 可能与QQ头像不同 |
| QQ空间可见性 | 尝试访问空间URL，封闭则需登录 | 封闭=完全无法获取内容 |
| QQ注册时间 | 第三方API（见下方详解） | 免费API可精确到秒，号段估算可到年份 |
| 手机号归属 | 前3位=运营商，前4-7位=城市段 | 无需API，对照表即可 |
| B站用户搜索 | `api.bilibili.com/x/web-interface/search/type` | 需先访问首页获取cookie |

**QQ注册时间查询（两种方式）**：

方式一：第三方API（精确到秒）
```bash
# 使用脚本一键查询（含昵称、等级、注册时间、注册天数等）
python scripts/qq_info.py --qq 123456789
```

| API | 地址 | 免费额度 | 返回数据 |
|-----|------|----------|----------|
| 小渡API | `openapi.dwo.cc/api/fh_zcsj` | 需注册获取ckey，2次/分 | 昵称、等级、注册时间、注册天数、头像修改时间、会员状态 |
| 76.al | `api.76.al/api/qq/query` | 需注册获取key | Q龄、注册时间 |
| 52api.cn | `52api.cn` | 免费10000次/天，需实名 | QQ等级、社交活跃度、注册时长 |

**注意**：第三方API需要注册获取key，接口可能随时变更。脚本默认使用小渡API。

方式二：号段估算（无需API，精度为年份）

| 号码位数 | 大致注册时间段 | 说明 |
|---------|-------------|------|
| 5位 | 1999年 | 最早批次（10001=马化腾） |
| 6位 | 2000-2001年 | 5位号用完后推出 |
| 7位 | 2001-2003年 | QQ用户快速增长期 |
| 8位 | 2003-2005年 | 大规模普及期 |
| 9位 | 2005-2009年 | 2006年开始流行 |
| 10位 | 2009年至今 | 2008年底开始发放 |
| 11位 | 2012年至今 | 部分新注册用户 |

**注意**：QQ号为随机分配（非严格递增），回收号/靓号等可能偏离此表。仅作为粗略参考。

**快速验证QQ号是否存在**：
```bash
python scripts/qq_avatar.py --qq 123456789
```

### Tier 2：本地 Playwright 浏览器自动化（**通用最有效方式**）

本地 Playwright + stealth 插件可以访问大部分中国社交平台，**这是不依赖任何云服务的通用方案**。

**安装**：
```bash
pip install playwright playwright-stealth
playwright install chromium
```

**搜索引擎搜索**（绕过大部分CAPTCHA）：

| 搜索引擎 | 可用性 | 说明 |
|----------|--------|------|
| Bing (cn.bing.com) | ✅ 可靠 | 无登录要求，中文搜索首选 |
| 百度 (baidu.com) | ⚠️ 偶发CAPTCHA | 搜索手机号关联企业可用 |
| DuckDuckGo HTML | ⚠️ 有限 | 中文查询成功率约50%，需URL编码 |
| 360搜索 | ⚠️ 偶尔成功 | 结果质量低 |

**Bing搜索技巧**：
- 搜索词带引号提高精度：`"<nickname>" <city>`
- `site:` 限定域名：`site:weibo.com "<nickname>"`、`site:douyin.com "<nickname>"`
- 搜索结果中 `.b_caption p` 包含摘要文本（最有价值的信息）

**DuckDuckGo HTML搜索**（无需浏览器）：
```python
import requests, urllib.parse
from bs4 import BeautifulSoup

encoded_query = urllib.parse.quote("<nickname> <city>")
url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
soup = BeautifulSoup(resp.text, 'html.parser')
for result in soup.select('.result'):
    title = result.select_one('.result__title a')
    snippet = result.select_one('.result__snippet')
    if title:
        print(f"{title.text.strip()}: {snippet.text.strip() if snippet else ''}")
```

### Tier 2.5：微博一次性窗口抓取

本地 Playwright + stealth 可以访问 m.weibo.cn，**但只有首次加载有效**，后续请求立即触发点击验证码。

**核心策略：一次加载，全部拦截**

```python
from playwright.async_api import async_playwright
from playwright_stealth import Stealth

# 1. 拦截API响应（最重要 — 在CAPTCHA触发前获取数据）
api_data = []
async def on_response(resp):
    if 'container/getIndex' in resp.url:
        data = await resp.json()
        cards = data.get('data', {}).get('cards', [])
        for card in cards:
            mblog = card.get('mblog', {})
            # 原创判断：not mblog.get('retweeted_status')
            # region_name: "发布于 <province>"  ← 极其重要的定位信息
            # pic_ids: 图片ID列表（但图片本身被防盗链）
            # source: "iPhone客户端"
            api_data.append(mblog)

page.on('response', on_response)
```

**关键发现**：
- containerid `107603{uid}` = 微博列表（含region_name等详细字段）
- containerid `100505{uid}` = 用户主页信息
- `region_name` 是定位利器（如"发布于 XX省"，可定位用户当前所在地）
- 首次加载成功后，**不要再请求任何微博页面** — 验证码一旦触发，整个session作废
- 微博图片(sinaimg.cn)有严格防盗链，即使用浏览器下载也返回403 — 只能截图保存
- 滚动翻页大概率触发验证码，不如只拿首页10条数据就停止

**图片获取变通方案**：用 `page.screenshot()` 截图保存页面中的图片，而非直接下载CDN图片。

**一键抓取**：
```bash
python scripts/weibo_scraper.py --uid 1234567890
```

### Tier 3：本地curl（**命中率≈0%，不要浪费时间**）

| 目标 | 结果 | 原因 |
|------|------|------|
| Bing | ❌ CAPTCHA | 需浏览器环境 |
| Baidu | ❌ CAPTCHA | 需浏览器环境 |
| Sogou | ❌ 空结果 | 对中文查询无效 |
| DuckDuckGo HTML | ⚠️ 偶尔有效 | 中文结果差 |
| Yandex | ❌ CAPTCHA | 需浏览器环境 |
| 360搜索 | ⚠️ 偶尔成功 | 结果质量低 |
| Weibo API | ❌ HTTP 432 | 需浏览器cookie |
| 小红书API | ❌ `{"code":-1}` | 需登录 |
| 抖音API | ❌ 空结果 | 需登录 |

**结论：所有搜索任务优先用 Playwright 浏览器自动化，不要在curl上浪费时间。**

### Tier 3.5：各平台直接访问情况

当通过浏览器自动化访问各平台时：

**必做前提**：先访问 `m.weibo.cn/` 建立cookie，否则微博直接弹验证码。

| 平台 | 结果 | 陷阱 |
|------|------|------|
| Bing (cn.bing.com) | ✅ 可靠 | 无登录要求，中文搜索首选 |
| 百度 (baidu.com) | ⚠️ 偶发CAPTCHA | 搜索手机号关联企业可用 |
| 微博 m.weibo.cn | ⚠️ 首次有效 | **一次窗口**：首次加载成功，后续请求立即触发验证码 |
| 抖音 douyin.com | ⚠️ 有限 | IP属地可见，但粉丝数/获赞数被隐藏需登录 |
| 小红书 | ❌ 需登录 | 搜索功能完全需登录 |
| QQ空间 | ❌ 需登录 | 非好友空间为空白页 |
| B站 space.bilibili.com | ✅ 可靠 | 用户详情公开可见（学校、签名、粉丝数等） |
| 天眼查/爱企查 | ❌ 地理围栏 | 海外IP显示"暂不支持访问"，不可绕过 |

## 关键陷阱

### 1. 视觉AI分析图片的局限性

视觉AI模型对本地文件路径分析不稳定，优先使用URL直接分析。

**替代方案**：下载头像后用PIL/numpy做基础分析（颜色丰富度、肤色占比、边缘密度）：

```bash
python scripts/avatar_analysis.py --url "https://q1.qlogo.cn/g?b=qq&nk=QQ号&s=640"
```

```python
from PIL import Image, ImageFilter
import numpy as np
img = Image.open('/tmp/avatar.jpg')
arr = np.array(img)
unique_colors = len(np.unique(arr.reshape(-1, 3), axis=0))  # >50000≈照片, <5000≈插画
skin_pct = ((arr[:,:,0]>150)&(arr[:,:,0]<255)&(arr[:,:,1]>80)&(arr[:,:,1]<200)&(arr[:,:,2]>50)&(arr[:,:,2]<180)).sum()/(arr.shape[0]*arr.shape[1])*100  # >20%≈真人
edge_intensity = np.array(img.filter(ImageFilter.FIND_EDGES)).mean()  # >8≈照片细节
```

### 2. QQ昵称GBK编码Bug

```python
# users.qzone.qq.com 返回的昵称数据编码混乱
# 示例hex: efbfbd efbfbd c8a6 c8a6
# efbfbd = UTF-8 replacement char（数据已在服务器端损坏）
# 后面的bytes用GBK解码可得到部分正确汉字
# 解决：对原始bytes分别用 UTF-8 和 GBK 解码，取可读部分拼合
```

### 3. Vision API 误判真实照片

- 街拍/时尚照片经常被误判为"二次元动漫风"
- **不能依赖视觉AI判断头像是否真人**
- 必须由人工确认

### 4. XLSX解析（无openpyxl时）

```python
import zipfile, xml.etree.ElementTree as ET
z = zipfile.ZipFile('file.xlsx')
ss = z.read('xl/sharedStrings.xml')
root = ET.fromstring(ss)
ns = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
strings = []
for si in root.findall(f'{ns}si'):
    t = si.find(f'{ns}t')
    if t is not None:
        strings.append(t.text or '')
```

### 5. **同名同姓极度常见**

- 常见昵称在多个平台可能有多人使用
- **生日是最佳区分因子**
- 必须用多维度交叉验证：生日+城市+教育经历+职业
- **微博 region_name 是极好的定位信号**，可以确认用户当前所在地
- 排除标准：IP属地、简介信息（学校/职业）、年龄感、内容风格

## 标准搜索流程

```
1. QQ号 → 头像+空间可见性（Tier 1 API直接获取）
2. 昵称 → 用昵称跑sherlock+maigret批量枚举平台，再用搜索引擎搜抖音/小红书/微博
3. 姓名+城市 → Playwright搜索Bing/百度、查天眼查快照（Tier 2）
4. 手机号 → 确认归属地+企业关联搜索（注意：多为数据污染，不代表真实工作关系）
5. Wayback Machine → CDX API查历史快照（成功率低，可跳过）
6. 交叉验证 → 用生日/城市/教育/年龄排除同名同姓
```

### QQ昵称提取实战经验

**2026年4月起QQ昵称API全部失效**：`r.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg` 等接口都返回登录要求，不再支持匿名查询。

**替代方案**（按可靠性排序）：
1. 让用户直接看QQ上的昵称（最可靠）
2. 第三方QQ查询网站（大多数已下线或返回空数据）
3. QQ空间页面title（封闭空间只显示"QQ空间-分享生活，留住感动"，不含昵称）
4. 搜索引擎缓存（QQ号+昵称的关联信息可能被索引过）

### "番番寻客宝"/企业关联 = 数据污染

手机号在百度搜索中出现企业关联（番番寻客宝/寻客宝），这些是百度企业黄页爬虫批量抓取的结果：
- 号码出现在多家不相关公司（跨省/跨行业）→ 大概率是数据污染
- 判断标准：企业地域是否和目标人物活动轨迹匹配
- **不能作为工作经历证据**，但可辅助确认号码归属地

### 昵称跨平台搜索经验

用QQ昵称做跨平台搜索时：
1. **sherlock + maigret** 先跑一遍，能快速枚举210+平台的注册情况
2. 同名用户极多，必须交叉验证
3. 排除标准：IP属地、简介信息（学校/职业）、年龄感、内容风格
- **B站空间页面（space.bilibili.com）无需登录即可看到**：用户名、签名、学校、Instagram、粉丝/关注数
- **常见昵称在搜索引擎中完全无法定位**，需用户手动在微信/支付宝验证手机号
- **微博防盗链极严**：sinaimg.cn图片即使用浏览器也返回403，只能截图保存

## 用户手动操作（自动化无法替代）

| 操作 | 方法 | 信息获取 |
|------|------|----------|
| 微信搜手机号 | 微信→添加朋友→手机号 | 头像、朋友圈（若公开） |
| 支付宝验证 | 转账0.01元到手机号 | 显示姓名最后一个字 |
| QQ访问空间 | 用自己QQ访问对方空间 | 可能需加好友 |
| 微博私信 | 在找到的微博发私信 | 直接联系 |

## 自动化工具

### Maigret（跨平台用户名搜索）
```bash
# 搜210+平台
pip install maigret
maigret "<username>" --no-color --timeout 15 --top-sites 200
```
- 覆盖平台：YouTube, Wikipedia, Discord, Minecraft, TikTok等210+主流平台
- 局限：不支持微信/微博/小红书/抖音等中国封闭平台（这些需Playwright浏览器自动化）
- 常见问题：中文用户名在部分平台报"Illegal Username Format"（正常）

### Sherlock（辅助用户名搜索）
```bash
pip install sherlock-project
sherlock "<username>" --no-color --timeout 10 --print-found
```
- 覆盖400+平台，与Maigret互补
- 对中文用户名误报率较高（需逐个验证）

### Bilibili API（直接可用，无需登录）
```bash
# 用户搜索（需先获取buvid3 cookie）
curl -s "https://www.bilibili.com" -c /tmp/bili_cookie.txt
curl -s "https://api.bilibili.com/x/web-interface/search/type?search_type=bili_user&keyword=<username>" \
  -H "Referer: https://www.bilibili.com" -b /tmp/bili_cookie.txt

# 用户详情
curl -s "https://api.bilibili.com/x/web-interface/card?mid=<mid>" \
  -H "Referer: https://www.bilibili.com"
```

### 反向图片搜索
- **百度识图**：`image.baidu.com`（需浏览器，本地curl不行）
- **Yandex Images**：`yandex.com/images`（对人脸识别较好）
- **头像MD5比对**：下载头像计算MD5，快速排除不同图片

## 值得手动尝试的平台

| 平台 | 方法 | 信息获取 |
|------|------|----------|
| 裁判文书网 | wenshu.court.gov.cn | 姓名+城市查法院判决 |
| 知网CNKI | kns.cnki.net | 姓名查论文→院校/单位 |
| 爱企查 | aiqicha.baidu.com | 免费，查企业关联人 |
| 脉脉 | maimai.cn | 职业社交网络 |
| 看准网 | kanzhun.com | 公司+员工信息 |
| 闲鱼 | goofish.com | 二手交易，暴露位置 |
| 搜狗微信 | weixin.sogou.com | 搜公众号文章 |

## 环境依赖
- **Playwright + playwright-stealth**（推荐，核心浏览器自动化工具）
- **Maigret + Sherlock**（用于国际平台用户名枚举，pip install）
- **Pillow + numpy**（用于头像像素分析判断真假照片）
- **requests + beautifulsoup4**（HTTP请求和HTML解析）
