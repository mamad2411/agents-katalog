---
name: ruoyi-api
description: 若依(RuoYi)系统管理 API 调用工具。当用户需要操作若依系统的用户、角色、菜单、部门时激活。触发词："若依"、"ruoyi"、"创建用户"、"分配角色"、"创建菜单"。需要配置 .env 文件（RUOYI_BASE_URL、RUOYI_TOKEN）。
---

# ruoyi-api

直接调用若依系统管理接口的工具。

## 配置

在项目根目录创建 `.env` 文件：

```bash
RUOYI_BASE_URL=http://localhost:3700
RUOYI_TOKEN=your_bearer_token_here
```

获取 Token：登录若依系统 → 浏览器开发者工具 → Network → 请求头中的 `Authorization` 字段（复制 `Bearer ` 后面的值）

## API 文档

详细接口文档按模块分类，按需查阅：

- **用户管理** - 见 [references/user.md](references/user.md)
- **角色管理** - 见 [references/role.md](references/role.md)
- **菜单管理** - 见 [references/menu.md](references/menu.md)
- **部门管理** - 见 [references/dept.md](references/dept.md)

## 快速开始

```python
from scripts.client import create_client

api = create_client()

# 查询用户
api.list_users({'pageNum': 1, 'pageSize': 10})

# 创建用户
api.create_user({
    'userName': 'test',
    'nickName': '测试',
    'password': '123456',
    'deptId': 100
})

# 创建角色
api.create_role({
    'roleName': '测试角色',
    'roleKey': 'test',
    'roleSort': 10
})
```

## 命令行使用

```bash
python3 scripts/client.py list-users
python3 scripts/client.py create-user --data '{"userName":"test","password":"123456","deptId":100}'
```
