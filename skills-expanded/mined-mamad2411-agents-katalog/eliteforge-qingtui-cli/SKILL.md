---
name: eliteforge-qingtui-cli
description: 通过 qingtui 命令操作轻推轻应用。当用户要求操作轻推、轻应用时应使用该包，支持用户查询、用户解析、openid 解析、文本发送操作。list-users，resolve-users，send-text。
---

# EliteForge QingTui CLI
## 依赖准备
以下工具不存在，先尝试自动安装：
- python3
- pipx
- jq
上下文或环境变量中的**内部变量**缺失，终止运行，提示用户补全相关变量。  

## 工作流
1. 先确认依赖和变量可用。
2. 每次使用前都检查 `eliteforge-qingtui-cli` 是否已安装。
   - 未安装时执行：`pipx install eliteforge-qingtui-cli`
3. 每次使用前都执行：`pipx upgrade eliteforge-qingtui-cli`
4. 先看帮助再执行具体命令，避免硬编码能力说明。
   - 总帮助：`qingtui -h`
   - 用户列表：`qingtui list-users -h`
   - 用户解析：`qingtui resolve-users -h`
   - 文本发送：`qingtui send-text -h`
5. 按用户目标执行命令，可编写脚本自行编排接口。
6. 涉及发送时，优先确认收件人来源，避免混淆 `--user-name`、`--user-login`、`--open-id`。

## 使用案例
向特定用户发送文本消息：
```bash
# 先通过用户手机号获取openid
openid=$(qingtui resolve-users --user-login '13800138000' | jq -r '.open_ids[0]')
# 发送文本消息
qingtui send-text --open-id $openid --content "Hello Alice!"
```

## Environment Hints
上下文或环境变量中应该存在:
  QINGTUI_APPID               [必填] 轻应用 ID
  QINGTUI_SECRET              [必填] 轻应用密钥
  QINGTUI_API_BASE            [可选] API 地址，默认 https://open.qingtui.com
  QINGTUI_USER_LIST_MAX_PAGES [可选] 用户列表分页上限，默认 5
  QINGTUI_USER_LIST_PAGE_SIZE [可选] 用户列表分页大小，默认 1000
  QINGTUI_MESSAGE_MAX_LENGTH  [可选] 文本消息最大长度，默认 500

## Output Rules
- 输出保持简洁，必要时可配合 `jq` 等Linux管道工具，处理接口JSON响应。
- 失败时返回实际执行的命令和关键报错。
- 需要更多命令说明时，继续引导查看对应 `-h`。
