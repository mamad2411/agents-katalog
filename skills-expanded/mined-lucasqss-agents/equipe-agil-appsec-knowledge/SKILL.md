---
name: equipe-agil-appsec-knowledge
description: Conhecimento específico do AppSec da Equipe Backend Ágil Kanban+XP. Cobre threat modeling leve (STRIDE), OWASP Top 10 + OWASP API Security Top 10 + OWASP ASVS, autenticação/autorização com OAuth2/OIDC (Quarkus OIDC), JWT pitfalls, Quarkus Security, supply chain security (SBOM via CycloneDX, SLSA), pipeline DevSecOps (SAST/DAST/SCA/secret scanning/IaC scan), criptografia em repouso/trânsito (TLS/mTLS), gestão de segredos (Vault), shift-left security em CI. Owner do RACI de segurança. Skill autossuficiente — todo o conteúdo necessário está aqui; não consultar fontes externas.
---

# AppSec — Conhecimento específico

Skill carregada pelo agente `equipe-agil-appsec` depois de `equipe-agil-xp-baseline` + `equipe-agil-kanban-method`. Cobre o conhecimento de **segurança de aplicação** que o time precisa para construir software seguro por design, em **Java 21 + Quarkus 3**.

## 1. Conceitos centrais

### 1.1 Mandato do AppSec na equipe

- **Owner da postura de segurança** da equipe (A/R): threat modeling, política de autz, supply chain, controles no pipeline.
- **Caça aos ASRs de segurança** no Replenishment (vide `arquitetura-base` §2.1).
- **Alimenta Risk Review** com ameaças, dívida de segurança, itens regulatórios pendentes.
- **Não substitui** dev (segurança é responsabilidade do time inteiro) nem SRE (continuidade). É consultor + gatekeeper das fitness functions de segurança no pipeline.
- RACI: A/R em política de segurança da aplicação, threat model por feature, controles no pipeline DevSecOps.

### 1.2 Stack default

- **Quarkus OIDC** (`quarkus-oidc`) — integração com Keycloak/Auth0/Cognito ou IdP corporativo.
- **Quarkus Security** (`quarkus-security`) — `@RolesAllowed`, `@Authenticated`, `SecurityIdentity`.
- **Quarkus Vault** (`quarkus-vault`) — segredos dinâmicos sem armazenar em config.
- **CycloneDX Maven Plugin** — SBOM por build (`mvn cyclonedx:makeAggregateBom`).
- **OWASP Dependency-Check** — SCA (Software Composition Analysis) por vulnerabilidade CVE.
- **Trivy** — scan de container (CVE + misconfig + secret leak).
- **Semgrep / SpotBugs+FindSecBugs** — SAST.
- **OWASP ZAP** — DAST em ambiente de staging.
- **TruffleHog / gitleaks** — secret scanning no pipeline.

### 1.3 Threat Modeling com STRIDE (Shostack — *Threat Modeling: Designing for Security*)

**STRIDE** = 6 categorias de ameaça por componente/data flow:

| Categoria | O que é | Propriedade ameaçada | Mitigações típicas |
|-----------|---------|----------------------|--------------------|
| **S**poofing | Fingir ser outro | Autenticação | OIDC, mTLS, MFA |
| **T**ampering | Alterar dado/código | Integridade | Assinatura, hash, controle de acesso |
| **R**epudiation | Negar ter feito | Não-repúdio | Log auditado, assinatura digital |
| **I**nformation Disclosure | Vazar dado | Confidencialidade | Encriptação, mascaramento, autz |
| **D**enial of Service | Indisponibilizar | Disponibilidade | Rate limit, throttling, resiliência |
| **E**levation of Privilege | Ganhar permissão extra | Autorização | Princípio do menor privilégio, RBAC/ABAC |

**Processo leve (1h por feature relevante)**:

1. Desenhe o data flow (componentes + fluxo + fronteiras de confiança).
2. Para cada componente/fluxo, pergunte cada letra do STRIDE.
3. Liste ameaças concretas com **impacto** + **probabilidade**.
4. Para cada ameaça relevante: decida **mitigar / aceitar / transferir / evitar**.
5. Registre como **ADR de segurança** + acione fitness function se aplicável.

### 1.4 OWASP Top 10 (Web Application — edição 2021)

1. **A01 Broken Access Control** — autz inconsistente; IDOR (acesso a recurso de outro via ID); rota oculta sem proteção.
2. **A02 Cryptographic Failures** — sem TLS, criptografia fraca, chave em código, hash com MD5/SHA-1.
3. **A03 Injection** — SQL injection (use parametrização), command injection, LDAP injection.
4. **A04 Insecure Design** — falha de modelagem; falta de threat model; ausência de controle por design.
5. **A05 Security Misconfiguration** — defaults inseguros, headers ausentes, debug em prod.
6. **A06 Vulnerable and Outdated Components** — dependência com CVE conhecido.
7. **A07 Identification and Authentication Failures** — credencial fraca, sessão sem expiração, sem MFA.
8. **A08 Software and Data Integrity Failures** — pipeline sem verificação de integridade; dependência sem checksum.
9. **A09 Security Logging and Monitoring Failures** — sem log de evento de segurança; sem alerta.
10. **A10 Server-Side Request Forgery (SSRF)** — servidor faz requisição a URL controlada por atacante.

### 1.5 OWASP API Security Top 10 (edição 2023)

1. **API1 Broken Object Level Authorization (BOLA)** — IDOR de API.
2. **API2 Broken Authentication** — JWT mal validado, refresh sem expirar.
3. **API3 Broken Object Property Level Authorization** — campo sensível exposto ou aceito sem checagem.
4. **API4 Unrestricted Resource Consumption** — sem rate limit, sem paginação, queries sem `LIMIT`.
5. **API5 Broken Function Level Authorization** — endpoint admin acessível por usuário comum.
6. **API6 Unrestricted Access to Sensitive Business Flows** — fluxo crítico sem proteção anti-abuso.
7. **API7 Server-Side Request Forgery** — repete A10 do Top 10 web.
8. **API8 Security Misconfiguration** — repete A05.
9. **API9 Improper Inventory Management** — endpoint desatualizado/esquecido exposto.
10. **API10 Unsafe Consumption of APIs** — confia cegamente em API externa.

### 1.6 OWASP ASVS — Application Security Verification Standard

- Catálogo de requisitos verificáveis em **3 níveis**:
  - **Nível 1** — baseline para qualquer aplicação (mínimo).
  - **Nível 2** — aplicações que processam dado sensível (default da equipe para sistemas regulados).
  - **Nível 3** — aplicações críticas (saúde, financeiro de alto risco).
- Use como **checklist de fitness function de segurança** no pipeline.

### 1.7 OAuth2 + OIDC com Quarkus OIDC

- **OAuth2** — autorização (delegada, escopos).
- **OIDC** — autenticação por cima de OAuth2 (ID token, userinfo).
- **Fluxos**:
  - *Authorization Code with PKCE* — clientes públicos (SPA, mobile).
  - *Client Credentials* — service-to-service (sem usuário humano).
  - *Authorization Code* — backend web tradicional.
  - **NÃO usar**: Password Grant (depreciado), Implicit (depreciado).
- Quarkus:
  ```properties
  quarkus.oidc.auth-server-url=https://idp.exemplo.com/realms/aco
  quarkus.oidc.client-id=aco-pedidos
  quarkus.oidc.credentials.secret=${OIDC_SECRET}
  quarkus.oidc.application-type=service        # ou web-app
  quarkus.oidc.token.principal-claim=preferred_username
  ```
- Em recursos REST:
  ```java
  @GET
  @Path("/admin")
  @RolesAllowed({"admin"})
  public Response admin() { /* ... */ }
  ```

### 1.8 JWT pitfalls

- **Alg=none**: rejeitar. Lista branca de algoritmos (RS256, ES256, HS256 com segredo forte).
- **`kid` confusion**: validar `kid` contra JWKS do IdP, não confiar.
- **`iss` e `aud`**: validar emissor e audiência — sem isso, token de outro tenant passa.
- **`exp`**: validar expiração; janela curta (5–15 min) + refresh token rotativo.
- **`nbf`**: validar "not before".
- **Replay**: para operações críticas, `jti` único + lista de revogação ou token de uso único.
- **Token em URL**: nunca; querystring vaza em logs/referrer.
- **Storage no front**: `HttpOnly` cookie é mais seguro que localStorage.
- **Tamanho**: JWT cresce com claims; em proxy/log, atenção.

### 1.9 Autorização — modelos

- **RBAC** (Role-Based Access Control) — usuário tem papéis; papéis têm permissões. Bom para autz coarse-grained.
- **ABAC** (Attribute-Based Access Control) — política avalia atributos (`if user.dep == doc.dep`). Bom para regras finas.
- **ReBAC** (Relationship-Based, Zanzibar/SpiceDB/OpenFGA) — autz por grafo de relações.
- **Policy as Code** (OPA — Open Policy Agent) — política externa ao código, versionada.
- **Heurística**: começar com RBAC; migrar para ABAC quando regras viram `if` espalhados.

### 1.10 Criptografia — defaults

- **TLS 1.3** mínimo em todo trânsito (interno e externo); HSTS habilitado.
- **mTLS** entre serviços internos (zero-trust).
- **AES-256-GCM** para encriptação simétrica (não AES-CBC sozinho).
- **RSA-2048+** ou **Curve25519** para assimétrica.
- **bcrypt / Argon2** para hash de senha (nunca MD5/SHA-1/SHA-256 sozinho).
- **Não invente cripto** — use bibliotecas auditadas (JDK built-in, BouncyCastle, libsodium binding).
- **HSM / KMS** (AWS KMS, Vault Transit) para chaves mestre; nunca chave mestre em código ou config.

### 1.11 Gestão de segredos

- **NUNCA** segredo no código nem no `application.properties` versionado.
- Usar **Vault** (`quarkus-vault`) ou KMS do cloud provider.
- Rotação automática quando viável (DB credentials dinâmicas via Vault).
- Pipeline com **secret scanning** (TruffleHog/gitleaks) bloqueando PR com segredo detectado.

### 1.12 Supply chain — SBOM, SLSA, dependências

- **SBOM (Software Bill of Materials)** — inventário de toda dependência (direta e transitiva). Formato **CycloneDX** ou SPDX. Gerar por build.
- **SLSA (Supply-chain Levels for Software Artifacts)** — framework de níveis (1–4) de garantia da cadeia (build reproduzível, atestações assinadas).
- **Dependency-Check / Trivy** — scan SCA contra CVE database; falha no pipeline se CVE crítico.
- **Renovate / Dependabot** — PRs automáticos para atualizar dependências.
- **Pin de versão** — sem `LATEST`; checksum quando possível.
- **Cuidado com namespace squatting** (typosquatting): valide cada nova dependência.

### 1.13 Pipeline DevSecOps — controles em cada estágio

```
[commit em pr-*]
    │
    ├── pre-commit hook: secret scan (TruffleHog/gitleaks)
    │
    ▼
[commit stage]
    ├── SAST (Semgrep / SpotBugs+FindSecBugs)
    ├── SCA (Dependency-Check / Trivy)
    ├── Secret scan no diff
    │
    ▼ (merge pr-* → feature/*)
[acceptance stage]
    ├── Container scan (Trivy image)
    ├── IaC scan (Trivy / Checkov se Terraform)
    ├── SBOM gerado (CycloneDX)
    │
    ▼
[quality stages]
    ├── DAST (ZAP em ambiente feature/preview)
    ├── Verificação de headers de segurança
    │
    ▼ ╔══════════════════════════════════════╗
      ║ feature/* → develop fora do escopo    ║
      ╚══════════════════════════════════════╝
```

Toda etapa que falha **bloqueia o pipeline da equipe**; não bypassar.

### 1.14 Headers de segurança HTTP (defaults)

- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `Content-Security-Policy: default-src 'self'` (ajustar por necessidade).
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: no-referrer-when-downgrade`
- `Permissions-Policy: ...` (restringir APIs do browser)
- Em Quarkus, usar `quarkus-http-headers` extension ou filtro JAX-RS.

### 1.15 Logging seguro

- **NUNCA** logar: senha, token (JWT inteiro, OAuth), cartão de crédito, CPF/RG sem mascarar, secret de qualquer tipo.
- **Sempre logar**: evento de segurança (login, falha de autz, mudança de papel, acesso a dado sensível) com contexto (usuário, IP, ação, recurso).
- **Mascaramento**: PII parcial (`***@dominio.com`, `***1234`).
- **Correlação**: incluir `trace_id` para investigar fluxos.

### 1.16 Anti-padrões frequentes

- ❌ "Validamos no front, no backend confia" — todo input é hostil até validado no backend.
- ❌ `ROLE_USER` por default em todo endpoint — sem mapeamento explícito vira A05.
- ❌ JWT armazenado em localStorage — XSS captura.
- ❌ Lista negra de patterns de SQL injection — sempre vaza; usar parametrização.
- ❌ "Authentication bypass" em dev para "facilitar" — código vaza para prod.
- ❌ Secret em variável de ambiente versionada (`.env` no git).
- ❌ `Access-Control-Allow-Origin: *` em endpoint autenticado.
- ❌ `eval` (em qualquer linguagem) com input do usuário.
- ❌ Endpoint admin sem `@RolesAllowed` confiando em "ninguém sabe a URL".
- ❌ Mensagem de erro detalhada para o usuário ("user não existe" vs "credenciais inválidas").

### 1.17 Padrões regulatórios brasileiros (contexto da equipe)

- **LGPD** — base legal para tratamento; minimização; direitos do titular; DPO; comunicação de incidente em 72h.
- **Resoluções BACEN** — circulares específicas por produto (consórcio, crédito, pagamentos).
- **PCI-DSS** — se tocar dado de cartão (default: não tocar; usar tokenização).
- **Open Finance / Open Insurance** — APIs com OAuth2/FAPI + mTLS.

AppSec é consultor obrigatório quando feature toca dado regulado.

## 2. Práticas e heurísticas operacionais

### 2.1 Quando AppSec entra no Replenishment

**Pergunta no item**: qualquer "sim" → AppSec consultado:
- Toca dado pessoal (LGPD), financeiro, de saúde?
- Cria/muda fronteira de confiança (novo cliente externo, novo serviço interno, nova rota pública)?
- Adiciona/altera autenticação ou autorização?
- Adiciona dependência nova?
- Toca em criptografia?
- Toca em log/auditoria?
- Adiciona campo em evento publicado?

### 2.2 Threat model leve em 1 hora

```
1. (10min) Desenhe data flow do escopo da feature — caixas + setas + fronteiras de confiança.
2. (30min) Para cada fronteira de confiança, percorra STRIDE; anote ameaças concretas.
3. (10min) Classifique por (impacto × probabilidade) — alta/média/baixa.
4. (10min) Para cada "alta": mitigar (escreva como) / aceitar / transferir / evitar.
5. Saída: ADR de segurança + fitness function nova (se aplicável).
```

### 2.3 Code review com olhar de segurança — checklist mental

- [ ] Input do usuário vai para SQL? Está parametrizado?
- [ ] Endpoint tem `@RolesAllowed` ou `@Authenticated`?
- [ ] Acesso a recurso por ID valida que o usuário é dono (anti-IDOR)?
- [ ] Sem hardcoded secret no diff?
- [ ] Log contém PII? Mascarado?
- [ ] Tratamento de exceção não vaza stack trace ao cliente?
- [ ] Nova dependência tem CVE? Está em SBOM?
- [ ] Cliente HTTP usa TLS? Valida certificado?
- [ ] JWT lido com validação completa (alg, iss, aud, exp)?
- [ ] Rate limit em endpoint público?
- [ ] CSRF em endpoint de mutação acessado por browser (cookie-auth)?

### 2.4 Anti-padrões organizacionais

- ❌ "AppSec é gatekeeper que só revisa no final" — vira gargalo, gera anti-segurança.
- ❌ "Time aprende segurança quando faz curso" — aprende **fazendo** com coach.
- ❌ "Pen test anual e pronto" — sem shift-left, vira teatro.
- ❌ "Sem AppSec dedicado, dev se vira" — sem owner, segurança é última prioridade na pressão.

### 2.5 Risk Review — entrada do AppSec

- Lista CVEs novos em dependências usadas (Renovate alerts).
- Lista findings de SAST/DAST/Container scan pendentes.
- Lista itens de threat model não mitigados.
- Lista dívida de autz (RBAC simplificado virou ABAC complexo).
- Lista incidentes de segurança (mesmo near-miss).
- Lista regulatório vindo (datas, escopo).

### 2.6 Colaboração

- **PO** — informar se feature tem dado regulado; ASR de segurança.
- **Arquitetos** — fronteiras de confiança, design seguro por padrão.
- **Tech Lead** — code review de segurança junto.
- **Quality Engineer** — testes de autz (cenários positivos e negativos).
- **DevOps** — pipeline DevSecOps, IaC scan, secrets em CI.
- **SRE** — incidente de segurança (resposta), observabilidade.
- **Data Engineer** — criptografia em repouso, mascaramento, retenção.

## 3. Templates e checklists

### 3.1 Template de threat model leve por feature

```markdown
# Threat Model — <Feature/ID>

## Escopo
<O que entra, o que sai, fronteiras de confiança>

## Data Flow
<Diagrama ou descrição textual: ator → boundary → componente → dado>

## Ameaças STRIDE

| ID | Fronteira | Categoria | Ameaça | Impacto | Prob | Decisão | Mitigação |
|----|-----------|-----------|--------|---------|------|---------|-----------|
| T1 | Edge → API | S         | …      | Alto    | Médio| Mitigar | mTLS + OIDC |
| T2 | API → Banco| T        | …      | Alto    | Baixa| Aceitar | -          |

## Fitness functions associadas
- <pipeline check, configuração, teste de autz>

## Aceito / Pendente
- <quem aprovou risco aceito; data>
```

### 3.2 Checklist DevSecOps no pipeline

- [ ] Pre-commit: secret scan (TruffleHog/gitleaks).
- [ ] Commit stage: SAST (Semgrep/SpotBugs+FindSecBugs) configurado e falha em high.
- [ ] Commit stage: SCA (Dependency-Check/Trivy) falha em CVE crítico.
- [ ] Acceptance stage: SBOM gerado e versionado.
- [ ] Acceptance stage: container scan (Trivy image).
- [ ] Acceptance stage: IaC scan se Terraform (Checkov/tfsec/Trivy).
- [ ] Quality stage: DAST (ZAP) em feature/preview.
- [ ] Headers de segurança validados (smoke test).
- [ ] Secret scan periódico no histórico do repo.

### 3.3 Padrão de endpoint protegido (Quarkus)

```java
@Path("/clientes/{id}")
public class ClienteResource {
    @Inject SecurityIdentity identity;
    @Inject ClienteService service;

    @GET
    @RolesAllowed({"cliente", "atendente"})
    @Produces(MediaType.APPLICATION_JSON)
    public ClienteDTO porId(@PathParam("id") UUID id) {
        // Anti-IDOR: cliente só vê o próprio
        if (identity.hasRole("cliente") && !service.pertenceA(id, identity.getPrincipal().getName())) {
            throw new ForbiddenException();
        }
        return service.porIdSeguro(id, identity);
    }
}
```

### 3.4 Template de ADR de segurança

```markdown
# ADR-NNNN: Adotaremos <controle de segurança X> para <ameaça Y>

- Status: Accepted
- ASR/Threat: T-id do threat model
- Risco: <descrição>

## Contexto
<Fronteira de confiança, dado em jogo, atacante plausível>

## Decisão
Adotaremos <controle> (ex.: mTLS entre serviços internos via Istio + autz Keycloak por escopo `pedido.read`/`pedido.write`).

## Consequências
**Positivas**: …
**Negativas**: latência extra, complexidade ops.

## Alternativas
- API key compartilhada — rejeitada (rotação difícil, vaza fácil).
- Network policy só — rejeitada (insuficiente, não identifica chamador).

## Fitness functions
- Smoke test garante 401 sem mTLS, 403 com escopo errado.
- ZAP scan no pipeline confirma sem rota anônima.
```

## 4. Como esta skill é usada pelo agente

Carregada **exclusivamente** pelo agente `equipe-agil-appsec`, **depois** de `equipe-agil-xp-baseline` + `equipe-agil-kanban-method`.

O AppSec usa esta skill para:
- Conduzir threat model leve por feature relevante.
- Definir controles de segurança no pipeline (SAST/DAST/SCA/IaC/secret/SBOM).
- Revisar código com foco em A01-A10 OWASP + API1-10.
- Decidir política de autenticação/autorização com Arquitetos.
- Alimentar Risk Review com ameaças e dívidas.
- Apoiar incidente de segurança (parceria com SRE).

Resto do time **executa** controles; AppSec **policia** e **coacha**.

## References

Bibliografia da seção 3.8 do prompt (apenas crédito — todo o conteúdo necessário já está nas seções 1–3 acima; **não consultar online**):

- *Threat Modeling: Designing for Security* — Shostack
- *The Web Application Hacker's Handbook* (2ª ed.) — Stuttard & Pinto
- *Real-World Cryptography* — Wong
- *OAuth 2 in Action* — Richer & Sanso
- *OWASP Top 10* (web e API) — OWASP Foundation
- *OWASP ASVS* — OWASP Foundation
- *OWASP SAMM* — OWASP Foundation
- *Building Secure & Reliable Systems* — Adkins et al. (Google SRE)
- *DevSecOps: Continuous Security in the Pipeline* — Bird
- *Quarkus Security Documentation* — Red Hat
- *SLSA Framework* — Google/Open Source Security Foundation
- *CycloneDX Specification* — OWASP/Ecma TC54
