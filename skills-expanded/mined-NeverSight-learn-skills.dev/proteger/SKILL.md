---
name: proteger
description: >
  Aplica automaticamente um conjunto de proteções jurídicas e técnicas em páginas e apps web
  (React, HTML, Vite, Next.js, etc.) para dificultar cópia, scraping e engenharia reversa.
  Inclui pop-up de consentimento legal com CPF/CNPJ, bloqueio de DevTools, marca d'água
  rastreável, bloqueio de impressão, anti-iframe e checklist de arquitetura segura.
  Use SEMPRE que o usuário mencionar: "proteger meu site", "proteger meu app", "proteger página",
  "evitar cópia do código", "cliente copiou meu site", "F12", "inspecionar elemento",
  "proteger projeto", "/proteger", "pop-up legal", "aviso de propriedade intelectual",
  ou quando estiver finalizando/entregando um projeto e quiser adicionar proteção antes do deploy.
  Também usar quando o usuário perguntar como impedir que alguém copie seu frontend com IA ou DevTools.
---

# Skill: Proteger Página / App

Quando acionada, esta skill guia o usuário com perguntas antes de gerar qualquer código,
depois aplica as camadas de proteção de forma sequencial, adaptando ao stack do projeto.

---

## Passo 0 — Entrevista de Contexto (OBRIGATÓRIO — fazer antes de gerar qualquer código)

Fazer as perguntas abaixo em dois blocos. Só gerar código após ter todas as respostas.

### Bloco A — Escopo

> "Antes de gerar o código, preciso entender seu projeto. Vou fazer algumas perguntas rápidas."

1. **"Qual página ou rota específica você quer proteger?"**
   - Exemplos: `/dashboard`, `/proposta`, `/relatorio`, a página inicial, ou o app todo?
   - ⚠️ Se o usuário disser "o app todo", avisar: "Recomendo proteger por página — aplicar DevTools detection e bloqueio de atalhos globalmente pode interferir em páginas de login, formulários e áreas administrativas. Quer continuar com o app todo mesmo assim?"

2. **"Qual é o framework do projeto?"**
   - Opções: React (Vite/CRA), Next.js, HTML puro, Vue, outro?

3. **"Essa página é pública (qualquer um acessa sem login) ou exige autenticação?"**
   - Relevante para decidir se o fingerprint de usuário logado faz sentido na Camada 4.

4. **"Já existe um rodapé (footer) na página com informações de direitos autorais, copyright ou créditos?"**
   - Se sim: "Prefere adaptar o que já está no rodapé ou adicionar os novos elementos junto a ele?"
   - ⚠️ Nunca duplicar ou sobrescrever um rodapé existente sem confirmação do usuário.

5. **"Qual é o estilo visual da página? (opcional, mas recomendado)"**
   - Pedir: cor de fundo principal, cor de destaque, se usa Tailwind, Material UI, shadcn, ou CSS próprio.
   - Alternativa: "Pode colar um trecho do seu CSS ou das classes Tailwind usadas na página?"
   - ⚠️ O modal e os demais elementos gerados devem seguir o estilo da página — nunca gerar um modal
     branco-e-preto genérico sem antes verificar o design existente.

### Bloco B — Identidade Legal

6. **"Qual é o nome completo ou razão social do dono do projeto?"**
   - Será exibido no pop-up legal, nos metadados e na marca d'água.

7. **"Você prefere usar CPF ou CNPJ no aviso legal?"**
   - Opções: CPF / CNPJ / Não quero incluir documento
   - Se CPF: "Qual é o CPF? (formato: 000.000.000-00)"
   - Se CNPJ: "Qual é o CNPJ? (formato: 00.000.000/0000-00)"
   - ⚠️ Informar: "O documento ficará visível no pop-up e nos metadados HTML. Isso é intencional — aumenta a credibilidade jurídica do aviso."

8. **"Qual é o e-mail ou site de contato para exibir no aviso legal?"**

Após coletar as respostas, confirmar:
> "Ótimo! Vou proteger a página **[ROTA]** do projeto **[FRAMEWORK]** em nome de **[NOME]** ([CPF/CNPJ]). Gerando o código agora…"

---

## Passo 1 — Aplicar as Camadas de Proteção

### Camada 0 — Pop-up de Consentimento Legal (aplicar primeiro)

Modal de tela cheia que aparece na primeira visita à página protegida.
Registra aceite no `localStorage` para não exibir novamente na mesma sessão/dispositivo.

**Comportamento:**
- **"Li e aceito"** → fecha o modal, libera o conteúdo, salva timestamp do aceite
- **"Não aceito"** → redireciona para `about:blank` (página em branco)

**Copy do aviso legal — usar exatamente este texto, interpolando os dados:**

```
AVISO DE PROPRIEDADE INTELECTUAL

Esta plataforma e todo o seu conteúdo — incluindo layouts, funcionalidades, textos,
imagens, fluxos e código-fonte — são de propriedade exclusiva de [NOME/RAZÃO SOCIAL],
[CPF/CNPJ], protegidos pela Lei de Direitos Autorais (Lei nº 9.610/1998) e pela
Lei de Software (Lei nº 9.609/1998).

Ao acessar esta página, você declara ciência e concordância plena de que:

▸ Qualquer reprodução, cópia, distribuição ou engenharia reversa não autorizada
  constitui violação de direitos autorais, passível de ação judicial imediata;

▸ O infrator estará sujeito à reparação civil por perdas e danos — incluindo lucros
  cessantes e danos morais — além de responsabilização criminal nos termos do
  Art. 184 do Código Penal Brasileiro, com pena de reclusão de 2 a 4 anos;

▸ Esta sessão poderá ser registrada para fins de auditoria, rastreamento e
  comprovação de autoria em eventual processo judicial.

Contato do titular: [EMAIL_OU_SITE]

Ao clicar em "Li e aceito os termos", você confirma que leu, compreendeu e
concordou integralmente com todas as condições acima.
```

**Implementação para React — criar `src/components/LegalConsentModal.tsx`:**

```tsx
import { useState, useEffect } from 'react';

const CONSENT_KEY = '__consent_v1__';

interface LegalConsentModalProps {
  owner: string;
  document: string; // CPF ou CNPJ formatado, ou string vazia
  contact: string;
}

export function LegalConsentModal({ owner, document, contact }: LegalConsentModalProps) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (!localStorage.getItem(CONSENT_KEY)) {
      setVisible(true);
    }
  }, []);

  const accept = () => {
    localStorage.setItem(CONSENT_KEY, new Date().toISOString());
    setVisible(false);
  };

  const decline = () => {
    window.location.href = 'about:blank';
  };

  if (!visible) return null;

  return (
    <div style={{
      position: 'fixed', inset: 0, zIndex: 99999,
      background: 'rgba(0,0,0,0.92)',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      padding: '1rem',
    }}>
      <div style={{
        background: '#fff', borderRadius: '8px',
        maxWidth: '640px', width: '100%',
        padding: '2rem', boxShadow: '0 20px 60px rgba(0,0,0,0.5)',
      }}>
        <h2 style={{ marginTop: 0, fontSize: '1rem', letterSpacing: '0.05em', color: '#111' }}>
          AVISO DE PROPRIEDADE INTELECTUAL
        </h2>
        <p style={{ fontSize: '0.875rem', lineHeight: 1.7, color: '#333' }}>
          Esta plataforma e todo o seu conteúdo são de propriedade exclusiva de{' '}
          <strong>{owner}</strong>{document ? `, ${document},` : ','} protegidos pela Lei de
          Direitos Autorais (Lei nº 9.610/1998) e pela Lei de Software (Lei nº 9.609/1998).
        </p>
        <p style={{ fontSize: '0.875rem', lineHeight: 1.7, color: '#333' }}>
          Ao acessar esta página, você declara ciência e concordância de que:
        </p>
        <ul style={{ fontSize: '0.875rem', lineHeight: 1.8, color: '#333', paddingLeft: '1.25rem' }}>
          <li>Qualquer reprodução, cópia ou engenharia reversa não autorizada constitui violação de
            direitos autorais, passível de ação judicial imediata;</li>
          <li>O infrator estará sujeito à reparação civil por perdas e danos e à responsabilização
            criminal nos termos do Art. 184 do Código Penal (pena de 2 a 4 anos de reclusão);</li>
          <li>Esta sessão poderá ser registrada para fins de auditoria e comprovação de autoria.</li>
        </ul>
        {contact && (
          <p style={{ fontSize: '0.8rem', color: '#666' }}>Contato do titular: {contact}</p>
        )}
        <div style={{ display: 'flex', gap: '0.75rem', marginTop: '1.5rem' }}>
          <button
            onClick={accept}
            style={{
              flex: 1, padding: '0.75rem', background: '#111', color: '#fff',
              border: 'none', borderRadius: '6px', cursor: 'pointer',
              fontSize: '0.875rem', fontWeight: 600,
            }}
          >
            Li e aceito os termos
          </button>
          <button
            onClick={decline}
            style={{
              padding: '0.75rem 1.25rem', background: 'transparent', color: '#666',
              border: '1px solid #ddd', borderRadius: '6px', cursor: 'pointer',
              fontSize: '0.875rem',
            }}
          >
            Não aceito
          </button>
        </div>
      </div>
    </div>
  );
}
```

Chamar na página protegida (ex: `Dashboard.tsx` ou `App.tsx` se for o app todo):

```tsx
import { LegalConsentModal } from './components/LegalConsentModal';

function Dashboard() {
  return (
    <>
      <LegalConsentModal
        owner="[NOME_DO_DESENVOLVEDOR]"
        document="[CPF/CNPJ]"
        contact="[EMAIL_OU_SITE]"
      />
      {/* resto do conteúdo da página */}
    </>
  );
}
```

**Para Next.js** — adicionar no componente da página específica (ex: `app/dashboard/page.tsx`) ou
em um Client Component wrapper, pois usa `localStorage`.

**Para HTML puro** — adicionar antes do `</body>`:

```html
<div id="__legal-modal__" style="position:fixed;inset:0;z-index:99999;background:rgba(0,0,0,0.92);display:flex;align-items:center;justify-content:center;padding:1rem;">
  <div style="background:#fff;border-radius:8px;max-width:640px;width:100%;padding:2rem;">
    <h2 style="margin-top:0;font-size:1rem;letter-spacing:.05em;">AVISO DE PROPRIEDADE INTELECTUAL</h2>
    <p style="font-size:.875rem;line-height:1.7;">
      Esta plataforma é de propriedade exclusiva de <strong>[NOME]</strong>, [CPF/CNPJ],
      protegida pela Lei nº 9.610/1998. Reprodução não autorizada sujeita à responsabilização
      civil e criminal (Art. 184 do Código Penal — pena de 2 a 4 anos).
    </p>
    <p style="font-size:.8rem;color:#666;">Contato: [EMAIL]</p>
    <div style="display:flex;gap:.75rem;margin-top:1.5rem;">
      <button onclick="acceptConsent()" style="flex:1;padding:.75rem;background:#111;color:#fff;border:none;border-radius:6px;cursor:pointer;font-weight:600;">Li e aceito os termos</button>
      <button onclick="window.location.href='about:blank'" style="padding:.75rem 1.25rem;border:1px solid #ddd;border-radius:6px;cursor:pointer;background:transparent;color:#666;">Não aceito</button>
    </div>
  </div>
</div>
<script>
  (function() {
    if (localStorage.getItem('__consent_v1__')) {
      document.getElementById('__legal-modal__').remove();
    }
  })();
  function acceptConsent() {
    localStorage.setItem('__consent_v1__', new Date().toISOString());
    document.getElementById('__legal-modal__').remove();
  }
</script>
```

---

### Camada 1 — Metadados de Autoria

Inserir no `index.html` ou `<head>` da página protegida:

```html
<meta name="author" content="[NOME_DO_DESENVOLVEDOR]" />
<meta name="copyright" content="© [ANO] [NOME_DO_DESENVOLVEDOR] — [CPF/CNPJ]. Todos os direitos reservados." />
<meta name="generator" content="Desenvolvido por [NOME_DO_DESENVOLVEDOR]" />
<link rel="canonical" href="[URL_DA_PÁGINA]" />
<!-- PROTECTED: Propriedade intelectual de [NOME] ([CPF/CNPJ]). Cópia não autorizada é proibida pela Lei 9.610/1998. -->
```

> A tag `<link rel="canonical">` facilita processos de DMCA ao provar a URL original do conteúdo.

---

### Camada 2 — Bloquear Clique Direito e Atalhos

Aplicar **apenas na página protegida**, não globalmente.

Para **React**, criar o hook `src/hooks/useProtection.ts`:

```typescript
import { useEffect } from 'react';

export function useProtection() {
  useEffect(() => {
    const blockContextMenu = (e: MouseEvent) => e.preventDefault();

    const blockKeys = (e: KeyboardEvent) => {
      const blocked =
        e.key === 'F12' ||
        (e.ctrlKey && e.shiftKey && ['I', 'J', 'C'].includes(e.key)) ||
        (e.ctrlKey && e.key === 'U') ||
        (e.ctrlKey && e.key === 'p');
      if (blocked) e.preventDefault();
    };

    document.addEventListener('contextmenu', blockContextMenu);
    document.addEventListener('keydown', blockKeys);

    return () => {
      document.removeEventListener('contextmenu', blockContextMenu);
      document.removeEventListener('keydown', blockKeys);
    };
  }, []);
}
```

Chamar no componente da página protegida:

```typescript
import { useProtection } from '../hooks/useProtection';

function Dashboard() {
  useProtection();
  // ...
}
```

Para **HTML puro**, adicionar no `<script>` da página específica:

```javascript
document.addEventListener('contextmenu', e => e.preventDefault());
document.addEventListener('keydown', e => {
  if (
    e.key === 'F12' ||
    (e.ctrlKey && e.shiftKey && ['I','J','C'].includes(e.key)) ||
    (e.ctrlKey && e.key === 'U') ||
    (e.ctrlKey && e.key === 'p')
  ) {
    e.preventDefault();
  }
});
```

---

### Camada 3 — Detectar DevTools Aberto

⚠️ **Ativar apenas em produção** via variável de ambiente.

```typescript
if (import.meta.env.PROD) { // Para Next.js: process.env.NODE_ENV === 'production'
  const devToolsDetector = () => {
    const threshold = 160;
    const widthDiff = window.outerWidth - window.innerWidth > threshold;
    const heightDiff = window.outerHeight - window.innerHeight > threshold;

    if (widthDiff || heightDiff) {
      document.body.style.filter = 'blur(10px)';
      document.title = '⚠️ Acesso restrito';
    } else {
      document.body.style.filter = 'none';
      document.title = '[TÍTULO_ORIGINAL]';
    }
  };

  const consoleDetector = new Image();
  Object.defineProperty(consoleDetector, 'id', {
    get() {
      document.body.innerHTML =
        '<div style="display:flex;align-items:center;justify-content:center;' +
        'height:100vh;font-family:sans-serif;font-size:1.25rem;color:#333;text-align:center;padding:2rem;">' +
        '⚠️ Inspeção de código não permitida nesta plataforma.<br>' +
        '<small style="color:#999;font-size:.9rem;">Propriedade de [NOME] — [CPF/CNPJ]</small>' +
        '</div>';
    },
  });

  setInterval(devToolsDetector, 1000);
  console.log('%c', consoleDetector);
}
```

---

### Camada 4 — Marca d'água Invisível com Fingerprint

Se o usuário estiver **logado**, inclui o fingerprint — torna screenshots rastreáveis até a pessoa.

Para **React** (componente da página protegida):

```tsx
<div
  id="__owner__"
  style={{ display: 'none' }}
  data-owner="[NOME]"
  data-document="[CPF/CNPJ]"
  data-contact="[EMAIL_OU_SITE]"
  data-year={new Date().getFullYear()}
  data-timestamp={new Date().toISOString()}
  data-session={typeof window !== 'undefined' ? btoa(user?.email ?? 'public') : ''}
  data-consent="true"
/>
```

> Se o projeto usa Supabase Auth, obter `user` via `supabase.auth.getUser()` e passar para o componente.

Para **HTML puro**, antes do `</body>`:

```html
<div id="__owner__"
  style="display:none;visibility:hidden;opacity:0;"
  data-owner="[NOME]"
  data-document="[CPF/CNPJ]"
  data-contact="[EMAIL]"
  data-year="[ANO]"
  data-timestamp=""
  data-consent="true">
</div>
<script>
  document.getElementById('__owner__').setAttribute('data-timestamp', new Date().toISOString());
</script>
```

---

### Camada 4.5 — Bloqueio de Impressão e Seleção de Texto

Adicionar ao CSS da página protegida:

```css
@media print {
  * { display: none !important; }
  body::before {
    content: "⚠️ Impressão não autorizada. Este conteúdo é propriedade intelectual de [NOME] ([CPF/CNPJ]).";
    display: block;
    font-size: 1.5rem;
    padding: 2rem;
    font-family: sans-serif;
  }
}

.protected-content,
.protected-content * {
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
}
```

Adicionar ao hook ou script de proteção:

```javascript
window.addEventListener('beforeprint', () => {
  alert('⚠️ Impressão bloqueada. Este conteúdo é propriedade intelectual protegida por lei.');
  window.stop?.();
});
```

Envolver o conteúdo sensível com a classe:

```tsx
{/* React */}
<main className="protected-content">
  {/* conteúdo da página */}
</main>
```

---

### Camada 4.8 — Anti-iframe / Framebusting

Impede que a página seja incorporada em outros sites via `<iframe>`.

Adicionar ao hook ou script de proteção (executar antes de qualquer render):

```javascript
if (window !== window.top) {
  window.top.location.href = window.location.href;
}
```

Para **Next.js**, adicionar em `next.config.js`:

```javascript
const nextConfig = {
  async headers() {
    return [
      {
        source: '/dashboard', // substitua pela rota protegida
        headers: [
          { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
          { key: 'Content-Security-Policy', value: "frame-ancestors 'self'" },
        ],
      },
    ];
  },
};
```

Para **Vite/HTML**, instruir o usuário a configurar o servidor de produção (Nginx, Vercel, Netlify headers).

---

### Camada 5 — Checklist de Arquitetura Segura

Apresentar esta lista ao usuário para revisão manual:

```
PROTEÇÃO TÉCNICA
[ ] Lógica de negócio está no backend (Edge Functions, API routes), não no frontend?
[ ] Chaves de API e tokens estão em variáveis de ambiente (.env), nunca no código frontend?
[ ] Build de produção com minificação e ofuscação ativada?
    → Vite: build.minify: 'terser' no vite.config.ts
    → Next.js: ativado automaticamente no next build
[ ] Imagens e assets sensíveis em storage protegido (ex: Supabase Storage com RLS)?
[ ] Todos os console.log com dados sensíveis foram removidos antes do deploy?

PROTEÇÃO JURÍDICA
[ ] Pop-up de consentimento legal ativo e testado em produção?
[ ] Anti-iframe configurado (header CSP no servidor + framebusting JS)?
[ ] Impressão bloqueada via @media print e beforeprint?
[ ] Seleção de texto desabilitada no conteúdo sensível (classe .protected-content)?
[ ] Watermark com fingerprint do usuário logado aplicado (se houver autenticação)?
[ ] Projeto registrado no DMCA.com para proteção legal internacional?
[ ] Cliente/contratante assinou NDA ou contrato de sigilo antes do primeiro acesso?
    → Ferramentas recomendadas: ClickSign (BR) ou DocuSign (internacional)
```

---

## Passo 2 — Entrega Final

Ao final, entregar:

1. **Todos os arquivos de código** prontos para colar:
   - `LegalConsentModal.tsx` (ou snippet HTML)
   - `useProtection.ts` (hook React) ou script JS
   - CSS de proteção de impressão/seleção
   - Configuração de headers (Next.js ou servidor)

2. **Tabela resumo das camadas aplicadas:**

| Camada | Proteção | Status |
|--------|----------|--------|
| 0 | Pop-up legal de consentimento | ✅ Aplicada |
| 1 | Metadados de autoria + canonical | ✅ Aplicada |
| 2 | Bloqueio de clique direito e atalhos | ✅ Aplicada |
| 3 | Detecção de DevTools (apenas produção) | ✅ Aplicada |
| 4 | Marca d'água invisível + fingerprint | ✅ Aplicada |
| 4.5 | Bloqueio de impressão + seleção de texto | ✅ Aplicada |
| 4.8 | Anti-iframe / framebusting | ✅ Aplicada |
| 5 | Checklist de arquitetura segura | ✅ Revisado |

3. **Aviso de limitações:** Nenhuma proteção frontend é absoluta — um desenvolvedor experiente
   pode contornar todas as camadas. O objetivo é **dissuadir o usuário comum** e **criar
   evidências jurídicas** de autoria e consentimento.

4. **Próximos passos recomendados:**
   - Registrar o projeto em [DMCA.com](https://dmca.com) para proteção legal internacional
   - Fazer o cliente assinar um NDA antes do primeiro acesso ao sistema:
     → [ClickSign](https://www.clicksign.com) (Brasil) ou [DocuSign](https://www.docusign.com) (internacional)
   - A tag `canonical` nos metadados facilita processos de DMCA ao provar a URL original

---

## Observações para o modelo

- Nunca pular o Passo 0 — as perguntas são obrigatórias para gerar código correto e personalizado
- Sempre substituir os placeholders `[NOME]`, `[CPF/CNPJ]`, `[EMAIL_OU_SITE]`, `[ANO]`, `[ROTA]` com os dados coletados
- Em projetos React com Supabase, o arquivo de entrada é `src/main.tsx`; o hook fica em `src/hooks/useProtection.ts`; o modal em `src/components/LegalConsentModal.tsx`
- A Camada 3 (DevTools) é a mais agressiva — reforçar que deve ser usada **apenas em produção**
- Se a página exige login, recomendar fortemente o fingerprint com o email do usuário logado na Camada 4
- O pop-up legal (Camada 0) é a **camada mais importante** — é a única que cria evidência jurídica de ciência e concordância do usuário
- **Design adaptável**: o modal e todos os elementos gerados devem seguir o estilo visual da página (cores, fontes, border-radius). Se o usuário informou paleta ou framework CSS, usar esses valores no código gerado. Nunca entregar um modal branco-e-preto genérico sem antes considerar o design existente
- **Rodapé existente**: se o usuário confirmou que já existe um footer com copyright, perguntar se adapta o atual ou adiciona junto. Nunca duplicar ou sobrescrever sem confirmação
- Nunca prometer proteção absoluta — ser honesto sobre as limitações técnicas e o papel complementar da proteção jurídica
- Se o usuário quiser aplicar direto em um arquivo existente, pedir para fazer upload ou colar o conteúdo
