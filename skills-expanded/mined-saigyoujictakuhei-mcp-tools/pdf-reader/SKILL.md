---
name: PDF Reader
description: PDF 文本提取模块，支持从本地文件和 URL 获取 PDF 文本内容
---

# PDF Reader 操作手册

## 功能概览
PDF Reader 模块提供 PDF 文本提取功能，支持：
- **本地文件**：从本地路径读取 PDF 并提取文本（支持路径遍历）
- **URL 远程文件**：从 HTTP/HTTPS URL 下载 PDF 并提取文本
- **底层引擎**：PyPDF2>=3.0.0

## 注册工具

### pdf_read_local
- **描述**：从本地 PDF 文件提取文本内容
- **参数**：
  - `path` (string, 必填): PDF 文件绝对或相对路径
- **返回值**：`{success: bool, data?: {text: string}, error?: string}`
- **示例**：
```json
{
  "path": "C:\\Docs\\report.pdf"
}
```
- **成功响应**：
```json
{
  "success": true,
  "data": {
    "text": "PDF 提取的文本内容..."
  }
}
```
- **失败响应**：
```json
{
  "success": false,
  "error": "PDF file not found: C:\\Docs\\report.pdf"
}
```

### pdf_read_url
- **描述**：从 URL PDF 提取文本内容（下载至内存）
- **参数**：
  - `url` (string, 必填): PDF 文件的 HTTP/HTTPS URL
- **返回值**：`{success: bool, data?: {text: string}, error?: string}`
- **示例**：
```json
{
  "url": "https://example.com/document.pdf"
}
```
- **成功响应**：
```json
{
  "success": true,
  "data": {
    "text": "PDF 提取的文本内容..."
  }
}
```
- **失败响应**：
```json
{
  "success": false,
  "error": "URL does not point to a PDF file. Content-Type: text/html"
}
```

## 内部模块
- `scripts/pdf_utils.py` : 公共 PDF 工具函数（extract_text_from_pdf, get_logger）
- `scripts/pdf_read_local.py` : 本地 PDF 读取工具
- `scripts/pdf_read_url.py` : URL PDF 读取工具

## 错误处理
- `FileNotFoundError`: 本地文件不存在
- `RequestException`: URL 请求失败（网络错误/超时/404等）
- `ValueError`: PDF 解析失败（损坏的 PDF 文件/密码保护）
- `ContentType 不匹配`: URL Content-Type 不是 application/pdf

## 依赖
- `PyPDF2>=3.0.0`: PDF 解析引擎
- `requests`: HTTP 客户端（仅 pdf_read_url 需要）

## 注意事项
- 本地文件路径支持相对路径（相对于工作目录）
- URL 读取超时默认 30 秒
- PDF 密码保护文件暂不支持
- 大 PDF 文件（>50MB）可能导致内存占用较高
