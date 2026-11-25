---
name: programacao-extrema
description: "Base de conhecimento de \"Programação eXtrema (XP) Explicada: Acolha as Mudanças\" por Kent Beck (1ª ed.). Use ao aplicar os frameworks de Beck para XP — quatro valores, 12 práticas, Jogo do Planejamento, projeto simples, refatoração, programação em pares, TDD, custo das modificações — estudar o livro ou consultar seus conceitos."
---

<!-- argument-hint: [tópico, nome de prática ou número de capítulo] -->

# Programação eXtrema (XP) Explicada: Acolha as Mudanças
**Autor**: Kent Beck | **Páginas**: ~164 | **Capítulos**: 27 (em 16 arquivos) | **Gerado**: 2026-06-26

## Como Usar Esta Skill

- **Sem argumentos** — carrega os frameworks centrais (valores, práticas) para referência.
- **Com um tópico** — pergunte sobre `programação em pares`, `jogo do planejamento`,
  `projeto simples`, `custo das modificações`; eu localizo e leio o capítulo relevante.
- **Com capítulo** — peça `ch06` para carregar aquele arquivo específico.
- **Navegar** — pergunte "quais capítulos você tem?" para ver o índice completo.

Quando você perguntar sobre um tópico fora dos Frameworks Centrais abaixo, eu lerei o
arquivo de capítulo correspondente antes de responder.

---

## Frameworks Centrais & Modelos Mentais

**A tese da XP**: o problema do software é o **risco**. A XP o ataca aceitando a mudança em
vez de tentar prevê-la. Isso só é viável porque a **curva de custo das modificações pode ser
achatada** (projeto simples + testes automatizados + refatoração constante) — a grande
premissa técnica do livro. Se mudar é barato, decida o mais tarde possível e preserve opções.

**Os Quatro Valores** (Ch 7) — critério de "como o desenvolvimento deve ser sentido":
- **Comunicação** · **Simplicidade** · **Feedback** · **Coragem** — sustentados por um quinto, **Respeito**.
- Regra: adote práticas que *forçam* comunicação; "otimismo é a doença, feedback é o tratamento"; coragem sem os outros três é só *hacking*.

**Cinco Princípios Fundamentais** (Ch 8): feedback rápido · simplicidade presumida ·
mudanças incrementais · aceitação das mudanças · alta qualidade. (+ ~10 menos fundamentais:
jogar para ganhar, viajar com pouca bagagem, aceitação de responsabilidades, adaptação local…)

**As Quatro Atividades** (Ch 9): **codificar, testar, ouvir, projetar** — tudo que a XP estrutura.

**As Quatro Variáveis** (Ch 4): custo, tempo, qualidade, **escopo**. Negócios fixam 3; o time
entrega o escopo. Nunca fixe as quatro (a qualidade some). Escopo é o seu volante.

**As 12 Práticas** (Ch 10 — o coração):
Jogo do Planejamento · Entregas frequentes · Metáfora · Projeto simples · Testes ·
Refatoração · Programação em pares · Propriedade coletiva · Integração contínua ·
Semana de 40 horas · Cliente presente · Padrões de codificação.
→ Nenhuma se sustenta sozinha (exceto testes); o ponto fraco de cada uma é compensado pelos
pontos fortes das outras (Ch 11). Valor pleno só com (quase) todas juntas (regra 20-80, Ch 23).

**Decisões-chave à moda Beck**:
- *Use XP quando* os requisitos forem vagos/instáveis; *não use* sob curva exponencial, time grande, feedback lento ou ambiente físico errado (Ch 25).
- *Projeto simples* = comunica · sem duplicação · menos classes · menos métodos (nessa ordem). "A coisa mais simples que poderia funcionar" (Ch 17).
- *Test-first*: teste só o que pode falhar; unidade a 100%, funcional em % (Ch 18).
- *Estime* em Tempo Ideal × fator de carga (~2–4); quem implementa, estima (Ch 15).
- *Dirija* o projeto com pequenas correções contínuas guiadas por feedback — o motorista é o cliente (Ch 6).

---

## Índice de Capítulos

| # | Título | Frameworks-chave |
|---|--------|------------------|
| [ch01](chapters/ch01-risco-economia-episodio.md) | Risco, Economia, Episódio (Cap. 1–3) | risco como problema, economia de opções, episódio de desenvolvimento |
| [ch02](chapters/ch02-quatro-variaveis-custo-mudanca.md) | Quatro Variáveis, Custo, Dirigir (Cap. 4–6) | quatro variáveis, curva achatada, metáfora da condução |
| [ch03](chapters/ch03-quatro-valores.md) | Os Quatro Valores (Cap. 7) | comunicação, simplicidade, feedback, coragem, respeito |
| [ch04](chapters/ch04-principios-basicos.md) | Princípios Básicos (Cap. 8) | 5 princípios fundamentais, jogar para ganhar, viajar leve |
| [ch05](chapters/ch05-quatro-atividades.md) | As Quatro Atividades (Cap. 9) | codificar, testar, ouvir, projetar; entropia |
| [ch06](chapters/ch06-doze-praticas.md) | As 12 Práticas (Cap. 10) | todas as 12 práticas; projeto simples (4 critérios) |
| [ch07](chapters/ch07-sinergia-praticas.md) | Sinergia das Práticas (Cap. 11) | "seria impossível… a não ser que…"; reforço mútuo |
| [ch08](chapters/ch08-gerenciamento-ambiente.md) | Gerenciamento e Ambiente (Cap. 12–13) | gerência descentralizada, métricas, mural, espaço aberto |
| [ch09](chapters/ch09-responsabilidades-negocio-tecnica.md) | Responsabilidades Negócio/Técnica (Cap. 14) | divisão de poder, tecnologia como decisão de negócio |
| [ch10](chapters/ch10-estrategia-planejamento.md) | Estratégia de Planejamento (Cap. 15) | Jogo do Planejamento, fases, tempo ideal, fator de carga |
| [ch11](chapters/ch11-estrategia-desenvolvimento.md) | Estratégia de Desenvolvimento (Cap. 16) | integração contínua, propriedade coletiva, pares |
| [ch12](chapters/ch12-estrategia-projeto.md) | Estratégia de Projeto (Cap. 17) | coisa mais simples, projeto via refatoração, once and only once |
| [ch13](chapters/ch13-estrategia-testes.md) | Estratégia de Testes (Cap. 18) | test-first, unidade vs. funcional, testar é apostar |
| [ch14](chapters/ch14-adotando-ajustando-ciclo-vida.md) | Adotar, Ajustar, Ciclo de Vida (Cap. 19–21) | pior problema primeiro, retrofitting, 5 fases |
| [ch15](chapters/ch15-papeis.md) | Papéis para Pessoas (Cap. 22) | programador, cliente, testador, rastreador, treinador, consultor, chefão |
| [ch16](chapters/ch16-regra-20-80-dificuldades-limites.md) | 20-80, Dificuldades, Limites (Cap. 23–27) | regra 20-80, XP é simples mas não fácil, quando não usar, contratos |

## Índice de Tópicos

- **Cliente presente / on-site customer** → ch06, ch09, ch15
- **Coragem** → ch03
- **Curva de custo das modificações** → ch02, ch12
- **Economia / opções** → ch01
- **Entregas frequentes / releases** → ch06, ch10, ch14
- **Episódio de desenvolvimento** → ch01, ch11
- **Estimativa / tempo ideal / fator de carga** → ch10
- **Integração contínua** → ch06, ch11
- **Jogo do Planejamento** → ch06, ch09, ch10
- **Limites / quando não usar XP** → ch16
- **Métricas / gerenciamento** → ch08
- **Metáfora** → ch06, ch12
- **Padrões de codificação** → ch06
- **Papéis** → ch15
- **Princípios** → ch04
- **Programação em pares** → ch06, ch11, ch15
- **Projeto simples / once and only once** → ch06, ch12
- **Propriedade coletiva** → ch06, ch11
- **Quatro atividades** → ch05
- **Quatro valores** → ch03
- **Quatro variáveis / escopo** → ch02
- **Refatoração** → ch06, ch12, ch14
- **Risco** → ch01
- **Semana de 40 horas** → ch06
- **Sinergia das práticas** → ch07
- **Testes / TDD / funcional / unidade** → ch05, ch06, ch13
- **Adoção / retrofitting / ciclo de vida** → ch14

## Arquivos de Apoio

- [glossary.md](glossary.md) — todos os termos do dicionário da XP com definições
- [patterns.md](patterns.md) — as práticas e técnicas (quando usar / como / trade-offs)
- [cheatsheet.md](cheatsheet.md) — tabelas de decisão: quando usar XP, "mais simples", o que testar, tells & smells

---

## Escopo & Limites

Esta skill cobre a **1ª edição** (2000) de *Extreme Programming Explained*, traduzida ao
português (Bookman, 2008). É a edição das **12 práticas** e da **semana de 40 horas** — a 2ª
edição (2004) reorganizou valores, adicionou princípios e renomeou/expandiu práticas (ex.:
"sustainable pace"). Para implementação no seu código, combine com ferramentas do projeto.
Para tópicos além do livro, consulte skills relacionadas ou pergunte ao agente.
