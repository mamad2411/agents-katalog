---
name: zero-lero
description: Remove padrões de escrita de IA de textos em português brasileiro. Use ao redigir, editar ou revisar qualquer prosa em pt-BR para eliminar os tiques previsíveis de texto gerado por máquina.
metadata:
  trigger: Escrever, editar ou revisar prosa em português brasileiro
  language: pt-BR
  methodology: Construída empiricamente a partir de corpora de slop em pt-BR — v1 (geração livre), v2 (teste adversarial multi-gênero), v2.1 (calibração com corpus humano) e v2.2 (validação externa em GPT-5.5). Ver README.md e CHANGELOG.md. Não é tradução da skill stop-slop em inglês.
---

# Zero-Lero

Elimine os padrões previsíveis de escrita de IA em português brasileiro.

Princípio central: **densidade é o tell, não a instância**. Um "além disso" é humano; um por parágrafo é máquina. Aplique as regras por acúmulo, não mecanicamente.

Esse princípio tem número desde a calibração com corpus humano (~24 mil palavras de blogs pt-BR pré-2022, ver [docs/achados-corpus-humano.md](docs/achados-corpus-humano.md)):

- **Padrões que humano também usa** ("de forma [adj]", "cada vez mais", "através de", contraste retórico ocasional): instância isolada é escrita normal. Flagre a partir de ~3-4× a taxa humana — na prática, 2+ ocorrências num texto curto ou recorrência a cada poucos parágrafos.
- **Discriminadores quase perfeitos** (taxa humana zero em todo o corpus de controle): "não é à toa que", "vem ganhando/crescendo" sem dado, conclusão rotulada ("Em resumo", "Resumindo:"), "faz toda a diferença", "um verdadeiro [X]". Uma ocorrência merece olhar; duas no mesmo texto são evidência forte.
- **Parágrafo curto uniforme é tell estrutural**: parágrafo de IA tem em média 19-28 palavras; o humano, 52, com mais variação. Texto inteiro em parágrafos de 2-3 frases escaneáveis é fôrma de legibilidade, não escrita. É o único tell que ficou **mais** forte ao testar outro modelo: 18,7 palavras por parágrafo no GPT-5.5.
- **Parte das listas descreve um modelo, não a língua.** "Conta com", "cada vez mais", gerundismo e atribuição evasiva deram zero no corpus GPT-5.5 e davam 0,5 a 1,4 por mil no Claude; em compensação, "por isso" em cadeia e as formas modais do contraste são do GPT e quase não aparecem no Claude. Se o texto não bate com a lista, olhe a estrutura antes de concluir que está limpo. Taxas por corpus em [references/frases.md](references/frases.md).

## Regras centrais

1. **Corte o editorializing.** "É importante ressaltar", "vale destacar", "vale lembrar" e toda a família. Se vale ressaltar, ressalte: afirme o fato direto. Veja [references/frases.md](references/frases.md).

2. **Quebre o contraste binário, em qualquer das formas.** É o padrão nº 1 do slop em pt-BR e o mais camuflado. Sete realizações medidas: "Não se trata de X. Trata-se de Y."; "Não é apenas X, é Y"; "deixou de ser X e se tornou Y"; a positiva, que engana revisor, "é mais do que um X. É Y."; a modal, "não deve / não deveria ser X"; a pronominal, "não é aquele que X. É aquele que Y."; e a aposta pós-posta, "você tem um calendário. Não uma estratégia.". O tell é a reversão telegrafada, e não o "não" — buscar pela negação perde metade. Numa thread do corpus GPT-5.5 há sete reversões em 414 palavras. Afirme Y diretamente e corte a rampa. Veja [references/estruturas.md](references/estruturas.md).

3. **Mate o gerúndio pós-vírgula.** Frases que terminam em ", proporcionando...", ", garantindo...", ", otimizando...", ", facilitando o seu dia a dia" colam interpretação vazia ao fato. Corte a cláusula ou substitua pela consequência concreta (número, exemplo, resultado).

4. **Elimine o gerundismo.** "Estaremos enviando" vira "enviaremos" ou "vamos enviar". Sem exceção.

5. **Use voz ativa com agente nomeado.** "O mercado exige", "os dados mostram", "a cultura muda" são falsa agência: nada disso age sozinho. Nomeie quem faz, ou use "você". Passivas de design ("foi cuidadosamente pensado") escondem o sujeito.

6. **Seja específico.** "Faz toda a diferença", "as implicações são profundas", "inúmeros benefícios" anunciam importância sem entregar nada. Troque pelo dado, pelo exemplo, pela consequência nomeada. "Estudos mostram" sem estudo nomeado: cite a fonte ou corte a frase.

7. **Derrube as molduras.** Aberturas "No mundo atual", "Nos dias de hoje", "Em um mundo cada vez mais [X]" e fechos "Em resumo", "Em suma" sob heading "Conclusão". Comece pelo assunto. Termine no último ponto que importa, sem rotular o fim.

8. **Quebre a cadeia de conectivos.** "Além disso... Dessa forma... Por fim..." em sequência expõe o esqueleto do texto. A maioria das frases se conecta sozinha; corte o conectivo e teste.

9. **Varie o ritmo.** Parágrafos de comprimento idêntico, toda seção fechando em frase de efeito, pergunta retórica respondida na linha seguinte, staccato de uma-frase-por-linha: tudo isso é metrônomo. Misture frases longas e curtas. Termine parágrafos de jeitos diferentes. Deixe pelo menos um final ser um fato, não uma exortação.

10. **Confie no leitor.** Sem "Você já parou para pensar...?", sem "Pense nisso.", sem "Gostou? Compartilhe!". Sem fecho motivacional obrigatório. Sem "a boa notícia?", sem "o que ninguém te conta". O leitor não precisa de instrução para refletir nem de permissão para concordar.

11. **Cheque o registro contra o público.** Cada gênero tem um dialeto slopado próprio: juridiquês ("cumpre esclarecer", "outrossim") para leigos, academiquês ("o presente estudo"), corporativês de desculpa ("lamentamos profundamente"), liturgia de plataforma ("deixa o like, ativa o sininho"), clichê de press release ("reforça seu compromisso"). O tell é registro em fôrma + público errado — e a execução da fôrma completa, na ordem canônica, sempre. Veja a seção "Slop de registro" em [references/frases.md](references/frases.md).

12. **Desconfie da espontaneidade perfeita.** Quando o texto tenta soar humano, o slop troca de pele: "vou ser sincero", "kkk" calculado, "né?" em intervalos regulares, "EDIT:" fabricado — verniz casual sobre estrutura de redação intacta. Ignore o tom e olhe a arquitetura: se cada parágrafo cumpre função de manual, é fôrma. Aplique também dentro de aspas: citação fabricada carrega o slop da casa onde o revisor baixa a guarda.

13. **Aprenda com o que o humano faz (e a IA não).** Do corpus de controle: digressão que não volta, opinião assumida como palpite sem "estudos mostram", referência cravada (preço, data, lugar, nome), primeira pessoa que cita o próprio erro, frase torta a favor do ritmo, e final que simplesmente para quando o assunto acaba — sem recap, sem moral, sem CTA. Não são regras pra fabricar (humanidade fabricada é a regra 12); são a direção da reescrita: na dúvida entre o arredondado e o específico, vá no específico.

## Verificações rápidas

Antes de entregar o texto:

- Alguma variante de "ressaltar/destacar/lembrar que"? Corte e afirme direto.
- "Não se trata de X" ou "não é apenas X"? Afirme Y, corte a negação.
- "Não deve ser X", "não é aquele que X", "não é porque X. É porque Y"? Mesma reversão, roupa modal ou pronominal — afirme Y.
- Frase curta isolada começando em "Não" logo depois de uma afirmação ("Não uma estratégia.")? Negação aposta: junte à frase anterior ou corte.
- Três ou mais "por isso" no texto? Cadeia de conectivo — corte e releia.
- Frase terminando em vírgula + gerúndio de benefício? Corte ou concretize.
- "Estaremos + gerúndio"? Conjugue o futuro.
- "Conta com"? Troque por "tem" ou reestruture pela informação.
- "Não é à toa que"? Corte; deixe a evidência falar.
- "Através de"? Troque por "por", "com" ou "via".
- "Cada vez mais" sem número? Corte ou quantifique.
- "De forma [adjetivo]"? Troque pelo advérbio direto ou corte — é advérbio disfarçado.
- "Vem ganhando/crescendo/se consolidando" sem dado? Quantifique ou corte.
- Dois ou mais "além disso" no texto? Deixe no máximo um.
- Abertura com moldura temporal? Comece pelo assunto.
- Bullets em série com `**Rótulo:** frase que reformula o rótulo`? Escolha: ou o rótulo, ou a frase.
- Três itens em toda lista? Teste com dois, ou com quatro desiguais.
- "Estudos mostram/especialistas apontam" sem fonte? Nomeie ou corte.
- "Jornada", "divisor de águas", "no final do dia"? Tradutês: reescreva em português de gente.
- Pergunta retórica de abertura ou autorespondida ("O melhor de tudo? ...")? Afirme.
- "A boa notícia?", "Spoiler:", "Resultado:" antes da informação? Entregue a informação direto.
- "É mais do que um X. É Y."? Reversão telegrafada sem negação — afirme Y.
- "O que ninguém te conta", "que poucos sabem"? Corte o teatro de revelação.
- "Vou ser sincero", "kkk"/"né?" em posição calculada, "EDIT:" fabricado? Espontaneidade performada — desorganize de verdade ou assuma o registro escrito.
- Anáfora tripla ("sem X, sem Y, sem Z" / "Chega de... Chega de...")? Uma afirmativa no lugar.
- Registro empolado para público leigo ("cumpre esclarecer", "o presente estudo")? Traduza para português comum.
- Liturgia de plataforma completa e na ordem ("deixa o like... se inscreve... ativa o sininho")? No máximo um pedido, com voz própria.
- Citação entre aspas com estrutura de slogan? Aplique as regras dentro das aspas também.
- Conclusão rotulada em qualquer variante ("Em resumo", "Resumindo:", "Diante do exposto", "Veredito")? Corte e termine no último ponto que importa.
- Texto termina em CTA/exortação? Teste terminar no fato mais forte.
- Parágrafos todos entre 15 e 30 palavras? Fôrma de legibilidade. Junte alguns, deixe outros longos.
- Nada afirmado sem "pode", "talvez", "provavelmente"? Ou tudo afirmado sem base? Os dois extremos são tell, de modelos diferentes.
- Leia em voz alta. Se soar como locutor de comercial, coach de LinkedIn ou petição jurídica, ainda tem slop.

## Pontuação

Avalie de 1 a 10 em cada dimensão:

| Dimensão | Pergunta |
|---|---|
| Objetividade | Afirmações diretas ou anúncios e molduras? |
| Ritmo | Variado ou metronômico (legato uniforme ou staccato uniforme)? |
| Confiança no leitor | Respeita a inteligência de quem lê, ou conduz pela mão e pede engajamento? |
| Autenticidade | Soa como uma pessoa específica escrevendo, ou como "conteúdo"? |
| Densidade | Sobra algo cortável: conectivo, gerúndio vazio, conclusão redundante? |

**Abaixo de 35/50: revise e repasse as verificações.**

Cuidado com o excesso: texto que obedece todas as regras ao pé da letra fica picotado e robótico — slop ao contrário. A pontuação existe para forçar julgamento, não para ser gabaritada.

## Exceções

- Travessão é legítimo em pt-BR (diálogo, aposto). O tell é o travessão duplo estilo inglês cravado em frase comercial, não o travessão em si.
- Guia de voz do cliente ou do autor vence qualquer regra daqui. Pergunta retórica deliberada de uma marca fica; documente a exceção.
- Nunca altere fato, número, afirmação, nome ou compromisso ao remover slop.

## Referências

- [references/frases.md](references/frases.md) — frases e expressões a remover, com frequências do corpus
- [references/estruturas.md](references/estruturas.md) — padrões estruturais e de ritmo
- [references/exemplos.md](references/exemplos.md) — transformações antes/depois extraídas do corpus
