---
name: postman-newman
description: Testes de API de caixa-preta com Postman e Newman — onde eles entram (smoke e regressão contra a aplicação rodando, não no lugar do REST Assured), coleção versionada no Git, environments sem segredos, login JWT no pre-request, encadeamento de ids, testes com pm.test e JSON Schema, dados únicos, data-driven, Newman no terminal e no CI contra docker compose e pós-deploy. Use quando quiser uma suíte Postman executável no pipeline ou um smoke test depois do deploy.
---

Antes de aplicar este pattern, leia também [`../integration-testing/SKILL.md`](../integration-testing/SKILL.md) (a suíte principal de integração, com REST Assured), [`../authentication/SKILL.md`](../authentication/SKILL.md) (`/auth/signin`), [`../docker-and-docker-compose/SKILL.md`](../docker-and-docker-compose/SKILL.md) e [`../github-actions/SKILL.md`](../github-actions/SKILL.md).

# Postman e Newman

O **Postman** organiza requests em **coleções** com scripts de teste; o **Newman** é o executor de linha de comando que roda a coleção no terminal ou no CI. A suíte é **caixa-preta**: só fala HTTP com a aplicação já rodando — não conhece código, banco nem Spring.

## 1. Onde entra (e onde não entra)

| Suíte | Roda contra | Prova | Fica onde |
|---|---|---|---|
| Unit e slice (`testing`) | Código | Regras e camadas isoladas | `src/test` |
| Integração (`integration-testing`) | App + banco em container, dentro do build | Fluxos, contrato de erro, persistência | `src/test` |
| **Postman/Newman (esta skill)** | **A app empacotada e rodando** (compose, staging, produção) | O artefato real responde como esperado: **smoke e regressão de caixa-preta** | `postman/` no repositório |

- **Não substitua o REST Assured pelo Newman.** Os testes de integração rodam no `mvn verify`, com dados isolados e cobertura medida; o Newman roda depois, contra a imagem/ambiente — ele pega erro de **empacotamento, configuração e infraestrutura** (variável de ambiente faltando, rota no Ingress, CORS, TLS).
- **Smoke pós-deploy** é o uso que mais compensa: poucos requests críticos (health, login, um GET e um POST) logo depois de cada deploy, com rollback se falhar.
- A coleção também serve como **documentação executável** para quem usa a API no Postman.

---

## 2. Estrutura no repositório

```
postman/
├── library-api.postman_collection.json      # exportada no formato v2.1
├── local.postman_environment.json
├── ci.postman_environment.json
└── data/books.csv                            # data-driven (opcional)
```
- **Exporte a coleção no formato Collection v2.1** e commite. Revise o diff no PR como código.
- Organize em **pastas por recurso** (`Auth`, `Book`, `File`) e, dentro, a ordem do fluxo (criar → ler → atualizar → apagar).
- **Variáveis:** `baseUrl` e credenciais no **environment**; valores calculados durante a execução (`accessToken`, `bookId`) em **collection variables**.

Environment sem segredos:
```json
{
  "name": "ci",
  "values": [
    { "key": "baseUrl", "value": "http://localhost:8080", "enabled": true },
    { "key": "username", "value": "", "enabled": true },
    { "key": "password", "value": "", "type": "secret", "enabled": true }
  ]
}
```
**Nunca commite senha ou token** num environment. No CI, passe com `--env-var "password=$API_PASSWORD"`; no Postman, use o "current value" local (não sincronizado) ou o vault do Postman. Use um **usuário de teste**, nunca credenciais de produção.

---

## 3. Login JWT automático

Script de **pre-request da coleção** (roda antes de cada request) que faz login quando ainda não há token:
```javascript
if (!pm.collectionVariables.get("accessToken")) {
    pm.sendRequest({
        url: pm.environment.get("baseUrl") + "/auth/signin",
        method: "POST",
        header: { "Content-Type": "application/json" },
        body: {
            mode: "raw",
            raw: JSON.stringify({
                username: pm.environment.get("username"),
                password: pm.environment.get("password")
            })
        }
    }, (err, res) => {
        pm.expect(err).to.be.null;
        pm.expect(res.code).to.eql(200);
        pm.collectionVariables.set("accessToken", res.json().accessToken);
    });
}
```
Na aba **Authorization** da coleção: tipo *Bearer Token* com `{{accessToken}}`; os requests herdam (*Inherit auth from parent*). Os requests de `/auth/**` usam *No Auth*.

---

## 4. Testes nos requests

Aba **Tests** (scripts pós-resposta) do `POST /api/book/v1`:
```javascript
const book = pm.response.json();

pm.test("status 200", () => pm.response.to.have.status(200));

pm.test("returns the created book", () => {
    pm.expect(book.id).to.be.a("number");
    pm.expect(book.title).to.eql(pm.collectionVariables.get("bookTitle"));
});

pm.test("matches the Book schema", () => {
    pm.response.to.have.jsonSchema({
        type: "object",
        required: ["id", "title", "author", "price", "launchDate"],
        properties: {
            id: { type: "number" },
            title: { type: "string" },
            price: { type: "number" }
        }
    });
});

pm.test("responds fast enough", () => pm.expect(pm.response.responseTime).to.be.below(1000));

pm.collectionVariables.set("bookId", book.id);
```
- **Encadeie pelo id gerado** (`bookId`), nunca por um id fixo que talvez não exista no ambiente.
- **Dados únicos por execução:** no pre-request do POST, `pm.collectionVariables.set("bookTitle", "newman-" + pm.variables.replaceIn("{{$guid}}"))`, e use `{{bookTitle}}` no body. Duas execuções simultâneas (dois PRs) não colidem.
- **Limpe o que criou:** a pasta termina com o `DELETE` do recurso criado. Em ambientes compartilhados, prefixe os dados (`newman-`) para uma limpeza de segurança.
- **Teste o contrato de erro também** (`exception-handling`): `GET` de id inexistente → `404` com `message`; body inválido → `400`; sem token → `403`.
- Sobre o link HATEOAS (`hateoas`): `pm.expect(book._links.self.href).to.include("/api/book/v1/" + book.id)`.
- A ordem importa **dentro** de um fluxo (é o objeto do teste); cada pasta deve rodar sozinha (`--folder Book`), sem depender de outra.

---

## 5. Newman

```bash
npm install -g newman newman-reporter-htmlextra

newman run postman/library-api.postman_collection.json \
  -e postman/ci.postman_environment.json \
  --env-var "username=$API_USERNAME" \
  --env-var "password=$API_PASSWORD" \
  --reporters cli,junit,htmlextra \
  --reporter-junit-export target/newman/results.xml \
  --reporter-htmlextra-export target/newman/report.html \
  --bail
```
- `--bail` para na primeira falha (bom para smoke); sem ele, roda tudo e relata todas as falhas (bom para regressão).
- `--folder "Book"` roda só uma pasta; `-n 3` repete; `-d postman/data/books.csv` executa a coleção uma vez por linha do CSV (**data-driven** — variáveis `{{title}}`, `{{price}}` vêm das colunas).
- `--timeout-request 10000` evita um request preso para sempre.
- Sem instalar Node: `docker run --rm --network host -v "$PWD/postman:/etc/newman" postman/newman:6-alpine run library-api.postman_collection.json -e ci.postman_environment.json` (fixe a tag da versão atual).

---

## 6. No CI

Job que sobe a **imagem construída** com o compose do projeto, espera ficar saudável e roda o Newman (`github-actions`):
```yaml
  api-tests:
    needs: build-test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Start the application
        run: docker compose up -d --build --wait
      - name: Run Newman
        run: |
          docker run --rm --network host \
            -v "$PWD/postman:/etc/newman" \
            postman/newman:6-alpine run library-api.postman_collection.json \
            -e ci.postman_environment.json \
            --env-var "username=${{ secrets.API_TEST_USERNAME }}" \
            --env-var "password=${{ secrets.API_TEST_PASSWORD }}" \
            --reporters cli,junit --reporter-junit-export /etc/newman/results.xml
      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: newman-results
          path: postman/results.xml
      - name: Stop the application
        if: always()
        run: docker compose down -v
```
- `docker compose up --wait` espera os **healthchecks** do compose (app e banco — `docker-and-docker-compose`) em vez de um `sleep`.
- O usuário de teste existe no banco do compose por uma migration/seed **só de teste** — nunca credenciais reais.
- **Pós-deploy:** o mesmo comando com o environment de staging/produção e só a pasta `Smoke`; se falhar, o pipeline aciona o rollback (`github-actions-aws`, `argocd`). Em produção, o smoke é **somente leitura** ou usa recursos de teste dedicados.

---

## 7. Alternativas

**Bruno** e **Hurl** guardam as coleções como arquivos de texto (diffs legíveis no PR) e rodam no CLI sem conta em nuvem. Se o time não usa a interface do Postman, considere-os; os princípios desta skill (sem segredos no Git, dados únicos, smoke pós-deploy) são os mesmos.

---

## Regras principais

- Postman/Newman é caixa-preta contra a aplicação **rodando**: smoke e regressão — **não** substitui os testes de integração com REST Assured.
- Coleção exportada em v2.1 e versionada em `postman/`; pastas por recurso, cada uma executável sozinha.
- Nenhum segredo commitado: credenciais por `--env-var`/secrets do CI, usuário de teste dedicado.
- Login JWT no pre-request da coleção; auth herdada; ids encadeados por collection variables, nunca fixos.
- Dados únicos por execução (`{{$guid}}`) e limpeza do que foi criado.
- Teste status, corpo, schema, tempo de resposta e o contrato de erro.
- No CI: `docker compose up --wait` com healthchecks, Newman com relatório JUnit publicado; pós-deploy só a pasta de smoke.
- Fixe a tag da imagem do Newman; nunca `latest`.
