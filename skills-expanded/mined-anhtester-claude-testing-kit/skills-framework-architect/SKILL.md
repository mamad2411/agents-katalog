---
name: skills-framework-architect
description: Skill thiết kế và scaffold automation framework hoàn chỉnh cho Playwright, Selenium, và Appium — bao gồm project structure, base classes, config management, reporting, và CI/CD integration.
---

# Framework Architect

## Description

Skill chuyên biệt giúp agent thiết kế, scaffold và triển khai automation framework từ đầu. Hỗ trợ đa nền tảng (Web, Mobile, API) với các framework phổ biến nhất.

Agent có thể:

- Thiết kế project structure theo best practices
- Sinh base classes, config management, driver/browser management
- Tích hợp reporting (Allure, HTML Report, Playwright Report)
- Cấu hình CI/CD pipeline (GitHub Actions, GitLab CI, Jenkins)
- Sinh template Page Object Model, fixtures, helpers
- Tạo file cấu hình (package.json, pom.xml, build.gradle, playwright.config.ts)

---

## When to Use

Sử dụng skill này khi:

- User yêu cầu tạo/thiết kế automation framework mới
- User cần scaffold project structure cho test automation
- User muốn chuẩn hóa framework hiện tại
- User cần tích hợp reporting hoặc CI/CD vào framework
- User hỏi về best practices cho framework design

Trigger keywords: "create framework", "design framework", "scaffold project", "thiết kế framework", "tạo project mới"

---

## Supported Stacks

### 🌐 Web Automation

| Stack | Ngôn ngữ | Runner | Report | Build Tool |
|---|---|---|---|---|
| **Playwright + TypeScript** | TypeScript | Playwright Test | HTML Report, Allure | npm |
| **Playwright + Java** | Java | TestNG / JUnit5 | Allure Report | Maven / Gradle |
| **Playwright + Python** | Python | Pytest | Allure, pytest-html | pip |
| **Selenium + Java** | Java | TestNG | Allure, ExtentReports | Maven / Gradle |
| **Selenium + Python** | Python | Pytest | Allure, pytest-html | pip |

### 📱 Mobile Automation

| Stack | Ngôn ngữ | Runner | Report | Build Tool |
|---|---|---|---|---|
| **Appium + Java** | Java | TestNG | Allure, ExtentReports | Maven / Gradle |
| **Appium + Python** | Python | Pytest | Allure, pytest-html | pip |

### 🔌 API Automation

| Stack | Ngôn ngữ | Runner | Report |
|---|---|---|---|
| **REST Assured** | Java | TestNG | Allure |
| **Playwright API** | TypeScript | Playwright Test | HTML Report |
| **Requests + Pytest** | Python | Pytest | Allure |

---

## Framework Components

Mỗi framework PHẢI bao gồm các thành phần sau (tùy chỉnh theo stack):

### 1. Project Structure (Mandatory)
- Cấu trúc thư mục rõ ràng, phân tách pages/tests/utils/config
- File README.md hướng dẫn setup + chạy test
- File .gitignore phù hợp

### 2. Configuration Management (Mandatory)
- Quản lý environment (dev/staging/prod) qua config file hoặc .env
- Centralized config — không hardcode giá trị trong test
- Sensitive data (credentials) qua environment variables, KHÔNG commit vào repo

### 3. Browser / Driver Management (Mandatory)
- **Playwright:** playwright.config.ts / conftest.py với browser setup
- **Selenium:** WebDriverManager hoặc Driver Factory pattern
- **Appium:** Desired Capabilities factory, Appium server config

### 4. Base Classes (Mandatory)
- Base Page — chứa common methods (wait, click, type, screenshot)
- Base Test — chứa setup/teardown, test lifecycle hooks
- Không hardcode waits — chỉ dùng smart waits

### 5. Page Object Model (Mandatory)
- Mỗi page/screen → 1 Page class
- Locators khai báo ở đầu class, không inline trong test
- Methods mô tả hành vi người dùng (không phải thao tác DOM)

### 6. Test Data Management (Mandatory)
- Data factory / builder pattern cho test data
- Data external (JSON/YAML/CSV) cho data-driven tests
- Data unique + traceable (timestamp/random prefix)

### 7. Utilities (Mandatory)
- Wait helpers (smart waits, custom conditions)
- Screenshot utilities (capture cuối MỌI test — cả PASS lẫn FAIL)
- Logger (structured logging, không dùng print/console.log)
- Date/Time helpers, String generators

### 8. Reporting (Mandatory)
- Tích hợp ít nhất 1 reporting tool (Allure ưu tiên)
- **Metadata mỗi test:** tên Tiếng Việt · Description · Severity · Tags · label `testId`
- **Test Body có step** `Arrange:` / `Act:` / `Assert:` — Base Page dùng step API để sinh sub-step
- **Screenshot attach cuối MỌI test** — cả PASS lẫn FAIL, không chỉ khi fail
- **KHÔNG** attachment `stdout` / `stderr`
- Test execution summary (pass/fail/skip counts)

> Chi tiết bắt buộc: [`.claude/rules/reporting_rules.md`](../../rules/reporting_rules.md)

### 9. CI/CD Pipeline (Optional — nhưng khuyến khích)
- GitHub Actions / GitLab CI / Jenkins pipeline template
- Parallel execution config
- Artifact upload (reports, screenshots)

---

## Project Structure Templates

### Playwright + TypeScript

```
project-root/
├── playwright.config.ts        # Playwright configuration
├── package.json                # Dependencies + scripts
├── .env.example                # Environment template
├── .gitignore
├── README.md
├── src/
│   ├── pages/                  # Page Object classes
│   │   ├── base.page.ts        # Base page (common methods)
│   │   ├── login.page.ts
│   │   └── dashboard.page.ts
│   ├── fixtures/               # Custom fixtures
│   │   ├── auth.fixture.ts     # Authentication fixture
│   │   └── base.fixture.ts     # Extended test with all fixtures
│   ├── utils/                  # Helpers & utilities
│   │   ├── test-data.ts        # Data generators
│   │   ├── env.config.ts       # Environment config reader
│   │   └── helpers.ts          # Common helper functions
│   └── tests/                  # Test specs
│       ├── auth/
│       │   └── login.spec.ts
│       └── dashboard/
│           └── dashboard.spec.ts
├── test-data/                  # External test data (JSON/YAML)
│   └── users.json
└── .github/
    └── workflows/
        └── playwright.yml      # CI pipeline
```

### Selenium + Java (Maven + TestNG)

```
project-root/
├── pom.xml                     # Maven config + dependencies
├── testng.xml                  # TestNG suite config
├── .env.example
├── .gitignore
├── README.md
├── src/
│   ├── main/java/
│   │   └── com/project/
│   │       ├── pages/          # Page Object classes
│   │       │   ├── BasePage.java
│   │       │   ├── LoginPage.java
│   │       │   └── DashboardPage.java
│   │       ├── drivers/        # Driver management
│   │       │   └── DriverFactory.java
│   │       ├── config/         # Configuration
│   │       │   └── ConfigReader.java
│   │       └── utils/          # Utilities
│   │           ├── WaitHelper.java
│   │           ├── ScreenshotUtil.java
│   │           └── TestDataGenerator.java
│   └── test/java/
│       └── com/project/
│           ├── base/
│           │   └── BaseTest.java
│           └── tests/
│               ├── LoginTest.java
│               └── DashboardTest.java
├── test-data/
│   └── users.json
└── .github/
    └── workflows/
        └── selenium.yml
```

### Appium + Java (Maven + TestNG)

```
project-root/
├── pom.xml
├── testng.xml
├── .env.example
├── .gitignore
├── README.md
├── src/
│   ├── main/java/
│   │   └── com/project/
│   │       ├── screens/        # Screen Object classes (mobile POM)
│   │       │   ├── BaseScreen.java
│   │       │   ├── LoginScreen.java
│   │       │   └── HomeScreen.java
│   │       ├── drivers/        # Appium driver management
│   │       │   ├── AppiumDriverFactory.java
│   │       │   └── CapabilitiesManager.java
│   │       ├── config/
│   │       │   └── AppConfig.java
│   │       └── utils/
│   │           ├── MobileGestures.java    # Swipe, scroll, tap
│   │           ├── ScreenshotUtil.java
│   │           └── TestDataGenerator.java
│   └── test/java/
│       └── com/project/
│           ├── base/
│           │   └── BaseTest.java
│           └── tests/
│               ├── LoginTest.java
│               └── HomeTest.java
├── apps/                       # APK/IPA files
│   └── .gitkeep
├── test-data/
│   └── users.json
└── .github/
    └── workflows/
        └── appium.yml
```

### Playwright + Python (Pytest)

```
project-root/
├── playwright.config.py        # Pytest-playwright config (nếu có)
├── pyproject.toml              # Python project config
├── requirements.txt            # Dependencies
├── conftest.py                 # Root fixtures + browser setup
├── .env.example
├── .gitignore
├── README.md
├── src/
│   ├── pages/
│   │   ├── base_page.py
│   │   ├── login_page.py
│   │   └── dashboard_page.py
│   ├── utils/
│   │   ├── config.py           # Env config reader
│   │   ├── test_data.py        # Data generators
│   │   └── helpers.py
│   └── tests/
│       ├── conftest.py         # Test-level fixtures
│       ├── test_login.py
│       └── test_dashboard.py
├── test-data/
│   └── users.json
└── .github/
    └── workflows/
        └── playwright.yml
```

---

## Browser Setup Rules (BẮT BUỘC)

Áp dụng cho mọi framework Web sinh ra từ skill này — kế thừa từ `CLAUDE.md > Browser Rules`:

| Quy tắc | Giá trị | Nơi cấu hình |
|---|---|---|
| **Viewport mặc định** | `1920 x 1080` | `playwright.config.ts` · `BrowserOptions.java` · `DriverFactory.java` · `conftest.py` |
| **Headed mode** | Bật khi debug local | Đọc từ biến môi trường `HEADLESS=false` |
| **Headless mode** | Chỉ khi chạy CI | CI pipeline set `HEADLESS=true` |
| **Hard sleep** | ❌ CẤM tuyệt đối | Chỉ smart waits — xem bảng Anti-Patterns bên dưới |

Framework **phải** cho phép bật/tắt headless qua config, **không** hardcode trong code.

---

## Design Principles

1. **DRY (Don't Repeat Yourself)** — Mỗi logic chỉ viết 1 lần, tái sử dụng qua Base classes và Utils
2. **Single Responsibility** — Mỗi class/module làm 1 việc (Page chỉ chứa UI interaction, Test chỉ chứa test logic)
3. **Open/Closed** — Framework dễ mở rộng (thêm page, thêm test) mà không sửa core
4. **Configuration over Code** — Env, browser, timeout... quản lý qua config, không hardcode
5. **Fail Fast, Log Rich** — Screenshot cuối mọi test, structured logging, clear assertion messages

---

## Anti-Patterns (FORBIDDEN)

| ❌ Anti-Pattern | ✅ Đúng cách |
|---|---|
| Hardcode URL/credentials trong code | Đọc từ .env hoặc config file |
| Locator inline trong test | Khai báo trong Page class |
| `Thread.sleep()` / `waitForTimeout()` | Smart waits (`expect()`, `WebDriverWait`) |
| Global mutable state | Isolated fixtures/setup per test |
| Monolithic test file (1 file 500+ dòng) | Tách theo module/feature |
| `System.out.println()` / `console.log()` | Logger framework (Log4j, winston, logging) |

---

## Rules References

Agent PHẢI tuân thủ các rules chi tiết:

- `.claude/rules/automation_rules.md` — General automation best practices
- `.claude/rules/reporting_rules.md` — Allure report: metadata, step, screenshot, cấm stdout
- `.claude/rules/locator_strategy.md` — Locator selection priority
- `.claude/rules/playwright_rules.md` — Playwright-specific rules
- `.claude/rules/selenium_rules.md` — Selenium-specific rules
- `.claude/rules/appium_rules.md` — Appium mobile automation rules
- `CLAUDE.md` > "Browser Rules" — Viewport 1920×1080, headed/headless
- `CLAUDE.md` > "Cleanup & Delivery" — Definition of Done trước khi bàn giao

---

## Related Files

| File | Vai trò |
|---|---|
| `.claude/rules/reporting_rules.md` | Quy tắc report bắt buộc — metadata, step, screenshot, thư mục `reports/` |
| `.claude/commands/generate_automation_framework.md` | Workflow 6 bước thực thi scaffold |
