---
name: nanofile-apps
description: Search installed Windows applications, launch desktop programs with arguments, and trigger app uninstall workflows using NanoFile.
---

# NanoFile 应用程序读写技能 (Application Management)

管理系统已安装应用程序：搜索应用、启动程序与引导卸载。

## 适用场景

- 用户想要查找电脑上安装了哪些软件，或按名称检索已安装应用。
- 用户需要启动某个桌面程序（可选附带参数或待打开的文件）。
- 用户需要卸载某个应用程序（合规唤起 Windows 设置中的应用管理界面）。

## 包含工具 (3 个)

### 1. `search_apps`

从 Windows 注册表检索已安装的桌面应用程序（包含名称、发布商、版本、安装目录）。

```json
{
  "query": "Visual Studio"
}
```

返回结果包含检索耗时统计（整数显示与自动进位单位，如 `450µs`、`18ms`、`2s`）与命中的应用清单：

```json
{
  "elapsed": "18ms",
  "elapsed_ms": 18,
  "total": 1,
  "apps": [
    {
      "name": "Visual Studio Code",
      "publisher": "Microsoft Corporation",
      "version": "1.93.0",
      "install_location": "C:\\Program Files\\Microsoft VS Code"
    }
  ]
}
```

### 2. `launch_app`

安全启动已安装的应用程序（支持附加命令行参数）。

```json
{
  "app_path_or_command": "notepad.exe",
  "arguments": ["C:\\Users\\Username\\notes.txt"]
}
```

### 3. `uninstall_app`

唤起 Windows 系统的应用卸载管理页，引导用户确认并安全卸载指定应用。

```json
{
  "app_name": "OldTool"
}
```
