# Desenvolvimento Cross-Platform com TypeScript e React

## Diretrizes Gerais de Simplificação

### 1. Remova Complexidade Desnecessária

- sempre que alterar a estrutura do projeto, atualizar a estrutura.md
- Elimine código redundante
- Remova funcionalidades não utilizadas
- Simplifique lógicas complexas
- Evite over-engineering
- manter logs extremamentes necessários
- Ocultar logs de sucesso (200)
- Ocultar mensagens de compilação
- Ocultar o aviso experimental do Node.js
- Manter apenas mensagens de erro importantes

### 2. Gerencie Dependências com Cuidado

- Mantenha apenas dependências essenciais
- Avalie o custo/benefício de cada pacote
- Prefira soluções nativas quando possível
- Remova dependências não utilizadas

### 3. Mantenha o Projeto Limpo

- Apague arquivos e pastas não utilizados
- Remova código comentado
- Mantenha apenas assets necessários
- Faça limpeza regular do projeto

### 4. Simplifique o package.json

- Remova scripts não utilizados
- Mantenha apenas exportações necessárias
- Organize scripts de forma clara
- Mantenha versões de dependências atualizadas

### 5. Desenvolva Componentes Eficientes

- Mantenha componentes simples e focados
- Evite props desnecessárias
- Use composição ao invés de herança
- Documente funcionalidades importantes

### 6. Monitore Padrões de Problemas

- Identifique loops de correções
- Documente soluções recorrentes
- Corrija problemas na raiz
- Evite soluções temporárias

## Processo de Desenvolvimento Incremental

1. **Evolução Gradual**:

   - Comece com uma única página funcional.
   - Adicione um componente por vez.
   - Teste cada adição antes de avançar.
   - Só adicione dependências quando absolutamente necessário.

2. **Regras de Ouro**:

   - Não adicione dependências desnecessárias.
   - Mantenha a simplicidade sempre.
   - Realize testes frequentes.
   - Faça commits pequenos e regulares.

3. **Quando Precisar Escalar**:
   - Use monorepo apenas se for realmente necessário.
   - Adicione ferramentas conforme a necessidade real.
   - Mantenha a documentação atualizada.
   - Faça mudanças incrementais.

## Configuração Inicial

### Remover Avisos Desnecessários

Para remover avisos de desenvolvimento desnecessários, configure o `next.config.js`:

```typescript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
};

module.exports = nextConfig;
```

### Configurar .gitignore

Adicione estas entradas essenciais ao `.gitignore`:

```plaintext
# Dependencies
node_modules

# Next.js
.next
out

# Build
build
dist

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env*.local
.env

# IDE
.idea
.vscode
```

### Criar um Projeto Next.js Básico

```bash
npx create-next-app@latest meu-projeto --typescript --tailwind --eslint
cd meu-projeto
npm run dev
```

### Página Inicial

Crie uma página simples em `src/pages/index.tsx`:

```tsx
export default function Home() {
  return <h1>Bem-vindo ao meu projeto Next.js!</h1>;
}
```

### Adicionar Componentes Básicos

Exemplo: `src/components/Button.tsx`

```tsx
import React from "react";

interface ButtonProps {
  label: string;
  onClick: () => void;
}

const Button: React.FC<ButtonProps> = ({ label, onClick }) => {
  return (
    <button onClick={onClick} className="bg-blue-500 text-white p-2 rounded">
      {label}
    </button>
  );
};

export default Button;
```

### Estilização com Tailwind CSS

Adicione estilos globais em `src/styles/globals.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Boas Práticas

### ✅ Faça:

- Comece com o mínimo necessário.
- Adicione funcionalidades uma por vez.
- Teste cada nova adição.
- Use TypeScript desde o início.
- Use Tailwind CSS para estilização.

### ❌ Não Faça:

- Não adicione dependências desnecessárias.
- Não crie estruturas complexas sem necessidade.
- Não use monorepo sem necessidade clara.
- Não misture múltiplas tecnologias de UI.
- Não tente implementar tudo de uma vez.

## Processo de Desenvolvimento

1. **Crie um Componente**
2. **Teste o Componente**
3. **Integre na Página**
4. **Teste Novamente**
5. **Faça o Commit**
6. **Repita o Ciclo**

## Checklist Antes de Adicionar Algo Novo

- Isso é realmente necessário agora?
- Existe uma solução mais simples?
- Isso vai adicionar complexidade?
- Vale a pena o trade-off?

## Sinais de Alerta

- Muitos arquivos de configuração.
- Dependências não utilizadas.
- Arquivos vazios.
- Imports não utilizados.
- Código comentado em excesso.

## Conclusão

- A simplicidade é a chave.
- Cada linha de código é uma responsabilidade.
- Menos é mais.
- Comece pequeno e cresça conforme necessário.
- Mantenha o projeto limpo e organizado.


### Descrição da Estrutura

- **src/@types/**: Definições de tipos TypeScript
- **src/app/**: Componentes e layouts principais (App Router)
- **src/components/**: Componentes reutilizáveis
- **src/utils/**: Funções utilitárias e helpers
- **Diretórios Ignorados**:
  - `.next/`: Build e cache do Next.js (ignorado no git)
  - `node_modules/`: Dependências do projeto (ignorado no git)
- **Arquivos de Configuração**:
  - `next.config.js`: Configuração do Next.js
  - `tailwind.config.ts`: Configuração do Tailwind CSS
  - `tsconfig.json`: Configuração do TypeScript
  - `.gitignore`: Arquivos a serem ignorados pelo Git
