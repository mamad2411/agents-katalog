---
name: security-app-file-upload
canonical_id: security.app.file_upload
aliases: [file-upload-security, upload-security, file-handling]
version: 1.0.0
status: stable
created_date: 2026-05-25
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
forbidden-tools: WebFetch
manual_gate_required: false
disable-model-invocation: false
standards_versions:
  - OWASP File Upload Cheat Sheet: living reference, checked 2026-05-25
  - OWASP ASVS: 5.0 (V5 File Handling)
  - OWASP Top 10: 2021 (A05 Misconfig + A04 Insecure Design)
  - NIST CSF: 2.0 (PR.DS)
sensitive_data_rules:
  never_read: [".env*", "secrets/**", "*.pem", "*.key", "real_uploaded_files/**"]
  never_write: ["actual user-uploaded content samples"]
  redact_on_output: ["user-provided filenames containing PII", "EXIF data with location/identity"]
upstream:
  - appsec-security-orchestrator
  - security-governance-threat-modeling (upload 是必检 abuse case)
downstream:
  - security-remediation
  - security-platform-secrets (signed URL secrets)
  - appsec-security-orchestrator (back with findings)
description: >-
  File upload security overlay - polyglots, content-type sniffing, AV/CDR scanning, sandboxed parsing, filename and path injection, archive bombs, signed URLs, storage backend isolation, served-back Content-Disposition, and parser hardening.
trigger_phrases:
  - file upload security / 文件上传安全 / upload validation
  - polyglot file / 多语言文件
  - antivirus / AV scan / CDR / content disarm
  - content-type sniffing / MIME sniffing
  - signed URL / pre-signed URL / S3 upload security
  - archive bomb / zip bomb / decompression bomb
---

# Security App — File Upload

## 1. Mission

文件上传是经典攻击面：polyglot / content-type 伪造 / 路径穿越 / 解析漏洞 / archive bomb / RCE via parser / XSS via served-back / IDOR via signed URL。本 skill 系统化覆盖。

**职责边界**：
- **owns**: upload validation / storage / serve-back / parser hardening
- **不做**: 替代 `security-platform-secrets`（signed URL secret 管理细节）

---

## 2. Activation Triggers

| Trigger | Action |
|---|---|
| 项目含 `multipart/form-data` endpoint | 默认激活 |
| 项目用 S3 / GCS / Azure Blob 用户 upload | 默认激活 + signed URL section |
| 项目处理 user-provided images / documents / videos | 默认激活 + parser hardening |
| 项目允许 archive upload (.zip / .tar / .rar) | 激活 archive bomb + path traversal |
| 项目处理 SVG / HTML / PDF / Office formats | 激活 parser-specific section |
| 项目 serve-back user uploads | 激活 served-back hardening |

---

## 3. 12-Step Upload Defense Checklist

### Step 1 — Auth + Authz
- Upload endpoint 强制 authenticated
- 每个 upload 校验 user 配额 + permission
- Multi-tenant 校验 tenant boundary

### Step 2 — Size Limits（多层）
- Per-file max（如 10 MB default; image 5 MB; video 100 MB；按类）
- Per-request max（避免 multipart 滥用）
- Per-user per-day total quota
- Per-IP per-minute rate
- 服务器 + 反向代理 + WAF 三层都设

### Step 3 — Content-Type 严格校验
- **不信任**客户端 Content-Type header
- **服务端**用 magic bytes / `file` / libmagic / `mime-types` library 重新探测
- 与声明的 Content-Type 必须**一致**（mismatch → reject）
- 与扩展名必须一致

### Step 4 — Extension Whitelist
- 白名单（不是黑名单）
- 检查 effective extension（`.tar.gz`、`.jpg.exe`、`.pdf.svg`）
- 全部小写后 normalize 比对
- 重命名为服务端生成 UUID + safe extension（不用 user filename）

### Step 5 — Polyglot Detection
- File 是否同时合法解析为多种格式（如 JPG + ZIP polyglot, GIFAR）
- 多层 magic bytes 检查
- 不允许 mismatch between magic bytes 和 declared type
- 特别警惕：JPEG with embedded PHP / SVG with `<script>` / PDF with embedded JavaScript

### Step 6 — Filename / Path 净化
- Strip `..`, `/`, `\`, `:`, null bytes
- 不让 user filename 决定服务端存储路径
- 服务端生成：UUID + safe extension
- 用户可见 filename（如 display in UI）单独存 metadata，不用作路径

### Step 7 — AV / CDR Scanning
- AV: ClamAV / VirusTotal API / 云端 AV
- CDR (Content Disarm & Reconstruction): 移除可疑 active content（macro / script / embedded object）
- 大文件 async scan + quarantine until clean
- AV 失败 → reject + alert

### Step 8 — Archive Bomb 防护
- Max decompressed size cap（如 100x compression ratio = suspect）
- Max file count in archive
- Max nesting depth
- 解压在 sandbox（cgroup / container / chroot）
- 不解压前先 inspect header

### Step 9 — Parser Hardening（按 format）
- **Image**: 用 sandbox image processor（ImageMagick policy.xml 严格 / sharp 安全 default）；strip EXIF（PII + location leak）
- **PDF**: disable JavaScript / external resource fetch
- **Office**: disable macros / external links
- **SVG**: strip `<script>`, `on*` handlers, `xlink:href` external
- **HTML**: 用 sanitizer (DOMPurify) ；禁止 served-back as text/html for untrusted
- **Video**: re-encode through ffmpeg with safe profile
- 解析在独立 process / container / Lambda
- 解析 timeout + memory cap

### Step 10 — Storage Backend Isolation
- Upload 存到独立 storage bucket（不与 application code / assets 同 bucket）
- Bucket 默认 private + block public access
- 服务端通过 signed URL serve（短期）
- 不用 user-provided path
- Lifecycle policy: auto-delete orphan / temp / abandoned uploads

### Step 11 — Served-back Hardening
- `Content-Disposition: attachment; filename="..."` for untrusted（强制 download，禁止 inline render）
- `X-Content-Type-Options: nosniff` 强制
- Served from 独立 domain（如 usercontent.example.com，cookie-less）
- 不允许 untrusted HTML / SVG served as `text/html` / `image/svg+xml`（强制 `application/octet-stream` 或 sanitized）

### Step 12 — Signed URL Design
- TTL 短（如 15 分钟）
- Method-restricted（PUT only for upload；GET only for download）
- IP / user agent 绑定（如适用）
- HMAC with rotation
- 不在 URL 泄露 internal storage path / bucket name
- Audit log: who issued, who consumed, when

---

## 4. Common Attack Patterns

| Attack | Defense |
|---|---|
| Upload `.php` / `.jsp` to web root → RCE | Whitelist extension + storage outside web root + safe served-back |
| Upload SVG with `<script>` → XSS | Strip script / `on*` / `<foreignObject>`; serve as `image/svg+xml` only after sanitize OR force download |
| Upload PDF with JavaScript → user RCE on download | Strip JS; disable JS in viewer; force download instead of inline |
| Upload ZIP bomb → DoS | Compression ratio cap + max files + sandbox decompression |
| Upload Polyglot JPG+ZIP → bypass content-type check | Multi-layer magic bytes + reject mismatch |
| Upload path traversal `../../etc/passwd` → write outside intended dir | Server-generated path + filename sanitization |
| Upload massive file → DoS | Multi-layer size limits |
| IDOR via signed URL guessing | HMAC + short TTL + audit |
| EXIF GPS coords leak user location | Strip EXIF on image processing |
| Stored XSS via served-back filename | Sanitize filename display + use ID for path |

---

## 5. Hard Rules

- ❌ **不**信任客户端 Content-Type
- ❌ **不**用 user-provided filename 作为存储路径
- ❌ **不**用 extension 黑名单（必须白名单）
- ❌ **不**让 untrusted HTML / SVG inline render
- ❌ **不**把 user upload 存到 web root / application code 同 bucket
- ❌ **不**用 long-lived signed URL（必须短 TTL）
- ❌ **不**让 archive 直接解压 without size + count + ratio cap
- ❌ **不**让 image processor parser default unsafe（ImageMagick policy.xml 必须 lock down）
- ❌ **不**serve user upload from same domain as application（cookie 盗 + XSS）
- ❌ **不**保留 EXIF（PII + location 风险）
- ❌ **不**忽略 AV scan 失败（fail closed not open）

---

## 6. Anti-patterns

- ❌ "用了 multer / formidable / busboy 就安全" — library 帮你 parse，不帮你 validate
- ❌ "S3 pre-signed URL 客户端直传更安全" — 仍要 enforce content-type + size + 验证完后端调用
- ❌ "用扩展名校验就够" — `.jpg.exe` / Unicode / null byte 都能 bypass
- ❌ "ClamAV 装了就好" — AV 漏报率高，配合 CDR + sandbox parsing
- ❌ "PDF 是文档，安全" — PDF JS / 字体 / 嵌入对象都是攻击面
- ❌ "SVG 是图像" — SVG 是 XML，可含 script / 外部资源
- ❌ "用户自己的文件，安全" — multi-user 平台，user A 上传 user B 下载 = XSS / 钓鱼
- ❌ "Image 处理用 ImageMagick default" — 多年来历史漏洞 (ImageTragick 等)，必须 policy.xml lock
- ❌ "Filename 给用户看正常，存的时候 sanitize" — display 也要 sanitize 防 stored XSS

---

## 7. Output Contract

每次 review 产出：

1. Upload endpoint inventory（per-endpoint policy）
2. 12-step checklist coverage matrix
3. Allowed MIME / extension whitelist（per-feature）
4. Storage isolation status（bucket per type / 独立 domain serve）
5. Signed URL design audit（TTL / method / HMAC）
6. AV / CDR / parser hardening config
7. Common attack pattern verification
8. EXIF / metadata stripping verification
9. SECURITY.md File Upload section + AppSec Release Evidence §12 叠加层
10. **Findings** —— 全部经 `appsec-sdk finding.add <file>`（canonical path，redact-first）落 `.appsec/findings/<tag>/`，符合 orchestrator §9 finding schema v1.0：
    - `source`（`manual_review` 或 sast 命中）；`severity` **小写**（critical/high/medium/low）；`cwe`；`reproduction_steps`（**禁含 raw secret / raw token / user-provided PII 文件名**——脱敏）
    - `asvs_mapping` 用版本化三段格式 `v5.0.0-<ch>.<sec>.<req>`（正则 `^v5\.0\.0-\d+\.\d+\.\d+$`；File Handling 用 ASVS V5），不用 4.x `V5.x` 旧标签
    - **绝不** Write 直写 `.appsec/findings/**`（orchestrator hook §18.5a 物理拦截 Write/Edit/MultiEdit）；只走 sdk
    - high+ finding → `security-remediation`（fix → 回归测试）；signed URL secret 命中 → `security-platform-secrets`

### 7.1 Overlay Evidence Contract（满足 release gate — 不可省）

> 起因：appsec-evidence-validator（orchestrator §16.9 check #3）对**每个激活的 overlay** HARD-REQUIRE `.appsec/evidence/<tag>/overlay-<name>/checklist.yaml`，缺一即 release **BLOCKED**。本 overlay 的 `<name>` = `file_upload`。

每次 review 结束，**两步落盘**（按序）：

1. **标记 overlay active**：
   ```bash
   appsec-sdk overlay.activate "<release-tag>" file_upload
   # → 建 .appsec/evidence/<tag>/overlay-file_upload/ + 写 .activated 标记
   ```
2. **写 overlay checklist evidence**（这是 validator 真正校验的文件）：
   - 写 `.appsec/evidence/<release-tag>/overlay-file_upload/checklist.yaml`
   - 直接 Write 即可（evidence 路径不被 hook 拦；只有 `.appsec/findings/**` + `.appsec/decisions/**` 被 §18.5a 拦）
   - 内容：把 §3 的 12-step checklist 逐项转成 `items[]`（每项 `id` / `requirement` / `asvs_ref`（`v5.0.0-5.x.x`）/ `status: pass|fail|na|not_tested` / `evidence_ref` / `notes`）+ `summary{total, pass, fail, na}`
   - 任何 `status: fail` 必须在 `evidence_ref`/`notes` 引用对应 `finding.add` 出的 finding id（finding 本体走 sdk，不塞进 checklist）
   - 模板：[`appsec-security-orchestrator/templates/overlay-checklist.template.yaml`](../appsec-security-orchestrator/templates/overlay-checklist.template.yaml)（含 file_upload 示例 items：content-type 校验 / size limit / AV scan / path traversal / stored-XSS on filename / archive bomb / storage isolation / EXIF strip）

无此 checklist.yaml → §16.9 validator BLOCK 整个 release。

---

## 8. References

- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- [OWASP ASVS 5.0 V5 File Handling](https://owasp.org/www-project-application-security-verification-standard/)
- [Image processor sandbox patterns](https://imagemagick.org/script/security-policy.php)
- [appsec-security-orchestrator](../appsec-security-orchestrator/SKILL.md) — §9 finding schema / §16.3 overlay activation / §16.9 evidence validation / §18.5a finding-path hook
- [overlay-checklist.template.yaml](../appsec-security-orchestrator/templates/overlay-checklist.template.yaml) — overlay-file_upload/checklist.yaml 模板
- [security-platform-secrets](../security-platform-secrets/SKILL.md) — signed URL secrets
- [security-governance-threat-modeling](../security-governance-threat-modeling/SKILL.md) — upload abuse cases
