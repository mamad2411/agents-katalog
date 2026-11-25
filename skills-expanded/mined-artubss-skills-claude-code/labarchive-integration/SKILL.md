---
name: labarchive-integration
description: "Integração com API de caderno eletrônico de laboratório. Acesse cadernos, gerencie entradas/anexos, faça backup de cadernos, integre com Protocols.io/Jupyter/REDCap, para workflows de ELN programáticos."
---

# Integração LabArchives

## Visão Geral

LabArchives é uma plataforma de caderno eletrônico de laboratório para documentação de pesquisa e gerenciamento de dados. Acesse cadernos, gerencie entradas e anexos, gere relatórios e integre com ferramentas de terceiros de forma programática via REST API.

## Quando Usar Esta Skill

Esta skill deve ser usada quando:
- Trabalhar com REST API do LabArchives para automação de cadernos
- Fazer backup de cadernos de forma programática
- Criar ou gerenciar entradas e anexos de cadernos
- Gerar relatórios de site e análises
- Integrar LabArchives com ferramentas de terceiros (Protocols.io, Jupyter, REDCap)
- Automatizar upload de dados para cadernos eletrônicos de laboratório
- Gerenciar acesso de usuários e permissões de forma programática

## Capacidades Principais

### 1. Autenticação e Configuração

Configure credenciais de acesso à API e endpoints regionais para integração com LabArchives API.

**Pré-requisitos:**
- Licença enterprise LabArchives com acesso à API habilitado
- ID de chave de acesso e senha da API fornecidos pelo administrador LabArchives
- Credenciais de autenticação do usuário (email e senha de aplicações externas)

**Configuração de setup:**

Use o script `scripts/setup_config.py` para criar um arquivo de configuração:

```bash
python3 scripts/setup_config.py
```

Isso cria um arquivo `config.yaml` com a seguinte estrutura:

```yaml
api_url: https://api.labarchives.com/api  # ou endpoint regional
access_key_id: YOUR_ACCESS_KEY_ID
access_password: YOUR_ACCESS_PASSWORD
```

**Endpoints regionais de API:**
- EUA/Internacional: `https://api.labarchives.com/api`
- Austrália: `https://auapi.labarchives.com/api`
- Reino Unido: `https://ukapi.labarchives.com/api`

Para instruções de autenticação detalhadas e resolução de problemas, consulte `references/authentication_guide.md`.

### 2. Recuperação de Informações do Usuário

Obtenha ID do usuário (UID) e informações de acesso necessárias para operações subsequentes de API.

**Fluxo de trabalho:**

1. Chame o método de API `users/user_access_info` com credenciais de login
2. Analise a resposta XML/JSON para extrair o ID do usuário (UID)
3. Use o UID para recuperar informações detalhadas do usuário via `users/user_info_via_id`

**Exemplo usando wrapper Python:**

```python
from labarchivespy.client import Client

# Initialize client
client = Client(api_url, access_key_id, access_password)

# Get user access info
login_params = {'login_or_email': user_email, 'password': auth_token}
response = client.make_call('users', 'user_access_info', params=login_params)

# Extract UID from response
import xml.etree.ElementTree as ET
uid = ET.fromstring(response.content)[0].text

# Get detailed user info
params = {'uid': uid}
user_info = client.make_call('users', 'user_info_via_id', params=params)
```

### 3. Operações de Caderno

Gerencie acesso a cadernos, backup e recuperação de metadados.

**Operações-chave:**

- **Listar cadernos:** Recupere todos os cadernos acessíveis para um usuário
- **Fazer backup de cadernos:** Baixe dados completos de cadernos com inclusão opcional de anexos
- **Obter IDs de cadernos:** Recupere identificadores de cadernos definidos pela instituição para integração com sistemas de gestão de projetos/bolsas
- **Obter membros do caderno:** Liste todos os usuários com acesso a um caderno específico
- **Obter configurações do caderno:** Recupere configuração e permissões para cadernos

**Exemplo de backup de caderno:**

Use o script `scripts/notebook_operations.py`:

```bash
# Backup com anexos (padrão, cria arquivo 7z)
python3 scripts/notebook_operations.py backup --uid USER_ID --nbid NOTEBOOK_ID

# Backup sem anexos, formato JSON
python3 scripts/notebook_operations.py backup --uid USER_ID --nbid NOTEBOOK_ID --json --no-attachments
```

**Formato de endpoint de API:**
```
https://<api_url>/notebooks/notebook_backup?uid=<UID>&nbid=<NOTEBOOK_ID>&json=true&no_attachments=false
```

Para documentação abrangente de métodos de API, consulte `references/api_reference.md`.

### 4. Gerenciamento de Entradas e Anexos

Crie, modifique e gerencie entradas de cadernos e anexos de arquivo.

**Operações de entrada:**
- Criar novas entradas em cadernos
- Adicionar comentários a entradas existentes
- Criar partes/componentes de entrada
- Upload de anexos de arquivo para entradas

**Fluxo de trabalho de anexos:**

Use o script `scripts/entry_operations.py`:

```bash
# Upload de anexo para uma entrada
python3 scripts/entry_operations.py upload --uid USER_ID --nbid NOTEBOOK_ID --entry-id ENTRY_ID --file /path/to/file.pdf

# Criar uma nova entrada com conteúdo de texto
python3 scripts/entry_operations.py create --uid USER_ID --nbid NOTEBOOK_ID --title "Resultados do Experimento" --content "Resultados do experimento de hoje..."
```

**Tipos de arquivo suportados:**
- Documentos (PDF, DOCX, TXT)
- Imagens (PNG, JPG, TIFF)
- Arquivos de dados (CSV, XLSX, HDF5)
- Formatos científicos (CIF, MOL, PDB)
- Arquivos (ZIP, 7Z)

### 5. Relatórios de Site e Análises

Gere relatórios institucionais sobre uso de cadernos, atividade e conformidade (recurso Enterprise).

**Relatórios disponíveis:**
- Relatório de Uso Detalhado: Métricas de atividade do usuário e estatísticas de engajamento
- Relatório Detalhado de Caderno: Metadados do caderno, listas de membros e configurações
- Relatório de Geração de Caderno PDF/Offline: Rastreamento de exportação para conformidade
- Relatório de Membros do Caderno: Controle de acesso e análises de colaboração
- Relatório de Configurações do Caderno: Auditoria de configuração e permissões

**Geração de relatório:**

```python
# Generate detailed usage report
response = client.make_call('site_reports', 'detailed_usage_report',
                           params={'start_date': '2025-01-01', 'end_date': '2025-10-20'})
```

### 6. Integrações de Terceiros

LabArchives integra-se com numerosas plataformas de software científico. Esta skill fornece orientação sobre o aproveitamento dessas integrações de forma programática.

**Integrações suportadas:**
- **Protocols.io:** Exporte protocolos diretamente para cadernos LabArchives
- **GraphPad Prism:** Exporte análises e figuras (Versão 8+)
- **SnapGene:** Integração direta de workflow de biologia molecular
- **Geneious:** Exportação de análise de bioinformática
- **Jupyter:** Incorpore notebooks Jupyter como entradas
- **REDCap:** Integração de captura de dados clínicos
- **Qeios:** Plataforma de publicação de pesquisa
- **SciSpace:** Gerenciamento de literatura

**Autenticação OAuth:**
LabArchives agora usa OAuth para todas as novas integrações. Integrações legadas podem usar autenticação de chave de API.

Para instruções detalhadas de setup de integração e casos de uso, consulte `references/integrations.md`.

## Fluxos de Trabalho Comuns

### Fluxo de trabalho completo de backup de caderno

1. Autentique e obtenha ID do usuário
2. Liste todos os cadernos acessíveis
3. Itere através de cadernos e faça backup de cada um
4. Armazene backups com metadados de timestamp

```bash
# Script de backup completo
python3 scripts/notebook_operations.py backup-all --email user@example.edu --password AUTH_TOKEN
```

### Fluxo de trabalho de upload automático de dados

1. Autentique com API LabArchives
2. Identifique caderno e entrada de destino
3. Faça upload de arquivos de dados experimentais
4. Adicione comentários de metadados a entradas
5. Gere relatório de atividade

### Exemplo de fluxo de trabalho de integração (Jupyter → LabArchives)

1. Exporte notebook Jupyter para HTML ou PDF
2. Use entry_operations.py para fazer upload para LabArchives
3. Adicione comentário com timestamp de execução e informações de ambiente
4. Marque entrada para fácil recuperação

## Instalação de Pacote Python

Instale o wrapper `labarchives-py` para acesso simplificado de API:

```bash
git clone https://github.com/mcmero/labarchives-py
cd labarchives-py
uv pip install .
```

Alternativamente, use requisições HTTP diretas via biblioteca `requests` do Python para implementações customizadas.

## Melhores Práticas

1. **Rate limiting:** Implemente atrasos apropriados entre chamadas de API para evitar throttling
2. **Tratamento de erros:** Sempre envolva chamadas de API em blocos try-except com logging apropriado
3. **Segurança de autenticação:** Armazene credenciais em variáveis de ambiente ou arquivos de configuração seguros (nunca em código)
4. **Verificação de backup:** Após backup de caderno, verifique integridade e completude do arquivo
5. **Operações incrementais:** Para cadernos grandes, use paginação e processamento em lotes
6. **Endpoints regionais:** Use o endpoint regional correto de API para desempenho otimizado

## Resolução de Problemas

**Problemas comuns:**

- **401 Unauthorized:** Verifique se ID de chave de acesso e senha estão corretos; confirme se acesso à API está habilitado para sua conta
- **404 Not Found:** Confirme que ID de caderno (nbid) existe e usuário tem permissões de acesso
- **403 Forbidden:** Verifique permissões do usuário para a operação solicitada
- **Resposta vazia:** Certifique-se de que parâmetros obrigatórios (uid, nbid) são fornecidos corretamente
- **Falhas de upload de anexo:** Verifique limites de tamanho de arquivo e compatibilidade de formato

Para suporte adicional, contate LabArchives em support@labarchives.com.

## Recursos

Esta skill inclui recursos agrupados para suportar integração com LabArchives API:

### scripts/

- `setup_config.py`: Gerador de arquivo de configuração interativo para credenciais de API
- `notebook_operations.py`: Utilitários para listar, fazer backup e gerenciar cadernos
- `entry_operations.py`: Ferramentas para criar entradas e fazer upload de anexos

### references/

- `api_reference.md`: Documentação abrangente de endpoint de API com parâmetros e exemplos
- `authentication_guide.md`: Instruções detalhadas de setup de autenticação e configuração
- `integrations.md`: Guias de setup de integração de terceiros e casos de uso