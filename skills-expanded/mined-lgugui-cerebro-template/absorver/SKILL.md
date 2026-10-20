---
name: absorver
description: >
  Recebe URLs, textos, dados brutos ou qualquer referência externa e converte em
  conhecimento estruturado no vault — extrai o essencial, descarta ruído, salva na
  pasta correta, commita. Ativar com /absorver seguido de URLs ou conteúdo.
---

# Skill: absorver

Transforma qualquer entrada externa (URL, texto, código, repo GitHub, artigo) em nota de conhecimento reutilizável no vault. Remove ruído, extrai substância, classifica, salva, commita.

---

## Gatilhos

- `/absorver URL1 URL2 ...`
- `/absorver [texto ou dados colados]`
- Usuário cola URLs sem comando → oferecer absorver
- Usuário diz "salva isso", "aprende com isso", "guarda essa referência"

---

## Fase 1 — Receber e classificar entradas

### 1.1 Identificar tipo de cada entrada

| Tipo de entrada | Como processar |
|---|---|
| URL de site / blog / doc | `WebFetch` com prompt de extração |
| URL do GitHub (repo) | `WebFetch` → extrair: o que é, stack, capacidades, como usar, casos de uso |
| URL do GitHub (arquivo específico) | `WebFetch` → extrair código e explicação |
| Texto colado | Processar diretamente sem fetch |
| PDF / DOCX | Usar skill `/pdf` ou `/docx` para extrair texto |
| Código bruto | Documentar: linguagem, o que faz, quando usar |
| Site/template/screenshot/UI visual | **Chamar `/visual-intelligence` automaticamente** — extrair Estrutura + Visual detalhado + Localização + Guia de Replicação + Aprimoramentos; salvar assets quando necessário |
| Código front-end (CSS, Tailwind, tokens, componente React/Vue, script Figma) | **Chamar `/visual-intelligence` automaticamente** — ler arquivo, extrair paleta/tipografia/espaçamento/componentes, gerar guia de replicação |

### 1.2 Processar múltiplas entradas em paralelo

Se o usuário enviou múltiplas URLs/dados, fazer o fetch de **todas em paralelo** (um `WebFetch` por entrada no mesmo turno), não sequencialmente.

---

## Fase 2 — Extração de conhecimento (prompt padrão)

Para cada entrada, usar este prompt de extração ao chamar `WebFetch`:

```
Extraia SOMENTE o conhecimento técnico e prático útil. Descarte:
- Navegação, menus, rodapés, banners
- CTAs comerciais e propaganda
- Conteúdo repetitivo ou óbvio
- Metadados irrelevantes

Extraia e estruture:
1. O QUE É — definição em 1-2 frases
2. COMO FUNCIONA — mecanismo interno se técnico
3. CAPACIDADES — lista do que pode fazer
4. COMO USAR — código ou passos práticos
5. QUANDO USAR — casos de uso concretos, momento certo
6. QUANDO NÃO USAR — limitações e alternativas
7. REQUISITOS — dependências, pré-requisitos
8. BOAS PRÁTICAS — dicas não óbvias
```

Adaptar o prompt conforme o tipo:
- **Blog / artigo:** focar em princípios, dicas, frameworks
- **GitHub repo:** focar em capacidades técnicas, instalação, exemplos de código
- **Documentação oficial:** focar em API, configuração, exemplos
- **Ferramenta / biblioteca:** focar em quando usar, integração, alternativas
- **UI/UX / site / template / screenshot:** usar regra obrigatoria `Estrutura + Visual detalhado + Localizacao`; capturar assets ou screenshots se o visual nao estiver suficientemente descrito por texto

---

## Fase 3 — Classificar destino no vault

### Regra de pasta

| Conteúdo | Pasta | Tipo nota |
|---|---|---|
| Conhecimento permanente, princípios, frameworks reutilizáveis | `02_Knowledge/` | `conceito` ou `procedimento` |
| Ferramenta / biblioteca / API externa | `05_Research/` | `recurso` |
| Padrao visual, UI/UX, wireframe, sitemap, dashboard | `10_Learning/Desenvolvimento/UI-UX/` | `procedimento` ou `referencia` |
| Empresa, produto, pessoa recorrente | `03_Entities/` | `recurso` |
| Exploração inicial, não consolidado | `05_Research/` | `recurso` |
| Processo ou decisão de projeto ativo | `04_Projects/[projeto]/` | `procedimento` |

### Regra de domínio

Inferir pelo conteúdo:
- Go, Python, JavaScript, Unity, C# → `dev`
- Design, Figma, UI/UX, wireframe → `dev`
- Vendas, CRM, leads, prospecção → `comercial`
- Direito, contratos, jurídico → `direito`
- Outro → `geral`

### Regra de nome de arquivo

```
kebab-case sem acentos sem espaços
Ex: globe-visualizacao-geografica.md
Ex: principios-typography-web.md
Ex: stripe-api-pagamentos.md
```

---

## Fase 4 — Verificar se nota já existe

Antes de criar:
1. `Grep` pelo nome do tema em `02_Knowledge/`, `05_Research/`, `03_Entities/`
2. Se existe nota similar → **atualizar** com nova seção, não criar duplicata
3. Se não existe → criar nova nota

---

## Fase 5 — Criar / atualizar nota

### Frontmatter obrigatório

```yaml
---
data: YYYY-MM-DD
tipo: referencia
dominio: dev | comercial | direito | pessoal | geral
tipo_nota: conceito | procedimento | recurso | caso
nivel: básico | intermediário | avançado
status_nota: ativo
tags: [tag1, tag2, tag3]
---
```

### Estrutura padrão da nota

```markdown
# [Nome da Ferramenta / Conceito]

**Fonte:** [URL ou origem]
**Stack/Tipo:** [tecnologia, linguagem, categoria]

---

## O que é
[1-2 frases]

---

## Como funciona
[mecanismo interno se técnico, fluxo de dados]

---

## Capacidades
[lista do que pode fazer]

---

## Como usar
[código ou passos, exemplos práticos]

---

## Quando usar
[tabela: situação → usar? + motivo]

---

## Quando NÃO usar / Limitações
[casos em que não se aplica, alternativas]

---

## Requisitos
[dependências, pré-requisitos, instalação]

---

## Boas práticas
[dicas não óbvias, armadilhas comuns]

---

## Momento de utilização nos projetos
[mapeamento explícito para projetos do vault]

---

## Relacionado
[wikilinks para notas relevantes do vault]
```

### Regras de qualidade

- **Nunca copiar literalmente** o conteúdo da fonte — reescrever com linguagem direta
- **Remover redundância** — se a nota de destino já tem um conceito, não repetir
- **Adicionar contexto dos projetos** — sempre mapear para projetos reais do vault
- **Código real** — incluir exemplos de código quando a fonte for técnica
- **Alternativas** — sempre listar pelo menos 2-3 alternativas com quando preferir cada

---

## Fase 6 — Salvar e commitar

### 6.1 Salvar nota

Usar `Write` (nova nota) ou `Edit` (atualização de existente).

### 6.2 Atualizar MAPA.md se nota for relevante

Se a nota for de `02_Knowledge/` ou criar nova seção em `05_Research/`:
- Adicionar link em `14_Indexes/MAPA.md` na seção correta

### 6.3 Commit e push

```bash
git add [arquivo-criado-ou-atualizado]
git commit -m "feat: absorver — [nome do recurso/conceito]

[1-2 linhas descrevendo o que foi extraído e de onde]

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
git push
```

---

## Fase 7 — Relatório de absorção

Ao final, informar:

```
Absorvido:
✅ [nome] → [pasta/arquivo.md] ([novo/atualizado])
✅ [nome] → [pasta/arquivo.md] ([novo/atualizado])

Descartado:
❌ [URL] — motivo (duplicata de [[nota]], sem conteúdo técnico, etc.)

Commit: [hash]
```

---

## Exemplos de ativação

```
/absorver https://github.com/mmcloughlin/globe
/absorver https://balsamiq.com/blog/wireframing-site-builders/ https://mailchimp.com/pt-br/resources/website-wireframe/
/absorver Essa biblioteca faz X, Y, Z. Usar quando precisar de W.
/absorver [cola conteúdo]
```

---

## Anti-padrões (nunca fazer)

- ❌ Copiar bloco de texto integral da fonte sem reescrever
- ❌ Criar nota sem frontmatter
- ❌ Criar nota duplicata de algo já no vault
- ❌ Salvar sem commitar
- ❌ Ignorar seção "momento de utilização nos projetos"
- ❌ Criar nota genérica sem vínculo com projetos reais do vault
- ❌ Incluir propaganda, CTAs ou conteúdo de UI da página fonte

---

## Relacionado

- [[99_System/SKILLS-REGISTRY]] — registro de skills
- [[99_System/COMANDOS-PADRAO]] — comandos de ferramentas locais
- [[02_Knowledge/fluxo-criacao-design-figma]] — exemplo de conhecimento bem estruturado
