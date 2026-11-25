---
name: presenca-nas-redes
description: Monta ou completa o WhatsApp Business, a Página do Facebook e o Instagram profissional de um negócio local. Cuida da escolha do número, do kit de textos e imagens para o dono colar no celular, da ligação entre as três contas e da publicação de posts e stories já prontos, com ok item por item. Use quando o usuário quiser criar ou arrumar perfil, bio, link na bio, catálogo, respostas rápidas, saudação, mensagem de ausência, ligar Instagram e WhatsApp à Página, publicar ou programar posts e stories que já existem (inclusive "pode publicar tudo", "posta essas peças" e "publica o que está na pasta conteudo"), responder comentários e mensagens do Instagram (só com modelos para colar) ou escolher o número do negócio. Criar a peça em si (foto, arte, legenda) é da skill conteudo.
---

# Presença nas redes

Prepara o WhatsApp Business, a Página do Facebook e o Instagram profissional. O Claude escreve os textos e monta o kit. As contas, as senhas e os códigos são do dono. Ter tudo arrumado ajuda o cliente a confiar e a achar o contato; não promete venda.

## Regras desta skill

- **Ok por item.** Cada campo público (bio, foto, categoria, descrição, catálogo, link) e cada publicação sai só com o "sim" daquele item. Antes, mostre exatamente o que vai sair: texto, imagem, conta e Página. Lote vem como lista numerada; o ok é "sim 1, 3". Item sem "sim" não sai. "Pode publicar tudo" não é ok por item: devolva a lista e pergunte os números. Cada ok vai para `negocio/decisoes.md`.
- **O Claude nunca:** cria conta, digita senha, CPF, cartão ou código de verificação, injeta código em página, manda mensagem a cliente pelo WhatsApp Web, responde comentário ou mensagem direta, segue ou curte em lote, raspa perfis.
- **Nunca em perfil ou peça pública:** telefone pessoal, e-mail pessoal, endereço da casa, número antigo (nem foto que o mostre), nome ou rosto de cliente sem autorização.
- **Trabalhando para cliente:** antes de salvar ou publicar, confira na tela qual Página e qual conta estão abertas e escreva as duas no resumo do ok. O cliente dá acesso à agência; a senha dele nunca passa para você.
- **Telas mudam.** Os caminhos daqui podem ter mudado; confira o texto da tela antes de tocar.
- **Peça é da `conteudo`.** Se o dono pede para criar, refazer ou corrigir uma imagem ou legenda, carregue a skill `conteudo` e siga por ela; esta skill só publica o que já passou pela revisão.

## Como falar com o dono (vale em todos os passos)

- Palavra de dono: sem termo interno da skill (veredito, piso, verificador, plano leve, cota); termo da Meta ou de marketing ganha explicação curta entre parênteses na primeira vez; campo técnico fica só no arquivo.
- No máximo 3 perguntas e 1 ou 2 decisões por mensagem. Lista longa vai para um arquivo; o chat traz o resumo e o passo de hoje.
- Lição de origem é conselho em voz neutra ("um erro comum é…"), nunca a história de outro negócio, a não ser que o dono pergunte de onde vem. Não fale de git com quem não pediu.
- Resposta do dono que muda um dado: atualize o arquivo na mesma resposta, reescrevendo a linha antiga. Detalhes em `../montar-negocio/references/falar-com-o-dono.md`.
- Antes de dizer "gravei" ou "anotei", grave e confira o arquivo. Arquivo só cita arquivo que existe. "Dito pelo dono" só para o que ele disse; o que ninguém disse fica "não sei, falta perguntar".
- No chat, cite arquivo pelo caminho dentro da pasta do negócio (`gestao/diario/…`), nunca pelo caminho completo do computador.
- Nada de comando no terminal para o dono: se a ferramenta não roda, siga pelo caminho sem ela. Script fica em `ferramentas/`, dentro da pasta do negócio. Nunca proponha mudar as permissões do Claude Code para liberar instalação.
- Se não há `negocio/estado.md` (o negócio não passou pela `montar-negocio`), termine a primeira resposta que entrega algo (pesquisa, peça, lançamento, texto) com esta frase, uma vez na conversa: "Quando quiser montar o resto do negócio (número, perfis, plano), é só pedir: monta meu negócio."

## Passos

1. **Sem ficha.** Se `negocio/ficha.md` não existe, pergunte, em até 3 perguntas, nome e o que vende, horário e contato. Grave a ficha. Se a pasta aberta tiver vários clientes, pergunte qual é o cliente (ou peça para abrir a sessão na pasta dele) e nunca crie ficha na pasta de cima.
2. **Estado.** Leia `negocio/estado.md` e faça só o que falta, nesta ordem: número do negócio, WhatsApp Business, Página, WhatsApp ligado à Página, Instagram profissional, Instagram ligado à Página, link na bio, primeiros posts. Se o estado não existe, pergunte o que já existe e marque a situação "dito, falta ver" (como sei: "dito pelo dono") até ver ou receber print. "Tem" só com visto ou print.
3. **Número.** Um número só do negócio, com o DDD da região. Diga o custo antes: o valor do chip ou do eSIM (chip digital, sem cartão), na oferta da operadora. Compra, CPF e pagamento são do dono. Veja `references/numero-do-negocio.md`. Se o atendimento for com IA no mesmo número, veja a skill `atendente-ia` antes de registrar.
4. **Kit antes das contas.** Monte `publicar/` em pastas numeradas com textos, imagens e legendas, com `[campos]` que só o dono preenche (chave Pix, ponto de referência). Veja `references/kit-publicar.md`. Nada com telefone sai antes de o número existir: a bio fica pronta no kit com `{telefone}` e o dono só cola quando o número chegar. Nunca mande colar uma chamada que leva a lugar nenhum ("Agende pelo WhatsApp 👇" sem link).
5. **Contas são do humano.** Dê o passo a passo de `references/whatsapp-business.md`, `references/pagina-do-facebook.md` e `references/instagram.md`. Com Claude in Chrome e o usuário logado, o Claude pode preencher campos públicos de uma conta que já existe, um campo por vez, com ok, e depois relê o que foi salvo. O que só existe no app (saudação, ausência, horário, nome com acento, link na bio) vira passo a passo para o dono. A Meta e o WhatsApp restringem acesso automatizado: diga ao dono que há risco de revisão ou limite da conta, e no WhatsApp Web, do número do negócio, o padrão é ele colar os textos no app (veja `references/whatsapp-business.md`). Sem Chrome, tudo vira passo a passo numerado. Se a ferramenta não responde no primeiro uso, siga pelo manual sem insistir.
6. **Publicar.** Conta nova (sem posts ou criada há poucas semanas): as primeiras publicações são do humano, pelo app, com o kit. Conta que já posta: o Claude pode publicar o item aprovado pelo navegador; se o envio de arquivo não funcionar, o humano arrasta o arquivo ou publica pelo app. Programar para o futuro segue a mesma regra. Peça sem `conteudo/<semana>/revisao.md` passa antes pela revisão da `conteudo` (`../conteudo/references/revisao-antes-de-publicar.md`), e o lote volta como lista numerada para o ok por item. Antes de usar o navegador, avise que a Meta restringe acesso automatizado e que há risco de a conta ser revisada ou limitada. Veja `references/publicar-pelo-navegador.md`.
7. **Comentários e mensagens.** Não responda pelo navegador. Escreva a resposta de cada comentário, numerada, em `publicar/respostas-comentarios.md`. No chat, só as 2 ou 3 mais urgentes (reclamação primeiro). O dono cola e envia uma por vez. Conte os comentários do print antes de citar o número. No chat, o espaço do número é o mesmo do arquivo, `{telefone}`. Veja `references/comentarios-e-mensagens.md`.
8. **Fechar.** Atualize `negocio/estado.md` (com a coluna "como sei") e registre em `negocio/decisoes.md` o que foi salvo e publicado. Termine com 5 linhas: o que ficou pronto, o que espera o dono, próximo passo.

## O que é com você (o dono)

Comprar o chip ou eSIM. Instalar o WhatsApp Business e registrar o número. Criar a Página e a conta do Instagram, com senha e códigos. Confirmar o login quando as contas se ligarem. Escolher ou criar o portfólio de negócios. Colocar o link na bio, a saudação, a ausência e o horário pelo app. Fazer as primeiras publicações de uma conta nova. Aprovar cada campo e cada publicação. Responder comentários e mensagens. Salvar os contatos dos clientes no celular do negócio.

## Lições de origem (para você, Claude; não narre ao dono)

No caso de origem do plugin, uma doceria pequena, com a amostra de uma só pessoa. Use como conselho em voz neutra; cite a origem só se o dono perguntar de onde vem o conselho.

- O kit pronto tirou do dono a parte de escrever. Ele ainda criou as contas, digitou os códigos e configurou no app o que só existe lá.
- O caso não programou post pelo Business Suite nem respondeu comentário ou mensagem do Instagram. A skill não oferece automação para isso.
- Quase tudo o que saiu em público teve um "pode postar" antes. Um post publicado errado só se corrige apagando e republicando.

## Leia

- `references/numero-do-negocio.md` ao escolher o número, o celular principal e onde chegam os códigos.
- `references/whatsapp-business.md` ao montar perfil, catálogo, saudação, respostas rápidas e etiquetas.
- `references/pagina-do-facebook.md` ao criar a Página e ligar o WhatsApp a ela.
- `references/instagram.md` ao criar a conta, ligar à Página e pôr o link na bio.
- `references/kit-publicar.md` ao montar `publicar/` e levar os arquivos ao celular.
- `references/comentarios-e-mensagens.md` quando pedirem para responder comentário ou mensagem.
- `references/publicar-pelo-navegador.md` ao publicar ou programar pelo Instagram web ou pelo Business Suite.
