---
name: api-documentation-generator
description: "Gere documentação abrangente e amigável para desenvolvedores a partir do código, incluindo endpoints, parâmetros, exemplos e melhores práticas"
---

# Gerador de Documentação de API

## Visão Geral

Gere automaticamente documentação clara e abrangente de API a partir do seu código-fonte. Esta skill ajuda você a criar documentação profissional que inclui descrições de endpoints, exemplos de requisição/resposta, detalhes de autenticação, tratamento de erros e diretrizes de uso.

Perfeita para APIs REST, GraphQL e WebSocket.

## Quando Usar Esta Skill

- Use quando precisar documentar uma nova API
- Use ao atualizar documentação de API existente
- Use quando sua API não tiver documentação clara
- Use ao integrar novos desenvolvedores à sua API
- Use ao preparar documentação de API para usuários externos
- Use ao criar especificações OpenAPI/Swagger

## Como Funciona

### Etapa 1: Analisar a Estrutura da API

Primeiro, examinarei seu código de API para entender:
- Endpoints e rotas disponíveis
- Métodos HTTP (GET, POST, PUT, DELETE, etc.)
- Parâmetros de requisição e estrutura do corpo
- Formatos de resposta e códigos de status
- Requisitos de autenticação e autorização
- Padrões de tratamento de erros

### Etapa 2: Gerar Documentação de Endpoints

Para cada endpoint, criarei documentação incluindo:

**Detalhes do Endpoint:**
- Método HTTP e caminho URL
- Breve descrição do que faz
- Requisitos de autenticação
- Informações de limite de taxa (se aplicável)

**Especificação de Requisição:**
- Parâmetros de caminho
- Parâmetros de query
- Headers de requisição
- Schema do corpo da requisição (com tipos e regras de validação)

**Especificação de Resposta:**
- Resposta de sucesso (código de status + estrutura do corpo)
- Respostas de erro (todos os códigos de erro possíveis)
- Headers de resposta

**Exemplos de Código:**
- Comando cURL
- JavaScript/TypeScript (fetch/axios)
- Python (requests)
- Outras linguagens conforme necessário

### Etapa 3: Adicionar Diretrizes de Uso

Incluirei:
- Guia de início rápido
- Configuração de autenticação
- Casos de uso comuns
- Melhores práticas
- Detalhes de limite de taxa
- Padrões de paginação
- Opções de filtro e ordenação

### Etapa 4: Documentar Tratamento de Erros

Documentação clara de erros incluindo:
- Todos os códigos de erro possíveis
- Formatos de mensagem de erro
- Guia de resolução de problemas
- Cenários de erro comuns e soluções

### Etapa 5: Criar Exemplos Interativos

Quando possível, fornecerei:
- Coleção Postman
- Especificação OpenAPI/Swagger
- Exemplos de código interativos
- Respostas de exemplo

## Exemplos

### Exemplo 1: Documentação de Endpoint REST API

```markdown
## Criar Usuário

Cria uma nova conta de usuário.

**Endpoint:** `POST /api/v1/users`

**Autenticação:** Obrigatória (token Bearer)

**Corpo da Requisição:**
\`\`\`json
{
  "email": "user@example.com",      // Obrigatório: Endereço de email válido
  "password": "SecurePass123!",     // Obrigatório: Min 8 caracteres, 1 maiúscula, 1 número
  "name": "John Doe",               // Obrigatório: 2-50 caracteres
  "role": "user"                    // Opcional: "user" ou "admin" (padrão: "user")
}
\`\`\`

**Resposta de Sucesso (201 Created):**
\`\`\`json
{
  "id": "usr_1234567890",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "createdAt": "2026-01-20T10:30:00Z",
  "emailVerified": false
}
\`\`\`

**Respostas de Erro:**

- `400 Bad Request` - Dados de entrada inválidos
  \`\`\`json
  {
    "error": "VALIDATION_ERROR",
    "message": "Formato de email inválido",
    "field": "email"
  }
  \`\`\`

- `409 Conflict` - Email já existe
  \`\`\`json
  {
    "error": "EMAIL_EXISTS",
    "message": "Já existe uma conta com este email"
  }
  \`\`\`

- `401 Unauthorized` - Token de autenticação ausente ou inválido

**Exemplo de Requisição (cURL):**
\`\`\`bash
curl -X POST https://api.example.com/api/v1/users \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "name": "John Doe"
  }'
\`\`\`

**Exemplo de Requisição (JavaScript):**
\`\`\`javascript
const response = await fetch('https://api.example.com/api/v1/users', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'SecurePass123!',
    name: 'John Doe'
  })
});

const user = await response.json();
console.log(user);
\`\`\`

**Exemplo de Requisição (Python):**
\`\`\`python
import requests

response = requests.post(
    'https://api.example.com/api/v1/users',
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    },
    json={
        'email': 'user@example.com',
        'password': 'SecurePass123!',
        'name': 'John Doe'
    }
)

user = response.json()
print(user)
\`\`\`
```

### Exemplo 2: Documentação de GraphQL API

```markdown
## Consulta de Usuário

Busca informações do usuário por ID.

**Consulta:**
\`\`\`graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    email
    name
    role
    createdAt
    posts {
      id
      title
      publishedAt
    }
  }
}
\`\`\`

**Variáveis:**
\`\`\`json
{
  "id": "usr_1234567890"
}
\`\`\`

**Resposta:**
\`\`\`json
{
  "data": {
    "user": {
      "id": "usr_1234567890",
      "email": "user@example.com",
      "name": "John Doe",
      "role": "user",
      "createdAt": "2026-01-20T10:30:00Z",
      "posts": [
        {
          "id": "post_123",
          "title": "Meu Primeiro Post",
          "publishedAt": "2026-01-21T14:00:00Z"
        }
      ]
    }
  }
}
\`\`\`

**Erros:**
\`\`\`json
{
  "errors": [
    {
      "message": "Usuário não encontrado",
      "extensions": {
        "code": "USER_NOT_FOUND",
        "userId": "usr_1234567890"
      }
    }
  ]
}
\`\`\`
```

### Exemplo 3: Documentação de Autenticação

```markdown
## Autenticação

Todas as requisições de API requerem autenticação usando tokens Bearer.

### Obter um Token

**Endpoint:** `POST /api/v1/auth/login`

**Requisição:**
\`\`\`json
{
  "email": "user@example.com",
  "password": "sua-senha"
}
\`\`\`

**Resposta:**
\`\`\`json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresIn": 3600,
  "refreshToken": "refresh_token_here"
}
\`\`\`

### Usar o Token

Inclua o token no header de Authorization:

\`\`\`
Authorization: Bearer YOUR_TOKEN
\`\`\`

### Expiração do Token

Os tokens expiram após 1 hora. Use o refresh token para obter um novo token de acesso:

**Endpoint:** `POST /api/v1/auth/refresh`

**Requisição:**
\`\`\`json
{
  "refreshToken": "refresh_token_here"
}
\`\`\`
```

## Melhores Práticas

### ✅ Faça Isto

- **Seja Consistente** - Use o mesmo formato para todos os endpoints
- **Inclua Exemplos** - Forneça exemplos de código funcionais em múltiplas linguagens
- **Documente Erros** - Liste todos os códigos de erro possíveis e seus significados
- **Mostre Dados Reais** - Use dados de exemplo realistas, não "foo" e "bar"
- **Explique Parâmetros** - Descreva o que cada parâmetro faz e suas restrições
- **Versione Sua API** - Inclua números de versão em URLs (/api/v1/)
- **Adicione Timestamps** - Mostre quando a documentação foi atualizada pela última vez
- **Vincule Endpoints Relacionados** - Ajude os usuários a descobrir funcionalidade relacionada
- **Inclua Limites de Taxa** - Documente todas as políticas de limitação de taxa
- **Forneça Coleção Postman** - Facilite o teste de sua API

### ❌ Não Faça Isto

- **Não Pule Casos de Erro** - Os usuários precisam saber o que pode dar errado
- **Não Use Descrições Vagas** - "Obtém dados" não é útil
- **Não Esqueça Autenticação** - Sempre documente requisitos de autenticação
- **Não Ignore Casos Extremos** - Documente paginação, filtro, ordenação
- **Não Deixe Exemplos Quebrados** - Teste todos os exemplos de código
- **Não Use Informações Desatualizadas** - Mantenha documentação sincronizada com código
- **Não Complique Demais** - Mantenha simples e fácil de escanear
- **Não Esqueça Response Headers** - Documente headers importantes

## Estrutura de Documentação

### Seções Recomendadas

1. **Introdução**
   - O que a API faz
   - URL base
   - Versão da API
   - Contato de suporte

2. **Autenticação**
   - Como autenticar
   - Gerenciamento de token
   - Melhores práticas de segurança

3. **Início Rápido**
   - Exemplo simples para começar
   - Passo a passo de caso de uso comum

4. **Endpoints**
   - Organizados por recurso
   - Detalhes completos para cada endpoint

5. **Modelos de Dados**
   - Definições de schema
   - Descrições de campos
   - Regras de validação

6. **Tratamento de Erros**
   - Referência de códigos de erro
   - Formato de resposta de erro
   - Guia de resolução de problemas

7. **Limite de Taxa**
   - Limites e quotas
   - Headers para verificar
   - Tratamento de erros de limite de taxa

8. **Changelog**
   - Histórico de versão da API
   - Mudanças incompatíveis
   - Avisos de descontinuação

9. **SDKs e Ferramentas**
   - Bibliotecas cliente oficiais
   - Coleção Postman
   - Especificação OpenAPI

## Armadilhas Comuns

### Problema: Documentação Fica Desatualizada
**Sintomas:** Exemplos não funcionam, parâmetros estão errados, endpoints retornam dados diferentes
**Solução:**
- Gere documentação a partir de comentários/anotações de código
- Use ferramentas como Swagger/OpenAPI
- Adicione testes de API que validem documentação
- Revise documentação a cada mudança de API

### Problema: Documentação de Erro Ausente
**Sintomas:** Usuários não sabem como lidar com erros, tickets de suporte aumentam
**Solução:**
- Documente cada código de erro possível
- Forneça mensagens de erro claras
- Inclua etapas de resolução de problemas
- Mostre exemplos de respostas de erro

### Problema: Exemplos Não Funcionam
**Sintomas:** Usuários não conseguem começar, frustração aumenta
**Solução:**
- Teste cada exemplo de código
- Use endpoints reais e funcionais
- Inclua exemplos completos (não fragmentos)
- Forneça um ambiente sandbox

### Problema: Requisitos de Parâmetro Pouco Claros
**Sintomas:** Usuários enviam requisições inválidas, erros de validação
**Solução:**
- Marque claramente obrigatório vs opcional
- Documente tipos de dados e formatos
- Mostre regras de validação
- Forneça valores de exemplo

## Ferramentas e Formatos

### OpenAPI/Swagger
Gere documentação interativa:
```yaml
openapi: 3.0.0
info:
  title: Minha API
  version: 1.0.0
paths:
  /users:
    post:
      summary: Criar um novo usuário
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
```

### Coleção Postman
Exporte coleção para teste fácil:
```json
{
  "info": {
    "name": "Minha API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Criar Usuário",
      "request": {
        "method": "POST",
        "url": "{{baseUrl}}/api/v1/users"
      }
    }
  ]
}
```

## Skills Relacionadas

- `@doc-coauthoring` - Para escrita colaborativa de documentação
- `@copywriting` - Para descrições claras e amigáveis ao usuário
- `@test-driven-development` - Para garantir que o comportamento de API corresponda à documentação
- `@systematic-debugging` - Para resolução de problemas de API

## Recursos Adicionais

- [Especificação OpenAPI](https://swagger.io/specification/)
- [Melhores Práticas de API REST](https://restfulapi.net/)
- [Documentação GraphQL](https://graphql.org/learn/)
- [Padrões de Design de API](https://www.apiguide.com/)
- [Documentação Postman](https://learning.postman.com/docs/)

---

**Dica Pro:** Mantenha sua documentação de API o mais próximo possível do seu código. Use ferramentas que gerem documentação a partir de comentários de código para garantir que fiquem sincronizadas!