---
name: mobai-reverse
description: MobAI Pro 会员系统逆向工程全流程。适用于 Go 64-bit PE 分析、license/quota 系统 patch、NSIS→7z SFX 重打包、以及 Go 二进制 embed.FS 前端提取。需要 IDA Pro MCP 连接。
---

# MobAI Pro 逆向工程 — 完整方法论

## 概述

目标：MobAI Pro (Android 设备自动化工具) — 绕过 Pro 会员验证，解锁无限设备、无限 token、离线模式。

**二进制**: `MobAI_payload.exe` (145 MB, Go 1.22+ 64-bit, NSIS v3.11 Unicode 安装器内嵌)

**补丁数**: 7 (v2.0) | **方法**: 根源数据覆写 + 服务器同步阻断

---

## 阶段 0: 侦察与解包

### 0.1 识别安装器类型

```bash
# 检查 EXE 签名
file MobAI.exe
# "Nullsoft Installer self-extracting archive (NSIS)"

# 提取 NSIS 载荷
7z x MobAI.exe -onsis-extract
# 产出:
#   MobAI_payload.exe  ← 真正的 Go 二进制 (145 MB)
#   $PLUGINSDIR/System.dll, nsDialogs.dll
#   $PLUGINSDIR/webview2bootstrapper/MicrosoftEdgeWebview2Setup.exe
```

### 0.2 识别二进制类型

```bash
file MobAI_payload.exe
# "PE32+ executable (console) x86-64 Go BuildID=..."

# 用 IDA 加载 → 17 个段，带 Go PCLNTAB 符号表
# .symtab 段: 函数名、包路径完整保留 (15 MB 符号表)
```

### 0.3 提取嵌入资源 (Go embed.FS)

Go 的 `embed.FS` 数据存储在 `.rdata`/`.data` 段中。使用 IDA MCP 搜索特征路径：

```python
# IDA Python: 搜索 "frontend/dist/"
results = ida_search.find_text("frontend/dist/", ...)
# 定位到 embedded.resources.Init() 中 embed.FS 引用

# 前端文件路径模式: frontend/dist/assets/index.xxxxxxxx.js
# 从 .rdata/.data 段提取: index.html, index.js (499KB), index.css (63KB)
```

**提取的文件**:
| 文件 | 大小 | 技术栈 |
|------|------|--------|
| `index.html` | 371 B | WebView2 入口 |
| `index.js` | 499,662 B | React 18 + TypeScript + Webpack 5 + Zustand |
| `index.css` | 63,833 B | Tailwind CSS + Nunito font |
| `scripts.js` | 100,000 B | 辅助逻辑 |
| `auth-success.html` | 485 B | Supabase OAuth 回调 |

---

## 阶段 1: Go 符号恢复与函数定位

### 1.1 利用 PCLNTAB 符号表

Go 编译器在 `.symtab` 段生成完整符号表。IDA 自动解析为函数名 `package.(*Type).Method`。

**关键命名空间**:
```
mobai_internal_license.(*Manager).*   ← 许可证核心
mobai_internal_quota.(*Manager).*     ← 配额/限额
mobai_internal_supabase.(*Client).*   ← 后端认证
mobai_internal_device/android/*       ← ADB 集成
mobai_internal_embedded.*             ← 内嵌资源
main.(*App).*                         ← 应用入口 + Go↔JS 桥接
```

### 1.2 定位关键 License 函数

```python
# IDA MCP: 列出 license 包函数
ida_func_query(filter="mobai_internal_license.*")
```

**核心函数表**:

| 函数 | 地址 (VA) | 说明 |
|------|-----------|------|
| `NewManager` | 0x140F311C0 | 初始化 license Manager |
| `GetTier` | 0x140F31500 | 读取 tier 字符串 |
| `IsPro` | 0x140F31620 | 判断是否 Pro |
| `HasUnlimitedTokens` | 0x140F31680 | 无限 token? |
| `HasUnlimitedDevices` | 0x140F316C0 | 无限设备? |
| `HasOfflineMode` | 0x140F31720 | 离线模式? |
| `CanMakeRequest` | 0x140F31780 | 允许发请求? |
| `CanConnectDevice` | 0x140F31A00 | 允许连设备? |
| `GetStatus` | 0x140F35020 | 向前端报告状态 |
| `SyncLicense` | 0x140F32000 | 从服务器同步 |
| `RefreshTier` | 0x140F33080 | 刷新 tier |
| `StartTierSync` | 0x140F33EC0 | 启动定时同步 |

---

## 阶段 2: License 系统架构分析

### 2.1 数据结构还原

从 `NewManager` 和 `GetTier`/`GetLimit` 反推出内存布局：

```c
// license.Manager (大小 0x60+)
// VA 参考: NewManager = 0x140F311C0
struct LicenseManager {
    void*   supabaseClient;   // +0x00: Supabase 客户端
    void*   quotaManager;     // +0x08: quota.Manager 指针
    string  tier;             // +0x10: tier 字符串 (ptr)
    int64   tierLen;          // +0x18: tier 长度
    void*   rwMutex;          // +0x20: 读写锁
    // +0x28: EventEmitter
    // +0x38: context/其他
};

// quota.Manager (大小 0x88+)
// VA 参考: NewManager = 0x140F2DEE0
struct QuotaManager {
    void*   supabaseClient;   // +0x00
    void*   eventEmitter;     // +0x08
    void*   storage;          // +0x10
    // ...
    string  tier;             // +0x38: tier 字符串 (ptr)
    int64   tierCode;         // +0x40: tier 代码 (4)
    int64   tokensRemaining;  // +0x48: 剩余 token 数 (初始 100)
    int64   limit;            // +0x50: 每日限额 (100 = free, -1 = pro)
    // +0x58: 离线票
    void*   offlineTicket;    // +0x68: 离线 ticket
};
```

### 2.2 验证逻辑链路

```
App 启动
  └─ license.NewManager()
       ├─ tier = "free", len = 4                              [地址: 0x140F3137D, 0x140F3138C]
       └─ quota.NewManager()
            ├─ tier = "free", code = 4                        [地址: 0x140F2DFEC, 0x140F2DFFB]
            ├─ tokensRemaining = 100                           [地址: 0x140F2DFFF]
            └─ limit = 100                                    [地址: 0x140F2E007]  ← ROOT CAUSE

  用户登录 → handleInitResult()
        ├─ 成功路径: 不调用 setTier (tier 保持 "free")
        ├─ 失败路径: setTier("free", 4)  [地址: 0x140F328A0, 0x140F329C0]
        └─ setTier() → quota.SetTier()
             └─ 只更新 +0x38, +0x40, 不更新 +0x50!  ← 设计缺陷

  服务器同步 → StartTierSync() 定时调用 RefreshTier()
        └─ RefreshTier() → SyncLicense() → 从 Supabase 获取真实 tier
             └─ 如果是 free 用户 → setTier("free", 4) → 覆盖!
```

### 2.3 IsPro / HasUnlimitedTokens 判断逻辑

```c
// IsPro @ 0x140F31620 — 反编译
bool IsPro(Manager* m) {
    Tier t = GetTier(m);   // 从 +0x10 读 tier 字符串
    return t.len == 3
        && *(uint16*)t.ptr == 0x7270  // "pr" (LE)
        && *(uint8*)(t.ptr+2) == 0x6F; // "o"
}

// HasUnlimitedTokens @ 0x140F31680 — 反编译
bool HasUnlimitedTokens(Manager* m) {
    return GetLimit(m->quotaManager) < 0;  // limit == -1 → true
}

// CanMakeRequest @ 0x140F31780 — 反编译
bool CanMakeRequest(Manager* m) {
    if (GetLimit(m->quotaManager) >= 0)    // limit >= 0 → 受限
        return CanUseToken(...);           // 检查并消耗 token
    return true;                           // limit < 0 → 无限制
}

// CanUseToken @ 0x140F2E3E0 — 反编译 (直接读字段!)
bool CanUseToken(QuotaManager* q) {
    if (q->limit >= 0)          // +0x50 字段
        return q->tokensRemaining > 0;  // +0x48 字段, 每次 -1
    return true;               // limit < 0 → 无限
}
```

---

## 阶段 3: 补丁策略演进

### 3.1 v1.0 失败原因

**策略**: 逐个修补布尔检查函数 (IsPro, HasUnlimitedTokens, HasOfflineMode...)

**失败根因**:
1. **地址错误**: RefreshTier (0xF3208A) 和 StartTierSync (0xF32ECF) 偏移了 ~0xFF6 字节
2. **只改判断不改数据**: IsPro 返回 true，但 GetTier() 仍返回 "free"，前端直接展示 tier 字符串
3. **字段直接访问**: `CanUseToken` 读 `+0x50` 字段 (100)，不调用 `GetLimit()`

### 3.2 v2.0 根源修正

**策略**: 直接修改数据源 + 阻止服务器覆盖

| # | 补丁 | 虚拟地址 | 原始字节 | 补丁字节 | 作用 |
|---|------|---------|---------|---------|------|
| 1 | GetLimit 返回路径 1 | 0x140F2FC85 | `48 8B 44 24 10` | `6A FF 58 90 90` | `push -1; pop rax` (5B) |
| 2 | GetLimit 返回路径 2 | 0x140F2FC95 | `48 8B 44 24 10` | `6A FF 58 90 90` | panic 恢复路径 |
| 3 | license.NewManager len | 0x140F3137D | `48 C7 40 18 04...` | `48 C7 40 18 03...` | tier 长度 4→3 |
| 4 | "free" 字符串覆写 | 0x1418D15B8 | `66 72 65 65` | `70 72 6F 00` | "free"→"pro\0" |
| 5 | quota.NewManager limit | 0x140F2E007 | `48 C7 40 50 64...` | `48 C7 40 50 FF...` | limit 100→-1 |
| 6 | RefreshTier 禁用 | 0x140F33080 | `49 3B 66 10...` | `31 C0 31 DB C3...` | 立即返回 |
| 7 | StartTierSync 禁用 | 0x140F33EC0 | `4C 8D 64 24 F8...` | `C3 90 90 90...` | 立即返回 |

### 3.3 补丁 1-2: GetLimit 编码技巧

原始指令 5 字节 `mov rax, [rsp+0x10]`。需要替换为 `rax = -1`。

`mov rax, -1` = `48 C7 C0 FF FF FF FF` (7B) → 超长!

**解决方案**: `push -1; pop rax` = `6A FF 58` (3B) + `NOP × 2` = 5B ✓

```
6A FF    push -1      ; -1 压栈 (sign-extended imm8)
58       pop rax       ; rax = 0xFFFFFFFFFFFFFFFF
90 90    nop; nop      ; 填充
```

### 3.4 补丁 6: RefreshTier 禁用验证

```
31 C0    xor eax, eax     ; rax = 0 (nil error → "成功"但无操作)
31 DB    xor ebx, ebx     ; rbx = 0 (nil 返回值)
C3       ret              ; 立即返回 — 不调用服务器!
90×4     nop              ; 填充
```

**关键**: Go 函数返回 `(result, error)` 在 `rax, rbx` 中。`xor eax,eax; xor ebx,ebx; ret` 等价于 `return nil, nil` ——调用方认为刷新成功但无数据返回，不会覆盖本地 tier。

---

## 阶段 4: 重打包安装器

### 4.1 NSIS → 7z SFX

NSIS 安装器无法直接修改后重新打包（需要 NSIS 编译器），使用 7z SFX 替代：

```bash
# 1. 用打补丁的 MobAI_payload.exe 替换原始文件
cp MobAI_payload.exe nsis-extract/MobAI.exe

# 2. 创建 7z 归档
7z a -t7z mobai-patched.7z ./pkg/* -mx=5

# 3. 拼接 SFX 安装器
cat 7z.sfx config.txt mobai-patched.7z > MobAI-Pro-Patched-v2.exe
```

### 4.2 SFX 配置文件 (config.txt)

```ini
;!@Install@!UTF-8!
Title="MobAI Installer (Pro Patched)"
BeginPrompt="This will install MobAI with Pro membership unlocked..."
Progress="yes"
RunProgram="MobAI.exe"
AutoInstall="yes"
Directory="MobAI"
;!@InstallEnd@!
```

### 4.3 PE 节表 → 文件偏移映射

补丁脚本需要正确处理 VA→文件偏移。PE 布局 (17 个段):

```
.text:   RVA 0x1000  → file 0x600    (120 MB)
.rdata:  RVA 0x1271000 → file 0x1270600 (100 MB)
.data:   RVA 0x76A7000 → file 0x76A6000 (8 MB)
```

**动态解析** 远比硬编码偏移可靠——`patcher.py` v2.0 实现了完整的 PE 解析器。

---

## 阶段 5: Go↔JS 桥接分析

### 5.1 通信协议

WebView2 通过 `window.chrome.webview.hostObjects.mobai` 暴露 Go 方法：

```javascript
// JS → Go (同步/异步调用)
await mobai.getLicense();       // → main.(*App).GetLicenseStatus → license.GetStatus
await mobai.connectDevice(sn);  // → main.(*App).ConnectDevice
await mobai.runTask(taskJSON);  // → 自动化执行
await mobai.upgradePro();       // → CreateCheckout

// Go → JS (事件推送)
window.chrome.webview.addEventListener('message', (e) => {
    const { type, payload } = JSON.parse(e.data);
    // license:updated, bridge:started, agent:progress
});
```

### 5.2 GetStatus 返回值追踪

```
main.GetLicenseStatus (+0x1411C60E0)
  └─ license.GetStatus (+0x140F35020)
       ├─ GetTier() → {ptr, len}         → result._r0, result._r1
       ├─ IsAuthenticated()               → result._r2
       ├─ GetUserEmail() → {ptr, len}    → result._r3, result._r4
       ├─ if GetLimit() >= 0: tokens     → result._r5, result._r6
       └─ GetOfflineTicketExpiry()        → result._r7
```

前端直接使用 `tier` 字符串显示 "Free"/"Pro" 标签。因此必须修改字符串本身而非仅 IsPro 返回值。

---

## 工具链

| 工具 | 用途 |
|------|------|
| IDA Pro 8.x + MCP 插件 | 反编译、反汇编、数据流追踪 |
| 7-Zip 23+ | NSIS 解包、7z SFX 打包 |
| Ghidra (备选) | Go PCLNTAB 符号恢复 |
| Python 3.11 | 补丁脚本、PE 解析 |
| Git + Git LFS | 二进制文件版本管理 |

## 关键教训

1. **Go 二进制逆向**: PCLNTAB 符号表是最大优势——函数名、包名、类型名全部可恢复
2. **根源修正 > 表面修补**: 修改初始化数据 (字符串、limit) 比修补每个判断函数更可靠
3. **直接字段访问陷阱**: Go 编译器可能内联字段访问，导致 `CanUseToken` 直接读 `+0x50` 而非调用 `GetLimit()`
4. **字符串长度匹配**: `"pro"` (3B) vs `"free"` (4B)，需要同时修改长度字段
5. **VA→文件偏移**: 不同二进制版本的段布局不同，动态 PE 解析是必须的
6. **服务器同步阻断**: `RefreshTier`/`StartTierSync` 必须禁用，否则服务器会覆盖本地修改
7. **5 字节约束**: x86-64 短指令编码技巧 (`push imm8; pop reg` = 3B) 在空间受限时非常有用
