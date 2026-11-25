---
name: guidetour
description: Cria tutoriais guiados no estilo onboarding de app para qualquer página HTML, web-app, artefato ou apresentação de ideias. A página fica escura e apagada; cada área, botão, campo ou conceito acende quando a pessoa clica, e um cartão grande explica o que é, como usar, custos, privacidade, requisitos e o estado real. Tem tour guiado em sequência, modo explorar livre e modo sem tutorial. Três modos de montagem — réplica (reconstrói a interface de um app para ensiná-lo), sobreposição (injeta o tour numa página ou app que já existe) e apresentação (uma tela de conceitos que se explicam um a um). Use sempre que a pessoa quiser entender, ensinar ou apresentar uma interface, um produto, um sistema ou uma ideia de forma visual e navegável — "monta um tutorial", "faz um onboarding", "explica essa tela", "tour guiado", "walkthrough", "apresenta esse conceito de um jeito interativo", "guidetour" — mesmo sem a palavra "tour". Não use para manual em texto, slides ou vídeo.
---

# guidetour

Um tutorial em que tudo começa apagado e acende sob o clique. A pessoa aprende mexendo, no ritmo dela, e cada explicação aparece junto do elemento que explica. Serve tanto para ensinar um app quanto para apresentar uma ideia.

O que faz um guidetour funcionar não é o efeito visual (o motor já resolve), e sim o conteúdo: cada item precisa dizer, em poucas linhas, algo verdadeiro e útil sobre aquele elemento, na ordem em que a pessoa vai precisar. Gaste o esforço aí.

## O que vem na skill

| Caminho | Para quê |
|---|---|
| `assets/engine/guidetour.css` · `guidetour.js` | O motor: foco, pontos, cartão, tour, explorar, sem tutorial, link direto (`#gt-id`), progresso salvo no navegador, celular. Não reescreva; configure. |
| `scripts/montar.py` | Confere o roteiro contra a página e embute motor + roteiro num HTML só. |
| `assets/templates/apresentacao.html` | Ponto de partida do modo apresentação. |
| `references/roteiro.md` | Formato do roteiro (JSON) e marcação da página. Leia antes de escrever o primeiro item. |
| `references/metodo.md` | Como inventariar, escrever os itens e ordenar o tour. Leia antes de começar o conteúdo. |
| `references/modos.md` | Detalhes de réplica, sobreposição e apresentação. Leia a seção do modo escolhido. |
| `references/exemplo/malha.*` | Exemplo completo e testado: réplica de um app fictício de operação de entregas (duas telas, 24 itens, 8 paradas). Copie a qualidade, não o conteúdo. |

## Escolher o modo

| Modo | Quando | Página |
|---|---|---|
| **Réplica** | Ensinar um app que você não pode ou não quer modificar (de terceiros, instalado, em produção). | Você reconstrói a interface em HTML, fiel aos textos e à estrutura reais. |
| **Sobreposição** | A página já existe e é sua: um artefato, um HTML, um web-app em desenvolvimento. | Você marca os elementos reais (`data-gt`) ou aponta seletores, e injeta o motor. |
| **Apresentação** | Explicar uma ideia, conceito, arquitetura, proposta ou plano. | Você desenha uma tela de blocos (um mapa do conceito), e cada bloco vira um item. |

Na dúvida entre réplica e sobreposição, prefira sobreposição: fica fiel à interface por definição e não envelhece quando ela muda.

## Fluxo

1. **Inventário.** Junte as fontes antes de escrever uma linha: a interface real (abra no navegador e percorra cada tela; leia os textos da página), o código quando houver, a documentação, e o que já se sabe na conversa. Anote o estado real que puder verificar (o que está instalado, conectado, pendente). Detalhes em `references/metodo.md`.
2. **Mapa de itens.** Liste as telas (vistas) e, em cada uma, os elementos que mudam o que a pessoa faz: áreas, controles, indicadores, campos com consequência. Uma tela costuma ter de 6 a 20 itens. Elementos decorativos ficam de fora.
3. **Escrever os itens** no formato de `references/roteiro.md`: título, o que é, como usar (passos curtos), notas de custo, privacidade, requisito ou dica, e estado real quando verificado. Escreva do lado de quem usa.
4. **Ordenar o tour** pela jornada de uso, não pela posição na tela: orientação → o controle que aparece em tudo → o caminho principal → configurações e pendências. O tamanho segue a página: numa página pequena (até uns 12 itens) o tour passa por todos; num app com várias telas, de 15 a 35 paradas, e o resto fica para o modo explorar.
5. **Montar a página.** Réplica e apresentação: escreva o HTML com `data-gt="id"` nos elementos e `data-gt-view` nas telas. Sobreposição: marque ou mapeie seletores na página existente. Depois:
   `python3 -I scripts/montar.py pagina.html roteiro.json -o saida.html`
   Para um app em desenvolvimento: `--snippet` gera só o bloco a incluir.
6. **Conferir.** O script já confere campos, ids e telas; corrija os erros. Depois abra a saída no navegador, servida por HTTP local (arquivo direto às vezes não roda scripts): faça três paradas do tour, um clique no modo explorar, abra um link `#gt-id` e olhe a largura de celular. Uma olhada, não um ciclo.
7. **Entregar.** Padrão: publicar como Artifact privado (o HTML montado é autocontido). Alternativas: arquivo HTML, ou o snippet dentro do projeto. Na resposta: como abrir, os três modos em uma linha, as descobertas do inventário e o que ficou sem verificar. Numa réplica de produto de terceiros, diga sempre, mesmo sem publicar, que a cópia é para uso interno de quem pediu e não para distribuir.

## Regras de conteúdo

- **Fiel ao real.** Na réplica, use os textos e a ordem da interface verdadeira. Não invente botões nem comportamentos; quando não verificou o que um botão faz, descreva só o que dá para afirmar ("leva para…", "abre…").
- **Exemplos marcados.** Se precisar mostrar um estado que a interface vazia não mostra (uma conversa, um pedido de aprovação), marque o bloco como exemplo, visualmente.
- **Notas com função.** `cost` para o que gasta dinheiro ou créditos; `privacy` para o que sai do computador ou da conta e para onde; `req` para o que precisa existir antes; `tip` para o atalho que muda o uso. Uma nota que não muda decisão nenhuma sai.
- **Estado real só verificado.** O campo `status` ("No seu Mac", "Neste projeto") é o que torna o tutorial pessoal, e por isso precisa ter sido conferido de fato. Na dúvida, deixe sem.
- **Descobertas viram aviso.** Se no inventário você achar algo que a pessoa precisa saber (uma configuração de privacidade ligada por padrão, um requisito faltando), ponha no item e conte na entrega.
- **Dados pessoais de verdade não entram na réplica.** Nomes, telefones e e-mails de clientes (pessoas de fora) que vieram numa página exportada viram dados fictícios do mesmo formato, marcados como exemplo. Os textos da interface, os números e as configurações da própria conta continuam reais: são o que a equipe precisa reconhecer. Conte a troca na entrega.
- **Breve.** O cartão é lido em pé: `body` com uma ou duas frases, `steps` com até cinco passos curtos.
- **Idioma da pessoa.** Escreva no idioma da conversa; troque os rótulos do motor em `labels` se não for português.

## Visual

O motor traz um cartão claro sobre a página escurecida, que funciona por cima de qualquer tema. Para casar com uma marca ou um design system, sobrescreva as variáveis `--gt-*` (cores, fontes) no `:root` da página; não edite o CSS do motor. Na réplica, reproduza o visual do app com tokens próprios; na apresentação, dê ao conceito uma identidade com cuidado de design, sem cair nos visuais genéricos de IA.

## Limites

- Réplica de produto de terceiros é para uso interno de quem pediu: publique como privado e diga isso na entrega.
- Itens com HTML vêm do autor do roteiro; não cole conteúdo não confiável no roteiro.
- Páginas dentro de iframes de outros domínios não podem ser sobrepostas; use réplica.
