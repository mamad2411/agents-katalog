---
name: playwright-java
description: "Crie, escreva, depure e melhore testes E2E Playwright de nível empresarial em Java usando Page Object Model, JUnit 5, relatórios Allure e execução paralela."
category: test-automation
risk: safe
source: community
date_added: "2025-03-08"
author: amalsam18
tags: [playwright, java, e2e-testing, junit5, page-object-model, allure, selenium-alternative]
tools: [claude, cursor, antigravity]
---

# Playwright Java – Automação de Testes Avançada

## Visão geral

Esta skill produz código de teste Playwright Java com qualidade de produção e nível empresarial.
Ela força o uso de Page Object Model (POM), estratégias rigorosas de localizador, execução paralela thread-safe
e integração completa com relatórios Allure. Direcionada para Java 17+ e Playwright 1.44+.

Arquivos de referência de suporte estão disponíveis para tópicos mais profundos:

| Tópico | Arquivo |
|-------|------|
| Maven POM, ConfigReader, Docker/setup de CI | `references/config.md` |
| Padrão de componente, dropdowns, uploads, waits | `references/page-objects.md` |
| API de assertion completa, soft assertions, visual testing | `references/assertions.md` |
| Fixtures, test data factory, auth state, retry | `references/fixtures.md` |
| Templates de classe base prontos para usar | `templates/BaseTest.java`, `templates/BasePage.java` |

---

## Quando usar esta skill

- Use ao criar um novo projeto Playwright Java do zero
- Use ao escrever classes Page Object ou classes de teste JUnit 5
- Use quando o usuário perguntar sobre testes cross-browser, execução paralela ou relatórios Allure
- Use ao corrigir testes flaky ou substituir `Thread.sleep()` por waits apropriados
- Use ao configurar Playwright em pipelines CI/CD (GitHub Actions, Jenkins, Docker)
- Use ao combinar chamadas de API e assertions de UI em um único teste (teste híbrido)
- Use quando o usuário mencionar "padrão POM", "BrowserContext", "Playwright fixtures" ou "traces"

---

## Como funciona

### Etapa 1: Decida a abordagem

Use esta matriz para escolher o padrão correto antes de escrever qualquer código:

| Solicitação do usuário | Abordagem |
|---|---|
| Novo projeto do zero | Scaffold completo — veja `references/config.md` |
| Teste de um recurso único | Classe POM + classe de teste JUnit5 |
| Híbrido API + UI | `APIRequestContext` ao lado de `Page` |
| Cross-browser | `@MethodSource` parametrizado sobre nomes de browser |
| Corrigir teste flaky | Substitua `sleep` por `waitFor` / `waitForResponse` |
| Integração de CI | `playwright install --with-deps` no pipeline |
| Execução paralela | `junit-platform.properties` + `ThreadLocal` |
| Relatórios avançados | Allure + Playwright trace + gravação de vídeo |

---

### Etapa 2: Crie a estrutura do projeto

Sempre use este layout ao criar um novo projeto:

```
src/
├── test/
│   ├── java/com/company/tests/
│   │   ├── base/
│   │   │   ├── BaseTest.java        ← templates/BaseTest.java
│   │   │   └── BasePage.java        ← templates/BasePage.java
│   │   ├── pages/
│   │   │   └── LoginPage.java
│   │   ├── tests/
│   │   │   └── LoginTest.java
│   │   ├── utils/
│   │   │   ├── TestDataFactory.java
│   │   │   └── WaitUtils.java
│   │   └── config/
│   │       └── ConfigReader.java
│   └── resources/
│       ├── test.properties
│       ├── junit-platform.properties
│       └── testdata/users.json
pom.xml
```

---

### Etapa 3: Configure BaseTest thread-safe

```java
public class BaseTest {
    protected static ThreadLocal<Playwright>     playwrightTL = new ThreadLocal<>();
    protected static ThreadLocal<Browser>        browserTL    = new ThreadLocal<>();
    protected static ThreadLocal<BrowserContext> contextTL    = new ThreadLocal<>();
    protected static ThreadLocal<Page>           pageTL       = new ThreadLocal<>();

    protected Page page() { return pageTL.get(); }

    @BeforeEach
    void setUp() {
        Playwright playwright = Playwright.create();
        playwrightTL.set(playwright);

        Browser browser = resolveBrowser(playwright).launch(
            new BrowserType.LaunchOptions()
                .setHeadless(ConfigReader.isHeadless()));
        browserTL.set(browser);

        BrowserContext context = browser.newContext(new Browser.NewContextOptions()
            .setViewportSize(1920, 1080)
            .setRecordVideoDir(Paths.get("target/videos/"))
            .setLocale("en-US"));
        context.tracing().start(new Tracing.StartOptions()
            .setScreenshots(true).setSnapshots(true));
        contextTL.set(context);
        pageTL.set(context.newPage());
    }

    @AfterEach
    void tearDown(TestInfo testInfo) {
        String name = testInfo.getDisplayName().replaceAll("[^a-zA-Z0-9]", "_");
        contextTL.get().tracing().stop(new Tracing.StopOptions()
            .setPath(Paths.get("target/traces/" + name + ".zip")));
        pageTL.get().close();
        contextTL.get().close();
        browserTL.get().close();
        playwrightTL.get().close();
    }

    private BrowserType resolveBrowser(Playwright pw) {
        return switch (System.getProperty("browser", "chromium").toLowerCase()) {
            case "firefox" -> pw.firefox();
            case "webkit"  -> pw.webkit();
            default        -> pw.chromium();
        };
    }
}
```

---

### Etapa 4: Construa classes Page Object

```java
public class LoginPage extends BasePage {

    // Declare TODOS os locators como campos — nunca inline em métodos de ação
    private final Locator emailInput;
    private final Locator passwordInput;
    private final Locator loginButton;
    private final Locator errorMessage;

    public LoginPage(Page page) {
        super(page);
        emailInput    = page.getByLabel("Email address");
        passwordInput = page.getByLabel("Password");
        loginButton   = page.getByRole(AriaRole.BUTTON,
                            new Page.GetByRoleOptions().setName("Sign in"));
        errorMessage  = page.getByTestId("login-error");
    }

    @Override protected String getUrl() { return "/login"; }

    // Métodos de navegação retornam o próximo Page Object — permite encadeamento fluente
    public DashboardPage loginAs(String email, String password) {
        fill(emailInput, email);
        fill(passwordInput, password);
        clickAndWaitForNav(loginButton);
        return new DashboardPage(page);
    }

    public LoginPage loginExpectingError(String email, String password) {
        fill(emailInput, email);
        fill(passwordInput, password);
        loginButton.click();
        errorMessage.waitFor();
        return this;
    }

    public String getErrorMessage() { return errorMessage.textContent(); }
}
```

---

### Etapa 5: Escreva testes com anotações Allure

```java
@ExtendWith(AllureJunit5.class)
class LoginTest extends BaseTest {

    private LoginPage loginPage;

    @BeforeEach
    void openLoginPage() {
        loginPage = new LoginPage(page());
        loginPage.navigate();
    }

    @Test
    @Severity(SeverityLevel.BLOCKER)
    @DisplayName("Credenciais válidas redirecionam para dashboard")
    void shouldLoginWithValidCredentials() {
        User user = TestDataFactory.getDefaultUser();
        DashboardPage dash = loginPage.loginAs(user.email(), user.password());

        assertThat(page()).hasURL(Pattern.compile(".*/dashboard"));
        assertThat(dash.getWelcomeBanner()).containsText("Welcome, " + user.firstName());
    }

    @Test
    void shouldShowErrorOnInvalidCredentials() {
        loginPage.loginExpectingError("bad@test.com", "wrongpass");

        SoftAssertions softly = new SoftAssertions();
        softly.assertThat(loginPage.getErrorMessage()).contains("Invalid email or password");
        softly.assertThat(page()).hasURL(Pattern.compile(".*/login"));
        softly.assertAll();
    }

    @ParameterizedTest
    @MethodSource("provideInvalidCredentials")
    void shouldRejectInvalidCredentials(String email, String password, String expectedError) {
        loginPage.loginExpectingError(email, password);
        assertThat(loginPage.getErrorMessage()).containsText(expectedError);
    }

    static Stream<Arguments> provideInvalidCredentials() {
        return Stream.of(
            Arguments.of("", "password123", "Email is required"),
            Arguments.of("user@test.com", "", "Password is required"),
            Arguments.of("notanemail", "pass", "Invalid email format")
        );
    }
}
```

---

## Exemplos

### Exemplo 1: Teste híbrido API + UI

```java
@Test
void shouldDisplayNewlyCreatedOrder() {
    // Arrange via API — mais rápido que navegar pela UI
    APIRequestContext api = page().context().request();
    APIResponse response = api.post("/api/orders",
        RequestOptions.create()
            .setHeader("Authorization", "Bearer " + authToken)
            .setData(Map.of("productId", "SKU-001", "quantity", 2)));
    assertThat(response).isOK();

    String orderId = new JsonParser().parse(response.text())
        .getAsJsonObject().get("id").getAsString();

    OrdersPage orders = new OrdersPage(page());
    orders.navigate();
    assertThat(orders.getOrderRowById(orderId)).isVisible();
}
```

### Exemplo 2: Mock de network

```java
@Test
void shouldHandleApiFailureGracefully() {
    page().route("**/api/products", route -> route.fulfill(
        new Route.FulfillOptions()
            .setStatus(503)
            .setBody("{\"error\":\"Service Unavailable\"}")
            .setContentType("application/json")));

    ProductsPage products = new ProductsPage(page());
    products.navigate();

    assertThat(products.getErrorBanner())
        .hasText("We're having trouble loading products. Please try again.");
}
```

### Exemplo 3: Teste cross-browser em paralelo

```java
@ParameterizedTest
@MethodSource("browsers")
void shouldRenderCheckoutOnAllBrowsers(String browserName) {
    System.setProperty("browser", browserName);
    new CheckoutPage(page()).navigate();
    assertThat(page().locator(".checkout-form")).isVisible();
}

static Stream<String> browsers() {
    return Stream.of("chromium", "firefox", "webkit");
}
```

### Exemplo 4: Config de execução paralela

```properties
# src/test/resources/junit-platform.properties
junit.jupiter.execution.parallel.enabled=true
junit.jupiter.execution.parallel.mode.default=concurrent
junit.jupiter.execution.parallel.config.strategy=fixed
junit.jupiter.execution.parallel.config.fixed.parallelism=4
```

### Exemplo 5: Pipeline GitHub Actions de CI

```yaml
- name: Install Playwright browsers
  run: mvn exec:java -e -Dexec.mainClass=com.microsoft.playwright.CLI -Dexec.args="install --with-deps"

- name: Run tests
  run: mvn test -Dbrowser=${{ matrix.browser }} -Dheadless=true

- name: Upload traces on failure
  uses: actions/upload-artifact@v4
  if: failure()
  with:
    name: playwright-traces
    path: target/traces/

- name: Upload Allure results
  uses: actions/upload-artifact@v4
  if: always()
  with:
    name: allure-results
    path: target/allure-results/
```

---

## Melhores práticas

- ✅ Use `ThreadLocal<Page>` para cada suíte de testes paralela e segura
- ✅ Declare todos os campos `Locator` no topo da classe Page Object
- ✅ Retorne o próximo Page Object a partir dos métodos de navegação (encadeamento fluente)
- ✅ Use `assertThat(locator)` — retenta automaticamente até o timeout
- ✅ Use `getByRole`, `getByLabel`, `getByTestId` como locators de primeira escolha
- ✅ Inicie tracing em `@BeforeEach` e pare com um caminho de arquivo em `@AfterEach`
- ✅ Use `SoftAssertions` ao validar múltiplos campos em uma única página
- ✅ Configure auth state salvo (`storageState`) para pular login entre classes de teste
- ❌ Nunca use `Thread.sleep()` — substitua por `waitFor()` ou `waitForResponse()`
- ❌ Nunca hardcode URLs base — sempre use `ConfigReader.getBaseUrl()`
- ❌ Nunca crie uma instância `Playwright` dentro de um Page Object
- ❌ Nunca use XPath para elementos dinâmicos ou que mudam frequentemente

---

## Armadilhas comuns

- **Problema:** Testes falham aleatoriamente em modo paralelo
  **Solução:** Garanta que cada teste crie sua própria cadeia `Playwright → Browser → BrowserContext → Page` via `ThreadLocal`. Nunca compartilhe uma `Page` entre threads.

- **Problema:** `assertThat(locator).isVisible()` dá timeout mesmo quando o elemento aparece
  **Solução:** Aumente o timeout com `.setTimeout(10_000)` ou eleve `context.setDefaultTimeout()` em `BaseTest`.

- **Problema:** `Thread.sleep(2000)` foi adicionado mas testes continuam flaky
  **Solução:** Substitua por `page.waitForResponse("**/api/endpoint", () -> action())` ou `assertThat(locator).hasText("Done")` que faz polling automaticamente.

- **Problema:** Arquivo zip de trace do Playwright está vazio ou ausente
  **Solução:** Garanta que `tracing().start()` seja chamado antes das ações de teste e `tracing().stop()` esteja em `@AfterEach` — não em `@AfterAll`.

- **Problema:** Relatório Allure está em branco ou faltam passos
  **Solução:** Adicione o agent AspectJ ao `maven-surefire-plugin` `<argLine>` em `pom.xml` — veja `references/config.md` para o snippet exato.

- **Problema:** Arquivo de auth `storageState` está obsoleto e testes redirecionam para login
  **Solução:** Re-execute `AuthSetup` para regenerar `target/auth/user-state.json` antes da suíte, ou adicione um `@BeforeAll` que o atualize condicionalmente.

---

## Skills relacionadas

- `@rest-assured-java` — Use para suítes de testes de API pura sem qualquer interação de UI
- `@selenium-java` — Alternativa legada; prefira Playwright para todos os novos projetos
- `@allure-reporting` — Mergulho profundo em anotações Allure, categorias e tendências de histórico
- `@testcontainers-java` — Use ao lado desta skill quando testes precisam de um banco de dados ou serviço ao vivo
- `@github-actions-ci` — Para construir pipelines completos de CI com matriz multi-browser