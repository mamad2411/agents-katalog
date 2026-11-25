---
name: drugbank-database
description: Acesse e analise informações abrangentes sobre medicamentos do banco de dados DrugBank, incluindo propriedades de fármacos, interações, alvo molecular, vias biológicas, estruturas químicas e dados de farmacologia. Esta habilidade deve ser usada ao trabalhar com dados farmacêuticos, pesquisa de descoberta de fármacos, estudos de farmacologia, análise de interações medicamentosas, identificação de alvo molecular, buscas de similaridade química, previsões ADMET ou qualquer tarefa que exija informações detalhadas de fármacos e alvo molecular do DrugBank.
---

# Banco de Dados DrugBank

## Visão Geral

DrugBank é um banco de dados abrangente de bioinformática e quiminformática contendo informações detalhadas sobre medicamentos e alvo molecular de fármacos. Esta habilidade permite acesso programático aos dados do DrugBank incluindo ~9.591 entradas de medicamentos (2.037 moléculas pequenas aprovadas pela FDA, 241 fármacos biotecnológicos, 96 nutracêuticos e 6.000+ compostos experimentais) com 200+ campos de dados por entrada.

## Capacidades Principais

### 1. Acesso de Dados e Autenticação

Baixe e acesse dados do DrugBank usando Python com autenticação apropriada. A habilidade fornece orientação sobre:

- Instalação e configuração do pacote `drugbank-downloader`
- Gerenciamento seguro de credenciais via variáveis de ambiente ou arquivos de configuração
- Download de versões específicas ou mais recentes do banco de dados
- Abertura e análise eficiente de dados XML
- Trabalho com dados em cache para otimizar desempenho

**Quando usar**: Configuração inicial do acesso ao DrugBank, download de atualizações de banco de dados, configuração inicial de projeto.

**Referência**: Consulte `references/data-access.md` para autenticação detalhada, procedimentos de download, acesso à API, estratégias de cache e solução de problemas.

### 2. Consultas de Informações sobre Medicamentos

Extraia informações abrangentes sobre medicamentos do banco de dados, incluindo identificadores, propriedades químicas, farmacologia, dados clínicos e referências cruzadas a bancos de dados externos.

**Capacidades de consulta**:
- Busca por ID DrugBank, nome, número CAS ou palavras-chave
- Extração de informações básicas de medicamentos (nome, tipo, descrição, indicação)
- Recuperação de propriedades químicas (SMILES, InChI, fórmula molecular)
- Obtenção de dados de farmacologia (mecanismo de ação, farmacodinâmica, ADME)
- Acesso a identificadores externos (PubChem, ChEMBL, UniProt, KEGG)
- Construção de conjuntos de dados de medicamentos pesquisáveis e exportação para DataFrames
- Filtragem de medicamentos por tipo (molécula pequena, biotecnológico, nutracêutico)

**Quando usar**: Recuperação de informações específicas sobre medicamentos, construção de bancos de dados de medicamentos, pesquisa em farmacologia, revisão de literatura, perfil de medicamento.

**Referência**: Consulte `references/drug-queries.md` para navegação XML, funções de consulta, métodos de extração de dados e otimização de desempenho.

### 3. Análise de Interações Medicamentosas

Analise interações medicamentosas (DDIs) incluindo mecanismo, significância clínica e redes de interação para farmacovigilância e suporte à decisão clínica.

**Capacidades de análise**:
- Extração de todas as interações para medicamentos específicos
- Construção de redes de interação bidirecionais
- Classificação de interações por gravidade e mecanismo
- Verificação de interações entre pares de medicamentos
- Identificação de medicamentos com mais interações
- Análise de regimes de polifarmácia para segurança
- Criação de matrizes de interação e gráficos de rede
- Detecção de comunidades em redes de interação
- Cálculo de pontuações de risco de interação

**Quando usar**: Análise de segurança em polifarmácia, suporte à decisão clínica, previsão de interação medicamentosa, pesquisa em farmacovigilância, identificação de contraindicações.

**Referência**: Consulte `references/interactions.md` para extração de interações, métodos de classificação, análise de rede e aplicações clínicas.

### 4. Alvo Molecular de Fármacos e Vias Biológicas

Acesse informações detalhadas sobre interações fármaco-proteína, incluindo alvo molecular, enzimas, transportadores, carreadores e vias biológicas.

**Capacidades de análise de alvo molecular**:
- Extração de alvo molecular de fármacos com ações (inibidor, agonista, antagonista)
- Identificação de enzimas metabólicas (CYP450, enzimas de Fase II)
- Análise de transportadores (captação, efluxo) para estudos ADME
- Mapeamento de medicamentos para vias biológicas (SMPDB)
- Busca de medicamentos direcionados a proteínas específicas
- Identificação de medicamentos com alvo molecular compartilhado para reposicionamento
- Análise de polifarmacologia e efeitos fora do alvo
- Extração de termos de Gene Ontology (GO) para alvo molecular
- Referência cruzada com UniProt para dados de proteína

**Quando usar**: Estudos de mecanismo de ação, pesquisa de reposicionamento de fármacos, identificação de alvo molecular, análise de vias, previsão de efeitos fora do alvo, compreensão do metabolismo de fármacos.

**Referência**: Consulte `references/targets-pathways.md` para extração de alvo molecular, análise de vias, estratégias de reposicionamento, perfil de CYP450 e análise de transportador.

### 5. Propriedades Químicas e Similaridade

Realize análise baseada em estrutura, incluindo buscas de similaridade molecular, cálculos de propriedades, buscas de subestrutura e previsões ADMET.

**Capacidades de análise química**:
- Extração de estruturas químicas (SMILES, InChI, fórmula molecular)
- Cálculo de propriedades físico-químicas (PM, logP, PSA, ligações H)
- Aplicação da Regra dos Cinco de Lipinski e regras de Veber
- Cálculo de similaridade Tanimoto entre moléculas
- Geração de impressões digitais moleculares (Morgan, MACCS, topológica)
- Realização de buscas de subestrutura com padrões SMARTS
- Busca de medicamentos estruturalmente similares para reposicionamento
- Criação de matrizes de similaridade para agrupamento de medicamentos
- Previsão de absorção oral e permeabilidade da barreira hematoencefálica
- Análise do espaço químico com PCA e agrupamento
- Exportação de bancos de dados de propriedades químicas

**Quando usar**: Estudos de relação estrutura-atividade (SAR), buscas de similaridade de medicamentos, modelagem QSAR, avaliação de semelhança química com fármacos, previsão ADMET, exploração de espaço químico.

**Referência**: Consulte `references/chemical-analysis.md` para extração de estrutura, cálculos de similaridade, geração de impressão digital, previsões ADMET e análise de espaço químico.

## Fluxos de Trabalho Típicos

### Fluxo de Trabalho de Descoberta de Fármacos
1. Use `data-access.md` para baixar e acessar dados mais recentes do DrugBank
2. Use `drug-queries.md` para construir banco de dados de medicamentos pesquisável
3. Use `chemical-analysis.md` para encontrar compostos similares
4. Use `targets-pathways.md` para identificar alvo molecular compartilhado
5. Use `interactions.md` para verificar segurança de combinações candidatas

### Análise de Segurança em Polifarmácia
1. Use `drug-queries.md` para procurar medicações de paciente
2. Use `interactions.md` para verificar todas as interações pareadas
3. Use `interactions.md` para classificar gravidade de interação
4. Use `interactions.md` para calcular pontuação de risco geral
5. Use `targets-pathways.md` para compreender mecanismos de interação

### Pesquisa de Reposicionamento de Fármacos
1. Use `targets-pathways.md` para encontrar medicamentos com alvo molecular compartilhado
2. Use `chemical-analysis.md` para encontrar medicamentos estruturalmente similares
3. Use `drug-queries.md` para extrair dados de indicação e farmacologia
4. Use `interactions.md` para avaliar terapias de combinação potenciais

### Estudo de Farmacologia
1. Use `drug-queries.md` para extrair medicamento de interesse
2. Use `targets-pathways.md` para identificar todas as interações proteicas
3. Use `targets-pathways.md` para mapear a vias biológicas
4. Use `chemical-analysis.md` para prever propriedades ADMET
5. Use `interactions.md` para identificar potenciais contraindicações

## Requisitos de Instalação

### Pacotes Python
```bash
uv pip install drugbank-downloader  # Acesso principal
uv pip install bioversions          # Detecção de versão mais recente
uv pip install lxml                 # Otimização de análise XML
uv pip install pandas               # Manipulação de dados
uv pip install rdkit                # Quiminformática (para similaridade)
uv pip install networkx             # Análise de rede (para interações)
uv pip install scikit-learn         # ML/agrupamento (para espaço químico)
```

### Configuração de Conta
1. Crie conta gratuita em go.drugbank.com
2. Aceite o acordo de licença (gratuito para uso acadêmico)
3. Obtenha credenciais de nome de usuário e senha
4. Configure credenciais conforme documentado em `references/data-access.md`

## Versão de Dados e Reprodutibilidade

Sempre especifique a versão do DrugBank para pesquisa reprodutível:

```python
from drugbank_downloader import download_drugbank
path = download_drugbank(version='5.1.10')  # Especifique versão exata
```

Documente a versão usada em publicações e scripts de análise.

## Melhores Práticas

1. **Credenciais**: Use variáveis de ambiente ou arquivos de configuração, nunca codifique
2. **Versionamento**: Especifique versão exata do banco de dados para reprodutibilidade
3. **Cache**: Coloque em cache dados analisados para evitar re-download e re-análise
4. **Namespaces**: Trate namespaces XML apropriadamente ao analisar
5. **Validação**: Valide estruturas químicas com RDKit antes de usar
6. **Referência cruzada**: Use identificadores externos (UniProt, PubChem) para integração
7. **Contexto clínico**: Sempre considere contexto clínico ao interpretar dados de interação
8. **Conformidade de licença**: Garanta licenciamento apropriado para seu caso de uso

## Documentação de Referência

Toda orientação de implementação detalhada está organizada em arquivos de referência modular:

- **references/data-access.md**: Autenticação, download, análise, acesso à API, cache
- **references/drug-queries.md**: Navegação XML, métodos de consulta, extração de dados, indexação
- **references/interactions.md**: Extração de DDI, classificação, análise de rede, pontuação de segurança
- **references/targets-pathways.md**: Extração de alvo molecular/enzima/transportador, mapeamento de vias, reposicionamento
- **references/chemical-analysis.md**: Extração de estrutura, similaridade, impressões digitais, previsão ADMET

Carregue essas referências conforme necessário com base em seus requisitos específicos de análise.