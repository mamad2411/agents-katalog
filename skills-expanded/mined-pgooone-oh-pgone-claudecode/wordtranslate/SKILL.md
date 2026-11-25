---
name: wordtranslate
description: |
  将Word文档(.docx)中的中文内容完整翻译成英文，同时保持原有格式和布局。
  使用此skill当用户需要：翻译Word文档、将中文docx转为英文、批量翻译Word中的文本、
  保持格式的文档翻译、处理Word XML结构进行翻译。适用于测试报告、技术文档、
  产品手册等需要完整保留格式的Word文档翻译场景。
---

# Word文档翻译 Skill

将Word文档(.docx)中的中文内容完整翻译成英文，同时保持原有格式和布局。

## 核心概念

Word文档(.docx)实际上是ZIP压缩包，包含XML文件：
- `word/document.xml` - 主文档内容（文本在此）
- `[Content_Types].xml` - 内容类型定义
- `word/_rels/document.xml.rels` - 资源关系定义
- 其他：样式、主题、媒体文件等

文本内容存储在 `<w:t>` 标签中。

## 翻译工作流程

### Phase 1: 文档解压
```bash
python scripts/unpack_docx.py input.docx unpacked/
```
或使用 docx skill 解压:
```bash
python scripts/office/unpack.py input.docx unpacked/
```

### Phase 2: 分析XML结构
读取 `unpacked/word/document.xml`，提取所有 `<w:t>` 标签中的文本：
- 识别包含中文字符的文本
- 建立原文→译文的映射表
- 统计翻译工作量

### Phase 3: 执行翻译
1. **加载术语表**：使用术语对照表确保专业术语翻译一致
2. **批量翻译**：按长度降序匹配（长词优先，避免部分替换）
3. **处理混合文本**：保留英文部分，只翻译中文
4. **处理特殊字符**：XML实体转义 (&, <, >, ", ')

### Phase 4: 残留清理（迭代）
第一轮翻译后，检查剩余中文：
- 识别未匹配的中文片段
- 创建补充术语映射
- 重复直到中文残留为0

### Phase 5: 重新打包
```bash
python scripts/office/pack.py unpacked/ output_EN.docx --original input.docx
```

### Phase 6: 质量验证
1. 解压翻译后的文档
2. 扫描 `<w:t>` 标签确认无中文残留
3. 使用pandoc转换为markdown验证格式
4. 生成验证报告

## 关键脚本

### unpack_docx.py - 解压脚本
将Word文档(.docx)解压为XML目录结构。

**用法:**
```bash
python scripts/unpack_docx.py <docx文件路径> [输出目录]
```

**示例:**
```bash
python scripts/unpack_docx.py report.docx
python scripts/unpack_docx.py report.docx unpacked/
```

### translate_docx.py - 主翻译脚本
提取XML中的中文文本，使用术语表翻译，然后替换。

核心功能：
- `extract_texts_from_xml()` - 提取所有 `<w:t>` 标签文本
- `create_translation_mapping()` - 创建翻译映射表
- `replace_texts_in_xml()` - 在XML中安全替换文本

**术语表排序原则**：按中文词组长度降序排序，优先匹配长词组，避免部分替换。

### pack_docx.py - 打包脚本
将解压的Word目录重新打包为docx文件。

### check_chinese.py - 中文检查脚本
扫描document.xml，统计中文残留。

## 术语表结构

```python
TERM_MAP = {
    # 测试用例字段
    "用例描述": "Test Case Description",
    "前置条件": "Prerequisites",
    "预期结果": "Expected Result",
    
    # 界面操作
    "点击": "Click",
    "选择": "Select",
    "输入": "Enter",
    
    # ... 更多术语
}
```

**术语分类**：
1. 测试用例字段 (Test Case Fields)
2. 测试结果状态 (Test Result Status)
3. 界面操作术语 (UI Operations)
4. 界面元素术语 (UI Elements)
5. 系统模块术语 (System Modules)
6. 密钥/安全相关术语
7. 设备相关术语
8. 部署架构术语
9. 通讯与接口术语
10. 数据与配置术语
11. 性能测试术语
12. 其他常用术语

## 处理规则

### 1. XML文本提取模式
```python
# 匹配 <w:t> 和 <w:t xml:space="preserve"> 标签
pattern = r'<w:t(?:\s+[^>]*)?>([^<]*)</w:t>'
```

### 2. 中文检测
```python
def contains_chinese(text):
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False
```

### 3. 安全替换原则
- 只替换 `<w:t>` 标签内的文本内容
- 保持所有格式属性 (`<w:rPr>`) 不变
- 保留 `xml:space="preserve"` 属性
- 按长度降序排序后替换，避免短词影响长词

### 4. 混合文本处理
原文: `点击OK按钮`
译文: `Click OK Button`

策略：术语替换后，剩余中文保留或根据上下文处理。

## 典型使用场景

### 场景1: 完整翻译流程
```
用户: 将这个中文Word文档翻译成英文
操作:
1. 解压文档
2. 运行translate_docx.py提取和翻译
3. 运行pack_docx.py打包
4. 运行check_chinese.py验证
```

### 场景2: 迭代清理残留
```
用户: 检查翻译后的文档还有中文吗
操作:
1. 解压翻译后的文档
2. 运行check_chinese.py统计残留
3. 如有残留，创建补充术语映射
4. 重新翻译→打包→验证
```

### 场景3: 自定义术语表
```
用户: 使用自定义术语表翻译
操作:
1. 编辑translate_docx.py中的TERM_MAP
2. 或从外部文件加载术语表
3. 执行标准翻译流程
```

## 常见问题

### Q: 翻译后格式错乱？
A: 确保只替换 `<w:t>` 标签内文本，不修改其他XML结构。

### Q: 部分中文未被翻译？
A: 
1. 检查术语表是否包含该词汇
2. 按长度降序排序术语表
3. 运行迭代清理脚本

### Q: 特殊字符显示异常？
A: 确保XML实体正确转义：
- `&` → `&amp;`
- `<` → `&lt;`
- `>` → `&gt;`
- `"` → `&quot;`

### Q: 文档打开报错？
A: 
1. 验证XML格式是否完整
2. 检查是否有未闭合标签
3. 使用 `--validate true` 选项重新打包

## 依赖要求

- Python 3.x
- docx skill (用于unpack/pack脚本)
- pandoc (用于验证，可选)

## 性能参考

- 11,541个文本元素，5,883个中文项
- 使用186个专业术语
- 创建1,173条唯一翻译映射
- 处理时间：数秒

## 输出产物

| 文件 | 说明 |
|------|------|
| `*_EN.docx` | 翻译后的英文文档 |
| `translation_mapping.json` | 翻译映射表 |
| `translation_report.md` | 翻译报告 |
| `chinese_check_report.json` | 中文残留检查报告 |

## 最佳实践

1. **翻译前**：准备专业术语对照表
2. **翻译中**：按长度降序排序术语，长词优先
3. **翻译后**：运行残留检查，迭代清理
4. **验证时**：使用pandoc+人工抽样检查
