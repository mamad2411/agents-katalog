---
name: omero-integration
description: "Plataforma de gerenciamento de dados de microscopia. Acesse imagens via Python, recupere datasets, analise pixels, gerencie ROIs/anotações, processamento em lote, para triagem de alto conteúdo e workflows de microscopia."
---

# Integração OMERO

## Visão Geral

OMERO é uma plataforma de código aberto para gerenciar, visualizar e analisar imagens de microscopia e metadados. Acesse imagens via API Python, recupere datasets, analise pixels, gerencie ROIs e anotações, para triagem de alto conteúdo e workflows de microscopia.

## Quando Usar Esta Habilidade

Esta habilidade deve ser utilizada quando:
- Trabalhar com API Python do OMERO (omero-py) para acessar dados de microscopia
- Recuperar imagens, datasets, projetos ou dados de triagem programaticamente
- Analisar dados de pixels e criar imagens derivadas
- Criar ou gerenciar ROIs (regiões de interesse) em imagens de microscopia
- Adicionar anotações, tags ou metadados a objetos OMERO
- Armazenar resultados de medições em tabelas OMERO
- Criar scripts do lado do servidor para processamento em lote
- Realizar análise de triagem de alto conteúdo

## Capacidades Principais

Esta habilidade cobre oito áreas de capacidade principais. Cada uma é documentada em detalhes no diretório references/:

### 1. Gerenciamento de Conexão e Sessão
**Arquivo**: `references/connection.md`

Estabeleça conexões seguras com servidores OMERO, gerencie sessões, trate autenticação e trabalhe com contextos de grupo. Use isso para padrões de configuração inicial e conexão.

**Cenários comuns:**
- Conectar ao servidor OMERO com credenciais
- Usar IDs de sessão existentes
- Alternar entre contextos de grupo
- Gerenciar ciclo de vida da conexão com gerenciadores de contexto

### 2. Acesso e Recuperação de Dados
**Arquivo**: `references/data_access.md`

Navegue pela estrutura hierárquica de dados do OMERO (Projetos → Datasets → Imagens) e dados de triagem (Screens → Plates → Wells). Recupere objetos, consulte por atributos e acesse metadados.

**Cenários comuns:**
- Listar todos os projetos e datasets de um usuário
- Recuperar imagens por ID ou dataset
- Acessar dados de placas de triagem
- Consultar objetos com filtros

### 3. Metadados e Anotações
**Arquivo**: `references/metadata.md`

Crie e gerencie anotações incluindo tags, pares chave-valor, anexos de arquivo e comentários. Vincule anotações a imagens, datasets ou outros objetos.

**Cenários comuns:**
- Adicionar tags a imagens
- Anexar resultados de análise como arquivos
- Criar metadados customizados de pares chave-valor
- Consultar anotações por namespace

### 4. Processamento e Renderização de Imagens
**Arquivo**: `references/image_processing.md`

Acesse dados de pixels brutos como arrays NumPy, manipule configurações de renderização, crie imagens derivadas e gerencie dimensões físicas.

**Cenários comuns:**
- Extrair dados de pixels para análise computacional
- Gerar imagens em miniatura
- Criar projeções de intensidade máxima
- Modificar configurações de renderização de canal

### 5. Regiões de Interesse (ROIs)
**Arquivo**: `references/rois.md`

Crie, recupere e analise ROIs com várias formas (retângulos, elipses, polígonos, máscaras, pontos, linhas). Extraia estatísticas de intensidade de regiões ROI.

**Cenários comuns:**
- Desenhar ROIs retangulares em imagens
- Criar máscaras de polígono para segmentação
- Analisar intensidades de pixels dentro de ROIs
- Exportar coordenadas de ROI

### 6. Tabelas OMERO
**Arquivo**: `references/tables.md`

Armazene e consulte dados tabulares estruturados associados a objetos OMERO. Útil para resultados de análise, medições e metadados.

**Cenários comuns:**
- Armazenar medições quantitativas para imagens
- Criar tabelas com múltiplos tipos de coluna
- Consultar dados de tabela com condições
- Vincular tabelas a imagens ou datasets específicos

### 7. Scripts e Operações em Lote
**Arquivo**: `references/scripts.md`

Crie OMERO.scripts que executem no servidor para processamento em lote, workflows automatizados e integração com clientes OMERO.

**Cenários comuns:**
- Processar múltiplas imagens em lote
- Criar pipelines de análise automatizados
- Gerar estatísticas resumidas em datasets
- Exportar dados em formatos customizados

### 8. Recursos Avançados
**Arquivo**: `references/advanced.md`

Abrange permissões, filesets, consultas entre grupos, operações de exclusão e outras funcionalidades avançadas.

**Cenários comuns:**
- Lidar com permissões de grupo
- Acessar arquivos originais importados
- Realizar consultas entre grupos
- Excluir objetos com callbacks

## Instalação

```bash
uv pip install omero-py
```

**Requisitos:**
- Python 3.7+
- Zeroc Ice 3.6+
- Acesso a um servidor OMERO (host, porta, credenciais)

## Início Rápido

Padrão básico de conexão:

```python
from omero.gateway import BlitzGateway

# Conectar ao servidor OMERO
conn = BlitzGateway(username, password, host=host, port=port)
connected = conn.connect()

if connected:
    # Realizar operações
    for project in conn.listProjects():
        print(project.getName())

    # Sempre fechar a conexão
    conn.close()
else:
    print("Falha na conexão")
```

**Padrão recomendado com gerenciador de contexto:**

```python
from omero.gateway import BlitzGateway

with BlitzGateway(username, password, host=host, port=port) as conn:
    # Conexão gerenciada automaticamente
    for project in conn.listProjects():
        print(project.getName())
    # Fechada automaticamente ao sair
```

## Selecionando a Capacidade Certa

**Para exploração de dados:**
- Comece com `references/connection.md` para estabelecer conexão
- Use `references/data_access.md` para navegar na hierarquia
- Consulte `references/metadata.md` para detalhes de anotações

**Para análise de imagens:**
- Use `references/image_processing.md` para acesso a dados de pixels
- Use `references/rois.md` para análise baseada em região
- Use `references/tables.md` para armazenar resultados

**Para automação:**
- Use `references/scripts.md` para processamento no servidor
- Use `references/data_access.md` para recuperação de dados em lote

**Para operações avançadas:**
- Use `references/advanced.md` para permissões e exclusão
- Consulte `references/connection.md` para consultas entre grupos

## Workflows Comuns

### Workflow 1: Recuperar e Analisar Imagens

1. Conectar ao servidor OMERO (`references/connection.md`)
2. Navegar até dataset (`references/data_access.md`)
3. Recuperar imagens do dataset (`references/data_access.md`)
4. Acessar dados de pixels como array NumPy (`references/image_processing.md`)
5. Realizar análise
6. Armazenar resultados como tabela ou anotação de arquivo (`references/tables.md` ou `references/metadata.md`)

### Workflow 2: Análise de ROI em Lote

1. Conectar ao servidor OMERO
2. Recuperar imagens com ROIs existentes (`references/rois.md`)
3. Para cada imagem, obter formas de ROI
4. Extrair intensidades de pixels dentro de ROIs (`references/rois.md`)
5. Armazenar medições em tabela OMERO (`references/tables.md`)

### Workflow 3: Criar Script de Análise

1. Desenhar workflow de análise
2. Usar framework OMERO.scripts (`references/scripts.md`)
3. Acessar dados por meio de parâmetros de script
4. Processar imagens em lote
5. Gerar saídas (novas imagens, tabelas, arquivos)

## Tratamento de Erros

Sempre envolva operações OMERO em blocos try-except e garanta que as conexões sejam fechadas adequadamente:

```python
from omero.gateway import BlitzGateway
import traceback

try:
    conn = BlitzGateway(username, password, host=host, port=port)
    if not conn.connect():
        raise Exception("Falha na conexão")

    # Realizar operações

except Exception as e:
    print(f"Erro: {e}")
    traceback.print_exc()
finally:
    if conn:
        conn.close()
```

## Recursos Adicionais

- **Documentação Oficial**: https://omero.readthedocs.io/en/stable/developers/Python.html
- **API BlitzGateway**: https://omero.readthedocs.io/en/stable/developers/Python.html#omero-blitzgateway
- **Modelo OMERO**: https://omero.readthedocs.io/en/stable/developers/Model.html
- **Fórum da Comunidade**: https://forum.image.sc/tag/omero

## Observações

- OMERO usa permissões baseadas em grupo (READ-ONLY, READ-ANNOTATE, READ-WRITE)
- Imagens no OMERO são organizadas hierarquicamente: Project > Dataset > Image
- Dados de triagem usam: Screen > Plate > Well > WellSample > Image
- Sempre feche conexões para liberar recursos do servidor
- Use gerenciadores de contexto para gerenciamento automático de recursos
- Dados de pixels são retornados como arrays NumPy para análise