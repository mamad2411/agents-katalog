---
name: protocolsio-integration
description: Integração com a API protocols.io para gerenciar protocolos científicos. Esta skill deve ser usada ao trabalhar com protocols.io para pesquisar, criar, atualizar ou publicar protocolos; gerenciar etapas e materiais de protocolo; lidar com discussões e comentários; organizar espaços de trabalho; fazer upload e gerenciar arquivos; ou integrar funcionalidade protocols.io em workflows. Aplicável para descoberta de protocolo, desenvolvimento colaborativo de protocolo, rastreamento de experimentos, gerenciamento de protocolo de laboratório e documentação científica.
---

# Integração Protocols.io

## Visão Geral

Protocols.io é uma plataforma abrangente para desenvolver, compartilhar e gerenciar protocolos científicos. Esta skill oferece integração completa com a API v3 protocols.io, permitindo acesso programático a protocolos, espaços de trabalho, discussões, gerenciamento de arquivos e recursos de colaboração.

## Quando Usar Esta Skill

Use esta skill ao trabalhar com protocols.io em qualquer um dos seguintes cenários:

- **Descoberta de Protocolo**: Pesquisar protocolos existentes por palavras-chave, DOI ou categoria
- **Gerenciamento de Protocolo**: Criar, atualizar ou publicar protocolos científicos
- **Gerenciamento de Etapas**: Adicionar, editar ou organizar etapas e procedimentos de protocolo
- **Desenvolvimento Colaborativo**: Trabalhar com membros da equipe em protocolos compartilhados
- **Organização do Espaço de Trabalho**: Gerenciar repositórios de protocolo de laboratório ou institucionais
- **Discussão e Feedback**: Adicionar ou responder comentários de protocolo
- **Gerenciamento de Arquivos**: Fazer upload de arquivos de dados, imagens ou documentos para protocolos
- **Rastreamento de Experimentos**: Documentar execuções de protocolo e resultados
- **Exportação de Dados**: Fazer backup ou migrar coleções de protocolo
- **Projetos de Integração**: Criar ferramentas que interagem com protocols.io

## Capacidades Principais

Esta skill oferece orientação abrangente em cinco áreas principais de capacidade:

### 1. Autenticação e Acesso

Gerenciar autenticação de API usando tokens de acesso e fluxos OAuth. Inclui tanto tokens de acesso do cliente (para conteúdo pessoal) quanto tokens OAuth (para aplicações multi-usuário).

**Operações principais:**
- Gerar links de autorização para fluxo OAuth
- Trocar códigos de autorização por tokens de acesso
- Renovar tokens expirados
- Gerenciar limites de taxa e permissões

**Referência:** Leia `references/authentication.md` para procedimentos detalhados de autenticação, implementação OAuth e melhores práticas de segurança.

### 2. Operações de Protocolo

Gerenciamento completo do ciclo de vida de protocolo, desde criação até publicação.

**Operações principais:**
- Pesquisar e descobrir protocolos por palavras-chave, filtros ou DOI
- Recuperar informações detalhadas de protocolo com todas as etapas
- Criar novos protocolos com metadados e tags
- Atualizar informações e configurações de protocolo
- Gerenciar etapas de protocolo (criar, atualizar, deletar, reordenar)
- Tratar materiais e reagentes de protocolo
- Publicar protocolos com emissão de DOI
- Marcar protocolos para acesso rápido
- Gerar PDFs de protocolo

**Referência:** Leia `references/protocols_api.md` para orientação abrangente sobre gerenciamento de protocolo, incluindo endpoints da API, parâmetros, workflows comuns e exemplos.

### 3. Discussões e Colaboração

Habilitar engajamento comunitário através de comentários e discussões.

**Operações principais:**
- Visualizar comentários no nível de protocolo e etapa
- Criar novos comentários e respostas encadeadas
- Editar ou deletar seus próprios comentários
- Analisar padrões de discussão e feedback
- Responder a perguntas e problemas de usuários

**Referência:** Leia `references/discussions.md` para gerenciamento de discussão, encadeamento de comentários e workflows de colaboração.

### 4. Gerenciamento de Espaço de Trabalho

Organizar protocolos dentro de espaços de trabalho de equipe com permissões baseadas em funções.

**Operações principais:**
- Listar e acessar espaços de trabalho do usuário
- Recuperar detalhes do espaço de trabalho e listas de membros
- Solicitar acesso ou ingressar em espaços de trabalho
- Listar protocolos específicos do espaço de trabalho
- Criar protocolos dentro de espaços de trabalho
- Gerenciar permissões e colaboração do espaço de trabalho

**Referência:** Leia `references/workspaces.md` para organização do espaço de trabalho, gerenciamento de permissões e padrões de colaboração em equipe.

### 5. Operações de Arquivo

Upload, organização e gerenciamento de arquivos associados a protocolos.

**Operações principais:**
- Pesquisar arquivos e pastas do espaço de trabalho
- Fazer upload de arquivos com metadados e tags
- Baixar arquivos e verificar uploads
- Organizar arquivos em hierarquias de pasta
- Atualizar metadados de arquivo
- Deletar e restaurar arquivos
- Gerenciar armazenamento e organização

**Referência:** Leia `references/file_manager.md` para procedimentos de upload de arquivo, estratégias de organização e gerenciamento de armazenamento.

### 6. Funcionalidades Adicionais

Funcionalidade complementar incluindo perfis, notificações e exportações.

**Operações principais:**
- Gerenciar perfis e configurações de usuário
- Consultar protocolos publicados recentemente
- Criar e rastrear registros de experimento
- Receber e gerenciar notificações
- Exportar dados da organização para arquivo

**Referência:** Leia `references/additional_features.md` para gerenciamento de perfil, descoberta de publicação, rastreamento de experimento e exportação de dados.

## Começando

### Passo 1: Configuração de Autenticação

Antes de usar qualquer funcionalidade da API protocols.io:

1. Obter um token de acesso (CLIENT_ACCESS_TOKEN ou OAUTH_ACCESS_TOKEN)
2. Ler `references/authentication.md` para procedimentos detalhados de autenticação
3. Armazenar o token com segurança
4. Incluir em todas as solicitações como: `Authorization: Bearer YOUR_TOKEN`

### Passo 2: Identificar Seu Caso de Uso

Determine qual área de capacidade atende suas necessidades:

- **Trabalhando com protocolos?** → Leia `references/protocols_api.md`
- **Gerenciando protocolos de equipe?** → Leia `references/workspaces.md`
- **Tratando comentários/feedback?** → Leia `references/discussions.md`
- **Fazendo upload de arquivos/dados?** → Leia `references/file_manager.md`
- **Rastreando experimentos ou perfis?** → Leia `references/additional_features.md`

### Passo 3: Implementar Integração

Siga a orientação nos arquivos de referência relevantes:

- Cada referência inclui documentação detalhada de endpoint
- Parâmetros de API e formatos de solicitação/resposta são especificados
- Casos de uso comuns e workflows são fornecidos com exemplos
- Orientação de melhores práticas e tratamento de erros incluída

## URL Base e Formato de Solicitação

Todas as solicitações de API usam a URL base:
```
https://protocols.io/api/v3
```

Todas as solicitações requerem o cabeçalho Authorization:
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

A maioria dos endpoints suporta formato de solicitação/resposta JSON com `Content-Type: application/json`.

## Opções de Formato de Conteúdo

Muitos endpoints suportam um parâmetro `content_format` para controlar como o conteúdo do protocolo é retornado:

- `json`: Formato Draft.js JSON (padrão)
- `html`: Formato HTML
- `markdown`: Formato Markdown

Incluir como parâmetro de query: `?content_format=html`

## Limite de Taxa

Esteja ciente dos limites de taxa da API:

- **Endpoints padrão**: 100 solicitações por minuto por usuário
- **Endpoint de PDF**: 5 solicitações/minuto (conectado), 3 solicitações/minuto (não conectado)

Implementar backoff exponencial para erros de limite de taxa (HTTP 429).

## Workflows Comuns

### Workflow 1: Importar e Analisar Protocolo

Para analisar um protocolo existente de protocols.io:

1. **Pesquisar**: Use `GET /protocols` com palavras-chave para encontrar protocolos relevantes
2. **Recuperar**: Obter detalhes completos com `GET /protocols/{protocol_id}`
3. **Extrair**: Analisar etapas, materiais e metadados para análise
4. **Revisar discussões**: Verificar `GET /protocols/{id}/comments` para feedback de usuários
5. **Exportar**: Gerar PDF se necessário para referência offline

**Arquivos de referência**: `protocols_api.md`, `discussions.md`

### Workflow 2: Criar e Publicar Protocolo

Para criar um novo protocolo e publicar com DOI:

1. **Autenticar**: Garantir que você tenha token de acesso válido (ver `authentication.md`)
2. **Criar**: Use `POST /protocols` com título e descrição
3. **Adicionar etapas**: Para cada etapa, use `POST /protocols/{id}/steps`
4. **Adicionar materiais**: Documentar reagentes em componentes de etapa
5. **Revisar**: Verificar se todo conteúdo está completo e preciso
6. **Publicar**: Emitir DOI com `POST /protocols/{id}/publish`

**Arquivos de referência**: `protocols_api.md`, `authentication.md`

### Workflow 3: Espaço de Trabalho de Laboratório Colaborativo

Para configurar gerenciamento de protocolo de equipe:

1. **Criar/ingressar no espaço de trabalho**: Acessar ou solicitar associação ao espaço de trabalho (ver `workspaces.md`)
2. **Organizar estrutura**: Criar hierarquia de pasta para protocolos de laboratório (ver `file_manager.md`)
3. **Criar protocolos**: Use `POST /workspaces/{id}/protocols` para protocolos de equipe
4. **Fazer upload de arquivos**: Adicionar dados experimentais e imagens
5. **Habilitar discussões**: Membros da equipe podem comentar e fornecer feedback
6. **Rastrear experimentos**: Documentar execuções de protocolo com registros de experimento

**Arquivos de referência**: `workspaces.md`, `file_manager.md`, `protocols_api.md`, `discussions.md`, `additional_features.md`

### Workflow 4: Documentação de Experimento

Para rastrear execuções de protocolo e resultados:

1. **Executar protocolo**: Realizar protocolo em laboratório
2. **Fazer upload de dados**: Use File Manager API para fazer upload de resultados (ver `file_manager.md`)
3. **Criar registro**: Documentar execução com `POST /protocols/{id}/runs`
4. **Vincular arquivos**: Referenciar arquivos de dados enviados em registro de experimento
5. **Anotar modificações**: Documentar quaisquer desvios ou otimizações de protocolo
6. **Analisar**: Revisar múltiplas execuções para avaliação de reprodutibilidade

**Arquivos de referência**: `additional_features.md`, `file_manager.md`, `protocols_api.md`

### Workflow 5: Descoberta e Citação de Protocolo

Para encontrar e citar protocolos em pesquisa:

1. **Pesquisar**: Consultar protocolos publicados com `GET /publications`
2. **Filtrar**: Usar filtros de categoria e palavra-chave para protocolos relevantes
3. **Revisar**: Ler detalhes de protocolo e comentários da comunidade
4. **Marcar**: Salvar protocolos úteis com `POST /protocols/{id}/bookmarks`
5. **Citar**: Usar DOI de protocolo em publicações (atribuição apropriada)
6. **Exportar PDF**: Gerar PDF formatado para referência offline

**Arquivos de referência**: `protocols_api.md`, `additional_features.md`

## Exemplos de Solicitações Python

### Pesquisa Básica de Protocolo

```python
import requests

token = "YOUR_ACCESS_TOKEN"
headers = {"Authorization": f"Bearer {token}"}

# Pesquisar protocolos CRISPR
response = requests.get(
    "https://protocols.io/api/v3/protocols",
    headers=headers,
    params={
        "filter": "public",
        "key": "CRISPR",
        "page_size": 10,
        "content_format": "html"
    }
)

protocols = response.json()
for protocol in protocols["items"]:
    print(f"{protocol['title']} - {protocol['doi']}")
```

### Criar Novo Protocolo

```python
import requests

token = "YOUR_ACCESS_TOKEN"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Criar protocolo
data = {
    "title": "CRISPR-Cas9 Gene Editing Protocol",
    "description": "Comprehensive protocol for CRISPR gene editing",
    "tags": ["CRISPR", "gene editing", "molecular biology"]
}

response = requests.post(
    "https://protocols.io/api/v3/protocols",
    headers=headers,
    json=data
)

protocol_id = response.json()["item"]["id"]
print(f"Created protocol: {protocol_id}")
```

### Fazer Upload de Arquivo para Espaço de Trabalho

```python
import requests

token = "YOUR_ACCESS_TOKEN"
headers = {"Authorization": f"Bearer {token}"}

# Fazer upload de arquivo
with open("data.csv", "rb") as f:
    files = {"file": f}
    data = {
        "folder_id": "root",
        "description": "Experimental results",
        "tags": "experiment,data,2025"
    }

    response = requests.post(
        "https://protocols.io/api/v3/workspaces/12345/files/upload",
        headers=headers,
        files=files,
        data=data
    )

file_id = response.json()["item"]["id"]
print(f"Uploaded file: {file_id}")
```

## Tratamento de Erros

Implementar tratamento robusto de erros para solicitações de API:

```python
import requests
import time

def make_request_with_retry(url, headers, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limit
                retry_after = int(response.headers.get('Retry-After', 60))
                time.sleep(retry_after)
                continue
            elif response.status_code >= 500:  # Server error
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                response.raise_for_status()

        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)

    raise Exception("Max retries exceeded")
```

## Arquivos de Referência

Carregue o arquivo de referência apropriado baseado em sua tarefa:

- **`authentication.md`**: Fluxos OAuth, gerenciamento de token, limite de taxa
- **`protocols_api.md`**: CRUD de protocolo, etapas, materiais, publicação, PDFs
- **`discussions.md`**: Comentários, respostas, colaboração
- **`workspaces.md`**: Espaços de trabalho de equipe, permissões, organização
- **`file_manager.md`**: Upload de arquivo, pastas, gerenciamento de armazenamento
- **`additional_features.md`**: Perfis, publicações, experimentos, notificações

Para carregar um arquivo de referência, leia o arquivo do diretório `references/` quando necessário para funcionalidade específica.

## Melhores Práticas

1. **Autenticação**: Armazenar tokens com segurança, nunca em código ou controle de versão
2. **Limite de Taxa**: Implementar backoff exponencial e respeitar limites de taxa
3. **Tratamento de Erros**: Lidar com todos os códigos de erro HTTP apropriadamente
4. **Validação de Dados**: Validar entrada antes de chamadas de API
5. **Documentação**: Documentar etapas de protocolo completamente
6. **Colaboração**: Usar comentários e discussões para comunicação de equipe
7. **Organização**: Manter convenções de nomenclatura e tagging consistentes
8. **Versionamento**: Rastrear versões de protocolo ao fazer atualizações
9. **Atribuição**: Citar protocolo apropriadamente usando DOIs
10. **Backup**: Exportar regularmente protocolos importantes e dados de espaço de trabalho

## Recursos Adicionais

- **Documentação Oficial da API**: https://apidoc.protocols.io/
- **Plataforma Protocols.io**: https://www.protocols.io/
- **Suporte**: Contacte o suporte protocols.io para acesso à API e problemas técnicos
- **Comunidade**: Engajar com a comunidade protocols.io para melhores práticas

## Solução de Problemas

**Problemas de Autenticação:**
- Verificar se o token é válido e não expirou
- Verificar formato do cabeçalho Authorization: `Bearer YOUR_TOKEN`
- Garantir tipo de token apropriado (CLIENT vs OAUTH)

**Limite de Taxa:**
- Implementar backoff exponencial para erros 429
- Monitorar frequência de solicitações
- Considerar cache para solicitações frequentes

**Erros de Permissão:**
- Verificar permissões de acesso de espaço de trabalho/protocolo
- Verificar função de usuário no espaço de trabalho
- Garantir que protocolo não seja privado se acessando sem permissão

**Falhas de Upload de Arquivo:**
- Verificar tamanho do arquivo contra limites do espaço de trabalho
- Verificar se tipo de arquivo é suportado
- Garantir que codificação multipart/form-data está correta

Para orientação detalhada de solução de problemas, consulte os arquivos de referência específicos cobrindo cada área de capacidade.