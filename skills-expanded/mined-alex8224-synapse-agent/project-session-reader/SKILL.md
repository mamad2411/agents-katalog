---
name: project-session-reader
description: "Read or search the sessions of a specified project (workspace directory) from its .synapse session database: list recent sessions, full-text message search, and read a session transcript by thread_id with pagination."
license: Apache-2.0
compatibility: Requires a synapse source checkout with uv and Python 3.12+, or synapse installed as an importable package.
allowed_tools: execute, read_file, write_file, search_files, find_files
---

# 读取 / 搜索指定项目的会话

当用户要求查看、搜索或读取**某个指定项目**（workspace 目录）的历史会话时使用本 Skill。
例如：“列出 `D:\work\foo` 最近有哪些会话”“搜一下 `F:\bar` 项目里聊过数据库迁移的会话”
“读一下 `C:\repo` 项目会话 `abc123def456` 的内容”。

## 触发场景

- 用户给出一个项目/工作区路径，要求列出、搜索或读取该项目的会话。
- 目标项目的会话数据在 `<project>/.synapse/` 下，**不是**当前工作区。
- 需要跨项目对比、排查某项目的历史对话。

## 数据文件

| 文件 | 作用 | 说明 |
| --- | --- | --- |
| `<project>/.synapse/sessions.sqlite` | 会话元数据（标题/模型/摘要/时间） | 列出、按标题/摘要/模型搜索的入口 |
| `<project>/.synapse/checkpoints.sqlite` | LangGraph 会话消息（事实来源） | 读取完整对话、重建全文索引 |
| `<project>/.synapse/search-index.sqlite` | 会话消息全文索引 | 首次全文搜索时惰性创建，可忽略 |

## 关键原则

1. **不要用内置的 `search_session` / `read_session` 工具**——它们绑定当前工作区自己的
   `.synapse/`，读不到别的项目。必须用 `execute` 运行 Python 脚本，把数据库路径显式指向
   `<project>/.synapse/`。
2. 先确认数据目录存在：`<project>/.synapse/sessions.sqlite`。缺失则向用户确认项目路径。
3. 读大会话必须分页：`read` 默认只返回最近 5 轮，用 `offset` / `limit` 或 `max_turns`
   控制范围；确需全量时显式加 `--all`。
4. 全文搜索会惰性同步索引（可能数秒），且默认只同步最近 50 个会话——结果可能是
   **不完整**的，必须把这一限制如实告诉用户；需要更大覆盖时加大 `--max-sync`。
5. 构造 `SessionStore` 可能对旧版 `sessions.sqlite` 做兼容性迁移（`ALTER TABLE` 补列）。
   这是幂等且安全的，但**会写目标项目数据**；如要求严格只读，先把数据库文件复制到
   临时目录再操作。

## 准备：一次性脚本

把下面的脚本写到临时文件 `/.tmp/project_session_reader.py`（用 `write_file`），
然后用 `uv run --no-sync python /.tmp/project_session_reader.py ...` 执行。
若 `import synapse` 失败，在脚本顶部加 `sys.path.insert(0, "<synapse-checkout>/src")`。

```python
"""读取/搜索指定项目 (workspace) 的会话。

用法:
  python project_session_reader.py list   <project> [limit]
  python project_session_reader.py search <project> <query> [limit] [--fulltext] [--max-sync=N]
  python project_session_reader.py read   <project> <thread_id> [max_turns] [offset] [limit] [--all] [--include-tools]
"""
import sys
from pathlib import Path

MAX_CHARS_PER_TURN = 8000
DEFAULT_MAX_TURNS = 5
DEFAULT_MAX_SYNC = 50


def data_dir(project: str) -> Path:
    return (Path(project).expanduser().resolve() / ".synapse")


def split_args(args: list[str]) -> tuple[list[str], set[str]]:
    """把位置参数与 --flag 分开（--max-sync=N 属于 flag）。"""
    pos: list[str] = []
    flags: set[str] = set()
    for a in args:
        if a.startswith("--"):
            flags.add(a)
        else:
            pos.append(a)
    return pos, flags


def max_sync_from_flags(flags: set[str]) -> int:
    for f in flags:
        if f.startswith("--max-sync="):
            try:
                return max(0, int(f.split("=", 1)[1]))
            except ValueError:
                return DEFAULT_MAX_SYNC
    return DEFAULT_MAX_SYNC


def _compact(value, limit: int = 400) -> str:
    import json
    if value is None:
        return ""
    try:
        s = json.dumps(value, ensure_ascii=False, default=str)
    except Exception:  # noqa: BLE001
        s = str(value)
    return s[:limit]


def render_turns(
    turns: list,
    *,
    include_tools: bool,
    max_turns: int,
    offset: int,
    limit: int,
) -> str:
    from synapse.sessions.transcript import message_to_export_dict

    target = turns[-max_turns:] if max_turns > 0 else turns
    total = len(turns)
    start = max(0, offset)
    end = start + limit if limit > 0 else None
    window = target[start:end]
    base = total - len(target)
    first_global = base + start + 1
    last_global = base + start + len(window)

    if not window:
        return "(无对话内容)"

    lines: list[str] = []
    if 0 < len(window) < total:
        lines.append(f"[共 {total} 轮，显示第 {first_global}-{last_global} 轮]\n")
    for i, turn in enumerate(window):
        lines.append(f"--- 第 {first_global + i} 轮 ---")
        for msg in turn:
            d = message_to_export_dict(msg)
            role = str(d.get("role") or "unknown").upper()
            content = (d.get("content") or "").strip()
            if include_tools:
                tcs = None
                if isinstance(msg, dict):
                    tcs = msg.get("tool_calls")
                else:
                    tcs = getattr(msg, "tool_calls", None)
                for c in (tcs or []):
                    name = c.get("name") if isinstance(c, dict) else getattr(c, "name", None)
                    cid = c.get("id") if isinstance(c, dict) else getattr(c, "id", None)
                    args = c.get("args") if isinstance(c, dict) else getattr(c, "args", None)
                    line = f"[TOOL_CALL] {name or '-'}"
                    if cid:
                        line += f" (id={cid})"
                    if args:
                        line += f"\n    args: {_compact(args)}"
                    lines.append(line)
            if content:
                if len(content) > MAX_CHARS_PER_TURN:
                    content = content[:MAX_CHARS_PER_TURN] + "\n...[截断]..."
                lines.append(f"[{role}] {content}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    pos, flags = split_args(sys.argv[1:])
    if len(pos) < 2:
        print(__doc__)
        sys.exit(2)
    mode, project = pos[0], pos[1]
    d = data_dir(project)
    sessions_path = d / "sessions.sqlite"
    checkpoint_path = d / "checkpoints.sqlite"
    if not sessions_path.is_file():
        print(f"未找到会话库: {sessions_path}")
        sys.exit(1)

    from synapse.sessions.store import SessionStore, format_session_table

    with SessionStore(sessions_path) as store:
        if mode == "list":
            limit = int(pos[2]) if len(pos) > 2 else 50
            items = store.list_nonempty(limit=limit)
            print(format_session_table(items, include_summary=True) or "(no sessions)")
            return

        if mode == "search":
            if len(pos) < 3:
                print("用法: search <project> <query> [limit] [--fulltext] [--max-sync=N]")
                sys.exit(2)
            query = pos[2]
            limit = int(pos[3]) if len(pos) > 3 else 50
            fulltext = "--fulltext" in flags
            meta = store.search(query, limit=limit)
            print("== 元数据命中 (标题/摘要/模型/thread_id) ==")
            print(format_session_table(meta, include_summary=True) or "(无元数据命中)")

            if fulltext:
                if not checkpoint_path.is_file():
                    print(f"\n(未找到 {checkpoint_path}，跳过全文搜索)")
                    return
                from synapse.sessions.search_index import (
                    SessionSearchIndex,
                    default_search_index_path,
                )
                index = SessionSearchIndex(
                    default_search_index_path(sessions_path),
                    store=store,
                    checkpoint_path=checkpoint_path,
                )
                try:
                    max_sync = max_sync_from_flags(flags)
                    recent = store.list_nonempty(limit=limit + 200)
                    synced = index.sync([s.thread_id for s in recent], max_sync=max_sync)
                    hits = index.search(query, limit=200, roles=("human", "ai"))
                    print(f"\n== 消息全文命中 (本次同步 {synced} 个会话的索引) ==")
                    printed: set[str] = set()
                    for h in hits:
                        tid = str(h["thread_id"])
                        if tid not in printed:
                            printed.add(tid)
                            info = store.get(tid)
                            title = (info.title if info else tid)[:80]
                            print(f"● {title}  [{tid}]")
                        snippet = str(h.get("content") or "").replace("\n", " ")[:120]
                        print(f"    - [{h.get('role')}] {snippet}")
                    if not hits:
                        print("(无消息命中；若会话数很多，可能是索引未覆盖，"
                              "加大 --max-sync 后重试)")
                finally:
                    index.close()
            return

        if mode == "read":
            if len(pos) < 3:
                print("用法: read <project> <thread_id> [max_turns] [offset] [limit] "
                      "[--all] [--include-tools]")
                sys.exit(2)
            thread_id = pos[2]
            try:
                max_turns = int(pos[3]) if len(pos) > 3 else DEFAULT_MAX_TURNS
                offset = int(pos[4]) if len(pos) > 4 else 0
                limit = int(pos[5]) if len(pos) > 5 else 0
            except ValueError:
                print("错误: max_turns/offset/limit 必须是整数")
                sys.exit(2)
            if "--all" in flags:
                max_turns = 0
            include_tools = "--include-tools" in flags

            info = store.get(thread_id)
            if info is None:
                print(f"会话未找到: {thread_id}（用 list 或 search 获取正确 thread_id）")
                sys.exit(1)

            from synapse.sessions.transcript import (
                load_messages_from_sqlite_file,
                split_messages_by_turns,
            )

            messages = load_messages_from_sqlite_file(checkpoint_path, thread_id)
            if not messages:
                print(f"会话 {thread_id} 没有对话记录（标题: {info.title}）")
                return

            if not include_tools:
                messages = [
                    m
                    for m in messages
                    if (m.get("type") if isinstance(m, dict) else getattr(m, "type", None)) != "tool"
                ]

            turns = split_messages_by_turns(messages)
            body = render_turns(
                turns,
                include_tools=include_tools,
                max_turns=max_turns,
                offset=offset,
                limit=limit,
            )
            print(f"会话: {info.thread_id}")
            print(f"标题: {info.title}")
            print(f"模型: {info.binding().display()}")
            print(f"轮次: {len(turns)}")
            print(f"创建: {info.created_at}  更新: {info.updated_at}")
            print("─" * 40)
            print(body)
            return

        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
```

## 使用方式

### 1. 列出最近会话

```powershell
uv run --no-sync python /.tmp/project_session_reader.py list "F:\work\foo" 20
```

### 2. 搜索会话

按标题/摘要/模型搜索（不建索引，快）：

```powershell
uv run --no-sync python /.tmp/project_session_reader.py search "F:\work\foo" "数据库迁移" 20
```

需要命中**消息正文**时加 `--fulltext`（首次会惰性同步索引，可能数秒；默认只同步最近
50 个会话，会话很多时用 `--max-sync=500` 扩大覆盖）：

```powershell
uv run --no-sync python /.tmp/project_session_reader.py search "F:\work\foo" "数据库迁移" 20 --fulltext
uv run --no-sync python /.tmp/project_session_reader.py search "F:\work\foo" "数据库迁移" 20 --fulltext --max-sync=500
```

### 3. 读取指定会话

先从上一步拿到 `thread_id`，再读取；默认返回最近 5 轮，大会话分页：

```powershell
# 最近 5 轮（默认）
uv run --no-sync python /.tmp/project_session_reader.py read "F:\work\foo" <thread_id>
# 最近 20 轮
uv run --no-sync python /.tmp/project_session_reader.py read "F:\work\foo" <thread_id> 20
# 跳过前 10 轮，再读 5 轮
uv run --no-sync python /.tmp/project_session_reader.py read "F:\work\foo" <thread_id> 0 10 5
# 完整内容（含工具调用与返回，需用户明确要求）
uv run --no-sync python /.tmp/project_session_reader.py read "F:\work\foo" <thread_id> --all --include-tools
```

## 注意事项

- `<project>` 用**绝对路径**最稳；路径含空格时用引号包住。
- `sessions.sqlite` 只存元数据；消息正文永远从 `checkpoints.sqlite` 读取，不要手写 SQL 拼消息。
- 全文索引表 `search-index.sqlite` 是可重建的派生缓存，缺失或过期无需修复，重新 `--fulltext` 即可。
- 不要把任何密钥、`.env` 内容写入脚本或输出；会话里可能含敏感信息，摘要给用户时先脱敏。
- 默认只读最近 5 轮是刻意的安全上限；不要在没有用户明确要求时用 `--all` 全量 dump 会话。
