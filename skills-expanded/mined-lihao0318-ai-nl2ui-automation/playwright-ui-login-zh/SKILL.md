---
name: playwright-ui-login-zh
description: Web login (simple + captcha OCR), state persistence. Used by run_case automatically. Triggers: login, run_login, state, captcha.
---

# Web 登录

## 登录类型

| 类型 | 配置块 | 实现 |
|------|--------|------|
| `simple` | `简单登录配置` | `scripts/web/web_simple_login.py` |
| `captcha` | `验证码配置` | `scripts/web/web_captcha_login.py` |

入口：`scripts/web/web_login.py`（按 spec 自动分发）

## 模板

- SauceDemo：`examples/web/logins/saucedemo-user.example.json`
- 验证码 Demo：`examples/web/logins/demo-captcha-user.example.json`

## state

| 路径 | 说明 |
|------|------|
| `state/*.json` | playwright storage state（gitignore） |

## 命令

```bash
python scripts/tools/run_login.py examples/web/logins/saucedemo-user.example.json
python scripts/tools/run_login.py examples/web/logins/demo-captcha-user.example.json --force
```

业务用例在 JSON 根字段声明 `登录配置`；`run_case.py` 无 state 时自动登录。

Schema：[`reference/login-spec-schema.md`](reference/login-spec-schema.md)
