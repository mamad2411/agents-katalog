---
description: CodeSpirit JavaScript 开发规范 - AMIS集成、模块模式、API请求、Token管理
globs: *.js
alwaysApply: false
---

# JavaScript 开发规范

## 模块模式

### IIFE 包装

所有 JS 文件使用立即调用函数表达式（IIFE）包装，启用严格模式：

```javascript
/**
 * 模块说明
 * @module ModuleName
 */
(function() {
    'use strict';
    
    // 模块代码
    
    // 导出到全局
    window.ModuleName = {
        // 公共 API
    };
})();
```

### 命名空间导出

全局对象使用 `window` 命名空间导出：

```javascript
// ✅ 正确：使用 window 命名空间
window.TokenManager = (function() {
    'use strict';
    
    function getToken() { /* ... */ }
    
    return {
        getToken,
        setToken,
        clearToken
    };
})();

// ✅ 正确：使用 CodeSpirit 命名空间
window.CodeSpirit = window.CodeSpirit || {};
window.CodeSpirit.i18n = {
    t: function(key, params) { /* ... */ }
};

// ✅ 正确：ES6 类导出
class NotificationClient {
    constructor(hubUrl = '/notification-hub') {
        this.hubUrl = hubUrl;
    }
}
window.NotificationClient = NotificationClient;
```

## 文档注释规范

### 文件头注释

```javascript
/**
 * 考试系统API请求管理器
 * 负责处理API地址转换和统一的请求处理
 * @module ExamApiManager
 * @version 2.0.0
 * @author CodeSpirit Team
 */
```

### 函数注释（JSDoc）

```javascript
/**
 * 设置认证token
 * @param {string} token - 访问token
 * @param {number} [expiryInHours=24] - 过期时间（小时）
 * @returns {void}
 * @throws {Error} 当token为空时抛出错误
 */
function setToken(token, expiryInHours = 24) {
    if (!token || typeof token !== 'string') {
        throw new Error('Token must be a non-empty string');
    }
    // ...
}

/**
 * 统一的API请求函数
 * @param {string} url - API路径
 * @param {Object} [options={}] - fetch选项
 * @returns {Promise<Object>} API响应数据
 * @example
 * const data = await ExamApiManager.request('/exam/api/questions', { method: 'GET' });
 */
async function request(url, options = {}) {
    // ...
}
```

## AMIS 框架集成

### 主题配置

项目使用 **antd** 主题 [[memory:8912919]]：

```javascript
// 初始化 AMIS
let amisScoped = amis.embed('#root', amisJSON, {
    location: history.location,
    data: {},
    context: {
        WEB_HOST: webHost
    }
}, { 
    theme: 'antd'  // 必须使用 antd 主题
});
```

### 事件系统

使用 `onEvent` 配置事件监听：

```javascript
{
    type: 'form',
    api: '/identity/api/identity/auth/login',
    onEvent: {
        // 表单提交成功事件
        submitSucc: {
            actions: [
                {
                    actionType: 'custom',
                    script: `
                        const token = event.data.token;
                        TokenManager.setToken(token, 24);
                        window.location.href = '/';
                    `
                }
            ]
        },
        // 数据初始化完成事件
        fetchInited: {
            actions: [
                {
                    actionType: 'custom',
                    script: 'window.fetchUnreadNotificationCount();'
                }
            ]
        }
    }
}
```

### 行为类型

优先使用 AMIS 内置行为类型（actionType）：

```javascript
// ✅ 核心行为
{ actionType: 'ajax', api: 'POST:/api/submit' }
{ actionType: 'link', link: '/dashboard' }
{ actionType: 'dialog', dialog: { /* ... */ } }
{ actionType: 'reload', target: 'crud' }
{ actionType: 'copy', content: '${text}' }

// ✅ 表单行为
{ actionType: 'submit' }
{ actionType: 'reset' }
{ actionType: 'clear' }

// ✅ 自定义脚本（仅在必要时使用）
{
    actionType: 'custom',
    script: `
        const tenantId = event.data.tenantId;
        window.location.href = '/' + tenantId + '/login';
    `
}
```

### 请求适配器

使用 `requestAdaptor` 和 `adaptor` 处理请求和响应：

```javascript
api: {
    method: 'post',
    url: '/identity/api/identity/auth/login',
    
    // 请求适配器 - 添加认证头
    requestAdaptor: function(api) {
        const token = TokenManager.getToken();
        api.headers = api.headers || {};
        api.headers['Authorization'] = token ? 'Bearer ' + token : '';
        api.headers['X-Forwarded-With'] = 'CodeSpirit';
        api.headers['X-Tenant-Id'] = window.tenantId || 'system';
        return api;
    },
    
    // 响应适配器 - 处理响应数据
    adaptor: function(payload, response, api) {
        if (response.status === 401) {
            window.location.href = '/login';
            return { msg: '登录过期！' };
        }
        
        if (payload.status === 0 && payload.data) {
            TokenManager.setToken(payload.data.token, 24);
        }
        
        return payload;
    }
}
```

## Token 管理

### TokenManager 使用

使用 `TokenManager` 统一管理认证状态：

```javascript
// 初始化模式
TokenManager.initSystemMode();           // 系统平台
TokenManager.initTenantMode('tenant-id'); // 租户平台
TokenManager.initClientMode('tenant-id', 'exam'); // 客户端平台

// Token 操作
TokenManager.setToken('access-token', 24);     // 设置 token（24小时过期）
const token = TokenManager.getToken();          // 获取 token
TokenManager.clearToken();                      // 清除 token
TokenManager.hasToken();                        // 检查是否有 token
TokenManager.isTokenExpired();                  // 检查是否过期
TokenManager.isAuthenticated();                 // 检查是否已认证

// 扩展功能
TokenManager.setTokenExtended(accessToken, refreshToken, expiresIn, tenantId);
TokenManager.getRefreshToken();
TokenManager.getAuthHeaders();                  // 获取认证请求头
TokenManager.setUserInfo(userInfo);
TokenManager.getUserInfo();
```

### 认证请求头

所有 API 请求必须携带认证头：

```javascript
const headers = {
    'Authorization': token ? 'Bearer ' + token : '',
    'X-Forwarded-With': 'CodeSpirit',
    'X-Tenant-Id': tenantId || 'system',
    'Content-Type': 'application/json'
};
```

## API 请求规范

### 服务发现路径

API 路径必须附带服务短名：

```javascript
// ✅ 正确：附带服务名
'/identity/api/identity/profile'
'/exam/api/exam/questions'
'/messaging/api/messaging/messages/my/list'
'/survey/api/surveys/${surveyId}'

// ❌ 错误：缺少服务名
'/api/identity/profile'
'/api/questions'
```

### API 管理器模式

使用统一的 API 管理器处理请求：

```javascript
/**
 * API管理器
 */
window.ExamApiManager = {
    /**
     * 统一的API请求函数
     * @param {string} url - API路径
     * @param {Object} options - fetch选项
     * @returns {Promise} API响应数据
     */
    request: async function(url, options = {}) {
        const token = window.TokenManager?.getToken();
        
        const requestConfig = {
            ...options,
            headers: {
                'Authorization': token ? 'Bearer ' + token : '',
                'X-Tenant-Id': window.tenantId,
                'X-Forwarded-With': 'CodeSpirit',
                'Content-Type': 'application/json',
                ...options.headers
            }
        };

        const response = await fetch(url, requestConfig);
        
        // 处理认证失败
        if (response.status === 401) {
            window.location.href = '/login';
            throw new Error('认证失败，请重新登录');
        }
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const result = await response.json();
        
        if (result.status !== undefined && result.status !== 0) {
            throw new Error(result.msg || '请求失败');
        }
        
        return result.data || result;
    },

    get: function(url, options = {}) {
        return this.request(url, { ...options, method: 'GET' });
    },

    post: function(url, data = null, options = {}) {
        return this.request(url, { 
            ...options, 
            method: 'POST',
            body: data ? JSON.stringify(data) : undefined
        });
    }
};
```

## 缓存管理

### 缓存键命名

使用租户隔离的缓存键：

```javascript
// 格式：{module}_cache_{tenantId}_{key}
const cacheKey = `exam_cache_${tenantId}_login_config`;
const cacheKey = `survey_cache_${tenantId}_form_data`;
```

### 缓存工具类

```javascript
const CacheManager = {
    /**
     * 获取缓存数据
     * @param {string} key - 缓存key
     * @param {string} tenantId - 租户ID
     * @returns {Object|null} 缓存的数据
     */
    get: function(key, tenantId) {
        try {
            const cacheKey = `exam_cache_${tenantId}_${key}`;
            const cached = sessionStorage.getItem(cacheKey);
            if (!cached) return null;

            const data = JSON.parse(cached);
            
            // 检查是否过期
            if (data.expiry && Date.now() > data.expiry) {
                sessionStorage.removeItem(cacheKey);
                return null;
            }
            
            return data.value;
        } catch (error) {
            console.error('[缓存读取失败]', error);
            return null;
        }
    },

    /**
     * 设置缓存数据
     * @param {string} key - 缓存key
     * @param {string} tenantId - 租户ID
     * @param {Object} value - 要缓存的数据
     * @param {number} ttl - 过期时间（毫秒）
     */
    set: function(key, tenantId, value, ttl = 30 * 60 * 1000) {
        try {
            const cacheKey = `exam_cache_${tenantId}_${key}`;
            const data = {
                value: value,
                expiry: ttl ? Date.now() + ttl : null
            };
            sessionStorage.setItem(cacheKey, JSON.stringify(data));
        } catch (error) {
            console.error('[缓存写入失败]', error);
        }
    }
};
```

## 国际化

使用 `CodeSpirit.i18n` 进行翻译：

```javascript
// 初始化（服务器端调用）
window.CodeSpirit.i18n.init('zh-CN', {
    'Login.Title': '用户登录',
    'Login.Success': '登录成功，欢迎 {userName}！'
});

// 获取翻译文本
const title = CodeSpirit.i18n.t('Login.Title');
const message = CodeSpirit.i18n.t('Login.Success', { userName: 'John' });

// 切换语言
CodeSpirit.i18n.switchLanguage('en');
```

## 类定义规范

使用 ES6 class 语法：

```javascript
/**
 * 通知客户端
 * 提供与通知服务的连接和消息处理功能
 */
class NotificationClient {
    /**
     * @param {string} hubUrl - SignalR Hub URL
     */
    constructor(hubUrl = '/notification-hub') {
        this.hubUrl = hubUrl;
        this.connection = null;
        this.handlers = new Map();
    }

    /**
     * 连接到通知服务
     * @returns {Promise} 连接Promise
     */
    async connect() {
        this.connection = new signalR.HubConnectionBuilder()
            .withUrl(this.hubUrl)
            .withAutomaticReconnect()
            .build();

        await this.connection.start();
        console.log('通知连接已建立');
    }

    /**
     * 注册消息处理器
     * @param {string} topic - 主题名称
     * @param {string} type - 消息类型
     * @param {Function} handler - 处理函数
     */
    on(topic, type, handler) {
        const key = `${topic}:${type}`;
        if (!this.handlers.has(key)) {
            this.handlers.set(key, []);
        }
        this.handlers.get(key).push(handler);
    }
}

window.NotificationClient = NotificationClient;
```

## 代码质量要求

### 函数长度限制

一个函数不超过 30 行代码，复杂逻辑拆分为多个小函数：

```javascript
// ✅ 正确：拆分为多个小函数
function handleLoginSuccess(payload) {
    saveToken(payload.data.token);
    redirectToTarget();
}

function saveToken(token) {
    TokenManager.setToken(token, 24);
}

function redirectToTarget() {
    const redirectUrl = getRedirectUrl();
    if (isValidRedirect(redirectUrl)) {
        window.location.href = redirectUrl;
    } else {
        window.location.href = '/';
    }
}
```

### 样式分离

样式写入独立的 CSS 文件，不在 JS 中内联样式：

```javascript
// ✅ 正确：使用 CSS 类名
element.className = 'survey-container loading';

// ❌ 避免：内联样式
element.style.backgroundColor = '#fff';
element.style.padding = '20px';
```

### 响应式支持

界面需要支持响应式布局和移动端适配：

```javascript
// AMIS 配置中使用响应式断点
{
    type: 'grid',
    columns: [
        {
            xs: 12,   // 手机：全宽
            sm: 6,    // 平板：半宽
            md: 4,    // 桌面：三分之一
            lg: 3,    // 大屏：四分之一
            body: { /* ... */ }
        }
    ]
}
```

## 禁止事项

```javascript
// ❌ 禁止：自定义 DOM 事件（使用 AMIS 事件系统）
document.getElementById('btn').addEventListener('click', handler);

// ❌ 禁止：直接操作 DOM（除非必要）
document.getElementById('content').innerHTML = html;

// ❌ 禁止：使用 var 声明变量
var token = getToken();

// ❌ 禁止：缺少错误处理
const response = await fetch(url);
const data = await response.json();

// ❌ 禁止：硬编码敏感信息
const apiKey = 'sk-xxxxxxxx';
```

## AMIS 官方文档

- 📖 组件文档：https://aisuda.bce.baidu.com/amis/zh-CN/docs/index
- 🎨 事件系统：https://aisuda.bce.baidu.com/amis/zh-CN/components/action#%E4%BA%8B%E4%BB%B6%E8%A1%A8
- 🔘 行为按钮：https://aisuda.bce.baidu.com/amis/zh-CN/components/action
- 📝 表单组件：https://aisuda.bce.baidu.com/amis/zh-CN/components/form/index
