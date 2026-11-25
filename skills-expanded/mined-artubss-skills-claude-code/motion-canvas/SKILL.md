---
name: motion-canvas
description: Guia completo pronto para produção do Motion Canvas com workarounds ESM/CommonJS, templates de setup completo e troubleshooting para criação de vídeos programática usando TypeScript
version: 2.0.0
author: motion-canvas
repo: https://github.com/motion-canvas/motion-canvas
license: MIT
tags: [Vídeo, TypeScript, Animação, Motion Canvas, Signals, Generators, Canvas API, Vetor, Sincronização de Áudio, Vite, ESM]
dependencies: [@motion-canvas/core>=3.0.0, @motion-canvas/2d>=3.0.0, @motion-canvas/ui>=3.0.0, @motion-canvas/vite-plugin>=3.0.0]
---

# Motion Canvas - Criação de Vídeos Pronto para Produção com TypeScript

Skill completo e pronto para produção para criar vídeos programáticos usando Motion Canvas, incluindo workarounds críticos ESM/CommonJS, templates de configuração completos e troubleshooting abrangente.

## ⚠️ CRÍTICO: Problema de Interoperabilidade ESM/CommonJS

**IMPORTANTE**: O pacote `@motion-canvas/vite-plugin` é distribuído como CommonJS, o que causa erros de importação em projetos ESM modernos. O padrão `import motionCanvas from '@motion-canvas/vite-plugin'` **NÃO FUNCIONARÁ**.

Você DEVE usar o workaround `createRequire` documentado na seção Setup abaixo.

## Quando usar

Use esta skill sempre que você estiver trabalhando com código Motion Canvas para obter conhecimento específico do domínio sobre:

- Criar vídeos animados usando TypeScript e generator functions
- Construir animações com signals e valores reativos
- Trabalhar com gráficos vetoriais e Canvas API
- Sincronizar animações com voice-overs e áudio
- Usar o editor de preview em tempo real para feedback instantâneo
- Implementar animações procedurais com controle de fluxo
- Criar visualizações e diagramas informativos
- Animar texto, formas e componentes customizados
- **Configurar projetos Motion Canvas do zero com configuração correta**
- **Troubleshoot erros comuns de setup e build**

## Conceitos Principais

Motion Canvas permite criar vídeos usando:
- **Generator Functions**: Descrever animações usando generators JavaScript com sintaxe `yield*`
- **Signals**: Valores reativos que atualizam automaticamente propriedades dependentes
- **Preview em Tempo Real**: Editor ao vivo com preview instantâneo powered por Vite
- **TypeScript-First**: Escrever animações em TypeScript com suporte completo a IDE
- **Canvas API**: Aproveitar Canvas 2D para rendering vetorial de alta performance
- **Sincronização de Áudio**: Sincronizar animações precisamente com voice-overs

## Guia Completo de Setup

### Passo 1: Inicializar Projeto

```bash
# Criar diretório do projeto
mkdir my-motion-canvas-project
cd my-motion-canvas-project

# Inicializar package.json
npm init -y
```

### Passo 2: Configurar package.json para ESM

**CRÍTICO**: Adicione `"type": "module"` para habilitar importações ESM.

```json
{
  "name": "my-motion-canvas-project",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

### Passo 3: Instalar TODAS as Dependências Requeridas

**CRÍTICO**: Deve incluir `@motion-canvas/ui` - o plugin falhará sem ele.

```bash
npm install --save-dev @motion-canvas/core @motion-canvas/2d @motion-canvas/vite-plugin @motion-canvas/ui vite typescript
```

### Passo 4: Criar Estrutura do Projeto

```
my-motion-canvas-project/
├── package.json          # "type": "module" obrigatório
├── vite.config.js        # Use .js NÃO .ts (ver Passo 5)
├── tsconfig.json         # Configuração TypeScript
├── index.html            # HTML entry point
└── src/
    ├── project.ts        # Configuração do projeto com cenas
    └── scenes/
        └── example.tsx   # Cena de animação
```

### Passo 5: Criar vite.config.js com Workaround ESM/CommonJS

**CRÍTICO**: Use `vite.config.js` (NÃO `.ts`) com o workaround `createRequire`.

**Arquivo: `vite.config.js`**
```javascript
import {defineConfig} from 'vite';
import {createRequire} from 'module';

// WORKAROUND: @motion-canvas/vite-plugin é CommonJS, deve usar require
const require = createRequire(import.meta.url);
const motionCanvasModule = require('@motion-canvas/vite-plugin');
const motionCanvas = motionCanvasModule.default || motionCanvasModule;

export default defineConfig({
  plugins: [
    motionCanvas({
      project: './src/project.ts',
    }),
  ],
});
```

**Por que .js em vez de .ts?**
- Vite config executa antes da compilação TypeScript
- O workaround `createRequire` funciona confiável em JavaScript puro
- Evita complexidade adicional de resolução de tipos

### Passo 6: Criar tsconfig.json

**CRÍTICO**: Inclua `esModuleInterop` e `allowSyntheticDefaultImports`.

**Arquivo: `tsconfig.json`**
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "ES2020",
    "lib": ["ES2020", "DOM"],
    "jsx": "react-jsx",
    "jsxImportSource": "@motion-canvas/2d/lib",
    "moduleResolution": "node",
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

### Passo 7: Criar index.html

**Arquivo: `index.html`**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Motion Canvas Project</title>
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/src/project.ts"></script>
</body>
</html>
```

### Passo 8: Criar src/project.ts

**Arquivo: `src/project.ts`**
```typescript
import {makeProject} from '@motion-canvas/core';
import example from './scenes/example?scene';

export default makeProject({
  scenes: [example],
});
```

### Passo 9: Criar Primeira Cena de Animação

**Arquivo: `src/scenes/example.tsx`**
```typescript
import {makeScene2D} from '@motion-canvas/2d/lib/scenes';
import {Circle} from '@motion-canvas/2d/lib/components';
import {createRef} from '@motion-canvas/core/lib/utils';
import {all} from '@motion-canvas/core/lib/flow';

export default makeScene2D(function* (view) {
  const circleRef = createRef<Circle>();

  view.add(
    <Circle
      ref={circleRef}
      size={70}
      fill="#e13238"
    />,
  );

  // Animar tamanho e posição do círculo
  yield* circleRef().size(140, 1);
  yield* circleRef().position.x(300, 1);
  yield* circleRef().fill('#e6a700', 1);

  // Animações paralelas
  yield* all(
    circleRef().scale(1.5, 0.5),
    circleRef().rotation(360, 1)
  );
});
```

### Passo 10: Executar Development Server

```bash
npm run dev
```

Abra o navegador em `http://localhost:5173` para ver o editor Motion Canvas.

## Troubleshooting

### Erro: `TypeError: motionCanvas is not a function`

**Causa**: Problema de interoperabilidade ESM/CommonJS com `@motion-canvas/vite-plugin`

**Solução**: Use o workaround `createRequire` em `vite.config.js` (veja Passo 5)

```javascript
// ❌ ERRADO - Não funcionará
import motionCanvas from '@motion-canvas/vite-plugin';

// ✅ CORRETO - Use createRequire
import {createRequire} from 'module';
const require = createRequire(import.meta.url);
const motionCanvasModule = require('@motion-canvas/vite-plugin');
const motionCanvas = motionCanvasModule.default || motionCanvasModule;
```

### Erro: `Cannot find module '@motion-canvas/ui'`

**Causa**: Dependência requerida faltando

**Solução**: Instale o pacote UI:
```bash
npm install --save-dev @motion-canvas/ui
```

### Erro: `Property 'default' does not exist on type ...`

**Causa**: Configuração TypeScript sem configurações ESM interop

**Solução**: Adicione a `tsconfig.json`:
```json
{
  "compilerOptions": {
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true
  }
}
```

### Aviso: `The CJS build of Vite's Node API is deprecated`

**Status**: Este é um aviso conhecido e pode ser ignorado com segurança. Ele aparece porque `@motion-canvas/vite-plugin` é CommonJS. O workaround garante funcionalidade apesar do aviso.

### Erro: `Failed to resolve import "*.tsx?scene"`

**Causa**: Plugin Vite não carregado ou configurado adequadamente

**Solução**:
1. Verifique se `vite.config.js` tem o workaround correto
2. Verifique se o path `project` aponta para o arquivo correto: `'./src/project.ts'`
3. Garanta que importações de cena usam o sufixo `?scene`: `import example from './scenes/example?scene';`

### Build falha com erros TypeScript

**Solução**:
1. Verifique se `tsconfig.json` inclui todas as opções requeridas (veja Passo 6)
2. Verifique se `jsxImportSource` está configurado para `@motion-canvas/2d/lib`
3. Garanta que todas as dependências estão instaladas

## Como usar

Leia arquivos de regras individuais para explicações detalhadas e exemplos de código:

### Conceitos Principais de Animação
- **[references/generators.md](references/generators.md)** - Generator functions para descrever animações
- **[references/signals.md](references/signals.md)** - Signals reativos para propriedades dinâmicas e dependências
- **[references/animations.md](references/animations.md)** - Tweening de propriedades e criação de animações suaves

Para tópicos adicionais como cenas, formas, renderização de texto, sincronização de áudio e funcionalidades avançadas, consulte a [documentação oficial do Motion Canvas](https://motioncanvas.io/docs).

## Exemplo Completo Funcional

Esta é uma estrutura de projeto completa e testada que funciona pronta para uso:

```
my-motion-canvas-project/
├── package.json
│   {
│     "name": "my-motion-canvas-project",
│     "type": "module",
│     "scripts": {
│       "dev": "vite",
│       "build": "vite build"
│     },
│     "devDependencies": {
│       "@motion-canvas/core": "^3.0.0",
│       "@motion-canvas/2d": "^3.0.0",
│       "@motion-canvas/vite-plugin": "^3.0.0",
│       "@motion-canvas/ui": "^3.0.0",
│       "vite": "^5.0.0",
│       "typescript": "^5.0.0"
│     }
│   }
│
├── vite.config.js (com workaround createRequire)
├── tsconfig.json (com esModuleInterop)
├── index.html
└── src/
    ├── project.ts (makeProject com array de cenas)
    └── scenes/
        └── example.tsx (makeScene2D com animações)
```

## Melhores Práticas

1. **Sempre use o workaround createRequire** - Não tente importações ESM padrão para o plugin Vite
2. **Use vite.config.js não .ts** - Evita complexidade adicional de compilação
3. **Inclua todas as dependências** - Não esqueça `@motion-canvas/ui`
4. **Use generator functions** - Todas as animações de cena devem usar sintaxe `function*` e `yield*`
5. **Aproveite signals** - Crie dependências reativas entre propriedades
6. **Pense em durações** - Especifique a duração da animação em segundos como segundo parâmetro
7. **Use refs para controle** - Crie referências a nós para controle de animação preciso
8. **Preview frequentemente** - Aproveite o editor em tempo real para feedback instantâneo
9. **Organize cenas** - Divida animações complexas em múltiplas cenas
10. **Type everything** - Use TypeScript para melhor suporte a IDE e menos erros

## Armadilhas Comuns a Evitar

1. ❌ Esquecer `"type": "module"` em package.json
2. ❌ Usar importação padrão para `@motion-canvas/vite-plugin`
3. ❌ Não instalar `@motion-canvas/ui`
4. ❌ Faltando `esModuleInterop` em tsconfig.json
5. ❌ Usar `vite.config.ts` em vez de `vite.config.js`
6. ❌ Esquecer sufixo `?scene` em importações de cena

## Recursos

- **Documentação**: https://motioncanvas.io/docs
- **Repositório**: https://github.com/motion-canvas/motion-canvas
- **Exemplos**: https://motioncanvas.io/docs/quickstart
- **Comunidade**: Discord e GitHub Discussions
- **Licença**: MIT