---
name: ml-paper-writing
description: Escreva papers prontos para publicação em NeurIPS, ICML, ICLR, ACL, AAAI, COLM. Use quando estiver elaborando papers a partir de repositórios de pesquisa, estruturando argumentos, verificando citações ou preparando submissões finais. Inclui templates LaTeX, diretrizes de revisores e workflows de verificação de citações.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Academic Writing, NeurIPS, ICML, ICLR, ACL, AAAI, COLM, LaTeX, Paper Writing, Citations, Research]
dependencies: [semanticscholar, arxiv, habanero, requests]
---

# ML Paper Writing para Principais Conferências de IA

Orientação em nível especializado para escrever papers prontos para publicação visando **NeurIPS, ICML, ICLR, ACL, AAAI e COLM**. Esta habilidade combina filosofia de escrita de pesquisadores top (Nanda, Farquhar, Karpathy, Lipton, Steinhardt) com ferramentas práticas: templates LaTeX, APIs de verificação de citações e checklists de conferências.

## Filosofia Principal: Escrita Colaborativa

**A escrita de papers é colaborativa, mas Claude deve ser proativo na entrega de drafts.**

O workflow típico começa com um repositório de pesquisa contendo código, resultados e artefatos experimentais. O papel de Claude é:

1. **Entender o projeto** explorando o repositório, resultados e documentação existente
2. **Entregar um draft completo** quando confiante sobre a contribuição
3. **Pesquisar literatura** usando web search e APIs para encontrar citações relevantes
4. **Refinar através de ciclos de feedback** quando o cientista fornece input
5. **Fazer perguntas de esclarecimento** apenas quando genuinamente incerto sobre decisões-chave

**Princípio-Chave**: Seja proativo. Se o repositório e resultados são claros, entregue um draft completo. Não aguarde feedback sobre cada seção—cientistas são ocupados. Produza algo concreto para eles reagirem e depois itere com base na resposta.

---

## ⚠️ CRÍTICO: Nunca Alucine Citações

**Esta é a regra mais importante em escrita acadêmica com assistência de IA.**

### O Problema
Citações geradas por IA têm uma **taxa de erro de ~40%**. Referências alucinadas—papers que não existem, autores errados, anos incorretos, DOIs fabricados—são uma forma séria de má conduta acadêmica que pode resultar em desk rejection ou retração.

### A Regra
**NUNCA gere entradas BibTeX de memória. SEMPRE busque programaticamente.**

| Ação | ✅ Correto | ❌ Errado |
|------|-----------|----------|
| Adicionar uma citação | Buscar API → verificar → buscar BibTeX | Escrever BibTeX de memória |
| Incerto sobre um paper | Marcar como `[CITATION NEEDED]` | Adivinhar a referência |
| Não consegue encontrar paper exato | Notar: "placeholder - verificar" | Inventar paper similar |

### Quando Você Não Consegue Verificar uma Citação

Se você não conseguir verificar programaticamente uma citação, você DEVE:

```latex
% PLACEHOLDER EXPLÍCITO - requer verificação humana
\cite{PLACEHOLDER_author2024_verify_this}  % TODO: Verificar se esta citação existe
```

**Sempre informe ao cientista**: "Marquei [X] citações como placeholders que precisam de verificação. Não consegui confirmar que estes papers existem."

### Recomendado: Instale Exa MCP para Busca de Papers

Para a melhor experiência de busca de papers, instale **Exa MCP** que fornece busca acadêmica em tempo real:

**Claude Code:**
```bash
claude mcp add exa -- npx -y mcp-remote "https://mcp.exa.ai/mcp"
```

**Cursor / VS Code** (adicione às configurações de MCP):
```json
{
  "mcpServers": {
    "exa": {
      "type": "http",
      "url": "https://mcp.exa.ai/mcp"
    }
  }
}
```

Exa MCP permite buscas como:
- "Encontre papers sobre RLHF para language models publicados após 2023"
- "Pesquise papers de arquitetura transformer de Vaswani"
- "Obtenha trabalhos recentes sobre sparse autoencoders para interpretabilidade"

Depois verifique resultados com API do Semantic Scholar e busque BibTeX via DOI.

---

## Workflow 0: Começando por um Repositório de Pesquisa

Ao iniciar a escrita de um paper, comece entendendo o projeto:

```
Entendimento do Projeto:
- [ ] Passo 1: Explorar a estrutura do repositório
- [ ] Passo 2: Ler README, documentação existente e resultados-chave
- [ ] Passo 3: Identificar a contribuição principal com o cientista
- [ ] Passo 4: Encontrar papers já citados no codebase
- [ ] Passo 5: Pesquisar literatura adicional relevante
- [ ] Passo 6: Estruturar o paper junto com o cientista
- [ ] Passo 7: Rascunhar seções iterativamente com feedback
```

**Passo 1: Explorar o Repositório**

```bash
# Entender a estrutura do projeto
ls -la
find . -name "*.py" | head -20
find . -name "*.md" -o -name "*.txt" | xargs grep -l -i "result\|conclusion\|finding"
```

Procure por:
- `README.md` - Visão geral do projeto e afirmações
- `results/`, `outputs/`, `experiments/` - Achados-chave
- `configs/` - Configurações experimentais
- Arquivos `.bib` existentes ou referências de citação
- Qualquer documento de draft ou notas

**Passo 2: Identificar Citações Existentes**

Verifique se há papers já referenciados no codebase:

```bash
# Encontrar citações existentes
grep -r "arxiv\|doi\|cite" --include="*.md" --include="*.bib" --include="*.py"
find . -name "*.bib"
```

Estes são pontos de sinal alto para Related Work—o cientista já os considerou relevantes.

**Passo 3: Esclarecer a Contribuição**

Antes de escrever, confirme explicitamente com o cientista:

> "Com base no meu entendimento do repositório, a contribuição principal parece ser [X].
> Os resultados-chave mostram [Y]. Essa é a estrutura que você quer para o paper,
> ou deveríamos enfatizar aspectos diferentes?"

**Nunca assuma a narrativa—sempre verifique com o humano.**

**Passo 4: Pesquisar Literatura Adicional**

Use web search para encontrar papers relevantes:

```
Queries de pesquisa a tentar:
- "[técnica principal] + [domínio de aplicação]"
- "[método baseline] comparação"
- "[nome do problema] estado-da-arte"
- Nomes de autores de citações existentes
```

Depois verifique e recupere BibTeX usando o workflow de citação abaixo.

**Passo 5: Entregar um Primeiro Draft**

**Seja proativo—entregue um draft completo em vez de pedir permissão para cada seção.**

Se o repositório fornece resultados claros e a contribuição é aparente:
1. Escreva o draft completo end-to-end
2. Apresente o draft completo para feedback
3. Itere com base na resposta do cientista

Se genuinamente incerto sobre estrutura ou afirmações principais:
1. Rascunhe o que conseguir fazer com confiança
2. Sinalize incertezas específicas: "Estruturei X como a contribuição principal—me avise se preferir enfatizar Y"
3. Continue com o draft em vez de bloquear

**Perguntas a incluir com o draft** (não antes):
- "Enfatizei X como a contribuição principal—ajuste se necessário"
- "Destaquei resultados A, B, C—me avise se outros são mais importantes"
- "Seção de Related Work inclui [papers]—adicione qualquer um que perdi"

---

## Quando Usar Esta Habilidade

Use esta habilidade quando:
- **Começando por um repositório de pesquisa** para escrever um paper
- **Rascunhando ou revisando** seções específicas
- **Encontrando e verificando citações** para trabalhos relacionados
- **Formatando** para submissão em conferência
- **Resubmetendo** para um venue diferente (conversão de formato)
- **Iterando** em drafts com feedback do cientista

**Sempre lembre**: Primeiros drafts são pontos de partida para discussão, não outputs finais.

---

## Equilibrando Proatividade e Colaboração

**Padrão: Seja proativo. Entregue drafts, depois itere.**

| Nível de Confiança | Ação |
|-------------------|------|
| **Alto** (repositório claro, contribuição óbvia) | Escreva draft completo, entregue, itere no feedback |
| **Médio** (alguma ambiguidade) | Escreva draft com incertezas sinalizadas, continue |
| **Baixo** (grandes desconhecidos) | Faça 1-2 perguntas direcionadas, depois rascunhe |

**Primeiro draft, depois pergunte** (não antes):

| Seção | Rascunhe Autonomamente | Sinalize com Draft |
|-------|------------------------|-------------------|
| Abstract | Sim | "Estruturei contribuição como X—ajuste se necessário" |
| Introduction | Sim | "Enfatizei problema Y—corrija se errado" |
| Methods | Sim | "Incluí detalhes A, B, C—adicione peças faltantes" |
| Experiments | Sim | "Destaquei resultados 1, 2, 3—reordene se necessário" |
| Related Work | Sim | "Citei papers X, Y, Z—adicione qualquer um que perdi" |

**Apenas bloqueie para input quando:**
- Venue-alvo é indefinido (afeta limites de página, estrutura)
- Múltiplas estruturas igualmente válidas parecem possíveis
- Resultados parecem incompletos ou inconsistentes
- Solicitação explícita para revisar antes de continuar

**Não bloqueie para:**
- Decisões de escolha de palavras
- Ordenação de seções
- Quais resultados específicos mostrar (faça uma escolha, sinalize)
- Completude de citações (rascunhe com o que encontrar, anote gaps)

---

## O Princípio da Narrativa

**A percepção mais crítica**: Seu paper não é uma coleção de experimentos—é uma história com uma contribuição clara suportada por evidências.

Todo paper de ML bem-sucedido centra-se no que Neel Nanda chama de "narrativa": uma pequena história técnica rigorosa, baseada em evidências com uma conclusão que leitores se importam.

**Três Pilares (devem estar cristal claros no fim da introdução):**

| Pilar | Descrição | Exemplo |
|------|-----------|---------|
| **O Quê** | 1-3 afirmações novamente específicas dentro de um tema coerente | "Provamos que X alcança Y sob condição Z" |
| **O Por Quê** | Evidência empírica rigorosa suportando afirmações | Baselines fortes, experimentos distinguindo hipóteses |
| **O Então Quê** | Por que leitores devem se importar | Conexão com problemas reconhecidos da comunidade |

**Se você não conseguir descrever sua contribuição em uma frase, você ainda não tem um paper.**

---

## Paper Structure Workflow

### Workflow 1: Escrevendo um Paper Completo (Iterativo)

Copie este checklist e acompanhe o progresso. **Cada passo envolve rascunho → feedback → revisão:**

```
Progresso da Escrita do Paper:
- [ ] Passo 1: Definir a contribuição em uma frase (com o cientista)
- [ ] Passo 2: Rascunhar Figure 1 → receber feedback → revisar
- [ ] Passo 3: Rascunhar abstract → receber feedback → revisar
- [ ] Passo 4: Rascunhar introduction → receber feedback → revisar
- [ ] Passo 5: Rascunhar methods → receber feedback → revisar
- [ ] Passo 6: Rascunhar experiments → receber feedback → revisar
- [ ] Passo 7: Rascunhar related work → receber feedback → revisar
- [ ] Passo 8: Rascunhar limitations → receber feedback → revisar
- [ ] Passo 9: Checklist completo do paper (obrigatório)
- [ ] Passo 10: Ciclo de revisão final e submissão
```

**Passo 1: Definir a Contribuição em Uma Frase**

**Este passo requer confirmação explícita do cientista.**

Antes de escrever qualquer coisa, articule e verifique:
- Qual é a única coisa que seu paper contribui?
- O que não era óbvio ou presente antes do seu trabalho?

> "Proponho estruturar a contribuição como: '[uma frase]'. Isso captura
> o que você vê como a conclusão principal? Deveríamos ajustar a ênfase?"

**Passo 2: Rascunhar Figure 1**

Figure 1 merece atenção especial—muitos leitores pulam direto para ela.
- Transmitir ideia principal, abordagem ou resultado mais interessante
- Usar gráficos vetoriais (PDF/EPS para plotagens)
- Escrever captions que funcionem sozinhas sem texto principal
- Garantir legibilidade em preto e branco (8% dos homens têm deficiência de visão de cores)

**Passo 3: Escrever Abstract (Fórmula de 5 Frases)**

De Sebastian Farquhar (DeepMind):

```
1. O que você alcançou: "Introduzimos...", "Provamos...", "Demonstramos..."
2. Por que isso é difícil e importante
3. Como você faz (com palavras-chave especialistas para descoberta)
4. Que evidências você tem
5. Seu número/resultado mais notável
```

**Delete** aberturas genéricas como "Large language models alcançaram sucesso notável..."

**Passo 4: Escrever Introduction (1-1.5 páginas máx)**

Deve incluir:
- Lista de contribuição 2-4 bullets (máx 1-2 linhas cada em formato duas colunas)
- Declaração clara do problema
- Visão geral breve da abordagem
- Methods devem começar na página 2-3 no máximo

**Passo 5: Seção Methods**

Permitir reimplementação:
- Outline conceitual ou pseudocódigo
- Todos os hiperparâmetros listados
- Detalhes arquiteturais suficientes para reprodução
- Apresentar decisões de design final; ablações vão em experiments

**Passo 6: Seção Experiments**

Para cada experimento, descreva explicitamente:
- Qual afirmação ele suporta
- Como se conecta à contribuição principal
- Configuração experimental (detalhes em appendix)
- O que observar: "a linha azul mostra X, o que demonstra Y"

Requisitos:
- Barras de erro com metodologia (desvio padrão vs erro padrão)
- Ranges de busca de hiperparâmetros
- Infraestrutura de computação (tipo GPU, horas totais)
- Métodos de configuração de seed

**Passo 7: Related Work**

Organize metodologicamente, não paper-por-paper:

**Bom:** "Uma linha de trabalho usa o pressuposto de Floogledoodle [refs] enquanto usamos o pressuposto de Doobersnoddle porque..."

**Ruim:** "Snap et al. introduziram X enquanto Crackle et al. introduziram Y."

Cite generosamente—reviewers provavelmente autorizaram papers relevantes.

**Passo 8: Seção Limitations (OBRIGATÓRIA)**

Todas as principais conferências exigem isso. Contra-intuitivamente, honestidade ajuda:
- Reviewers são instruídos a não penalizar reconhecimento honesto de limitações
- Pré-empa críticas identificando fraquezas primeiro
- Explique por que limitações não enfraquecem afirmações principais

**Passo 9: Checklist do Paper**

NeurIPS, ICML e ICLR todos exigem paper checklists. Ver [references/checklists.md](references/checklists.md).

---

## Filosofia de Escrita para Principais Conferências de ML

**Esta seção destila os princípios de escrita mais importantes de pesquisadores de ML líderes.** Estas não são sugestões opcionais de estilo—são o que separa papers aceitos de rejeitados.

> "Um paper é uma pequena, rigorosa, baseada em evidências história técnica com uma conclusão que leitores se importam." — Neel Nanda

### As Fontes por Trás desta Orientação

Esta habilidade sintetiza filosofia de escrita de pesquisadores que publicaram extensivamente em venues top:

| Fonte | Contribuição-Chave | Link |
|-------|-------------------|------|
| **Neel Nanda** (Google DeepMind) | O Princípio da Narrativa, framework What/Why/So What | [How to Write ML Papers](https://www.alignmentforum.org/posts/eJGptPbbFPZGLpjsp/highly-opinionated-advice-on-how-to-write-ml-papers) |
| **Sebastian Farquhar** (DeepMind) | Fórmula de abstract de 5 frases | [How to Write ML Papers](https://sebastianfarquhar.com/on-research/2024/11/04/how_to_write_ml_papers/) |
| **Gopen & Swan** | 7 princípios de expectativas do leitor | [Science of Scientific Writing](https://cseweb.ucsd.edu/~swanson/papers/science-of-writing.pdf) |
| **Zachary Lipton** | Escolha de palavras, eliminando hedge | [Heuristics for Scientific Writing](https://www.approximatelycorrect.com/2018/01/29/heuristics-technical-scientific-writing-machine-learning-perspective/) |
| **Jacob Steinhardt** (UC Berkeley) | Precisão, terminologia consistente | [Writing Tips](https://bounded-regret.ghost.io/) |
| **Ethan Perez** (Anthropic) | Dicas de clareza em nível micro | [Easy Paper Writing Tips](https://ethanperez.net/easy-paper-writing-tips/) |
| **Andrej Karpathy** | Foco em contribuição única | Várias palestras |

**Para mergulhos mais profundos em qualquer uma destas, ver:**
- [references/writing-guide.md](references/writing-guide.md) - Explicações completas com exemplos
- [references/sources.md](references/sources.md) - Bibliografia completa

### Alocação de Tempo (De Neel Nanda)

Passe aproximadamente **tempo igual** em cada um de:
1. O abstract
2. A introduction
3. As figuras
4. Todo o resto combinado

**Por quê?** A maioria dos reviewers forma julgamentos antes de ler seus methods. Leitores encontram seu paper como: **título → abstract → introduction → figuras → talvez o resto.**

### Diretrizes de Estilo de Escrita

#### Clareza em Nível de Sentença (7 Princípios de Gopen & Swan)

Estes princípios baseiam-se em como leitores realmente processam prosa. Violá-los força leitores a gastar esforço cognitivo em estrutura ao invés de conteúdo.

| Princípio | Regra | Exemplo |
|-----------|------|---------|
| **Proximidade sujeito-verbo** | Mantenha sujeito e verbo próximos | ❌ "O modelo, que foi treinado em..., alcança" → ✅ "O modelo alcança... após treinamento em..." |
| **Stress position** | Coloque ênfase no fim de sentença | ❌ "A acurácia melhora 15% ao usar atenção" → ✅ "Ao usar atenção, a acurácia melhora **15%**" |
| **Topic position** | Coloque contexto primeiro, info nova depois | ✅ "Dadas essas restrições, propomos..." |
| **Velho antes de novo** | Info familiar → info desconhecida | Vincule para trás, depois introduza o novo |
| **Uma unidade, uma função** | Cada parágrafo faz um ponto | Divida parágrafos multi-ponto |
| **Ação no verbo** | Use verbos, não nominalizações | ❌ "Realizamos uma análise" → ✅ "Analisamos" |
| **Contexto antes de novo** | Defina contexto antes de apresentar | Explique antes de mostrar equação |

**7 princípios completos com exemplos detalhados:** Ver [references/writing-guide.md](references/writing-guide.md#the-7-principles-of-reader-expectations)

#### Dicas em Nível Micro (Ethan Perez)

Estas pequenas mudanças acumulam em prosa significativamente mais clara:

- **Minimize pronomes**: ❌ "Isso mostra..." → ✅ "Este resultado mostra..."
- **Verbos cedo**: Posicione verbos perto do início da sentença
- **Desdobrar apóstrofos**: ❌ "Y de X" → ✅ "O Y de X" (quando estranho)
- **Delete palavras de enchimento**: "realmente," "um pouco," "muito," "bastante," "basicamente," "quase," "essencialmente"

**Dicas micro-completas com exemplos:** Ver [references/writing-guide.md](references/writing-guide.md#micro-level-writing-tips)

#### Escolha de Palavras (Zachary Lipton)

- **Seja específico**: ❌ "performance" → ✅ "acurácia" ou "latência" (diga o que você quer dizer)
- **Elimine hedge**: Remova "pode" e "consegue" a menos que genuinamente incerto
- **Evite vocabulário incremental**: ❌ "combinar," "modificar," "expandir" → ✅ "desenvolver," "propor," "introduzir"
- **Delete intensificadores**: ❌ "fornece *muito* aproximação apertada" → ✅ "fornece aproximação apertada"

#### Precisão Sobre Brevidade (Jacob Steinhardt)

- **Terminologia consistente**: Diferentes termos para mesmo conceito criam confusão. Escolha um e mantenha.
- **Declare assunções formalmente**: Antes de teoremas, liste todas as assunções explicitamente
- **Intuição + rigor**: Forneça explicações intuitivas junto com provas formais

### O Que Reviewers Realmente Leem

Entender comportamento de reviewer ajuda a priorizar seu esforço:

| Seção do Paper | % Reviewers que Leem | Implicação |
|----------------|---------------------|------------|
| Abstract | 100% | Deve ser perfeito |
| Introduction | 90%+ (skimmed) | Coloque contribuição na frente |
| Figures | Examinadas antes dos methods | Figure 1 é crítica |
| Methods | Apenas se interessado | Não esconda o ouro |
| Appendix | Raramente | Coloque apenas detalhes suplementares |

**Bottom line**: Se seu abstract e intro não engancharem reviewers, eles podem nunca ler sua brilhante seção de methods.

---

## Referência Rápida de Requisitos de Conferência

| Conferência | Limite de Página | Extra para Camera-Ready | Requisito-Chave |
|-------------|-----------------|------------------------|-----------------|
| **NeurIPS 2025** | 9 páginas | +0 | Checklist obrigatório, lay summary para aceitos |
| **ICML 2026** | 8 páginas | +1 | Broader Impact Statement obrigatório |
| **ICLR 2026** | 9 páginas | +1 | Divulgação de LLM obrigatória, reviewing recíproco |
| **ACL 2025** | 8 páginas (long) | varia | Seção Limitations obrigatória |
| **AAAI 2026** | 7 páginas | +1 | Aderência estrita ao arquivo de estilo |
| **COLM 2025** | 9 páginas | +1 | Foco em language models |

**Requisitos Universais:**
- Blind review dupla (anonimizar submissões)
- Referências não contam para limite de página
- Apêndices ilimitados mas reviewers não são obrigados a ler
- LaTeX obrigatório para todos os venues

**Templates LaTeX:** Ver diretório [templates/](templates/) para todos os templates de conferência.

---

## Usando Templates LaTeX Corretamente

### Workflow 4: Começando um Novo Paper de Template

**Sempre copie todo o diretório de template primeiro, depois escreva nele.**

```
Checklist de Setup do Template:
- [ ] Passo 1: Copiar todo o diretório de template para novo projeto
- [ ] Passo 2: Verificar que template compila como-está (antes de mudanças)
- [ ] Passo 3: Ler conteúdo de exemplo do template para entender estrutura
- [ ] Passo 4: Substituir conteúdo de exemplo seção por seção
- [ ] Passo 5: Manter comentários/exemplos do template como referência até terminar
- [ ] Passo 6: Limpar artefatos de template apenas no final
```

**Passo 1: Copiar o Template Completo**

```bash
# Criar diretório de seu paper com o template completo
cp -r templates/neurips2025/ ~/papers/meu-novo-paper/
cd ~/papers/meu-novo-paper/

# Verificar que a estrutura está completa
ls -la
# Deve ver: main.tex, neurips.sty, Makefile, etc.
```

**⚠️ IMPORTANTE**: Copie o DIRETÓRIO INTEIRO, não apenas `main.tex`. Templates incluem:
- Arquivos de estilo (`.sty`) - necessários para compilação
- Estilos de bibliografia (`.bst`) - necessários para referências
- Conteúdo de exemplo - útil como referência
- Makefiles - para compilação fácil

**Passo 2: Verificar que Template Compila Primeiro**

Antes de FAZER QUALQUER MUDANÇA, compile o template como-está:

```bash
# Usando latexmk (recomendado)
latexmk -pdf main.tex

# Ou compilação manual
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Se o template não modificado não compilar, conserte isso primeiro. Problemas comuns:
- Pacotes TeX faltantes → instale via `tlmgr install <package>`
- Distribuição TeX errada → use TeX Live (recomendado)

**Passo 3: Manter Conteúdo de Template como Referência**

Não delete imediatamente todo conteúdo de exemplo. Em vez disso:

```latex
% MANTER exemplos de template comentados enquanto escreve
% Isso mostra o formato esperado

% Exemplo de template (manter para referência):
% \begin{figure}[t]
%   \centering
%   \includegraphics[width=0.8\linewidth]{example-image}
%   \caption{Template mostra estilo de caption}
% \end{figure}

% Sua figura real:
\begin{figure}[t]
  \centering
%   \includegraphics[width=0.8\linewidth]{sua-figura.pdf}
  \caption{Sua caption seguindo o mesmo estilo.}
\end{figure}
```

**Passo 4: Substituir Conteúdo Seção por Seção**

Trabalhe pelo paper sistematicamente:

```
Ordem de Substituição:
1. Título e autores (anonimizar para submissão)
2. Abstract
3. Introduction
4. Methods
5. Experiments
6. Related Work
7. Conclusion
8. References (seu arquivo .bib)
9. Appendix
```

Para cada seção:
1. Leia o conteúdo de exemplo do template
2. Note qualquer formatação especial ou macros usados
3. Substitua pelo seu conteúdo seguindo os mesmos padrões
4. Compile frequentemente para pegar erros cedo

**Passo 5: Use Macros do Template**

Templates frequentemente definem macros úteis. Verifique o preamble para:

```latex
% Macros comuns de template para usar:
\newcommand{\method}{SeuNomeDoMetodo}  % Nomenclatura consistente de método
\newcommand{\eg}{e.g.,\xspace}        % Abreviações próprias
\newcommand{\ie}{i.e.,\xspace}
\newcommand{\etal}{\textit{et al.}\xspace}
```

**Passo 6: Limpar Apenas no Final**

Remova artefatos de template apenas quando o paper estiver quase completo:

```latex
% ANTES DE SUBMETER - remova estes:
% - Exemplos de template comentados
% - Pacotes não usados
% - Figuras/tabelas de exemplo do template
% - Texto Lorem ipsum ou placeholder

% MANTENHA estes:
%