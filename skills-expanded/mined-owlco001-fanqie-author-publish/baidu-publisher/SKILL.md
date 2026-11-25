---
name: baidu-publisher
description: 自动在百度作家平台后台创建章节、填写标题正文、保存草稿或发布章节。适用于网文章节上传、草稿保存、批量发布前的浏览器自动化任务。
allowed-tools: exec, read, write
---

# baidu-publisher

用于百度作家平台后台的章节自动化发布。

## 输入参数

- `BOOK_ID`: 书籍 ID
- `TITLE`: 章节标题
- `BODY_PATH`: 正文文件路径
- `AUTO_PUBLISH`: 是否自动发布，`true` / `false`
- `MIN_WORDS`: 最低字数要求

## 执行原则

1. 进入百度作家平台后台并确认已登录。
2. 进入目标作品并打开章节编辑器。
3. 填写标题后必须验证输入框回显。
4. 填写正文后必须验证编辑器内容和字数同步。
5. 保存草稿后必须等待保存状态出现。
6. 若 `AUTO_PUBLISH=true`，则继续执行发布并等待终态。
7. 失败时必须截图并说明卡点。
