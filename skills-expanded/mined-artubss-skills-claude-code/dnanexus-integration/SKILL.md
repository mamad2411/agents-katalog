---
name: dnanexus-integration
description: "Plataforma de genômica em nuvem DNAnexus. Crie apps/applets, gerencie dados (upload/download), Python SDK dxpy, execute workflows, FASTQ/BAM/VCF, para desenvolvimento e execução de pipelines genômicos."
---

# Integração DNAnexus

## Visão Geral

DNAnexus é uma plataforma em nuvem para análise de dados biomédicos e genômica. Crie e implante apps/applets, gerencie objetos de dados, execute workflows e use o Python SDK dxpy para desenvolvimento e execução de pipelines genômicos.

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada quando:
- Criar, construir ou modificar apps/applets no DNAnexus
- Fazer upload, download, pesquisar ou organizar arquivos e registros
- Executar análises, monitorar jobs, criar workflows
- Escrever scripts usando dxpy para interagir com a plataforma
- Configurar dxapp.json, gerenciar dependências, usar Docker
- Processar arquivos FASTQ, BAM, VCF ou outros formatos de bioinformática
- Gerenciar projetos, permissões ou recursos da plataforma

## Capacidades Principais

A habilidade está organizada em cinco áreas principais, cada uma com documentação de referência detalhada:

### 1. Desenvolvimento de Apps

**Propósito**: Criar programas executáveis (apps/applets) que executam na plataforma DNAnexus.

**Operações Principais**:
- Gerar esqueleto de app com `dx-app-wizard`
- Escrever apps em Python ou Bash com pontos de entrada apropriados
- Tratar objetos de dados de entrada/saída
- Fazer deploy com `dx build` ou `dx build --app`
- Testar apps na plataforma

**Casos de Uso Comuns**:
- Pipelines de bioinformática (alinhamento, chamada de variantes)
- Workflows de processamento de dados
- Controle de qualidade e filtragem
- Ferramentas de conversão de formato

**Referência**: Consulte `references/app-development.md` para:
- Estrutura e padrões completos de app
- Decoradores de ponto de entrada Python
- Tratamento de entrada/saída com dxpy
- Melhores práticas de desenvolvimento
- Problemas comuns e soluções

### 2. Operações de Dados

**Propósito**: Gerenciar arquivos, registros e outros objetos de dados na plataforma.

**Operações Principais**:
- Upload/download de arquivos com `dxpy.upload_local_file()` e `dxpy.download_dxfile()`
- Criar e gerenciar registros com metadados
- Pesquisar objetos de dados por nome, propriedades ou tipo
- Clonar dados entre projetos
- Gerenciar pastas de projeto e permissões

**Casos de Uso Comuns**:
- Upload de dados de sequenciamento (arquivos FASTQ)
- Organizar resultados de análises
- Pesquisar amostras ou experimentos específicos
- Fazer backup de dados em projetos
- Gerenciar genomas de referência e anotações

**Referência**: Consulte `references/data-operations.md` para:
- Operações completas de arquivo e registro
- Ciclo de vida de objetos de dados (estados aberto/fechado)
- Padrões de pesquisa e descoberta
- Gerenciamento de projetos
- Operações em lote

### 3. Execução de Jobs

**Propósito**: Executar análises, monitorar execução e orquestrar workflows.

**Operações Principais**:
- Lançar jobs com `applet.run()` ou `app.run()`
- Monitorar status e logs de jobs
- Criar subjobs para processamento paralelo
- Construir e executar workflows com múltiplas etapas
- Encadear jobs com referências de saída

**Casos de Uso Comuns**:
- Executar análises genômicas em dados de sequenciamento
- Processamento paralelo de múltiplas amostras
- Pipelines de análise com múltiplas etapas
- Monitorar computações de longa duração
- Depuração de jobs com falha

**Referência**: Consulte `references/job-execution.md` para:
- Ciclo de vida completo de jobs e estados
- Criação e orquestração de workflows
- Padrões de execução paralela
- Monitoramento e depuração de jobs
- Gerenciamento de recursos

### 4. Python SDK (dxpy)

**Propósito**: Acesso programático à plataforma DNAnexus através de Python.

**Operações Principais**:
- Trabalhar com manipuladores de objetos de dados (DXFile, DXRecord, DXApplet, etc.)
- Usar funções de alto nível para tarefas comuns
- Fazer chamadas diretas de API para operações avançadas
- Criar links e referências entre objetos
- Pesquisar e descobrir recursos da plataforma

**Casos de Uso Comuns**:
- Scripts de automação para gerenciamento de dados
- Pipelines de análise customizados
- Workflows de processamento em lote
- Integração com ferramentas externas
- Migração e organização de dados

**Referência**: Consulte `references/python-sdk.md` para:
- Referência completa de classes dxpy
- Funções utilitárias de alto nível
- Documentação de métodos de API
- Padrões de tratamento de erros
- Padrões de código comuns

### 5. Configuração e Dependências

**Propósito**: Configurar metadados de app e gerenciar dependências.

**Operações Principais**:
- Escrever dxapp.json com entradas, saídas e especificações de execução
- Instalar pacotes do sistema (execDepends)
- Agrupar ferramentas e recursos customizados
- Usar assets para dependências compartilhadas
- Integrar contêineres Docker
- Configurar tipos de instância e timeouts

**Casos de Uso Comuns**:
- Definir especificações de entrada/saída de app
- Instalar ferramentas de bioinformática (samtools, bwa, etc.)
- Gerenciar dependências de pacotes Python
- Usar imagens Docker para ambientes complexos
- Selecionar recursos computacionais

**Referência**: Consulte `references/configuration.md` para:
- Especificação completa de dxapp.json
- Estratégias de gerenciamento de dependências
- Padrões de integração Docker
- Configuração regional e de recursos
- Configurações de exemplo

## Exemplos de Início Rápido

### Upload e Análise de Dados

```python
import dxpy

# Fazer upload do arquivo de entrada
input_file = dxpy.upload_local_file("sample.fastq", project="project-xxxx")

# Executar análise
job = dxpy.DXApplet("applet-xxxx").run({
    "reads": dxpy.dxlink(input_file.get_id())
})

# Aguardar conclusão
job.wait_on_done()

# Fazer download dos resultados
output_id = job.describe()["output"]["aligned_reads"]["$dnanexus_link"]
dxpy.download_dxfile(output_id, "aligned.bam")
```

### Pesquisar e Fazer Download de Arquivos

```python
import dxpy

# Encontrar arquivos BAM de um experimento específico
files = dxpy.find_data_objects(
    classname="file",
    name="*.bam",
    properties={"experiment": "exp001"},
    project="project-xxxx"
)

# Fazer download de cada arquivo
for file_result in files:
    file_obj = dxpy.DXFile(file_result["id"])
    filename = file_obj.describe()["name"]
    dxpy.download_dxfile(file_result["id"], filename)
```

### Criar App Simples

```python
# src/my-app.py
import dxpy
import subprocess

@dxpy.entry_point('main')
def main(input_file, quality_threshold=30):
    # Fazer download da entrada
    dxpy.download_dxfile(input_file["$dnanexus_link"], "input.fastq")

    # Processar
    subprocess.check_call([
        "quality_filter",
        "--input", "input.fastq",
        "--output", "filtered.fastq",
        "--threshold", str(quality_threshold)
    ])

    # Fazer upload da saída
    output_file = dxpy.upload_local_file("filtered.fastq")

    return {
        "filtered_reads": dxpy.dxlink(output_file)
    }

dxpy.run()
```

## Árvore de Decisão de Workflow

Ao trabalhar com DNAnexus, siga esta árvore de decisão:

1. **Precisa criar um novo executável?**
   - Sim → Use **Desenvolvimento de Apps** (references/app-development.md)
   - Não → Continue para o passo 2

2. **Precisa gerenciar arquivos ou dados?**
   - Sim → Use **Operações de Dados** (references/data-operations.md)
   - Não → Continue para o passo 3

3. **Precisa executar uma análise ou workflow?**
   - Sim → Use **Execução de Jobs** (references/job-execution.md)
   - Não → Continue para o passo 4

4. **Escrevendo scripts Python para automação?**
   - Sim → Use **Python SDK** (references/python-sdk.md)
   - Não → Continue para o passo 5

5. **Configurando settings de app ou dependências?**
   - Sim → Use **Configuração** (references/configuration.md)

Frequentemente você precisará de múltiplas capacidades juntas (por exemplo, desenvolvimento de app + configuração, ou operações de dados + execução de jobs).

## Instalação e Autenticação

### Instalar dxpy

```bash
uv pip install dxpy
```

### Fazer Login no DNAnexus

```bash
dx login
```

Isso autentica sua sessão e configura acesso a projetos e dados.

### Verificar Instalação

```bash
dx --version
dx whoami
```

## Padrões Comuns

### Padrão 1: Processamento em Lote

Processar múltiplos arquivos com a mesma análise:

```python
# Encontrar todos os arquivos FASTQ
files = dxpy.find_data_objects(
    classname="file",
    name="*.fastq",
    project="project-xxxx"
)

# Lançar jobs em paralelo
jobs = []
for file_result in files:
    job = dxpy.DXApplet("applet-xxxx").run({
        "input": dxpy.dxlink(file_result["id"])
    })
    jobs.append(job)

# Aguardar todas as conclusões
for job in jobs:
    job.wait_on_done()
```

### Padrão 2: Pipeline com Múltiplas Etapas

Encadear múltiplas análises:

```python
# Etapa 1: Controle de qualidade
qc_job = qc_applet.run({"reads": input_file})

# Etapa 2: Alinhamento (usa saída de QC)
align_job = align_applet.run({
    "reads": qc_job.get_output_ref("filtered_reads")
})

# Etapa 3: Chamada de variantes (usa saída de alinhamento)
variant_job = variant_applet.run({
    "bam": align_job.get_output_ref("aligned_bam")
})
```

### Padrão 3: Organização de Dados

Organizar resultados de análises sistematicamente:

```python
# Criar estrutura de pasta organizada
dxpy.api.project_new_folder(
    "project-xxxx",
    {"folder": "/experiments/exp001/results", "parents": True}
)

# Fazer upload com metadados
result_file = dxpy.upload_local_file(
    "results.txt",
    project="project-xxxx",
    folder="/experiments/exp001/results",
    properties={
        "experiment": "exp001",
        "sample": "sample1",
        "analysis_date": "2025-10-20"
    },
    tags=["validated", "published"]
)
```

## Melhores Práticas

1. **Tratamento de Erros**: Sempre envolver chamadas de API em blocos try-except
2. **Gerenciamento de Recursos**: Escolher tipos de instância apropriados para as cargas de trabalho
3. **Organização de Dados**: Usar estruturas de pasta consistentes e metadados
4. **Otimização de Custos**: Arquivar dados antigos, usar classes de armazenamento apropriadas
5. **Documentação**: Incluir descrições claras em dxapp.json
6. **Testes**: Testar apps com vários tipos de entrada antes do uso em produção
7. **Controle de Versão**: Usar versionamento semântico para apps
8. **Segurança**: Nunca codificar credenciais no código-fonte
9. **Logging**: Incluir mensagens de log informativas para depuração
10. **Limpeza**: Remover arquivos temporários e jobs com falha

## Recursos

Esta habilidade inclui documentação de referência detalhada:

### references/

- **app-development.md** - Guia completo para construir e fazer deploy de apps/applets
- **data-operations.md** - Gerenciamento de arquivos, registros, pesquisa e operações de projeto
- **job-execution.md** - Executar jobs, workflows, monitoramento e processamento paralelo
- **python-sdk.md** - Referência abrangente da biblioteca dxpy com todas as classes e funções
- **configuration.md** - Especificação de dxapp.json e gerenciamento de dependências

Carregue essas referências quando você precisar de informações detalhadas sobre operações específicas ou ao trabalhar em tarefas complexas.

## Obtendo Ajuda

- Documentação oficial: https://documentation.dnanexus.com/
- Referência de API: http://autodoc.dnanexus.com/
- Repositório GitHub: https://github.com/dnanexus/dx-toolkit
- Suporte: support@dnanexus.com