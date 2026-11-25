---
name: excalidraw
description: "Use when working with *.excalidraw or *.excalidraw.json files, user mentions diagrams/flowcharts, or requests architecture visualization - delegates all Excalidraw operations to subagents to prevent context exhaustion from verbose JSON (single files: 4k-22k tokens, can exceed read limits)"
---

# Delegação para Subagente Excalidraw

## Visão Geral

**Princípio fundamental:** Agentes principais NUNCA leem arquivos Excalidraw diretamente. Sempre delegue a subagentes para isolar o consumo de contexto.

Arquivos Excalidraw são JSON com alto custo de token, mas baixa densidade de informação. Arquivos individuais variam de 4k-22k tokens (maiores podem exceder limites de leitura). Ler múltiplos diagramas rapidamente esgota o orçamento de contexto (7 arquivos = 67k tokens = 33% do orçamento).

## O Problema

Estrutura JSON do Excalidraw:
- Cada forma tem 20+ propriedades (x, y, width, height, strokeColor, seed, version, etc.)
- A maioria das propriedades é metadados visuais (posicionamento, estilo, roughness)
- Conteúdo real: rótulos de texto e relacionamentos entre elementos (<10% do arquivo)
- **Taxa sinal-ruído é extremamente baixa**

Exemplo: diagrama com 14 elementos = 596 linhas, 16K, ~4k tokens. Diagrama com 79 elementos = 2.916 linhas, 88K, ~22k tokens (excede limite de leitura).

## Quando Usar

**Gatilho em QUALQUER um destes:**
- Caminho do arquivo contém `.excalidraw` ou `.excalidraw.json`
- Usuário solicita: "explicar/atualizar/criar diagrama", "mostrar arquitetura", "visualizar fluxo"
- Usuário menciona: "flowchart", "diagrama de arquitetura", "arquivo Excalidraw"
- Tarefas de documentação de arquitetura/design envolvendo artefatos visuais

**Use delegação mesmo para:**
- Arquivos "pequenos" (o menor é 4k tokens - ainda significativo)
- "Verificações rápidas" (verificar nomes de componentes ainda carrega JSON completo)
- Operações de arquivo único (isolamento evita poluição de contexto)
- Modificações (não precisa de compreensão completa de formato no contexto principal)

## Padrão de Delegação

### Responsabilidades do Agente Principal

**NUNCA:**
- ❌ Use a ferramenta Read em arquivos *.excalidraw
- ❌ Analise JSON do Excalidraw no contexto principal
- ❌ Carregue múltiplos diagramas para comparação
- ❌ Inspecione arquivo para "entender o formato"

**SEMPRE:**
- ✅ Delegue TODAS as operações Excalidraw a subagentes
- ✅ Forneça descrição clara de tarefa ao subagente
- ✅ Solicite resumos em texto (não JSON bruto)
- ✅ Mantenha análise de diagrama isolada do trabalho principal

### Modelos de Tarefa para Subagente

#### Operação de Leitura/Compreensão
```
Tarefa: Extrair e explicar componentes em [file.excalidraw.json]

Abordagem:
1. Ler o JSON do Excalidraw
2. Extrair apenas elementos de texto (ignorar posicionamento/estilo)
3. Identificar relacionamentos entre componentes
4. Resumir arquitetura/fluxo

Retornar:
- Lista de componentes/serviços com descrições
- Relacionamentos e dependências entre conexões
- Insights principais sobre a arquitetura
- NÃO retornar JSON bruto ou detalhes verbosos de elementos
```

#### Operação de Modificação
```
Tarefa: Adicionar [componente] a [file.excalidraw.json], conectado a [componente-existente]

Abordagem:
1. Ler arquivo para identificar elementos existentes
2. Encontrar [componente-existente] e sua posição
3. Criar JSON de novo elemento para [componente]
4. Adicionar elementos de seta para conexões
5. Escrever arquivo atualizado

Retornar:
- Confirmação das mudanças feitas
- Posição do novo elemento
- IDs de elementos criados
```

#### Operação de Criação
```
Tarefa: Criar novo diagrama Excalidraw mostrando [descrição]

Abordagem:
1. Desenhar layout para [número] de componentes
2. Criar elementos retângulo com rótulos de texto
3. Adicionar setas mostrando relacionamentos
4. Usar estilo consistente (cores, fontes)
5. Escrever para [file.excalidraw.json]

Retornar:
- Confirmação do arquivo criado
- Resumo de componentes inclusos
- Localização do arquivo
```

#### Operação de Comparação
```
Tarefa: Comparar abordagens de arquitetura em [file1] vs [file2]

Abordagem:
1. Ler ambos os arquivos
2. Extrair rótulos de texto de cada um
3. Identificar diferenças estruturais
4. Comparar relacionamentos e fluxos de componentes

Retornar:
- Diferenças principais na arquitetura
- Componentes únicos para cada abordagem
- Diferenças de relacionamento/fluxo
- NÃO retornar detalhes completos de elementos de ambos os arquivos
```

## Racionalizações Comuns (PARE e Delegue em Vez disso)

| Desculpa | Realidade | O Que Fazer |
|----------|-----------|------------|
| "Leitura direta é mais eficiente" | Consome 4k-22k tokens desnecessariamente | Delegue ao subagente |
| "É eficiente em termos de token ler diretamente" | Testes de linha de base mostraram uso de 9-45% do orçamento | Sempre delegue |
| "Isso é ótimo para análise única" | "Uma vez" ainda polui contexto principal | Isolamento de subagente |
| "O JSON é direto" | Simplicidade ≠ eficiência de token | Delegue de qualquer forma |
| "Preciso entender o formato" | Compreensão de formato não é necessária no agente principal | Subagente trata do formato |
| "Dentro de limites razoáveis" (18k tokens) | "Razoável" é racionalização subjetiva | Regra rígida: delegue |
| "Apenas uma verificação rápida de componentes" | "Verificação rápida" ainda carrega JSON completo | Extraia texto via subagente |
| "Arquivo é pequeno (16K)" | 4k tokens NÃO é pequeno | Tamanho não importa |

## Bandeiras Vermelhas - PARE e Delegue

Pegue a si mesmo prestes a:
- Usar a ferramenta Read em arquivo .excalidraw
- "Verificação rápida" de quais componentes existem
- "Entender a estrutura" antes de modificar
- Carregar arquivo para "ver o que há"
- Comparar múltiplos diagramas lado a lado
- Analisar JSON para "extrair apenas o texto"

**Todos esses significam: Use a ferramenta Task com subagente em vez disso.**

## Referência Rápida

| Operação | Ação do Agente Principal | Subagente Retorna |
|----------|-------------------------|------------------|
| **Entender diagrama** | Delegue com modelo "Extrair e explicar" | Lista de componentes + relacionamentos |
| **Modificar diagrama** | Delegue com modelo "Adicionar [X] conectado a [Y]" | Confirmação + mudanças feitas |
| **Criar diagrama** | Delegue com modelo "Criar mostrando [descrição]" | Localização do arquivo + resumo |
| **Comparar diagramas** | Delegue com modelo "Comparar [A] vs [B]" | Diferenças principais (não JSON bruto) |

## Análise de Token (Por Que Isso Importa)

Dados reais de testes de linha de base:

| Cenário | Sem Delegação | Com Delegação | Economia |
|---------|---------------|---------------|----------|
| Arquivo único grande | 22k tokens (45% do orçamento) | ~500 tokens (resumo subagente) | 98% |
| Comparação de dois arquivos | 18k tokens (9% do orçamento) | ~800 tokens (resumo diff) | 96% |
| Tarefa de modificação | 14k tokens (7% do orçamento) | ~300 tokens (confirmação) | 98% |

**Impacto de poluição de contexto:**
- Ler todos os 7 diagramas de projeto: 67k tokens (33% do orçamento de 200k)
- Com delegação: ~2k tokens (isolados em subagentes)
- **Economia: 97% de orçamento de contexto preservado**

## Exemplo de Implementação

**❌ RUIM (Leitura Direta):**
```
Usuário: "Qual arquitetura é mostrada em detailed-architecture.excalidraw.json?"
Agente: Deixe-me ler esse arquivo... [lê 22k tokens no contexto principal]
```

**✅ BOM (Delegação para Subagente):**
```
Usuário: "Qual arquitetura é mostrada em detailed-architecture.excalidraw.json?"
Agente: Vou usar um subagente para extrair os detalhes da arquitetura.

[Despacha ferramenta Task com subagente de propósito geral]
Tarefa: Extrair e explicar componentes em .ryanquinn3/ticketing/detailed-architecture.excalidraw.json

[Recebe resumo de ~500 tokens com lista de componentes e relacionamentos]
[Responde ao usuário com explicação de arquitetura, contexto principal preservado]
```

## Por Que "JSON Direto" Não Importa

Agentes frequentemente racionalizam: "O formato é simples, posso apenas ler."

**O problema não é complexidade - é verbosidade:**
- Estrutura simples com 20+ propriedades por elemento
- Metadados repetitivos (seed, version, nonce, roughness)
- Dados de posicionamento (x, y, width, height) não úteis semanticamente
- Estilo visual (strokeColor, opacity, fillStyle) irrelevante para conteúdo

**Custo de token vem do volume, não da complexidade.**

Mesmo JSON "direto" consome 4k-22k tokens porque:
- 79 elementos × ~280 tokens/elemento = 22k tokens
- A maioria dos tokens é ruído de metadados
- Apenas rótulos de texto e relacionamentos importam (~10% do conteúdo)

## A Lei de Ferro

**Agentes principais NUNCA leem arquivos Excalidraw. Sem exceções.**

Não para:
- "Verificações rápidas"
- "Arquivos pequenos"
- "Compreensão de formato"
- "Análise única"
- "Eficiência ótima"

**Sempre delegue. Isolamento é gratuito via subagentes.**