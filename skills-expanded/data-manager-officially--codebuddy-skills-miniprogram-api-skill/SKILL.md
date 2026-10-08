---
name: "miniprogram-api"
description: "微信小程序 API 调用封装和最佳实践。适用于封装请求、处理响应、错误重试、Token 管理。当用户要求开发小程序 API 层时调用。"
---

# 微信小程序 API 调用

## 概述

统一封装小程序的 API 调用，处理认证、错误和响应格式。

## 项目结构

```
miniprogram/
└── api/
    ├── api.js          # 统一请求封装
    ├── auth.js         # 认证相关
    ├── config.js       # API 配置
    └── modules/        # 按模块分离
        ├── user.js
        ├── evaluation.js
        └── report.js
```

## 统一请求封装

### 基础请求函数

```javascript
// miniprogram/api/request.js
const app = getApp();

const request = (options) => {
  return new Promise((resolve, reject) => {
    const token = app.getToken();

    wx.request({
      url: `${app.globalData.baseUrl}${options.url}`,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : ''
      },
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data);
        } else if (res.statusCode === 401) {
          app.clearUserInfo();
          wx.redirectTo({ url: '/pages/index/index' });
          reject({ code: 401, message: '未授权' });
        } else {
          reject(res.data || { message: '请求失败' });
        }
      },
      fail: (err) => {
        reject({ code: -1, message: '网络错误' });
      }
    });
  });
};
```

## 认证 API

### 登录

```javascript
// miniprogram/api/auth.js
const login = (username, password) => {
  return new Promise((resolve, reject) => {
    wx.request({
      url: `${app.globalData.baseUrl}/auth/login`,
      method: 'POST',
      header: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      data: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data);
        } else {
          reject(res.data);
        }
      },
      fail: reject
    });
  });
};

const getUserInfo = () => {
  return request({ url: '/auth/me', method: 'GET' });
};
```

## 业务 API 模块化

### 示例：评估模块

```javascript
// miniprogram/api/modules/evaluation.js
const evaluate = (formData) => {
  return request({
    url: '/evaluation/evaluate',
    method: 'POST',
    data: { form_data: formData }
  });
};

const getHistory = (userId, limit = 10) => {
  return request({
    url: `/evaluation/user/${userId}/history?limit=${limit}`
  });
};

const getVipStatus = () => {
  return request({ url: '/evaluation/vip-status' });
};

module.exports = { evaluate, getHistory, getVipStatus };
```

## 错误处理策略

### 1. Token 过期处理

```javascript
// 自动刷新 Token 或跳转登录
if (res.statusCode === 401) {
  // 尝试刷新 Token
  const refreshed = await refreshToken();
  if (refreshed) {
    // 重新发起请求
    return request(options);
  }
  // 刷新失败，跳转登录页
  app.clearUserInfo();
  wx.redirectTo({ url: '/pages/index/index' });
}
```

### 2. 网络错误重试

```javascript
const requestWithRetry = async (options, maxRetries = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await request(options);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(r => setTimeout(r, 1000 * (i + 1)));
    }
  }
};
```

## 最佳实践

1. **统一封装**：所有 API 通过 request 函数，避免直接使用 wx.request
2. **Promise 化**：便于 async/await 使用
3. **错误分类**：区分网络错误、业务错误、认证错误
4. **Loading 状态**：避免重复请求
5. **参数校验**：前端先校验参数格式

## 适用场景

- 封装新的 API 调用
- 处理 API 响应错误
- 用户登录、Token 管理
- 业务数据请求（评估、报告等）
