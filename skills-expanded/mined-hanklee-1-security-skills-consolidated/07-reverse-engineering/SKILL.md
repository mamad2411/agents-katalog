# 逆向工程

## 工具链

| 工具 | 平台 | 用途 |
|------|------|------|
| IDA Pro | 全平台 | 反编译、反汇编、数据流分析 |
| Ghidra | 全平台 | 开源反编译 |
| radare2 | 全平台 | CLI二进制分析：r2/rabin2/rasm2/radiff2 |
| GDB | Linux | 调试器 |
| Frida | 全平台 | 动态插桩、Hook |
| angr | Python | 符号执行 |
| Unicorn | Python | CPU仿真 |
| Qiling | Python | 高级仿真框架 |
| Binary Ninja | 全平台 | 反编译分析 |

## radare2常用命令

```bash
# 基本分析
r2 -A binary          # 打开并分析
r2 -d binary          # 调试模式
aaa                   # 分析所有
afl                   # 列出函数
pdf @main             # 反编译main函数
s sym.main            # 跳转到main
V                     # 可视化模式
VV                    # 图形模式

# 信息查看
iI                    # 二进制信息
iS                    # section信息
ii                    # 导入函数
ie                    # 入口点
iz                    # 字符串

# 调试
db main               # 断点
dc                    # 继续执行
ds                    # 单步
dr                    # 寄存器
px @rsp               # 查看内存

# 搜索
/x 9090               # 搜索字节
/ string              # 搜索字符串
```

## IDA Pro常用操作

```
# 快捷键
Space        # 切换图形/文本视图
F5           # 反编译(Hex-Rays)
X            # 交叉引用
N            # 重命名
Y            # 修改类型
G            # 跳转到地址
;            # 添加注释
H            # 十进制/十六进制切换

# 常用窗口
IDA View     # 反汇编视图
Pseudocode   # 伪代码视图
Strings      # 字符串窗口
Imports      # 导入函数
Exports      # 导出函数
Functions    # 函数列表
```

## Frida Hook

```javascript
// Hook Java方法
Java.perform(function() {
    var MainActivity = Java.use('com.target.MainActivity');
    MainActivity.checkLogin.implementation = function(username, password) {
        console.log('Username: ' + username);
        console.log('Password: ' + password);
        return true; // 强制返回true
    };
});

// Hook Native函数
Interceptor.attach(Module.findExportByName('libnative.so', 'check'), {
    onEnter: function(args) {
        console.log('arg0: ' + Memory.readUtf8String(args[0]));
    },
    onLeave: function(retval) {
        retval.replace(1); // 修改返回值
    }
});

// Hook libc
Interceptor.attach(Module.findExportByName(null, 'strcmp'), {
    onEnter: function(args) {
        console.log('strcmp: ' + Memory.readUtf8String(args[0]) + ' vs ' + Memory.readUtf8String(args[1]));
    }
});
```

## APK逆向

1. APK解包：`apktool d target.apk`
2. 反编译：`jadx-gui target.apk`
3. smali修改关键逻辑
4. Frida Hook关键函数
5. 重打包签名：`apktool b target/ && jarsigner -keystore key.jks target.apk alias`

## 前端JS逆向

1. 签名链路定位（抓包分析加密参数）
2. 加密参数分析（搜索关键字段名）
3. 运行时采样（断点调试）
4. Node补环境复现
5. 联动工具自动化

## 固件渗透（OWASP FSTM九阶段）

1. 固件获取
2. 固件提取（binwalk -e firmware.bin）
3. 文件系统分析
4. 静态分析
5. 动态分析（Firmadyne仿真）
6. 漏洞发现
7. AFL++ Fuzzing
8. 实机利用
9. 报告编写

## EDR绕过逆向

红队场景：逆向EDR hook表 → Direct Syscall / Hell's Gate / Call Stack Spoof

```c
// Direct Syscall示例
__asm__(
    "mov r10, rcx
"
    "mov eax, 0x" SYSCALL_NUMBER "
"
    "syscall
"
    "ret
"
);
```
