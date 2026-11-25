---
name: perplexity-search
description: Realizar buscas na web com IA avançada e informações em tempo real usando modelos Perplexity via LiteLLM e OpenRouter. Esta skill deve ser usada ao conduzir buscas na web por informações atuais, encontrar literatura científica recente, obter respostas fundamentadas com citações de fontes, ou acessar informações além do conhecimento do modelo. Fornece acesso a múltiplos modelos Perplexity incluindo Sonar Pro, Sonar Pro Search (busca agentic avançada) e Sonar Reasoning Pro através de uma única chave API OpenRouter.
---

# Perplexity Search

## Visão Geral

Realizar buscas na web com IA usando modelos Perplexity através do LiteLLM e OpenRouter. Perplexity fornece respostas em tempo real fundamentadas na web com citações de fontes, ideal para encontrar informações atuais, literatura científica recente e fatos além do cutoff de treinamento do modelo.

Esta skill fornece acesso a todos os modelos Perplexity através do OpenRouter, exigindo apenas uma única chave API (nenhuma conta separada do Perplexity necessária).

## Quando Usar Esta Skill

Use esta skill quando:
- Buscar informações atuais ou desenvolvimentos recentes (2024 em diante)
- Encontrar as mais recentes publicações científicas e pesquisas
- Obter respostas em tempo real fundamentadas em fontes da web
- Verificar fatos com citações de fontes
- Conduzir buscas de literatura em múltiplos domínios
- Acessar informações além do cutoff de conhecimento do modelo
- Realizar pesquisa específica de domínio (biomédica, técnica, clínica)
- Comparar abordagens ou tecnologias atuais

**Não use** para:
- Cálculos simples ou problemas de lógica (use diretamente)
- Tarefas que requerem execução de código (use ferramentas padrão)
- Perguntas bem dentro dos dados de treinamento do modelo (a menos que verificação seja necessária)

## Guia Rápido

### Configuração (Uma vez)

1. **Obter chave API OpenRouter**:
   - Visite https://openrouter.ai/keys
   - Crie uma conta e gere a chave API
   - Adicione créditos à conta (mínimo de R$ 25 recomendado)

2. **Configurar ambiente**:
   ```bash
   # Definir chave API
   export OPENROUTER_API_KEY='sk-or-v1-your-key-here'

   # Ou use o script de configuração
   python scripts/setup_env.py --api-key sk-or-v1-your-key-here
   ```

3. **Instalar dependências**:
   ```bash
   uv pip install litellm
   ```

4. **Verificar configuração**:
   ```bash
   python scripts/perplexity_search.py --check-setup
   ```

Veja `references/openrouter_setup.md` para instruções detalhadas de configuração, solução de problemas e melhores práticas de segurança.

### Uso Básico

**Busca simples:**
```bash
python scripts/perplexity_search.py "Quais são os últimos desenvolvimentos em edição de genes CRISPR?"
```

**Salvar resultados:**
```bash
python scripts/perplexity_search.py "Recentes ensaios clínicos de terapia CAR-T" --output results.json
```

**Usar modelo específico:**
```bash
python scripts/perplexity_search.py "Compare vacinas de mRNA e vetores virais" --model sonar-pro-search
```

**Saída detalhada:**
```bash
python scripts/perplexity_search.py "Computação quântica para descoberta de fármacos" --verbose
```

## Modelos Disponíveis

Acesse modelos via parâmetro `--model`:

- **sonar-pro** (padrão): Busca geral, melhor equilíbrio entre custo e qualidade
- **sonar-pro-search**: Busca agentic mais avançada com raciocínio em múltiplas etapas
- **sonar**: Modelo básico, mais econômico para consultas simples
- **sonar-reasoning-pro**: Raciocínio avançado com análise passo a passo
- **sonar-reasoning**: Capacidades básicas de raciocínio

**Guia de seleção de modelo:**
- Consultas padrão → `sonar-pro`
- Análise complexa com múltiplas etapas → `sonar-pro-search`
- Raciocínio explícito necessário → `sonar-reasoning-pro`
- Buscas simples de fatos → `sonar`
- Consultas em lote sensíveis ao custo → `sonar`

Veja `references/model_comparison.md` para comparação detalhada, casos de uso, preços e características de desempenho.

## Elaborando Consultas Eficazes

### Seja Específico e Detalhado

**Bons exemplos:**
- "Quais são os últimos resultados de ensaios clínicos para terapia com células CAR-T no tratamento de linfoma de células B publicados em 2024?"
- "Compare os perfis de eficácia e segurança de vacinas de mRNA versus vacinas de vetor viral para COVID-19"
- "Explique as melhorias do AlphaFold3 sobre o AlphaFold2 com métricas de precisão específicas da pesquisa 2023-2024"

**Maus exemplos:**
- "Me fale sobre tratamento de câncer" (muito amplo)
- "CRISPR" (muito vago)
- "vacinas" (falta especificidade)

### Incluir Restrições de Tempo

As buscas Perplexity acessam dados da web em tempo real:
- "Quais artigos foram publicados em Nature Medicine em 2024 sobre COVID longo?"
- "Quais são os últimos desenvolvimentos (últimos 6 meses) em eficiência de modelos de linguagem grande?"
- "O que foi anunciado na NeurIPS 2023 sobre segurança de IA?"

### Especificar Domínio e Fontes

Para resultados de alta qualidade, mencione preferências de fontes:
- "De acordo com publicações revisadas por pares em periódicos de alto impacto..."
- "Baseado em tratamentos aprovados pela FDA..."
- "De registros de ensaios clínicos como clinicaltrials.gov..."

### Estruturar Consultas Complexas

Divida questões complexas em componentes claros:
1. **Tópico**: Assunto principal
2. **Escopo**: Aspecto específico de interesse
3. **Contexto**: Período, domínio, restrições
4. **Saída**: Formato desejado ou tipo de resposta

**Exemplo:**
"Quais melhorias o AlphaFold3 oferece sobre o AlphaFold2 para predição de estrutura de proteína, de acordo com pesquisas publicadas entre 2023 e 2024? Inclua métricas de precisão específicas e benchmarks."

Veja `references/search_strategies.md` para orientação abrangente sobre design de consultas, padrões específicos de domínio e técnicas avançadas.

## Casos de Uso Comuns

### Busca de Literatura Científica

```bash
python scripts/perplexity_search.py \
  "O que pesquisas recentes (2023-2024) dizem sobre o papel do microbioma intestinal na doença de Parkinson? Foque em estudos revisados por pares e inclua espécies bacterianas específicas identificadas." \
  --model sonar-pro
```

### Documentação Técnica

```bash
python scripts/perplexity_search.py \
  "Como implementar streaming de dados em tempo real do Kafka para PostgreSQL usando Python? Inclua considerações para lidar com backpressure e garantir semântica exactly-once." \
  --model sonar-reasoning-pro
```

### Análise Comparativa

```bash
python scripts/perplexity_search.py \
  "Compare PyTorch versus TensorFlow para implementação de modelos transformer em termos de facilidade de uso, desempenho e suporte de ecossistema. Inclua benchmarks de estudos recentes." \
  --model sonar-pro-search
```

### Pesquisa Clínica

```bash
python scripts/perplexity_search.py \
  "Qual é a evidência para jejum intermitente no manejo de diabetes tipo 2 em adultos? Foque em ensaios clínicos randomizados e reporte mudanças em HbA1c e perda de peso." \
  --model sonar-pro
```

### Análise de Tendências

```bash
python scripts/perplexity_search.py \
  "Quais são as principais tendências em tecnologia de sequenciamento de RNA de célula única nos últimos 5 anos? Destaque melhorias em throughput, custo e resolução, com exemplos específicos." \
  --model sonar-pro
```

## Trabalhando com Resultados

### Acesso Programático

Use `perplexity_search.py` como um módulo:

```python
from scripts.perplexity_search import search_with_perplexity

result = search_with_perplexity(
    query="Quais são os últimos desenvolvimentos em CRISPR?",
    model="openrouter/perplexity/sonar-pro",
    max_tokens=4000,
    temperature=0.2,
    verbose=False
)

if result["success"]:
    print(result["answer"])
    print(f"Tokens usados: {result['usage']['total_tokens']}")
else:
    print(f"Erro: {result['error']}")
```

### Salvar e Processar Resultados

```bash
# Salvar como JSON
python scripts/perplexity_search.py "consulta" --output results.json

# Processar com jq
cat results.json | jq '.answer'
cat results.json | jq '.usage'
```

### Processamento em Lote

Crie um script para múltiplas consultas:

```bash
#!/bin/bash
queries=(
  "Desenvolvimentos CRISPR 2024"
  "Avanços em tecnologia de vacina mRNA"
  "Melhorias de precisão AlphaFold3"
)

for query in "${queries[@]}"; do
  echo "Buscando: $query"
  python scripts/perplexity_search.py "$query" --output "results_$(echo $query | tr ' ' '_').json"
  sleep 2  # Limitação de taxa
done
```

## Gestão de Custos

Os modelos Perplexity têm diferentes faixas de preço:

**Custos aproximados por consulta:**
- Sonar: R$ 0,005-0,010 (mais econômico)
- Sonar Pro: R$ 0,010-0,025 (padrão recomendado)
- Sonar Reasoning Pro: R$ 0,025-0,050
- Sonar Pro Search: R$ 0,100-0,250+ (mais abrangente)

**Estratégias de otimização de custos:**
1. Use `sonar` para buscas simples de fatos
2. Padrão para `sonar-pro` na maioria das consultas
3. Reserve `sonar-pro-search` para análise complexa
4. Defina `--max-tokens` para limitar comprimento de resposta
5. Monitore uso em https://openrouter.ai/activity
6. Defina limites de gastos no dashboard OpenRouter

## Solução de Problemas

### Chave API Não Definida

**Erro**: "Chave API OpenRouter não configurada"

**Solução**:
```bash
export OPENROUTER_API_KEY='sk-or-v1-your-key-here'
# Ou execute o script de configuração
python scripts/setup_env.py --api-key sk-or-v1-your-key-here
```

### LiteLLM Não Instalado

**Erro**: "LiteLLM não instalado"

**Solução**:
```bash
uv pip install litellm
```

### Limitação de Taxa

**Erro**: "Taxa de requisições excedida"

**Soluções**:
- Aguarde alguns segundos antes de tentar novamente
- Aumente o limite de taxa em https://openrouter.ai/keys
- Adicione atrasos entre requisições em processamento em lote

### Créditos Insuficientes

**Erro**: "Créditos insuficientes"

**Solução**:
- Adicione créditos em https://openrouter.ai/account
- Ative recarregamento automático para evitar interrupções

Veja `references/openrouter_setup.md` para guia abrangente de solução de problemas.

## Integração com Outras Skills

Esta skill complementa outras skills científicas:

### Revisão de Literatura

Use com a skill `literature-review`:
1. Use Perplexity para encontrar artigos e preprints recentes
2. Complemente buscas PubMed com resultados da web em tempo real
3. Verifique citações e encontre trabalhos relacionados
4. Descubra desenvolvimentos mais recentes após indexação em banco de dados

### Escrita Científica

Use com a skill `scientific-writing`:
1. Encontre referências recentes para introdução/discussão
2. Verifique estado da arte atual
3. Verifique terminologia e convenções mais recentes
4. Identifique abordagens concorrentes recentes

### Geração de Hipóteses

Use com a skill `hypothesis-generation`:
1. Busque os últimos achados de pesquisa
2. Identifique lacunas atuais no conhecimento
3. Encontre avanços metodológicos recentes
4. Descubra direções de pesquisa emergentes

### Pensamento Crítico

Use com a skill `scientific-critical-thinking`:
1. Encontre evidências a favor e contra hipóteses
2. Localize críticas metodológicas
3. Identifique controvérsias no campo
4. Verifique afirmações com evidências atuais

## Melhores Práticas

### Design de Consultas

1. **Seja específico**: Inclua domínio, período e restrições
2. **Use terminologia**: Palavras-chave e frases apropriadas ao domínio
3. **Especifique fontes**: Mencione tipos de publicação ou periódicos preferidos
4. **Estruture perguntas**: Componentes claros com contexto explícito
5. **Itere**: Refine com base nos resultados iniciais

### Seleção de Modelo

1. **Comece com sonar-pro**: Bom padrão para a maioria das consultas
2. **Aumente para complexidade**: Use sonar-pro-search para análise com múltiplas etapas
3. **Reduza para simplicidade**: Use sonar para fatos básicos
4. **Use modelos de raciocínio**: Quando análise passo a passo for necessária

### Otimização de Custos

1. **Escolha modelos apropriados**: Corresponda modelo à complexidade da consulta
2. **Defina limites de token**: Use `--max-tokens` para controlar custos
3. **Monitore uso**: Verifique dashboard OpenRouter regularmente
4. **Processe em lote eficientemente**: Combine consultas simples relacionadas quando possível
5. **Cache de resultados**: Salve e reutilize resultados para consultas repetidas

### Segurança

1. **Proteja chaves API**: Nunca faça commit no controle de versão
2. **Use variáveis de ambiente**: Mantenha chaves separadas do código
3. **Defina limites de gastos**: Configure no dashboard OpenRouter
4. **Monitore uso**: Fique atento a atividades inesperadas
5. **Rotacione chaves**: Mude as chaves periodicamente

## Recursos

### Recursos Inclusos

**Scripts:**
- `scripts/perplexity_search.py`: Script de busca principal com interface CLI
- `scripts/setup_env.py`: Helper de configuração e validação de ambiente

**Referências:**
- `references/search_strategies.md`: Guia abrangente de design de consultas
- `references/model_comparison.md`: Comparação detalhada de modelos e guia de seleção
- `references/openrouter_setup.md`: Guia completo de configuração, solução de problemas e segurança

**Assets:**
- `assets/.env.example`: Modelo de arquivo de ambiente de exemplo

### Recursos Externos

**OpenRouter:**
- Dashboard: https://openrouter.ai/account
- Chaves API: https://openrouter.ai/keys
- Modelos Perplexity: https://openrouter.ai/perplexity
- Monitoramento de Uso: https://openrouter.ai/activity
- Documentação: https://openrouter.ai/docs

**LiteLLM:**
- Documentação: https://docs.litellm.ai/
- Provedor OpenRouter: https://docs.litellm.ai/docs/providers/openrouter
- GitHub: https://github.com/BerriAI/litellm

**Perplexity:**
- Documentação Oficial: https://docs.perplexity.ai/

## Dependências

### Obrigatórias

```bash
# LiteLLM para acesso à API
uv pip install litellm
```

### Opcionais

```bash
# Para suporte a arquivo .env
uv pip install python-dotenv

# Para processamento JSON (geralmente pré-instalado)
uv pip install jq
```

### Variáveis de Ambiente

Obrigatórias:
- `OPENROUTER_API_KEY`: Sua chave API OpenRouter

Opcionais:
- `DEFAULT_MODEL`: Modelo padrão a usar (padrão: sonar-pro)
- `DEFAULT_MAX_TOKENS`: Tokens máximos padrão (padrão: 4000)
- `DEFAULT_TEMPERATURE`: Temperatura padrão (padrão: 0.2)

## Resumo

Esta skill fornece:

1. **Busca na web em tempo real**: Acesse informações atuais além do cutoff de treinamento
2. **Múltiplos modelos**: De Sonar econômico para Sonar Pro Search avançado
3. **Configuração simples**: Única chave API OpenRouter, nenhuma conta separada do Perplexity
4. **Orientação abrangente**: Referências detalhadas para design de consultas e seleção de modelos
5. **Econômico**: Preços pagos conforme você usa com monitoramento de uso
6. **Foco científico**: Otimizado para pesquisa, busca de literatura e consultas técnicas
7. **Integração fácil**: Funciona perfeitamente com outras skills científicas

Conduza buscas na web com IA para encontrar informações atuais, pesquisas recentes e respostas fundamentadas com citações de fontes.