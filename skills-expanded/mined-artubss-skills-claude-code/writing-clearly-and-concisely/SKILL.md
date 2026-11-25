---
name: writing-clearly-and-concisely
description: Use quando estiver escrevendo prosa que humanos vão ler—documentação, mensagens de commit, mensagens de erro, explicações, relatórios ou texto de interface. Aplica as regras atemporais de Strunk para uma escrita mais clara, forte e profissional.
---

# Escrevendo com Clareza e Concisão

## Visão Geral

Escreva com clareza e força. Essa habilidade cobre o que fazer (Strunk) e o que não fazer (padrões de IA).

## Quando Usar Essa Habilidade

Use essa habilidade sempre que escrever prosa para humanos:

- Documentação, arquivos README, explicações técnicas
- Mensagens de commit, descrições de pull request
- Mensagens de erro, copy de interface, texto de ajuda, comentários
- Relatórios, resumos ou qualquer explicação
- Edição para melhorar a clareza

**Se você está escrevendo frases para um humano ler, use essa habilidade.**

## Estratégia com Contexto Limitado

Quando o contexto está apertado:

1. Escreva seu rascunho usando seu julgamento
2. Delegue a um subagente com seu rascunho e o arquivo da seção relevante
3. Deixe o subagente revisar e retornar a revisão

Carregar uma única seção (~1.000-4.500 tokens) em vez de tudo economiza contexto significativo.

## Elementos de Estilo

*The Elements of Style* (1918) de William Strunk Jr. ensina você a escrever com clareza e cortar com rigor.

### Regras

**Regras Elementares de Uso (Gramática/Pontuação)**:

1. Forme possessivo singular adicionando 's
2. Use vírgula após cada termo em série exceto o último
3. Coloque expressões parentéticas entre vírgulas
4. Vírgula antes de conjunção introduzindo cláusula coordenada
5. Não junte cláusulas independentes com vírgula
6. Não divida frases em duas
7. Frase participial no início refere-se ao sujeito gramatical

**Princípios Elementares de Composição**:

8. Um parágrafo por tópico
9. Comece parágrafo com frase-tema
10. **Use voz ativa**
11. **Coloque afirmações em forma positiva**
12. **Use linguagem definida, específica e concreta**
13. **Omita palavras desnecessárias**
14. Evite sucessão de frases soltas
15. Expresse ideias coordenadas em forma similar
16. **Mantenha palavras relacionadas juntas**
17. Mantenha um tempo único em resumos
18. **Coloque palavras enfáticas no final da frase**

### Arquivos de Referência

As regras acima são resumidas do texto original de Strunk. Para explicações completas com exemplos:

| Seção | Arquivo | ~Tokens |
|-------|---------|---------|
| Gramática, pontuação, regras de vírgula | `02-elementary-rules-of-usage.md` | 2.500 |
| Estrutura de parágrafo, voz ativa, concisão | `03-elementary-principles-of-composition.md` | 4.500 |
| Títulos, citações, formatação | `04-a-few-matters-of-form.md` | 1.000 |
| Escolha de palavras, erros comuns | `05-words-and-expressions-commonly-misused.md` | 4.000 |

**A maioria das tarefas precisa apenas de `03-elementary-principles-of-composition.md`** — cobre voz ativa, forma positiva, linguagem concreta e omissão de palavras desnecessárias.

## Padrões de Escrita de IA para Evitar

LLMs regridem para a média estatística, produzindo prosa genérica e inchada. Evite:

- **Exagero:** pivotal, crucial, vital, testemunho, legado duradouro
- **Frases "-ing" vazias:** assegurando confiabilidade, mostrando recursos, destacando capacidades
- **Adjetivos promocionais:** revolucionário, perfeito, robusto, ponta de lança
- **Vocabulário de IA sobregasado:** explorar profundamente, aproveitar, multifacetado, fomentar, domínio, tapeçaria
- **Uso excessivo de formatação:** bullets em excesso, decorações com emoji, negrito em toda outra palavra

Seja específico, não grandiloqüente. Diga o que realmente faz.

Para pesquisa abrangente sobre por que esses padrões ocorrem, veja `signs-of-ai-writing.md`. Editores da Wikipedia desenvolveram esse guia para detectar submissões geradas por IA — seus padrões são bem documentados e testados em campo.

## Resumo

Escrevendo para humanos? Carregue a seção relevante de `elements-of-style/` e aplique as regras. Para a maioria das tarefas, `03-elementary-principles-of-composition.md` cobre o que realmente importa.