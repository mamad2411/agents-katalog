---
name: unit-test-go
description: Go 单元测试（UT）编写规范与落地清单（默认可被 `-run=TestUnit` 筛选），并提供基础测试、表驱动、结构体方法、并发、基准测试、错误处理 6 类可直接套用的测试模板。使用 gomonkey/gomock/testify 进行 mock 和断言，支持 table-driven test、benchmark test、concurrent test 等场景。
license: Complete terms in LICENSE.txt
---

## 禁止操作
- [ ] 修改非`_test.go`结尾文件

> **何时不生成测试**：对于纯数据结构（无逻辑的 getter/setter、只含字段赋值的 New 函数），不强制生成单元测试；测试收益低于维护成本时可跳过。

## 生成策略
- **质量优先**：生成的测试用例必须能编译通过并正确运行，不生成缺少依赖或无法执行的代码
- **完整覆盖**：覆盖正常路径、关键边界（空值/nil/越界等）和错误路径
- **场景独立**：每个子用例（t.Run）独立可运行，互不依赖执行顺序

## 单测代码规范
- **使用 testing 框架**：多场景时使用表驱动 + t.Run 划分子测试，每个子测试对应一个独立场景；**单一场景**（函数语义唯一，无需覆盖多组输入）可直接用 AAA 结构，不强制 t.Run。
- **必要的 import 语句**：包括 testing 包以及所有被测试函数和 mock 对象所需的包。
- **测试函数**：每个被测函数/方法对应一个测试函数（TestUnit_Foo），函数内通过表驱动组织多个测试用例。
- **测试逻辑**：在测试函数中，首先创建被测试函数所需的依赖（包括 mock 对象），然后调用被测试函数，最后使用断言来验证函数的行为是否符合预期。
- **测试函数命名**：见下方「工程约定 → 测试函数命名（核心）」
- **断言库**：统一使用 `github.com/stretchr/testify/assert`；断言失败后无法继续执行后续步骤时（如依赖数据未初始化），改用 `testify/require`（立即终止当前测试）。
- **测试文件包名**：与被测文件保持同包（`package foo`，非 `package foo_test`），确保可访问包内私有符号（gomonkey patch 私有方法依赖此设置）。

## Mock 生成规范

`//go:generate` 指令写在 interface 定义上方，与 interface 同文件；mock 生成到 `./mock/` 子目录，**禁止手写 mock**。

详细规范（mockgen 安装、go:generate 用法、路径对齐）见 `reference/mock-generation.md`。

## 工程约定

### 测试执行命令
> GOARCH=amd64 go test ./... -gcflags=all=-l -ldflags "-X google.golang.org/protobuf/reflect/protoregistry.conflictPolicy=warn" -run=TestUnit

> **必须携带参数**：
> - `-gcflags=all=-l`：禁用内联优化，gomonkey 通过修改机器码实现 patch，内联会导致 mock 失效
> - `-ldflags "-X google.golang.org/protobuf/reflect/protoregistry.conflictPolicy=warn"`：解决 protobuf 注册冲突

> `GOARCH=amd64`：gomonkey 依赖 x86/x64 指令集，在 ARM 架构（如 Apple M 芯片）下 mock 会失效，需指定 amd64 架构编译执行。

### 测试函数命名（核心）
- 测试函数必须以 `TestUnit` 开头（示例：`func TestUnit_Foo(t *testing.T)`）
- 若被测函数为 `func Foo(...)`：
  - 使用 `func TestUnit_Foo(t *testing.T)`（允许且仅允许在该位置使用下划线）
- 若被测方法为 `func (b *Bar) Foo(...)`：
  - 使用 `func TestUnitBar_Foo(t *testing.T)`
- 基准测试函数使用 `Benchmark` 前缀（如 `BenchmarkFoo`），豁免 `TestUnit` 前缀规则
- 以上规则之外，下划线**不得**出现在测试函数名的任何其他位置

### 行数与风格
- 测试文件：最多 **1600 行**
- 测试函数：最多 **160 行**
- 代码行长度：不超过 **120 列**
- 圈复杂度、列宽限制、`import` 分组等：与普通代码保持一致
- 单测文件中的函数通常不对外：可导出函数可以不写注释；结构体定义尽量不要导出

### 文件位置
```
demo/
├── service/
│   ├── policy/
│   │   ├── policy.go
│   │   └── policy_test.go      # 与源码同级目录，同包名
│   └── role/
│       ├── mock/
│       │    └── role_mock.go  # package roleMock
│       ├── role.go
│       └── role_test.go
└── infra/                       # 基础设施层
```

## 单测代码范例

遵循范例中的编码风格与测试模式，同时须满足本 skill 所有规范的要求。此范例是风格参考的首要来源，在风格选择上优先对齐范例；但本 skill 中的明确规范（命名、断言顺序、层级等）具有更高优先级。

### 范例剖析要点
生成新代码前，须从以下几个维度剖析范例中的关键模式并严格遵守：
- **初始化**：从范例中解析初始化方式，用相同的方式进行初始化和对象的实例化
- **mock 策略**：从范例中解析 mock 方式，若范例未对数据库操作 mock，新代码同样不 mock
- **断言风格**：从范例中解析断言方式（if/assert/require），新代码保持一致，不混用
- **context 传递**：从范例中解析 context 的使用方式（`trpc.BackgroundContext()` 或 `context.Background()`），新代码保持一致

### 范例文件引入规则
根据被测函数特点，引入对应 reference 文件：
- **基础测试**：适用于纯函数测试（无外部依赖、无需 mock）
  - 引入文件：`reference/basic-test.md`
- **表驱动测试**：适用于需要覆盖多组输入/输出场景的函数或方法
  - 引入文件：`reference/table-driven-test.md`
- **结构体方法测试**：适用于测试结构体的方法，支持 mock、stub 和接口测试
  - 适用场景：测试结构体的方法、需要使用 mock 或 stub、测试接口实现
  - 关键要点：创建 mock 实现依赖接口、使用依赖注入、验证方法的副作用
  - 引入文件：`reference/struct-method-test.md`
- **并发测试**：适用于测试并发安全性，使用 goroutine、sync 包等
  - 引入文件：`reference/concurrent-test.md`
- **基准测试**：适用于性能测试和优化，使用 `Benchmark` 函数
  - 引入文件：`reference/benchmark-test.md`
- **错误处理和断言**：适用于测试错误处理和断言
  - 引入文件：`reference/error-handling.md`

## 快速检查清单
- 测试函数名是否符合命名规则：普通函数 `TestUnit_Foo`，结构体方法 `TestUnitBar_Foo`，可被 `-run=TestUnit` 筛选
- 多场景时是否优先使用表驱动 `tests := []struct{...}{...}` 组织用例
- `t.Run` 中的 `tt.name` 是否**唯一且语义化**（不得出现重复的 `"test"` / `"normal"`）
- 每个 `t.Run` 内是否有**至少一条断言**（无断言等于无效测试）
- 函数返回的 error 是否均被处理（不得用 `_` 忽略 error）
- `assert.Equal` 参数顺序是否正确：`assert.Equal(t, want, got)`（expected 在前，actual 在后）
- 是否覆盖：正常路径 + 关键边界 + 错误路径（如除零、空值、越界等）
- （执行提示）执行 go test 是否携带完整参数：`-gcflags=all=-l` 和 `-ldflags "-X google.golang.org/protobuf/reflect/protoregistry.conflictPolicy=warn"`
- import 分组是否符合项目规范（必要时使用 `imports` skill 协助）
