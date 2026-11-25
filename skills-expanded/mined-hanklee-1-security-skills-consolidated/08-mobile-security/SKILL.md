# 移动安全

## Android渗透测试（runtime-first原则）

### 核心操作顺序
1. **确认设备** → adb连接
2. **准备抓包** → Burp/Charles代理配置
3. **scrcpy驱动** → UI自动化业务流程
4. **检查抓包** → 分析HTTP/HTTPS流量
5. **能重放则直接Web测试** → Burp Repeater
6. **抓不到包才升级** → jadx/frida/ida

### 工具链
| 工具 | 用途 |
|------|------|
| adb | 设备连接、应用管理 |
| jadx | APK反编译 |
| Burp Suite | 代理抓包 |
| Frida | 动态Hook |
| scrcpy | 屏幕投射 |
| Objection | 快速Hook框架 |
| Magisk | Root管理 |

### ADB常用命令
```bash
adb devices                           # 列出设备
adb install target.apk                # 安装APK
adb shell pm list packages            # 列出包名
adb shell pm path com.target.app      # 查看APK路径
adb pull /data/app/com.target.app/    # 拉取APK
adb shell dumpsys activity top        # 当前Activity
adb logcat | grep -i "password\|token\|key"  # 日志监控
```

## SSL Pinning绕过

### Frida绕过
```javascript
Java.perform(function() {
    var TrustManager = Java.registerClass({
        name: 'com.custom.TrustManager',
        implements: [Java.use('javax.net.ssl.X509TrustManager')],
        methods: {
            checkClientTrusted: function(chain, authType) {},
            checkServerTrusted: function(chain, authType) {},
            getAcceptedIssuers: function() { return []; }
        }
    });

    var SSLContext = Java.use('javax.net.ssl.SSLContext');
    var ctx = SSLContext.getInstance('TLS');
    ctx.init(null, [TrustManager.$new()], null);
    
    var OkHttp = Java.use('okhttp3.OkHttpClient$Builder');
    OkHttp.sslSocketFactory.implementation = function(ssf, tm) {
        return this.sslSocketFactory(ctx.getSocketFactory(), TrustManager.$new());
    };
});
```

### Objection绕过
```bash
objection -g com.target.app explore
android sslpinning disable
```

## Root/越狱检测绕过

- Frida Hook检测函数返回false
- Magisk Hide / Shamiko
- iOS: Liberty Lite / Shadow

### Frida绕过Root检测
```javascript
Java.perform(function() {
    // 常见Root检测类
    var RootDetection = Java.use('com.target.security.RootDetection');
    RootDetection.isRooted.implementation = function() {
        return false;
    };
    
    // 常见检测方法
    var Runtime = Java.use('java.lang.Runtime');
    Runtime.exec.overload('java.lang.String').implementation = function(cmd) {
        if (cmd.indexOf('su') !== -1 || cmd.indexOf('which') !== -1) {
            return null;
        }
        return this.exec(cmd);
    };
});
```

## iOS安全

- 越狱设备分析
- Keychain数据提取：`keychain_dumper`
- IPA逆向：class-dump + Hopper
- 签名机制分析：`codesign -dv --verbose=4 Target.app`
