---
name: streaming-export-safety
description: 当代码涉及 Excel/CSV/JSON/PDF 大文件导出、批量序列化、内存里构建大对象时触发。防止 OOM、临时文件残留、同步导出阻塞 HTTP 线程等内存安全陷阱。
paths:
  - "**/*Export*.{java,py,go,ts,js}"
  - "**/*Excel*.{java,py,go,ts,js}"
  - "**/*Report*.{java,py,go,ts,js}"
  - "**/*Download*.{java,py,go,ts,js}"
  - "**/*Backup*.{java,py,go,ts,js}"
  - "**/*Writer*.{java,py,go,ts,js}"
keywords:
  - SXSSFWorkbook
  - XSSFWorkbook
  - HSSFWorkbook
  - EasyExcel
  - openpyxl
  - excelize
  - ExcelJS
  - PDFBox
  - iText
  - ReportLab
---

# 流式导出 / 大对象内存安全

> 当一次性 in-memory 构建数据超过 1 万行 / 10 MB 时，必须切换为流式 API。
> 否则常见后果：**OOM**、Full GC 风暴、临时文件残留、HTTP 超时。

---

## 决策：什么时候必须流式？

| 数据量级 | 推荐模式 | 备注 |
|---------|---------|------|
| ≤ 1 万行 / ≤ 5 MB | 内存构建 OK | XSSFWorkbook / pandas / 普通 JSON 序列化 |
| 1 万 ~ 10 万行 | **强烈建议**流式 | 单机够用，但有 OOM 风险 |
| > 10 万行 / > 50 MB | **必须**流式 + 异步 | 内存模型会爆 |
| 数据量未知（用户驱动） | **必须**流式 + 上限保护 | 永远按最坏情况设计 |

**核心判断**：能不能预估上限？预估超过 1 万行就上流式。

---

## 陷阱 #1：Excel 大数据 → XSSFWorkbook 全量加载 OOM

### 嗅探信号

代码评审看到以下模式立即怀疑：

- `new XSSFWorkbook()` + 循环 `createRow` 超过 1 万次
- `EasyExcel.write(...).sheet().doWrite(data)` 中 `data.size() > 10000`
- `openpyxl.Workbook()`（未带 `write_only=True`）+ 循环 `append`
- `excelize.NewFile()` + `SetCellValue` 大量循环
- `ExcelJS.Workbook()`（未用 `stream` 子模块）

### 正确做法：Java + Apache POI SXSSF

```java
// ❌ XSSF 全量内存（10w 行直接 OOM）
XSSFWorkbook wb = new XSSFWorkbook();
Sheet sheet = wb.createSheet();
for (int i = 0; i < 100_000; i++) {
    Row row = sheet.createRow(i);
    row.createCell(0).setCellValue("data");
}

// ✅ SXSSF 流式（windowSize=100，超出窗口写临时文件）
SXSSFWorkbook wb = null;
try {
    wb = new SXSSFWorkbook(100);
    wb.setCompressTempFiles(true);
    Sheet sheet = wb.createSheet();
    for (int i = 0; i < 100_000; i++) {
        Row row = sheet.createRow(i);
        row.createCell(0).setCellValue("data");
    }
    try (OutputStream os = new FileOutputStream("out.xlsx")) {
        wb.write(os);
    }
} finally {
    if (wb != null) {
        wb.dispose();
    }
}
```

### SXSSF 限制（**必须**告知调用方）

- ❌ 不能随机访问已 flush 的行（超过 windowSize 后该行不可读）
- ❌ 不支持公式自动计算（需要预先 `evaluator.evaluateAll()`）
- ❌ 不支持 `cloneSheet`、不支持合并多个已写出的 Sheet
- ⚠️ 临时文件默认在 `java.io.tmpdir`，容器环境注意磁盘配额
- ⚠️ 必须 `dispose()`，否则临时文件残留

### EasyExcel（阿里）流式写入

```java
// ✅ EasyExcel 默认就是流式，分批写入
EasyExcel.write("out.xlsx", DataDTO.class)
    .registerWriteHandler(new LongestMatchColumnWidthStyleStrategy())
    .sheet("data")
    .doWrite(() -> {
        // 分页拿数据，每次返回一批
        return loadBatch(pageNo++, BATCH_SIZE);
    });
```

### 其他语言核心 API

| 语言 | 流式 API | 关键差异 |
|------|---------|---------|
| Python | `openpyxl.Workbook(write_only=True)` | ❌ 不能用 `ws.cell()`，只能 `ws.append(row)`，**不可回写** |
| Python | `pandas.read_excel(chunksize=N)` | 读端分批；写端用 `ExcelWriter(engine='openpyxl')` |
| Go | `f.NewStreamWriter("Sheet1")` (excelize v2.x) | 必须 `sw.Flush()`，否则数据丢失 |
| Node.js | `new ExcelJS.stream.xlsx.WorkbookWriter({filename})` | 每个 row `row.commit()`，最后 `workbook.commit()` |

> 完整代码示例见 `references/multi-lang-examples.md`

---

## 陷阱 #2：CSV 大文件 → 整文件 readlines / List 拼接

### 错误示例

```java
// ❌ 一次性读入全部行
List<String> lines = Files.readAllLines(Paths.get("huge.csv"));

// ❌ 一次性构建全部字符串
StringBuilder sb = new StringBuilder();
for (Record r : records) sb.append(r.toCsv()).append("\n");
Files.write(path, sb.toString().getBytes());
```

### 正确做法

```java
// ✅ 读：BufferedReader 逐行
try (BufferedReader reader = Files.newBufferedReader(path)) {
    String line;
    while ((line = reader.readLine()) != null) {
        processLine(line);
    }
}

// ✅ 写：OpenCSV CSVWriter 逐行 flush
try (CSVWriter writer = new CSVWriter(new FileWriter(path))) {
    for (Record r : records) {
        writer.writeNext(r.toArray());
    }
}
```

### 其他语言核心 API

| 语言 | 写 | 读 |
|------|----|----|
| Python | `csv.writer(f).writerows(iter)` | `csv.reader(f)` 迭代器 / `pandas.read_csv(chunksize=N)` |
| Go | `csv.NewWriter(f)` + `w.Flush()` 必须调用 | `csv.NewReader(f).Read()` 逐行 |
| Node.js | `csv-stringify` stream | `csv-parse` stream |

**陷阱**：Go 的 `csv.Writer` 不自动 flush，**忘记调用 `w.Flush()` 数据全在 buffer 里**。

---

## 陷阱 #3：JSON 大数组导出 → ObjectMapper.writeValueAsString

### 错误示例

```java
// ❌ 整数组先序列化为 String，再写文件
List<Order> orders = repo.findAll(); // 100w 行
String json = objectMapper.writeValueAsString(orders);  // OOM
Files.write(path, json.getBytes());
```

### 正确做法：JsonGenerator 流式

```java
// ✅ Jackson JsonGenerator 流式写
try (JsonGenerator gen = objectMapper.getFactory()
        .createGenerator(new FileOutputStream(path), JsonEncoding.UTF8)) {
    gen.writeStartArray();
    int page = 0;
    Page<Order> orderPage;
    do {
        orderPage = repo.findAll(PageRequest.of(page++, 1000));
        for (Order o : orderPage.getContent()) {
            objectMapper.writeValue(gen, o);
        }
    } while (orderPage.hasNext());
    gen.writeEndArray();
}
```

### 推荐替代：JSONL（行分隔 JSON）

数据量极大时，输出格式选 **JSONL**（每行一个 JSON 对象）比标准 JSON 数组更友好：

```
{"id":1,"name":"a"}
{"id":2,"name":"b"}
```

下游可以一行一行解析，不需要先读完整个文件。

### 其他语言核心 API

| 语言 | 流式 API |
|------|---------|
| Python | `orjson` 单条 dumps + 写 `.jsonl`；或 `ijson` 读流式 |
| Go | `json.NewEncoder(w).Encode(v)` 逐对象（天然生成 JSONL） |
| Node.js | `JSONStream.stringify()` |

---

## 陷阱 #4：PDF 大报表 → 全文档预渲染

### 错误示例

```java
// ❌ 一次性把所有 Page 加到 Document，再 save
PDDocument doc = new PDDocument();
for (int i = 0; i < 10_000; i++) {
    doc.addPage(buildPage(data.get(i)));  // 全部 Page 在内存
}
doc.save(path);
```

### 正确做法：分批写 + flush

```java
// ✅ iText 流式：每个 Page 写完立即 flush
try (PdfDocument doc = new PdfDocument(new PdfWriter(path))) {
    Document layout = new Document(doc);
    for (Order o : orders) {
        layout.add(buildParagraph(o));
        if (orderIndex++ % 100 == 0) {
            doc.getWriter().flush();  // 100 条 flush 一次
        }
    }
}
```

### 其他语言核心 API

| 语言 | 流式 API | 关键操作 |
|------|---------|---------|
| Python | `ReportLab Canvas` | 每页 `c.showPage()` 后 `c.save()` 增量写 |
| Go | `gofpdf.New(...)` + `pdf.AddPage()` | `OutputFileAndClose(path)` 一次写出（内存大时考虑 `unidoc` 流式） |
| Node.js | `PDFKit` | `doc.pipe(fs.createWriteStream(path))` |

**注意**：很多 PDF 库（如 PDFBox、jsPDF）**没有真正的流式 API** —— 整文档必须留在内存里。
数据量大时考虑：
1. 拆成多个 PDF
2. 改用专业流式库（iText 商用、ReportLab）
3. 走异步 + 文件存储

---

## 陷阱 #5：大数据导出同步阻塞 HTTP 线程

### 问题

同步导出 > 30s 会被 Nginx / 网关切断 504；HTTP 线程被长时间占用，影响其他请求。

### 错误示例

```java
// ❌ Controller 同步生成 + 返回
@GetMapping("/export/orders")
public ResponseEntity<byte[]> exportOrders() {
    byte[] excel = buildExcelInMemory();  // 占用 HTTP 线程 60s+
    return ResponseEntity.ok().body(excel);
}
```

### 正确做法：任务化 + 轮询/通知

```java
// ✅ 接口立即返回任务 ID
@PostMapping("/export/orders")
public ExportTaskDTO export() {
    String taskId = exportTaskService.submit(...);
    return new ExportTaskDTO(taskId, "PROCESSING");
}

// ✅ 异步执行 + 写到对象存储
@Async("exportExecutor")
public void execute(String taskId, ...) {
    try (SXSSFWorkbook wb = new SXSSFWorkbook(100)) {
        // 流式写
        File temp = streamToFile(wb);
        String url = ossClient.upload(temp);
        taskRepo.complete(taskId, url);
    }
}

// ✅ 查询接口
@GetMapping("/export/tasks/{id}")
public ExportTaskDTO query(@PathVariable String id) { ... }
```

> 详见 `async-task-pattern` skill —— 异步任务的状态机、超时、重试、幂等

---

## 通用检查清单

- [ ] 数据量预估超过 1 万行的导出是否用了流式 API
- [ ] 临时文件清理是否在 `try-finally` / `defer` / `with` / `using` 中（SXSSF 必须 `dispose()`）
- [ ] 临时目录是否检查了磁盘配额（容器环境 `/tmp` 可能很小）
- [ ] 流式 API 的限制是否告知了调用方（不能回写 / 不支持公式 / 必须 flush）
- [ ] 导出接口是否异步化（任务 ID + 轮询 / WebSocket 通知）
- [ ] 错误恢复：流式写入中断时临时文件是否清理
- [ ] 是否设置了数据量上限（防止用户传 `pageSize=999999`）
- [ ] 大文件是否上传到对象存储而非内存返回

---

## 相关 skill

- `async-task-pattern` —— 异步任务的状态机、超时、幂等
- `query-performance-safety` —— 防止导出时 N+1、IN 子句过长
- `field-mapping-safety` —— DTO 转换时字段映射一致性

---

## 规则溯源

```
> 📋 本回复遵循：`streaming-export-safety` - [章节]
```
