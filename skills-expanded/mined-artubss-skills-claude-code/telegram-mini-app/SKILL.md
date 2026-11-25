---
name: telegram-mini-app
description: "Especialista em construir Telegram Mini Apps (TWA) - aplicações web que rodam dentro do Telegram com experiência nativa. Abrange o ecossistema TON, Telegram Web App API, pagamentos, autenticação de usuários e construção de mini apps virais que monetizam. Use quando: telegram mini app, TWA, telegram web app, TON app, mini app."
source: vibeship-spawner-skills (Apache 2.0)
---

# Telegram Mini App

**Papel**: Arquiteto de Telegram Mini App

Você constrói apps onde 800M+ usuários do Telegram já estão. Você entende que o ecossistema de Mini Apps está explodindo - jogos, DeFi, utilitários, apps sociais. Você conhece blockchain TON e como monetizar com criptografia. Você projeta para o paradigma UX do Telegram, não para web tradicional.

## Capacidades

- Telegram Web App API
- Arquitetura de Mini App
- Integração TON Connect
- Pagamentos in-app
- Autenticação de usuários via Telegram
- Padrões de UX de Mini App
- Mecânicas de Mini App viral
- Integração blockchain TON

## Padrões

### Configuração de Mini App

Iniciando um novo Mini App

**Quando usar**: Ao iniciar um novo Mini App

```javascript
// Configuração Básica
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

    // Dados do usuário
    const user = tg.initDataUnsafe.user;
    console.log(user.first_name, user.id);
  </script>
</body>
</html>
```

### Configuração React
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

  return <div>Olá, {user?.first_name}</div>;
}
```

### Integração com Bot
```javascript
// Bot envia Mini App
bot.command('app', (ctx) => {
  ctx.reply('Abra o app:', {
    reply_markup: {
      inline_keyboard: [[
        { text: '🚀 Abrir App', web_app: { url: 'https://your-app.com' } }
      ]]
    }
  });
});
```
```

### Integração TON Connect

Conexão de carteira para blockchain TON

**Quando usar**: Ao construir Mini Apps Web3

```python
## Integração TON Connect

### Configuração
```bash
npm install @tonconnect/ui-react
```

### Integração React
```jsx
import { TonConnectUIProvider, TonConnectButton } from '@tonconnect/ui-react';

// Envolva o app
function App() {
  return (
    <TonConnectUIProvider manifestUrl="https://your-app.com/tonconnect-manifest.json">
      <MainApp />
    </TonConnectUIProvider>
  );
}

// Use em componentes
function WalletSection() {
  return (
    <TonConnectButton />
  );
}
```

### Arquivo de Manifest
```json
{
  "url": "https://your-app.com",
  "name": "Your Mini App",
  "iconUrl": "https://your-app.com/icon.png"
}
```

### Enviar Transação TON
```jsx
import { useTonConnectUI } from '@tonconnect/ui-react';

function PaymentButton({ amount, to }) {
  const [tonConnectUI] = useTonConnectUI();

  const handlePay = async () => {
    const transaction = {
      validUntil: Math.floor(Date.now() / 1000) + 60,
      messages: [{
        address: to,
        amount: (amount * 1e9).toString(), // TON para nanoton
      }]
    };

    await tonConnectUI.sendTransaction(transaction);
  };

  return <button onClick={handlePay}>Pagar {amount} TON</button>;
}
```
```

### Monetização de Mini App

Ganhando dinheiro com Mini Apps

**Quando usar**: Ao planejar receita de Mini App

```javascript
## Monetização de Mini App

### Fluxos de Receita
| Modelo | Exemplo | Potencial |
|-------|---------|-----------|
| Pagamentos TON | Recursos premium | Alto |
| Compras in-app | Bens virtuais | Alto |
| Anúncios (Telegram Ads) | Exibição de anúncios | Médio |
| Referência | Compartilhar para ganhar | Médio |
| Vendas NFT | Colecionáveis digitais | Alto |

### Telegram Stars (Novo!)
```javascript
// No seu bot
bot.command('premium', (ctx) => {
  ctx.replyWithInvoice({
    title: 'Acesso Premium',
    description: 'Desbloqueie todos os recursos',
    payload: 'premium',
    provider_token: '', // Vazio para Stars
    currency: 'XTR', // Telegram Stars
    prices: [{ label: 'Premium', amount: 100 }], // 100 Stars
  });
});
```

### Mecânicas Virais
```jsx
// Sistema de referência
function ReferralShare() {
  const { tg, user } = useTelegram();
  const referralLink = `https://t.me/your_bot?start=ref_${user.id}`;

  const share = () => {
    tg.openTelegramLink(
      `https://t.me/share/url?url=${encodeURIComponent(referralLink)}&text=Confira isto!`
    );
  };

  return <button onClick={share}>Convide Amigos (+10 moedas)</button>;
}
```

### Gamificação para Retenção
- Recompensas diárias
- Bônus de sequência
- Placar de líderes
- Emblemas de conquistas
- Bônus de referência
```

## Anti-Padrões

### ❌ Ignorar Tema do Telegram

**Por que é ruim**: Parece estranho dentro do Telegram.
Experiência do usuário ruim.
Transições abruptas.
Usuários não confiam.

**Em vez disso**: Use tg.themeParams.
Combine cores do Telegram.
Use UI de aspecto nativo.
Teste em modo claro/escuro.

### ❌ Mini App Primeiro para Desktop

**Por que é ruim**: 95% do Telegram é mobile.
Alvos de toque muito pequenos.
Não se encaixa na UI do Telegram.
Problemas de scroll.

**Em vez disso**: Mobile-first sempre.
Teste em telefones reais.
Botões amigáveis ao toque.
Adeque-se ao frame do Telegram.

### ❌ Sem Estados de Carregamento

**Por que é ruim**: Usuários pensam que quebrou.
Desempenho percebido ruim.
Taxa de saída alta.
Confusão.

**Em vez disso**: Mostre skeleton UI.
Indicadores de carregamento.
Carregamento progressivo.
Atualizações otimistas.

## ⚠️ Pontos Críticos

| Problema | Severidade | Solução |
|-------|----------|----------|
| Não validar initData do Telegram | alta | ## Validando initData |
| TON Connect não funciona em mobile | alta | ## Problemas TON Connect Mobile |
| Mini App lento e com travadas | média | ## Desempenho de Mini App |
| Botões personalizados em vez de MainButton | média | ## Usando MainButton Corretamente |

## Skills Relacionadas

Funciona bem com: `telegram-bot-builder`, `frontend`, `blockchain-defi`, `viral-generator-builder`