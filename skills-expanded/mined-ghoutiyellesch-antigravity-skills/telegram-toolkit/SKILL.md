---
name: telegram-toolkit
description: Consolidated toolkit for telegram. Covers telegram-mini-app, telegram-automation, telegram-bot-builder
---
# Telegram Toolkit

## Core Capabilities
# Telegram Toolkit

# Telegram Mini App

**Role**: Telegram Mini App Architect

You build apps where 800M+ Telegram users already are. You understand
the Mini App ecosystem is exploding - games, DeFi, utilities, social
apps. You know TON blockchain and how to monetize with crypto. You
design for the Telegram UX paradigm, not traditional web.

## Capabilities

- Telegram Web App API
- Mini App architecture
- TON Connect integration
- In-app payments
- User authentication via Telegram
- Mini App UX patterns
- Viral Mini App mechanics
- TON blockchain integration

## Patterns

### Mini App Setup

Getting started with Telegram Mini Apps

**When to use**: When starting a new Mini App

```javascript
## Mini App Setup

### Basic Structure
```html
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://telegram.org/js/telegram-web-app.js"></script>
</head>
<body>
  <script>
    const tg = window.Telegram.WebApp;
    tg.ready();
    tg.expand();

    // User data
    const user = tg.initDataUnsafe.user;
    console.log(user.first_name, user.id);
  </script>
</body>
</html>
```

### React Setup
```jsx
// hooks/useTelegram.js
export function useTelegram() {
  const tg = window.Telegram?.WebApp;

  return {
    tg,
    user: tg?.initDataUnsafe?.user,
    queryId: tg?.initDataUnsafe?.query_id,
    expand: () => tg?.expand(),
    close: () => tg?.close(),
    ready: () => tg?.ready(),
  };
}

// App.jsx
function App() {
  const { tg, user, expand, ready } = useTelegram();

  useEffect(() => {
    ready();
    expand();
  }, []);

  return <div>Hello, {user?.first_name}</div>;
}
```

### Bot Integration
```javascript
// Bot sends Mini App
bot.command('app', (ctx) => {
  ctx.reply('Open the app:', {
    reply_markup: {
      inline_keyboard: [[
        { text: '🚀 Open App', web_app: { url: 'https://your-app.com' } }
      ]]
    }
  });
});
```
```

### TON Connect Integration

Wallet connection for TON blockchain

**When to use**: When building Web3 Mini Apps

```python
## TON Connect Integration

### Setup
```bash
npm install @tonconnect/ui-react
```

### React Integration
```jsx
import { TonConnectUIProvider, TonConnectButton } from '@tonconnect/ui-react';

// Wrap app
function App() {
  return (
    <TonConnectUIProvider manifestUrl="https://your-app.com/tonconnect-manifest.json">
      <MainApp />
    </TonConnectUIProvider>
  );
}

// Use in components
function WalletSection() {
  return (
    <TonConnectButton />
  );
}
```

### Manifest File
```json
{
  "url": "https://your-app.com",
  "name": "Your Mini App",
  "iconUrl": "https://your-app.com/icon.png"
}
```

### Send TON Transaction
```jsx
import { useTonConnectUI } from '@tonconnect/ui-react';

function PaymentButton({ amount, to }) {
  const [tonConnectUI] = useTonConnectUI();

  const handlePay = async () => {
    const transaction = {
      validUntil: Math.floor(Date.now() / 1000) + 60,
      messages: [{
        address: to,
        amount: (amount * 1e9).toString(), // TON to nanoton
      }]
    };

    await tonConnectUI.sendTransaction(transaction);
  };

  return <button onClick={handlePay}>Pay {amount} TON</button>;
}
```
```

### Mini App Monetization

Making money from Mini Apps

**When to use**: When planning Mini App revenue

```javascript
## Mini App Monetization

### Revenue Streams
| Model | Example | Potential |
|-------|---------|-----------|
| TON payments | Premium features | High |
| In-app purchases | Virtual goods | High |
| Ads (Telegram Ads) | Display ads | Medium |
| Referral | Share to earn | Medium |
| NFT sales | Digital collectibles | High |

### Telegram Stars (New!)
```javascript
// In your bot
bot.command('premium', (ctx) => {
  ctx.replyWithInvoice({
    title: 'Premium Access',
    description: 'Unlock all features',
    payload: 'premium',
    provider_token: '', // Empty for Stars
    currency: 'XTR', // Telegram Stars
    prices: [{ label: 'Premium', amount: 100 }], // 100 Stars
  });
});
```

### Viral Mechanics
```jsx
// Referral system
function ReferralShare() {
  const { tg, user } = useTelegram();
  const referralLink = `https://t.me/your_bot?start=ref_${user.id}`;

  const share = () => {
    tg.openTelegramLink(
      `https://t.me/share/url?url=${encodeURIComponent(referralLink)}&text=Check this out!`
    );
  };

  return <button onClick={share}>Invite Friends (+10 coins)</button>;
}
```

### Gamification for Retention
- Daily rewards
- Streak bonuses
- Leaderboards
- Achievement badges
- Referral bonuses
```

## Anti-Patterns

### ❌ Ignoring Telegram Theme

**Why bad**: Feels foreign in Telegram.
Bad user experience.
Jarring transitions.
Users don't trust it.

**Instead**: Use tg.themeParams.
Match Telegram colors.
Use native-feeling UI.
Test in both light/dark.

### ❌ Desktop-First Mini App

**Why bad**: 95% of Telegram is mobile.
Touch targets too small.
Doesn't fit in Telegram UI.
Scrolling issues.

**Instead**: Mobile-first always.
Test on real phones.
Touch-friendly buttons.
Fit within Telegram frame.

### ❌ No Loading States

**Why bad**: Users think it's broken.
Poor perceived performance.
High exit rate.
Confusion.

**Instead**: Show skeleton UI.
Loading indicators.
Progressive loading.
Optimistic updates.

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Not validating initData from Telegram | high | ## Validating initData |
| TON Connect not working on mobile | high | ## TON Connect Mobile Issues |
| Mini App feels slow and janky | medium | ## Mini App Performance |
| Custom buttons instead of MainButton | medium | ## Using MainButton Properly |

## Related Skills

Works well with: `telegram-bot-builder`, `frontend`, `blockchain-defi`, `viral-generator-builder`

---

# Telegram Automation via Rube MCP

Automate Telegram operations through Composio's Telegram toolkit via Rube MCP.

## Prerequisites

- Rube MCP must be connected (RUBE_SEARCH_TOOLS available)
- Active Telegram connection via `RUBE_MANAGE_CONNECTIONS` with toolkit `telegram`
- Always call `RUBE_SEARCH_TOOLS` first to get current tool schemas
- Telegram Bot Token required (created via @BotFather)

## Setup

**Get Rube MCP**: Add `https://rube.app/mcp` as an MCP server in your client configuration. No API keys needed — just add the endpoint and it works.

1. Verify Rube MCP is available by confirming `RUBE_SEARCH_TOOLS` responds
2. Call `RUBE_MANAGE_CONNECTIONS` with toolkit `telegram`
3. If connection is not ACTIVE, follow the returned auth link to configure the Telegram bot
4. Confirm connection status shows ACTIVE before running any workflows

## Core Workflows

### 1. Send Messages

**When to use**: User wants to send text messages to a Telegram chat

**Tool sequence**:
1. `TELEGRAM_GET_ME` - Verify bot identity and connection [Prerequisite]
2. `TELEGRAM_GET_CHAT` - Get chat details and verify access [Optional]
3. `TELEGRAM_SEND_MESSAGE` - Send a text message [Required]

**Key parameters**:
- `chat_id`: Numeric chat ID or channel username (e.g., '@channelname')
- `text`: Message text content
- `parse_mode`: 'HTML' or 'MarkdownV2' for formatting
- `disable_notification`: Send silently without notification sound
- `reply_to_message_id`: Message ID to reply to

**Pitfalls**:
- Bot must be a member of the chat/group to send messages
- MarkdownV2 requires escaping special characters: `_*[]()~>#+-=|{}.!`
- HTML mode supports limited tags: `<b>`, `<i>`, `<code>`, `<pre>`, `<a>`
- Messages have a 4096 character limit; split longer content

### 2. Send Photos and Documents

**When to use**: User wants to share images or files in a Telegram chat

**Tool sequence**:
1. `TELEGRAM_SEND_PHOTO` - Send an image [Optional]
2. `TELEGRAM_SEND_DOCUMENT` - Send a file/document [Optional]

**Key parameters**:
- `chat_id`: Target chat ID
- `photo`: Photo URL or file_id (for SEND_PHOTO)
- `document`: Document URL or file_id (for SEND_DOCUMENT)
- `caption`: Optional caption for the media

**Pitfalls**:
- Photo captions have a 1024 character limit
- Document captions also have a 1024 character limit
- Files up to 50MB can be sent via bot API
- Photos are compressed by Telegram; use SEND_DOCUMENT for uncompressed images

### 3. Manage Chats

**When to use**: User wants to get chat information or manage chat settings

**Tool sequence**:
1. `TELEGRAM_GET_CHAT` - Get detailed chat information [Required]
2. `TELEGRAM_GET_CHAT_ADMINISTRATORS` - List chat admins [Optional]
3. `TELEGRAM_GET_CHAT_MEMBERS_COUNT` - Get member count [Optional]
4. `TELEGRAM_EXPORT_CHAT_INVITE_LINK` - Generate invite link [Optional]

**Key parameters**:
- `chat_id`: Target chat ID or username

**Pitfalls**:
- Bot must be an administrator to export invite links
- GET_CHAT returns different fields for private chats vs groups vs channels
- Member count may be approximate for very large groups
- Admin list does not include regular members

### 4. Edit and Delete Messages

**When to use**: User wants to modify or remove previously sent messages

**Tool sequence**:
1. `TELEGRAM_EDIT_MESSAGE` - Edit a sent message [Optional]
2. `TELEGRAM_DELETE_MESSAGE` - Delete a message [Optional]

**Key parameters**:
- `chat_id`: Chat where the message is located
- `message_id`: ID of the message to edit or delete
- `text`: New text content (for edit)

**Pitfalls**:
- Bots can only edit their own messages
- Messages can only be deleted within 48 hours of sending
- In groups, bots with delete permissions can delete any message
- Editing a message removes its 'edited' timestamp history

### 5. Forward Messages and Get Updates

**When to use**: User wants to forward messages or retrieve recent updates

**Tool sequence**:
1. `TELEGRAM_FORWARD_MESSAGE` - Forward a message to another chat [Optional]
2. `TELEGRAM_GET_UPDATES` - Get recent bot updates/messages [Optional]
3. `TELEGRAM_GET_CHAT_HISTORY` - Get chat message history [Optional]

**Key parameters**:
- `from_chat_id`: Source chat for forwarding
- `chat_id`: Destination chat for forwarding
- `message_id`: Message to forward
- `offset`: Update offset for GET_UPDATES
- `limit`: Number of updates to retrieve

**Pitfalls**:
- Forwarded messages show the original sender attribution
- GET_UPDATES returns a limited window of recent updates
- Chat history access may be limited by bot permissions and chat type
- Use offset to avoid processing the same update twice

### 6. Manage Bot Commands

**When to use**: User wants to set or update bot command menu

**Tool sequence**:
1. `TELEGRAM_SET_MY_COMMANDS` - Set the bot's command list [Required]
2. `TELEGRAM_ANSWER_CALLBACK_QUERY` - Respond to inline button presses [Optional]

**Key parameters**:
- `commands`: Array of command objects with `command` and `description`
- `callback_query_id`: ID of the callback query to answer

**Pitfalls**:
- Commands must start with '/' and be lowercase
- Command descriptions have a 256 character limit
- Callback queries must be answered within 10 seconds or they expire
- Setting commands replaces the entire command list

## Common Patterns

### Chat ID Resolution

**From username**:
```
1. Use '@username' format as chat_id (for public channels/groups)
2. For private chats, numeric chat_id is required
3. Call GET_CHAT with username to retrieve numeric ID
```

**From GET_UPDATES**:
```
1. Call TELEGRAM_GET_UPDATES
2. Extract chat.id from message objects
3. Use numeric chat_id in subsequent calls
```

### Message Formatting

- Use `parse_mode: 'HTML'` for `<b>bold</b>`, `<i>italic</i>`, `<code>code</code>`
- Use `parse_mode: 'MarkdownV2'` for `*bold*`, `_italic_`, `` `code` ``
- Escape special chars in MarkdownV2: `_ * [ ] ( ) ~ > # + - = | { } . !`
- Omit parse_mode for plain text without formatting

## Known Pitfalls

**Bot Permissions**:
- Bots must be added to groups/channels to interact
- Admin permissions needed for: deleting messages, exporting invite links, managing members
- Bots cannot initiate conversations; users must start them first

**Rate Limits**:
- 30 messages per second to the same group
- 20 messages per minute to the same user in groups
- Bulk operations should implement delays between calls
- API returns 429 Too Many Requests when limits are hit

**Chat Types**:
- Private chat: One-on-one with the bot
- Group: Multi-user chat (bot must be added)
- Supergroup: Enhanced group with admin features
- Channel: Broadcast-only (bot must be admin to post)

**Message Limits**:
- Text messages: 4096 characters max
- Captions: 1024 characters max
- File uploads: 50MB max via bot API
- Inline keyboard buttons: 8 per row

## Quick Reference

| Task | Tool Slug | Key Params |
|------|-----------|------------|
| Verify bot | TELEGRAM_GET_ME | (none) |
| Send message | TELEGRAM_SEND_MESSAGE | chat_id, text, parse_mode |
| Send photo | TELEGRAM_SEND_PHOTO | chat_id, photo, caption |
| Send document | TELEGRAM_SEND_DOCUMENT | chat_id, document, caption |
| Edit message | TELEGRAM_EDIT_MESSAGE | chat_id, message_id, text |
| Delete message | TELEGRAM_DELETE_MESSAGE | chat_id, message_id |
| Forward message | TELEGRAM_FORWARD_MESSAGE | chat_id, from_chat_id, message_id |
| Get chat info | TELEGRAM_GET_CHAT | chat_id |
| Get chat admins | TELEGRAM_GET_CHAT_ADMINISTRATORS | chat_id |
| Get member count | TELEGRAM_GET_CHAT_MEMBERS_COUNT | chat_id |
| Export invite link | TELEGRAM_EXPORT_CHAT_INVITE_LINK | chat_id |
| Get updates | TELEGRAM_GET_UPDATES | offset, limit |
| Get chat history | TELEGRAM_GET_CHAT_HISTORY | chat_id |
| Set bot commands | TELEGRAM_SET_MY_COMMANDS | commands |
| Answer callback | TELEGRAM_ANSWER_CALLBACK_QUERY | callback_query_id |

---

# Telegram Bot Builder

**Role**: Telegram Bot Architect

You build bots that people actually use daily. You understand that bots
should feel like helpful assistants, not clunky interfaces. You know
the Telegram ecosystem deeply - what's possible, what's popular, and
what makes money. You design conversations that feel natural.

## Capabilities

- Telegram Bot API
- Bot architecture
- Command design
- Inline keyboards
- Bot monetization
- User onboarding
- Bot analytics
- Webhook management

## Patterns

### Bot Architecture

Structure for maintainable Telegram bots

**When to use**: When starting a new bot project

```python
## Bot Architecture

### Stack Options
| Language | Library | Best For |
|----------|---------|----------|
| Node.js | telegraf | Most projects |
| Node.js | grammY | TypeScript, modern |
| Python | python-telegram-bot | Quick prototypes |
| Python | aiogram | Async, scalable |

### Basic Telegraf Setup
```javascript
import { Telegraf } from 'telegraf';

const bot = new Telegraf(process.env.BOT_TOKEN);

// Command handlers
bot.start((ctx) => ctx.reply('Welcome!'));
bot.help((ctx) => ctx.reply('How can I help?'));

// Text handler
bot.on('text', (ctx) => {
  ctx.reply(`You said: ${ctx.message.text}`);
});

// Launch
bot.launch();

// Graceful shutdown
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
```

### Project Structure
```
telegram-bot/
├── src/
│   ├── bot.js           # Bot initialization
│   ├── commands/        # Command handlers
│   │   ├── start.js
│   │   ├── help.js
│   │   └── settings.js
│   ├── handlers/        # Message handlers
│   ├── keyboards/       # Inline keyboards
│   ├── middleware/      # Auth, logging
│   └── services/        # Business logic
├── .env
└── package.json
```
```

### Inline Keyboards

Interactive button interfaces

**When to use**: When building interactive bot flows

```python
## Inline Keyboards

### Basic Keyboard
```javascript
import { Markup } from 'telegraf';

bot.command('menu', (ctx) => {
  ctx.reply('Choose an option:', Markup.inlineKeyboard([
    [Markup.button.callback('Option 1', 'opt_1')],
    [Markup.button.callback('Option 2', 'opt_2')],
    [
      Markup.button.callback('Yes', 'yes'),
      Markup.button.callback('No', 'no'),
    ],
  ]));
});

// Handle button clicks
bot.action('opt_1', (ctx) => {
  ctx.answerCbQuery('You chose Option 1');
  ctx.editMessageText('You selected Option 1');
});
```

### Keyboard Patterns
| Pattern | Use Case |
|---------|----------|
| Single column | Simple menus |
| Multi column | Yes/No, pagination |
| Grid | Category selection |
| URL buttons | Links, payments |

### Pagination
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

### Bot Monetization

Making money from Telegram bots

**When to use**: When planning bot revenue

```javascript
## Bot Monetization

### Revenue Models
| Model | Example | Complexity |
|-------|---------|------------|
| Freemium | Free basic, paid premium | Medium |
| Subscription | Monthly access | Medium |
| Per-use | Pay per action | Low |
| Ads | Sponsored messages | Low |
| Affiliate | Product recommendations | Low |

### Telegram Payments
```javascript
// Create invoice
bot.command('buy', (ctx) => {
  ctx.replyWithInvoice({
    title: 'Premium Access',
    description: 'Unlock all features',
    payload: 'premium_monthly',
    provider_token: process.env.PAYMENT_TOKEN,
    currency: 'USD',
    prices: [{ label: 'Premium', amount: 999 }], // $9.99
  });
});

// Handle successful payment
bot.on('successful_payment', (ctx) => {
  const payment = ctx.message.successful_payment;
  // Activate premium for user
  await activatePremium(ctx.from.id);
  ctx.reply('🎉 Premium activated!');
});
```

### Freemium Strategy
```
Free tier:
- 10 uses per day
- Basic features
- Ads shown

Premium ($5/month):
- Unlimited uses
- Advanced features
- No ads
- Priority support
```

### Usage Limits
```javascript
async function checkUsage(userId) {
  const usage = await getUsage(userId);
  const isPremium = await checkPremium(userId);

  if (!isPremium && usage >= 10) {
    return { allowed: false, message: 'Daily limit reached. Upgrade?' };
  }
  return { allowed: true };
}
```
```

## Anti-Patterns

### ❌ Blocking Operations

**Why bad**: Telegram has timeout limits.
Users think bot is dead.
Poor experience.
Requests pile up.

**Instead**: Acknowledge immediately.
Process in background.
Send update when done.
Use typing indicator.

### ❌ No Error Handling

**Why bad**: Users get no response.
Bot appears broken.
Debugging nightmare.
Lost trust.

**Instead**: Global error handler.
Graceful error messages.
Log errors for debugging.
Rate limiting.

### ❌ Spammy Bot

**Why bad**: Users block the bot.
Telegram may ban.
Annoying experience.
Low retention.

**Instead**: Respect user attention.
Consolidate messages.
Allow notification control.
Quality over quantity.

## Related Skills

Works well with: `telegram-mini-app`, `backend`, `ai-wrapper-product`, `workflow-automation`

---
