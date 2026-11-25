---
name: latchbio-integration
description: "Plataforma Latch para workflows de bioinformática. Construa pipelines com Latch SDK, decoradores @workflow/@task, deploy de workflows serverless, LatchFile/LatchDir, integração Nextflow/Snakemake."
---

# Integração LatchBio

## Visão Geral

Latch é um framework Python para construir e implantar workflows de bioinformática como pipelines serverless. Construído sobre Flyte, crie workflows com decoradores @workflow/@task, gerencie dados em nuvem com LatchFile/LatchDir, configure recursos e integre pipelines Nextflow/Snakemake.

## Capacidades Principais

A plataforma Latch oferece quatro áreas principais de funcionalidade:

### 1. Criação e Implantação de Workflows
- Defina workflows serverless usando decoradores Python
- Suporte para pipelines nativos em Python, Nextflow e Snakemake
- Containerização automática com Docker
- Interfaces de usuário sem código geradas automaticamente
- Controle de versão e reprodutibilidade

### 2. Gerenciamento de Dados
- Abstrações de armazenamento em nuvem (LatchFile, LatchDir)
- Organização estruturada de dados com Registry (Projetos → Tabelas → Registros)
- Operações de dados type-safe com links e enums
- Transferência automática de arquivos entre local e nuvem
- Correspondência de padrões glob para seleção de arquivos

### 3. Configuração de Recursos
- Decoradores de tarefas pré-configurados (@small_task, @large_task, @small_gpu_task, @large_gpu_task)
- Especificações de recursos personalizadas (CPU, memória, GPU, armazenamento)
- Suporte a GPU (K80, V100, A100)
- Configuração de timeout e armazenamento
- Estratégias de otimização de custos

### 4. Workflows Verificados
- Pipelines pré-construídos prontos para produção
- Bulk RNA-seq, DESeq2, análise de pathways
- AlphaFold e ColabFold para predição de estrutura de proteínas
- Ferramentas de célula única (ArchR, scVelo, emptyDropsR)
- Análise CRISPR, filogenética e muito mais

## Início Rápido

### Instalação e Configuração

```bash
# Instale o Latch SDK
python3 -m uv pip install latch

# Faça login no Latch
latch login

# Inicialize um novo workflow
latch init my-workflow

# Registre o workflow na plataforma
latch register my-workflow
```

**Pré-requisitos:**
- Docker instalado e rodando
- Credenciais de conta Latch
- Python 3.8+

### Exemplo de Workflow Básico

```python
from latch import workflow, small_task
from latch.types import LatchFile

@small_task
def process_file(input_file: LatchFile) -> LatchFile:
    """Process a single file"""
    # Processing logic
    return output_file

@workflow
def my_workflow(input_file: LatchFile) -> LatchFile:
    """
    My bioinformatics workflow

    Args:
        input_file: Input data file
    """
    return process_file(input_file=input_file)
```

## Quando Usar Esta Skill

Esta skill deve ser usada quando encontrar qualquer um dos seguintes cenários:

**Desenvolvimento de Workflows:**
- "Criar um workflow Latch para análise RNA-seq"
- "Implantar meu pipeline no Latch"
- "Converter meu pipeline Nextflow para Latch"
- "Adicionar suporte a GPU ao meu workflow"
- Trabalhar com decoradores `@workflow`, `@task`

**Gerenciamento de Dados:**
- "Organizar meus dados de sequenciamento no Latch Registry"
- "Como usar LatchFile e LatchDir?"
- "Configurar rastreamento de amostras no Latch"
- Trabalhar com caminhos `latch:///`

**Configuração de Recursos:**
- "Configurar GPU para AlphaFold no Latch"
- "Minha tarefa está ficando sem memória"
- "Como otimizar custos de workflow?"
- Trabalhar com decoradores de tarefas

**Workflows Verificados:**
- "Executar AlphaFold no Latch"
- "Usar DESeq2 para expressão diferencial"
- "Workflows pré-construídos disponíveis"
- Usar módulo `latch.verified`

## Documentação Detalhada

Esta skill inclui documentação de referência abrangente organizada por capacidade:

### references/workflow-creation.md
**Leia isto para:**
- Criar e registrar workflows
- Definição de tarefas e decoradores
- Suporte para Python, Nextflow, Snakemake
- Launch plans e seções condicionais
- Execução de workflows (CLI e programática)
- Pipelines multi-etapas e paralelos
- Resolução de problemas de registro

**Tópicos-chave:**
- Comandos `latch init` e `latch register`
- Decoradores `@workflow` e `@task`
- Noções básicas de LatchFile e LatchDir
- Anotações de tipo e docstrings
- Launch plans com parâmetros predefinidos
- Seções de UI condicionais

### references/data-management.md
**Leia isto para:**
- Armazenamento em nuvem com LatchFile e LatchDir
- Sistema Registry (Projetos, Tabelas, Registros)
- Registros vinculados e relacionamentos
- Colunas com enum e tipo
- Operações em massa e transações
- Integração com workflows
- Gerenciamento de conta e workspace

**Tópicos-chave:**
- Formato de caminho `latch:///`
- Transferência de arquivos e padrões glob
- Criação e consulta de tabelas Registry
- Tipos de coluna (string, number, file, link, enum)
- Operações CRUD de registros
- Integração Workflow-Registry

### references/resource-configuration.md
**Leia isto para:**
- Decoradores de recursos de tarefas
- Configuração customizada de CPU, memória, GPU
- Tipos de GPU (K80, V100, A100)
- Configurações de timeout e armazenamento
- Estratégias de otimização de recursos
- Design de workflow econômico
- Monitoramento e depuração

**Tópicos-chave:**
- `@small_task`, `@large_task`, `@small_gpu_task`, `@large_gpu_task`
- `@custom_task` com especificações precisas
- Configuração multi-GPU
- Seleção de recursos por tipo de carga de trabalho
- Limites e quotas da plataforma

### references/verified-workflows.md
**Leia isto para:**
- Workflows de produção pré-construídos
- Bulk RNA-seq e DESeq2
- AlphaFold e ColabFold
- Análise de célula única (ArchR, scVelo)
- Análise de edição CRISPR
- Enriquecimento de pathways
- Integração com workflows customizados

**Tópicos-chave:**
- Importações de módulo `latch.verified`
- Workflows verificados disponíveis
- Parâmetros e opções de workflow
- Combinação de etapas verificadas e customizadas
- Gerenciamento de versão

## Padrões Comuns de Workflow

### Pipeline RNA-seq Completo

```python
from latch import workflow, small_task, large_task
from latch.types import LatchFile, LatchDir

@small_task
def quality_control(fastq: LatchFile) -> LatchFile:
    """Run FastQC"""
    return qc_output

@large_task
def alignment(fastq: LatchFile, genome: str) -> LatchFile:
    """STAR alignment"""
    return bam_output

@small_task
def quantification(bam: LatchFile) -> LatchFile:
    """featureCounts"""
    return counts

@workflow
def rnaseq_pipeline(
    input_fastq: LatchFile,
    genome: str,
    output_dir: LatchDir
) -> LatchFile:
    """RNA-seq analysis pipeline"""
    qc = quality_control(fastq=input_fastq)
    aligned = alignment(fastq=qc, genome=genome)
    return quantification(bam=aligned)
```

### Workflow Acelerado com GPU

```python
from latch import workflow, small_task, large_gpu_task
from latch.types import LatchFile

@small_task
def preprocess(input_file: LatchFile) -> LatchFile:
    """Prepare data"""
    return processed

@large_gpu_task
def gpu_computation(data: LatchFile) -> LatchFile:
    """GPU-accelerated analysis"""
    return results

@workflow
def gpu_pipeline(input_file: LatchFile) -> LatchFile:
    """Pipeline with GPU tasks"""
    preprocessed = preprocess(input_file=input_file)
    return gpu_computation(data=preprocessed)
```

### Workflow Integrado com Registry

```python
from latch import workflow, small_task
from latch.registry.table import Table
from latch.registry.record import Record
from latch.types import LatchFile

@small_task
def process_and_track(sample_id: str, table_id: str) -> str:
    """Process sample and update Registry"""
    # Get sample from registry
    table = Table.get(table_id=table_id)
    records = Record.list(table_id=table_id, filter={"sample_id": sample_id})
    sample = records[0]

    # Process
    input_file = sample.values["fastq_file"]
    output = process(input_file)

    # Update registry
    sample.update(values={"status": "completed", "result": output})
    return "Success"

@workflow
def registry_workflow(sample_id: str, table_id: str):
    """Workflow integrated with Registry"""
    return process_and_track(sample_id=sample_id, table_id=table_id)
```

## Melhores Práticas

### Design de Workflow
1. Use anotações de tipo para todos os parâmetros
2. Escreva docstrings claros (aparecem na UI)
3. Comece com decoradores de tarefas padrão, escale conforme necessário
4. Divida workflows complexos em tarefas modulares
5. Implemente tratamento adequado de erros

### Gerenciamento de Dados
6. Use estruturas de pastas consistentes
7. Defina esquemas Registry antes de entrada em massa
8. Use registros vinculados para relacionamentos
9. Armazene metadados em Registry para rastreabilidade

### Configuração de Recursos
10. Dimensione recursos adequadamente (não superaloque)
11. Use GPU apenas quando algoritmos a suportarem
12. Monitore métricas de execução e otimize
13. Design para execução paralela quando possível

### Fluxo de Trabalho de Desenvolvimento
14. Teste localmente com Docker antes do registro
15. Use controle de versão para código de workflow
16. Documente requisitos de recursos
17. Profile workflows para determinar necessidades reais

## Resolução de Problemas

### Problemas Comuns

**Falhas de Registro:**
- Certifique-se de que Docker está rodando
- Verifique autenticação com `latch login`
- Verifique todas as dependências no Dockerfile
- Use flag `--verbose` para logs detalhados

**Problemas de Recursos:**
- Falta de memória: Aumente memória no decorador de tarefas
- Timeouts: Aumente parâmetro de timeout
- Problemas de armazenamento: Aumente storage_gib efêmero

**Acesso a Dados:**
- Use formato correto de caminho `latch:///`
- Verifique se arquivo existe no workspace
- Verifique permissões para workspaces compartilhados

**Erros de Tipo:**
- Adicione anotações de tipo a todos os parâmetros
- Use LatchFile/LatchDir para parâmetros de arquivo/diretório
- Garanta que tipo de retorno do workflow corresponda ao retorno real

## Recursos Adicionais

- **Documentação Oficial**: https://docs.latch.bio
- **Repositório GitHub**: https://github.com/latchbio/latch
- **Comunidade Slack**: Junte-se ao workspace Latch SDK
- **Referência de API**: https://docs.latch.bio/api/latch.html
- **Blog**: https://blog.latch.bio

## Suporte

Para problemas ou dúvidas:
1. Verifique links de documentação acima
2. Pesquise issues no GitHub
3. Faça perguntas na comunidade Slack
4. Entre em contato com support@latch.bio