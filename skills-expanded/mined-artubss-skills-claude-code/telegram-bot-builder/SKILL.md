---
name: telegram-bot-builder
description: "Especialista em construir bots do Telegram que resolvem problemas reais - desde automação simples até bots complexos com IA. Abrange arquitetura de bots, a API de Bot do Telegram, experiência do usuário, estratégias de monetização e escalabilidade de bots para milhares de usuários. Use quando: telegram bot, bot api, automação telegram, chat bot telegram, tg bot."
source: vibeship-spawner-skills (Apache 2.0)
---

# Telegram Bot Builder

**Função**: Arquiteto de Bots do Telegram

Você constrói bots que as pessoas realmente usam diariamente. Você compreende que os bots devem parecer assistentes úteis, não interfaces desajeitadas. Você conhece o ecossistema do Telegram profundamente - o que é possível, o que é popular e o que gera receita. Você projeta conversas que parecem naturais.

## Capacidades

- Telegram Bot API
- Arquitetura de bots
- Design de comandos
- Teclados inline
- Monetização de bots
- Onboarding de usuários
- Analytics de bots
- Gerenciamento de webhooks

## Padrões

### Arquitetura de Bot

Estrutura para bots do Telegram mantíveis

**Quando usar**: Ao iniciar um novo projeto de bot

```python
## Arquitetura de Bot

### Opções de Stack
| Linguagem | Biblioteca | Melhor para |
|-----------|-----------|-------------|
| Node.js | telegraf | Maioria dos projetos |
| Node.js | grammY | TypeScript, moderno |
| Python | python-telegram-bot | Prototipagem rápida |
| Python | aiogram | Async, escalável |

### Configuração Básica do Telegraf
```javascript
import { Telegraf } from 'telegraf';

const bot = new Telegraf(process.env.BOT_TOKEN);

// Handlers de comando
bot.start((ctx) => ctx.reply('Bem-vindo!'));
bot.help((ctx) => ctx.reply('Como posso ajudar?'));

// Handler de texto
bot.on('text', (ctx) => {
  ctx.reply(`Você disse: ${ctx.message.text}`);
});

// Iniciar
bot.launch();

// Encerramento gracioso
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
```

### Estrutura do Projeto
```
telegram-bot/
├── src/
│   ├── bot.js           # Inicialização do bot
│   ├── commands/        # Handlers de comando
│   │   ├── start.js
│   │   ├── help.js
│   │   └── settings.js
│   ├── handlers/        # Handlers de mensagem
│   ├── keyboards/       # Teclados inline
│   ├── middleware/      # Autenticação, logging
│   └── services/        # Lógica de negócio
├── .env
└── package.json
```
```

### Teclados Inline

Interfaces de botões interativas

**Quando usar**: Ao construir fluxos de bot interativos

```python
## Teclados Inline

### Teclado Básico
```javascript
import { Markup } from 'telegraf';

bot.command('menu', (ctx) => {
  ctx.reply('Escolha uma opção:', Markup.inlineKeyboard([
    [Markup.button.callback('Opção 1', 'opt_1')],
    [Markup.button.callback('Opção 2', 'opt_2')],
    [
      Markup.button.callback('Sim', 'yes'),
      Markup.button.callback('Não', 'no'),
    ],
  ]));
});

// Lidar com cliques em botões
bot.action('opt_1', (ctx) => {
  ctx.answerCbQuery('Você escolheu Opção 1');
  ctx.editMessageText('Você selecionou Opção 1');
});
```

### Padrões de Teclado
| Padrão | Caso de Uso |
|--------|------------|
| Coluna única | Menus simples |
| Multi coluna | Sim/Não, paginação |
| Grade | Seleção de categoria |
| Botões de URL | Links, pagamentos |

### Paginação
```javascript
function getPaginatedKeyboard(items, page, perPage = 5) {
  const start = page * perPage;
  const pageItems = items.slice(start, start + perPage);

  const buttons = pageItems.map(item =>
    [Markup.button.callback(item.name, `item_${item.id}`)]
  );

  const nav = [];
  if (page > 0) nav.push(Markup.button.callback('◀️', `page_${page-1}`));
  if (start + perPage < items.length) nav.push(Markup.button.callback('▶️', `page_${page+1}`));

  return Markup.inlineKeyboard([...buttons, nav]);
}
```
```

### Monetização de Bots

Ganhando dinheiro com bots do Telegram

**Quando usar**: Ao planejar receita de bots

```javascript
## Monetização de Bots

### Modelos de Receita
| Modelo | Exemplo | Complexidade |
|--------|---------|-------------|
| Freemium | Básico grátis, premium pago | Médio |
| Assinatura | Acesso mensal | Médio |
| Por uso | Pagamento por ação | Baixo |
| Anúncios | Mensagens patrocinadas | Baixo |
| Afiliado | Recomendações de produtos | Baixo |

### Pagamentos do Telegram
```javascript
// Criar invoice
bot.command('buy', (ctx) => {
  ctx.replyWithInvoice({
    title: 'Acesso Premium',
    description: 'Desbloqueie todos os recursos',
    payload: 'premium_monthly',
    provider_token: process.env.PAYMENT_TOKEN,
    currency: 'USD',
    prices: [{ label: 'Premium', amount: 999 }], // $9.99
  });
});

// Lidar com pagamento bem-sucedido
bot.on('successful_payment', (ctx) => {
  const payment = ctx.message.successful_payment;
  // Ativar premium para usuário
  await activatePremium(ctx.from.id);
  ctx.reply('🎉 Premium ativado!');
});
```

### Estratégia Freemium
```
Plano gratuito:
- 10 usos por dia
- Recursos básicos
- Anúncios exibidos

Premium (R$ 25/mês):
- Usos ilimitados
- Recursos avançados
- Sem anúncios
- Suporte prioritário
```

### Limites de Uso
```javascript
async function checkUsage(userId) {
  const usage = await getUsage(userId);
  const isPremium = await checkPremium(userId);

  if (!isPremium && usage >= 10) {
    return { allowed: false, message: 'Limite diário atingido. Quer fazer upgrade?' };
  }
  return { allowed: true };
}
```
```

## Anti-Padrões

### ❌ Operações Bloqueantes

**Por que é ruim**: O Telegram tem limites de timeout. Os usuários pensam que o bot está morto. Experiência ruim. Requisições se acumulam.

**Em vez disso**: Reconheça imediatamente. Processe em background. Envie atualização quando concluído. Use indicador de digitação.

### ❌ Sem Tratamento de Erros

**Por que é ruim**: Usuários não recebem resposta. O bot parece quebrado. Pesadelo para debug. Confiança perdida.

**Em vez disso**: Handler de erro global. Mensagens de erro graciosas. Log de erros para debug. Rate limiting.

### ❌ Bot Spam

**Por que é ruim**: Usuários bloqueiam o bot. O Telegram pode banir. Experiência irritante. Retenção baixa.

**Em vez disso**: Respeite a atenção do usuário. Consolide mensagens. Permita controle de notificações. Qualidade sobre quantidade.

## Habilidades Relacionadas

Funciona bem com: `telegram-mini-app`, `backend`, `ai-wrapper-product`, `workflow-automation`