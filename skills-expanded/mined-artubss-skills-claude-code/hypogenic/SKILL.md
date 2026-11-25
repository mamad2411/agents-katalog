---
name: hypogenic
description: Geração automatizada de hipóteses e testes usando modelos de linguagem grandes. Use esta habilidade ao gerar hipóteses científicas a partir de conjuntos de dados, combinando insights de literatura com dados empíricos, testando hipóteses contra dados observacionais, ou conduzindo exploração sistemática de hipóteses para descoberta científica em domínios como detecção de engano, detecção de conteúdo IA, análise de saúde mental ou outras tarefas de pesquisa empírica.
---

# Hypogenic

## Visão Geral

Hypogenic oferece geração e testes automatizados de hipóteses usando modelos de linguagem grandes para acelerar a descoberta científica. O framework suporta três abordagens: HypoGeniC (geração de hipóteses orientada por dados), HypoRefine (integração sinérgica de literatura e dados) e métodos Union (combinação mecanicista de hipóteses de literatura e orientadas por dados).

## Início Rápido

Comece com Hypogenic em minutos:

```bash
# Instalar o pacote
uv pip install hypogenic

# Clonar conjuntos de dados de exemplo
git clone https://github.com/ChicagoHAI/HypoGeniC-datasets.git ./data

# Executar geração básica de hipóteses
hypogenic_generation --config ./data/your_task/config.yaml --method hypogenic --num_hypotheses 20

# Executar inferência em hipóteses geradas
hypogenic_inference --config ./data/your_task/config.yaml --hypotheses output/hypotheses.json
```

**Ou use a API Python:**

```python
from hypogenic import BaseTask

# Criar tarefa com sua configuração
task = BaseTask(config_path="./data/your_task/config.yaml")

# Gerar hipóteses
task.generate_hypotheses(method="hypogenic", num_hypotheses=20)

# Executar inferência
results = task.inference(hypothesis_bank="./output/hypotheses.json")
```

## Quando Usar Esta Habilidade

Use esta habilidade ao trabalhar em:
- Geração de hipóteses científicas a partir de conjuntos de dados observacionais
- Testes sistemáticos de múltiplas hipóteses concorrentes
- Combinação de insights de literatura com padrões empíricos
- Aceleração da descoberta científica através de ideação automatizada de hipóteses
- Domínios que exigem análise orientada por hipóteses: detecção de engano, identificação de conteúdo gerado por IA, indicadores de saúde mental, modelagem preditiva ou outras pesquisas empíricas

## Recursos Principais

**Geração Automatizada de Hipóteses**
- Gere 10-20+ hipóteses testáveis a partir de dados em minutos
- Refinamento iterativo com base no desempenho de validação
- Suporte para LLMs baseados em API (OpenAI, Anthropic) e locais

**Integração de Literatura**
- Extraia insights de artigos científicos via processamento de PDF
- Combine fundações teóricas com padrões empíricos
- Pipeline sistemático de literatura para hipótese com GROBID

**Otimização de Desempenho**
- Cache Redis reduz custos de API para experimentos repetidos
- Processamento paralelo para testes em larga escala de hipóteses
- Refinamento adaptativo focado em exemplos desafiadores

**Configuração Flexível**
- Engenharia de prompts baseada em templates com injeção de variáveis
- Extração de rótulos personalizada para tarefas específicas de domínio
- Arquitetura modular para fácil extensão

**Resultados Comprovados**
- Melhoria de 8,97% em relação a baselines com poucos exemplos
- Melhoria de 15,75% em relação a abordagens apenas de literatura
- Diversidade de hipóteses 80-84% (insights não redundantes)
- Avaliadores humanos relatam melhorias significativas na tomada de decisão

## Capacidades Principais

### 1. HypoGeniC: Geração de Hipóteses Orientada por Dados

Gere hipóteses unicamente a partir de dados observacionais através de refinamento iterativo.

**Processo:**
1. Inicialize com um pequeno subconjunto de dados para gerar hipóteses candidatas
2. Refine iterativamente as hipóteses com base no desempenho
3. Substitua hipóteses com baixo desempenho por novas a partir de exemplos desafiadores

**Melhor para:** Pesquisa exploratória sem literatura existente, descoberta de padrões em conjuntos de dados novos

### 2. HypoRefine: Integração de Literatura e Dados

Combine sinergicamente literatura existente com dados empíricos através de um framework de agente.

**Processo:**
1. Extraia insights de artigos científicos relevantes (tipicamente 10 artigos)
2. Gere hipóteses fundamentadas em teoria a partir de literatura
3. Gere hipóteses orientadas por dados a partir de padrões observacionais
4. Refine ambos os bancos de hipóteses através de melhoria iterativa

**Melhor para:** Pesquisa com fundações teóricas estabelecidas, validação ou extensão de teorias existentes

### 3. Métodos Union

Combine mecanicisticamente hipóteses apenas de literatura com outputs do framework.

**Variantes:**
- **Literature ∪ HypoGeniC**: Combina hipóteses de literatura com geração orientada por dados
- **Literature ∪ HypoRefine**: Combina hipóteses de literatura com abordagem integrada

**Melhor para:** Cobertura abrangente de hipóteses, eliminação de redundância mantendo perspectivas diversas

## Instalação

Instale via pip:
```bash
uv pip install hypogenic
```

**Dependências opcionais:**
- **Servidor Redis** (porta 6832): Ativa cache de respostas de LLM para reduzir significativamente custos de API durante geração iterativa de hipóteses
- **s2orc-doc2json**: Necessário para processar PDFs de literatura em workflows HypoRefine
- **GROBID**: Necessário para pré-processamento de PDF (veja seção Processamento de Literatura)

**Clone conjuntos de dados de exemplo:**
```bash
# Para exemplos HypoGeniC
git clone https://github.com/ChicagoHAI/HypoGeniC-datasets.git ./data

# Para exemplos HypoRefine/Union
git clone https://github.com/ChicagoHAI/Hypothesis-agent-datasets.git ./data
```

## Formato de Conjunto de Dados

Conjuntos de dados devem seguir o formato HuggingFace datasets com convenções de nomenclatura específicas:

**Arquivos obrigatórios:**
- `<TASK>_train.json`: Dados de treinamento
- `<TASK>_val.json`: Dados de validação  
- `<TASK>_test.json`: Dados de teste

**Chaves obrigatórias em JSON:**
- `text_features_1` até `text_features_n`: Listas de strings contendo valores de features
- `label`: Lista de strings contendo rótulos de verdade fundamental

**Exemplo (previsão de cliques em headlines):**
```json
{
  "headline_1": [
    "What Up, Comet? You Just Got *PROBED*",
    "Scientists Made a Breakthrough in Quantum Computing"
  ],
  "headline_2": [
    "Scientists Everywhere Were Holding Their Breath Today. Here's Why.",
    "New Quantum Computer Achieves Milestone"
  ],
  "label": [
    "Headline 2 has more clicks than Headline 1",
    "Headline 1 has more clicks than Headline 2"
  ]
}
```

**Notas importantes:**
- Todas as listas devem ter o mesmo comprimento
- O formato do rótulo deve corresponder ao formato de saída da função `extract_label()`
- As chaves de features podem ser customizadas para corresponder ao seu domínio (ex: `review_text`, `post_content`, etc.)

## Configuração

Cada tarefa exige um arquivo `config.yaml` especificando:

**Elementos obrigatórios:**
- Caminhos de conjunto de dados (train/val/test)
- Templates de prompts para:
  - Geração de observações
  - Geração em lote de hipóteses
  - Inferência de hipóteses
  - Verificação de relevância
  - Métodos adaptativos (para HypoRefine)

**Capacidades de template:**
- Placeholders de conjunto de dados para injeção dinâmica de variáveis (ex: `${text_features_1}`, `${num_hypotheses}`)
- Funções de extração de rótulos personalizadas para análise específica de domínio
- Estrutura de prompt baseada em papéis (papéis system, user, assistant)

**Estrutura de configuração:**
```yaml
task_name: your_task_name

train_data_path: ./your_task_train.json
val_data_path: ./your_task_val.json
test_data_path: ./your_task_test.json

prompt_templates:
  # Chaves adicionais para componentes de prompt reutilizáveis
  observations: |
    Feature 1: ${text_features_1}
    Feature 2: ${text_features_2}
    Observation: ${label}
  
  # Templates obrigatórios
  batched_generation:
    system: "Your system prompt here"
    user: "Your user prompt with ${num_hypotheses} placeholder"
  
  inference:
    system: "Your inference system prompt"
    user: "Your inference user prompt"
  
  # Templates opcionais para features avançadas
  few_shot_baseline: {...}
  is_relevant: {...}
  adaptive_inference: {...}
  adaptive_selection: {...}
```

Consulte `references/config_template.yaml` para um exemplo de configuração completa.

## Processamento de Literatura (HypoRefine/Union Methods)

Para usar geração de hipóteses baseada em literatura, você deve pré-processar artigos em PDF:

**Passo 1: Configurar GROBID** (primeira vez apenas)
```bash
bash ./modules/setup_grobid.sh
```

**Passo 2: Adicionar arquivos PDF**
Coloque artigos científicos em `literature/YOUR_TASK_NAME/raw/`

**Passo 3: Processar PDFs**
```bash
# Inicie o serviço GROBID
bash ./modules/run_grobid.sh

# Processe PDFs para sua tarefa
cd examples
python pdf_preprocess.py --task_name YOUR_TASK_NAME
```

Isso converte PDFs para formato estruturado para extração de hipóteses. Busca automatizada de literatura será suportada em futuras releases.

## Uso CLI

### Geração de Hipóteses

```bash
hypogenic_generation --help
```

**Parâmetros principais:**
- Caminho do arquivo de configuração da tarefa
- Seleção de modelo (baseado em API ou local)
- Método de geração (HypoGeniC, HypoRefine ou Union)
- Número de hipóteses a gerar
- Diretório de output para bancos de hipóteses

### Inferência de Hipóteses

```bash
hypogenic_inference --help
```

**Parâmetros principais:**
- Caminho do arquivo de configuração da tarefa
- Caminho do arquivo do banco de hipóteses
- Caminho do conjunto de dados de teste
- Método de inferência (padrão ou multi-hipótese)
- Arquivo de output para resultados

## Uso da API Python

Para controle programático e workflows customizados, use Hypogenic diretamente no seu código Python:

### Geração Básica HypoGeniC

```python
from hypogenic import BaseTask

# Clone conjuntos de dados de exemplo primeiro
# git clone https://github.com/ChicagoHAI/HypoGeniC-datasets.git ./data

# Carregue sua tarefa com função extract_label customizada
task = BaseTask(
    config_path="./data/your_task/config.yaml",
    extract_label=lambda text: extract_your_label(text)
)

# Gerar hipóteses
task.generate_hypotheses(
    method="hypogenic",
    num_hypotheses=20,
    output_path="./output/hypotheses.json"
)

# Executar inferência
results = task.inference(
    hypothesis_bank="./output/hypotheses.json",
    test_data="./data/your_task/your_task_test.json"
)
```

### Métodos HypoRefine/Union

```python
# Para abordagens integradas com literatura
# git clone https://github.com/ChicagoHAI/Hypothesis-agent-datasets.git ./data

# Gerar com HypoRefine
task.generate_hypotheses(
    method="hyporefine",
    num_hypotheses=15,
    literature_path="./literature/your_task/",
    output_path="./output/"
)
# Isto gera 3 bancos de hipóteses:
# - HypoRefine (abordagem integrada)
# - Hipóteses apenas de literatura
# - Literature∪HypoRefine (union)
```

### Inferência de Multi-Hipótese

```python
from examples.multi_hyp_inference import run_multi_hypothesis_inference

# Teste múltiplas hipóteses simultaneamente
results = run_multi_hypothesis_inference(
    config_path="./data/your_task/config.yaml",
    hypothesis_bank="./output/hypotheses.json",
    test_data="./data/your_task/your_task_test.json"
)
```

### Extração de Rótulo Customizada

A função `extract_label()` é crítica para análise de outputs de LLM. Implemente-a com base em sua tarefa:

```python
def extract_label(llm_output: str) -> str:
    """Extraia rótulo predito do texto de inferência do LLM.
    
    Comportamento padrão: procura por padrão 'final answer:\s+(.*)'.
    Customize para formato de output específico de seu domínio.
    """
    import re
    match = re.search(r'final answer:\s+(.*)', llm_output, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return llm_output.strip()
```

**Importante:** Os rótulos extraídos devem corresponder ao formato dos valores de `label` no seu conjunto de dados para cálculo correto de acurácia.

## Exemplos de Workflow

### Exemplo 1: Geração de Hipóteses Orientada por Dados (HypoGeniC)

**Cenário:** Detectar conteúdo gerado por IA sem framework teórico prévio

**Passos:**
1. Prepare conjunto de dados com amostras de texto e rótulos (humano vs. gerado por IA)
2. Crie `config.yaml` com templates de prompts apropriados
3. Execute geração de hipóteses:
   ```bash
   hypogenic_generation --config config.yaml --method hypogenic --num_hypotheses 20
   ```
4. Execute inferência no conjunto de teste:
   ```bash
   hypogenic_inference --config config.yaml --hypotheses output/hypotheses.json --test_data data/test.json
   ```
5. Analise resultados para padrões como formalidade, precisão gramatical e diferenças de tom

### Exemplo 2: Testes de Hipóteses Informados por Literatura (HypoRefine)

**Cenário:** Detecção de engano em avaliações de hotel com base em pesquisa existente

**Passos:**
1. Colete 10 artigos relevantes sobre sinais linguísticos de engano
2. Prepare conjunto de dados com avaliações genuínas e fraudulentas
3. Configure `config.yaml` com templates de processamento de literatura e geração de dados
4. Execute HypoRefine:
   ```bash
   hypogenic_generation --config config.yaml --method hyporefine --papers papers/ --num_hypotheses 15
   ```
5. Teste hipóteses examinando frequência de pronomes, especificidade de detalhes e outros padrões linguísticos
6. Compare desempenho de hipóteses baseadas em literatura e orientadas por dados

### Exemplo 3: Cobertura Abrangente de Hipóteses (Método Union)

**Cenário:** Detecção de estresse mental maximizando diversidade de hipóteses

**Passos:**
1. Gere hipóteses de literatura a partir de artigos de pesquisa em saúde mental
2. Gere hipóteses orientadas por dados a partir de posts em redes sociais
3. Execute método Union para combinar e desduplicar:
   ```bash
   hypogenic_generation --config config.yaml --method union --literature_hypotheses lit_hyp.json
   ```
4. Inferência captura tanto construtos teóricos (mudanças no comportamento de postagem) quanto padrões de dados (mudanças em linguagem emocional)

## Otimização de Desempenho

**Cache:** Ative cache Redis para reduzir custos de API e tempo de computação para chamadas repetidas de LLM

**Processamento Paralelo:** Aproveite múltiplos workers para geração em larga escala e testes de hipóteses

**Refinamento Adaptativo:** Use exemplos desafiadores para melhorar iterativamente a qualidade das hipóteses

## Resultados Esperados

Pesquisa usando hypogenic demonstrou:
- Melhoria de 14,19% de acurácia em tarefas de detecção de conteúdo IA
- Melhoria de 7,44% de acurácia em tarefas de detecção de engano
- 80-84% dos pares de hipóteses oferecem insights distintos não redundantes
- Altas classificações de utilidade de avaliadores humanos em múltiplos domínios de pesquisa

## Solução de Problemas

**Problema:** Hipóteses geradas são muito genéricas
**Solução:** Refine templates de prompts em `config.yaml` para solicitar hipóteses mais específicas e testáveis

**Problema:** Desempenho fraco de inferência
**Solução:** Garanta que o conjunto de dados tenha exemplos de treinamento suficientes, ajuste parâmetros de geração de hipóteses ou aumente número de hipóteses

**Problema:** Falhas de extração de rótulo
**Solução:** Implemente função `extract_label()` customizada para análise de output específica de domínio

**Problema:** Falha de processamento de PDF do GROBID
**Solução:** Garanta que o serviço GROBID está em execução (`bash ./modules/run_grobid.sh`) e PDFs são artigos científicos válidos

## Criando Tarefas Customizadas

Para adicionar uma nova tarefa ou conjunto de dados ao Hypogenic:

### Passo 1: Prepare Seu Conjunto de Dados

Crie três arquivos JSON seguindo o formato obrigatório:
- `your_task_train.json`
- `your_task_val.json`
- `your_task_test.json`

Cada arquivo deve ter chaves para features de texto (`text_features_1`, etc.) e `label`.

### Passo 2: Crie config.yaml

Defina a configuração de sua tarefa com:
- Nome da tarefa e caminhos de conjunto de dados
- Templates de prompts para observações, geração, inferência
- Qualquer chave adicional para componentes de prompt reutilizáveis
- Variáveis placeholder (ex: `${text_features_1}`, `${num_hypotheses}`)

### Passo 3: Implemente Função extract_label

Crie uma função de extração de rótulo customizada que analisa outputs de LLM para seu domínio:

```python
from hypogenic import BaseTask

def extract_my_label(llm_output: str) -> str:
    """Extração de rótulo customizada para sua tarefa.
    
    Deve retornar rótulos no mesmo formato que o campo 'label' do conjunto de dados.
    """
    # Exemplo: Extrair de formato específico
    if "Final prediction:" in llm_output:
        return llm_output.split("Final prediction:")[-1].strip()
    
    # Fallback para padrão padrão
    import re
    match = re.search(r'final answer:\s+(.*)', llm_output, re.IGNORECASE)
    return match.group(1).strip() if match else llm_output.strip()

# Use sua tarefa customizada
task = BaseTask(
    config_path="./your_task/config.yaml",
    extract_label=extract_my_label
)
```

### Passo 4: (Opcional) Processe Literatura

Para métodos HypoRefine/Union:
1. Crie diretório `literature/your_task_name/raw/`
2. Adicione PDFs de artigos científicos relevantes
3. Execute pré-processamento GROBID
4. Processe com `pdf_preprocess.py`

### Passo 5: Gere e Teste

Execute geração de hipóteses e inferência usando CLI ou API Python:

```bash
# Abordagem CLI
hypogenic_generation --config your_task/config.yaml --method hypogenic --num_hypotheses 20
hypogenic_inference --config your_task/config.yaml --hypotheses output/hypotheses.json

# Ou use API Python (veja seção Uso da API Python)
```

## Estrutura do Repositório

Compreendendo o layout do repositório:

```
hypothesis-generation/
├── hypogenic/              # Código do pacote principal
├── hypogenic_cmd/          # Pontos de entrada CLI
├── hypothesis_agent/       # Framework de agente HypoRefine
├── literature/            # Utilitários de processamento de literatura
├── modules/               # Módulos GROBID e pré-processamento
├── examples/              # Scripts de exemplo
│   ├── generation.py      # Geração HypoGeniC básica
│   ├── union_generation.py # Geração HypoRefine/Union
│   ├── inference.py       # Inferência de hipótese única
│   ├── multi_hyp_inference.py # Inferência de múltiplas hipóteses
│   └── pdf_preprocess.py  # Processamento de PDF de literatura
├── data/                  # Conjuntos de dados de exemplo (clone separadamente)
├── tests/                 # Testes unitários
└── IO_prompting/          # Templates de prompts e experimentos
```

**Diretórios principais:**
- **hypogenic/**: Pacote principal com BaseTask e lógica de geração
- **examples/**: Implementações de referência para workflows comuns
- **literature/**: Ferramentas para processamento de PDF e extração de literatura
- **modules/**: Integrações de ferramentas externas (GROBID, etc.)

## Publicações Relacionadas

### HypoBench (2025)

Liu, H., Huang, S., Hu, J., Zhou, Y., & Tan, C. (2025). HypoBench: Towards Systematic and Principled Benchmarking for Hypothesis Generation. arXiv preprint arXiv:2504.11524.

- **Paper:** https://arxiv.org/abs/2504.11524
- **Description:** Framework de benchmarking para avaliação sistemática de métodos de geração de hipóteses

**BibTeX:**
```bibtex
@misc{liu2025hypobenchsystematicprincipledbenchmarking,
      title={HypoBench: Towards Systematic and Principled Benchmarking for Hypothesis Generation}, 
      author={Haokun Liu and Sicong Huang and Jingyu Hu and Yangqiaoyu Zhou and Chenhao Tan},
      year={2025},
      eprint={2504.11524},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2504.11524}, 
}
```

### Literature Meets Data (2024)

Liu, H., Zhou, Y., Li, M., Yuan, C., & Tan, C. (2024). Literature Meets Data: A Synergistic Approach to Hypothesis Generation. arXiv preprint arXiv:2410.17309.

- **Paper:** https://arxiv.org/abs/2410.17309
- **Code:** https://github.com/ChicagoHAI/hypothesis-generation
- **Description:** Apresenta HypoRefine e demonstra combinação sinérgica de geração de hipóteses baseada em literatura e orientada por dados

**BibTeX:**
```bibtex
@misc{liu2024literaturemeetsdatasynergistic,
      title={Literature Meets Data: A Synergistic Approach to Hypothesis Generation}, 
      author={Haokun Liu and Yangqiaoyu Zhou and Mingxuan Li and Chenfei Yuan and Chenhao Tan},
      year={2024},
      eprint={2410.17309},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2410.17309}, 
}
```

### Hypothesis Generation with Large Language Models (2024)

Zhou, Y., Liu, H., Srivastava, T., Mei, H., & Tan, C. (2024). Hypothesis Generation with Large Language Models. In Proceedings of EMNLP Workshop of NLP for Science.

- **Paper:** https://aclanthology.org/2024.nlp4science-1.10/
- **Description:** Framework HypoGeniC original para geração de hipóteses orientada por dados

**BibTeX:**
```bibtex
@inproceedings{zhou2024hypothesisgenerationlargelanguage,
      title={Hypothesis Generation with Large Language Models}, 
      author={Yangqiaoyu Zhou and Haokun Liu and Tejes Srivastava and Hongyuan Mei and Chenhao Tan},
      booktitle = {Proceedings of EMNLP Workshop of NLP for Science},
      year={2024},
      url={https://aclanthology.org/2024.nlp4science-1.10/},
}
```

## Recursos Adicionais

### Links Oficiais

- **Repositório GitHub:** https://github.com/ChicagoHAI/hypothesis-generation
- **Pacote PyPI:** https://pypi.org/project/hypogenic/
- **Licença:** MIT License
- **Issues & Suporte:** https://github.com/ChicagoHAI/hypothesis-generation/issues

### Conjuntos de Dados de Exemplo

Clone estes repositórios para exemplos prontos para uso:

```bash
# Exemplos HypoGeniC (apenas orientado por dados)
git clone https://github.com/ChicagoHAI/HypoGeniC-datasets.git ./data

# Exemplos HypoRefine/Union (literatura + dados)
git clone https://github.com/ChicagoHAI/Hypothesis-agent-datasets.git ./data
```

### Comunidade & Contribuições

- **Contribuidores:** 7+ colaboradores ativos
- **Stars:** 89+ no GitHub
- **Tópicos:** research-tool, interpretability, hypothesis-generation, scientific-discovery, llm-application

Para contribuições ou dúvidas, visite o repositório GitHub e verifique a página de issues.

## Recursos Locais

### references/

`config_template.yaml` - Arquivo de configuração de exemplo completo com todos os templates de prompts obrigatórios e parâmetros. Isto inclui:
- Estrutura YAML completa para configuração de tarefa
- Templates de prompts de exemplo para todos os métodos
- Documentação de variáveis placeholder
- Exemplos de prompt baseado em papéis

### scripts/

Diretório de scripts está disponível para:
- Utilitários de preparação de dados customizados
- Ferramentas de conversão de formato
- Scripts de análise e avaliação
- Integração com ferramentas externas

### assets/

Diretório de assets está disponível para:
- Conjuntos de dados de exemplo e templates
- Bancos de hipóteses de exemplo
- Outputs de visualização
- Suplementos de documentação