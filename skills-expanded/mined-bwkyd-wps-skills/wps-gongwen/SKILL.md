---
name: wps-gongwen
description: |
  公文排版。按国标GB/T 9704格式排版通知、请示、批复、函件等公文，
  红头文件格式自动处理。
  用于帮助用户排版公文。当用户提到公文、红头文件、通知、请示、批复时触发。
  Chinese government document formatter per GB/T 9704.
license: MIT
user-invocable: true
argument-hint: '[文种] [主题/内容描述]'
allowed-tools: 'Read, Grep, Glob, Bash, Write, Edit'
metadata:
  author: BWKYD
  title: 公文排版
  description_zh: 按国标GB/T 9704格式排版通知、请示、批复、函件等公文
  tags:
    - 公文
    - GB/T 9704
    - 红头文件
    - python-docx
    - WPS
  version: 1.0.2
  license: MIT
---

# 公文写作排版助手

按 **GB/T 9704-2012《党政机关公文格式》** 标准，自动生成规范公文 .docx 文件。

## When to Use

- 用户需要撰写党政机关公文（通知、请示、批复、报告等）
- 用户需要生成红头文件
- 用户需要按国标格式排版企业行政公文
- 用户说"帮我写一份XX通知/请示/批复/报告"

## When NOT to Use

- 普通Word文档（非公文格式）→ 使用 `docx-writer`
- 仅需要公文内容不需要格式 → 直接撰写即可
- WPS宏脚本开发 → 使用 `jsa-macro`

## 公文文种速查

| 文种 | 适用场景 | 行文方向 |
|------|---------|---------|
| **通知** | 发布规章、转发公文、安排工作 | 下行 |
| **通报** | 表彰先进、批评错误、传达情况 | 下行 |
| **请示** | 请求上级批准或指示 | 上行 |
| **报告** | 向上级汇报工作、反映情况 | 上行 |
| **批复** | 答复下级请示 | 下行 |
| **函** | 平级或不相隶属单位间商洽 | 平行 |
| **纪要** | 记载会议主要情况和议定事项 | — |
| **决定** | 对重要事项作出决策和部署 | 下行 |
| **意见** | 对重要问题提出见解和处理办法 | 多向 |
| **命令(令)** | 公布规章、嘉奖有功人员 | 下行 |
| **公告** | 向国内外宣布重要事项 | 下行 |
| **通告** | 在一定范围内公布应当遵守事项 | 下行 |
| **议案** | 提请审议事项 | 上行 |
| **决议** | 经会议讨论通过的重大决策事项 | 下行 |
| **公报** | 公开发布重要决定或重大事件 | 下行 |

## 工作流程

### Step 1: 确认要素

向用户确认以下公文要素（未提供的合理推断或询问）：

**必填要素：**
- **文种**：通知/请示/批复/报告/函/纪要/决定/意见 等
- **发文机关**：发文单位名称
- **主题/事由**：公文的核心内容
- **主送机关**：收文单位

**可选要素（有则填写）：**
- **发文字号**：如"X办发〔2026〕1号"
- **密级/紧急程度**：如"机密""特急"
- **抄送机关**：需知悉的其他单位
- **附件**：附件标题列表
- **签发人**：上行文必须标注

### Step 2: 撰写公文内容

根据文种特点撰写内容，遵循以下原则：

**语言规范：**
- 使用书面语，语气庄重
- 避免口语化表达
- 用语准确规范，不产生歧义
- 人称使用"本机关/本单位"，不用"我们"

**结构规范：**
- 通知：依据→事项→要求→执行期限
- 请示：缘由→事项→请求语（"妥否，请批复"）
- 报告：报告缘由→主体内容→结尾（"特此报告"）
- 函：去函事由→具体事项→希望或要求
- 纪要：会议概况→议定事项（逐条列出）

**成文日期：**
- 使用阿拉伯数字标注完整年月日，如"2026年3月22日"
- 联合行文以最后签发日期为准

### Step 3: 生成 .docx 文件

使用 python-docx 生成标准格式公文文件。

**先确保依赖已安装：**
```bash
pip install python-docx 2>/dev/null || pip3 install python-docx 2>/dev/null
```

**生成脚本必须严格遵循以下格式标准：**

#### 页面设置
```text
纸张：A4 (210mm × 297mm)
上边距：37mm（上行文为37mm）
下边距：35mm
左边距：28mm
右边距：26mm
页码：外侧，4号半角阿拉伯数字
```

#### 版头区域（红头）
```text
份号（如有）：顶格，3号阿拉伯数字
密级和保密期限（如有）：3号黑体
紧急程度（如有）：3号黑体
发文机关标志：红色（小标宋体/黑体），上边缘至版心上边缘 35mm
                字号根据机关名称长度调整，推荐使用上22下20区间
发文字号：3号仿宋，居中（联合行文居中）
签发人（上行文）：3号仿宋，"签发人："后标3号楷体人名
分隔线：红色，上距发文字号4mm
```

#### 主体区域
```text
标题：2号方正小标宋（备选华文中宋），居中，行距固定值28.95pt
      可分一行或多行排列，回行时做到词意完整
主送机关：3号仿宋，顶格，回行时顶格
正文：3号仿宋_GB2312，首行缩进2字符
      行距：固定值28.95pt
      每面排22行，每行排28个字
结构层次序号：
  第一层 "一、"   黑体
  第二层 "（一）" 楷体
  第三层 "1."    仿宋
  第四层 "（1）"  仿宋
附件说明：正文下一行，左空2字，3号仿宋
          "附件：1. XXXXX"
```

#### 版记区域
```text
发文机关署名：右空4字，发文机关全称或规范简称
成文日期：右空4字，阿拉伯数字，"XXXX年X月X日"
印章：端正、居中下压发文机关署名和成文日期
分隔线：版记上方，与正文间隔一行
抄送机关（如有）：4号仿宋，"抄送：XXXX。"
印发机关和日期：4号仿宋，左标印发机关，右标印发日期
```

#### python-docx 核心代码模式

```python
from docx import Document
from docx.shared import Pt, Mm, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import os

def create_gongwen(
    title,           # 公文标题
    doc_type,        # 文种（通知/请示/批复等）
    issuing_org,     # 发文机关
    doc_number,      # 发文字号
    main_recv,       # 主送机关
    body_text,       # 正文内容（段落列表）
    date_str,        # 成文日期
    cc_orgs=None,    # 抄送机关
    attachments=None,# 附件列表
    urgency=None,    # 紧急程度
    secret_level=None,# 密级
    signer=None,     # 签发人（上行文）
    output_path=None # 输出路径
):
    doc = Document()

    # === 页面设置 ===
    section = doc.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.top_margin = Mm(37)
    section.bottom_margin = Mm(35)
    section.left_margin = Mm(28)
    section.right_margin = Mm(26)

    # === 辅助函数 ===
    def add_para(text, font_name='仿宋_GB2312', size=16, bold=False,
                 align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0,
                 space_after=0, first_indent=None):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = Pt(28.95)
        if first_indent:
            p.paragraph_format.first_line_indent = Pt(first_indent)
        run = p.add_run(text)
        run.font.size = Pt(size)
        run.font.name = font_name
        run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
        run.bold = bold
        return p, run

    # === 版头：发文机关标志（红头） ===
    p_org = doc.add_paragraph()
    p_org.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_org.paragraph_format.space_before = Pt(60)
    p_org.paragraph_format.space_after = Pt(0)
    run_org = p_org.add_run(issuing_org)
    run_org.font.size = Pt(22)
    run_org.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
    run_org.font.name = '方正小标宋简体'
    run_org._element.rPr.rFonts.set(qn('w:eastAsia'), '方正小标宋简体')
    run_org.bold = True

    # "文件" 二字（如需要）
    if not issuing_org.endswith('文件'):
        run_wj = p_org.add_run('文件')
        run_wj.font.size = Pt(22)
        run_wj.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
        run_wj.font.name = '方正小标宋简体'
        run_wj._element.rPr.rFonts.set(qn('w:eastAsia'), '方正小标宋简体')
        run_wj.bold = True

    # === 发文字号 ===
    if doc_number:
        add_para(doc_number, '仿宋_GB2312', 16, False, WD_ALIGN_PARAGRAPH.CENTER)

    # === 红色分隔线 ===
    p_line = doc.add_paragraph()
    p_line.paragraph_format.space_before = Pt(4)
    p_line.paragraph_format.space_after = Pt(0)
    # 使用底部边框模拟红线
    pPr = p_line._element.get_or_add_pPr()
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:bottom w:val="single" w:sz="12" w:space="1" w:color="FF0000"/>'
        f'</w:pBdr>'
    )
    pPr.append(pBdr)

    # === 标题 ===
    add_para(title, '方正小标宋简体', 22, False, WD_ALIGN_PARAGRAPH.CENTER,
             space_before=10, space_after=10)

    # === 主送机关 ===
    add_para(main_recv + '：', '仿宋_GB2312', 16, False,
             WD_ALIGN_PARAGRAPH.LEFT)

    # === 正文 ===
    for para_text in body_text:
        # 检测结构层次
        if para_text.strip().startswith(('一、','二、','三、','四、','五、',
                                          '六、','七、','八、','九、','十')):
            add_para(para_text, '黑体', 16, False,
                     WD_ALIGN_PARAGRAPH.JUSTIFY, first_indent=32)
        elif para_text.strip().startswith(('（一）','（二）','（三）','（四）','（五）')):
            add_para(para_text, '楷体_GB2312', 16, False,
                     WD_ALIGN_PARAGRAPH.JUSTIFY, first_indent=32)
        else:
            add_para(para_text, '仿宋_GB2312', 16, False,
                     WD_ALIGN_PARAGRAPH.JUSTIFY, first_indent=32)

    # === 附件说明 ===
    if attachments:
        attach_text = '附件：'
        for i, att in enumerate(attachments, 1):
            if i == 1:
                attach_text += f'{i}. {att}'
            else:
                attach_text += f'\n      {i}. {att}'
        add_para(attach_text, '仿宋_GB2312', 16, False,
                 WD_ALIGN_PARAGRAPH.LEFT, first_indent=32)

    # === 发文机关署名 + 成文日期 ===
    doc.add_paragraph()  # 空行
    add_para(issuing_org, '仿宋_GB2312', 16, False,
             WD_ALIGN_PARAGRAPH.RIGHT)
    add_para(date_str, '仿宋_GB2312', 16, False,
             WD_ALIGN_PARAGRAPH.RIGHT)

    # === 版记 ===
    if cc_orgs:
        # 版记分隔线
        p_sep = doc.add_paragraph()
        pPr = p_sep._element.get_or_add_pPr()
        pBdr = parse_xml(
            f'<w:pBdr {nsdecls("w")}>'
            f'  <w:top w:val="single" w:sz="6" w:space="1" w:color="000000"/>'
            f'</w:pBdr>'
        )
        pPr.append(pBdr)
        cc_text = '抄送：' + '，'.join(cc_orgs) + '。'
        add_para(cc_text, '仿宋_GB2312', 14, False, WD_ALIGN_PARAGRAPH.LEFT)

    # === 保存 ===
    if not output_path:
        safe_title = title.replace(' ', '_')[:30]
        output_path = f'{safe_title}.docx'
    doc.save(output_path)
    return os.path.abspath(output_path)
```

### Step 4: 交付和验证

1. 生成 .docx 文件到用户指定目录（默认当前目录）
2. 告知文件路径
3. 提示用户用WPS打开检查格式
4. 如需调整，根据反馈修改后重新生成

## 常见公文模板

### 通知结尾语
- "特此通知。"
- "请遵照执行。"
- "请认真贯彻落实。"

### 请示结尾语
- "妥否，请批复。"
- "以上请示，请予审批。"
- "当否，请批示。"

### 报告结尾语
- "特此报告。"
- "以上报告，请审阅。"

### 函结尾语
- "请予函复。"（去函）
- "特此函复。"（复函）

### 批复结尾语
- "此复。"

## 示例

```bash
# 生成一份放假通知
/wps-gongwen 通知 关于2026年清明节放假安排的通知

# 生成一份请示
/wps-gongwen 请示 关于申请增加办公设备采购预算的请示

# 生成一份会议纪要
/wps-gongwen 纪要 关于第三季度工作推进会议纪要
```

输出：在当前目录生成 `关于2026年清明节放假安排的通知.docx`，用WPS打开即为标准红头公文格式。

## 格式参考

详细格式标准见 [reference/gb-t-9704.md](reference/gb-t-9704.md)。
中文排版通用规范见 [../shared/chinese-typesetting.md](../shared/chinese-typesetting.md)。
