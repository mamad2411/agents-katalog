---
name: acf-python-task-package
description: Generate AutoCodeFlow-compatible automation Python task packages that can be zipped, uploaded (executor-package / application-zip channel), and version-iterated. Use when the user asks to create, scaffold, package, upload, or version a Python automation task/script for the AutoCodeFlow platform, or mentions manifest.yaml / requirements.txt task upload, 打包上传, 执行器包, 任务包, 版本迭代.
---

# AutoCodeFlow Python 任务包

> **受众**：要按规范打包 Python 任务的开发者（完整规范） · **状态**：稳定 · **最后核对**：2026-11-02

给 AI 的规范：产出一个**能被 AutoCodeFlow 平台接受、打包成 zip 上传部署、并支持版本迭代**的自动化 Python 任务包。

> 完整可复制模板见 [TEMPLATE.md](TEMPLATE.md)；结构校验与打包脚本见 `scripts/package.py`。
> 平台侧原始说明：`docs/autoapp-skill.md`；执行器实际消费逻辑：`apps/executor-python/manifest.py`、`apps/executor-python/routers/execute.py`。

## ⚠️ 铁律：这不是 pip 包

- **禁止** `pyproject.toml` / `setup.py` / `pip build` / `.whl` / `.tar.gz` 作为任务包载体。
- 任务包 = **一个 zip**，平台解压后**直接执行脚本**。
- 平台靠根目录 `manifest.yaml` 识别入口，靠 `requirements.txt` 装依赖。
- 打 `.whl` / `.tar.gz` 只用于「执行器本体」发布，**不是**业务任务包，别混淆。

## 项目结构（固定，勿改）

```text
my-app/
├── manifest.yaml        # 必须，在 zip 根目录（不要多套一层目录）
├── main.py              # 任务入口脚本（entrypoint 指向它；也可放 tasks/main.py）
└── requirements.txt     # 仅当有第三方依赖时需要
```

- **不要** `__init__.py` / `pyproject.toml` / `setup.py` / `Dockerfile` / `src/`。
- 业务代码可按需拆分子目录（如 `tasks/`、`lib/`），但 `manifest.yaml` 与 `requirements.txt` 必须在根。

## manifest.yaml 字段（执行器实际读取）

执行器读 `manifest.yaml`（或 `manifest.yml`）并用**任务字段覆盖 manifest 字段**：

| 字段 | 含义 | 默认 | 备注 |
|------|------|------|------|
| `runtime` | `python` 或 `node` | `python` | zip 应用渠道须与任务 runtime 一致 |
| `entrypoint` | 相对 zip 根的脚本路径 | `main.py` | 例：`tasks/main.py` |
| `timeout` | 执行超时秒数 | 平台默认 | `0` = 不限时 |
| `requirements` | 依赖列表（list） | 无 | 与包内 `requirements.txt` 合并 |
> **执行器运行 zip 任务时只消费 `runtime/entrypoint/timeout/requirements` 四个字段**（`apps/executor-python/manifest.py`）。
> `name/version` 由**应用(application)记录**承载（上传时指定，见「上传部署」）；单入口任务用 `entrypoint` 即可，**不必写 `tasks[]`**。
> 多任务自动注册仅在 **git 仓库部署**时读取根目录的 **`manifest.json`**（JSON，非 zip 的 manifest.yaml），任务项字段是 `entrypoint`（`apps/admin-api/.../application.service.ts`）——zip 单入口任务不涉及它，别把两套混用。

## 任务脚本契约（main.py）

脚本只需一个 `main()`：**返回 dict = 成功，抛异常 = 失败**。执行结果回调由执行器统一处理，**任务脚本不需要持有平台 token**。

> ⚠️ **成败判定只看进程退出码**。执行器检查的是子进程 `returncode`（`apps/executor-python/routers/execute.py` 的 `if proc.returncode != 0:`），**不解析返回的 dict**。
> 因此 `except` 里 `return {"success": False}` 会让进程以退出码 0 结束 → 平台判为**成功**（假绿）。要失败必须 **`raise`**。

```python
import os, json

def main() -> dict:
    target = os.environ.get("AUTOFLOW_TARGET", "prod")   # 参数以 AUTOFLOW_ 前缀注入
    # ...业务逻辑...
    return {"success": True, "target": target}

if __name__ == "__main__":
    print(json.dumps(main(), ensure_ascii=False, default=str))   # 本地调试
```

**推荐用官方 SDK**（能力探测 + 主动回调更规范）：`import autoflow_sdk` 并加入 `requirements.txt`。
写法见 [TEMPLATE.md](TEMPLATE.md) 的 SDK 版入口。

### 平台注入的环境变量

| 变量 | 说明 |
|------|------|
| `TASK_ID` / `TASK_NAME` / `EXECUTION_ID` | 任务与本次执行标识 |
| `AUTOFLOW_<KEY>` | 触发时传入的运行时参数（读参优先级：`AUTOFLOW_*` > 代码默认值）|
| `AUTOFLOW_ADMIN_API_URL` | Admin API 基址（N23 起，回调可用时注入）|
| `AUTOFLOW_CALLBACK_TOKEN` | 一次性 `v1.` HMAC token，绑定本次 executionId（N23 起）|
| `AUTOFLOW_EXECUTOR_ADDRESS` | 执行器注册地址（N27 起，SDK 自动补进回调项）|
| `AUTOFLOW_ARTIFACTS_DIR` | 产物目录 `<work_dir>/artifacts/`（FEAT-05，执行器已预建）|
| `AUTOFLOW_TRACE_ID` | 链路追踪 ID（仅 admin 开启追踪时注入）|

旧版自建执行器不注入回调凭证 → `ctx.callback.enabled == False`，任何上报抛 `CallbackDisabledError`（fail-closed）。**必须先能力探测再回调**，不可用时降级为「只打日志、继续执行」。

### ⚠️ 参数键名陷阱（camelCase 会静默失效）

执行器注入时把键名**大写**（`AUTOFLOW_{k.upper()}`），而 Python SDK 读回时把键名**小写**（`context.py`: `params[k[len("AUTOFLOW_"):].lower()]`）。后果：

- 任务参数写成 `sourceDir` → `ctx.params` 里只有 `sourcedir`
- `ctx.get_param("sourceDir")` 返回 **`None`**，**静默落回代码默认值**，不报错

**纪律**：顶层参数名一律用**全小写**（`sourcedir`、`createtestfiles`）。数组/对象**内部**的键不受影响（整体 JSON 序列化后传递），如 `operations[].preserveStructure` 保持 camelCase。

## 执行产物（artifacts，FEAT-05）

任务产生的文件（截图 / 报表 / CSV …）**只有**通过产物通道才能在 UI 看到。把文件写进 `AUTOFLOW_ARTIFACTS_DIR`，执行器在任务结束时扫描该目录、上传文件，并把清单 `[{name, size, sha256}]` 随终态回调上报，用户即可在**执行详情页**查看/下载。

```python
import os
from pathlib import Path

def main() -> dict:
    # 执行器注入并预建该目录；本地裸跑时回退到临时目录
    art_dir = Path(os.environ.get("AUTOFLOW_ARTIFACTS_DIR", "/tmp/artifacts"))
    art_dir.mkdir(parents=True, exist_ok=True)
    (art_dir / "report.csv").write_text("a,b\n1,2\n", encoding="utf-8")
    return {"success": True, "artifact": "report.csv"}
```

Node 侧对等：`process.env.AUTOFLOW_ARTIFACTS_DIR`。

**硬约束**（`apps/executor-python/artifacts.py` / `apps/executor-node/src/artifacts.ts`，与 admin 侧同源）：

| 约束 | 值 |
|------|-----|
| 文件数上限 | **20**（超出部分静默跳过）|
| 单文件大小上限 | **100 MB** |
| 文件名 | 须匹配 `^[A-Za-z0-9][A-Za-z0-9._-]{0,254}$`（字母/数字开头；禁空格、`#`、前导 `.`/`_`）|
| 扫描范围 | 仅**顶层**普通文件，**不递归**子目录 |
| 失败语义 | best-effort：收集/上传任何异常只记日志，**绝不**阻塞终态回调 |

> 清单只收录**实际上传成功**的条目。把文件写到 `/tmp`、或只把路径放进返回 dict，UI 里都看不到。
> 例：RPA 截图任务把 `pyautogui.screenshot()` 的目标路径指向该目录，截图即出现在执行详情页。

## 依赖（requirements.txt）红线

- **只能写包规格**：`requests>=2.31`、`acfdemopkg` 等。**禁止以 `-` 开头的 option 行**（如 `--index-url`），执行器 R4-C 直接拒绝，防索引劫持。
- 私服源由执行器侧 `PYPI_REGISTRY_URL` 配置，**不写进** requirements.txt。
- 包内 `requirements.txt` 与任务级 `requirements` **合并**：任务级同名覆盖、其余并集、顺序稳定。
- 大小写不敏感扫描 zip 顶层的 `requirements.txt`；单文件超字节上限会被**忽略**（改用任务级依赖）。
- requirements 仅对**打包(entrypoint)任务**生效，glue 脚本任务忽略。

## Python 版本声明（多版本运行时）

- 可声明区间 `3.7 ~ 3.14`，格式必须是 `主.次`（`^\d+\.\d+$`，如 `3.12`），否则 400。
- **在线可下载** = `3.8 ~ 3.14`（主路径）；`3.7` 仅「离线预填缓存卷」，声明 3.7 但池无 3.7 → 失败分因 `interpreter_unavailable`。
- Tier1（完全支持）：`3.10 / 3.11 / 3.12 / 3.13 / 3.14`。**无特殊需求优先选 3.12**。
- 版本在**任务**上声明（`runtimeVersion`），不写进 manifest；不声明 = 走宿主默认解释器（存量行为不变）。

## 打包成 zip（关键：manifest 必须在根）

优先用脚本，自动校验 + 正确布局 + 排除垃圾文件：

```bash
python scripts/package.py my-app/
# 产物：../my-app-1.0.0.zip（版本号取自 manifest.yaml）
```

手动打包（等价）：

```bash
cd my-app/
zip -r ../my-app-1.0.0.zip manifest.yaml main.py tasks/ requirements.txt
unzip -l ../my-app-1.0.0.zip   # 根须直接是 manifest.yaml / main.py
```

❌ 错误（会多套一层目录，平台找不到 manifest）：

```bash
zip -r my-app-1.0.0.zip my-app/
```

zip 安全红线（执行器 vet+safe_extract 强制）：不得含 `..` 逃逸、绝对路径、盘符路径、符号链接条目；压缩方法仅 stored/deflate；有条数/单文件/总解压量/压缩比上限。`scripts/package.py` 已规避（相对路径、只存实际业务文件）。

## 上传部署

**业务 Python 任务包 = 一个「应用(application)zip」**，执行器通过任务上的 `packageUrl`（由 admin 从 `applications` 表解析）下载并运行。上传走应用上传端点：

管理后台：**应用管理 → 上传**（填 name/runtime=python，选 zip，≤200MB，zip 魔数 + zip-bomb 结构审查 + 可选 ClamAV 扫描）。

API（AI agent 用这个）：

```bash
# 1) 登录取 token（响应字段是 accessToken，驼峰；不是 access_token）
TOKEN=$(curl -s -X POST http://<HOST>:3105/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"<PASSWORD>"}' \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['accessToken'])")

# 2) 上传应用 zip（multipart 字段：file / name / runtime）
curl -X POST http://<HOST>:3105/api/applications/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "name=my-app" -F "runtime=python" \
  -F "file=@my-app-1.0.0.zip"
# -> 返回 Application 记录，含 id（记下来，建任务用）
```

> 另有 `POST /api/executor-packages`（字段 `name/version/type`）与 `PATCH :id/deprecate`、`:id/activate`、`:id/push` 端点，用于**分发执行器本体运行环境到各执行器节点**，不是业务任务包的正牌部署路径；业务任务请用上面的 `applications/upload`。

创建任务：`POST /api/tasks`，代码来源三选一互斥（`gitRepo` / `glueSource` / `codeSource='application_zip'`+`applicationId`）。zip 任务示例：

```bash
curl -X POST http://<HOST>:3105/api/tasks \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{
    "name": "每日跑批",
    "triggerType": "cron",
    "cronExpression": "0 9 * * *",
    "runtime": "python",
    "runtimeVersion": "3.12",
    "codeSource": "application_zip",
    "applicationId": "<APP_UUID>",
    "entrypoint": "main.py",
    "params": {"target": "prod"}
  }'
```

关键 DTO 字段（`apps/admin-api/src/modules/task/dto/create-task.dto.ts`，**没有** `executorPackageName` / `taskEntry` / `scheduleType` 这些字段）：

- `triggerType`：**必填**，枚举 `manual | cron | fixed_rate | api`（不是 `scheduleType`）。
- `applicationId` + `codeSource="application_zip"`：引用上传的应用包（不是 `executorPackageName`）。
- `entrypoint`：入口脚本路径（不是 `taskEntry`）；缺省读包内 manifest 的 `entrypoint`。
- `runtimeVersion`：可选，`X.Y` 格式；`cron` 时配 `cronExpression`。
- `alarmEmail` / `alarmChannels`：告警配置（**没有** `notificationConfig`）。
- `id`：可选，若提供必须是 **UUID v4**。

### 常见错误字段名对照

全局 ValidationPipe 开了 `whitelist: true` + `forbidNonWhitelisted: true`（`apps/admin-api/src/main.ts`），**请求体里任何未知字段都会 400**。以下名字是历史文档里的错误写法：

| ❌ 错误写法 | ✅ 正确写法 |
|------------|------------|
| `scheduleType` | `triggerType` |
| `taskEntry` | `entrypoint` |
| `executorPackageName` | `applicationId` + `codeSource="application_zip"` |
| `notificationConfig` | `alarmEmail` / `alarmChannels` |
| 响应字段 `access_token` | `accessToken`（驼峰）|

### cron 表达式：严格 5 段纯数字

`cronExpression` 只接受 **5 段**（`分 时 日 月 周`）、**纯数字**（`apps/admin-api/src/modules/task/dto/cron-expression.constraint.ts`）：

| 写法 | 结果 |
|------|------|
| `0 9 * * *` | ✅ 每天 9:00 |
| `0 9 * * 1-5` | ✅ 工作日 9:00 |
| `*/30 * * * *` | ✅ 每 30 分钟 |
| `0 12,18 * * *` | ✅ 每天 12 点与 18 点 |
| `0 9-17 * * *` | ✅ 时段范围 |
| `0 0 9 * * *` | ❌ 6 段（带秒）→ 400 |
| `0 */30 * * * *` | ❌ 6 段 → 400 |
| `0 12 * * sun` | ❌ 星期名 → 400（只认数字）|
| `0 12 * jan *` | ❌ 月名 → 400（只认数字）|

## 版本迭代（发新版）

`Application` 带 `version` 列，平台按应用维度保留版本历史/快照（`ApplicationVersion`）。发版流程：

1. 改代码/依赖。
2. 重新打包（产物名带新版本号，便于人工核对）：`python scripts/package.py my-app/`。
3. 以同一 `name` 上传新版本 zip（`POST /api/applications/upload`）→ 平台按 name upsert、版本递增。
4. 让任务指向新版本：更新任务的 `applicationId` 指向新记录，或对旧包执行废弃：

```bash
# 废弃旧执行器包（仅 executor-packages 渠道有该端点；applications 渠道以版本历史管理）
curl -X PATCH http://<HOST>:3105/api/executor-packages/<OLD_PKG_ID>/deprecate \
  -H "Authorization: Bearer $TOKEN"
```

**迭代纪律**：入口 `entrypoint` 尽量向后兼容，改了要同步任务配置；`secrets`/接口如有 schema 变更，在 CHANGELOG 记录并优先「新增可缺省字段」而非破坏性改动。

## 验证

```bash
# 手动触发
curl -X POST http://<HOST>:3105/api/tasks/<TASK_ID>/trigger \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"params":{"target":"test"}}'

# 查执行结果
curl "http://<HOST>:3105/api/executions?taskId=<TASK_ID>" \
  -H "Authorization: Bearer $TOKEN"
```

失败分因排查：`interpreter_unavailable`（版本不可得）、`dependency_install_failed`（依赖）、`script_error`（脚本报错）。
