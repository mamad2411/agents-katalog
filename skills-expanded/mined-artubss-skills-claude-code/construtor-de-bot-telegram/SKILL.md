---
name: Construtor de Bot Telegram
description: Esta skill deve ser usada quando o usuário pedir para "criar um bot Telegram", "construir um chatbot Telegram", "configurar webhook Telegram", "adicionar teclados inline a um bot", "manipular callback queries do Telegram", "implementar pagamentos Telegram", "enviar mídia via bot Telegram", "configurar comandos de bot Telegram", "fazer deploy de um bot Telegram", ou mencionar Telegram Bot API, tokens de bot telegram, getUpdates, setWebhook, ou frameworks de bot como node-telegram-bot-api, grammy, python-telegram-bot, ou aiogram. Fornece orientação abrangente para construir bots Telegram prontos para produção com Node.js e Python.
---

# Construtor de Bot Telegram

Orientação abrangente para construir bots Telegram usando a Bot API (v9.4). Cobre os ecossistemas Node.js e Python com padrões prontos para produção em autenticação, mensagens, teclados, manipulação de mídia, pagamentos, modo inline, webhooks e deployment.

## Quando Usar Esta Skill

Use esta skill quando:
- Construir um novo bot Telegram do zero
- Integrar mensagens Telegram a uma aplicação existente
- Configurar webhooks ou long polling para atualizações do bot
- Criar menus interativos com teclados inline e callback queries
- Manipular mídia (fotos, vídeos, documentos, stickers)
- Implementar Telegram Payments ou Telegram Stars
- Construir funcionalidade de modo inline
- Gerenciar grupos, canais ou tópicos de fórum via bot
- Fazer deploy de bots em produção (Docker, PM2, serverless)

## Conceitos Principais

### Autenticação

Todo bot possui um token único obtido em [@BotFather](https://t.me/BotFather). Formato do token: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`.

Todas as chamadas à API vão para: `https://api.telegram.org/bot<TOKEN>/METHOD_NAME`

```bash
# arquivo .env
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
```

Armazene o token em variáveis de ambiente. Nunca commite para o código-fonte.

### Recebendo Atualizações: Polling vs Webhook

**Long Polling** (`getUpdates`) - Mais simples, sem HTTPS obrigatório, ideal para desenvolvimento:

```javascript
// Node.js com node-telegram-bot-api
const bot = new TelegramBot(process.env.BOT_TOKEN, { polling: true });
```

```python
# Python com python-telegram-bot
app = Application.builder().token(os.getenv("BOT_TOKEN")).build()
app.run_polling()
```

**Webhook** (`setWebhook`) - Melhor para produção, latência menor, requer HTTPS (portas 443, 80, 88 ou 8443):

```javascript
bot.setWebHook('https://yourdomain.com/webhook', { secret_token: SECRET });
```

Escolha polling para desenvolvimento e bots pequenos. Escolha webhooks para deployments em produção com alto tráfego.

### Tipos de Mensagem e Formatação

Envie texto com `sendMessage`. Modos de parse suportados:

- **HTML**: `<b>negrito</b>`, `<i>itálico</i>`, `<code>código</code>`, `<pre>bloco</pre>`, `<a href="url">link</a>`, `<tg-spoiler>spoiler</tg-spoiler>`
- **MarkdownV2**: `*negrito*`, `_itálico_`, `` `código` ``, ` ```bloco``` `, `[link](url)`, `||spoiler||`. Requer escape: `_*[]()~>#+-=|{}.!`

Prefira HTML para escape mais fácil. Use MarkdownV2 quando formatação mais simples for suficiente.

### Teclados e Elementos Interativos

**Teclado Inline** - Botões anexados às mensagens:

```javascript
bot.sendMessage(chatId, 'Escolha:', {
  reply_markup: {
    inline_keyboard: [
      [{ text: 'Opção A', callback_data: 'a' }, { text: 'Opção B', callback_data: 'b' }],
      [{ text: 'Visite o Site', url: 'https://example.com' }]
    ]
  }
});
```

**Teclado de Resposta** - Teclado customizado abaixo do campo de entrada:

```javascript
bot.sendMessage(chatId, 'Escolha:', {
  reply_markup: {
    keyboard: [[{ text: '📊 Estatísticas' }, { text: '⚙️ Configurações' }]],
    resize_keyboard: true,
    one_time_keyboard: true
  }
});
```

Manipule pressionamentos de botões inline com `callback_query`. O campo `callback_data` é limitado a 64 bytes. Sempre chame `answerCallbackQuery` para descartar o indicador de carregamento.

### Enviando Mídia

```javascript
// Foto (file_id, URL ou upload)
bot.sendPhoto(chatId, 'https://example.com/photo.jpg', { caption: 'Uma foto' });

// Documento
bot.sendDocument(chatId, fs.createReadStream('./file.pdf'), { caption: 'Relatório' });

// Álbum (2-10 itens)
bot.sendMediaGroup(chatId, [
  { type: 'photo', media: 'https://example.com/1.jpg', caption: 'Primeiro' },
  { type: 'photo', media: 'https://example.com/2.jpg' }
]);
```

Três formas de especificar arquivos: `file_id` (reutilizar upload anterior), URL HTTP (Telegram faz download), ou upload multipart. Limites de arquivo: 50MB upload, 20MB download via Bot API.

### Estado de Conversa

Para interações em múltiplas etapas (registro, formulários, wizards), mantenha estado de conversa por chat:

- **Node.js**: Use um `Map` ou Redis para rastrear `{ step, data }` por `chatId`
- **Python**: Use `ConversationHandler` de `python-telegram-bot` (máquina de estado integrada)

Veja `reference/patterns_and_examples.md` para implementações completas de fluxo de conversa.

### Tratamento de Erros

Manipule cenários de erro comuns:
- **429 Too Many Requests**: Leia `retry_after` da resposta, aguarde e tente novamente
- **403 Forbidden**: Bot foi bloqueado pelo usuário ou removido do chat
- **400 Bad Request**: Parâmetros inválidos (verifique campo `description`)
- **409 Conflict**: Outra instância de bot usando o mesmo token com polling

Limites de taxa: ~30 mensagens/segundo para chats diferentes, ~20 mensagens/minuto para mesmo grupo. Implemente backoff exponencial para retries.

### Comandos de Bot

Registre comandos visíveis no menu do Telegram:

```javascript
bot.setMyCommands([
  { command: 'start', description: 'Iniciar o bot' },
  { command: 'help', description: 'Mostrar ajuda' },
  { command: 'settings', description: 'Configurações do bot' }
]);
```

Comandos podem ser direcionados para chats, usuários ou idiomas específicos usando `BotCommandScope`.

## Padrões Comuns

### Início Rápido (Node.js)

```bash
mkdir my-bot && cd my-bot
npm init -y
npm install node-telegram-bot-api dotenv
echo "BOT_TOKEN=your_token_here" > .env
```

### Início Rápido (Python)

```bash
mkdir my-bot && cd my-bot
pip install python-telegram-bot python-dotenv
echo "BOT_TOKEN=your_token_here" > .env
```

### Bibliotecas Populares

| Linguagem | Biblioteca | Estilo | Melhor Para |
|---|---|---|---|
| Node.js | `node-telegram-bot-api` | Baseada em callback | Bots simples, protótipos rápidos |
| Node.js | `grammy` | Baseada em middleware | Bots complexos, plugins |
| Node.js | `telegraf` | Baseada em middleware | Ecossistema maduro |
| Python | `python-telegram-bot` | Baseada em handler | Completa, conversas |
| Python | `aiogram` | Async-first | Bots de alto desempenho async |

### Categorias de Método-Chave da API

| Categoria | Métodos-Chave |
|---|---|
| Mensagens | `sendMessage`, `sendPhoto`, `sendVideo`, `sendDocument`, `editMessageText`, `deleteMessage` |
| Teclados | `InlineKeyboardMarkup`, `ReplyKeyboardMarkup`, `answerCallbackQuery` |
| Gerenciamento de Chat | `getChat`, `banChatMember`, `promoteChatMember`, `setChatPermissions` |
| Arquivos | `getFile`, `sendMediaGroup`, `sendDocument` |
| Modo Inline | `answerInlineQuery` com tipos `InlineQueryResult*` |
| Pagamentos | `sendInvoice`, `answerPreCheckoutQuery` (use `currency: "XTR"` para Telegram Stars) |
| Configuração de Bot | `setMyCommands`, `setMyDescription`, `setWebhook` |

## Opções de Deployment

- **PM2**: `pm2 start bot.js --name telegram-bot` - Gerenciador de processo com auto-restart
- **Docker**: Deployment containerizado com `docker-compose`
- **Serverless**: Handler webhook como função Vercel/AWS Lambda
- **VPS**: Deployment direto com serviço systemd

Veja `reference/patterns_and_examples.md` para configurações de Docker, PM2 e deployment serverless.

## Checklist de Segurança

- Armazene `BOT_TOKEN` em variáveis de ambiente
- Valide `X-Telegram-Bot-Api-Secret-Token` em endpoints webhook
- Verifique IDs de usuário para comandos de admin
- Implemente rate limiting por usuário
- Sanitize entrada do usuário antes de armazenar em banco de dados
- Use HTTPS para todos os endpoints webhook
- Restrinja `allowed_updates` apenas aos tipos necessários

## Arquivos de Referência

Para documentação detalhada da API e padrões de implementação, consulte:

- **[`reference/api_methods.md`](./reference/api_methods.md)** - Lista completa de 100+ métodos da Bot API organizados por categoria (mensagens, gerenciamento de chat, stickers, pagamentos, modo inline, jogos, tópicos de fórum, presentes, passport e mais)
- **[`reference/api_types.md`](./reference/api_types.md)** - Lista completa de 200+ tipos da Bot API com todos os campos (Update, Message, Chat, User, teclados, tipos de mídia, tipos de pagamento, membros de chat, reações e mais)
- **[`reference/patterns_and_examples.md`](./reference/patterns_and_examples.md)** - Padrões de implementação prontos para produção para Node.js e Python incluindo: teclados inline, webhooks, manipulação de mídia, gerenciamento de estado de conversa, integração de banco de dados, painéis de admin, suporte multilíngue, deployment Docker/PM2/serverless, pagamentos com Telegram Stars e modo inline

Ao construir um bot, comece com SKILL.md para conceitos principais, depois carregue o arquivo de referência apropriado para informações detalhadas da API ou padrões de implementação conforme necessário.