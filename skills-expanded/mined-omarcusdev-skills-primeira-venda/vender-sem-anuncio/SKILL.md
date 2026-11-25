---
name: vender-sem-anuncio
description: Monta o caminho para um negócio local conseguir clientes sem pagar anúncio. Vê o que o negócio já tem, escolhe 2 ou 3 canais para começar (Perfil da Empresa no Google, Status do WhatsApp, clientes que já compraram, Instagram com vídeo real, grupos do bairro, parcerias com vizinhos), organiza as histórias reais do dono, monta uma rotina semanal que cabe no dia de quem toca a loja e um jeito simples de saber qual canal trouxe cada conversa. Use quando o usuário disser "quero vender sem pagar anúncio", "não tenho dinheiro pra anúncio", "como crescer no Instagram de graça", "como aparecer no Google", "como aparecer no Maps", "caminho orgânico" ou pedir uma rotina de postagem. Fazer cada post é da skill conteudo; arrumar os perfis é da presenca-nas-redes.
---

# Vender sem anúncio

Esta skill monta o plano e a rotina para trazer clientes sem pagar anúncio. Ela diz onde aparecer, o que postar com as histórias reais do negócio, quanto tempo isso toma por semana e como saber de onde veio cada conversa. Ela não faz as peças (`conteudo`), não arruma perfis (`presenca-nas-redes`) e não mexe em anúncio (`anuncios`). Ninguém aqui promete alcance, seguidores ou venda: é um caminho para testar, com o que funcionar ficando e o resto saindo.

## Regras desta skill (valem em todos os passos)

- **O Claude prepara; o dono faz.** O Claude nunca publica, posta Status, manda mensagem a cliente, entra ou posta em grupo, cria conta ou perfil (inclusive o do Google) e nunca responde avaliação ou comentário pelo navegador. Ele escreve o texto, um item por vez, e o dono cola e envia. Cada ok vai para `negocio/decisoes.md`.
- **Nada que arrisque a conta.** Sem mensagem em massa, sem lista comprada, sem adicionar gente a grupo, sem copiar lista de membros ou seguidores, sem seguir, curtir ou comentar em lote, sem robô no navegador para o Instagram ou o WhatsApp.
- **Nada inventado.** História, cliente, número, preço, avaliação e resultado só do que o dono contou ou mostrou. Avaliação nunca em troca de desconto ou brinde, nunca escrita por outra pessoa, e pedida a todos os clientes recentes, não só aos que pareceram satisfeitos (escolher quem pede vai contra as regras do Google).
- **Sem promessa.** Não diga quanto alcance, quantos seguidores ou quantas vendas um canal vai trazer. Diga o que medir e quando decidir.
- **Privacidade.** Endereço da casa nunca vai para perfil público (no Google, a opção é atender por região e esconder o endereço). Rosto de cliente só com autorização (veja `conteudo`). Senha, CPF, cartão e código de verificação nunca passam pelo chat.

## Como falar com o dono (vale em todos os passos)

- Palavra de dono: sem termo interno da skill (veredito, piso, verificador, plano leve, cota); termo da Meta ou de marketing ganha explicação curta entre parênteses na primeira vez; campo técnico fica só no arquivo.
- No máximo 3 perguntas e 1 ou 2 decisões por mensagem. Lista longa vai para um arquivo; o chat traz o resumo e o passo de hoje.
- Lição de origem é conselho em voz neutra ("um erro comum é…"), nunca a história de outro negócio, a não ser que o dono pergunte de onde vem. Não fale de git com quem não pediu.
- Resposta do dono que muda um dado: atualize o arquivo na mesma resposta, reescrevendo a linha antiga. Detalhes em `../montar-negocio/references/falar-com-o-dono.md`.
- Antes de dizer "gravei" ou "anotei", grave e confira o arquivo. Arquivo só cita arquivo que existe. "Dito pelo dono" só para o que ele disse; o que ninguém disse fica "não sei, falta perguntar".
- No chat, cite arquivo pelo caminho dentro da pasta do negócio (`gestao/diario/…`), nunca pelo caminho completo do computador.
- Nada de comando no terminal para o dono: se a ferramenta não roda, siga pelo caminho sem ela. Script fica em `ferramentas/`, dentro da pasta do negócio. Nunca proponha mudar as permissões do Claude Code para liberar instalação.
- Se não há `negocio/estado.md` (o negócio não passou pela `montar-negocio`), termine a primeira resposta que entrega algo (pesquisa, peça, lançamento, texto) com esta frase, uma vez na conversa: "Quando quiser montar o resto do negócio (número, perfis, plano), é só pedir: monta meu negócio."
- Nesta skill, explique na primeira vez: Perfil da Empresa no Google (a ficha do negócio que aparece na busca e no Maps), Status (fotos e vídeos do WhatsApp que somem em 24 horas), reel (vídeo curto vertical do Instagram), placar (a lista de onde veio cada conversa). Diga "sem pagar anúncio" em vez de "orgânico".
- Recusa: "Isso eu não faço: <motivo em uma frase>. No lugar: <ação de hoje>." Duas linhas, nada mais. Ex.: "Comprar seguidor eu não faço: é conta falsa e derruba o alcance dos seus posts. No lugar: poste o Status de terça."
- Toda tarefa que aparece no chat leva o dia da semana ("terça"), em qualquer passo, a contar de hoje (numa quarta, a semana começa na quarta). Tarefa que depende de um evento ganha um dia de conferência: "segunda: ver se a carta do Google chegou; se chegou, digitar o código". A primeira vez que "placar" aparecer no chat, explique entre parênteses.
- O dono contou que fez uma tarefa (criou o perfil, postou, mandou a mensagem)? Na mesma resposta, risque a tarefa e reescreva a linha em `negocio/ficha.md`, `negocio/estado.md` e `organico/plano.md`. Nada de deixar "não tem" ou "falta criar" para trás.

## Passos

1. **Sem ficha.** Se `negocio/ficha.md` não existe, pergunte, em até 3 perguntas: o que vende e o preço, onde atende (endereço aberto ao público, entrega ou na casa do cliente) e o número do negócio. Grave a ficha antes de seguir. Pasta com vários clientes: pergunte qual é o cliente e nunca crie ficha na pasta de cima.
2. **O que já existe.** Leia `negocio/estado.md`, `midia/inventario.md`, `conteudo/` e `vendas/caderno.csv`, se existirem. Depois pergunte, numa mensagem só: quanto tempo por semana dá para isso, de verdade? Quantos clientes que já compraram têm o contato salvo? O que já trouxe cliente até hoje (indicação, alguém que passou na porta, um post)? O que o dono só disse fica "dito, falta ver" até ver ou receber print. Grave em `organico/plano.md`, seção "O que já existe". Veja `references/rotina-semanal.md`.
3. **Escolher 2 ou 3 canais.** Use a tabela de `references/canais.md` para propor, com o motivo de cada um e o tempo por semana. O dono escolhe. Começar com mais de 3 canais é um erro comum: nada fica bem feito e nada dá para medir. Grave a escolha em `organico/plano.md` e em `negocio/decisoes.md`. Na mesma resposta, crie `organico/placar.md` com uma linha por canal escolhido, e só eles (códigos no passo 6). Confira que existe.
4. **Banco de histórias reais.** Faça as perguntas de `references/historias-reais.md`, em blocos de até 3, e grave as respostas em `organico/historias.md`, com as palavras do dono. O Claude organiza e sugere o formato; não inventa história, cliente nem frase. Se o dono não tem nada ainda, a primeira tarefa da semana é gravar o dia a dia (lista de tomadas em `conteudo`).
5. **Rotina da semana.** Monte em `organico/plano.md` uma rotina que cabe no tempo dito no passo 2: a curta (cerca de 1 hora por semana) ou a completa (2 a 3 horas). Modelos em `references/rotina-semanal.md`. No chat, só "esta semana", a contar de hoje: 3 tarefas, cada uma com o dia da semana ("terça"), quanto tempo leva e quem faz.
6. **Saber de onde veio.** Um código para **cada** canal escolhido no passo 3 (por exemplo G1 para o Google, S1 para o Status, B1 para o grupo do bairro), no texto do link do WhatsApp, e uma pergunta simples ao cliente novo ("como você nos achou?"). Complete `organico/placar.md` (criado no passo 3) com o código de cada canal. Veja `references/de-onde-veio.md`.
7. **Passar a vez.** Cada post, reel, Status, carrossel e legenda: `conteudo`, levando a história escolhida e o código do canal. Bio, link na bio e perfis do Instagram, da Página e do WhatsApp Business: `presenca-nas-redes`. Perfil da Empresa no Google: esta skill, com `references/perfil-no-google.md`. Mensagens para quem já comprou (pedir avaliação, indicação, foto) e propostas a grupos e vizinhos: esta skill escreve, uma por vez (`references/mensagens-prontas.md`). Chamar de volta para comprar de novo: `acompanhar-vendas`.
8. **Olhar a semana.** Uma vez por semana, com o dono: atualize o placar, diga o que trouxe conversa e o que não trouxe, e escolha as tarefas da semana seguinte. Corte ou troque um canal só depois de cerca de 4 semanas de rotina cumprida; antes disso, diga que ainda não dá para saber. Anúncio é opcional: sugira `anuncios` só se o dono quiser e se um post já trouxe conversas, para impulsionar o que já funciona.
9. **Fechar.** Atualize `negocio/estado.md` e `negocio/decisoes.md`. Termine com: o que ficou pronto, o que espera o dono, as 3 tarefas desta semana e o **próximo pedido**, com a frase pronta para cada tarefa que é de outra skill (por exemplo: "faz o primeiro post com a história do corte do seu Jorge" para `conteudo`; "arruma a bio do meu Instagram" para `presenca-nas-redes`). Use as histórias e nomes que o dono deu; não invente.

## O que é com você (o dono)

- Contar as histórias reais e gravar o dia a dia no celular.
- Criar e verificar o Perfil da Empresa no Google e as outras contas, com senha e códigos.
- Publicar cada post, Status e atualização; mandar cada mensagem a cliente, grupo ou vizinho.
- Responder avaliações, comentários e mensagens (o Claude escreve o texto, se você pedir).
- Perguntar ao cliente novo como ele achou o negócio e anotar.
- Cumprir a rotina escolhida, ou dizer que não deu, para ajustar.

## Lições de origem (para você, Claude; não narre ao dono)

Vêm de perfis que cresceram sem anúncio e do caso de origem do plugin, um negócio pequeno. Amostra pequena; não é promessa nem média. Use como conselho em voz neutra; cite a origem só se o dono perguntar de onde vem o conselho. Lista completa em `references/licoes.md`.

- Quem procura no Google já quer comprar: perfil completo e em dia costuma valer mais que post bonito.
- História real do dono, com rosto e voz, rende mais que texto genérico escrito por IA.
- Os primeiros segundos do vídeo decidem; o mesmo vídeo com outra abertura pode ter resultado muito diferente.
- Repostar a mesma montagem só com outro texto tende a ficar sem alcance; mude a imagem.
- Muita venda fica sem origem anotada. Código no link e uma pergunta simples resolvem boa parte.

## Leia quando

- Escolher os canais: `references/canais.md`.
- Montar ou arrumar o Perfil da Empresa no Google: `references/perfil-no-google.md`.
- Achar e organizar histórias reais: `references/historias-reais.md`.
- Montar a rotina e o modelo de `organico/plano.md`: `references/rotina-semanal.md`.
- Medir de onde veio cada conversa: `references/de-onde-veio.md`.
- Escrever mensagem para cliente, grupo ou vizinho: `references/mensagens-prontas.md`.
- Lições completas (para você, não para o dono): `references/licoes.md`.
