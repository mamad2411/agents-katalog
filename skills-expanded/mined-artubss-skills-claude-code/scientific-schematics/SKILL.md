---
name: scientific-schematics
description: "Crie diagramas científicos de qualidade para publicação usando Nano Banana Pro AI com refinamento iterativo inteligente. Usa Gemini 3 Pro para revisão de qualidade. Regenera apenas se a qualidade estiver abaixo do limite para seu tipo de documento. Especializado em arquiteturas de redes neurais, diagramas de sistema, fluxogramas, vias biológicas e visualizações científicas complexas."
allowed-tools: [Read, Write, Edit, Bash]
---

# Esquemas e Diagramas Científicos

## Visão Geral

Esquemas e diagramas científicos transformam conceitos complexos em representações visuais claras para publicação. **Esta habilidade usa Nano Banana Pro AI para geração de diagramas com revisão de qualidade por Gemini 3 Pro.**

**Como funciona:**
- Descreva seu diagrama em linguagem natural
- Nano Banana Pro gera imagens de qualidade para publicação automaticamente
- **Gemini 3 Pro revisa a qualidade** em relação aos limites do tipo de documento
- **Iteração inteligente**: Regenera apenas se a qualidade estiver abaixo do limite
- Saída pronta para publicação em minutos
- Sem código, templates ou desenho manual necessário

**Limites de Qualidade por Tipo de Documento:**
| Tipo de Documento | Limite | Descrição |
|------------------|--------|-----------|
| journal | 8.5/10 | Nature, Science, periódicos revisados por pares |
| conference | 8.0/10 | Artigos de conferência |
| thesis | 8.0/10 | Dissertações, teses |
| grant | 8.0/10 | Propostas de financiamento |
| preprint | 7.5/10 | arXiv, bioRxiv, etc. |
| report | 7.5/10 | Relatórios técnicos |
| poster | 7.0/10 | Pôsteres acadêmicos |
| presentation | 6.5/10 | Slides, palestras |
| default | 7.5/10 | Propósito geral |

**Basta descrever o que você quer, e Nano Banana Pro cria.** Todos os diagramas são armazenados na subpasta figures/ e referenciados em papers/posters.

## Início Rápido: Gere Qualquer Diagrama

Crie qualquer diagrama científico simplesmente descrevendo-o. Nano Banana Pro cuida de tudo automaticamente com **iteração inteligente**:

```bash
# Gere para artigo de periódico (limite de qualidade mais alto: 8.5/10)
python scripts/generate_schematic.py "Diagrama de fluxo de participantes CONSORT com 500 rastreados, 150 excluídos, 350 randomizados" -o figures/consort.png --doc-type journal

# Gere para apresentação (limite menor: 6.5/10 - mais rápido)
python scripts/generate_schematic.py "Arquitetura encoder-decoder do Transformer mostrando atenção multi-cabeça" -o figures/transformer.png --doc-type presentation

# Gere para pôster (limite moderado: 7.0/10)
python scripts/generate_schematic.py "Via de sinalização MAPK de EGFR para transcrição gênica" -o figures/mapk_pathway.png --doc-type poster

# Iterações máximas personalizadas (máx 2)
python scripts/generate_schematic.py "Diagrama de circuito complexo com amp-op, resistores e capacitores" -o figures/circuit.png --iterations 2 --doc-type journal
```

**O que acontece nos bastidores:**
1. **Geração 1**: Nano Banana Pro cria imagem inicial seguindo as melhores práticas para diagramas científicos
2. **Revisão 1**: **Gemini 3 Pro** avalia a qualidade em relação ao limite do tipo de documento
3. **Decisão**: Se qualidade >= limite → **PRONTO** (sem mais iterações necessárias!)
4. **Se abaixo do limite**: Prompt aprimorado baseado na crítica, regenera
5. **Repete**: Até que a qualidade atenda ao limite OU máximo de iterações atingido

**Benefícios da Iteração Inteligente:**
- ✅ Economiza chamadas de API se a primeira geração é boa o suficiente
- ✅ Padrões de qualidade mais altos para artigos de periódicos
- ✅ Entrega mais rápida para apresentações/pôsteres
- ✅ Qualidade apropriada para cada caso de uso

**Saída**: Imagens versionadas mais um log detalhado de revisão com pontuações de qualidade, críticas e informações de parada antecipada.

### Configuração

Defina sua chave de API do OpenRouter:
```bash
export OPENROUTER_API_KEY='your_api_key_here'
```

Obtenha uma chave de API em: https://openrouter.ai/keys

### Melhores Práticas para Geração de IA

**Prompts Eficazes para Diagramas Científicos:**

✓ **Bons prompts** (específicos, detalhados):
- "Fluxograma CONSORT mostrando fluxo de participantes desde rastreamento (n=500) através de randomização até análise final"
- "Arquitetura de rede neural Transformer com pilha de encoder à esquerda, pilha de decoder à direita, mostrando conexões de atenção multi-cabeça e atenção cruzada"
- "Cascata de sinalização biológica: receptor EGFR → RAS → RAF → MEK → ERK → núcleo, com etapas de fosforilação rotuladas"
- "Diagrama de bloco do sistema IoT: sensores → microcontrolador → módulo WiFi → servidor em nuvem → aplicativo móvel"

✗ **Evite prompts vagos**:
- "Faça um fluxograma" (muito genérico)
- "Rede neural" (qual tipo? quais componentes?)
- "Diagrama de via" (qual via? quais moléculas?)

**Elementos-chave a incluir:**
- **Tipo**: Fluxograma, diagrama de arquitetura, via, circuito, etc.
- **Componentes**: Elementos específicos a incluir
- **Fluxo/Direção**: Como os elementos se conectam (esquerda-para-direita, topo-para-baixo)
- **Rótulos**: Anotações ou texto chave a incluir
- **Estilo**: Quaisquer requisitos visuais específicos

**Diretrizes de Qualidade Científica** (aplicadas automaticamente):
- Fundo limpo/claro branco
- Alto contraste para legibilidade
- Rótulos claros e legíveis (mínimo 10pt)
- Tipografia profissional (fontes sem serifa)
- Cores amigáveis para daltônicos (paleta Okabe-Ito)
- Espaçamento adequado para evitar aglomeração
- Barras de escala, legendas, eixos quando apropriado

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada quando:
- Criar diagramas de arquitetura de rede neural (Transformers, CNNs, RNNs, etc.)
- Ilustrar arquiteturas de sistema e diagramas de fluxo de dados
- Desenhar fluxogramas de metodologia para design de estudo (CONSORT, PRISMA)
- Visualizar workflows de algoritmos e pipelines de processamento
- Criar diagramas de circuito e esquemas elétricos
- Representar vias biológicas e interações moleculares
- Gerar topologias de rede e estruturas hierárquicas
- Ilustrar frameworks conceituais e modelos teóricos
- Projetar diagramas de bloco para artigos técnicos

## Como Usar Esta Habilidade

**Simplesmente descreva seu diagrama em linguagem natural.** Nano Banana Pro gera automaticamente:

```bash
python scripts/generate_schematic.py "sua descrição do diagrama" -o output.png
```

**Pronto!** A IA cuida de:
- ✓ Layout e composição
- ✓ Rótulos e anotações
- ✓ Cores e estilo
- ✓ Revisão de qualidade e refinamento
- ✓ Saída pronta para publicação

**Funciona para todos os tipos de diagrama:**
- Fluxogramas (CONSORT, PRISMA, etc.)
- Arquiteturas de rede neural
- Vias biológicas
- Diagramas de circuito
- Arquiteturas de sistema
- Diagramas de bloco
- Qualquer visualização científica

**Sem código, templates ou desenho manual necessário.**

---

# Modo de Geração por IA (Nano Banana Pro + Revisão por Gemini 3 Pro)

## Workflow de Refinamento Iterativo Inteligente

O sistema de geração por IA usa **iteração inteligente** - regenera apenas se a qualidade estiver abaixo do limite para seu tipo de documento:

### Como a Iteração Inteligente Funciona

```
┌─────────────────────────────────────────────────────┐
│  1. Gere imagem com Nano Banana Pro                 │
│                    ↓                                │
│  2. Revise qualidade com Gemini 3 Pro               │
│                    ↓                                │
│  3. Pontuação >= limite?                            │
│       SIM → PRONTO! (parada antecipada)             │
│       NÃO  → Melhore prompt, vá para etapa 1       │
│                    ↓                                │
│  4. Repita até qualidade atingida OU máx iterações │
└─────────────────────────────────────────────────────┘
```

### Iteração 1: Geração Inicial
**Construção de Prompt:**
```
Diretrizes de diagrama científico + Solicitação do usuário
```

**Saída:** `diagram_v1.png`

### Revisão de Qualidade por Gemini 3 Pro

Gemini 3 Pro avalia o diagrama em:
1. **Precisão Científica** (0-2 pontos) - Conceitos, notação, relações corretos
2. **Clareza e Legibilidade** (0-2 pontos) - Fácil de entender, hierarquia clara
3. **Qualidade de Rótulos** (0-2 pontos) - Rótulos completos, legíveis, consistentes
4. **Layout e Composição** (0-2 pontos) - Fluxo lógico, balanceado, sem sobreposições
5. **Aparência Profissional** (0-2 pontos) - Qualidade pronta para publicação

**Exemplo de Saída de Revisão:**
```
PONTUAÇÃO: 8.0

PONTOS FORTES:
- Fluxo claro de topo para base
- Todas as fases devidamente rotuladas
- Tipografia profissional

PROBLEMAS:
- Contagens de participantes ligeiramente pequenas
- Pequena sobreposição na caixa de exclusão

VEREDICTO: ACEITÁVEL (para pôster, limite 7.0)
```

### Ponto de Decisão: Continuar ou Parar?

| Se Pontuação... | Ação |
|-----------------|------|
| >= limite | **PARAR** - Qualidade é boa o suficiente para este tipo de documento |
| < limite | Continuar para próxima iteração com prompt aprimorado |

**Exemplo:**
- Para um **pôster** (limite 7.0): Pontuação de 7.5 → **PRONTO após 1 iteração!**
- Para um **periódico** (limite 8.5): Pontuação de 7.5 → Continuar melhorando

### Iterações Subsequentes (Apenas Se Necessário)

Se a qualidade estiver abaixo do limite, o sistema:
1. Extrai problemas específicos da revisão de Gemini 3 Pro
2. Melhora o prompt com instruções de aprimoramento
3. Regenera com Nano Banana Pro
4. Revisa novamente com Gemini 3 Pro
5. Repete até que o limite seja atingido ou máximo de iterações alcançado

### Log de Revisão
Todas as iterações são salvas com um log de revisão JSON que inclui informações de parada antecipada:
```json
{
  "user_prompt": "Diagrama de fluxo de participantes CONSORT...",
  "doc_type": "poster",
  "quality_threshold": 7.0,
  "iterations": [
    {
      "iteration": 1,
      "image_path": "figures/consort_v1.png",
      "score": 7.5,
      "needs_improvement": false,
      "critique": "PONTUAÇÃO: 7.5\nPONTOS FORTES:..."
    }
  ],
  "final_score": 7.5,
  "early_stop": true,
  "early_stop_reason": "Pontuação de qualidade 7.5 atende ao limite 7.0 para pôster"
}
```

**Nota:** Com iteração inteligente, você pode ver apenas 1 iteração em vez das 2 completas se a qualidade for alcançada cedo!

## Uso Avançado de Geração por IA

### API Python

```python
from scripts.generate_schematic_ai import ScientificSchematicGenerator

# Inicializar gerador
generator = ScientificSchematicGenerator(
    api_key="your_openrouter_key",
    verbose=True
)

# Gere com refinamento iterativo (máx 2 iterações)
results = generator.generate_iterative(
    user_prompt="Diagrama de arquitetura Transformer",
    output_path="figures/transformer.png",
    iterations=2
)

# Acesse resultados
print(f"Pontuação final: {results['final_score']}/10")
print(f"Imagem final: {results['final_image']}")

# Revise iterações individuais
for iteration in results['iterations']:
    print(f"Iteração {iteration['iteration']}: {iteration['score']}/10")
    print(f"Crítica: {iteration['critique']}")
```

### Opções de Linha de Comando

```bash
# Uso básico (limite padrão 7.5/10)
python scripts/generate_schematic.py "descrição do diagrama" -o output.png

# Especifique tipo de documento para limite de qualidade apropriado
python scripts/generate_schematic.py "diagrama" -o out.png --doc-type journal      # 8.5/10
python scripts/generate_schematic.py "diagrama" -o out.png --doc-type conference   # 8.0/10
python scripts/generate_schematic.py "diagrama" -o out.png --doc-type poster       # 7.0/10
python scripts/generate_schematic.py "diagrama" -o out.png --doc-type presentation # 6.5/10

# Iterações máximas personalizadas (1-2)
python scripts/generate_schematic.py "diagrama complexo" -o diagram.png --iterations 2

# Saída detalhada (veja todas as chamadas de API e revisões)
python scripts/generate_schematic.py "fluxograma" -o flow.png -v

# Forneça chave de API via flag
python scripts/generate_schematic.py "diagrama" -o out.png --api-key "sk-or-v1-..."

# Combine opções
python scripts/generate_schematic.py "rede neural" -o nn.png --doc-type journal --iterations 2 -v
```

### Dicas de Engenharia de Prompt

**1. Seja Específico Sobre Layout:**
```
✓ "Fluxograma com fluxo vertical, topo para base"
✓ "Diagrama de arquitetura com encoder à esquerda, decoder à direita"
✓ "Diagrama de via circular com fluxo no sentido horário"
```

**2. Inclua Detalhes Quantitativos:**
```
✓ "Rede neural com camada de entrada (784 nós), camada oculta (128 nós), saída (10 nós)"
✓ "Fluxograma mostrando n=500 rastreados, n=150 excluídos, n=350 randomizados"
✓ "Circuito com resistor de 1kΩ, capacitor de 10µF, fonte de 5V"
```

**3. Especifique Estilo Visual:**
```
✓ "Diagrama de bloco minimalista com linhas limpas"
✓ "Via biológica detalhada com estruturas de proteína"
✓ "Esquema técnico com notação de engenharia"
```

**4. Solicite Rótulos Específicos:**
```
✓ "Rotule todas as setas com ativação/inibição"
✓ "Inclua dimensões de camada em cada caixa"
✓ "Mostre progressão de tempo com timestamps"
```

**5. Mencione Requisitos de Cor:**
```
✓ "Use cores amigáveis para daltônicos"
✓ "Design compatível com escala de cinza"
✓ "Código de cores por função: azul para entrada, verde para processamento, vermelho para saída"
```

## Exemplos de Geração por IA

### Exemplo 1: Fluxograma CONSORT
```bash
python scripts/generate_schematic.py \
  "Diagrama de fluxo de participantes CONSORT para ensaio clínico randomizado. \
   Comece com 'Avaliado para elegibilidade (n=500)' no topo. \
   Mostre 'Excluído (n=150)' com motivos: idade<18 (n=80), recusou (n=50), outro (n=20). \
   Então 'Randomizado (n=350)' dividido em dois grupos: \
   'Grupo de tratamento (n=175)' e 'Grupo controle (n=175)'. \
   Cada grupo mostra 'Perdido em acompanhamento' (n=15 e n=10). \
   Termine com 'Analisado' (n=160 e n=165). \
   Use caixas azuis para etapas de processo, laranja para exclusão, verde para análise final." \
  -o figures/consort.png
```

### Exemplo 2: Arquitetura de Rede Neural
```bash
python scripts/generate_schematic.py \
  "Diagrama de arquitetura encoder-decoder Transformer. \
   Lado esquerdo: Pilha de encoder com embedding de entrada, codificação posicional, \
   atenção multi-cabeça auto-supervisionada, adicionar & normalizar, alimentação direta, adicionar & normalizar. \
   Lado direito: Pilha de decoder com embedding de saída, codificação posicional, \
   atenção auto-supervisionada mascarada, adicionar & normalizar, atenção cruzada (recebendo do encoder), \
   adicionar & normalizar, linear & softmax. \
   Mostre conexão de atenção cruzada do encoder para decoder com linha tracejada. \
   Use azul claro para encoder, vermelho claro para decoder. \
   Rotule todos os componentes claramente." \
  -o figures/transformer.png --iterations 2
```

### Exemplo 3: Via Biológica
```bash
python scripts/generate_schematic.py \
  "Diagrama de via de sinalização MAPK. \
   Comece com receptor EGFR na membrana celular (topo). \
   Seta para baixo para RAS (com rótulo GTP). \
   Seta para quinase RAF. \
   Seta para quinase MEK. \
   Seta para quinase ERK. \
   Seta final para núcleo mostrando transcrição gênica. \
   Rotule cada seta com 'fosforilação' ou 'ativação'. \
   Use retângulos arredondados para proteínas, cores diferentes para cada. \
   Inclua linha de limite de membrana no topo." \
  -o figures/mapk_pathway.png
```

### Exemplo 4: Arquitetura de Sistema
```bash
python scripts/generate_schematic.py \
  "Diagrama de arquitetura de bloco do sistema IoT. \
   Camada inferior: Sensores (temperatura, umidade, movimento) em caixas verdes. \
   Camada do meio: Microcontrolador (ESP32) em caixa azul. \
   Conexões com módulo WiFi (caixa laranja) e Display (caixa roxa). \
   Camada superior: Servidor em nuvem (caixa cinza) conectado a aplicativo móvel (caixa azul claro). \
   Mostre setas de fluxo de dados entre todos os componentes. \
   Rotule conexões com protocolos: I2C, UART, WiFi, HTTPS." \
  -o figures/iot_architecture.png
```

---

## Uso de Linha de Comando

O ponto de entrada principal para gerar esquemas científicos:

```bash
# Uso básico
python scripts/generate_schematic.py "descrição do diagrama" -o output.png

# Iterações personalizadas (máx 2)
python scripts/generate_schematic.py "diagrama complexo" -o diagram.png --iterations 2

# Modo detalhado
python scripts/generate_schematic.py "diagrama" -o out.png -v
```

**Nota:** O sistema de geração por IA Nano Banana Pro inclui revisão automática de qualidade em seu processo de refinamento iterativo. Cada iteração é avaliada quanto à precisão científica, clareza e acessibilidade.

## Resumo de Melhores Práticas

### Princípios de Design

1. **Clareza sobre complexidade** - Simplifique, remova elementos desnecessários
2. **Estilo consistente** - Use templates e arquivos de estilo
3. **Acessibilidade para daltônicos** - Use paleta Okabe-Ito, codificação redundante
4. **Tipografia apropriada** - Fontes sem serifa, mínimo 7-8 pt
5. **Formato vetorial** - Sempre use PDF/SVG para publicação

### Requisitos Técnicos

1. **Resolução** - Vetorial preferível, ou 300+ DPI para raster
2. **Formato de arquivo** - PDF para LaTeX, SVG para web, PNG como fallback
3. **Espaço de cor** - RGB para digital, CMYK para impressão (converta se necessário)
4. **Espessura de linha** - Mínimo 0.5 pt, típico 1-2 pt
5. **Tamanho de texto** - Mínimo 7-8 pt no tamanho final

### Diretrizes de Integração

1. **Inclua em LaTeX** - Use `\includegraphics{}` para imagens geradas
2. **Legenda completa** - Descreva todos os elementos e abreviações
3. **Referencie no texto** - Explique diagrama no fluxo narrativo
4. **Mantenha consistência** - Mesmo estilo em todos os gráficos do artigo
5. **Controle de versão** - Mantenha prompts e imagens geradas no repositório

## Resolução de Problemas Comuns

### Problemas de Geração por IA

**Problema**: Texto ou elementos sobrepostos
- **Solução**: Geração por IA cuida automaticamente de espaçamento
- **Solução**: Aumente iterações: `--iterations 2` para melhor refinamento

**Problema**: Elementos não conectam adequadamente
- **Solução**: Torne seu prompt mais específico sobre conexões e layout
- **Solução**: Aumente iterações para melhor refinamento

### Problemas de Qualidade de Imagem

**Problema**: Qualidade de exportação fraca
- **Solução**: Geração por IA produz imagens de alta qualidade automaticamente
- **Solução**: Aumente iterações para melhores resultados: `--iterations 2`

**Problema**: Elementos se sobrepõem após geração
- **Solução**: Geração por IA cuida automaticamente de espaçamento
- **Solução**: Aumente iterações: `--iterations 2` para melhor refinamento
- **Solução**: Torne seu prompt mais específico sobre requisitos de layout e espaçamento

### Problemas de Verificação de Qualidade

**Problema**: Detecção falsa positiva de sobreposição
- **Solução**: Ajuste limite: `detect_overlaps(image_path, threshold=0.98)`
- **Solução**: Revise manualmente regiões sinalizadas no relatório visual

**Problema**: Qualidade de imagem gerada é baixa
- **Solução**: Geração por IA produz imagens de alta qualidade por padrão
- **Solução**: Aumente iterações para melhores resultados: `--iterations 2`

**Problema**: Simulação de daltonismo mostra contraste fraco
- **Solução**: Mude para paleta Okabe-Ito explicitamente no código
- **Solução**: Adicione codificação redundante (formas, padrões, estilos de linha)
- **Solução**: Aumente saturação de cor e diferenças de luminosidade

**Problema**: Sobreposições de alta severidade detectadas
- **Solução**: Revise overlap_report.json para posições exatas
- **Solução**: Aumente espaçamento nessas regiões específicas
- **Solução**: Re-execute com parâmetros ajustados e verifique novamente

**Problema**: Geração de relatório visual falha
- **Solução**: Verifique instalações de Pillow e matplotlib
- **Solução**: Garanta que arquivo de imagem é legível: `Image.open(path).verify()`
- **Solução**: Verifique espaço em disco suficiente para geração de relatório

### Problemas de Acessibilidade

**Problema**: Cores indistinguíveis em escala de cinza
- **Solução**: Execute verificador de acessibilidade: `verify_accessibility(image_path)`
- **Solução**: Adicione padrões, formas ou estilos de linha para redundância
- **Solução**: Aumente contraste entre elementos adjacentes

**Problema**: Texto muito pequeno quando impresso
- **Solução**: Execute validador de resolução: `validate_resolution(image_path)`
- **Solução**: Projete no tamanho final, use fontes mínimas de 7-8 pt
- **Solução**: Verifique dimensões físicas no relatório de resolução

**Problema**: Verificações de acessibilidade falham consistentemente
- **Solução**: Revise accessibility_report.json para falhas específicas
- **Solução**: Aumente contraste de cor em pelo menos 20%
- **Solução**: Teste com conversão real em escala de cinza antes de finalizar

## Recursos e Referências

### Referências Detalhadas

Carregue estes arquivos para informações abrangentes sobre tópicos específicos:

- **`references/diagram_types.md`** - Catálogo de tipos de diagrama científico com exemplos
- **`references/best_practices.md`** - Padrões de publicação e diretrizes de acessibilidade

### Recursos Externos

**Bibliotecas Python**
- Documentação Schemdraw: https://schemdraw.readthedocs.io/
- Documentação NetworkX: https://networkx.org/documentation/
- Documentação Matplotlib: https://matplotlib.org/

**Padrões de Publicação**
- Diretrizes de Gráficos da Nature: https://www.nature.com/nature/for-authors/final-submission
- Diretrizes de Gráficos da Science: https://www.science.org/content/page/instructions-preparing-initial-manuscript
- Diagrama CONSORT: http://www.consort-statement.org/consort-statement/flow-diagram

## Integração com Outras Habilidades

Esta habilidade funciona sinergeticamente com:

- **Escrita Científica** - Diagramas seguem melhores práticas de gráficos
- **Visualização Científica** - Compartilha paletas de cores e estilo
- **Pôsteres LaTeX** - Gere diagramas para apresentações em pôster
- **Financiamento de Pesquisa** - Diagramas de metodologia para propostas
- **Revisão por Pares** - Avalie clareza e acessibilidade de diagrama

## Lista de Verificação de Referência Rápida

Antes de enviar diagramas, verifique:

### Qualidade Visual
- [ ] Formato de imagem de alta qualidade (PNG da geração por IA)
- [ ] Sem elementos sobrepostos (IA cuida automaticamente)
- [ ] Espaçamento adequado entre todos os componentes (IA otimiza)
- [ ] Alinhamento limpo e profissional
- [ ] Todas as setas conectam adequadamente aos alvos pretendidos

### Acessibilidade
- [ ] Paleta segura para daltonismo (Okabe-Ito) usada
- [ ] Funciona em escala de cinza (testado com verificador de acessibilidade)
- [ ] Contraste suficiente entre elementos (verificado)
- [ ] Codificação redundante quando apropriado (formas + cores)
- [ ] Simulação de daltonismo passa em todas as verificações

### Tipografia e Legibilidade
- [ ] Texto mínimo 7-8 pt no tamanho final
- [ ] Todos os elementos rotulados claramente e completamente
- [ ] Família e tamanho de fonte consistentes
- [ ] Sem sobreposição ou corte de texto
- [ ] Unidades incluídas quando aplicável

### Padrões de Publicação
- [ ] Estilo consistente com outros gráficos no manuscrito
- [ ] Legenda abrangente escrita com todas as abreviações definidas
- [ ] Referenciado apropriadamente no texto do manuscrito
- [ ] Atende aos requisitos de dimensão específicos da revista
- [ ] Exportado