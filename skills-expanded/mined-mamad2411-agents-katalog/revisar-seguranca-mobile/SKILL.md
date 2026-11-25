---
name: revisar-seguranca-mobile
description: "Checklist shift-left de segurança mobile — SecureStore, logs, deep link, WebView e permissões — como parte do DoD. Use quando o dev-mobile, o dev-security ou o tech-lead valida segurança antes do merge."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: revisar-seguranca-mobile

Checklist "shift left" de segurança para **React Native + Expo**: armazenamento seguro, dados em log, permissões, deep link hijacking, WebView, dependências e exposição de informações. Parte obrigatória do DoD do dev-mobile.

**Agente:** `dev-mobile`, `dev-security`, `tech-lead`  
**Guardrails aplicáveis:** `mobile.md §7`, `mobile.md §10`, `seguranca.md`, `appsec.md`

---

## Quando usar

- **Obrigatoriamente** antes de abrir qualquer PR (faz parte do DoD do dev-mobile)
- Ao revisar código de outro desenvolvedor como par de segurança
- Ao integrar uma nova biblioteca nativa no projeto
- Ao implementar funcionalidade que lida com dados pessoais ou autenticação

---

## Processo de execução

---

### §1 — Armazenamento seguro (`mobile.md §7`)

- [ ] **Tokens de autenticação** em `expo-secure-store` — nunca em `AsyncStorage`, MMKV ou `useState`
- [ ] **Chaves de API** em `expo-secure-store` ou em variável de ambiente via `app.config.ts` (nunca hardcoded)
- [ ] **Dados pessoais sensíveis** (CPF, número de cartão, senha) — nunca persistidos localmente sem criptografia
- [ ] `AsyncStorage` usado apenas para dados não-sensíveis (tema, idioma, flags de onboarding)
- [ ] Nenhum dado sensível em `Constants.expoConfig.extra` — esse objeto é embarcado no bundle e legível

```typescript
// ⛔ bloqueados
await AsyncStorage.setItem('jwt', token);
const token = process.env.API_KEY;              // hardcoded em bundle
Constants.expoConfig?.extra?.secretKey;         // exposto no bundle

// ✅ corretos
await SecureStore.setItemAsync('auth_token', token);
// Chaves de API ficam no backend — o app nunca as carrega diretamente
```

---

### §2 — Dados em logs e debugging

- [ ] Nenhum `console.log` com dados pessoais, tokens ou PII (nome completo, CPF, email, endereço)
- [ ] Interceptors de erro do `axios` logam apenas status HTTP e URL — nunca o body da resposta
- [ ] `console.log` removidos ou substituídos por logger condicional (`__DEV__`) antes do PR

```typescript
// ⛔ bloqueado
console.log('Usuário logado:', user);           // vaza dados pessoais
console.log('Token:', token);                   // vaza credencial

// ✅ correto
if (__DEV__) console.log('[DEBUG] Login bem-sucedido');
// Logger de produção: apenas status e contexto sem dados
```

---

### §3 — Deep link hijacking

- [ ] Parâmetros recebidos via deep link são **validados e sanitizados** antes de uso
- [ ] IDs e parâmetros de rota não são usados para montar URLs ou queries sem validação
- [ ] Ações críticas (pagamento, deleção) **nunca** são acionadas diretamente por parâmetro de deep link sem confirmação do usuário

```typescript
// ⛔ bloqueado — parâmetro de deep link usado diretamente em navegação sem validação
const { targetUrl } = useLocalSearchParams();
router.push(targetUrl);   // pode navegar para rota arbitrária

// ✅ correto — validar contra lista de rotas permitidas
const { action } = useLocalSearchParams();
const allowedActions = ['confirm', 'cancel', 'view'] as const;
if (!allowedActions.includes(action as typeof allowedActions[number])) return;
```

---

### §4 — WebView (quando presente)

- [ ] `javaScriptEnabled={false}` quando JavaScript não é necessário
- [ ] `originWhitelist` restrito ao domínio esperado — nunca `['*']`
- [ ] `onShouldStartLoadWithRequest` implementado para bloquear navegação para URLs externas
- [ ] Sem injeção de conteúdo dinâmico do usuário via `injectedJavaScript`

```tsx
// ✅ WebView com restrições mínimas
<WebView
  source={{ uri: 'https://meudominio.com/termos' }}
  javaScriptEnabled={false}
  originWhitelist={['https://meudominio.com']}
  onShouldStartLoadWithRequest={(request) => {
    return request.url.startsWith('https://meudominio.com');
  }}
/>
```

---

### §5 — Permissões e dados pessoais (`mobile.md §10`)

- [ ] Permissões solicitadas **sob demanda**, nunca no startup (`mobile.md §10`)
- [ ] Antes de solicitar permissão nativa, o app exibe explicação clara do motivo
- [ ] Mensagens de permissão no `app.config.ts` são descritivas e em português
- [ ] Dados de localização, câmera e microfone não são transmitidos ao BFF sem consentimento explícito do usuário
- [ ] Coleta de dados pessoais coberta pela política de privacidade do app

---

### §6 — Exposição de informações no bundle

- [ ] Nenhum secret, token ou chave de API hardcoded em código TypeScript/JavaScript
- [ ] `app.config.ts` `extra` não contém dados sensíveis — só configurações públicas (URLs de BFF, ambiente)
- [ ] Strings com informações de ambiente interno (IPs internos, nomes de serviços) removidas do código de produção
- [ ] `__DEV__` blocos garantem que ferramentas de debug (React Query Devtools, Reactotron) não carregam em produção

```typescript
// ⛔ bloqueado
const extra = {
  apiKey: 'sk-1234567890abcdef',   // exposto no bundle
  dbPassword: 'senha123',          // exposto no bundle
};

// ✅ correto
const extra = {
  bffUrl: process.env.BFF_URL,     // URL do BFF — não é secret
  environment: process.env.APP_ENV, // configuração pública
};
```

---

### §7 — Segurança de autenticação

- [ ] Token JWT verificado no BFF — o app mobile **não valida** o token localmente
- [ ] Logout invalida o token no BFF e remove do `SecureStore`
- [ ] Refresh token implementado com rotação (se aplicável)
- [ ] Sessão invalidada ao detectar mudança de conta no dispositivo (biometria, FaceID)
- [ ] Dados do usuário limpos do Zustand e TanStack Query cache no logout

```typescript
// ✅ logout completo
async function logout() {
  await SecureStore.deleteItemAsync('auth_token');
  await SecureStore.deleteItemAsync('refresh_token');
  queryClient.clear();           // limpa cache TanStack Query
  authStore.getState().logout(); // limpa Zustand
  router.replace('/(auth)/login');
}
```

---

### §8 — Dependências e supply chain

- [ ] Nenhuma dependência nova adicionada sem avaliação de necessidade e reputação
- [ ] Scripts `postinstall` de novas dependências inspecionados antes de instalar
- [ ] `npm audit` executado — vulnerabilidades HIGH/CRITICAL resolvidas antes do PR
- [ ] Expo SDK e dependências Expo atualizadas conforme `expo upgrade` (não manualmente)

---

## Formato de saída

Ao concluir, emitir relatório:

```
## Revisão de segurança mobile — <feature/PR>

**Status:** ✅ Aprovado | ⛔ Bloqueado (corrigir antes do PR)

### Achados
| Severidade | Arquivo | Problema | Regra |
|---|---|---|---|
| HIGH | useAuth.ts:34 | Token em AsyncStorage | mobile.md §7 |
| MEDIUM | LoginScreen.tsx:89 | console.log com email do usuário | seguranca.md §2 |

### Confirmações (itens verificados e aprovados)
- [lista dos §§ verificados sem problemas]
```

**Achados HIGH/CRITICAL bloqueiam o PR.**  
Achados MEDIUM/LOW devem ser corrigidos ou documentados com justificativa.

---

## Checklist de conclusão da skill

- [ ] Todos os 8 blocos executados
- [ ] Nenhum achado HIGH ou CRITICAL pendente
- [ ] `npm audit` sem vulnerabilidades HIGH/CRITICAL
- [ ] Relatório emitido e anexado à descrição do PR
