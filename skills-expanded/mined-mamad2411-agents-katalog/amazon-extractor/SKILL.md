---
name: amazon-extractor
description: Amazon 商品子 HTML 块的结构化提取器（清洗器）。读取分块后的子 HTML，清洗 DOM 噪声，输出结构化 Markdown。包含 4 个子技能（ppd / customer-reviews / aplus / product-details），每个负责一种块类型。当 agent 需要从子 HTML 中提取结构化数据时调度此技能。
type: orchestration
---

# 提取器（Extractor）

## 子技能

| 子技能 | 技能名 | 复杂度 | 说明 |
| --- | --- | --- | --- |
| PPD | `ppd-extractor` | 复杂（6 子阶段） | Core/Buybox/Twister/Overview/Bullets/Images |
| Customer Reviews | `customer-reviews-extractor` | 简单 | 强制复制模版，清洗后直接提取 |
| A+ | `aplus-extractor` | 复杂（3 子阶段） | Comparison/Assets/Brand Story |
| Product Details | `product-details-extractor` | 简单 | 清洗后提取表格数据 |

## 通用清洗规则（所有块共用）

提取前必须清洗的 DOM 噪声：
- `<br>`, `<br/>` → 换行或空格
- `<script>`, `<style>` 标签 → 移除
- `&nbsp;` / `\xa0` → 普通空格
- 连续空白 → 单空格
- 前后空白 → strip
- CSS 样式：`style=""` → 移除
- Script 脚本：`<script></script>` → 移除

```python
def _normalize_text(value: str) -> str:
    value = value.replace("\xa0", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip()

def _extract_text(node: Tag | None) -> str:
    if node is None:
        return ""
    for br in node.find_all("br"):
        br.replace_with("\n")
    return _normalize_text(node.get_text(" ", strip=True))
```

## Markdown 表格渲染硬性规则

所有输出中的 Markdown 表格**必须**包含三部分，否则判定为格式错误：

1. **表头行**（Header row）
2. **分隔行**（Separator row）：`| --- | --- |`
3. **数据行**（Data rows）

**正确格式（唯一允许的格式）：**
```markdown
| Field | Value |
| --- | --- |
| Department | womens |
| ASIN | B0C7BMLGP2 |
```

**错误格式（严禁出现）：**
```markdown
| Department | womens |
| ASIN | B0C7BMLGP2 |
```

表格渲染代码必须使用以下模式：
```python
lines.append("| Field | Value |")
lines.append("| --- | --- |")
for row in rows:
    key = row.key.replace("|", "\\|")
    value = row.value.replace("|", "\\|")
    lines.append(f"| {key} | {value} |")
```nes.append(f"| {opt.name} | {opt.current} | {opt.list} | {opt.discount} | {opt.prime} | {opt.status} |")
```

## 通用约束

1. **不依赖用户给 selector**：自行从 HTML 样本归纳，提供主备路径
2. **产出是可复用的提取器代码**，不是一次性抽取结果
3. **BeautifulSoup + lxml**：所有 HTML 解析用 `BeautifulSoup(html, "lxml")`
4. **不引入新依赖**：只用 `bs4`, `lxml`, `re`, `pathlib`, 标准库
5. **缺失字段写 `N/A`**，不得臆造
6. **文件编码统一 UTF-8**
7. **严禁使用 `[class*='xxx']` 通配符 selector**

### Selector 优先级

1. `#id` — 最稳定
2. `[data-hook="xxx"]` — Amazon 语义标记
3. `.class1.class2` — 组合 class
4. `#parent > .child` — 限定父级
5. 避免 `:nth-child` 和绝对 DOM 路径

### 多 selector fallback 模式

```python
for selector in ["#primary", "#fallback", ".class_based"]:
    node = soup.select_one(selector)
    if node:
        break
else:
    node = None
```

## 模板代码结构约定

每个提取器必须遵循以下结构：

1. **数据结构**：用 `@dataclass(frozen=True)` 定义提取结果
2. **通用清洗**：`_normalize_text()` + `_clean_text_from_tag()`
3. **字段提取**：多 selector fallback 模式
4. **Markdown 渲染**：`_render_markdown()` 生成结构化输出
5. **统一入口**：`extract_<block>_markdown(html_path: Path, out_path: Path | None = None) -> Path`
6. **manifest 集成**：调用 `update_manifest_block_for_output()`
7. **CLI 入口**：`argparse` + `main()` + `if __name__ == "__main__"`

写新提取器时，先读 `skills/customer-reviews/customer_reviews_extract.py`，然后按同样结构实现。
