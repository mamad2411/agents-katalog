---
name: fowler-refactoring
description: "Base de conhecimento de \"Refatoração: Aperfeiçoando o Projeto de Código Existente, 2ª ed\" por Martin Fowler. Use ao aplicar as refatorações e a mecânica de Fowler — extrair função, maus cheiros, testes, encapsulamento, condicionais, APIs, herança — estudar o livro ou consultar seus conceitos."
---

<!-- argument-hint: [tópico, nome de refatoração, cheiro ou número do capítulo] -->

# Refatoração — Aperfeiçoando o Projeto de Código Existente (2ª ed.)
**Autor**: Martin Fowler (com Kent Beck) | **Páginas**: ~480 | **Capítulos**: 12 | **Gerado**: 2026-07-04

## Como usar esta skill

- **Sem argumentos** — carrega os frameworks centrais abaixo.
- **Com um tópico** — pergunte sobre `cláusulas de guarda`, `extrair função`, `maus cheiros`, `polimorfismo`; localizo e leio o capítulo relevante.
- **Com um cheiro** — diga o cheiro (ex.: `função longa`) e sugiro as refatorações que o curam ([cheatsheet.md](cheatsheet.md)).
- **Com capítulo** — peça `ch10`; carrego aquele capítulo.
- **Catálogo** — 61 refatorações em [patterns.md](patterns.md); peça "liste o catálogo".

Ao perguntar um tópico fora dos Frameworks Centrais abaixo, leio o capítulo relevante antes de responder.

---

## Frameworks & modelos mentais centrais

**O que é refatoração.** Modificar a *estrutura interna* do código para deixá-lo mais fácil de entender e barato de alterar, **sem mudar o comportamento observável**. Não é "qualquer limpeza" — é uma cadeia de passos pequenos que preservam comportamento. Se o código ficou quebrado por horas/dias, não foi refatoração.

**Dois Chapéus (Kent Beck).** A cada instante você usa UM chapéu: *adicionar funcionalidade* (novos testes passam) ou *refatorar* (não adiciona teste, não muda comportamento). Troque de chapéu conscientemente; nunca use os dois juntos.

**Ritmo dos pequenos passos.** Testes verdes → um passo da mecânica → rodar testes → verde = commit; vermelho = desfaça o passo (não depure). A refatoração é segura porque cada passo é reversível e testado.

**Código autotestável é pré-requisito.** Sem uma suíte de testes confiável, não refatore — você não saberá se preservou o comportamento. "Não sou ótimo programador; sou bom programador com ótimos hábitos" (Beck). Escreva testes onde é mais provável dar errado; sonde limites (vazio/zero/negativo/nulo).

**Quando refatorar (gatilhos):**
- **Regra de Três** — na terceira duplicação, elimine-a.
- **Refatoração preparatória** — antes de adicionar uma feature em código difícil, reestruture para tornar a mudança fácil.
- **Refatoração para compreensão** — ao decifrar código obscuro, grave o entendimento nele.
- **Oportunista (escoteiro)** — deixe o código melhor do que o encontrou, de passagem.

**Maus cheiros = quando/onde.** Cheiros (Ch 3) são heurísticas que apontam código a refatorar: Função longa, Nome misterioso, Código duplicado, Lista longa de parâmetros, Switches repetidos, Inveja de recursos, Cirurgia com rifle, Obsessão por primitivos, Herança recusada, etc. O cheiro indica o problema; o catálogo (Ch 6–12) fornece a cura. Mapa cheiro→refatoração no [cheatsheet.md](cheatsheet.md).

**As refatorações mais alavancadas (Ch 6):**
- **Extrair função (Extract Function)** — o movimento mais frequente: nomeie um trecho pela sua *intenção*. Inversa: Internalizar função.
- **Extrair/Internalizar variável** — nomeie subexpressões complexas.
- **Mudar declaração de função (Change Function Declaration)** — corrija nomes e assinaturas; use *procedimento de migração* quando há muitos chamadores.
- **Encapsular variável / Renomear** — controle acesso antes de renomear dado muito usado.

**Grandes movimentos estruturais:**
- **Separar em fases (Split Phase)** — divida "faz duas coisas em sequência" em etapas distintas.
- **Substituir condicional por polimorfismo** — troque switches repetidos sobre tipo por subclasses.
- **Cláusulas de guarda** — troque condicionais aninhadas por retornos antecipados para casos excepcionais.
- **Separar consulta de modificador** — uma função consulta OU modifica, nunca ambos (CQS).
- **Remover argumento de flag** — booleanos que selecionam comportamento viram funções explícitas.
- **Herança vs delegação** — quando a subclasse recusa a herança ou precisa mudar de tipo em runtime, prefira delegação (composição).

**Refatoração × desempenho.** Refatore para clareza; otimize depois, guiado por profiler. Código bem fatorado é mais fácil de acelerar. Yagni: não construa flexibilidade especulativa.

---

## Índice de capítulos

| # | Título | Frameworks-chave |
|---|--------|------------------|
| [ch01](chapters/ch01-primeiro-exemplo.md) | Refatoração: um primeiro exemplo | Extract Function, Replace Temp with Query, Split Phase, polimorfismo |
| [ch02](chapters/ch02-principios.md) | Princípios da refatoração | Dois Chapéus, Regra de Três, refatoração preparatória, Yagni |
| [ch03](chapters/ch03-maus-cheiros.md) | Maus cheiros no código | 24 cheiros → refatorações que curam |
| [ch04](chapters/ch04-escrevendo-testes.md) | Escrevendo testes | Código autotestável, fixture, sondar limites |
| [ch05](chapters/ch05-apresentacao-catalogo.md) | Apresentação do catálogo | Formato do verbete: nome/motivação/mecânica |
| [ch06](chapters/ch06-primeiro-conjunto.md) | Primeiro conjunto de refatorações | Extract/Inline Function, Change Declaration, Split Phase (11) |
| [ch07](chapters/ch07-encapsulamento.md) | Encapsulamento | Encapsular registro/coleção, Extrair classe, Ocultar delegação (9) |
| [ch08](chapters/ch08-movendo-recursos.md) | Movendo recursos | Mover função/campo, Dividir laço, Loop→Pipeline (9) |
| [ch09](chapters/ch09-organizando-dados.md) | Organizando dados | Separar variável, referência↔valor (5) |
| [ch10](chapters/ch10-condicionais.md) | Simplificando lógicas condicionais | Cláusulas de guarda, polimorfismo, caso especial (6) |
| [ch11](chapters/ch11-refatorando-apis.md) | Refatorando APIs | CQS, Remover flag, Preservar objeto inteiro, Command (10) |
| [ch12](chapters/ch12-heranca.md) | Lidando com herança | Subir/Descer método, Type Code→Subclasses, delegação (11) |

## Índice de tópicos

- **Cláusulas de guarda** → ch10
- **Código autotestável / testes** → ch04
- **Command-Query Separation** → ch11
- **Dois Chapéus** → ch02
- **Encapsulamento** → ch07
- **Extrair função** → ch01, ch06
- **Herança vs delegação** → ch12
- **Maus cheiros (24)** → ch03
- **Mecânica / procedimento de migração** → ch05, ch06
- **Mover função/campo** → ch08
- **Objeto de valor (referência↔valor)** → ch09
- **Pipeline (Loop→map/filter/reduce)** → ch08
- **Polimorfismo (substituir condicional)** → ch10
- **Princípios / quando refatorar** → ch02
- **Regra de Três** → ch02
- **Separar em fases (Split Phase)** → ch01, ch06
- **Testes de limite (boundary)** → ch04

## Arquivos de apoio

- [glossary.md](glossary.md) — termos conceituais com definições
- [patterns.md](patterns.md) — catálogo completo das 61 refatorações
- [cheatsheet.md](cheatsheet.md) — regras de decisão: quando refatorar, cheiro→cura, ritmo

---

## Escopo & limites

Cobre o conteúdo do livro (exemplos em JavaScript). Para aplicar na sua base de código, combine com testes e ferramentas do projeto. As refatorações têm mecânica passo a passo nos capítulos — siga-a em passos pequenos, testando entre cada um.
