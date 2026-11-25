---
name: apifox-api
description: >-
  Use this skill when working in a JavaScript/TypeScript frontend project
  and the user asks to inspect a page, component, API request file, or
  feature to find what interfaces it calls, what request paths/methods
  are used, or what request/response TypeScript types are needed. Also
  use when the user provides an API URL or endpoint path directly. Trigger
  phrases include "看看这个页面的接口", "这个页面调了哪些接口",
  "查一下这个接口的入参返回值", "补接口类型", "根据页面找接口",
  "JS 项目没有类型", "分析一下这个请求", "帮我理解这段代码",
  "这个返回结构是什么". The agent should first inspect the project source
  code to locate API request functions, extract the request URL/path and
  HTTP method, then run `apifox-api get "<path>"` or
  `apifox-api get METHOD "<path>"`. If the user provides a complete URL,
  never search first: extract the pathname and run `get` first. Use
  `search` only for vague keywords or after `get` cannot find the endpoint.
---

# apifox-api --- Apifox API Interface Assistant

This skill controls how to use the apifox-api CLI.

The CLI provides:

-   Search Apifox API interfaces
-   Generate TypeScript request/response types
-   Understand API contracts from frontend code
-   Help create missing API request functions

# Primary Trigger (read first)

When the user asks to inspect a frontend page, component, feature, or
existing API request function and understand its API interfaces, use
this skill.

Common user requests:

- 看看这个页面的接口
- 这个页面调了哪些接口
- 帮我把这个 JS 页面用到的接口类型补一下
- 根据这个页面找接口的入参返回值
- 这个接口请求函数没有类型，查一下 Apifox
- 看下这个模块需要哪些 API 类型

In this workflow, do NOT start with `apifox-api search`.

First inspect the project source code, find the request function, and
extract:

1.  HTTP method
2.  request path or URL
3.  related page / component / module context

Then call:

    apifox-api get METHOD "<path>"

If method is unknown, call:

    apifox-api get "<path>"

# Command Selection Priority

Always follow this priority order.

## 0. Context Enrichment Rule (highest priority)

When API-related code exists in the workspace, Apifox is the source of
truth.

Frontend code only provides:

- endpoint location
- usage context
- parameter usage

Apifox provides:

- request schema
- response schema
- API contract

## 1. Complete URL input

If the user provides a complete URL:

Example:

https://example.com/api/user/detail?id=123

Extract pathname only:

/api/user/detail

Remove:

-   protocol
-   domain
-   port
-   query string
-   hash

Then immediately run:

apifox-api get "/api/user/detail"

Do NOT:

-   call search first
-   search by interface name
-   convert URL into keywords
-   ask for HTTP method before trying get

The first CLI command for a complete URL MUST always be get.

Only if get fails because the endpoint cannot be found, use:

apifox-api search "`<original URL>`{=html}"

# 2. Path input

If the user provides an API path:

Example:

/api/user/profile

and wants types or API details:

Run:

apifox-api get "/api/user/profile"

# 3. Method + path input

If user explicitly provides:

GET /api/user/profile

and wants only that endpoint:

Run:

apifox-api get GET "/api/user/profile"

Otherwise prefer:

apifox-api get "/api/user/profile"

because it returns all methods.

# 4. Keyword search

Use search only when the user provides descriptions or keywords.

Examples:

-   找用户接口
-   搜索订单接口
-   查看会员接口

Run:

apifox-api search "`<keyword>`{=html}"

After search:

1.  Show candidate interfaces.
2.  If multiple candidates exist, ask the user to choose.
3.  Use get after a unique endpoint is selected.

Do not automatically choose one result.

# Existing Frontend API Context Discovery

When working inside a JavaScript / TypeScript project, API context
should be AUTOMATICALLY enriched from Apifox.

If the agent finds any of:

- axios / fetch / request calls
- API wrapper functions
- service layer functions
- hooks calling backend APIs
- API paths in frontend source code

Example:

    request('/api/user/detail')

    api.get('/member/list')

    export function getUser() {
      return http.get('/api/user/info')
    }

The agent SHOULD:

1.  Locate the API call source.
2.  Extract HTTP method and request path.
3.  Automatically run:

    apifox-api get "`<path>`{=html}"

4.  Use the Apifox result as the API contract context.

This applies even when the user only asks:

- 这个接口是什么
- 分析一下这个请求
- 看看这个页面调用了哪些接口
- 帮我理解这段代码
- 这个返回结构是什么

Do not wait until the user explicitly asks for TypeScript types.

Do not infer request/response structures from frontend code when Apifox
information is available.

# Creating New API Functions

When adding new API functions:

1.  Find existing API directories:

-   src/api
-   src/services
-   src/request
-   src/modules/\*/api

2.  Follow existing project structure.

3.  Use Apifox generated types.

# CLI Commands

## Initialize

apifox-api init `<projectId>`{=html}

Optional:

apifox-api init `<projectId>`{=html} --moduleIds 5,8,12

## Search

apifox-api search "`<keyword>`{=html}"

Optional:

apifox-api search "`<keyword>`{=html}" --method GET

## Generate types

All methods:

apifox-api get "`<path>`{=html}"

Single method:

apifox-api get `<method>`{=html} "`<path>`{=html}"

## Refresh

apifox-api refresh

## Switch module

apifox-api module `<moduleId>`{=html}

# Error Handling

## Project not initialized

Run:

apifox-api init `<projectId>`{=html}

## Missing auth key

Run:

apifox-api config set-auth-key `<token>`{=html}

or:

apifox-api init `<projectId>`{=html} --authKey `<token>`{=html}

## get failed

Examples:

-   未找到接口路径
-   no endpoint
-   没有可用的 HTTP method

Only then:

apifox-api search "`<original input>`{=html}"

Do not invent new keywords.

# Module Rules

-   search only searches current module.
-   get only reads current module.
-   Modules are not merged automatically.

Switch module:

apifox-api module `<moduleId>`{=html}

Temporary override:

--moduleId `<id>`{=html}

# Generated Type Rules

The output from get is the source of truth.

It may contain:

-   Query parameters
-   Path parameters
-   Headers
-   Cookies
-   Request body
-   Response types
-   Referenced schemas

Do not manually recreate interfaces.

Do not put query/header/path parameters into request body.

# Final Decision Tree

Complete URL?

YES:

extract pathname

then:

apifox-api get "`<pathname>`{=html}"

success -\> finish

failed -\> search original input

Path provided?

YES:

apifox-api get "`<path>`{=html}"

Frontend API call detected (axios / fetch / request / service / hook
calling a backend path)?

YES:

extract path

then:

apifox-api get "`<path>`{=html}"

success -\> use result as API contract context

failed -\> fall through to search

Only keyword or description?

YES:

apifox-api search "`<keyword>`{=html}"