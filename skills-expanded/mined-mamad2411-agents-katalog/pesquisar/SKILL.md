---
name: pesquisar
description: Pesquisa informações na web sobre um tema ou tarefa do vault e cria nota de pesquisa em 05_Research/. Ativar quando Luiz disser "/pesquisar TEMA", "/pesquisar T-XXX-NNN", "pesquise sobre X", "busca na web X" ou "adiciona pesquisa sobre X ao vault".
---

# Skill: pesquisar

Pesquisa um tema na web, sintetiza os resultados e cria nota estruturada em `05_Research/`.

Aceita dois modos:
- **Tópico livre:** `/pesquisar contratos de compra e venda`
- **Tarefa do vault:** `/pesquisar T-JUR-001` — extrai o tema da tarefa e pesquisa o conteúdo necessário

---

## Fase 0 — Clarificação e Vault Pre-check

### Passo 0a — Clarificar contexto (se ambíguo)

Se o tema for amplo, genérico ou sem contexto de uso claro, perguntar **antes** de qualquer busca:

```
"Para qual contexto é esta pesquisa?"
  a) Estágio jurídico
  b) Faculdade (matéria: ___)
  c) Kermartin / CRM
  d) Aprimorador / IA
  e) Geral
```

Se o contexto estiver claro na mensagem ou no ID da tarefa, pular.

### Passo 0b — Verificar vault antes de buscar web

Antes de qualquer WebSearch, buscar palavras-chave do tema em:
- `02_Knowledge/**/*.md`
- `05_Research/**/*.md`
- `10_Learning/**/*.md`

**Se encontrar 1+ notas relevantes:**

```
─────────────────────────────────────────
Encontrei no vault:
  • [[nota-1]] — [1 linha de contexto]
  • [[nota-2]] — [1 linha de contexto]

Como quer prosseguir?
  a) Aprofundar uma destas notas (sem busca web)
  b) Buscar na web mesmo assim para complementar
  c) Cancelar — as notas já cobrem o tema
─────────────────────────────────────────
```

**Se não encontrar nada relacionado:** ir direto ao Passo 1 (busca web) sem perguntar.

---

## Passo 1 — Identificar tema

### Se o argumento for um ID de tarefa (padrão `T-XXX-NNN`):

1. Identificar a equipe pelo prefixo:
   - `T-JUR` → `99_System/equipes/juridica-tarefas.md`
   - `T-COM` → `99_System/equipes/comercial-tarefas.md`
   - `T-DEV` → `99_System/equipes/dev-tarefas.md`
   - `T-PES` → `99_System/equipes/pesquisa-tarefas.md`
   - `T-PSS` → `99_System/equipes/pessoal-tarefas.md`

2. Ler o arquivo da equipe e localizar o bloco da tarefa pelo ID
3. Extrair: título, descrição, critérios de aceitação e notas base
4. Derivar o tema de pesquisa a partir do título + descrição

### Se o argumento for texto livre:
- Usar o texto diretamente como tema de pesquisa

---

## Passo 2 — Pesquisar na web

### Passo 2a — WebSearch (descoberta de URLs)

Executar **3 a 5 buscas** cobrindo ângulos diferentes do tema:

#### Para temas jurídicos (palavras-chave: direito, lei, artigo, CPC, CDC, etc.):
- Busca 1: conceito e definição jurídica
- Busca 2: legislação aplicável (artigos de lei específicos)
- Busca 3: jurisprudência relevante (STJ, STF, tribunais estaduais)
- Busca 4: doutrina / comentários de especialistas
- Busca 5: aplicação prática / exemplos

#### Para temas de tecnologia/programação (palavras-chave: C#, Unity, Python, API, etc.):
- Busca 1: documentação oficial
- Busca 2: tutorial prático / exemplo de código
- Busca 3: casos de uso comuns e boas práticas
- Busca 4: problemas frequentes e soluções (Stack Overflow / GitHub)

#### Para temas de UI/UX/design visual (palavras-chave: UI, UX, design, dashboard, landing, wireframe, sitemap, template, Figma, Moqups):
- Busca 1: fonte oficial ou galeria/template original
- Busca 2: exemplos visuais e assets publicos
- Busca 3: boas praticas do tipo de tela
- Busca 4: acessibilidade/responsividade/performance
- Acionar `/visual-intelligence`: extrair `Estrutura + Visual detalhado + Localizacao`
- Se necessario, salvar imagens publicas ou screenshots para leitura visual

#### Para temas de negócios/comercial (palavras-chave: CRM, funil, vendas, SaaS, etc.):
- Busca 1: conceito e frameworks do mercado
- Busca 2: exemplos práticos e cases
- Busca 3: ferramentas e métricas relevantes

#### Para temas gerais:
- Busca 1: visão geral / introdução ao tema
- Busca 2: aspectos técnicos ou aprofundados
- Busca 3: aplicações práticas ou exemplos reais

Após as buscas, identificar as **2–3 URLs mais relevantes** para aprofundamento.

---

### Passo 2b — Apify Deep Fetch (conteúdo completo)

Usar o Actor `apify/rag-web-browser` via MCP para buscar o conteúdo completo das URLs selecionadas no Passo 2a.

**Quando usar Apify:**
- Documentação oficial (docs.*, developer.*, etc.)
- Artigos técnicos ou jurídicos com conteúdo substancial
- Páginas que WebSearch retornou truncadas ou sem detalhes suficientes

**Quando NÃO usar Apify (economizar créditos):**
- Páginas simples já cobertas pelo snippet do WebSearch
- Sites de notícias com conteúdo superficial
- URLs que já forneceram informação suficiente nos resultados do Passo 2a

**Limite:** máximo **3 URLs por pesquisa** para conservar créditos do free tier ($5/mês).

**Fallback:** se Apify não estiver conectado (MCP offline), pular este passo e sintetizar apenas com resultados do WebSearch — registrar no resumo final como "Apify: não utilizado".

---

## Passo 3 — Sintetizar

Consolidar os resultados em uma síntese estruturada:

- Eliminar informações redundantes entre as fontes
- Priorizar fontes primárias (legislação, documentação oficial) sobre secundárias
- Destacar divergências ou controvérsias encontradas
- Incluir citações diretas apenas quando o texto exato for relevante
- Anotar lacunas: o que não foi encontrado / precisa de aprofundamento

Se a pesquisa for visual/UI/UX, incluir obrigatoriamente:
- estrutura da tela;
- camada visual detalhada;
- mapa de localizacao dos elementos;
- logica visual;
- padroes reutilizaveis;
- quando usar/evitar.

---

## Passo 4 — Criar nota em 05_Research/

### Nome do arquivo
- Formato: `kebab-case-sem-acentos.md`
- Exemplos: `titulos-de-credito-resumo.md`, `unity-collider-trigger.md`, `funil-vendas-saas.md`
- Se vier de tarefa: prefixar com ID — `t-jur-001-titulos-de-credito.md`

### Frontmatter

```yaml
---
data: YYYY-MM-DD
área: direito | programação | comercial | pessoal | geral
tema: [tema principal, subtemas]
fonte: [URLs das principais fontes consultadas]
método: websearch+apify | websearch  (websearch+apify se Apify foi usado)
status: rascunho
tags: [tag1, tag2]
tarefa: T-XXX-NNN  (se veio de tarefa — omitir se tópico livre)
---
```

### Estrutura da nota

```markdown
# [Título do Tema]

> Pesquisa realizada em DD/MM/YYYY. Status: rascunho — revisar antes de usar.

## Resumo
[2-4 frases: o essencial do tema]

## Conceito / Definição
[O que é, origem, definição formal]

## Aspectos Principais
[Tópicos mais relevantes encontrados — usar subtítulos H3 se necessário]

## Aplicação Prática
[Como isso se aplica ao contexto do Luiz — estágio, vault, projeto Kermartin, etc.]

## Legislação / Documentação Relevante
[Leis, artigos, docs oficiais, links]

## Referências
- [Fonte 1](URL)
- [Fonte 2](URL)
- [Fonte 3](URL)

## Lacunas / Aprofundar
- [ ] ponto que ficou incompleto
- [ ] ponto que precisa de verificação

## Relacionado
[[link-para-nota-relevante-no-vault]]
```

> Omitir seções que não se aplicam ao tema (ex: "Legislação" para temas de programação).

---

## Passo 5 — Atualizar vault

### Se veio de tarefa:
1. Adicionar link da nota criada no bloco da tarefa em `99_System/equipes/XXX-tarefas.md`, na seção `#### 🔗 Dependências > Notas base:`
2. Adicionar log no bloco da tarefa: `| YYYY-MM-DD | pesquisador | Nota de pesquisa criada: [[05_Research/nome-da-nota]] |`

### Sempre:
1. Adicionar link da nota em `14_Indexes/MAPA.md` na seção correspondente à área
2. Se a área tiver MOC (`14_Indexes/moc-{área}.md`): adicionar link na seção correta do MOC

---

## Passo 6 — Confirmar ao Luiz

Exibir resumo:

```
✅ PESQUISA CONCLUÍDA
─────────────────────────────────────────
Tema:     [tema pesquisado]
Nota:     05_Research/[nome-do-arquivo].md
Buscas:   X realizadas
Apify:    X páginas extraídas (ou "não utilizado")
Fontes:   X fontes consultadas
Tarefa:   T-XXX-NNN atualizada (se aplicável)
MAPA:     link adicionado

📋 Lacunas encontradas:
  - [item que ficou incompleto]
─────────────────────────────────────────
Quer que eu aprofunde algum ponto?
```

---

## Referências Vault (sugerir ao completar)

Ao confirmar a pesquisa concluída, sugerir:
- Notas encontradas no Passo 0b que ainda não foram linkadas na nota criada
- MOC da área na nota criada: se tema = direito → `[[14_Indexes/moc-direito]]`; dev → `[[14_Indexes/IDX-dev]]`
- Tarefas relacionadas ao tema (se ID de tarefa foi fornecido, já está no bloco da tarefa)

## Restrições

- **Mínimo 3 buscas WebSearch** por tema — nunca criar nota com fonte única
- **Máximo 3 URLs Apify** por pesquisa — conservar créditos do free tier
- **Nunca inventar** informações jurídicas — se não encontrar lei/artigo, registrar como lacuna
- **Sempre incluir URLs** das fontes na nota criada
- **Nunca sobrescrever** nota existente com mesmo nome — sufixar com `-v2` se houver conflito
- Se Luiz não especificar ID de tarefa mas o tema claramente corresponder a uma tarefa ativa, mencionar a tarefa relacionada na confirmação final
- Apify é complementar, não substituto — WebSearch sempre primeiro para descoberta
