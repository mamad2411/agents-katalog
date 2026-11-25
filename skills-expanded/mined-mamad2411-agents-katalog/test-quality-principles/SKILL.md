---
name: test-quality-principles
description: |
  测试质量原则。写测试前必须读被测代码的真实实现，确保测试验证的是正确行为而非复刻 Bug。
  四条铁律：先读实现再写测试 / 测行为不测实现 / 失败路径必测 / Mock 依赖不 Mock 被测对象。
  触发词：写测试、单元测试、测试用例、测试覆盖、pytest、jest、vitest、测试规范、测试质量、测试原则、
  unit test、write test、test quality、test principle、mocking、test coverage。
---

# 测试质量原则 — Test Quality Principles

> 写测试前必须读被测代码的真实实现，确保测试验证的是正确行为，而非复刻 Bug。

## 触发条件

编写新测试、修改现有测试、审查测试代码时自动适用。

## 四条铁律

### 1. 先读实现再写测试

测试断言必须与代码的**真实设计意图**对齐，不能仅匹配当前输出。

**❌ 错误示范**（测试跟着 Bug 一起写错了）：

```python
# field_maps.py 中 title 被错误放在 desc 前面
"content": {"candidates": ["title", "question_title", "desc", "content"]}

# 测试断言了 Bug 行为
assert standard["content"] == raw["title"]   # Bug！
```

**✅ 正确做法**：先确认 `desc` 才是正文字段，再写：

```python
assert standard["content"] == raw["desc"]     # 正确！
```

**验证方法**：读被测函数的调用链——数据从哪里来？字段名在上下游叫什么？不只看函数签名。

---

### 2. 测行为不测实现

测试验证 **"做了什么"**（调了 commit、派发了任务），不验证 **"怎么做的"**（调了 flush、用了 async）。

**❌ 错误**：测内部实现细节

```python
# Python
mock_db.flush.assert_called()   # 脆弱，换 ORM 就挂

# JavaScript
expect(container.querySelector('.spinner')).toBeNull()  # 脆弱，换 UI 库就挂
```

**✅ 正确**：测外部可观察行为

```python
# Python
mock_db.commit.assert_awaited_once()   # 验证事务提交

# JavaScript
expect(mockTaskApi.start).toHaveBeenCalledWith(99)  # 验证爬虫被派发

# 任何语言
expect(response.status).toBe(200)                   # 验证接口返回状态
expect(db.query("SELECT COUNT(*) FROM orders").one()[0]).toBe(3)  # 验证数据结果
```

---

### 3. 失败路径必测

正常路径测试再多也防不住异常分支。**每个 `if/except/return None` 分支至少一个测试。**

| 必须覆盖的失败场景 | 示例 |
|---|---|
| 依赖返回 None/空 | Repository 查不到记录 → 方法正确 fallback |
| 外部调用抛异常 | API 调用失败 → 不崩溃，返回错误信息 |
| 输入为边界值 | 空列表、超长字符串、null、undefined |
| 事务异常回滚 | 写入失败 → rollback 被调用 |
| 权限不足 | 未认证用户访问需权限接口 → 403 |

**验证方法**：数被测函数的 `if/except/return None/raise` 分支，每个分支至少一个测试。

**对称场景全覆盖**：修复一个影响多个对称方向的 bug 后，**每个方向都要单独写测试**，不要只测一个方向就认为全修好了。

```text
错误路径：
  修复了大小写匹配 bug（影响 top/bottom/left/right 四个方向）
  → 只写了"纵向缩放生效"的测试
  → 横向没测
  → 横向其实坏了，但本地测试全过
  → 用户实测才发现

正确路径：
  修复后，bottomRight 的横向、bottomRight 的纵向、
  topLeft 的横向、topLeft 的纵向，各写一个测试
  → 本地就能抓到"横向没修好"
  → 不用转嫁验证成本给用户
```

> 这适用于所有对称场景：CRUD 四操作、文件导入/导出、编码/解码、序列化/反序列化、push/pop、展开/折叠等。

---

### 4. Mock 依赖，不 Mock 被测对象

测试的目标是验证被测代码，不是验证 Mock 框架。

| 被测层 | Mock 这一层 | 不 Mock |
|--------|-----------|---------|
| Service / UseCase | Repository、外部 API、外部 Service | Service 自身的方法 |
| API 端点 / Controller | Service | 端点自身的处理函数 |
| 前端组件 | API 模块、Store、路由 | 组件自身的逻辑方法 |

**❌ 错误**：

```python
# Python —— Mock 了被测方法本身，什么都没测
svc.import_cookie = AsyncMock()

# JavaScript —— Mock 了组件自己的方法
wrapper.vm.handleSubmit = jest.fn()
```

**✅ 正确**：

```python
# Python —— Mock 依赖的 Repository
svc.cookie_repository.upsert_cookie = AsyncMock()
result = await svc.import_cookie("zhihu", "test", 1)  # 测真实方法

# JavaScript —— Mock 依赖的 API 模块
mockApi.createOrder.mockResolvedValue({ id: 1 })
result = await service.submitOrder({ items: [] })     # 测真实方法
```

---

## 检查清单（写测试前逐项确认）

- [ ] 我读了被测函数及其全部调用链的代码
- [ ] 我确认了输入数据的真实字段名和类型（不是猜测）
- [ ] 我覆盖了正常路径 + 至少 2 个失败/边界路径 + 对称场景全方向
- [ ] 我 Mock 的是依赖，不是被测对象本身
- [ ] 我的断言验证的是可观察行为，不是内部实现
- [ ] 我跑过测试覆盖检查，确认新增行被覆盖且无 side effect
