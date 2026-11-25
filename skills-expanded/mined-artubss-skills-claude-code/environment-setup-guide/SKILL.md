---
name: environment-setup-guide
description: "Guie desenvolvedores na configuração de ambientes de desenvolvimento com ferramentas, dependências e configurações adequadas"
---

# Guia de Configuração de Ambiente

## Visão Geral

Ajude desenvolvedores a configurar ambientes de desenvolvimento completos do zero. Esta skill fornece orientação passo a passo para instalar ferramentas, configurar dependências, definir variáveis de ambiente e verificar se a configuração funciona corretamente.

## Quando Usar Esta Skill

- Use ao iniciar um novo projeto e precisar configurar o ambiente de desenvolvimento
- Use ao integrar novos membros da equipe a um projeto
- Use ao mudar para uma nova máquina ou sistema operacional
- Use ao solucionar problemas relacionados ao ambiente
- Use ao documentar instruções de configuração para um projeto
- Use ao criar documentação de ambiente de desenvolvimento

## Como Funciona

### Passo 1: Identificar Requisitos

Vou ajudar você a determinar o que precisa ser instalado:
- Linguagem de programação e versão (Node.js, Python, Go, etc.)
- Gerenciadores de pacotes (npm, pip, cargo, etc.)
- Sistemas de banco de dados (PostgreSQL, MongoDB, Redis, etc.)
- Ferramentas de desenvolvimento (Git, Docker, extensões de IDE, etc.)
- Variáveis de ambiente e arquivos de configuração

### Passo 2: Verificar Configuração Atual

Antes de instalar qualquer coisa, vou ajudar a verificar o que já está instalado:
```bash
# Verificar versões de ferramentas instaladas
node --version
python --version
git --version
docker --version
```

### Passo 3: Fornecer Instruções de Instalação

Vou disponibilizar comandos de instalação específicos para cada plataforma:
- **macOS:** Usando Homebrew
- **Linux:** Usando apt, yum ou gerenciador de pacotes
- **Windows:** Usando Chocolatey, Scoop ou instaladores diretos

### Passo 4: Configurar o Ambiente

Ajudar a configurar:
- Variáveis de ambiente (arquivos .env)
- Arquivos de configuração (.gitconfig, .npmrc, etc.)
- Configurações de IDE (VS Code, IntelliJ, etc.)
- Configuração de shell (.bashrc, .zshrc, etc.)

### Passo 5: Verificar Instalação

Fornecer etapas de verificação para garantir que tudo funcione:
- Executar verificações de versão
- Testar comandos básicos
- Verificar conexões de banco de dados
- Confirmar se as variáveis de ambiente são carregadas

## Exemplos

### Exemplo 1: Configuração de Projeto Node.js

```markdown
## Configurando Ambiente de Desenvolvimento Node.js

### Pré-requisitos
- macOS, Linux ou Windows
- Acesso a Terminal/Prompt de Comando
- Conexão com internet

### Passo 1: Instalar Node.js

**macOS (usando Homebrew):**
\`\`\`bash
# Instalar Homebrew se não estiver instalado
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Node.js
brew install node
\`\`\`

**Linux (Ubuntu/Debian):**
\`\`\`bash
# Atualizar lista de pacotes
sudo apt update

# Instalar Node.js e npm
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
\`\`\`

**Windows (usando Chocolatey):**
\`\`\`powershell
# Instalar Chocolatey se não estiver instalado
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Instalar Node.js
choco install nodejs
\`\`\`

### Passo 2: Verificar Instalação

\`\`\`bash
node --version  # Deve exibir v20.x.x ou superior
npm --version   # Deve exibir 10.x.x ou superior
\`\`\`

### Passo 3: Instalar Dependências do Projeto

\`\`\`bash
# Clonar o repositório
git clone https://github.com/seu-repositorio/projeto.git
cd projeto

# Instalar dependências
npm install
\`\`\`

### Passo 4: Configurar Variáveis de Ambiente

Criar um arquivo \`.env\`:
\`\`\`bash
# Copiar arquivo de exemplo do ambiente
cp .env.example .env

# Editar com seus valores
nano .env
\`\`\`

Conteúdo exemplo \`.env\`:
\`\`\`
NODE_ENV=development
PORT=3000
DATABASE_URL=postgresql://localhost:5432/mydb
API_KEY=sua-chave-api-aqui
\`\`\`

### Passo 5: Executar o Projeto

\`\`\`bash
# Iniciar servidor de desenvolvimento
npm run dev

# Deve exibir: Servidor executando em http://localhost:3000
\`\`\`

### Solução de Problemas

**Problema:** "node: command not found"
**Solução:** Reinicie o terminal ou execute \`source ~/.bashrc\` (Linux) ou \`source ~/.zshrc\` (macOS)

**Problema:** Erros "Permission denied"
**Solução:** Não use sudo com npm. Corrija as permissões:
\`\`\`bash
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
\`\`\`
```

### Exemplo 2: Configuração de Projeto Python

```markdown
## Configurando Ambiente de Desenvolvimento Python

### Passo 1: Instalar Python

**macOS:**
\`\`\`bash
brew install python@3.11
\`\`\`

**Linux:**
\`\`\`bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
\`\`\`

**Windows:**
\`\`\`powershell
choco install python --version=3.11
\`\`\`

### Passo 2: Verificar Instalação

\`\`\`bash
python3 --version  # Deve exibir Python 3.11.x
pip3 --version     # Deve exibir pip 23.x.x
\`\`\`

### Passo 3: Criar Ambiente Virtual

\`\`\`bash
# Navegar para diretório do projeto
cd meu-projeto

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
\`\`\`

### Passo 4: Instalar Dependências

\`\`\`bash
# Instalar a partir de requirements.txt
pip install -r requirements.txt

# Ou instalar pacotes individualmente
pip install flask sqlalchemy python-dotenv
\`\`\`

### Passo 5: Configurar Variáveis de Ambiente

Criar arquivo \`.env\`:
\`\`\`
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=sqlite:///app.db
SECRET_KEY=sua-chave-secreta-aqui
\`\`\`

### Passo 6: Executar a Aplicação

\`\`\`bash
# Executar app Flask
flask run

# Deve exibir: Executando em http://127.0.0.1:5000
\`\`\`
```

### Exemplo 3: Ambiente de Desenvolvimento com Docker

```markdown
## Configurando Ambiente de Desenvolvimento Docker

### Passo 1: Instalar Docker

**macOS:**
\`\`\`bash
brew install --cask docker
# Ou baixe Docker Desktop de docker.com
\`\`\`

**Linux:**
\`\`\`bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER
newgrp docker
\`\`\`

**Windows:**
Baixe Docker Desktop de docker.com

### Passo 2: Verificar Instalação

\`\`\`bash
docker --version        # Deve exibir Docker versão 24.x.x
docker-compose --version # Deve exibir Docker Compose versão 2.x.x
\`\`\`

### Passo 3: Criar docker-compose.yml

\`\`\`yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://postgres:password@db:5432/mydb
    volumes:
      - .:/app
      - /app/node_modules
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydb
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
\`\`\`

### Passo 4: Iniciar Serviços

\`\`\`bash
# Build e iniciar containers
docker-compose up -d

# Visualizar logs
docker-compose logs -f

# Parar serviços
docker-compose down
\`\`\`

### Passo 5: Verificar Serviços

\`\`\`bash
# Verificar containers em execução
docker ps

# Testar conexão com banco de dados
docker-compose exec db psql -U postgres -d mydb
\`\`\`
```

## Boas Práticas

### ✅ Faça Isso

- **Documente Tudo** - Escreva instruções de configuração claras
- **Use Gerenciadores de Versão** - nvm para Node, pyenv para Python
- **Crie .env.example** - Mostre variáveis de ambiente necessárias
- **Teste em Sistema Limpo** - Verifique se as instruções funcionam do zero
- **Inclua Solução de Problemas** - Documente problemas comuns e soluções
- **Use Docker** - Para ambientes consistentes entre máquinas
- **Fixe Versões** - Especifique versões exatas em arquivos de pacotes
- **Automatize a Configuração** - Crie scripts de setup quando possível
- **Verifique Pré-requisitos** - Liste ferramentas necessárias antes de começar
- **Forneça Etapas de Verificação** - Ajude usuários a confirmar que o setup funciona

### ❌ Não Faça Isso

- **Não Assuma que Ferramentas Estão Instaladas** - Sempre verifique e forneça instruções de instalação
- **Não Pule Variáveis de Ambiente** - Documente todas as variáveis necessárias
- **Não Use Sudo com npm** - Corrija as permissões em vez disso
- **Não Esqueça Diferenças de Plataforma** - Forneça instruções específicas para cada SO
- **Não Deixe de Incluir Verificação** - Sempre inclua etapas de teste
- **Não Use Instalações Globais** - Prefira ambientes locais/virtuais
- **Não Ignore Erros** - Documente como lidar com erros comuns
- **Não Pule Configuração de Banco de Dados** - Inclua etapas de inicialização do banco de dados

## Armadilhas Comuns

### Problema: "Comando não encontrado" após instalação
**Sintomas:** Ferramenta instalada mas terminal não a reconhece
**Solução:**
- Reinicie o terminal ou execute o arquivo de configuração do shell
- Verifique a variável de ambiente PATH
- Confirme o local da instalação
```bash
# Verificar PATH
echo $PATH

# Adicionar ao PATH (exemplo)
export PATH="/usr/local/bin:$PATH"
```

### Problema: Erros de permissão com npm/pip
**Sintomas:** Erros "EACCES" ou "Permission denied"
**Solução:**
- Não use sudo
- Corrija as permissões do npm ou use nvm
- Use ambientes virtuais para Python
```bash
# Corrigir permissões do npm
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
```

### Problema: Porta já está em uso
**Sintomas:** "Porta 3000 já está em uso"
**Solução:**
- Encontre e encerre o processo usando a porta
- Use uma porta diferente
```bash
# Encontrar processo na porta 3000
lsof -i :3000

# Encerrar processo
kill -9 <PID>

# Ou usar porta diferente
PORT=3001 npm start
```

### Problema: Falha na conexão com banco de dados
**Sintomas:** "Conexão recusada" ou "Falha de autenticação"
**Solução:**
- Verifique se o banco de dados está em execução
- Verifique a string de conexão
- Verifique as credenciais
```bash
# Verificar se PostgreSQL está em execução
sudo systemctl status postgresql

# Testar conexão
psql -h localhost -U postgres -d mydb
```

## Template de Script de Configuração

Crie um script `setup.sh` para automatizar a configuração:

```bash
#!/bin/bash

echo "🚀 Configurando ambiente de desenvolvimento..."

# Verificar pré-requisitos
command -v node >/dev/null 2>&1 || { echo "❌ Node.js não instalado"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "❌ Git não instalado"; exit 1; }

echo "✅ Verificação de pré-requisitos concluída"

# Instalar dependências
echo "📦 Instalando dependências..."
npm install

# Copiar arquivo de ambiente
if [ ! -f .env ]; then
    echo "📝 Criando arquivo .env..."
    cp .env.example .env
    echo "⚠️  Por favor, edite .env com suas configurações"
fi

# Executar migrações de banco de dados
echo "🗄️  Executando migrações de banco de dados..."
npm run migrate

# Verificar setup
echo "🔍 Verificando configuração..."
npm run test:setup

echo "✅ Configuração concluída! Execute 'npm run dev' para começar"
```

## Skills Relacionadas

- `@brainstorming` - Planeje requisitos de ambiente antes da configuração
- `@systematic-debugging` - Depure problemas de ambiente
- `@doc-coauthoring` - Crie documentação de configuração
- `@git-pushing` - Configure a configuração do Git

## Recursos Adicionais

- [Guia de Instalação do Node.js](https://nodejs.org/en/download/)
- [Ambientes Virtuais Python](https://docs.python.org/3/tutorial/venv.html)
- [Documentação do Docker](https://docs.docker.com/get-started/)
- [Homebrew (macOS)](https://brew.sh/)
- [Chocolatey (Windows)](https://chocolatey.org/)
- [nvm (Node Version Manager)](https://github.com/nvm-sh/nvm)
- [pyenv (Python Version Manager)](https://github.com/pyenv/pyenv)

---

**Dica Pro:** Crie um script `setup.sh` ou `setup.ps1` para automatizar todo o processo de configuração. Teste em um sistema limpo para garantir que funciona!