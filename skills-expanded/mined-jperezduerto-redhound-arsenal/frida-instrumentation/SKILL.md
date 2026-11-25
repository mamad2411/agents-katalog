---
name: frida-instrumentation
description: >
  Operate Frida — a dynamic instrumentation toolkit for hooking and modifying running
  processes. Use when performing runtime analysis of desktop or mobile applications,
  bypassing SSL pinning or root detection, hooking native/Java/Objective-C functions,
  reversing mobile apps (Android/iOS), or automating instrumentation with Objection.
  Covers installation, JavaScript API (Interceptor, Module, Memory, NativeFunction), frida-trace,
  RPC exports, Objection integration, Android/iOS setup with frida-server, and end-to-end
  mobile app pentesting workflows.
license: LGPL-2.1
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/frida/frida
---

# frida-instrumentation Agent Skill

## When to Use This Skill

Use this skill when:
- Bypassing SSL certificate pinning in Android or iOS apps during DAST
- Hooking Java/Kotlin/Objective-C/Swift methods at runtime without modifying APK/IPA
- Tracing native function calls in a running process
- Reversing mobile app encryption, license checks, or anti-tampering mechanisms
- Bypassing root detection, emulator detection, or jailbreak detection
- Automating mobile app pentesting with Objection
- Building dynamic analysis scripts for malware or binary research

## What Frida Does

Frida is a cross-platform dynamic instrumentation framework that injects a JavaScript engine
(V8/Duktape) into a target process at runtime. It enables reading/writing memory, hooking
arbitrary functions, intercepting calls across Java, Objective-C, and native code layers,
and exporting RPC interfaces for external control — all without recompilation or source
access. It runs on Windows, macOS, Linux, Android, and iOS, making it the primary tool
for mobile application security testing and runtime analysis.

## Installation

### frida-tools (host machine)

```bash
# Python package (pip) — installs frida, frida-trace, frida-ps, frida-ls-devices
pip install frida-tools

# Verify
frida --version
frida-ps --version

# Upgrade
pip install -U frida-tools

# Specific version (pin to match frida-server version)
pip install frida==16.2.1 frida-tools==12.4.3
```

### frida-server (Android device)

```bash
# 1. Find device architecture
adb shell getprop ro.product.cpu.abi
# → arm64-v8a, armeabi-v7a, x86, x86_64

# 2. Download matching frida-server from:
# https://github.com/frida/frida/releases
# e.g.: frida-server-16.2.1-android-arm64.xz

# 3. Push and start
xz -d frida-server-16.2.1-android-arm64.xz
adb push frida-server-16.2.1-android-arm64 /data/local/tmp/frida-server
adb shell chmod +x /data/local/tmp/frida-server
adb shell /data/local/tmp/frida-server &

# 4. Verify connection
frida-ps -U        # -U = USB device
frida-ps -U | grep -i target_app
```

### frida-server (iOS device — jailbroken)

```bash
# Via Cydia/Sileo — add Frida repo: https://build.frida.re
# Install: Frida (package)

# Verify
frida-ps -U        # USB, or -R for remote TCP

# TCP connection (if USB unavailable)
frida-ps -H 192.168.1.50:27042
```

### frida-gadget (non-rooted / non-jailbroken)

```bash
# Inject frida-gadget.so into APK (requires APK repackaging)
# Tool: objection patchapk (easiest method)
objection patchapk -s target.apk

# Or manual:
# 1. Download frida-gadget-XX-android-arm64.so.xz
# 2. Embed in APK lib directory
# 3. Load via modified smali or patched native library entry point
```

## Core Concepts

### Attach vs Spawn

```bash
# Attach to running process (by name or PID)
frida -U -n "com.target.app"              # attach by package name
frida -U -p 1234                          # attach by PID

# Spawn (start app, pause before main, inject)
frida -U -f com.target.app --no-pause     # spawn and run
frida -U -f com.target.app                # spawn, pause at entry (for early hooks)

# Load script at attach/spawn
frida -U -f com.target.app -l hook.js --no-pause
```

### Script execution modes

```bash
# Interactive REPL
frida -U -n com.target.app
# → JavaScript REPL prompt

# One-shot script
frida -U -n com.target.app -l script.js

# Script with output (eval mode)
frida -U -n com.target.app -e "Java.perform(function(){ console.log('hi'); })"
```

## JavaScript API Reference

### Java API (Android)

```javascript
// All Java hooking must be inside Java.perform()
Java.perform(function() {

    // Hook a class method
    var MainActivity = Java.use('com.target.app.MainActivity');

    // Hook instance method
    MainActivity.checkPin.implementation = function(pin) {
        console.log('[*] checkPin called with: ' + pin);
        var result = this.checkPin(pin);   // call original
        console.log('[*] checkPin result: ' + result);
        return result;
    };

    // Override return value
    MainActivity.isRooted.implementation = function() {
        console.log('[*] isRooted hooked — returning false');
        return false;
    };

    // Hook overloaded method (specify signature)
    var String = Java.use('java.lang.String');
    String.equals.overload('java.lang.String').implementation = function(other) {
        var result = this.equals(other);
        if (this.toString().indexOf('password') !== -1) {
            console.log('[*] String.equals: ' + this + ' == ' + other + ' → ' + result);
        }
        return result;
    };

    // Enumerate loaded classes
    Java.enumerateLoadedClasses({
        onMatch: function(className) {
            if (className.indexOf('target') !== -1) {
                console.log('[*] Found class: ' + className);
            }
        },
        onComplete: function() {}
    });

    // Instantiate a Java object
    var SecretClass = Java.use('com.target.app.SecretClass');
    var instance = SecretClass.$new('arg1');
    console.log(instance.getSecret());

    // Access static field
    console.log(MainActivity.SECRET_KEY.value);

    // Modify instance field
    MainActivity.checkPin.implementation = function(pin) {
        this.mMaxAttempts.value = 9999;   // modify field
        return this.checkPin(pin);
    };
});
```

### Interceptor API (Native / C functions)

```javascript
// Hook by exported symbol name
Interceptor.attach(Module.findExportByName('libc.so', 'strcmp'), {
    onEnter: function(args) {
        // args[0], args[1] are NativePointer objects
        var s1 = args[0].readUtf8String();
        var s2 = args[1].readUtf8String();
        if (s1 !== null && s2 !== null) {
            console.log('[strcmp] "' + s1 + '" vs "' + s2 + '"');
        }
        this.s2 = s2;   // save for onLeave
    },
    onLeave: function(retval) {
        console.log('[strcmp] returned: ' + retval);
        // Force return 0 (strings equal)
        retval.replace(0);
    }
});

// Hook by absolute address
var targetAddr = Module.findBaseAddress('libapp.so').add(0x1234);
Interceptor.attach(targetAddr, {
    onEnter: function(args) {
        console.log('[*] hit target function, arg0 = ' + args[0]);
    },
    onLeave: function(retval) {
        retval.replace(ptr(1));   // return 1 (true)
    }
});

// Replace entire function
Interceptor.replace(targetAddr, new NativeCallback(function(a, b) {
    console.log('[*] replaced function called');
    return 1;    // always return 1
}, 'int', ['int', 'int']));
```

### Module API

```javascript
// List loaded modules
Process.enumerateModules().forEach(function(m) {
    console.log(m.name, m.base, m.size);
});

// Find module by name
var lib = Process.findModuleByName('libssl.so');
console.log('Base:', lib.base);

// Enumerate exports of a module
Module.enumerateExports('libc.so').forEach(function(exp) {
    if (exp.name.indexOf('SSL') !== -1) {
        console.log(exp.name, exp.address);
    }
});

// Find base address
var base = Module.findBaseAddress('libapp.so');
console.log('libapp.so base:', base);

// Get all symbols (including non-exported)
Module.enumerateSymbols('libapp.so').forEach(function(sym) {
    if (sym.name.indexOf('check') !== -1) {
        console.log(sym.name, sym.address);
    }
});
```

### Memory API

```javascript
// Read memory
var addr = ptr('0x7f001234');
console.log(addr.readU8());           // 1 byte unsigned
console.log(addr.readU32());          // 4 bytes
console.log(addr.readUtf8String());   // null-terminated C string
console.log(addr.readByteArray(16));  // raw 16 bytes

// Write memory
addr.writeU8(0x90);                   // write single byte (NOP)
addr.writeByteArray([0x90, 0x90]);    // write bytes
addr.writeUtf8String('patched');      // write string

// Allocate new memory
var buf = Memory.alloc(64);
buf.writeUtf8String('injected_string');

// Search memory for pattern
Memory.scan(base, 0x1000, '41 42 43 ?? 45', {
    onMatch: function(address, size) {
        console.log('[*] Pattern at: ' + address);
    },
    onComplete: function() {}
});

// Protect / change permissions
Memory.protect(ptr('0x401000'), 0x1000, 'rwx');
```

### NativeFunction and NativeCallback

```javascript
// Call an existing native function
var strlen = new NativeFunction(
    Module.findExportByName('libc.so', 'strlen'),
    'size_t',         // return type
    ['pointer']       // argument types
);
var len = strlen(Memory.allocUtf8String('hello'));
console.log('length:', len);

// Create a native function to pass as callback
var myCallback = new NativeCallback(function(data, len) {
    console.log('[*] callback triggered, len =', len);
    return 0;
}, 'int', ['pointer', 'int']);

// Register as callback with a target function
var setCallback = new NativeFunction(
    Module.findExportByName('libapp.so', 'register_callback'),
    'void',
    ['pointer']
);
setCallback(myCallback);
```

### ObjC API (iOS)

```javascript
// Hook Objective-C method
var className = 'AppDelegate';
var methodName = '- validateLicense:';

if (ObjC.available) {
    var klass = ObjC.classes[className];
    var method = klass[methodName];

    Interceptor.attach(method.implementation, {
        onEnter: function(args) {
            // args[0] = self, args[1] = selector, args[2+] = method args
            var licenseKey = ObjC.Object(args[2]).toString();
            console.log('[*] validateLicense called: ' + licenseKey);
        },
        onLeave: function(retval) {
            // ObjC BOOL is int (0/1)
            retval.replace(ptr(1));  // always return YES
        }
    });

    // Enumerate all methods of a class
    klass.$ownMethods.forEach(function(method) {
        console.log(method);
    });
}
```

## frida-trace — Automatic Hooking

```bash
# Trace all calls to functions matching pattern
frida-trace -U -n com.target.app -i "Java_*"     # all JNI functions
frida-trace -U -n com.target.app -i "SSL_*"      # all SSL functions
frida-trace -U -n com.target.app -i "strcmp"     # single function

# Trace Objective-C methods (iOS)
frida-trace -U -n TargetApp -m "-[AppDelegate *]"  # all AppDelegate methods
frida-trace -U -n TargetApp -m "*validate*"         # methods containing 'validate'

# Trace ObjC + native
frida-trace -U -f com.target.app -i "open*" -m "-[NSURLSession *]" --no-pause

# Custom handler output directory
frida-trace -U -n com.target.app -i "SSL_read" -o ./handlers
# Creates handlers/SSL_read.js — auto-generated, edit for custom logic
```

## RPC Exports (Calling Frida from Python)

```javascript
// script.js — export functions for Python caller
rpc.exports = {
    dumpStrings: function() {
        var results = [];
        Java.perform(function() {
            Java.enumerateLoadedClasses({
                onMatch: function(c) { results.push(c); },
                onComplete: function() {}
            });
        });
        return results;
    },
    callDecrypt: function(ciphertext) {
        var result = null;
        Java.perform(function() {
            var Crypto = Java.use('com.target.app.CryptoUtils');
            result = Crypto.decrypt(Java.use('java.lang.String').$new(ciphertext));
        });
        return result ? result.toString() : null;
    }
};
```

```python
# caller.py
import frida, sys

def on_message(message, data):
    print('[msg]', message)

device = frida.get_usb_device()
session = device.attach('com.target.app')

with open('script.js', 'r') as f:
    script = session.create_script(f.read())

script.on('message', on_message)
script.load()

# Call exported RPC functions
api = script.exports
classes = api.dump_strings()
print(f'Found {len(classes)} classes')

plaintext = api.call_decrypt('U2FsdGVkX1+...')
print('Decrypted:', plaintext)
```

## Common Workflows

### SSL Pinning Bypass (Android)

```javascript
// Universal SSL bypass — covers OkHttp3, Trustmanager, Network Security Config
Java.perform(function() {

    // Method 1: TrustManager override
    var TrustManagerImpl = Java.use('com.android.org.conscrypt.TrustManagerImpl');
    TrustManagerImpl.verifyChain.implementation = function(untrustedChain, trustAnchorChain, host, clientAuth, ocspData, tlsSctData) {
        console.log('[*] TrustManagerImpl.verifyChain bypassed for: ' + host);
        return untrustedChain;
    };

    // Method 2: OkHttp3 CertificatePinner
    try {
        var CertificatePinner = Java.use('okhttp3.CertificatePinner');
        CertificatePinner.check.overload('java.lang.String', 'java.util.List').implementation = function(hostname, certs) {
            console.log('[*] OkHttp3 CertificatePinner.check bypassed for: ' + hostname);
        };
    } catch(e) { console.log('[!] OkHttp3 not found: ' + e); }

    // Method 3: SSLContext
    var X509TrustManager = Java.use('javax.net.ssl.X509TrustManager');
    var TrustAllManager = Java.registerClass({
        name: 'com.frida.TrustAll',
        implements: [X509TrustManager],
        methods: {
            checkClientTrusted: function(chain, authType) {},
            checkServerTrusted: function(chain, authType) {},
            getAcceptedIssuers: function() { return []; }
        }
    });
    var SSLContext = Java.use('javax.net.ssl.SSLContext');
    var ctx = SSLContext.getInstance('TLS');
    ctx.init(null, [TrustAllManager.$new()], null);
    SSLContext.getDefault.implementation = function() { return ctx; };
});
```

```bash
# Or use Objection for one-liner SSL bypass
objection --gadget com.target.app explore
objection> android sslpinning disable
```

### Root Detection Bypass

```javascript
Java.perform(function() {

    // RootBeer / common root check classes
    var classes = [
        'com.scottyab.rootbeer.RootBeer',
        'com.topjohnwu.superuser.Shell',
    ];

    classes.forEach(function(cls) {
        try {
            var c = Java.use(cls);
            if (c.isRooted) {
                c.isRooted.implementation = function() { return false; };
                console.log('[*] Hooked ' + cls + '.isRooted');
            }
        } catch(e) {}
    });

    // Hook common file existence checks
    var File = Java.use('java.io.File');
    File.exists.implementation = function() {
        var path = this.getAbsolutePath();
        var rootPaths = ['/su', '/system/bin/su', '/sbin/su', '/system/xbin/su'];
        if (rootPaths.indexOf(path) !== -1) {
            console.log('[*] File.exists blocked for: ' + path);
            return false;
        }
        return this.exists();
    };

    // Block Runtime.exec calls for 'su'
    var Runtime = Java.use('java.lang.Runtime');
    Runtime.exec.overload('[Ljava.lang.String;').implementation = function(cmd) {
        var command = cmd.join(' ');
        if (command.indexOf('su') !== -1 || command.indexOf('which') !== -1) {
            console.log('[*] Blocked exec: ' + command);
            throw Java.use('java.io.IOException').$new('File not found');
        }
        return this.exec(cmd);
    };
});
```

### Crypto Key Extraction

```javascript
// Hook javax.crypto.SecretKeySpec to grab AES keys
Java.perform(function() {
    var SecretKeySpec = Java.use('javax.crypto.SecretKeySpec');
    SecretKeySpec.$init.overload('[B', 'java.lang.String').implementation = function(keyBytes, algorithm) {
        console.log('[*] SecretKeySpec created:');
        console.log('    Algorithm: ' + algorithm);
        console.log('    Key (hex): ' + bytesToHex(keyBytes));
        return this.$init(keyBytes, algorithm);
    };

    // Hook Cipher for encrypt/decrypt
    var Cipher = Java.use('javax.crypto.Cipher');
    Cipher.doFinal.overload('[B').implementation = function(input) {
        var result = this.doFinal(input);
        console.log('[Cipher.doFinal]');
        console.log('    Input:  ' + bytesToHex(input));
        console.log('    Output: ' + bytesToHex(result));
        return result;
    };
});

function bytesToHex(bytes) {
    var hex = '';
    for (var i = 0; i < bytes.length; i++) {
        hex += ('0' + (bytes[i] & 0xFF).toString(16)).slice(-2);
    }
    return hex;
}
```

### iOS Jailbreak Detection Bypass

```javascript
if (ObjC.available) {
    // Hook file existence checks (jailbreak file paths)
    Interceptor.attach(Module.findExportByName('libc.dylib', 'access'), {
        onEnter: function(args) {
            var path = args[0].readUtf8String();
            var jbPaths = ['/Applications/Cydia.app', '/bin/bash', '/usr/sbin/sshd',
                           '/etc/apt', '/private/var/lib/apt'];
            if (jbPaths.some(p => path && path.includes(p))) {
                console.log('[*] access() blocked for: ' + path);
                args[0] = Memory.allocUtf8String('/nonexistent');
            }
        }
    });

    // Hook stat
    Interceptor.attach(Module.findExportByName('libSystem.B.dylib', 'stat'), {
        onEnter: function(args) {
            var path = args[0].readUtf8String();
            if (path && path.includes('Cydia')) {
                args[0] = Memory.allocUtf8String('/nonexistent');
            }
        }
    });

    // Hook Objective-C string comparisons used in JB checks
    var NSFileManager = ObjC.classes.NSFileManager;
    Interceptor.attach(NSFileManager['- fileExistsAtPath:'].implementation, {
        onEnter: function(args) {
            var path = ObjC.Object(args[2]).toString();
            if (path.includes('Cydia') || path.includes('substrate')) {
                console.log('[*] fileExistsAtPath blocked: ' + path);
                this.block = true;
            }
        },
        onLeave: function(retval) {
            if (this.block) retval.replace(ptr(0));
        }
    });
}
```

## Objection Framework Integration

Objection is a runtime exploration toolkit built on Frida that provides common pentest
operations as simple commands without writing scripts.

```bash
pip install objection

# Connect to running app
objection --gadget com.target.app explore

# Connect to spawned app
objection --gadget com.target.app --startup-command 'android sslpinning disable' explore

# Common Objection commands (inside explore session):

# Android
android sslpinning disable              # disable SSL pinning
android root disable                    # bypass root detection
android keystore list                   # list keystore entries
android keystore dump                   # dump keystore keys
android intent launch_activity <class>  # launch activity
android hooking list classes            # list all classes
android hooking list class_methods <cls> # list methods
android hooking watch class <cls>       # hook all methods of class
android hooking watch method <cls>.<method> --dump-args --dump-return
android hooking search classes <term>   # search class names
android heap instances of <class>       # get live instances from heap
android heap evaluate <cls> this.<method>()  # call method on live instance

# iOS
ios sslpinning disable                  # disable SSL pinning
ios jailbreak disable                   # bypass jailbreak detection
ios keychain dump                       # dump Keychain entries
ios plist cat <path>                    # read plist file
ios hooking list classes
ios hooking watch method "+[ClassName method:]" --dump-args

# General
jobs list                               # list active hooks
jobs kill <id>                          # remove hook
memory dump all <outfile>               # dump process memory
memory search "<hex pattern>"           # search memory
```

## Troubleshooting

**`frida-server` not found / connection refused**
```bash
# Verify frida-server is running
adb shell ps | grep frida-server
# Restart
adb shell pkill frida-server
adb shell /data/local/tmp/frida-server &
# Check version mismatch (must match frida Python package)
frida --version
adb shell /data/local/tmp/frida-server --version
```

**`Unable to find application with identifier 'com.target.app'`**
```bash
# App not running — use -f to spawn, or start app first then attach
frida-ps -Ua         # list running apps on USB device
frida -U -f com.target.app --no-pause -l hook.js
```

**`Script not responding / Java.perform callback never fires`**
```javascript
// Java.perform is asynchronous on attach
// Ensure hook is reached by user interaction, or use setImmediate
setImmediate(function() {
    Java.perform(function() {
        // hook code here
    });
});
```

**`ClassNotFoundException` for target class**
```javascript
// Class may not be loaded yet — use ClassLoader enumeration
Java.enumerateClassLoaders({
    onMatch: function(loader) {
        try {
            var cls = loader.loadClass('com.target.app.HiddenClass');
            Java.use('com.target.app.HiddenClass');
            // use class here
        } catch(e) {}
    },
    onComplete: function() {}
});
```

**Frida detected / anti-Frida bypasses**
```bash
# Apps may detect frida-server port (27042) or /proc/self/maps entries
# Use frida-gadget with custom config instead of frida-server
# Or use Magisk module to hide frida-server process name
# Rename frida-server binary to a system process name:
adb shell cp /data/local/tmp/frida-server /data/local/tmp/svchost
adb shell /data/local/tmp/svchost &
```

**`EPERM` when attaching to system process**
```bash
# Frida-server must run as root for system process attachment
adb shell su -c '/data/local/tmp/frida-server &'
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
