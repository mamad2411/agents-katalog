---
name: pdf-reports
description: Relatórios PDF com JasperReports 7 no Spring Boot 4 — dependencies e o repositório extra no Gradle, templates .jrxml no formato da versão 7, compilação uma vez com cache, PdfExporter na estrutura de exporters, parâmetros, sub-relatórios, QR code com ZXing, fontes no container, memória e testes. Use quando a API precisar gerar um PDF de listagem ou de um registro, ou quando um template Jasper antigo parar de carregar.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md), [`../code-style/SKILL.md`](../code-style/SKILL.md), [`../file-import-export/SKILL.md`](../file-import-export/SKILL.md) (contratos `FileExporter`, factory e `MediaTypes`) e [`../maven-config/SKILL.md`](../maven-config/SKILL.md). Imagem de container com fontes: [`../docker-and-docker-compose/SKILL.md`](../docker-and-docker-compose/SKILL.md).

# Relatórios PDF (JasperReports)

O **JasperReports** gera PDFs a partir de um **template** (`.jrxml`, desenhado no **Jaspersoft Studio**) preenchido com dados (uma lista de DTOs) e **parâmetros** (título, filtros, imagens). O PDF é mais um formato da exportação: um `PdfExporter` implementa o mesmo `FileExporter` de `file-import-export`, e o endpoint `exportPage` passa a aceitar `Accept: application/pdf`.

> **Alternativas.** Para um PDF simples gerado a partir de HTML (comprovante, recibo), um template HTML + Thymeleaf convertido com **OpenHTMLtoPDF**/**Flying Saucer** pode ser mais fácil de manter que um `.jrxml`. Use Jasper quando o relatório tem layout de relatório de verdade: colunas, agrupamentos, totais, sub-relatórios, paginação.

## 1. Dependencies (JasperReports 7)

A versão 7 dividiu a library em módulos (`maven-config`, tabela de libraries fora do BOM):

| Artifact | Para quê |
|---|---|
| `net.sf.jasperreports:jasperreports` | Núcleo: compilar e preencher |
| `net.sf.jasperreports:jasperreports-pdf` | Exportar para PDF (usa OpenPDF) |
| `net.sf.jasperreports:jasperreports-fonts` | Fontes DejaVu embutidas — sem elas, o PDF depende das fontes do sistema |
| `net.sf.jasperreports:jasperreports-jdt` | Compilador das expressões do template em runtime |

Todos com `${jasperreports.version}`. Para QR code: `com.google.zxing:core` e `com.google.zxing:javase` (`${zxing.version}`).

**Gradle:** o `jasperreports-pdf` depende de um OpenPDF publicado no repositório da Jaspersoft; o Maven segue o repositório declarado no POM da dependency, o Gradle **não**. Sem o repositório extra, o build falha com `Could not find com.github.librepdf:openpdf:…`:
```groovy
repositories {
    mavenCentral()
    maven { url 'https://jaspersoft.jfrog.io/jaspersoft/third-party-ce-artifacts/' }
}
```
(Kotlin DSL: `maven("https://jaspersoft.jfrog.io/jaspersoft/third-party-ce-artifacts/")`.) Releases 7.0.x recentes funcionam também com o OpenPDF comum para a maior parte dos relatórios; confira as notas da versão resolvida.

---

## 2. Templates

```
src/main/resources/
└── templates/
    ├── books.jrxml
    ├── book.jrxml
    └── book_details.jrxml        # sub-relatório
```
- **O formato do `.jrxml` mudou na versão 7.** A 7.0 trocou o parser por Jackson XML: templates `.jrxml`/`.jrtx` criados com a versão 6 ou anterior **não carregam** na 7, e arquivos `.jasper` antigos precisam ser recompilados. Converta abrindo e salvando no **Jaspersoft Studio 7+**. Templates copiados de tutoriais antigos são a causa nº 1 de "o relatório não carrega".
- Os campos do template (`<field name="title" class="java.lang.String"/>`) casam com os **getters do DTO** (`JRBeanCollectionDataSource` lê por reflexão): renomear um campo do DTO quebra o relatório em runtime, não na compilação — por isso os testes da seção 7.
- Textos do relatório (título, cabeçalhos de coluna) são voltados ao usuário: sigam o idioma salvo (`code-organization`), via parâmetros ou um resource bundle do Jasper.

---

## 3. Compilar uma vez

Compilar um `.jrxml` é caro (centenas de ms). Compile **uma vez** e reutilize o `JasperReport` (ele é imutável e pode ser compartilhado entre threads):

```java
@Component
public class ReportTemplates {

    private final Map<String, JasperReport> compiled = new ConcurrentHashMap<>();

    public JasperReport get(String templatePath) {
        return compiled.computeIfAbsent(templatePath, this::compile);
    }

    private JasperReport compile(String templatePath) {
        try (var input = new ClassPathResource(templatePath).getInputStream()) {
            return JasperCompileManager.compileReport(input);
        } catch (IOException | JRException e) {
            throw new FileStorageException("Error compiling report template " + templatePath, e);
        }
    }
}
```
Alternativa: compilar no build (plugin Maven/Gradle de Jasper ou um passo que gera `.jasper`) e carregar com `JRLoader.loadObject(...)` — tira o compilador (`jasperreports-jdt`) do runtime.

---

## 4. PdfExporter

```java
@Component
public class PdfExporter implements FileExporter {

    @Autowired
    private ReportTemplates templates;

    @Override
    public Resource exportFile(List<BookDTO> books) throws Exception {
        var report = templates.get("templates/books.jrxml");
        var parameters = new HashMap<String, Object>();
        parameters.put("REPORT_TITLE", "Books Report");
        var print = JasperFillManager.fillReport(report, parameters, new JRBeanCollectionDataSource(books));
        return new ByteArrayResource(JasperExportManager.exportReportToPdf(print));
    }
}
```
Com o `PdfExporter` registrado na `FileExporterFactory` (`file-import-export`), o `exportPage` existente já responde `Accept: application/pdf` com o `Content-Disposition` de `books_exported.pdf`.

### Relatório de um registro, com sub-relatório e QR code
```java
public Resource exportBook(Long id) throws Exception {
    var book = findById(id);
    var parameters = new HashMap<String, Object>();
    parameters.put("SUB_REPORT", templates.get("templates/book_details.jrxml"));
    parameters.put("SUB_REPORT_DATA_SOURCE", new JRBeanCollectionDataSource(List.of(book)));
    parameters.put("QR_CODEIMAGE", qrCode(book.getLinks().getRequiredLink("self").getHref()));
    var print = JasperFillManager.fillReport(templates.get("templates/book.jrxml"), parameters,
        new JRBeanCollectionDataSource(List.of(book)));
    return new ByteArrayResource(JasperExportManager.exportReportToPdf(print));
}

private InputStream qrCode(String content) throws WriterException, IOException {
    var matrix = new QRCodeWriter().encode(content, BarcodeFormat.QR_CODE, 200, 200);
    var output = new ByteArrayOutputStream();
    MatrixToImageWriter.writeToStream(matrix, "PNG", output);
    return new ByteArrayInputStream(output.toByteArray());
}
```
- No template, o parâmetro de imagem é `class="java.io.InputStream"` e o sub-relatório recebe `$P{SUB_REPORT}` com `$P{SUB_REPORT_DATA_SOURCE}`.
- O QR code aponta para o link `self` do recurso (`hateoas`); sem HATEOAS, monte a URL com `ServletUriComponentsBuilder.fromCurrentContextPath()`.
- Endpoint: `GET /api/book/v1/export/{id}` com `produces = MediaTypes.APPLICATION_PDF_VALUE`, mesma forma de `ResponseEntity<Resource>` com `ContentDisposition.attachment()`.

---

## 5. Fontes e container

- **Use as fontes do `jasperreports-fonts`** (DejaVu) no template, não "Arial": uma fonte que não existe no container é substituída ou falha, e o PDF sai diferente do que funcionou na máquina do desenvolvedor.
- Imagens Docker mínimas (Alpine, distroless) podem não ter `fontconfig`, que o AWT usa para medir texto: o preenchimento falha com `NullPointerException`/`UnsatisfiedLinkError` em `sun.awt.FontConfiguration`. Instale `fontconfig` (e uma fonte base) na imagem — ex.: `apt-get install -y --no-install-recommends fontconfig` (Debian/Ubuntu) ou `apk add fontconfig ttf-dejavu` (Alpine) — veja `docker-and-docker-compose`.
- Rode a JVM em modo headless (`-Djava.awt.headless=true`; é o default quando não há display, mas declare na imagem).

---

## 6. Memória, tempo e segurança

- O `JasperPrint` inteiro fica na memória até a exportação. Para relatórios grandes (milhares de páginas), use um **virtualizer** (`JRSwapFileVirtualizer` no parâmetro `JRParameter.REPORT_VIRTUALIZER`) ou gere em background e entregue por link (S3 — `aws-s3-sqs`).
- A exportação de listagem é **paginada** (`pagination`); "gerar o relatório de tudo" é um job assíncrono, não uma request.
- **Nunca aceite templates enviados por usuários:** as expressões de um `.jrxml` são **código Java** executado no servidor. Templates vêm do repositório, revisados como código.
- Dados pessoais em relatórios: só o necessário, com autorização no endpoint (`privacy-lgpd`).

---

## 7. Testes

- **Compilação de todos os templates** num teste rápido: falha cedo quando alguém salva um `.jrxml` no formato antigo ou com erro de expressão.
```java
@ParameterizedTest
@ValueSource(strings = {"templates/books.jrxml", "templates/book.jrxml", "templates/book_details.jrxml"})
void compilesTheTemplate(String template) {
    assertThat(new ReportTemplates().get(template)).isNotNull();
}
```
- **Conteúdo do PDF:** gere com dados conhecidos e leia o texto de volta (Apache PDFBox `PDFTextStripper`, dependency só de teste) — confira título e uma linha de dado. Comparar bytes do PDF não funciona (metadados com data mudam a cada geração).
- **Integração:** `accept(MediaTypes.APPLICATION_PDF_VALUE)` → `200`, `Content-Type: application/pdf`, corpo começando com `%PDF`.

---

## Regras principais

- JasperReports 7: `jasperreports` + `jasperreports-pdf` + `jasperreports-fonts` (+ `jasperreports-jdt` se compilar em runtime), versão por property; no Gradle, o repositório extra da Jaspersoft.
- Templates `.jrxml` no **formato da versão 7** (convertidos no Jaspersoft Studio 7+); templates da versão 6 não carregam.
- Compile cada template **uma vez** e reutilize o `JasperReport` (cache) — ou pré-compile no build.
- `PdfExporter` implementa o `FileExporter` de `file-import-export`; o formato vem do `Accept`.
- Fontes do `jasperreports-fonts` no template; `fontconfig` na imagem do container.
- Relatórios grandes: virtualizer ou geração em background; listagens sempre paginadas.
- Nunca execute templates enviados por usuários.
- Teste a compilação de todos os templates e o texto do PDF gerado.
- **Sem Lombok** — deliberado.
