---
name: uibp-push-guard
description: >
  在每次新会话开始时检查用户第一条提示词是否包含项目名称、项目作者、项目描述，缺失则主动提问补齐；
  在用户要求推送 Docker 镜像到 UIBP 底座时检查本体用户名、本体密码、推送路径、英文项目名称是否齐全，缺失则主动提问补齐；
  每次推送前强制将版本号增加 0.1 并作为 Docker TAG；推送成功后询问用户是否保存本体密码。
allowed-tools: Bash, Read, Write, Edit
---

# 项目信息与推送守护技能

本技能用于保证每个会话开始和每次推送前都满足强制的信息完整性要求。

## 状态文件

- 默认状态文件路径：`{{project_root_dir}}/<project_name_en>/.push-guard-state.json`
- 辅助脚本路径：`{{current_skill_dir_path}}/scripts/guard.py`

状态文件结构：

```json
{
  "project_name": "",
  "project_author": "",
  "project_description": "",
  "project_name_en": "",
  "body_username": "",
  "body_password": "",
  "push_path": "",
  "version": "0.0"
}
```

- `project_name_en` 为英文项目名称，用于 Docker 镜像名。
- `push_path` 为完整 Docker 仓库路径（不含 TAG），例如 `reg.saitron.net/uibp_user/my-app`。
- `version` 初始值为 `0.0`，表示尚未推送；每次推送前将 `version` 增加 `0.1`，并作为 Docker TAG，例如 `0.0 -> 0.1`、`0.1 -> 0.2`、`1.0 -> 1.1`。

---

## 一、新会话开始检查

在收到本会话**第一条用户消息**时，按以下步骤执行：

1. 从第一条消息中提取以下三个字段：
   - `项目名称`：项目叫什么。
   - `项目作者`：作者或负责人是谁。
   - `项目描述`：项目做什么、目标是什么。

2. 如果三个字段**全部存在且明确**，继续第 3 步；否则先只询问缺失字段：
   ```
   开始前请先补充以下项目信息：
   1. 项目名称
   2. 项目作者
   3. 项目描述
   ```
   - 等待用户补齐后继续。
   - 在补齐前不要执行开发、修改、推送等其他任务。

3. **自动生成英文项目名称** `project_name_en`：
   - 如果第一条消息中用户已经给出英文项目名称，优先使用用户给出的名称。
   - 否则根据 `项目名称`、`项目描述` 等内容自动生成，例如使用拼音、英文翻译或简洁英文短语。
   - 规范化规则：
     - 只保留小写字母、数字、`-`、`_`、`.`；
     - 空格统一转为 `-`；
     - 不能以分隔符开头或结尾；
     - 例如：`示例项目` 可生成 `demo-project` 或 `example-project`。
   - 将生成结果告知用户，例如：
     ```
     已自动创建英文项目名称：demo-project
     ```

4. **创建项目目录**：
   - 以 `project_name_en` 为目录名，在项目根目录下创建：
     ```bash
     mkdir -p {{project_root_dir}}/<project_name_en>
     ```
   - 此后本项目的**所有文件**（代码、配置、文档、`.push-guard-state.json` 等）都必须创建在该目录下。
   - 如果目录已存在，直接复用，不删除、不覆盖已有内容。

5. **在项目目录内写入状态文件**：
   ```bash
   python {{current_skill_dir_path}}/scripts/guard.py init --state {{project_root_dir}}/<project_name_en>/.push-guard-state.json
   python {{current_skill_dir_path}}/scripts/guard.py set --key project_name --value "提取到的项目名称" --state {{project_root_dir}}/<project_name_en>/.push-guard-state.json
   python {{current_skill_dir_path}}/scripts/guard.py set --key project_author --value "提取到的项目作者" --state {{project_root_dir}}/<project_name_en>/.push-guard-state.json
   python {{current_skill_dir_path}}/scripts/guard.py set --key project_description --value "提取到的项目描述" --state {{project_root_dir}}/<project_name_en>/.push-guard-state.json
   python {{current_skill_dir_path}}/scripts/guard.py set --key project_name_en --value "生成的英文项目名称" --state {{project_root_dir}}/<project_name_en>/.push-guard-state.json
   ```

6. 完成上述步骤后，继续执行用户请求，并把项目文件写入 `{{project_root_dir}}/{{project_name_en}}/` 下。

---

## 二、Docker 推送前检查

推送目标为 **UIBP 底座**，规则为：

```bash
docker push reg.saitron.net/<本体用户名>/<英文项目名称>[:TAG]
```

其中：
- `本体用户名` 用于 `docker login`。
- `英文项目名称` 必须与新会话开始时生成的 `project_name_en` 完全一致，并对应项目目录名。
- `[:TAG]` 为版本号 TAG，由版本号强制 `+0.1` 后自动获得，例如 `0.1`。

当用户消息包含明确推送意图时（如：`推送`、`push`、`上传推送`、`发布推送`、`推到...`），按以下步骤执行：

### 1. 确认推送要素

必须确认以下字段都齐全：

- `本体用户名`：用于 `docker login`。
- `本体密码`：用于 `docker login`。
- `英文项目名称` `project_name_en`：优先从状态文件读取；如果缺失，先补齐项目信息并自动生成。
- `推送路径`：默认**自动生成**，无需用户额外提供：

  ```
  push_path = reg.saitron.net/<body_username>/<project_name_en>
  ```

  如果用户消息或环境变量 `PUSH_PATH` 提供了完整路径，则优先使用该路径，但其最后一段必须与 `project_name_en` 相同；不一致时提醒用户，并以 `project_name_en` 为准。

字段来源优先级：

1. 环境变量：`BODY_USERNAME`、`BODY_PASSWORD`；`PUSH_PATH` 可选覆盖自动生成的路径。
2. 当前用户消息中明确给出的值。
3. 状态文件 `{{project_root_dir}}/<project_name_en>/.push-guard-state.json` 中已保存的值。
4. 自动生成：`push_path = reg.saitron.net/<body_username>/<project_name_en>`。

### 2. 缺失则提问

如果 `本体用户名` 或 `本体密码` 缺失：

- 只询问缺失字段。
- 例如：
  ```
  推送前请先补充以下信息：
  1. 本体用户名
  2. 本体密码
  ```
- 等待用户补齐后再继续推送流程。
- 在补齐前**不得执行 `docker login` 或 `docker push`**。

### 3. 写入自动生成的推送路径

如果状态文件中 `push_path` 为空，执行：

```bash
python {{current_skill_dir_path}}/scripts/guard.py set --key push_path --value "reg.saitron.net/实际本体用户名/生成的英文项目名称" --state {{project_root_dir}}/<project_name_en>/.push-guard-state.json
```

### 4. 执行 Docker 登录

推送前必须先登录 UIBP 底座镜像仓库：

```bash
printf '%s\n' "$BODY_PASSWORD" | docker login reg.saitron.net -u "$BODY_USERNAME" --password-stdin
```

- 如果环境变量不可用，则在当前会话中临时使用用户提供的本体用户名和本体密码执行等价命令。
- 登录成功后再执行镜像推送。

### 5. 询问是否保存本体密码

`docker login` 成功后，必须询问用户：

```
是否将本体密码保存到状态文件？
```

- 用户明确同意后，才写入状态文件：
  ```bash
  python {{current_skill_dir_path}}/scripts/guard.py set --key body_password --value "用户提供的本体密码" --state {{project_root_dir}}/<project_name_en>/.push-guard-state.json
  ```
- 用户不同意或未明确同意，则本体密码只在当前会话中使用，不落盘。
- 优先建议用户使用环境变量 `BODY_PASSWORD`，避免明文保存本体密码。

---

## 三、构建镜像 + 版本号 +0.1（强制）

每次推送前必须执行版本号递增并构建镜像，规则如下：

1. 确保状态文件存在：
   ```bash
   python {{current_skill_dir_path}}/scripts/guard.py init --state {{project_root_dir}}/<project_name_en>/.push-guard-state.json
   ```

2. 递增版本号：
   ```bash
   python {{current_skill_dir_path}}/scripts/guard.py bump-version --state {{project_root_dir}}/<project_name_en>/.push-guard-state.json
   ```
   脚本会输出新版本号，例如 `0.1`。

3. 构建并直接推送 Docker 镜像，并把以下项目信息写入 OCI annotation（这样才能通过 Harbor API 在顶层 `annotations` 字段中看到项目信息，与 tangshan-weather 的最终效果一致）：

   - `project_name`
   - `project_author`
   - `project_description`
   - `project_name_en`

   使用 `docker build --push`，并加上 `--provenance=false --sbom=false`（否则会生成 OCI index + attestation，annotation 落在内层 manifest 上，Harbor API 顶层 artifact 读不到），把 annotation 合并成**一行**：

   ```bash
   docker build --push --provenance=false --sbom=false --annotation "project_name=<项目名称>" --annotation "project_author=<项目作者>" --annotation "project_description=<项目描述>" --annotation "project_name_en=<英文项目名称>" -t reg.saitron.net/<body_username>/<英文项目名称>:<新版本号> {{project_root_dir}}/<英文项目名称>
   ```

   注意：这里使用 `--annotation`，不要使用 `--label`；`--annotation` 需要配合 `--push` 才能写入，且必须加 `--provenance=false --sbom=false` 保证生成的是单 OCI manifest，这样 Harbor API 顶层 `annotations` 才会展示项目信息。

   如果镜像已经构建过且代码未变化，可跳过重复构建，但必须确认镜像已带有上述 annotations。

4. `--push` 会直接完成推送，无需再单独执行 `docker push`；镜像名使用与项目目录同名的 `project_name_en`，推送目标示例：

   ```text
   reg.saitron.net/uibp_user/my-app:0.1
   ```

5. 在推送说明中明确包含新版本号。

6. 步长固定为 `0.1`，不得跳号或使用其他步长；TAG 直接使用新版本号，不加 `v` 前缀。

---

## 四、辅助脚本命令

```bash
# 初始化状态文件（已存在则补全默认字段）
python {{current_skill_dir_path}}/scripts/guard.py init --state {{project_root_dir}}/<project_name_en>/.push-guard-state.json

# 写入某个字段
python {{current_skill_dir_path}}/scripts/guard.py set --key project_name --value "示例项目" --state {{project_root_dir}}/<project_name_en>/.push-guard-state.json

# 读取某个字段
python {{current_skill_dir_path}}/scripts/guard.py get --key version --state {{project_root_dir}}/<project_name_en>/.push-guard-state.json

# 检查当前状态文件还缺哪些字段
python {{current_skill_dir_path}}/scripts/guard.py missing --scope session --state {{project_root_dir}}/<project_name_en>/.push-guard-state.json
python {{current_skill_dir_path}}/scripts/guard.py missing --scope push --state {{project_root_dir}}/<project_name_en>/.push-guard-state.json

# 查看完整状态（本体密码会脱敏显示）
python {{current_skill_dir_path}}/scripts/guard.py show --state {{project_root_dir}}/<project_name_en>/.push-guard-state.json
```

---

## 五、执行原则

1. **先补齐，后执行**：任何强制信息缺失时，先提问并等待，不执行用户请求的主体任务。
2. **只问缺失项**：用户已经提供的信息不要重复询问。
3. **版本号不可跳过**：每次推送都必须先完成 `+0.1` 并留下记录。
4. **安全优先**：本体密码默认不落盘，优先使用环境变量；`docker login` 成功后必须询问用户是否保存本体密码，用户明确同意后才写入状态文件。
