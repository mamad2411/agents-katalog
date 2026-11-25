---
name: pesquisa-e-plano
description: Pesquisa na web o mercado, os custos, a concorrência, as regras e a logística de um negócio local, confere os números reabrindo as fontes e transforma tudo num plano com decisões A/B/C e num teste curto de venda com meta e mínimo da semana escritos antes de começar. Use quando o usuário pedir pesquisa de mercado, preço, concorrentes, custo, margem, ponto de equilíbrio, plano de negócio ou plano de marketing para um negócio local, inclusive uma pesquisa rápida ou leve de preço e concorrência, "vale a pena?" e "quanto vou ganhar por mês". Carregue antes da primeira busca na web. Não monta perfis, posts nem anúncios.
---

# Pesquisa e plano

Esta skill só lê a web e escreve arquivos no projeto do usuário. Não publica, não gasta, não manda mensagem a ninguém. Se o usuário pedir uma dessas coisas, passe para a skill da etapa (`presenca-nas-redes`, `anuncios`, `conteudo`).

Nada é obrigatório para começar. Sem pesquisa na web, o plano usa só o que o dono informa e tudo leva a marca "não verificado". Sem subagentes, rodam as mesmas 3 frentes da versão leve, uma depois da outra. A versão leve sempre tem as 3 frentes e a conferência das fontes.

## Como falar com o dono (vale em todos os passos)

- Palavra de dono: sem termo interno da skill (veredito, piso, verificador, plano leve, cota); termo da Meta ou de marketing ganha explicação curta entre parênteses na primeira vez; campo técnico fica só no arquivo.
- No máximo 3 perguntas e 1 ou 2 decisões por mensagem. Lista longa vai para um arquivo; o chat traz o resumo e o passo de hoje.
- Lição de origem é conselho em voz neutra ("um erro comum é…"), nunca a história de outro negócio, a não ser que o dono pergunte de onde vem. Não fale de git com quem não pediu.
- Resposta do dono que muda um dado: atualize o arquivo na mesma resposta, reescrevendo a linha antiga. Detalhes em `../montar-negocio/references/falar-com-o-dono.md`.
- Antes de dizer "gravei" ou "anotei", grave e confira o arquivo. Arquivo só cita arquivo que existe. "Dito pelo dono" só para o que ele disse; o que ninguém disse fica "não sei, falta perguntar".
- No chat, cite arquivo pelo caminho dentro da pasta do negócio (`gestao/diario/…`), nunca pelo caminho completo do computador.
- Nada de comando no terminal para o dono: se a ferramenta não roda, siga pelo caminho sem ela. Script fica em `ferramentas/`, dentro da pasta do negócio. Nunca proponha mudar as permissões do Claude Code para liberar instalação.
- Se não há `negocio/estado.md` (o negócio não passou pela `montar-negocio`), termine a primeira resposta que entrega algo (pesquisa, peça, lançamento, texto) com esta frase, uma vez na conversa: "Quando quiser montar o resto do negócio (número, perfis, divulgação), é só pedir: monta meu negócio."

## Passos

1. **Sem ficha, ou ficha sem custos.** Se `negocio/ficha.md` não existe, pergunte o mínimo desta etapa, em blocos de até 3 perguntas por mensagem: o que vende ou que serviço presta, preços atuais, **cidade e bairro** (só para a pesquisa; nunca entram em peça pública), quanto pode gastar e em quanto tempo quer ver resultado. Pergunte também se há marca vizinha ou parente que não pode aparecer. Sempre que a ficha não tiver os custos, com ou sem ficha, pergunte: o custo do material por serviço ou produto, a taxa da maquininha, o tempo de cada serviço e os custos fixos (aluguel, cadeira). Grave a ficha antes de seguir. Se a pasta aberta tiver vários clientes, pergunte qual é o cliente (ou peça para abrir a sessão na pasta dele) e nunca crie ficha na pasta de cima. Sem a região, a pesquisa sai genérica.
2. **Escolha o tamanho e diga o custo antes.** Leve: 3 frentes (custos e preço, concorrência, canais de venda), cada uma com verificador. Completa: até 9 frentes, mais preço e finanças, crítico de completude, até 4 frentes de lacuna e síntese. Cada agente gasta do plano do Claude do usuário, e a completa usa muitos agentes e pode esgotar as buscas no meio. A leve é o padrão; a completa só com ok. Ao dono, diga em palavras simples: "um plano curto, que não custa dinheiro" ou "um plano completo, que usa bem mais do seu plano do Claude".
3. **Oriente as buscas antes.** Defina um limite de buscas por frente e uma reserva para a verificação (modelo em `references/frentes-de-pesquisa.md`). Não pergunte da cota ao dono: comece pela leve, a não ser que ele peça a completa. Cota acabando: pare, grave o que tem e liste o que ficou de fora. Nunca preencha com chute.
4. **Monte o bloco CONTEXTO** único para todos os pesquisadores: fatos da ficha, formato A/B/C, "todo número com fonte e data, ou marcado (estimativa) com a conta à mostra", proibido inventar concorrente, preço ou lei, preferência por fonte primária e do ano corrente, concorrência só por busca e páginas públicas.
5. **Rode as frentes** (em paralelo se a cota deixar; senão em lotes ou em sequência). Cada uma grava `pesquisa/NN-frente.md`. Antes do passo 8, confira que existem `pesquisa/01-custos-e-preco.md`, `pesquisa/02-concorrencia.md` e `pesquisa/03-canais.md`, cada um com "## Verificação". Se faltar um, rode a frente antes. Busca feita antes de carregar esta skill não substitui as frentes: grave-a como parte da frente certa e complete.
6. **Verificador cético** em cada frente grande: reabre as fontes, busca segunda fonte e dá veredito por afirmação (confirmado, corrigido, desatualizado, não verificável; na dúvida, não confirma). Corrige o arquivo e anexa "## Verificação" com as contagens. Ao dono, diga só "conferi as fontes" e o que ficou sem confirmar. Veja `references/verificador-cetico.md`.
7. **Crítico de completude** (só na completa): lista as lacunas por importância. Pesquise as 4 principais e diga quais ficaram de fora.
8. **Síntese** em `plano/plano.md`: resumo, números-chave, "onde as fontes não batem e qual número usamos", decisões A/B/C (exatamente uma recomendada, com custo e urgência), premissas (medido, dito pelo dono, fonte ou estimativa), riscos e pendências. Modelo em `references/sintese-e-decisoes.md`; contas em `references/custo-e-margem.md`. Sem os custos do dono, o plano mostra o preço, a concorrência e os canais, e diz o que falta para a conta do mês. Não mostre renda mensal com custo que o dono não deu.
9. **Teste curto de venda** em `plano/teste.md`: de 3 a 4 semanas, meta semanal, mínimo da semana, clientes novos de fora do círculo de conhecidos, origem de cada venda e o resultado (seguir, ajustar, parar) escrito antes de começar. Veja `references/teste-de-venda.md`.
10. **Decisões, poucas por vez.** Todas ficam em `plano/plano.md`. No chat, peça só as que travam o próximo passo, no máximo 2 por mensagem, cada uma com as opções e a recomendada; as outras esperam a hora de agir. Cada decisão é perguntada uma vez só. O dono responde por item e você grava em `negocio/decisoes.md`, inclusive quando ele vota contra a recomendação (execute o voto dele e registre a divergência). Página de votação só se o usuário pedir, e privada.

## O que é com você

- Passar preços e custos reais, e dizer o que o negócio aguenta gastar.
- Decidir cada A/B/C. Recomendação é do Claude; a decisão é sua.
- Simular o frete no aplicativo de entrega do seu celular: os apps não publicam tarifa, e a pesquisa na web não resolve isso.
- Conferir com a fonte oficial as regras de formalização, vigilância e rotulagem da sua cidade. O Claude resume o que achou e marca "confira".

## Custos

Esta skill não custa dinheiro: usa o seu plano do Claude. Se o plano indicar anúncio, o gasto real (com o imposto que a Meta cobra por cima) só entra com o ok da skill `anuncios`.

## Regras

- Número de pesquisa leva fonte e data, ou "(estimativa)" com a conta. Preço, prazo, estoque e lei nunca são inventados; o que faltar vira pergunta ao dono.
- Faixa de preço tirada de buscas cujas páginas você não abriu é pista, com o rótulo "pista". Não serve de base para dizer que o preço do dono está caro ou barato.
- O que o dono contou é "dito pelo dono", não "medido".
- Pesquisa de concorrente só por busca na web e páginas públicas. Nada de raspar perfil, entrar em conta ou seguir alguém. Site que bloqueia (erro 403, captcha) vira "não verificável", sem contornar.
- Nomes e números vindos de prints de conversa do dono não vão para os relatórios.
- O plano é hipótese. O teste mede. Nenhuma promessa de venda ou lucro.
- Depois de decidido, execute. Não mande outra rodada de votação sobre o que já foi decidido.

## Lições de origem (para você, Claude; não narre ao dono)

Vêm do caso de origem do plugin, uma doceria pequena. Amostra minúscula: é lição de processo, não estatística de mercado. Use como conselho em voz neutra; cite a origem só se o dono perguntar de onde vem o conselho.

- Das 182 afirmações que os verificadores checaram, 34 (cerca de 19%) estavam erradas, incluindo a margem de um produto. Sem verificador, o plano teria nascido com conta errada.
- A cota de busca acabou no meio: a concorrência ficou com 8 vendedores verificados em vez de 15 a 30. Oriente as buscas por frente.
- Preço de entrega por aplicativo não se pesquisa na web. Simular no celular real do dono.
- A meta do plano foi otimista: uma semana do teste fechou abaixo da meta. Trate a meta como hipótese e meça.
- Um plano de 90 dias virou um teste de 4 semanas com veredito escrito antes, porque o dono quis provar que vende antes de gastar tempo com burocracia. Isso é escolha do dono e fica em `negocio/decisoes.md`; adiar não elimina obrigação legal.
- O canal de cada venda foi rastreado com um código no texto pré-preenchido do link de WhatsApp, porque o link `wa.me` não aceita UTM.
- O dono recusou votar de novo as mesmas decisões. Uma rodada de votação, depois execução.

## Leia as references quando

- `references/frentes-de-pesquisa.md`: ao escolher frentes, montar o CONTEXTO e orçar buscas.
- `references/verificador-cetico.md`: ao verificar uma frente.
- `references/sintese-e-decisoes.md`: ao escrever `plano.md`, conciliar contradições e apresentar as decisões.
- `references/teste-de-venda.md`: ao escrever `teste.md` e definir os códigos de origem.
- `references/custo-e-margem.md`: ao calcular custo, margem, ponto de equilíbrio e quanto um anúncio pode custar por venda.
