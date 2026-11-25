---
name: cc-streaming-export-safety
description: 当实现用户驱动的大文件导出或批量序列化（Excel/CSV/JSON/JSONL/PDF，数据量未知或超过 1 万行/10 MB）时触发；普通小文件下载、静态资源下载、非导出 Writer/Report 类不触发。防止 OOM、临时文件残留、同步导出阻塞 HTTP 线程和表格公式注入。
---

# 流式导出 / 大对象内存安全

> 当一次性 in-memory 构建数据超过 1 万行 / 10 MB，或数据量由用户筛选决定且无法预估上限时，必须切换为流式 / 分页 API。
> 否则常见后果：**OOM**、Full GC 风暴、临时文件残留、HTTP 超时。

---

## 触发边界

适用：

- 用户驱动的全量导出、报表下载、备份导出、批量序列化
- Excel / CSV / JSON / JSONL / PDF 文件可能超过 1 万行或 10 MB
- 代码里出现 `SXSSFWorkbook`、`XSSFWorkbook`、`EasyExcel`、`openpyxl`、`excelize`、`ExcelJS`、`PDFKit`、`ReportLab`、`JsonGenerator` 等导出库

不适用：

- 固定小文件下载、静态资源下载、头像/附件转发
- 普通 `Writer` / `Report` / `Download` 命名但不涉及大数据导出
- 单条 JSON 响应或常规分页接口

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
- `EasyExcel.write(...).sheet().doWrite(data)` 里 `data` 已经全量加载且超过 1 万条
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
- ⚠️ 必须在 `finally` 中 `dispose()`，否则 SXSSF backing temp files 会残留

### EasyExcel（阿里）流式写入

```java
// ✅ 已使用 EasyExcel 的项目：用 ExcelWriter 分批写，不要先构建全量 data
ExcelWriter writer = null;
try {
    writer = EasyExcel.write("out.xlsx", DataDTO.class).build();
    WriteSheet sheet = EasyExcel.writerSheet("data")
            .registerWriteHandler(new LongestMatchColumnWidthStyleStrategy())
            .build();
    int pageNo = 0;
    while (true) {
        List<DataDTO> batch = loadBatch(pageNo++, BATCH_SIZE);
        if (batch.isEmpty()) {
            break;
        }
        writer.write(batch, sheet);
    }
} finally {
    if (writer != null) {
        writer.finish();
    }
}
```

> EasyExcel 已进入维护模式。新项目优先评估 Apache POI SXSSF、FastExcel / Apache Fesod 或项目已有导出栈。

### 其他语言核心 API

| 语言 | 流式 API | 关键差异 |
|------|---------|---------|
| Python | `openpyxl.Workbook(write_only=True)` | 写端不能用 `ws.cell()`，只能 `ws.append(row)`，**不可回写** |
| Python | `openpyxl.load_workbook(read_only=True)` | 读端按行迭代；超大数据优先考虑 CSV / JSONL |
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

## 陷阱 #4：PDF 大报表 → 假流式 / 全文档预渲染

### 错误示例

```java
// ❌ 一次性把所有 Page 加到 Document，再 save
PDDocument doc = new PDDocument();
for (int i = 0; i < 10_000; i++) {
    doc.addPage(buildPage(data.get(i)));  // 全部 Page 在内存
}
doc.save(path);
```

### 正确做法：先验证库是否真实增量写出

```java
// ✅ 写到文件流，分批取数；但仍需压测验证库内部是否保留完整文档状态
try (PdfWriter writer = new PdfWriter(path);
     PdfDocument pdf = new PdfDocument(writer);
     Document layout = new Document(pdf)) {
    for (Order o : orders) {
        layout.add(buildParagraph(o));
    }
}
```

### 其他语言核心 API

| 语言 | 流式 API | 关键操作 |
|------|---------|---------|
| Python | `ReportLab Canvas` | 分页绘制，换页 `c.showPage()`，最终 `c.save()` |
| Go | `gofpdf.New(...)` + `pdf.AddPage()` | `OutputFileAndClose(path)` 一次写出（内存大时考虑 `unidoc` 流式） |
| Node.js | `PDFKit` | `doc.pipe(fs.createWriteStream(path))` |

**注意**：PDF 库的“写到文件流”不等于内存恒定。很多库仍会在保存前保留完整文档状态。
数据量大时考虑：
1. 拆成多个 PDF
2. 改用已验证的增量写出库
3. 走异步 + 文件存储

---

## 陷阱 #5：CSV / Excel 公式注入

### 问题

用户可控字段如果以 `=`、`+`、`-`、`@` 开头，部分表格软件会按公式解释。导出文件被打开时，可能触发恶意公式或外部链接。

### 正确做法

- 对用户可控的文本单元格做公式前缀转义，例如按项目约定加单引号或制表符前缀
- 只处理文本字段，不要破坏数字、日期、金额等结构化字段
- 在 DTO / cell writer 层集中处理，避免每个导出点各自拼规则

---

## 陷阱 #6：大数据导出同步阻塞 HTTP 线程

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
    File temp = null;
    SXSSFWorkbook wb = null;
    try {
        temp = File.createTempFile("export-", ".xlsx");
        wb = new SXSSFWorkbook(100);
        wb.setCompressTempFiles(true);
        streamWriteExcel(wb, ...);
        try (OutputStream os = new FileOutputStream(temp)) {
            wb.write(os);
        }
        String url = ossClient.upload(temp);
        taskRepo.complete(taskId, url);
    } catch (Exception e) {
        taskRepo.fail(taskId, e.getMessage());
    } finally {
        if (wb != null) {
            wb.dispose();
        }
        if (temp != null && !temp.delete()) {
            log.warn("Failed to delete export temp file: {}", temp);
        }
    }
}

// ✅ 查询接口
@GetMapping("/export/tasks/{id}")
public ExportTaskDTO query(@PathVariable String id) { ... }
```

> 详见 `cc-async-task-pattern` skill —— 异步任务的状态机、超时、重试、幂等

---

## 通用检查清单

- [ ] 数据量预估超过 1 万行的导出是否用了流式 API
- [ ] 临时文件清理是否在 `try-finally` / `defer` / `with` / `using` 中（SXSSF 必须 `dispose()`）
- [ ] 临时目录是否检查了磁盘配额（容器环境 `/tmp` 可能很小）
- [ ] 流式 API 的限制是否告知了调用方（不能回写 / 不支持公式 / 必须 flush）
- [ ] PDF 库是否压测确认了真实内存占用，而不是只看到写入文件流
- [ ] 用户可控的 CSV / Excel 文本字段是否处理了公式注入前缀
- [ ] 导出接口是否异步化（任务 ID + 轮询 / WebSocket 通知）
- [ ] 错误恢复：流式写入中断时临时文件是否清理
- [ ] 是否设置了数据量上限（防止用户传 `pageSize=999999`）
- [ ] 大文件是否上传到对象存储而非内存返回

---

## 相关 skill

- `cc-async-task-pattern` —— 异步任务的状态机、超时、幂等
- `cc-query-performance-safety` —— 防止导出时 N+1、IN 子句过长
- `cc-field-mapping-safety` —— DTO 转换时字段映射一致性

---

## 规则溯源

```
> 📋 本回复遵循：`cc-streaming-export-safety` - [章节]
```
