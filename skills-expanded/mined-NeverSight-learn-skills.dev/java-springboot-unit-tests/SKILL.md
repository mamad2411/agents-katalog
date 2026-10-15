---
name: java-springboot-unit-tests
description: 为 Java Spring Boot 项目自动生成单元测试。使用 JUnit 5 与 Mockito，覆盖 Controller、Service 及工具类。当用户需要为 Spring Boot 类编写单元测试、生成测试用例、补充测试覆盖，或提到“写测试”“单元测试”“单测”时使用。
---

# Java Spring Boot 单元测试

为 Spring Boot 项目生成符合惯例的单元测试，使用 JUnit 5 和 Mockito，测试文件放在 `src/test/java` 并镜像主代码包结构。

## 工作流

生成单元测试时按此清单执行：

```
任务进度：
- [ ] 步骤 1：确认被测类及依赖（Controller/Service/工具类）
- [ ] 步骤 2：确定测试策略（纯单元 / 需 Spring 上下文）
- [ ] 步骤 3：创建测试类，放置于 src/test/java 对应包下
- [ ] 步骤 4：编写用例（正常路径、边界、异常）
- [ ] 步骤 5：运行 mvn test 验证
```

**步骤 1–2**：阅读被测类，识别依赖（`@Autowired` 构造注入、接口、外部调用）。Controller 用 `@WebMvcTest` 或 MockMvc 单测；Service 用 `@ExtendWith(MockitoExtension.class)` + `@Mock` 依赖，不启动完整 Spring 容器。

**步骤 3**：测试类路径与主类一致，仅根目录由 `src/main/java` 换为 `src/test/java`。类名：`被测类名 + Test`（如 `RagController` → `RagControllerTest`）。

**步骤 4**：见下方「测试类型与模板」。

**步骤 5**：在项目根目录执行 `mvn test -Dtest=被测类名Test` 验证。

---

## 技术约定

| 用途       | 技术选型 |
|------------|----------|
| 测试框架   | JUnit 5（`org.junit.jupiter.api.*`） |
| Mock       | Mockito（`org.mockito.*`） |
| Service 单测 | `@ExtendWith(MockitoExtension.class)`，依赖用 `@Mock`，被测类用 `@InjectMocks` |
| Controller 单测 | `@WebMvcTest(被测Controller.class)`，依赖用 `@MockBean`，使用 `MockMvc` 发请求 |
| 断言       | AssertJ（`org.assertj.core.api.Assertions`）或 JUnit `Assertions`，二者择一保持一致 |

- 不启动完整应用时，优先 `MockitoExtension` + Mock，避免 `@SpringBootTest`。
- 需要验证 HTTP 层时再用 `@WebMvcTest` + `MockMvc`。

---

## 测试类型与模板

### Service 单元测试

- 使用 `@ExtendWith(MockitoExtension.class)`。
- 所有依赖以 `@Mock` 注入，被测 Service 用 `@InjectMocks`。
- 用例：正常返回值、异常、边界（空列表、null 等）。
- 使用 `when(...).thenReturn(...)` / `thenThrow(...)` 规定依赖行为；用 `verify(mock, times(n)).method(...)` 校验调用次数。

```java
package com.example.springai.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class RagServiceTest {

    @Mock
    private SomeDependency someDependency;

    @InjectMocks
    private RagService ragService;

    @BeforeEach
    void setUp() {
        // 可选：通用 stub
    }

    @Test
    void givenValidInput_whenDoSomething_thenReturnsResult() {
        when(someDependency.call(any())).thenReturn("expected");
        String result = ragService.doSomething("input");
        assertThat(result).isEqualTo("expected");
        verify(someDependency).call(any());
    }

    @Test
    void givenInvalidInput_whenDoSomething_thenThrows() {
        when(someDependency.call(any())).thenThrow(new IllegalArgumentException("bad"));
        assertThatThrownBy(() -> ragService.doSomething("bad"))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessageContaining("bad");
    }
}
```

### Controller 单元测试

- 使用 `@WebMvcTest(被测Controller.class)`，只加载 Web 层。
- 控制器依赖的 Service 等用 `@MockBean` 提供 Mock。
- 使用 `MockMvc` 发起请求，用 `andExpect(status().isOk())`、`jsonPath("$.field").value(...)` 等做断言。

```java
package com.example.springai.controller;

import com.example.springai.service.RagService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.mock.web.MockMultipartFile;
import org.springframework.test.web.servlet.MockMvc;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@WebMvcTest(RagController.class)
class RagControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private RagService ragService;

    @Test
    void uploadDocument_whenSuccess_thenReturns200() throws Exception {
        when(ragService.uploadDocument(any())).thenReturn("uploaded");
        MockMultipartFile file = new MockMultipartFile("file", "doc.pdf",
            "application/pdf", "content".getBytes());
        mockMvc.perform(multipart("/api/rag/upload").file(file))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.content").value("uploaded"))
            .andExpect(jsonPath("$.type").value("rag"));
    }

    @Test
    void uploadDocument_whenServiceThrows_thenReturns5xx() throws Exception {
        when(ragService.uploadDocument(any())).thenThrow(new RuntimeException("error"));
        MockMultipartFile file = new MockMultipartFile("file", "x.pdf", "application/pdf", new byte[0]);
        mockMvc.perform(multipart("/api/rag/upload").file(file))
            .andExpect(status().is5xxServerError());
    }
}
```

### 工具类 / 无依赖类

- 不需要 Mock，直接 `new` 被测类，测试静态方法或实例方法即可。
- 仍使用 JUnit 5 + AssertJ/JUnit Assertions。

---

## 命名与结构

- **测试类名**：`*Test`（如 `RagServiceTest`、`RagControllerTest`）。
- **测试方法名**：推荐 `given条件_when操作_then结果` 或 `方法名_场景_预期`，如 `uploadDocument_whenSuccess_thenReturns200`。
- **包**：与主代码一致，例如主类 `com.example.springai.service.RagService` → 测试类 `com.example.springai.service.RagServiceTest`。
- **一个测试方法只验证一个行为**；多个场景拆成多个 `@Test`。

---

## Guidelines

1. **先测行为再测实现**：断言返回值和状态变化，必要时再校验与 Mock 的交互（`verify`）。
2. **避免测试私有方法**：通过公共 API 覆盖逻辑；若必须测私有逻辑，可考虑包级可见或重构为可测单元。
3. **不依赖顺序**：不依赖 `@Order` 或执行顺序；每个测试独立、可乱序执行。
4. **外部依赖必须 Mock**：HTTP 客户端、仓库、AI 客户端等一律 Mock，不在单测中发起真实调用。
5. **异常路径要测**：空指针、非法参数、依赖抛异常时的控制器/服务响应。
6. **保持简洁**：Given-When-Then 清晰；重复的构建数据可提取为 `@BeforeEach` 或私有方法，避免冗长。

---

## 依赖说明

默认假设项目已包含：

- `spring-boot-starter-test`（含 JUnit 5、Mockito、AssertJ、MockMvc）
- 无需额外依赖即可按本 skill 生成并运行上述测试。

若项目使用 JUnit 4 或不同 Mock 库，需在生成前说明，以便调整注解与导入。
