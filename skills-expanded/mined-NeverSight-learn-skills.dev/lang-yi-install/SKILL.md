---
name: lang-yi-install
description: |
  意心会内部 ASOP Skill 安装器。从飞书云空间下载并部署 skill/tool 到本地。
  触发方式：/lang-yi-install、「安装意心会skill」「部署内部skill」「同步飞书skill」
  YiXinHui internal ASOP skill installer. Downloads and deploys skills/tools from Feishu Drive.
  Trigger: /lang-yi-install, "install yi skills", "deploy internal skills", "sync feishu skills"
---

# lang-yi-install — 意心会内部 Skill 安装器

从飞书云空间动态扫描并下载意心会内部 ASOP skill 到本地 `~/.claude/` 目录。

## 前置条件

- `lark-cli` 已安装：`npm install -g @larksuite/cli`
- `lark-cli config init --new` 已完成初始化
- `lark-cli auth login` 已完成认证
- 需要以下 scope（环境检查会自动校验）：
  - `drive:drive:readonly`（列出文件夹内容）
  - `drive:file:download`（下载文件）

## 默认飞书文件夹

**YiXinSKILL**：`https://fcntz0gsnz8y.feishu.cn/drive/folder/B06yfyHVXl9SqWd4pk6cw29SnSc`

## 使用方式

用户调用 `/lang-yi-install` 后：

1. 如果用户提供了飞书文件夹 URL，使用该 URL
2. 如果没有提供，使用默认 URL（YiXinSKILL）
3. 执行下载部署流程

---

## 执行流程

### Step 1：环境检查

**必须完整运行，任何一项失败都停止执行。**

```bash
echo "=== 意心会 Skill 安装器 ==="
echo ""

INSTALL_STEPS='请先执行以下三步：

  1. npm install -g @larksuite/cli
  2. lark-cli config init --new
  3. lark-cli auth login

完成后重新运行 /lang-yi-install'

# 1. 检查 lark-cli 是否安装
if ! command -v lark-cli &>/dev/null; then
  echo "ERROR: lark-cli 未安装。"
  echo ""
  echo "$INSTALL_STEPS"
  exit 1
fi
echo "[OK] lark-cli 已安装"

# 2. 检查是否已认证
AUTH_RESULT=$(lark-cli auth status 2>&1)
if ! echo "$AUTH_RESULT" | grep -q '"appId"'; then
  echo "ERROR: lark-cli 未认证。请运行："
  echo ""
  echo "  lark-cli auth login"
  exit 1
fi
echo "[OK] lark-cli 已认证"

# 3. 检查关键 scope
MISSING_SCOPES=""

CHECK1=$(lark-cli auth check --scope "drive:drive:readonly" 2>&1)
if echo "$CHECK1" | grep -q '"missing"' && echo "$CHECK1" | grep -q 'drive:drive:readonly'; then
  MISSING_SCOPES="$MISSING_SCOPES drive:drive:readonly"
fi

CHECK2=$(lark-cli auth check --scope "drive:file:download" 2>&1)
if echo "$CHECK2" | grep -q '"missing"' && echo "$CHECK2" | grep -q 'drive:file:download'; then
  MISSING_SCOPES="$MISSING_SCOPES drive:file:download"
fi

if [ -n "$MISSING_SCOPES" ]; then
  echo ""
  echo "ERROR: 缺少以下飞书权限 scope：$MISSING_SCOPES"
  echo ""
  echo "修复方法（二选一）："
  echo ""
  echo "  方法A：在飞书开放平台给应用添加 scope 后重新登录"
  echo "    1. 打开 https://open.feishu.cn → 找到你的应用 → 权限管理"
  echo "    2. 搜索并开通上述 scope"
  echo "    3. 运行：lark-cli auth login"
  echo ""
  echo "  方法B：让管理员把你加入飞书文件夹的协作者（有权限的人分享链接给你）"
  exit 1
fi
echo "[OK] scope 检查通过"

# 4. 测试 API 连通性（用一个轻量接口验证）
TEST_RESULT=$(lark-cli api GET /open-apis/authen/v1/user_info --as user 2>&1)
if ! echo "$TEST_RESULT" | grep -q '"code": 0'; then
  echo ""
  echo "ERROR: API 连通测试失败。可能是网络问题或 token 过期。"
  echo "请重新运行：lark-cli auth login"
  exit 1
fi
echo "[OK] API 连通正常"

echo ""
echo "环境检查全部通过，开始下载。"
```

### Step 2：递归下载文件夹内容

**直接运行以下 Python 脚本，不做任何修改。**

关键点：
- API 调用格式：`lark-cli api GET <path> --params '<json>' --as user`
- `--as user` 必须加，否则默认用 bot 身份（没有文件权限）

```bash
python3 << 'PYEOF'
import subprocess
import json
import os
import sys
import time

SKILLS_DIR = os.path.expanduser("~/.claude/skills")
TOOLS_DIR = os.path.expanduser("~/.claude/tools")
META_DIR = os.path.expanduser("~/.claude/skills/.yi-meta")

# 根目录文件（放到 .yi-meta/）
ROOT_META_FILES = {"README.md", "VERSION", "setup.md", "publish.sh"}


def lark_list_folder(folder_token):
    """调用飞书 API 列出文件夹内容（自动分页）"""
    all_files = []
    page_token = None

    while True:
        params = {"folder_token": folder_token, "page_size": "50"}
        if page_token:
            params["page_token"] = page_token

        # 正确格式：lark-cli api GET <path> --params '<json>' --as user
        cmd = [
            "lark-cli", "api", "GET",
            "/open-apis/drive/v1/files",
            "--params", json.dumps(params),
            "--as", "user"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0 or not result.stdout.strip():
            print(f"  ERROR: 列出文件夹失败 (token={folder_token})", file=sys.stderr)
            if result.stderr.strip():
                print(f"         {result.stderr.strip()[:200]}", file=sys.stderr)
            break

        try:
            resp = json.loads(result.stdout)
        except json.JSONDecodeError:
            print(f"  ERROR: JSON 解析失败: {result.stdout[:200]}", file=sys.stderr)
            break

        data = resp.get("data", {})
        files = data.get("files", [])
        all_files.extend(files)

        if data.get("has_more") and data.get("page_token"):
            page_token = data["page_token"]
        else:
            break

    return all_files


def lark_download(file_token, output_path):
    """用 lark-cli drive +download 下载单个文件"""
    output_dir = os.path.dirname(output_path)
    filename = os.path.basename(output_path)
    os.makedirs(output_dir, exist_ok=True)

    result = subprocess.run(
        ["lark-cli", "drive", "+download",
         "--file-token", file_token,
         "--output", filename,
         "--as", "user"],
        capture_output=True, text=True,
        cwd=output_dir
    )
    if result.returncode != 0:
        print(f"  WARN: 下载失败 {output_path}: {result.stderr.strip()[:200]}", file=sys.stderr)
        return False
    return True


def determine_target_dir(relative_path):
    """根据顶层目录决定本地映射路径"""
    parts = relative_path.strip("/").split("/")

    if len(parts) == 1 and parts[0] in ROOT_META_FILES:
        return os.path.join(META_DIR, parts[0])

    top_dir = parts[0] if len(parts) > 1 else ""

    if top_dir == "skills":
        return os.path.join(SKILLS_DIR, "/".join(parts[1:]))
    elif top_dir == "tools":
        return os.path.join(TOOLS_DIR, "/".join(parts[1:]))
    else:
        return os.path.join(META_DIR, relative_path)


def crawl_and_download(folder_token, relative_path=""):
    """递归遍历文件夹并下载所有文件"""
    files = lark_list_folder(folder_token)
    total = 0

    for f in files:
        name = f.get("name", "unknown")
        token = f.get("token", "")
        file_type = f.get("type", "")

        item_path = f"{relative_path}/{name}" if relative_path else name

        if file_type == "folder":
            print(f"  [DIR]  {item_path}/")
            total += crawl_and_download(token, item_path)
            time.sleep(0.3)  # 避免 API 限流
        else:
            target = determine_target_dir(item_path)
            display = target.replace(os.path.expanduser("~"), "~")
            print(f"  [FILE] {item_path} -> {display} ... ", end="", flush=True)
            if lark_download(token, target):
                print("OK")
                total += 1
            else:
                print("FAIL")

    return total


# --- Main ---
folder_token = os.environ.get("FOLDER_TOKEN", "B06yfyHVXl9SqWd4pk6cw29SnSc")

print(f"飞书源: {folder_token}")
print(f"Skills -> {SKILLS_DIR}")
print(f"Tools  -> {TOOLS_DIR}")
print(f"Meta   -> {META_DIR}")
print()

for d in [SKILLS_DIR, TOOLS_DIR, META_DIR]:
    os.makedirs(d, exist_ok=True)

print("正在扫描飞书文件夹并下载...")
print()
count = crawl_and_download(folder_token)

# 设置脚本可执行权限
export_sh = os.path.join(SKILLS_DIR, "yi-poster/scripts/export_poster.sh")
if os.path.exists(export_sh):
    os.chmod(export_sh, 0o755)

print()
print(f"=== 完成：共下载 {count} 个文件 ===")
PYEOF
```

### Step 3：验证安装

```bash
echo "=== 验证安装结果 ==="
echo ""

# 检查 skills 目录
echo "已安装的 Skills："
if [ -d ~/.claude/skills ]; then
  find ~/.claude/skills -name "SKILL.md" -maxdepth 3 -type f | sort | while read f; do
    skill_dir=$(dirname "$f")
    skill_name=$(basename "$skill_dir")
    # 只显示 yi 系列
    case "$skill_name" in yi|yi-*|yiskill-*)
      echo "  [OK] $skill_name"
    esac
  done
fi

# 检查 tools 目录
echo ""
echo "已安装的 Tools："
if [ -d ~/.claude/tools/feishu-sync ]; then
  echo "  [OK] feishu-sync"
else
  echo "  (无)"
fi

# 版本
echo ""
if [ -f ~/.claude/skills/.yi-meta/VERSION ]; then
  echo "版本：v$(cat ~/.claude/skills/.yi-meta/VERSION)"
fi

echo ""
echo "安装完成。新开会话即可使用 /yi 系列命令。"
```

---

## 目录映射规则

| 飞书文件夹中的路径 | 本地目标路径 |
|---|---|
| `skills/*` | `~/.claude/skills/*` |
| `tools/*` | `~/.claude/tools/*` |
| `README.md` / `VERSION` / `setup.md` / `publish.sh` | `~/.claude/skills/.yi-meta/` |
| 其他文件 | `~/.claude/skills/.yi-meta/` |

---

## 错误处理

| 错误场景 | 处理方式 |
|---|---|
| `lark-cli` 未安装 | 提示三步安装流程（install → config init → auth login），停止 |
| 未认证 | 提示 `lark-cli auth login`，停止 |
| 缺 scope | **Step 1 提前检测**，提示去飞书开放平台添加 scope，停止（不等到下载才报错） |
| API 不通 | 提示检查网络或重新 auth login，停止 |
| 单个文件下载失败 | 打印 FAIL，继续下载其他文件 |

---

## lark-cli API 调用格式备忘

**正确格式**（避免踩坑）：

```bash
# 列出文件夹内容
lark-cli api GET /open-apis/drive/v1/files \
  --params '{"folder_token":"<token>","page_size":"50"}' \
  --as user

# 下载文件
lark-cli drive +download \
  --file-token <token> \
  --output <filename> \
  --as user
```

**常见错误**：
- ❌ `lark-cli api --method GET --uri /open-apis/...` → 格式不对
- ❌ `lark-cli drive +list --folder-token ...` → `+list` 命令不存在
- ❌ 不加 `--as user` → 默认 bot 身份，没有文件访问权限
- ❌ `page_size` 传数字 50 → 必须传字符串 `"50"`

---

## 注意事项

- 已有同名文件会被覆盖（等同于"同步最新版"）
- 不会删除本地已有但飞书上不存在的文件（只做增量覆盖）
- 下载完成后建议新开会话，让新 skill 生效
