---
name: security-app-fuzzing
canonical_id: security.app.fuzzing
aliases: [fuzzing, fuzz-testing, coverage-guided-fuzzing, structure-aware-fuzzing]
version: 1.0.0
status: stable
created_date: 2026-06-15
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
forbidden-tools: WebFetch
manual_gate_required: false
disable-model-invocation: false
standards_versions:
  - Trail of Bits Testing Handbook (appsec.guide/fuzzing): living reference, checked 2026-06-15
  - ClusterFuzzLite: v1 (pinned google/clusterfuzzlite/actions/*@v1)
  - OSS-Fuzz build conventions: living reference, checked 2026-06-15
  - OWASP ASVS: 5.0 (V5 Input Validation / V11 Cryptography overlap)
  - OWASP Top 10 for Agentic Applications (ASI01-ASI10): 2025-12 (tool-boundary fuzzing)
  - NIST CSF: 2.0 (ID.RA risk identification via fuzz-found defects)
sensitive_data_rules:
  never_read: [".env*", "secrets/**", "*.pem", "*.key", "corpus/**/raw_pii/**"]
  never_write: ["actual crashing inputs containing user PII to chat/log", "real API keys into fuzz harness configs"]
  redact_on_output: ["crash reproducers containing PII / secrets", "stack traces leaking internal paths beyond the bug location"]
upstream:
  - appsec-security-orchestrator
  - security-governance-threat-modeling   # parser / deserializer / upload abuse cases drive harness targets
  - security-app-llm                       # agent tool-boundary surface to fuzz
  - security-app-file-upload               # upload parser boundaries to fuzz
downstream:
  - security-remediation                   # crash-confirmed defect → fix → regression
  - security-app-sast-deep                 # crash points fed back as taint sink hypotheses
  - appsec-security-orchestrator           # back with findings
description: >-
  Coverage-guided and structure-aware fuzzing of code the project OWNS, wrapping per-language CLIs (libFuzzer / AFL++ / cargo-fuzz / Atheris / Jazzer / fast-check) plus ClusterFuzzLite in CI. Covers parsers, deserializers, crypto boundaries and AI-agent tool boundaries. Defensive only - never an attack tool or network scanner, no DoS, no exploitation.
trigger_phrases:
  - fuzzing / fuzz test / fuzz testing / 模糊测试
  - libFuzzer / AFL++ / cargo-fuzz / Atheris / Jazzer / ClusterFuzzLite
  - coverage-guided fuzzing / structure-aware fuzzing / 覆盖引导 / 结构化模糊
  - fuzz the parser / fuzz the deserializer / fuzz the decoder
  - fuzz agent tool boundary / fuzz tool arguments / agent input fuzzing / 工具边界模糊
  - corpus / seed corpus / crash reproducer / fuzz harness
---

# Security App — Fuzzing

## 1. Mission

现有 22 个 AppSec skill 静态审、威胁建模、SCA 都强，但**没有一个动态 fuzzing 能力**。Fuzzing 是用海量 mutated 输入去**自动发现**人写不出来的边界 case：parser crash、deserializer RCE、整数溢出、内存破坏、解析死循环、未捕获异常导致 DoS。本 skill 把 fuzzing 从"听说过"变成"每个边界 target 都能上 harness + 进 CI"。

**主战场（本 harness 优先级）**：根据 user 画像，AI Agent 部署/植入是大头。Agent 的 **tool boundary** 是新型攻击面——tool-argument schema、structured-output 解析、agent 间消息——这些都是"接收不可信结构化输入并解析/执行"的边界，正是 fuzzing 的菜（见 §7）。

**职责边界**：
- **owns**: fuzz harness 编写指导 + per-language CLI 包装 + corpus/CI 接法 + crash triage → §9 finding
- **handoff to**: `security-remediation`（crash → fix → 回归）；`security-app-sast-deep`（crash 点回喂做 taint sink）；`security-app-llm`（agent tool 语义边界设计）；`security-app-file-upload`（upload 策略层）
- **不做**: 不是 attack 工具、不扫网络、不打未授权目标；不做 active pentest（那是 `authorized-pentest-validation` 的硬门）；不替代 unit test（fuzzing 是补充，不是替代）

---

## 2. Activation Triggers

| Trigger | Action |
|---|---|
| 项目含 parser / decoder / deserializer（JSON/XML/protobuf/自定义二进制/markdown/模板）| 默认激活：结构化 fuzz harness |
| 项目含 file upload / 媒体处理 / 压缩解压 | 激活 + 与 `security-app-file-upload` 串联（parser hardening 的动态验证）|
| 项目含 crypto 边界（自实现 / wrapper / 签名验证 / 编解码）| 激活 crypto fuzz harness（差分 fuzz + 边界）|
| 项目是 **AI agent / 有 tool calling / structured output / 多 agent 消息** | **激活 agent-boundary fuzzing**（§7，主战场）|
| 项目有原生扩展（C/C++/Rust native module、Python C-ext、JNI）| 激活内存安全 fuzz（sanitizer 必开）|
| 高危模块上线前 / 接手陌生 parser 库 | 激活，先跑 corpus 短时 fuzz 找 low-hanging crash |
| CI 已有 GitHub Actions 且要持续 fuzz | 激活 ClusterFuzzLite CI 接法（§8）|

**判断规则**：fuzzing 的价值集中在"**接收不可信输入 + 有解析/状态/内存操作**"的边界。纯 CRUD / 纯展示无需 fuzz。先按本表判断 target，再写 harness——不要无差别全项目 fuzz。

---

## 3. 何时 fuzz（target 选择 —— 先于写 harness）

Fuzzing 不是"对整个项目跑"，是"对**值得的边界**写 harness"。优先级排序：

1. **Parser / deserializer**（最高价值）：任何把 bytes/string 变成结构的代码。历史上 fuzz 找到的绝大多数 RCE/DoS 在这里。JSON/XML/YAML/protobuf/CBOR/MessagePack/自定义协议/模板引擎/markdown/正则。
2. **不可信输入入口**：HTTP body 解析、query param 解析、cookie/header 解析、webhook payload、上传文件头解析。
3. **Crypto 边界**：签名验证、token 解析（JWT/PASETO）、编解码（base64/hex/ASN.1/DER）、自实现或 wrapper 的加密原语 —— 差分 fuzz（与参考实现对比）尤其有效。
4. **AI agent tool boundary**（本 harness 主战场，§7）：tool-argument 反序列化、structured-output（JSON mode）解析、agent 间消息解析、检索内容→prompt 的组装边界。
5. **状态机 / 协议实现**：WebSocket frame 解析、自定义 RPC、流式解析器（部分输入 + 增量喂入）。
6. **原生代码 / FFI**：C/C++/Rust unsafe、Python/Node 原生扩展 —— 内存破坏只有这里才有，**sanitizer 必开**。

**反向：什么不值得写 fuzz harness** —— 纯 ORM CRUD、纯静态页面渲染、配置读取（除非配置本身是不可信输入）、已被成熟库（如标准库 `json`）覆盖且你不加工的解析。

---

## 4. Fuzzing 的两种形态

| 形态 | 是什么 | 何时用 |
|---|---|---|
| **Coverage-guided（覆盖引导）** | fuzzer 用代码覆盖反馈引导 mutation（libFuzzer/AFL++/cargo-fuzz/Atheris/Jazzer 都是）。给一段 `bytes`，越走到新代码路径的输入越被保留繁殖 | 默认形态。适合 parser / 二进制解析 / 任意 `bytes → 行为` |
| **Structure-aware（结构化）** | 不是喂 raw bytes，而是喂**符合语法的结构**（protobuf/自定义 grammar/typed input），fuzzer 在结构层 mutate。避免 99% 输入卡在第一层格式校验 | 当输入有强结构（JSON schema / protobuf / 类型化 API / tool-argument schema）时。**agent tool boundary 几乎总是结构化**（§7）|

**经验法则**：输入是"裸 bytes / 文件"→ coverage-guided 直接上；输入是"结构化对象（必须先过 schema 才到逻辑）"→ structure-aware（否则 fuzzer 把时间浪费在生成无效 JSON 上）。两者可叠加：structure-aware 生成合法骨架 + coverage 引导填充。

---

## 5. Per-Language CLI 包装（CLI-first；不假设已装）

> 全部是 **defensive、跑在你自己的 target 上**。安装命令附上——**不假设环境已装**；跨平台（Windows 多数 fuzzer 需 WSL2/Linux container，下方标注）。

### 5.1 C / C++ — libFuzzer / AFL++

```bash
# libFuzzer（随 clang 内置；Linux/macOS；Windows 用 WSL2）
clang++ -g -O1 -fsanitize=fuzzer,address,undefined harness.cc target.cc -o fuzz_target
./fuzz_target corpus/ -max_total_time=300 -print_final_stats=1

# AFL++（apt install afl++ / brew install afl++ / Docker: aflplusplus/aflplusplus）
afl-clang-fast++ -fsanitize=address harness.cc target.cc -o fuzz_target
afl-fuzz -i corpus/ -o findings/ -- ./fuzz_target @@
```

Harness 入口固定签名（libFuzzer 约定，ClusterFuzzLite 也认它）：
```c
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size) {
    parse_thing(data, size);   // 把不可信输入喂给被测边界；崩了 = bug
    return 0;
}
```

### 5.2 Rust — cargo-fuzz（libFuzzer 后端）

```bash
cargo install cargo-fuzz                  # 需 nightly toolchain
cargo fuzz init                           # 建 fuzz/ 目录
cargo fuzz add parse_target
cargo fuzz run parse_target -- -max_total_time=300
```
```rust
// fuzz/fuzz_targets/parse_target.rs
#![no_main]
use libfuzzer_sys::fuzz_target;
fuzz_target!(|data: &[u8]| {
    let _ = my_crate::parse(data);        // panic / OOM / timeout = finding
});
// structure-aware: fuzz_target!(|input: MyTypedInput| { ... }) with arbitrary::Arbitrary
```

### 5.3 Python — Atheris（含 native ext 内存安全）

```bash
pip install atheris                        # native ext fuzz 需 clang；纯 py 不需 LD_PRELOAD
```
```python
import atheris, sys
with atheris.instrument_imports():
    import my_module
def TestOneInput(data):
    fdp = atheris.FuzzedDataProvider(data)
    try:
        my_module.parse(fdp.ConsumeUnicodeNoSurrogates(sys.maxsize))
    except (ValueError, KeyError):
        pass                               # 已知良性异常吞掉；未预期异常 = finding
atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()
```
> Python 还可用 **Hypothesis**（property-based）当 harness 写法，与 QA 的 property/generative（4-qa.md Q5）共用——`hypothesis write <module>` 生成起手 harness。

### 5.4 JVM (Java/Kotlin) — Jazzer

```bash
# Jazzer：下载 release jar 或 Docker cifuzz/jazzer；Maven/Gradle 插件亦可
java -cp jazzer_standalone.jar:target/classes \
  com.code_intelligence.jazzer.Jazzer --target_class=ParseFuzzer
```
```java
import com.code_intelligence.jazzer.api.FuzzedDataProvider;
public class ParseFuzzer {
  public static void fuzzerTestOneInput(FuzzedDataProvider data) {
    MyParser.parse(data.consumeRemainingAsString());   // uncaught exception / OOM = finding
  }
}
```

### 5.5 Go — 原生 fuzzing（go test，无需外部工具）

```bash
go test -fuzz=FuzzParse -fuzztime=300s ./pkg/...
```
```go
func FuzzParse(f *testing.F) {
    f.Add([]byte(`{"seed":1}`))                  // seed corpus
    f.Fuzz(func(t *testing.T, data []byte) {
        _, _ = mypkg.Parse(data)                 // panic = finding；go 自动记录复现 corpus
    })
}
```

### 5.6 JavaScript / TypeScript — fast-check（structure-aware property fuzz）

```bash
npm i -D fast-check                              # 跨平台，纯 JS，无需 Linux
```
```ts
import fc from 'fast-check';
// structure-aware：让 fast-check 按 schema 生成 tool-argument，喂给解析/校验边界
fc.assert(fc.property(fc.object(), (input) => {
  const r = parseToolArgs(input);                // 抛未预期异常 / 违反不变量 = finding
  expect(r).toSatisfy(invariant);
}), { numRuns: 5000 });
```
> JS 还可用 **Jazzer.js**（`@jazzer.js/core`）做 coverage-guided fuzz（Node native）。fast-check 优势是与 vitest/jest 同栈、无 Linux 依赖、最适合 agent tool-argument 这类结构化输入。

---

## 6. 写一个好 harness 的纪律

1. **每个 harness 只测一个边界**：一个 parser 一个 harness。混在一起 = 覆盖反馈互相干扰。
2. **被测函数必须确定性**：同一输入同一行为。harness 内不要打网络、不要读时间/随机（否则 crash 不可复现）。
3. **吞掉已知良性异常，放过未预期的**：`ValueError`/`KeyError` 之类预期拒绝吞掉；段错误/OOM/未捕获异常/断言失败/超时 = 真 finding。
4. **加 invariant / 差分校验放大信号**：不只看"崩没崩"，还可断言往返不变（`decode(encode(x)) == x`）、与参考实现一致（crypto 差分 fuzz）、输出永不越界。
5. **种子 corpus 要真实**：用真实样本 + 边界样本（空、超长、嵌套深、非法 UTF-8）做 seed corpus。好种子 = 快速进入深层路径。
6. **sanitizer 必开（native）**：C/C++/Rust/native-ext 一律 `-fsanitize=address,undefined`。没 sanitizer 的内存破坏 fuzz 等于瞎跑。
7. **资源上限防自伤**：harness 设 timeout / rss_limit，防 fuzz 把本机吃爆（`-timeout=25 -rss_limit_mb=2048`）。
8. **结构化输入用 structure-aware**：见 §4——别让 fuzzer 把预算烧在生成无效格式上。

---

## 7. AI-Agent Tool-Boundary Fuzzing（主战场）

> 这是本 harness 相对通用 fuzzing 的**重点扩展**。Agent 系统把"不可信结构化输入"送进解析/调度/执行，是高价值 fuzz 边界。与 `security-app-llm` 互补：那边设计 tool-permission/语义边界；这边用 fuzzing **动态压**这些边界的解析与校验层。

### 7.1 该 fuzz 的 agent 边界

| 边界 | 不可信输入 | fuzz 什么 |
|---|---|---|
| **Tool-argument 反序列化** | LLM 产出的 tool-call args（JSON）| schema 校验是否真挡住非法/越界/类型混淆 args；解析器是否对畸形 JSON 崩溃/挂起 |
| **Structured-output 解析** | LLM JSON-mode / function-call 输出 | 应用解析 LLM 输出的代码——LLM 会产出畸形/截断/嵌套爆炸 JSON，解析层必须不崩 |
| **Inter-agent 消息** | 其它 agent 发来的 message（ASI07）| 消息解析 + 完整性校验；不可信 agent 消息能否触发解析异常或注入 |
| **检索内容 → prompt 组装** | RAG 取回的文档片段 | 组装边界对超长/特殊字符/嵌套分隔符是否健壮（结合 indirect prompt injection） |
| **Tool-result → context 回填** | tool 返回值（可能来自外部 API）| 回填解析对畸形/超大 tool result 是否健壮 |

### 7.2 怎么 fuzz（structure-aware 为主）

```ts
// 例：fuzz 一个 agent 的 tool-argument 校验+解析边界（fast-check structure-aware）
import fc from 'fast-check';

const toolArgArb = fc.record({
  path: fc.oneof(fc.string(), fc.constant('../../etc/passwd'), fc.string({ minLength: 5000 })),
  count: fc.oneof(fc.integer(), fc.double(), fc.constant(Number.MAX_SAFE_INTEGER), fc.constant(-1)),
  flags: fc.array(fc.string(), { maxLength: 1000 }),
});

fc.assert(fc.property(toolArgArb, (rawArgs) => {
  // 被测：应用侧 tool-arg 校验 + 反序列化（不真正执行 tool 的副作用！）
  const result = validateAndParseToolArgs('readFile', rawArgs);
  // 不变量：要么 reject（合法拒绝），要么产出已 sanitize 的安全 args；绝不抛未捕获异常、绝不放过 path traversal
  if (result.ok) {
    expect(result.args.path).not.toContain('..');     // traversal 必须被挡
    expect(result.args.count).toBeGreaterThanOrEqual(0);
  }
}), { numRuns: 10000 });
```

> **运行时依赖（copy-run 注意）**：上例的 `expect(...)` 来自测试框架（vitest / jest），需在 `*.test.ts` 里经测试 runner（`npx vitest run` / `npx jest`）跑。**裸 `node harness.ts` 会 `expect is not defined`**。无测试框架时把断言换成纯 node：`if (result.args.path.includes('..')) throw new Error('TRAVERSAL_SLIPPED');` + `import assert from 'node:assert'`（`assert(result.args.count >= 0)`），即可 `node`/`tsx` 直跑。

**铁律（agent fuzz 安全）**：
- fuzz **校验/解析层**，**不要**让 harness 真触发 tool 的副作用（不真删文件、不真发请求、不真转账）。被测对象是"args 校验 + 反序列化 + 调度决策"，副作用执行 stub 掉。
- 用 **structure-aware**：tool-arg 几乎总有 schema，裸 bytes fuzz 会卡在 JSON 解析层。
- 把"危险值"塞进 generator：path traversal、超大数、负数、Unicode 同形字、超长字符串、深层嵌套、null/undefined、type 混淆——这些是 agent 边界真实的攻击输入。
- crash / invariant 违反 → §9 finding，`source: manual_review`（harness 是人写的）或与 `security-app-llm` 协同标 ASI02（Tool Misuse）/ ASI07（inter-agent comm）。

---

## 8. ClusterFuzzLite — CI 持续 fuzz（config 驱动，pinned action）

> ClusterFuzzLite = OSS-Fuzz 的 CI-first 轻量版。**config 驱动**：放几个 `.github/workflows/cflite_*.yml` + 一个 `.clusterfuzzlite/` 构建目录即可。action 固定 pin 到 `@v1`。

### 8.1 PR fuzzing（最小集 — 只 fuzz 受 PR 影响的 target）

`.github/workflows/cflite_pr.yml`：
```yaml
name: ClusterFuzzLite PR fuzzing
on:
  pull_request:
    paths: ['**']
permissions: read-all          # 最小权限
jobs:
  PR:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        sanitizer: [address]   # 按需加 undefined / memory
    steps:
    - name: Build Fuzzers
      uses: google/clusterfuzzlite/actions/build_fuzzers@v1   # pin @v1
      with:
        language: c++          # 改成你的语言：c++/rust/python/jvm/go
        github-token: ${{ secrets.GITHUB_TOKEN }}
        sanitizer: ${{ matrix.sanitizer }}
    - name: Run Fuzzers
      uses: google/clusterfuzzlite/actions/run_fuzzers@v1     # pin @v1
      with:
        github-token: ${{ secrets.GITHUB_TOKEN }}
        fuzz-seconds: 600
        mode: 'code-change'    # 只 fuzz PR 改动影响的 target，快
        sanitizer: ${{ matrix.sanitizer }}
        output-sarif: true     # 产 SARIF → 可进 code scanning / 喂 §9 triage
```

### 8.2 batch + cron（持续累积 corpus + pruning + coverage）

- `.github/workflows/cflite_batch.yml`：`mode: 'batch'`，cron 定时（如每 6 小时），让 corpus 随时间长大。
- `.github/workflows/cflite_cron.yml`：`mode: 'prune'`（去冗余、保覆盖）+ `mode: 'coverage'`（出覆盖报告）。
- **跑了 batch 必须配 prune**（否则 corpus 无限膨胀）。
- 大 build 慎开 continuous build（吃 GitHub Actions 配额，docs 明确警告）。

### 8.3 `.clusterfuzzlite/` 构建目录

每语言放 `Dockerfile` + `build.sh`（把 harness 编译进 `$OUT`）+ `project.yaml`（`language:` 字段）。Python 用 `FROM gcr.io/oss-fuzz-base/base-builder-python`；纯 py harness 去掉 `LD_PRELOAD`（docs 注明，否则误触 sanitizer 启动崩溃）。

### 8.4 本地短跑（不进 CI 也能用）

CI 之外，§5 的每语言 CLI 都能本地直接跑（`-max_total_time=300` 短时找 low-hanging crash）。接手陌生 parser 库时，先本地短 fuzz 一轮再决定要不要进 CI。

---

## 9. Crash Triage → §9 Finding

Fuzzer 报 crash 不等于"安全漏洞"。triage 流程：

1. **复现**：用 fuzzer 吐出的 reproducer input 跑一次确认稳定复现（不稳定 = harness 非确定性，先修 harness）。
2. **最小化**：libFuzzer `-minimize_crash=1` / `cargo fuzz tmin` / Go 自动最小化 —— 拿到最小复现。
3. **分类崩溃类型**：
   - 内存破坏（heap-overflow / use-after-free / OOB，sanitizer 报）→ **critical/high**，可能 RCE。
   - 未捕获异常 / panic → DoS 风险（medium/high，看是否可远程触发）。
   - 死循环 / timeout / OOM → DoS（medium/high）。
   - 逻辑不变量违反（差分 fuzz）→ correctness/security 看场景。
4. **判可达性 + 可利用性**：crash 的输入路径在生产里是否真能被不可信输入触达？（不可达 → 降级，但记录。可联动 `security-app-sast-deep` 做 taint 确认。）
5. **脱敏**：reproducer / stack trace 若含 PII / secret / 内部路径，**先 `appsec-sdk redact`**，绝不把 raw crashing input 贴进 chat / log / finding。

---

## 10. Hard Rules

- ❌ **不**把 fuzzing 当 attack 工具——只 fuzz **你自己拥有/被授权**的 target；不扫网络、不打第三方服务
- ❌ **不**在 agent fuzz harness 里真触发 tool 副作用（删文件/发请求/转账）——副作用 stub，只 fuzz 校验+解析层
- ❌ **不**跑无 sanitizer 的 native fuzz（C/C++/Rust/native-ext 必开 `-fsanitize=address,undefined`）
- ❌ **不**写非确定性 harness（打网络/读时间/读随机 → crash 不可复现）
- ❌ **不**把 raw crashing input / stack trace（含 PII/secret/内部路径）贴进 chat / log / report——先 `appsec-sdk redact`
- ❌ **不**用浮动 tag 引 ClusterFuzzLite action——pin 到 `@v1`（供应链纪律，与 supply-chain skill 一致）
- ❌ **不**把"跑了 fuzz 没崩"当"该边界安全"——fuzz 是补充信号，覆盖率/时长不够时是弱证据
- ❌ **不**对结构化输入用裸 bytes fuzz（预算全卡在格式层 → 用 structure-aware）
- ❌ **不**让 batch fuzzing 没有配套 prune（corpus 无限膨胀烧配额/磁盘）
- ❌ **不**替代 unit test / 不替代 active pentest（那是 `authorized-pentest-validation` 硬门，本 skill 不碰）

---

## 11. Anti-patterns

- ❌ "对整个项目跑 fuzz" —— fuzz 是按边界写 harness，不是无差别全量；先按 §3 选 target
- ❌ "fuzz 一晚上没崩就是安全了" —— 覆盖率没测、时长不够、harness 太浅都会假阴；要看 coverage + 边界是否真被打到
- ❌ "agent 用的是大厂模型，tool 边界不用 fuzz" —— LLM 必然产畸形/截断/嵌套爆炸输出，你的**解析层**才是被测对象
- ❌ "tool-arg 校验过了 schema 就安全" —— schema 通过不代表语义安全（path traversal 是合法 string），要 fuzz + invariant 双查
- ❌ "结构化输入直接喂 raw bytes fuzzer" —— 99% 输入卡在第一层解析，深层逻辑根本没被打到
- ❌ "native 代码不开 sanitizer 也能 fuzz" —— 内存破坏静默发生，不开 sanitizer 等于看不见
- ❌ "crash 就是漏洞" —— 要 triage：可达性 + 可利用性 + 崩溃类型，不可达的良性 panic ≠ 安全漏洞
- ❌ "harness 里直接调真 tool 看会不会出事" —— 危险且不可复现；副作用必须 stub
- ❌ "ClusterFuzzLite action 用 @latest" —— 第三方 action 必须 SHA/版本 pin，否则供应链门户大开

---

## 12. Output Contract

每次 fuzzing engagement 产出：

1. **Fuzz target inventory**：按 §3 选出的边界清单（per-target：语言 / 形态 coverage-vs-structure / 不可信输入来源）
2. **Harness 清单**：每个 target 的 harness 文件路径 + 入口签名 + invariant（如有）
3. **Corpus 状态**：seed corpus 来源 + 大小 + （CI 场景）storage repo / artifact 位置
4. **Run evidence**：每次 run 的 stats（执行次数 / 覆盖 / 时长 / 是否 crash），CI 场景附 SARIF 路径
5. **Crash triage 表**：每个 crash 的复现状态 / 最小化输入引用（脱敏）/ 崩溃类型 / 可达性 / 可利用性判定
6. **Findings** —— crash-confirmed 缺陷全部经 `appsec-sdk finding.add <file>`（canonical path，redact-first）落 `.appsec/findings/<tag>/`，符合 orchestrator §9 finding schema v1.0：
   - `source`：`manual_review`（harness 人写）；不发明新 enum 值（PreToolUse prewrite hook 拒 schema 漂移）
   - `detector`：fuzzer 名 + 版本（如 `libfuzzer@clang-18` / `cargo-fuzz@0.x` / `atheris@2.x` / `jazzer@0.x` / `go-test-fuzz@1.x` / `fast-check@3.x`）
   - `severity` **小写**（critical/high/medium/low）；内存破坏类倾向 high+，纯 DoS 看可远程触发性
   - `cwe`：按崩溃类型（CWE-787 OOB write / CWE-416 UAF / CWE-400 uncontrolled resource / CWE-502 deserialization / CWE-674 uncontrolled recursion 等）
   - `asvs_mapping`：versioned `v5.0.0-<ch>.<sec>.<req>`（input-validation 用 V5；crypto 边界用 V11；正则 `^v5\.0\.0-\d+\.\d+\.\d+$`）。无诚实映射时留空 `[]` + 写 `unmapped_reason`，**禁止编造**
   - `reproduction_steps`：**禁含 raw crashing input / raw secret / PII**——引用脱敏后的最小复现文件路径
   - **绝不** Write 直写 `.appsec/findings/**`（orchestrator hook §18.5 物理拦截）；只走 sdk
   - 内存破坏 / 可远程 DoS → `security-remediation`（fix → 回归 fuzz 验证 crash 不再复现）；crash 点 → `security-app-sast-deep` 做 taint sink 确认
7. SECURITY.md 追加 Fuzzing 小节 + AppSec Release Evidence 引用（fuzz 是 §5 SAST 的动态补充信号；evidence 归 `.appsec/evidence/<tag>/fuzz/`）

---

## 13. References

- [Trail of Bits Testing Handbook — Fuzzing](https://appsec.guide/docs/fuzzing/) — per-language playbook（libFuzzer/AFL++/cargo-fuzz/Atheris/Jazzer）
- [ClusterFuzzLite](https://google.github.io/clusterfuzzlite/) — CI-first fuzzing（本仓库 staged: `staging/cloned-repos/clusterfuzzlite/`）
- [libFuzzer](https://llvm.org/docs/LibFuzzer.html) / [AFL++](https://aflplus.plus/)
- [cargo-fuzz](https://github.com/rust-fuzz/cargo-fuzz) / [Rust Fuzz Book](https://rust-fuzz.github.io/book/)
- [Atheris (Python)](https://github.com/google/atheris) / [Hypothesis (property-based)](https://hypothesis.readthedocs.io/)
- [Jazzer (JVM)](https://github.com/CodeIntelligenceTesting/jazzer) / [Jazzer.js](https://github.com/CodeIntelligenceTesting/jazzer.js)
- [Go native fuzzing](https://go.dev/security/fuzz/) / [fast-check (JS/TS)](https://fast-check.dev/)
- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/) — agent tool-boundary threat context
- [appsec-security-orchestrator](../appsec-security-orchestrator/SKILL.md) — §9 finding schema / §18.5 finding-path hook
- [security-app-llm](../security-app-llm/SKILL.md) — agent tool-permission / semantic boundary design (upstream)
- [security-app-file-upload](../security-app-file-upload/SKILL.md) — upload parser boundaries (sibling)
- [security-app-sast-deep](../security-app-sast-deep/SKILL.md) — taint confirmation of fuzz crash reachability (downstream)
- [security-remediation](../security-remediation/SKILL.md) — crash → fix → regression
