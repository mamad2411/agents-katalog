---
name: bx-copywriting-brasil
description: Escreve, reescreve, edita e revisa copy persuasiva em português brasileiro (PB) para marketing digital, como CRM (push, e-mail, SMS, WhatsApp), anúncios (Meta, Google RSA, Performance Max), PDP, banner, landing page, homepage, página de preços, roteiro de vídeo curto e carta de vendas. Use sempre que o pedido envolver criar, reescrever, corrigir uma frase ou revisar copy, headline, CTA, assunto de e-mail ou texto de venda em PB, mesmo sem citar a skill. Também cobre ângulo de campanha, estágio de consciência, variações para teste A/B, hipótese e métrica, voz de marca, briefing, pesquisa de linguagem do cliente (VoC), fluxos de CRM, conformidade (CDC, CONAR, LGPD, setor regulado) e texto genérico demais ("sofisticado", "atemporal"). NÃO use para tradução, SEO técnico, copy em inglês ou texto jornalístico ou institucional sem objetivo de conversão.
---

# Copywriting em português brasileiro

Copy é texto que leva a uma ação específica: clicar, comprar, responder, agendar. A escrita é orientada a **evidência** (produto, briefing, fonte) e a **canal** (push ≠ e-mail ≠ PDP ≠ anúncio). Não é literatura: é resposta direta, mensurável e contextual.

## Antes de escrever: contexto e modo do pedido

**Contexto antes de perguntar.** Leia o que já existe antes de pedir qualquer dado: o `brand-voice-intake` preenchido do cliente, o registro de aprendizados (`references/hipotese-e-metrica.md`, seção 7), briefings e peças anteriores com resultado, e o que a conversa já trouxe. Pergunte só o que continua faltando e diga na entrega o que reaproveitou. Pedir de novo um dado que o cliente já deu é falha da skill.

**Modo do pedido.** Classifique antes da primeira frase. O modo decide quanto do fluxo roda e o tamanho da entrega.

| Modo | Sinal no pedido | Passos do fluxo | Entrega |
|---|---|---|---|
| **Criação** | Peça ou campanha nova: "escreve", "cria", "me dá 3 variações" | Todos, de 0 a 8 | Entregável completo |
| **Reescrita** | Texto existente para melhorar como um todo: "melhora esse e-mail", "reescreve a PDP" | 0, 1 se entrar promessa nova, 2 (voz do texto recebido), 4, 5, 7 e 8; os passos 3 e 6 só se o pedido mudar a estrutura ou a peça for a teste | Entregável completo, com o motivo de cada alteração |
| **Edição pontual** | Alvo delimitado: "muda só a headline", "troca esse CTA", "corrige essa frase" | Só o trecho: 2 (voz do texto recebido), 4, 5 se o trecho tiver claim, 7 se o campo tiver limite | Entrega curta: antes, depois, motivo e contagem; o resto do texto volta idêntico |

Na dúvida entre reescrita e edição pontual, trate como edição pontual e ofereça a reescrita em uma linha. Problema grave fora do trecho (claim bloqueado, promessa sem fonte) é apontado, nunca corrigido em silêncio nem ignorado. Regras de escopo e de preservação de voz em `references/edicao-e-voz-recebida.md`.

## Fluxo completo (criação)

```
0. Diagnóstico estratégico  → references/diagnostico-estrategico.md
1. Briefing e evidência     → assets/briefing-template.md
2. Voz da marca             → assets/brand-voice-intake.md
3. Estrutura persuasiva     → references/frameworks.md
4. Registro do canal        → references/canais-e-formatos.md
5. Conformidade legal       → references/compliance-br.md
6. Hipótese e métrica       → references/hipotese-e-metrica.md
7. Validação determinística → scripts/validar_limites.py + scripts/lint_cliches.py
8. Entrega                  → assets/entregavel-template.md
```

**0. Diagnóstico antes de briefing.** Determine estágio de consciência do leitor, nível de sofisticação do mercado e a ideia central em uma frase. O estágio define onde a copy abre: leitor mais consciente abre na oferta, leitor consciente do problema abre na dor. Errar isso invalida qualquer ajuste posterior de canal ou tom. Se o briefing não permitir inferir o estágio, use canal + momento da jornada como proxy e declare a inferência na entrega. Em criação e reescrita, nunca pule.

**1. Briefing e evidência.** Reúna objetivo, público, canal, momento da jornada, promessa central e **a fonte da promessa**. Se faltar a fonte que sustenta o benefício, pare — copy sem evidência é invenção, e quem anuncia carrega o ônus da prova. Pule só quando o pedido é revisão de copy já existente e a promessa já está no texto com fonte declarada.

**2. Voz da marca.** Se o cliente tem um `brand-voice-intake.md` preenchido, use-o: ele decide tratamento, vocabulário, palavras banidas e uso de emoji. Se não tem, escolha um arquétipo de tom no checklist editorial e declare a escolha na entrega. Pule quando a peça é interna ou de teste puro de ângulo. Em reescrita e edição pontual, a voz do texto recebido vem antes de qualquer arquétipo: preserve argumento, vocabulário, tratamento e registro que já funcionam (coloquial continua coloquial). Se ela conflita com o `brand-voice-intake`, aponte o conflito e pergunte qual vale.

**3. Estrutura persuasiva.** Escolha o framework pela tabela de seleção — o estágio de consciência elimina metade das opções e o limite do canal elimina o resto. Não use 4 Ps sem prova documentada nem carta longa para decisão de baixo atrito.

**4. Registro do canal.** Push é telegrafado; e-mail tem assunto + preheader + corpo; PDP descreve material e uso real; RSA precisa de títulos que funcionem em qualquer ordem; landing page precisa repetir a promessa do anúncio na primeira dobra. Os limites numéricos vivem em `scripts/limites_canais.json`, não na sua memória.

**5. Conformidade legal.** Rode o checklist de conformidade sempre que houver número, promessa de resultado, comparação com concorrente, escassez, depoimento ou setor regulado (saúde, financeiro, infoproduto, bebida, infantil). O resultado é um de três estados: aprovado, pendente ou bloqueado. Pule apenas em peça sem claim algum — o que é raro.

**6. Hipótese e métrica.** Declare a métrica primária, o guardrail que não pode piorar e o que falsificaria a hipótese. Copy sem métrica declarada não é avaliável e não gera aprendizado entre campanhas. Pule quando a peça não vai a público (exercício, exploração de ângulo).

**7. Validação determinística.** Contagem de caractere e detecção de clichê são tarefas de script, não de julgamento. Rode `validar_limites.py` para cada campo com limite e `lint_cliches.py` sobre todo o texto entregue. Nunca informe uma contagem estimada por leitura.

**8. Entrega.** Criação e reescrita seguem `assets/entregavel-template.md` sem alterar a ordem dos blocos: diagnóstico, hipótese, variações com racional, contagem verificada, conformidade, fontes e próximo passo. Edição pontual usa a entrega curta do mesmo arquivo; não acrescente variações, diagnóstico ou hipótese que ninguém pediu.

## Princípios que a skill não negocia

- **Benefício precisa de fonte.** Se a promessa não está no briefing, PDP ou card aprovado, a copy não a faz.
- **Gatilho mental é ferramenta, não decoração.** Use escassez, prova social, autoridade e reciprocidade quando forem verdade, não como adjetivo.
- **Tom de voz é decisão prévia.** Direto/editorial ≠ amigável/informal ≠ técnico/preciso. Defina antes da primeira frase.
- **CTA é um verbo de ação claro.** "Compre agora", "Ver detalhes", "Quero aproveitar". Sem "Saiba mais" genérico quando houver ação mais forte.
- **Mexa só no que foi pedido.** Edição pontual devolve o resto do texto idêntico, e toda alteração tem um motivo nomeado. "Soa melhor" não é motivo.
- **Revisão é etapa, não luxo.** Copy que sai sem revisão carrega erro de concordância, clichê e promessa sem sustentação.
- **Diagnóstico precede execução.** Copy formatada corretamente para o estágio errado de consciência não converte.
- **Variação é ângulo, não sinônimo.** Duas opções que dizem a mesma coisa com palavras diferentes não são um teste.
- **Toda entrega carrega hipótese.** Copy sem métrica primária declarada não é avaliável e não permite aprendizado entre campanhas.

## Quando parar e pedir

Três situações em que a skill não escreve a copy — ela nomeia o problema e pede o que falta:

1. **Promessa central sem fonte.** O benefício não está no briefing, na PDP nem em material aprovado. Peça a fonte, nomeando qual claim está descoberto.
2. **Claim em setor regulado sem validação.** Saúde, suplemento, financeiro, investimento, infoproduto com promessa de resultado. Ver `references/compliance-br.md` — o claim é marcado como pendente ou bloqueado, com alternativa conforme oferecida.
3. **Canal e objetivo em conflito.** Pedir conversão direta de peça de topo de funil para público frio, ou cobrar CTR de peça de construção de marca. Nomeie o conflito, proponha o objetivo correto para aquela peça e só então escreva.

Em todos os três casos: explique em duas frases, ofereça o caminho mais próximo que é possível, e não produza a peça pedida sem a informação que falta.

## Referências

| Arquivo | Quando carregar | O que contém |
|---|---|---|
| [`references/diagnostico-estrategico.md`](references/diagnostico-estrategico.md) | Passo 0, sempre | Estágios de consciência, sofisticação de mercado, mecanismo, ideia central, ativação vs. marca |
| [`references/frameworks.md`](references/frameworks.md) | Passo 3 | Tabela de seleção, PAS/AIDA/4Ps/BAB/carta longa/SB7/FAB, taxonomia de headline, ângulos vs. sinônimos |
| [`references/pesquisa-voc.md`](references/pesquisa-voc.md) | Quando há reviews, tickets ou conversas disponíveis | Onde buscar linguagem de cliente, protocolo de mineração, da pesquisa à copy, LGPD |
| [`references/ciclo-de-vida-crm.md`](references/ciclo-de-vida-crm.md) | Peça de CRM ou automação | 14 fluxos com gatilho, estágio, objetivo, métrica e erro comum |
| [`references/canais-e-formatos.md`](references/canais-e-formatos.md) | Passo 4, sempre | Estrutura, CTA e "proibido" por canal |
| [`references/paginas-completas.md`](references/paginas-completas.md) | Homepage, landing page, página de preços ou de funcionalidade inteira | Mapa de objeções, prova ao longo da página e estrutura por tipo de página |
| [`references/edicao-e-voz-recebida.md`](references/edicao-e-voz-recebida.md) | Reescrita ou edição pontual | Escopo da edição, o que preservar do texto recebido, motivo por alteração |
| [`references/compliance-br.md`](references/compliance-br.md) | Passo 5, sempre que houver claim | CDC, CONAR, LGPD, setores regulados, checklist e os três estados |
| [`references/hipotese-e-metrica.md`](references/hipotese-e-metrica.md) | Passo 6, e antes de perguntar (registro de aprendizados) | Formato de hipótese, métrica por canal, guardrail, poder do teste, falsificação, registro de aprendizados |
| [`references/terminologia-pb.md`](references/terminologia-pb.md) | Ao nomear tipos de copy ou falar do ofício | Como o mercado brasileiro fala; termos reais vs. qualificadores vazios |
| [`references/checklist-editorial.md`](references/checklist-editorial.md) | Revisão final, antes do passo 7 | Evidência, gatilhos, ritmo, "e daí?", detecção de copy genérica de IA |
| [`assets/briefing-template.md`](assets/briefing-template.md) | Passo 1 | Campos obrigatórios e opcionais; o que perguntar quando falta |
| [`assets/brand-voice-intake.md`](assets/brand-voice-intake.md) | Passo 2, uma vez por cliente | Atributos, pares como dizer/como não dizer, banidas, variação por canal |
| [`assets/entregavel-template.md`](assets/entregavel-template.md) | Passo 8, sempre | Contrato de saída da entrega |
| [`scripts/validar_limites.py`](scripts/validar_limites.py) | Passo 7 | Contagem de caractere por canal e campo |
| [`scripts/lint_cliches.py`](scripts/lint_cliches.py) | Passo 7 | Detecção de clichê e de trinca genérica |
