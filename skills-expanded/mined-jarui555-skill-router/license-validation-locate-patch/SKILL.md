---
name: license-validation-locate-patch
description: 在二进制里快速找到"那个 if" —— 决定授权通过与否的分支。含字符串锚点、API 锚点、调用栈回溯、返回值特征、多版本 AOB 迁移。
---

# 定位校验点并打补丁

目标：找到 `if (valid)` 这个分支，把它变成永远为真。

难点不在 patch（一个字节的事），在**找对地方**。找错地方的表现是：改了没反应，或者改了能启动但功能崩。

---

## 一、五种定位法，按命中率排序

### 1. 字符串锚点（最快，60% 的情况够用）

搜这些词：

```
Invalid license / License expired / Trial expired / Unregistered
Please activate / Activation required / Thank you for purchasing
未授权 / 试用已过期 / 请激活 / 授权失败 / 剩余天数
```

**技巧**：

- 多语言软件要搜所有语言的字符串
- 字符串被加密时搜不到 → 用 x64dbg 在 `MessageBoxA/W` 下断，看调用栈
- 搜到字符串后**不要直接改字符串**，要往上找引用它的判断

```bash
# IDA / radare2 里找交叉引用
r2 -A target.exe -q -c 'izz~Invalid license' -c 'axt @ <addr>'
```

### 2. API 锚点（定位"校验动作"发生的地方）

按机制选 API：

| 机制 | API |
| :--- | :--- |
| 时间校验 | `GetSystemTime` / `GetLocalTime` / `time` / `clock_gettime` |
| 注册表读取 | `RegOpenKeyEx` / `RegQueryValueEx` |
| 文件读取 | `CreateFileW` / `ReadFile`（读 license.dat 时） |
| 签名验证 | `CryptVerifySignature` / `BCryptVerifySignature` / `EVP_DigestVerify*` |
| 网络请求 | `WinHttpSendRequest` / `InternetReadFile` / `curl_easy_perform` |
| 硬件信息 | `GetVolumeInformation` / `GetAdaptersInfo` / `cpuid` |
| 加密狗 | `DongleCheck` / 厂商 SDK 导出函数 |

**在这些 API 上下断，回溯调用栈**，比盲搜字符串准得多。

### 3. 调用栈回溯（最准，但需要能跑起来）

```
1. 让程序走到"授权失败"的弹窗
2. 断在 MessageBoxA
3. 看 backtrace，往上 3-5 层
4. 那个 `test al, al` / `cmp eax, 0` 就是判定点
```

**注意**：Release 版本常常内联，backtrace 可能只有 2-3 层。这时看寄存器：`eax` / `al` 里通常就是判定结果。

### 4. 返回值特征（找"布尔判定"）

授权函数几乎都是 `bool check_license()`。编译后长这样：

```asm
call check_license
test al, al          ; 或 test eax, eax
jz   loc_fail        ; 或 je / jne
```

**搜这种模式**：`call` 后紧跟 `test al,al` + 条件跳转。

IDA 里可以用 IDAPython 批量找：

```python
import idautils, idc, ida_bytes

for ea in idautils.Heads():
    # 找 test al, al (F6 C0 00 / 84 C0)
    if ida_bytes.get_bytes(ea, 2) == b"\x84\xc0":
        nxt = idc.next_head(ea)
        mnem = idc.print_insn_mnem(nxt)
        if mnem in ("jz", "je", "jnz", "jne"):
            prev = idc.prev_head(ea)
            if idc.print_insn_mnem(prev) == "call":
                print(f"{hex(ea)}: call → test al,al → {idc.print_insn_mnem(nxt)}")
```

命中可能很多，但结合"这个 call 附近有 license 相关字符串"能快速收敛。

### 5. 多版本 AOB 特征码（有补丁表时）

见下面第四节。

---

## 二、单一判定 vs 多处判定

**这是最容易翻车的地方。**

改完能启动 ≠ 成功。有些软件有三套独立判定：

```
启动时：判一次 → 不通过就退出
打开项目时：判一次 → 不通过就只读
导出时：判一次 → 不通过就加水印
```

**验证方法**：patch 完之后，把所有重功能跑一遍：

```
[ ] 启动
[ ] 新建
[ ] 打开已有文件
[ ] 保存 / 另存为
[ ] 导出（PDF/图片/视频，各种格式）
[ ] 批量处理
[ ] 打印
[ ] 挂机 2 小时后再操作
```

**挂机测试很关键**：有些软件在运行 N 分钟后重新校验一次（心跳）。

**怎么快速找全所有判定点**：搜同一个字符串的所有交叉引用，或者 hook 那个校验函数看被调用几次、从哪调用。

```javascript
// Frida：统计校验函数调用次数和来源
var addr = Module.findBaseAddress("target.exe").add(0x12345);
Interceptor.attach(addr, {
    onEnter: function () {
        console.log("check_license called from:\n" + Thread.backtrace(this.context, Backtracer.ACCURATE)
            .map(DebugSymbol.fromAddress).join("\n"));
    },
    onLeave: function (retval) {
        console.log("  → returns " + retval);
        retval.replace(ptr(1));   // 直接改返回值，不用 patch 文件
    }
});
```

**先用 Frida 改返回值验证，确认逻辑通了再 patch 二进制。** 省得反复改文件。

---

## 三、补丁的四种写法

### 1. 改返回值

```asm
; 原
call check_license
test al, al
jz   fail

; 改 1：让 call 后强制 al=1
mov  al, 1        ; B0 01
nop
nop

; 改 2：改跳转
jmp  ok            ; EB xx
```

**字节**：`B0 01` 是 `mov al, 1`，配 `90 90` 填充。

### 2. 改条件跳转

```asm
jz  fail    ; 74 xx
→
jmp fail    ; EB xx  （跳过成功路径，反向操作）
; 或
nop nop     ; 90 90  （两个分支都走成功路径）
```

**注意**：`jz` → `jnz` 是 `74` → `75`，改一个字节。这是最省事的 patch，但要注意后续逻辑是否依赖标志位。

### 3. 改比较常量

```asm
cmp eax, 0
jne fail
→
cmp eax, eax    ; 39 C0，永远相等
```

适合"返回值是错误码"的情况（0 = 成功）。

### 4. Hook（不改文件）

适合：
- 文件有完整性校验
- 需要动态开关
- 只是验证思路

```javascript
// Frida
Interceptor.attach(Module.findExportByName(null, "CryptVerifySignatureW"), {
    onLeave: function (retval) { retval.replace(ptr(1)); }
});
```

---

## 四、多版本 AOB 迁移

有了一套能用的特征码补丁表，软件升级后失效 —— 这是常态。

### 为什么会失效

- 编译优化变了，指令重排
- 加了新功能，偏移全变
- 编译器版本升级，指令选择变了（`cmp` 变 `test`）

### 迁移方法：三段锚定

```
[前一个函数的尾部] + [目标函数序言] + [目标指令特征]
```

**只用函数序言会双命中**（很多函数序言一样：`55 8B EC 83 EC ??`）。所以要加左侧锚点。

```python
# 特征码生成：取目标指令前后各 N 字节，中间用通配符
# 示例：55 8B EC ?? ?? 83 7D 08 00 74 ?? B8 01 00 00 00
#       ^^^^^^^ 序言      ^^^^^^^ 比较    ^^^^ 跳转  ^^^^^^^^^ 返回值
```

**通配符原则**：只把**会变的字节**（偏移、立即数、跳转距离）设成 `??`，其余保留。

### 跨版本验证

```
[ ] 在版本 N 上命中（基线）
[ ] 在版本 N+1 上命中
[ ] 在版本 N+2 上命中
[ ] 在版本 N-1 上命中（向后兼容）
[ ] 每个版本命中次数 = 1（唯一性）
```

**命中次数 > 1 就不可靠**，必须加长特征码或换锚点。

---

## 五、完整性校验

patch 完启动就崩，八成是完整性校验。

### 常见形式

| 形式 | 特征 | 绕过 |
| :--- | :--- | :--- |
| 文件哈希 | 启动时算自身哈希，比对内嵌值 | 找到哈希比较点，改内嵌值或 patch 比较 |
| 代码段 CRC | 只校验 `.text` | patch 后重算 CRC 写回 |
| 数字签名 | Authenticode | 去掉签名（会留痕）或 patch 验签 |
| 分段校验 | 多处分散校验 | 全部找到，逐个 patch |
| 反调试触发 | 检测到调试器就崩 | 先过反调试 |

**判断方法**：patch 一个字节，如果启动崩溃/闪退 → 有完整性校验。如果正常运行但功能没变 → patch 点不对。

### 快速定位

在 `CreateFileW` 打开自身路径时下断，看读完文件后谁在算哈希（`CryptHashData` / `BCryptHashData` / 自实现循环）。

---

## 六、检查清单

```
[ ] 找到判定点了吗：        是(地址___)
[ ] 是唯一判定点吗：        是 / 否(共___处)
[ ] 有完整性校验吗：        有 / 无 / 未测
[ ] 有反调试吗：            有 / 无
[ ] Frida 验证通过了吗：    是 / 否
[ ] 二进制 patch 后启动：   正常 / 崩溃 / 功能异常
[ ] 全功能跑过了吗：        是 / 否
[ ] 挂机 2 小时后正常吗：   是 / 否
[ ] 重启后正常吗：          是 / 否
```

**"重启后正常吗"必测**：有些软件把授权状态写到临时文件，patch 后第一次能跑，重启后读旧状态又变回去。
