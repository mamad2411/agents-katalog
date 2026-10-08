---
name: alibaba-product-research
description: 阿里巴巴国际站产品调研分析。自动搜索关键词、归类产品分类、提取供应商和价格信息、输出结构化分析报告。触发词：「调研」「搜索分析」「产品调研」「市场调研」「alibaba」「阿里巴巴」「电商调研」「搜索电商」「产品分析」。
---

# 阿里巴巴国际站产品调研

使用 Playwright MCP 访问阿里巴巴国际站，搜索指定关键词，归类分析产品，输出结构化调研报告。

## 适用场景

- 用户说「调研 XXX 产品」「搜索分析 XXX」「市场调研 XXX」
- 用户说「alibaba 搜索 XXX」「阿里巴巴搜索 XXX」
- 用户说「XXX 产品有哪些供应商」「XXX 市场价格」

## 工作流程

### Step 1: 打开阿里巴巴国际站并搜索

1. 使用 `browser_navigate` 打开 `https://www.alibaba.com`
2. 等待页面加载完成（至少等待3秒）
3. 使用 `browser_type` 在搜索框输入用户指定的关键词
4. 使用 `browser_click` 点击搜索按钮或按 Enter 提交搜索
5. **重要**：搜索后等待8-10秒让AI分析完成

### Step 2: 获取热门品类

搜索结果页面会显示相关热门品类。使用 `browser_snapshot` 或 `browser_take_screenshot` 获取页面内容，然后使用 `browser_evaluate` 提取热门品类信息：

- 热门品类名称（如 Garden Tools、Plant Pots 等）
- 各品类的产品数量或热度

### Step 3: 点击具体品类查看详情

1. 从热门品类中选择一个具体品类（如园艺工具）
2. 使用 `browser_click` 点击进入该品类详情页
3. 等待页面加载，使用截图或 evaluate 获取产品列表

### Step 4: 提取产品数据

**增强的数据提取代码（多重选择器 + 错误处理）：**

```javascript
// 安全提取函数
const safeText = (el, defaultVal = '') => {
  try {
    return el?.textContent?.trim() || defaultVal;
  } catch { return defaultVal; }
};

// 获取产品标题和链接
const getProducts = () => {
  const products = [];
  const seen = new Set();
  const selectors = [
    'a[href*="product-detail"]',
    'h3 a', '.title a', '[class*="title"] a',
    '.product-item a', '.offer-list a'
  ];

  selectors.forEach(selector => {
    try {
      document.querySelectorAll(selector).forEach(link => {
        const href = link.href || '';
        const text = safeText(link);
        if (href && href.includes('product-detail') && !seen.has(href) && text.length > 5) {
          seen.add(href);
          products.push({
            title: text.substring(0, 60),
            url: href.split('?')[0]
          });
        }
      });
    } catch {}
  });
  return [...new Map(products.map(p => [p.url, p])).values()].slice(0, 10);
};

// 获取价格
const getPrices = () => {
  const prices = [];
  const priceSelectors = [
    '[class*="price"]', '.price-text', '.Price',
    '[data-price]', '.sale-price', '.ma-spec-price'
  ];

  priceSelectors.forEach(selector => {
    try {
      document.querySelectorAll(selector).forEach(el => {
        const text = safeText(el);
        if (text && /\$[\d,]+\.?\d*/.test(text)) {
          prices.push(text.match(/\$[\d,]+\.?\d*/)[0]);
        }
      });
    } catch {}
  });
  return [...new Set(prices)].slice(0, 15);
};

// 获取供应商
const getSuppliers = () => {
  const suppliers = [];
  const supplierSelectors = [
    '[class*="supplier"]', '[class*="company"]',
    '.supplier-name', '.company-name', '[data-supplier]'
  ];

  supplierSelectors.forEach(selector => {
    try {
      document.querySelectorAll(selector).forEach(el => {
        const text = safeText(el);
        if (text && text.length > 3 && text.length < 80) {
          suppliers.push(text.replace(/\n/g, ' ').trim());
        }
      });
    } catch {}
  });
  return [...new Set(suppliers)].slice(0, 10);
};

// 返回结果
return {
  products: getProducts(),
  prices: getPrices(),
  suppliers: getSuppliers()
};
```

### Step 5: 归类分析

根据提取的数据，进行归类分析：

1. **产品分类**：按产品类型分组（如工具类、配件类、设备类）
2. **价格区间**：整理出低价位、中价位、高价位产品
3. **供应商分析**：提取主要供应商名称、认证年限
4. **热门属性**：分析页面中的热门属性标签（如无绳、降噪、防水等）
5. **平台服务**：识别平台提供的服务（无忧退、运费优惠、批发折扣等）

### Step 6: 输出结构化报告

按以下模板输出调研报告：

```markdown
# [关键词] 市场调研报告

> 平台：阿里巴巴国际站 | 生成日期：YYYY-MM-DD

## 一、热门品类概览

| 品类名称 | 产品热度 |
|---------|---------|
| 品类1  | 高/中/低 |
| 品类2  | 高/中/低 |

## 二、热门属性分析

| 属性 | 热度 |
|------|------|
| 属性1 | 非常高/高/中 |
| 属性2 | 非常高/高/中 |

## 三、具体品类分析：[品类名称]

### 3.1 产品分类与价格

| 产品类别 | 代表产品 | 价格区间 |
|---------|---------|---------|
| 类别1  | 产品名  | US$X-X  |
| 类别2  | 产品名  | US$X-X  |

### 3.2 主要供应商

| 供应商名称 | 认证年限 | 类型 | 评分 |
|-----------|---------|------|------|
| 公司名   | X年     | 制造商/贸易商 | X/X |

### 3.3 价格特点

- **低价位**：US$X-X（xxx 产品）
- **中价位**：US$X-X（xxx 产品）
- **高价位**：US$X+（xxx 产品）

### 3.4 平台服务

- 🛡️ 无忧退
- 🚚 本地库存/运费优惠
- 💰 批发折扣
- ⚡ 快速定制/OEM
- ⏰ 准时送达
- 💳 Trade Assurance

## 四、市场洞察

简要分析该品类的市场特点、供应链情况、选品建议、趋势观察等。

## 五、相关产品链接

从页面提取的实际产品链接：
- [产品名称](实际URL)
```

## 错误处理与重试策略

### 页面加载超时
- 如果 `browser_navigate` 后页面加载慢，使用 `browser_wait_for` 等待 5-10 秒
- 添加重试逻辑：最多尝试 3 次，每次间隔 3 秒

### 数据提取失败
- 使用 try-catch 包裹每个选择器
- 失败时使用备用选择器列表
- 数据不足时使用截图补充分析

### AI搜索模式卡住
- 如果搜索后长时间停留在"正在分析"界面
- 尝试点击"产品"标签切换到普通搜索模式
- 或直接使用 evaluate 提取已加载的产品数据

## 注意事项

1. 页面加载较慢时使用 `browser_wait_for` 等待足够时间
2. 如果页面有弹窗，使用 `browser_handle_dialog` 处理
3. 数据提取困难时多截图，用视觉分析补充
4. 保持客观，只报告页面显示的数据，不要猜测
5. 产品链接必须使用真实URL，去除URL参数
