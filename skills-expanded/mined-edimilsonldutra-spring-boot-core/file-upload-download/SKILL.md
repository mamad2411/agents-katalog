---
name: file-upload-download
description: Upload e download de arquivos no Spring Boot 4 — MultipartFile, limites de tamanho, FileStorageService com nome gerado e sanitização contra path traversal, validação de tipo por assinatura (Tika), download em stream com Content-Disposition seguro, metadados no banco com dono, disco local × S3, 413 e testes. Use quando a API receber ou servir arquivos, ou ao revisar um endpoint de upload.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md), [`../code-style/SKILL.md`](../code-style/SKILL.md) e [`../exception-handling/SKILL.md`](../exception-handling/SKILL.md) (`FileStorageException`, `FileNotFoundException`). Armazenamento na AWS: [`../aws-s3-sqs/SKILL.md`](../aws-s3-sqs/SKILL.md). Importar planilhas a partir do upload: `file-import-export`.

# Upload e download de arquivos

Upload é uma das superfícies de ataque mais exploradas de uma API: **path traversal** (`../../etc/passwd`), sobrescrita de arquivos de outros usuários, arquivo executável disfarçado de imagem, zip bomb, disco cheio. O código de "salvar o arquivo" é curto; o que importa são as **validações** em volta.

## 1. Onde guardar

| Armazenamento | Quando | Observação |
|---|---|---|
| **Disco local** (`file.upload-dir`) | Desenvolvimento, protótipo, uma instância única | **Não** sobrevive a um pod/container recriado e não é compartilhado entre réplicas |
| **Volume persistente** (PVC no Kubernetes) | Poucas réplicas, sem nuvem de objetos | `ReadWriteMany` é necessário para várias réplicas — caro e lento em muitos provedores |
| **Object storage** (S3 e equivalentes) | Produção, várias réplicas, arquivos grandes | Padrão recomendado: veja `aws-s3-sqs` (presigned URL, bucket privado) |

O código abaixo isola o armazenamento em um `FileStorageService`, para que trocar disco por S3 mude **uma classe**.

---

## 2. Configuração

```yaml
spring:
  servlet:
    multipart:
      enabled: true
      file-size-threshold: 2KB
      max-file-size: 10MB
      max-request-size: 12MB

file:
  upload-dir: ${FILE_UPLOAD_DIR:uploads}
```
- `max-file-size`/`max-request-size`: o **teto** por arquivo e por request. Escolha pelo caso de uso (uma foto de perfil não precisa de 200 MB). Acima do limite, o Spring lança `MaxUploadSizeExceededException`, que o `ResponseEntityExceptionHandler` estendido pelo handler do projeto responde com **413** (`ProblemDetail`).
- Atrás de Ingress/proxy, o limite do proxy também vale (`nginx.ingress.kubernetes.io/proxy-body-size`) — o menor dos dois ganha.
- No `application.yml` de **teste** (cópia completa — `code-organization`), aponte para o build: `file.upload-dir: target/test-uploads` (Gradle: `build/test-uploads`).

```java
@Configuration
@ConfigurationProperties(prefix = "file")
public class FileStorageConfig {

    private String uploadDir;

    public String getUploadDir() {
        return uploadDir;
    }

    public void setUploadDir(String uploadDir) {
        this.uploadDir = uploadDir;
    }
}
```

---

## 3. FileStorageService

```java
@Service
public class FileStorageService {

    private static final Logger logger = LoggerFactory.getLogger(FileStorageService.class);
    private static final Set<String> ALLOWED_TYPES = Set.of("image/png", "image/jpeg", "application/pdf");

    private final Path fileStorageLocation;
    private final Tika tika = new Tika();

    @Autowired
    public FileStorageService(FileStorageConfig fileStorageConfig) {
        this.fileStorageLocation = Paths.get(fileStorageConfig.getUploadDir()).toAbsolutePath().normalize();
        try {
            Files.createDirectories(this.fileStorageLocation);
        } catch (IOException e) {
            throw new FileStorageException("Could not create the directory where files will be stored!", e);
        }
    }

    public String storeFile(MultipartFile file) {
        if (file == null || file.isEmpty()) throw new BadRequestException("File must not be empty!");
        var originalName = StringUtils.cleanPath(Objects.requireNonNullElse(file.getOriginalFilename(), ""));
        if (originalName.contains("..")) throw new BadRequestException("Filename contains an invalid path sequence!");

        if (!ALLOWED_TYPES.contains(detectType(file))) throw new BadRequestException("File type not allowed!");

        var storedName = UUID.randomUUID() + extensionOf(originalName);
        var target = fileStorageLocation.resolve(storedName).normalize();
        if (!target.startsWith(fileStorageLocation)) throw new BadRequestException("Invalid file location!");

        try (var input = file.getInputStream()) {
            Files.copy(input, target, StandardCopyOption.REPLACE_EXISTING);
            logger.info("Stored file {} as {}", originalName, storedName);
            return storedName;
        } catch (IOException e) {
            throw new FileStorageException("Could not store file " + originalName + ". Please try again!", e);
        }
    }

    public Resource loadFileAsResource(String storedName) {
        var filePath = fileStorageLocation.resolve(storedName).normalize();
        if (!filePath.startsWith(fileStorageLocation)) throw new FileNotFoundException("File not found: " + storedName);
        var resource = new PathResource(filePath);
        if (!resource.exists()) throw new FileNotFoundException("File not found: " + storedName);
        return resource;
    }

    private String detectType(MultipartFile file) {
        try (var input = file.getInputStream()) {
            return tika.detect(input);
        } catch (IOException e) {
            throw new FileStorageException("Could not read the file!", e);
        }
    }

    private String extensionOf(String name) {
        var dot = name.lastIndexOf('.');
        return dot < 0 ? "" : name.substring(dot).toLowerCase(Locale.ROOT);
    }
}
```
Por que cada linha existe:
- **O nome gravado é um UUID**, nunca o nome do client: elimina path traversal, colisão e sobrescrita do arquivo de outro usuário. O nome original vira **metadado** (seção 5).
- **`normalize()` + `startsWith(root)`** na gravação **e** na leitura: a última barreira contra `..`, links e nomes codificados.
- **Tipo pela assinatura, não pela extensão nem pelo `Content-Type`** do client (ambos são declarados pelo client e mentem). `org.apache.tika:tika-core` (fora do BOM — property de versão, `maven-config`) lê os *magic bytes*; chame `tika.detect(InputStream)` **sem** o nome do arquivo, para que a extensão do client não influencie o resultado. Use uma **lista permitida** do que o caso de uso aceita; nunca uma lista de proibidos.
- **Stream, nunca `file.getBytes()`**: `getBytes()` carrega o arquivo inteiro na memória (10 réplicas × 10 uploads de 200 MB = OOM).
- Mensagens das exceptions seguem o idioma salvo (`exception-handling`).
- Com a preferência de field injection, a injeção por constructor aqui é deliberada: o diretório é resolvido uma vez na construção.

**Conteúdo perigoso:** imagens podem carregar payload (SVG com script — não aceite SVG de usuários, ou sanitize), PDFs podem ter JavaScript. Para arquivos que outros usuários vão baixar, considere **antivírus** (ClamAV em um serviço separado, assíncrono) antes de liberar o download.

---

## 4. Controller

```java
@RestController
@RequestMapping("/api/file/v1")
@Tag(name = "File Endpoint")
public class FileController implements FileControllerDocs {

    private static final Logger logger = LoggerFactory.getLogger(FileController.class);

    @Autowired
    private FileStorageService service;

    @PostMapping("/uploadFile")
    @Override
    public UploadFileResponseDTO uploadFile(@RequestParam("file") MultipartFile file) {
        var storedName = service.storeFile(file);
        var downloadUri = ServletUriComponentsBuilder.fromCurrentContextPath()
            .path("/api/file/v1/downloadFile/")
            .path(storedName)
            .toUriString();
        return new UploadFileResponseDTO(storedName, downloadUri, file.getContentType(), file.getSize());
    }

    @PostMapping("/uploadMultipleFiles")
    @Override
    public List<UploadFileResponseDTO> uploadMultipleFiles(@RequestParam("files") MultipartFile[] files) {
        return Arrays.stream(files).map(this::uploadFile).toList();
    }

    @GetMapping("/downloadFile/{fileName:.+}")
    @Override
    public ResponseEntity<Resource> downloadFile(@PathVariable("fileName") String fileName, HttpServletRequest request) {
        var resource = service.loadFileAsResource(fileName);
        var contentType = contentTypeOf(resource, request);
        return ResponseEntity.ok()
            .contentType(MediaType.parseMediaType(contentType))
            .header(HttpHeaders.CONTENT_DISPOSITION,
                ContentDisposition.attachment().filename(resource.getFilename(), StandardCharsets.UTF_8).build().toString())
            .header("X-Content-Type-Options", "nosniff")
            .body(resource);
    }

    private String contentTypeOf(Resource resource, HttpServletRequest request) {
        try {
            var type = request.getServletContext().getMimeType(resource.getFile().getAbsolutePath());
            return type == null ? MediaType.APPLICATION_OCTET_STREAM_VALUE : type;
        } catch (IOException e) {
            logger.warn("Could not determine file type of {}", resource.getFilename());
            return MediaType.APPLICATION_OCTET_STREAM_VALUE;
        }
    }
}
```
- `UploadFileResponseDTO` é um DTO comum em `data/dto` (fileName, fileDownloadUri, fileType, size) — sem Lombok.
- **`{fileName:.+}`**: sem o regex, o Spring trataria o `.pdf` como extensão de path e cortaria o nome.
- **`ContentDisposition.attachment().filename(nome, UTF_8)`** monta o header com escape correto (aspas, acentos, `filename*`); concatenar `"attachment; filename=\"" + nome + "\""` abre **injeção de header** com nomes maliciosos.
- **`attachment` + `nosniff`**: o browser baixa em vez de renderizar — um HTML/SVG enviado por um usuário não executa no domínio da API. Use `inline` só para tipos seguros que você validou (PNG/JPEG/PDF).
- `Resource` no `ResponseEntity` é escrito em **stream** pelo Spring (sem carregar na memória). Para arquivos muito grandes, suporte a `Range` (download retomável) já vem com `ResourceHttpMessageConverter`/`ResourceRegionHttpMessageConverter`.
- Upload em lote: limite a quantidade de arquivos por request.
- **Swagger:** documente com `@RequestBody(content = @Content(mediaType = MediaType.MULTIPART_FORM_DATA_VALUE))` na interface `*ControllerDocs`; o download como `@Content(mediaType = MediaType.APPLICATION_OCTET_STREAM_VALUE)` (`swagger`).

---

## 5. Metadados e autorização (produção)

O exemplo acima serve qualquer arquivo para quem souber o nome — aceitável num protótipo local, **IDOR** em produção. Em uma aplicação real:
- Grave uma linha por arquivo (`files`: `id`, `stored_name`, `original_name`, `content_type`, `size`, `owner_id`, `created_at`) com migration Flyway (`flyway-migrations`) e entity própria (`spring-data-jpa`).
- O download recebe o **id** do arquivo, carrega a linha, **confere o dono/permissão** (`authentication`) e só então lê o `stored_name`.
- Exclusão: apague a linha e o arquivo; para LGPD, o arquivo entra no fluxo de eliminação do titular (`privacy-lgpd`).
- Em S3, prefira **presigned URL** de curta duração em vez de passar o arquivo pela API (`aws-s3-sqs`).

---

## 6. Testes

- **Unit** (`testing`): `FileStorageService` com um diretório temporário (`@TempDir`) — nome gerado, rejeição de `..`, de tipo não permitido (um `.png` que na verdade é texto), de arquivo vazio; leitura fora do diretório lança `FileNotFoundException`.
- **Integração** (`integration-testing`): upload multipart com REST Assured e download do mesmo conteúdo:
```java
var response = api().contentType(ContentType.MULTIPART)
    .multiPart("file", "cover.png", pngBytes, "image/png")
    .when().post("/api/file/v1/uploadFile")
    .then().statusCode(200)
    .extract().jsonPath();

api().accept(ContentType.ANY)
    .when().get("/api/file/v1/downloadFile/{name}", response.getString("fileName"))
    .then().statusCode(200)
    .header("Content-Disposition", startsWith("attachment"));
```
Teste também: arquivo acima do limite (**413**), tipo proibido (**400**), nome com `../` (**400**), arquivo inexistente (**404**).

---

## Regras principais

- O nome gravado é gerado (UUID + extensão normalizada); o nome do client é só metadado.
- `normalize()` + `startsWith(diretórioRaiz)` na gravação e na leitura.
- Tipo validado pela **assinatura** (Tika) contra uma **lista permitida** — nunca pela extensão ou pelo `Content-Type` do client.
- Limites explícitos (`max-file-size`, `max-request-size`, quantidade por lote); acima do limite, 413.
- Stream (`getInputStream()`, `Resource`), nunca `getBytes()` para arquivos de tamanho arbitrário.
- Download com `ContentDisposition.attachment().filename(nome, UTF_8)` e `X-Content-Type-Options: nosniff`; nunca header montado por concatenação.
- Produção: metadados no banco com dono e checagem de permissão no download (sem IDOR); várias réplicas → object storage (`aws-s3-sqs`), não disco local.
- Diretório de upload de teste dentro de `target/`/`build/`.
- **Sem Lombok** — deliberado.
