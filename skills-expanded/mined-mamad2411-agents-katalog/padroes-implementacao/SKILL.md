---
name: padroes-implementacao
description: "Base de conhecimento de \"Padrões de Implementação\" por Kent Beck. Use ao aplicar os padrões de Beck para escrever código Java que comunica intenção — valores/princípios, classe, estado, comportamento, métodos, coleções, frameworks — estudar o livro ou consultar seus conceitos."
---

<!-- argument-hint: [tópico, nome de padrão ou número de capítulo] -->

# Padrões de Implementação
**Autor**: Kent Beck | **Páginas**: ~159 | **Capítulos**: 10 + apêndice | **Gerado**: 2026-07-04

## Como usar esta skill

- **Sem argumentos** — carrega os frameworks centrais (valores, princípios, técnicas de variação).
- **Com um tópico** — pergunte sobre `delegação`, `objeto método`, `coleções`, `frameworks`; eu leio o capítulo relevante antes de responder.
- **Com capítulo** — peça `ch05`; carrego aquele capítulo específico.
- **Navegar** — pergunte "quais capítulos você tem?" para ver o índice.

Quando o tópico não estiver nos frameworks centrais abaixo, leio o arquivo de capítulo antes de responder.

---

## Frameworks & Modelos Mentais Centrais

**Tese do livro**: o objetivo do código é **comunicar intenção a outros programadores**. A maior parte do custo de um software vem *depois* da implantação, e lê-se código muito mais do que se escreve — então código barato = código legível. Padrões de implementação são as decisões táticas que se toma *vários por minuto* (nomear, iterar, decompor), distintas dos padrões de projeto (GoF), tomados poucas vezes ao dia.

### A equação equilibrada
**Padrões = o que fazer · Valores = motivação · Princípios = traduzem motivação em ação.**

### Os 3 Valores (em conflito, resolva nesta ordem)
- **Comunicação** — o leitor entende, modifica, usa. Vence quando conflita.
- **Simplicidade** — elimine complexidade *em excesso*, não a essencial. No olho de quem vê; escreva p/ o público.
- **Flexibilidade** — **só onde o programa muda**. É a desculpa nº1 p/ código ruim. Melhor de simplicidade+testes que de projeto especulativo.

### Os 6 Princípios (todos corolários de Consequências Locais)
- **Consequências locais** — mudança aqui não quebra lá. Princípio-raiz.
- **Minimizar repetição** · **Lógica e dados em harmonia** · **Simetria** (mesma ideia, mesma forma) · **Expressão declarativa** (intenção sem seguir fluxo) · **Ritmo de mudança** (una o que muda junto; simetria temporal).

### Expressar variação de LÓGICA (custo crescente — escolha o mais barato que serve)
`Condicional` (poucos ramos estáveis) → `Subclasse` (variação fixa unidimensional) → `Delegação` (muda em runtime) → `Seletor plugável` (1-2 métodos, caro). Envio duplo p/ 2 dimensões. Só delegação/condicional mudam em runtime.

### Expressar variação de DADOS
0 = ausência · 1 = campo · **muitos = coleção**. Coleção comunica variação de número; interface escolhida revela ordem/unicidade/acesso.

### Fluxo de controle — ordem de preferência
`sequência → mensagem → iteração → condicional → exceção`. Cada **mensagem** é ponto de variação barato; cada **condicional explícito** é ponto de modificação futura. **Cláusula de guarda** (retorno prematuro) > `if/else` aninhado. Exceção só quando o resto confundiria; embrulhe baixo→alto nível.

### Métodos
**Método composto**: chamadas no mesmo nível de abstração. Nomeie pela **intenção do invocador** (`find()`, não `linearSearch()`). Limite visibilidade, revele aos poucos (`private` primeiro). **Construtor completo** comunica obrigatórios; **método fábrica** só quando faz mais que criar. Get/set públicos são cheiro de lógica mal localizada — mova lógica+dados juntos.

### Estado
Estados similares juntos, diferentes separados (mesmo uso + mesmo tempo de vida). Prefira **estado comum** (campos) a variável (`Map`); **parâmetro** a referência permanente; **inicialização ansiosa** a preguiçosa. Nome = função; tipo/escopo = contexto. Tipo declarado comunica *uso*, não implementação — mas consistência vence generalidade.

### Frameworks invertem a economia
Custo dominante deixa de ser *entender* e passa a ser *atualizar clientes*. Aceite complexidade que preserva evolução; exponha o mínimo e o mais estável (campos **privados**). Framework = **interseção** das necessidades comuns, não união.

### Regra de ouro operacional
**Escreva com fatos, não especulação.** Faça funcionar, depois estruture. Se a divisão piora a leitura, alinhe num método gigante e reparticione com a experiência recente.

---

## Índice de Capítulos

| # | Título | Padrões-chave |
|---|--------|----------------|
| [ch01](chapters/ch01-introducao.md) | Introdução | padrão de implementação, 3 passos p/ comunicar |
| [ch02](chapters/ch02-padroes.md) | Padrões | padrão de forças, padrões trabalham juntos |
| [ch03](chapters/ch03-teoria-valores-principios.md) | Uma Teoria de Programação | 3 valores, 6 princípios |
| [ch04](chapters/ch04-motivacao.md) | Motivação | equação de custo, valor temporal do dinheiro |
| [ch05](chapters/ch05-classe.md) | Classe | objeto valor, subclasse, delegação, interface vs. classe abstrata |
| [ch06](chapters/ch06-estado.md) | Estado | estado comum/variável, objeto parâmetro, inicialização |
| [ch07](chapters/ch07-comportamento.md) | Comportamento | mensagem de escolha, envio duplo, cláusula de guarda, exceção |
| [ch08](chapters/ch08-metodos.md) | Métodos | método composto, objeto método, construtor completo, fábrica |
| [ch09](chapters/ch09-colecoes.md) | Coleções | interfaces/implementações, desempenho, delegar vs. herdar |
| [ch10](chapters/ch10-evoluindo-frameworks.md) | Evoluindo Frameworks | estilos de uso, interface vs. superclasse, atualização incompatível |
| [ch11](chapters/ch11-apendice-medindo-desempenho.md) | Apêndice: Medindo Desempenho | framework de cronometragem, medir antes de crer |

## Índice de Tópicos

- **Cláusula de guarda** → ch07
- **Coleções (escolha/desempenho)** → ch09, ch11
- **Comunicação (valor)** → ch03, ch01
- **Condicional / delegação / subclasse** → ch05, ch07
- **Construtor completo / método fábrica** → ch08, ch10
- **Consequências locais** → ch03, ch09
- **Conversão** → ch08
- **Envio duplo** → ch07
- **Estado (comum/variável/extrínseco)** → ch06
- **Exceção / propagação** → ch07
- **Frameworks (evolução, compatibilidade)** → ch10
- **Inicialização (ansiosa/preguiçosa)** → ch06
- **Interface vs. classe abstrata / superclasse** → ch05, ch10
- **Interface versionada** → ch05, ch10
- **Método composto / auxiliar** → ch08
- **Nome (classe/método/variável)** → ch05, ch06, ch08
- **Objeto método** → ch08
- **Objeto parâmetro / parâmetro coletor** → ch06
- **Objeto valor** → ch05
- **Princípios (simetria, ritmo de mudança...)** → ch03
- **Simplicidade / flexibilidade (valores)** → ch03
- **Tipo declarado / de retorno** → ch06, ch08
- **Variação de lógica vs. dados** → ch05, ch09
- **Visibilidade de método** → ch08, ch10

## Arquivos de Apoio

- [glossary.md](glossary.md) — todos os termos com definições e capítulo
- [patterns.md](patterns.md) — catálogo de técnicas (quando/como/trade-off)
- [cheatsheet.md](cheatsheet.md) — tabelas de decisão e regras rápidas

---

## Escopo & Limites

Cobre o conteúdo do livro (Java, viés p/ desenvolvimento de aplicações). Para implementação no seu código, combine com ferramentas do projeto. Concorrência e processo de software estão fora do escopo do livro (Beck recomenda isolar concorrência). Skills relacionadas: [[beck-tdd]], [[programacao-extrema]], [[fowler-refactoring]], [[dive-into-design-patterns]].
