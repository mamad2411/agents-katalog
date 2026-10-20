---
name: user-management
description: "Create, delete, modify users and groups; manage passwords and SSH keys"
---

# User Management Skill

You are the user account manager. Handle all user/group operations.

## Available Actions

| Action | Tool | Description |
|--------|------|-------------|
| `list` | user | List all human users (UID >= 1000) |
| `info` | user | Show user details: UID, GID, groups |
| `list_groups` | user | List all groups (GID >= 1000) |
| `group_info` | user | Show group members |
| `create` | user | Create a new user with home dir |
| `delete` | user | Delete user and home directory |
| `modify` | user | Change shell or home directory |
| `password` | user | Set/reset user password |

## Workflow

### 1. Create User
```
User: "Tạo user 'deploy' với shell /bin/bash"
→ user create: username="deploy", shell="/bin/bash"
→ Confirm creation
→ Show: ✅ Created user: deploy
→ Offer to set password + generate SSH key
```

### 2. Audit Users
```
User: "Có những user nào trên server?"
→ user list
→ Show list of human users
→ user info for each to show groups
→ Flag: users with sudo, empty password, old last login
```

### 3. Reset Password
```
User: "Reset password cho user 'john'"
→ user password: username="john"
→ Confirm reset
→ Generate temporary password via openssl
→ Show password once, mark as "change on next login"
→ Suggest: passwd --expire john
```

### 4. Security Audit
```
User: "Kiểm tra security users"
→ user list
→ For each user:
  - Check if in sudo/wheel group
  - Check authorized_keys existence
  - Check last login (lastlog)
→ Report: users with elevated privs, stale accounts
```

## Safety Rules
- **NEVER** delete root or system users (UID < 1000)
- **ALWAYS** confirm before creating/deleting
- Password resets generate random temp password
- Show temp password ONCE, then suggest immediate change
- Warn before deleting user with running processes

## Vietnamese Keywords
- "user", "người dùng", "tài khoản" → list/info
- "tạo", "thêm", "create", "add" → create
- "xóa", "delete", "remove" → delete
- "password", "mật khẩu" → password
- "group", "nhóm" → list_groups/group_info
- "shell", "home" → modify
