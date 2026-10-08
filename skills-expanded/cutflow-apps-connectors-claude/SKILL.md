# apps/connectors

离线 ETL 连接器层，把外部投放平台导出的离线归档解析成案例指标导入请求；当前仅 OceanEngine/巨量引擎。与主 API 分离的独立进程，自带 CLI，不发任何网络请求——只产出 payload。

## 职责
- 遍历 RPA 归档树 `<archive_root>/raw/<date>/<source_page>/<run_id>/<file>.xlsx`，解析 XLSX → 归一化 → 去重 → 产出 `MetricsImportRequest`。
- 支持 4 个 source_page：`video_analysis` / `localpush_account` / `localpush_unit` / `comment_content`（comment 无 spend 指标，但仍按点赞/回复等 engagement 计数产出导入行）。
- 把各页中文列名归一成统一形态：`external_ref` + 英文键的数值 `metrics` map + 文本 `attributes` + 原始 `raw`，每行带内容 `row_fingerprint`。
- 两级去重（文件 sha256 + 行 fingerprint）使重复导入成为整体跳过/仅增量行，幂等。
- POST 到 `POST /api/cases/{case_id}/metrics/import` 由调用方负责（连接器不投递）。

## 关键文件
- `oceanengine/ingest.py` — 主入口：`import_archive_tree` / `import_archived_xlsx`，`IngestResult`/`IngestSummary`，`build_import_rows`（每条 metric 一行）、`infer_source_page`、`default_archive`。
- `oceanengine/cli.py` — `python -m apps.connectors.oceanengine.cli {import-archive|import-file}`（prog `oceanengine-connector`），打印 JSON。
- `oceanengine/normalize.py` — 每页 normalizer + `NORMALIZERS` 注册表。
- `oceanengine/xlsx.py` — openpyxl 懒加载读首个 sheet（`read_first_sheet`）；缺失抛 `XlsxUnsupportedError`，`openpyxl_available()` 可探测。
- `oceanengine/metrics.py` — `parse_number`/`parse_int`（中文货币/百分比）、`pick` 别名容错、`canonical_json`、`hash_row` 指纹。
- `oceanengine/archive.py` — 本地 SQLite 去重库（`ImportArchive`，默认 `<archive_root>/db/oceanengine_offline.sqlite3`），无密钥。

## 约定与要求
- contract-first：导入行结构来自 `packages.core.contracts`（`MetricsImportRequest`/`OceanEngineMetricRow`/`OceanEngineSourcePage`，定义在 `cases.py`），改字段须同步 contracts。
- 确定性：fingerprint 走 `canonical_json`（sort_keys）+ sha256，必须可复现；blank/占位单元格返回 `None`，不得静默归零。
- 离线 ETL 不猜 `publish_record_id`，只带 `external_ref` + `oceanengine_row_fingerprint` 交给 API 端匹配。
- openpyxl 是可选依赖：缺失不崩溃，标 `status="unsupported"` 显式上报。

## 测试
- `pytest tests/connectors`（`test_oceanengine_import.py`，`pytest.importorskip("openpyxl")` + 测试时合成 XLSX）。

## 坑
- 真实归档 XLSX 尚缺，端到端验收仅靠合成 fixture。
- 路径须严格 4 段 `raw/<date>/<source_page>/<run_id>/<file>.xlsx`，否则 `infer_source_page` 报错。
- CLI 仅产出 payload，不写库/不投递；推送与 outbox 去重由调用方处理。
