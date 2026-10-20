---
name: beck-tdd
description: "Base de conhecimento de \"TDD: Desenvolvimento Guiado por Testes (Test Driven Development: By Example)\" por Kent Beck. Use ao aplicar o método TDD de Beck — ciclo vermelho/verde/refatore, Fake It, Triangulação, Implementação Óbvia, lista de testes, padrões de teste e de projeto, refatoração — estudar o livro ou consultar seus conceitos."
---

<!-- argument-hint: [tópico, nome do padrão ou número do capítulo] -->

# TDD: Desenvolvimento Guiado por Testes
**Autor**: Kent Beck (trad. Bookman, 2010 — orig. *Test Driven Development: By Example*, 2003) | **Páginas**: ~215 | **Capítulos**: 32 (em 12 arquivos) | **Gerado**: 2026-06-26

## Como Usar Esta Skill

- **Sem argumentos** — carrega os frameworks centrais (ciclo, regras, padrões de barra verde).
- **Com um tópico** — pergunte sobre `fake it`, `triangulação`, `mock object`, `value object`, `lista de testes`; eu acho e leio o capítulo relevante.
- **Com capítulo** — peça `ch07` e eu carrego aquele arquivo.
- **Navegar** — pergunte "quais capítulos você tem?" para ver o índice.

Quando você perguntar sobre um tópico fora dos Frameworks Centrais abaixo, eu leio o arquivo de capítulo antes de responder.

---

## Frameworks & Modelos Mentais Centrais

### As duas regras (origem de tudo)
1. **Escreva um teste automático que falhe** antes de qualquer código de produção.
2. **Remova duplicação.**
Dependência é o problema-chave do software; duplicação é o sintoma. Remover duplicação (regra 2) elimina dependência.

### Ciclo vermelho/verde/refatore
1. Adicione um pequeno teste → 2. Rode todos e veja falhar → 3. Faça a mudança mínima (pode ser feia) → 4. Rode todos e veja passar → 5. Refatore para remover duplicação.
> **Resolva "funciona" primeiro, "limpo" depois.** "Um verde rápido perdoa todos os pecados — por um momento." Meta: *código limpo que funciona* (Ron Jeffries).

### As três formas de chegar ao verde (o coração ensinável)
- **Faça de Conta (Fake It)** — retorne uma constante e transforme-a gradualmente em expressão com variáveis. Use quando não souber a implementação.
- **Triangulação (Triangulate)** — só abstraia com **dois ou mais exemplos**. Use quando inseguro sobre a abstração.
- **Implementação Óbvia (Obvious Implementation)** — apenas digite a solução simples quando souber. "Segunda marcha"; reduza se barras vermelhas o surpreenderem.

### Disciplina de teste
- **Lista de Testes (Test List)** — antes de começar, liste todos os testes que sabe que precisará; um por vez (nunca em massa).
- **Test First / Assert First** — teste antes do código; comece o teste pela asserção e preencha de trás para frente. É controle de escopo e projeto, não cerimônia.
- **Teste Isolado** — testes rápidos, independentes de ordem. Um teste quebrado = um problema. Força alta coesão / baixo acoplamento.
- **One Step Test** — pegue o próximo teste que *ensina algo* e que você *confia que consegue* implementar.

### Heurísticas de seleção e parada
- "Escreva testes até o **medo virar tédio**" (Phlip). Teste condicionais, laços, operações, polimorfismo — mas só do *seu* código.
- Quantos testes? Calibre pelo **TMEF** (Tempo Médio Entre Falhas), não por permutações.
- Apague um teste só se redundante em **confiança** *e* **comunicação**.
- **Testes são o canário da mina**: setup longo/duplicado, testes lentos ou frágeis sinalizam problema de *projeto*, não de teste. Suíte ≤ 10 min.

### Padrões que emergem na refatoração
Value Object (resolve aliasing; implementa igualdade), Null Object, Composite + Collecting Parameter, Template Method, Pluggable Object, Factory Method. No TDD eles **emergem ao eliminar duplicação** — não são desenhados antes. "Como fornecer variável global? **Não forneça**" (sem Singleton).

### Smells acionáveis
- 2+ mensagens a outro objeto num método → **Move Method**.
- Condicional explícito se espalhando → **Pluggable Object**.
- Teste grande demais → **Child Test**. Recurso caro → **Mock Object**.
- Terminar sessão: solo → deixe um teste quebrado; em time → **Clean Check-in** (tudo verde).

---

## Índice de Capítulos

| # | Título | Frameworks-chave |
|---|--------|------------------|
| [ch01](chapters/ch01-money-ciclos-iniciais.md) | Money — Ciclos Iniciais (Caps. 1–9) | duas regras, vermelho/verde/refatore, Value Object, Factory Method |
| [ch02](chapters/ch02-money-expression-bank.md) | Money — Expression, Bank, Retrospectiva (10–17) | metáfora Expression, Reduce, métricas, TMEF |
| [ch03](chapters/ch03-xunit-exemplo.md) | Exemplo xUnit em Python (18–24) | bootstrap, Template Method, Composite, Collecting Parameter |
| [ch04](chapters/ch04-padroes-tdd.md) | Padrões de TDD (25) | Test List, Test First, Assert First, Isolated/Evident Data |
| [ch05](chapters/ch05-padroes-barra-vermelha.md) | Padrões de Barra Vermelha (26) | One Step/Starter/Regression/Learning Test, Pausa |
| [ch06](chapters/ch06-padroes-de-teste.md) | Padrões de Teste (27) | Child Test, Mock, Self Shunt, Log String, Crash Test Dummy |
| [ch07](chapters/ch07-padroes-barra-verde.md) | Padrões de Barra Verde (28) | Fake It, Triangulate, Obvious Implementation, One to Many |
| [ch08](chapters/ch08-padroes-xunit.md) | Padrões xUnit (29) | Assertion, Fixture, Test Method, Exception Test, All Tests |
| [ch09](chapters/ch09-padroes-de-projeto.md) | Padrões de Projeto (30) | Value Object, Null Object, Composite, Pluggable, Command |
| [ch10](chapters/ch10-refatoracao.md) | Refatoração (31) | Reconcile Differences, Isolate Change, Migrate Data, Extract/Move Method |
| [ch11](chapters/ch11-dominando-tdd.md) | Dominando TDD (32) | tamanho de passos, TMEF, ATDD, frameworks via Aberto/Fechado |
| [ch12](chapters/ch12-apendices.md) | Apêndices + Posfácio | diagramas de influência, Fibonacci, modos monológicos (Fowler) |

## Índice de Tópicos

- **Assert First / Evident Data / Test Data** → ch04
- **ATDD (Application TDD)** → ch11
- **Bank / Expression / Reduce** → ch02
- **Child Test** → ch06
- **Composite** → ch03, ch09
- **Collecting Parameter** → ch03, ch09
- **Crash Test Dummy** → ch06
- **Diagramas de influência** → ch04, ch12
- **Duplicação vs. dependência** → ch01
- **Exception Test** → ch08
- **Fake It (Faça de Conta)** → ch07
- **Factory Method** → ch01, ch09
- **Fibonacci dirigido por testes** → ch12
- **Fixture / setUp / tearDown** → ch08
- **Lista de Testes (Test List)** → ch04
- **Mock Object** → ch06
- **Move Method / Extract Method / Inline / Migrate Data** → ch10
- **Null Object** → ch09
- **Obvious Implementation** → ch07
- **One Step / Starter / Regression / Learning Test** → ch05
- **One to Many** → ch07
- **Pluggable Object / Selector** → ch09
- **Self Shunt / Log String** → ch06
- **Template Method** → ch08, ch09
- **TMEF / quantos testes** → ch11
- **Triangulação** → ch07
- **Value Object** → ch01, ch09
- **Vermelho/verde/refatore** → ch01
- **xUnit (TestCase/TestResult/TestSuite)** → ch03, ch08

## Arquivos de Apoio

- [glossary.md](glossary.md) — todos os termos e padrões com definição e capítulo
- [patterns.md](patterns.md) — todas as técnicas/padrões (When/How/Trade-off)
- [cheatsheet.md](cheatsheet.md) — tabelas de decisão e heurísticas de bolso

---

## Escopo & Limites

Cobre o conteúdo do livro (TDD por exemplos em Java/Python, padrões de teste, de projeto e refatoração). Para teste de unidade aprofundado (mocks vs. stubs, pilares de bons testes), veja as skills `khorikov-unit-testing` e `art-of-unit-testing`. Para legado, `working-effectively-legacy-code`. TDD é uma das 12 práticas de XP — veja `programacao-extrema`.
