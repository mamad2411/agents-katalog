---
name: deeptools
description: "Kit de ferramentas para análise NGS. Conversão de BAM para bigWig, QC (correlação, PCA, fingerprints), heatmaps/profiles (TSS, peaks), para visualização de ChIP-seq, RNA-seq, ATAC-seq."
---

# deepTools: Kit de Ferramentas para Análise de Dados NGS

## Visão Geral

deepTools é uma suíte abrangente de ferramentas Python de linha de comando projetada para processar e analisar dados de sequenciamento de alto rendimento. Use deepTools para realizar controle de qualidade, normalizar dados, comparar amostras e gerar visualizações de qualidade de publicação para experimentos ChIP-seq, RNA-seq, ATAC-seq, MNase-seq e outros NGS.

**Capacidades principais:**
- Converter alinhamentos BAM para faixas de cobertura normalizadas (bigWig/bedGraph)
- Avaliação de controle de qualidade (fingerprint, correlação, cobertura)
- Análise de comparação e correlação de amostras
- Geração de heatmaps e gráficos de profile ao redor de features genômicas
- Análise de enriquecimento e visualização de regiões de peaks

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada quando:

- **Conversão de arquivos**: "Converter BAM para bigWig", "gerar faixas de cobertura", "normalizar dados ChIP-seq"
- **Controle de qualidade**: "verificar qualidade ChIP", "comparar replicatas", "avaliar profundidade de sequenciamento", "análise QC"
- **Visualização**: "criar heatmap ao redor de TSS", "plotar sinal ChIP", "visualizar enriquecimento", "gerar gráfico de profile"
- **Comparação de amostras**: "comparar tratamento vs controle", "correlacionar amostras", "análise PCA"
- **Workflows de análise**: "analisar dados ChIP-seq", "cobertura RNA-seq", "análise ATAC-seq", "workflow completo"
- **Trabalho com tipos de arquivos específicos**: arquivos BAM, arquivos bigWig, arquivos de região BED em contexto genômico

## Início Rápido

Para usuários novos em deepTools, comece com validação de arquivos e workflows comuns:

### 1. Validar Arquivos de Entrada

Antes de executar qualquer análise, valide arquivos BAM, bigWig e BED usando o script de validação:

```bash
python scripts/validate_files.py --bam sample1.bam sample2.bam --bed regions.bed
```

Isso verifica existência de arquivos, índices BAM e correção de formato.

### 2. Gerar Modelo de Workflow

Para análises padrão, use o gerador de workflow para criar scripts personalizados:

```bash
# Listar workflows disponíveis
python scripts/workflow_generator.py --list

# Gerar workflow QC ChIP-seq
python scripts/workflow_generator.py chipseq_qc -o qc_workflow.sh \
    --input-bam Input.bam --chip-bams "ChIP1.bam ChIP2.bam" \
    --genome-size 2913022398

# Tornar executável e executar
chmod +x qc_workflow.sh
./qc_workflow.sh
```

### 3. Operações Mais Comuns

Veja `assets/quick_reference.md` para comandos e parâmetros frequentemente usados.

## Instalação

```bash
uv pip install deeptools
```

## Workflows Principais

Os workflows do deepTools geralmente seguem este padrão: **QC → Normalização → Comparação/Visualização**

### Workflow de Controle de Qualidade ChIP-seq

Quando usuários solicitam QC ChIP-seq ou avaliação de qualidade:

1. **Gerar script de workflow** usando `scripts/workflow_generator.py chipseq_qc`
2. **Passos-chave de QC**:
   - Correlação de amostra (multiBamSummary + plotCorrelation)
   - Análise PCA (plotPCA)
   - Avaliação de cobertura (plotCoverage)
   - Validação de tamanho de fragmento (bamPEFragmentSize)
   - Força de enriquecimento ChIP (plotFingerprint)

**Interpretando resultados:**
- **Correlação**: Replicatas devem se agrupar juntas com alta correlação (>0,9)
- **Fingerprint**: ChIP forte mostra subida acentuada; diagonal plana indica enriquecimento fraco
- **Cobertura**: Avaliar se a profundidade de sequenciamento é adequada para análise

Detalhes completos do workflow em `references/workflows.md` → "Workflow de Controle de Qualidade ChIP-seq"

### Workflow de Análise Completa ChIP-seq

Para análise ChIP-seq completa de BAM para visualizações:

1. **Gerar faixas de cobertura** com normalização (bamCoverage)
2. **Criar faixas de comparação** (bamCompare para razão log2)
3. **Computar matrizes de sinal** ao redor de features (computeMatrix)
4. **Gerar visualizações** (plotHeatmap, plotProfile)
5. **Análise de enriquecimento** em peaks (plotEnrichment)

Use `scripts/workflow_generator.py chipseq_analysis` para gerar modelo.

Sequências de comando completas em `references/workflows.md` → "Workflow de Análise ChIP-seq"

### Workflow de Cobertura RNA-seq

Para faixas de cobertura RNA-seq específicas de fita:

Use bamCoverage com `--filterRNAstrand` para separar fitas forward e reverse.

**Importante:** NUNCA use `--extendReads` para RNA-seq (estenderia sobre junções de splice).

Use normalização: CPM para bins fixos, RPKM para análise em nível de gene.

Modelo disponível: `scripts/workflow_generator.py rnaseq_coverage`

Detalhes em `references/workflows.md` → "Workflow de Cobertura RNA-seq"

### Workflow de Análise ATAC-seq

ATAC-seq requer correção de offset Tn5:

1. **Deslocar leituras** usando alignmentSieve com `--ATACshift`
2. **Gerar cobertura** com bamCoverage
3. **Analisar tamanhos de fragmento** (esperar padrão de ladder de nucleossoma)
4. **Visualizar em peaks** se disponível

Modelo: `scripts/workflow_generator.py atacseq`

Workflow completo em `references/workflows.md` → "Workflow ATAC-seq"

## Categorias de Ferramentas e Tarefas Comuns

### Processamento de BAM/bigWig

**Converter BAM para cobertura normalizada:**
```bash
bamCoverage --bam input.bam --outFileName output.bw \
    --normalizeUsing RPGC --effectiveGenomeSize 2913022398 \
    --binSize 10 --numberOfProcessors 8
```

**Comparar duas amostras (razão log2):**
```bash
bamCompare -b1 treatment.bam -b2 control.bam -o ratio.bw \
    --operation log2 --scaleFactorsMethod readCount
```

**Ferramentas-chave:** bamCoverage, bamCompare, multiBamSummary, multiBigwigSummary, correctGCBias, alignmentSieve

Referência completa: `references/tools_reference.md` → "Ferramentas de Processamento de Arquivos BAM e bigWig"

### Controle de Qualidade

**Verificar enriquecimento ChIP:**
```bash
plotFingerprint -b input.bam chip.bam -o fingerprint.png \
    --extendReads 200 --ignoreDuplicates
```

**Correlação de amostra:**
```bash
multiBamSummary bins --bamfiles *.bam -o counts.npz
plotCorrelation -in counts.npz --corMethod pearson \
    --whatToShow heatmap -o correlation.png
```

**Ferramentas-chave:** plotFingerprint, plotCoverage, plotCorrelation, plotPCA, bamPEFragmentSize

Referência completa: `references/tools_reference.md` → "Ferramentas de Controle de Qualidade"

### Visualização

**Criar heatmap ao redor de TSS:**
```bash
# Computar matriz
computeMatrix reference-point -S signal.bw -R genes.bed \
    -b 3000 -a 3000 --referencePoint TSS -o matrix.gz

# Gerar heatmap
plotHeatmap -m matrix.gz -o heatmap.png \
    --colorMap RdBu --kmeans 3
```

**Criar gráfico de profile:**
```bash
plotProfile -m matrix.gz -o profile.png \
    --plotType lines --colors blue red
```

**Ferramentas-chave:** computeMatrix, plotHeatmap, plotProfile, plotEnrichment

Referência completa: `references/tools_reference.md` → "Ferramentas de Visualização"

## Métodos de Normalização

Escolher a normalização correta é crítico para comparações válidas. Consulte `references/normalization_methods.md` para orientação abrangente.

**Guia de seleção rápida:**

- **Cobertura ChIP-seq**: Use RPGC ou CPM
- **Comparação ChIP-seq**: Use bamCompare com log2 e readCount
- **Bins RNA-seq**: Use CPM
- **Genes RNA-seq**: Use RPKM (leva em conta comprimento do gene)
- **ATAC-seq**: Use RPGC ou CPM

**Métodos de normalização:**
- **RPGC**: Cobertura de genoma 1× (requer --effectiveGenomeSize)
- **CPM**: Contagens por milhão de leituras mapeadas
- **RPKM**: Leituras por kb por milhão (leva em conta comprimento da região)
- **BPM**: Bins por milhão
- **None**: Contagens brutas (não recomendado para comparações)

Explicação completa: `references/normalization_methods.md`

## Tamanhos de Genoma Efetivos

Normalização RPGC requer tamanho de genoma efetivo. Valores comuns:

| Organismo | Assembly | Tamanho | Uso |
|----------|----------|--------|-----|
| Humano | GRCh38/hg38 | 2.913.022.398 | `--effectiveGenomeSize 2913022398` |
| Camundongo | GRCm38/mm10 | 2.652.783.500 | `--effectiveGenomeSize 2652783500` |
| Peixe-zebra | GRCz11 | 1.368.780.147 | `--effectiveGenomeSize 1368780147` |
| *Drosophila* | dm6 | 142.573.017 | `--effectiveGenomeSize 142573017` |
| *C. elegans* | ce10/ce11 | 100.286.401 | `--effectiveGenomeSize 100286401` |

Tabela completa com valores específicos por comprimento de leitura: `references/effective_genome_sizes.md`

## Parâmetros Comuns Entre Ferramentas

Muitos comandos deepTools compartilham essas opções:

**Desempenho:**
- `--numberOfProcessors, -p`: Ativar processamento paralelo (sempre use núcleos disponíveis)
- `--region`: Processar regiões específicas para teste (ex., `chr1:1-1000000`)

**Filtragem de Leitura:**
- `--ignoreDuplicates`: Remover duplicatas PCR (recomendado para a maioria das análises)
- `--minMappingQuality`: Filtrar por qualidade de alinhamento (ex., `--minMappingQuality 10`)
- `--minFragmentLength` / `--maxFragmentLength`: Limites de comprimento de fragmento
- `--samFlagInclude` / `--samFlagExclude`: Filtragem de flag SAM

**Processamento de Leitura:**
- `--extendReads`: Estender para comprimento de fragmento (ChIP-seq: SIM, RNA-seq: NÃO)
- `--centerReads`: Centralizar no ponto médio do fragmento para sinais mais nítidos

## Melhores Práticas

### Validação de Arquivos
**Sempre valide arquivos primeiro** usando `scripts/validate_files.py` para verificar:
- Existência e legibilidade de arquivos
- Índices BAM presentes (arquivos .bai)
- Correção de formato BED
- Tamanhos de arquivo razoáveis

### Estratégia de Análise

1. **Comece com QC**: Execute análise de correlação, cobertura e fingerprint antes de prosseguir
2. **Teste em pequenas regiões**: Use `--region chr1:1-10000000` para teste de parâmetros
3. **Documente comandos**: Salve linhas de comando completas para reprodutibilidade
4. **Use normalização consistente**: Aplique o mesmo método em amostras em comparações
5. **Verifique assembly de genoma**: Certifique-se de que arquivos BAM e BED usam builds de genoma correspondentes

### Específico para ChIP-seq

- **Sempre estenda leituras** para ChIP-seq: `--extendReads 200`
- **Remova duplicatas**: Use `--ignoreDuplicates` na maioria dos casos
- **Verifique enriquecimento primeiro**: Execute plotFingerprint antes da análise detalhada
- **Correção GC**: Aplique apenas se viés significativo detectado; nunca use `--ignoreDuplicates` após correção GC

### Específico para RNA-seq

- **Nunca estenda leituras** para RNA-seq (estenderia sobre junções de splice)
- **Específico de fita**: Use `--filterRNAstrand forward/reverse` para bibliotecas com fita
- **Normalização**: CPM para bins, RPKM para genes

### Específico para ATAC-seq

- **Aplique correção Tn5**: Use alignmentSieve com `--ATACshift`
- **Filtragem de fragmento**: Defina comprimentos mín/máx de fragmento apropriados
- **Verifique padrão de nucleossoma**: Gráfico de tamanho de fragmento deve mostrar padrão de ladder

### Otimização de Desempenho

1. **Use múltiplos processadores**: `--numberOfProcessors 8` (ou núcleos disponíveis)
2. **Aumente tamanho de bin** para processamento mais rápido e arquivos menores
3. **Processe cromossomos separadamente** para sistemas com memória limitada
4. **Pré-filtre arquivos BAM** usando alignmentSieve para criar arquivos filtrados reutilizáveis
5. **Use bigWig em vez de bedGraph**: Comprimido e mais rápido para processar

## Solução de Problemas

### Problemas Comuns

**Índice BAM ausente:**
```bash
samtools index input.bam
```

**Memória insuficiente:**
Processe cromossomos individualmente usando `--region`:
```bash
bamCoverage --bam input.bam -o chr1.bw --region chr1
```

**Processamento lento:**
Aumente `--numberOfProcessors` e/ou aumente `--binSize`

**Arquivos bigWig muito grandes:**
Aumente tamanho de bin: `--binSize 50` ou maior

### Erros de Validação

Execute script de validação para identificar problemas:
```bash
python scripts/validate_files.py --bam *.bam --bed regions.bed
```

Erros comuns e soluções explicados na saída do script.

## Documentação de Referência

Esta habilidade inclui documentação de referência abrangente:

### references/tools_reference.md
Documentação completa de todos os comandos deepTools organizada por categoria:
- Ferramentas de processamento BAM e bigWig (9 ferramentas)
- Ferramentas de controle de qualidade (6 ferramentas)
- Ferramentas de visualização (3 ferramentas)
- Ferramentas diversas (2 ferramentas)

Cada ferramenta inclui:
- Propósito e visão geral
- Parâmetros-chave com explicações
- Exemplos de uso
- Notas importantes e melhores práticas

**Use esta referência quando:** Usuários perguntam sobre ferramentas específicas, parâmetros ou uso detalhado.

### references/workflows.md
Exemplos de workflows completos para análises comuns:
- Workflow de controle de qualidade ChIP-seq
- Workflow de análise completa ChIP-seq
- Workflow de cobertura RNA-seq
- Workflow de análise ATAC-seq
- Workflow de comparação multi-amostra
- Workflow de análise de região de peak
- Dicas de solução de problemas e desempenho

**Use esta referência quando:** Usuários precisam de pipelines de análise completos ou exemplos de workflows.

### references/normalization_methods.md
Guia abrangente para métodos de normalização:
- Explicação detalhada de cada método (RPGC, CPM, RPKM, BPM, etc.)
- Quando usar cada método
- Fórmulas e interpretação
- Guia de seleção por tipo de experimento
- Armadilhas comuns e soluções
- Tabela de referência rápida

**Use esta referência quando:** Usuários perguntam sobre normalização, comparação de amostras ou qual método usar.

### references/effective_genome_sizes.md
Valores de tamanho de genoma efetivo e uso:
- Valores comuns de organismos (humano, camundongo, mosca, verme, peixe-zebra)
- Valores específicos por comprimento de leitura
- Métodos de cálculo
- Quando e como usar em comandos
- Instruções de cálculo de genoma personalizado

**Use esta referência quando:** Usuários precisam de tamanho de genoma para normalização RPGC ou correção de viés GC.

## Scripts de Auxílio

### scripts/validate_files.py

Valida arquivos BAM, bigWig e BED para análise deepTools. Verifica existência de arquivos, índices e formato.

**Uso:**
```bash
python scripts/validate_files.py --bam sample1.bam sample2.bam \
    --bed peaks.bed --bigwig signal.bw
```

**Quando usar:** Antes de iniciar qualquer análise, ou ao solucionar problemas de erros.

### scripts/workflow_generator.py

Gera modelos de script bash personalizáveis para workflows deepTools comuns.

**Workflows disponíveis:**
- `chipseq_qc`: Controle de qualidade ChIP-seq
- `chipseq_analysis`: Análise ChIP-seq completa
- `rnaseq_coverage`: Cobertura RNA-seq com fita específica
- `atacseq`: ATAC-seq com correção Tn5

**Uso:**
```bash
# Listar workflows
python scripts/workflow_generator.py --list

# Gerar workflow
python scripts/workflow_generator.py chipseq_qc -o qc.sh \
    --input-bam Input.bam --chip-bams "ChIP1.bam ChIP2.bam" \
    --genome-size 2913022398 --threads 8

# Executar workflow gerado
chmod +x qc.sh
./qc.sh
```

**Quando usar:** Usuários solicitam workflows padrão ou precisam de scripts de modelo para personalizar.

## Assets

### assets/quick_reference.md

Cartão de referência rápida com os comandos mais comuns, tamanhos de genoma efetivos e padrão de workflow típico.

**Quando usar:** Usuários precisam de exemplos de comando rápidos sem documentação detalhada.

## Lidando com Solicitações de Usuários

### Para Usuários Novos

1. Comece com verificação de instalação
2. Valide arquivos de entrada usando `scripts/validate_files.py`
3. Recomende workflow apropriado com base no tipo de experimento
4. Gere modelo de workflow usando `scripts/workflow_generator.py`
5. Guie pela customização e execução

### Para Usuários Experientes

1. Forneça comandos de ferramentas específicas para operações solicitadas
2. Referencie seções apropriadas em `references/tools_reference.md`
3. Sugira otimizações e melhores práticas
4. Ofereça solução de problemas para problemas

### Para Tarefas Específicas

**"Converter BAM para bigWig":**
- Use bamCoverage com normalização apropriada
- Recomende RPGC ou CPM com base no caso de uso
- Forneça tamanho de genoma efetivo para organismo
- Sugira parâmetros relevantes (extendReads, ignoreDuplicates, binSize)

**"Verificar qualidade ChIP":**
- Execute workflow QC completo ou use plotFingerprint especificamente
- Explique interpretação de resultados
- Sugira ações de acompanhamento com base em resultados

**"Criar heatmap":**
- Guie por processo em duas etapas: computeMatrix → plotHeatmap
- Ajude a escolher modo de matriz apropriado (reference-point vs scale-regions)
- Sugira parâmetros de visualização e opções de clustering

**"Comparar amostras":**
- Recomende bamCompare para comparação de duas amostras
- Sugira multiBamSummary + plotCorrelation para múltiplas amostras
- Guie seleção de método de normalização

### Referenciando Documentação

Quando usuários precisam de informações detalhadas:
- **Detalhes de ferramentas**: Direcione para seções específicas em `references/tools_reference.md`
- **Workflows**: Use `references/workflows.md` para pipelines de análise completos
- **Normalização**: Consulte `references/normalization_methods.md` para seleção de método
- **Tamanhos de genoma**: Referencie `references/effective_genome_sizes.md`

Busque referências usando padrões grep:
```bash
# Encontrar documentação de ferramenta
grep -A 20 "^### toolname" references/tools_reference.md

# Encontrar workflow
grep -A 50 "^## Workflow Name" references/workflows.md

# Encontrar método de normalização
grep -A 15 "^### Method Name" references/normalization_methods.md
```

## Exemplos de Interações

**Usuário: "Preciso analisar meus dados ChIP-seq"**

Abordagem de resposta:
1. Pergunte sobre arquivos disponíveis (arquivos BAM, peaks, genes)
2. Valide arquivos usando script de validação
3. Gere modelo de workflow chipseq_analysis
4. Customize para seus arquivos e organismo específicos
5. Explique cada etapa conforme o script executa

**Usuário: "Qual normalização devo usar?"**

Abordagem de resposta:
1. Pergunte sobre tipo de experimento (ChIP-seq, RNA-seq, etc.)
2. Pergunte sobre objetivo de comparação (dentro da amostra ou entre amostras)
3. Consulte guia de seleção `references/normalization_methods.md`
4. Recomende método apropriado com justificativa
5. Forneça exemplo de comando com parâmetros

**Usuário: "Criar um heatmap ao redor de TSS"**

Abordagem de resposta:
1. Verifique se arquivos bigWig e BED de genes estão disponíveis
2. Use computeMatrix com modo reference-point em TSS
3. Gere plotHeatmap com parâmetros de visualização apropriados
4. Sugira clustering se o dataset é grande
5. Ofereça gráfico de profile como complemento

## Lembretes-Chave

- **Validação de arquivo primeiro**: Sempre valide arquivos de entrada antes da análise
- **Normalização importa**: Escolha método apropriado para tipo de comparação
- **Estenda leituras com cuidado**: SIM para ChIP-seq, NÃO para RNA-seq
- **Use todos os núcleos**: Defina `--numberOfProcessors` para núcleos disponíveis
- **Teste em regiões**: Use `--region` para teste de parâmetros
- **Verifique QC primeiro**: Execute controle de qualidade antes da análise detalhada
- **Documente tudo**: Salve comandos para reprodutibilidade
- **Referencie documentação**: Use referências abrangentes para orientação detalhada