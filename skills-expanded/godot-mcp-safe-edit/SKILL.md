---
name: godot-mcp-safe-edit
description: "安全编辑 edit_script search_and_replace validate_scripts 确认令牌 remove_node headless 改盘 editor 覆盖 沙箱 防误用 CRLF tab 缩进 —— 当你编辑 .gd/.tscn、删节点或执行危险操作时使用"
---

## 安全编辑流

编辑 `.gd`/`.tscn`、删节点、运行危险操作时的防护 checklist。工具细节见 `godot-mcp-core.md` 与 `godot-mcp-editor.md`。

**何时用**：编辑 `.gd`/`.tscn`、删节点、执行危险操作时。

**checklist**：
- [ ] 1. `edit_script` **优先 search_and_replace**（内容匹配、行号偏移鲁棒、CRLF 安全、免确认 token）；**禁用内置 Edit 工具改 .gd**（tab 缩进匹配率极低）
- [ ] 2. 改 `.gd` 后必跑 `validate_scripts`（验证语法）
- [ ] 3. headless 改盘 + editor 开同场景 → Ctrl+S 覆盖风险：建议 editor 内 Reload 场景或关闭该场景后再操作
- [ ] 4. 危险操作（`remove_node` 等）需显式确认令牌
- [ ] 5. GDScript 沙箱是**防误用层非防对抗**（间接构造可绕过；真正隔离须容器/VM + `GODOT_MCP_ALLOW_UNSAFE=false`）
- [ ] 6. `write_script`/`edit_script` 写 .gd 前也走沙箱扫描（与 `execute_gdscript` 同威胁面，发现已知危险 API 模式（含 @tool 加载即执行等，清单不列举防被侦察）阻断 SANDBOX_VIOLATION；双 opt-in 旁路 `UNRESTRICTED + DISABLE_SAFETY`）

**常见偏离**：
- 用内置 Edit 工具改 `.gd`（tab 缩进失败）
- 改完不 validate
- headless 改盘后被 editor 旧版本 Ctrl+S 覆盖（MCP 不可控，须 Reload）
