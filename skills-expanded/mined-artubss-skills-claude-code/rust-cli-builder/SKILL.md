---
name: rust-cli-builder
description: Planeje e construa ferramentas CLI em Rust prontas para produção usando clap para parsing de argumentos, com subcomandos, suporte a arquivo de configuração, saída colorida e tratamento adequado de erros. Usa planejamento orientado por entrevista para esclarecer comandos, formatos de entrada/saída e estratégia de distribuição antes de escrever qualquer código.
tags: [rust, cli, clap, terminal, command-line, devtools]
---

# Construtor de Ferramentas CLI em Rust

## Quando usar

Use essa habilidade quando você precisar:

- Estruturar uma nova ferramenta CLI em Rust do zero com clap
- Adicionar subcomandos a uma aplicação CLI existente
- Implementar carregamento de arquivo de configuração (TOML/JSON/YAML)
- Configurar tratamento adequado de erros com anyhow/thiserror
- Adicionar saída de terminal colorida e formatada
- Estruturar um projeto CLI para distribuição via cargo install ou GitHub releases

## Fase 1: Explorar (Modo Planejamento)

Entre em modo planejamento. Antes de escrever qualquer código, explore o projeto existente:

### Se estendendo um projeto existente
- Encontre `Cargo.toml` e verifique dependências atuais (versão do clap, serde, tokio, etc.)
- Localize o ponto de entrada da CLI (`src/main.rs` ou `src/cli.rs`)
- Verifique se clap está usando macros de derivação ou padrão de construtor
- Identifique a estrutura de subcomandos existente
- Procure por tipos de erro existentes, structs de configuração e formatação de saída
- Verifique se há um `src/lib.rs` separando lógica de biblioteca da CLI

### Se começando do zero
- Verifique o workspace para qualquer projeto Rust existente ou `Cargo.toml` de workspace
- Procure por `.cargo/config.toml` com configurações personalizadas
- Verifique `rust-toolchain.toml` para saber qual edição do Rust usar

## Fase 2: Entrevista (AskUserQuestion)

Use AskUserQuestion para esclarecer requisitos. Pergunte em rodadas.

### Rodada 1: Propósito da ferramenta e comandos

```
Pergunta: "Que tipo de ferramenta CLI você está construindo?"
Cabeçalho: "Tipo de ferramenta"
Opções:
  - "Comando único (como ripgrep, curl)" — Uma ação principal com flags e argumentos
  - "Multi-comando (como git, cargo)" — Múltiplos subcomandos sob um binário
  - "REPL interativo (como psql)" — Sessão persistente com loop de prompt
  - "Ferramenta de pipeline (como jq, sed)" — Lê stdin, transforma, escreve stdout

Pergunta: "Com o que a ferramenta operará?"
Cabeçalho: "Entrada"
Opções:
  - "Arquivos/diretórios" — Ler, processar ou gerar arquivos
  - "Rede/API" — Requisições HTTP, conexões TCP, chamadas de API
  - "Recursos do sistema" — Processos, informações de hardware, configuração do SO
  - "Fluxos de dados (stdin/stdout)" — Amigável para pipes, processamento de texto/binário
```

### Rodada 2: Subcomandos (se multi-comando)

```
Pergunta: "Descreva os subcomandos que você precisa (ex: 'init', 'build', 'deploy')"
Cabeçalho: "Comandos"
Opções:
  - "2-3 subcomandos (vou descrevê-los)" — Ferramenta pequena e focada
  - "4-8 subcomandos com grupos" — Ferramenta média, pode precisar de grupos de comandos
  - "Tenho uma lista aproximada, me ajude a projetar a API" — Design colaborativo de comandos
```

### Rodada 3: Configuração e saída

```
Pergunta: "Como a ferramenta deve ser configurada?"
Cabeçalho: "Configuração"
Opções:
  - "Apenas flags de CLI (Recomendado)" — Toda configuração via argumentos de linha de comando
  - "Arquivo de config (TOML)" — Carregue padrões de ~/.config/toolname/config.toml
  - "Arquivo de config + sobrescrita por CLI" — Arquivo de config para padrões, flags sobrescrevem valores específicos
  - "Variáveis de ambiente + flags" — Variáveis de ambiente para segredos, flags para tudo mais

Pergunta: "Que formato de saída a ferramenta precisa?"
Cabeçalho: "Saída"
Opções:
  - "Legível para humanos (texto colorido)" — Saída de terminal bonita com cores e formatação
  - "Legível para máquina (JSON)" — Saída estruturada para pipe com outras ferramentas
  - "Ambos (flag --format)" — Padrão legível para humanos, --json ou --format=json para máquinas
  - "Mínimo (códigos de saída apenas)" — Sucesso/falha via código de saída, erros para stderr
```

### Rodada 4: Operações assíncronas e tratamento de erros

```
Pergunta: "A ferramenta precisa de operações assíncronas?"
Cabeçalho: "Async"
Opções:
  - "Não — síncrono está certo (Recomendado)" — I/O de arquivo, computação, operações simples
  - "Sim — tokio (I/O de rede)" — Requisições HTTP, conexões simultâneas, I/O de arquivo assíncrono
  - "Sim — tokio multi-thread" — Paralelismo pesado, múltiplas tarefas simultâneas

Pergunta: "Como os erros devem ser apresentados aos usuários?"
Cabeçalho: "Erros"
Opções:
  - "Mensagens simples (anyhow) (Recomendado)" — Cadeias de erro legíveis para humanos, bom para maioria das CLIs
  - "Erros tipados (thiserror)" — Enum de erro personalizado com variantes específicas para cada falha
  - "Ambos (thiserror para lib, anyhow para bin)" — Código de biblioteca é tipado, CLI envolve com anyhow
```

## Fase 3: Plano (ExitPlanMode)

Escreva um plano de implementação concreto cobrindo:

1. **Estrutura do projeto** — dependências em `Cargo.toml`, layout de `src/`
2. **Definição de CLI** — structs de derivação clap para todos os comandos, args e flags
3. **Carregamento de config** — formato de arquivo de configuração e estratégia de merge com args de CLI
4. **Lógica principal** — funções principais para cada subcomando, separadas da camada de CLI
5. **Tipos de erro** — enum de erro ou uso de anyhow, mensagens de erro voltadas ao usuário
6. **Formatação de saída** — saída colorida, modo JSON, indicadores de progresso
7. **Testes** — testes unitários para lógica principal, testes de integração para comportamento de CLI

Apresente via ExitPlanMode para aprovação do usuário.

## Fase 4: Executar

Após aprovação, implemente seguindo essa ordem:

### Etapa 1: Configuração do projeto (Cargo.toml)

```toml
[package]
name = "toolname"
version = "0.1.0"
edition = "2021"
description = "Descrição curta da ferramenta"

[dependencies]
clap = { version = "4", features = ["derive", "env"] }
serde = { version = "1", features = ["derive"] }
anyhow = "1"
# Adicione com base na entrevista:
# thiserror = "2"              # se erros tipados
# tokio = { version = "1", features = ["full"] }  # se async
# serde_json = "1"             # se saída JSON
# toml = "0.8"                 # se config TOML
# colored = "2"                # se saída colorida
# indicatif = "0.17"           # se barras de progresso
# dirs = "5"                   # se arquivo de config (~/.config/)
```

### Etapa 2: Definição de CLI com clap derive

```rust
use clap::{Parser, Subcommand};

/// Descrição de uma linha curta da ferramenta
#[derive(Parser, Debug)]
#[command(name = "toolname", version, about, long_about = None)]
pub struct Cli {
    /// Aumentar verbosidade (-v, -vv, -vvv)
    #[arg(short, long, action = clap::ArgAction::Count, global = true)]
    pub verbose: u8,

    /// Formato de saída
    #[arg(long, default_value = "text", global = true)]
    pub format: OutputFormat,

    /// Caminho do arquivo de configuração
    #[arg(long, global = true)]
    pub config: Option<std::path::PathBuf>,

    #[command(subcommand)]
    pub command: Commands,
}

#[derive(Subcommand, Debug)]
pub enum Commands {
    /// Inicializar um novo projeto
    Init {
        /// Nome do projeto
        name: String,

        /// Template a usar
        #[arg(short, long, default_value = "default")]
        template: String,
    },

    /// Construir o projeto
    Build {
        /// Construir em modo release
        #[arg(short, long)]
        release: bool,

        /// Diretório de saída
        #[arg(short, long)]
        output: Option<std::path::PathBuf>,
    },

    /// Mostrar status do projeto
    Status,
}

#[derive(clap::ValueEnum, Clone, Debug)]
pub enum OutputFormat {
    Text,
    Json,
}
```

### Etapa 3: Tratamento de erros

```rust
// Com anyhow (abordagem simples):
use anyhow::{Context, Result};

fn load_config(path: &Path) -> Result<Config> {
    let content = std::fs::read_to_string(path)
        .with_context(|| format!("Falha ao ler arquivo de config: {}", path.display()))?;
    let config: Config = toml::from_str(&content)
        .context("TOML inválido no arquivo de config")?;
    Ok(config)
}

// Com thiserror (abordagem tipada):
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Arquivo de config não encontrado: {path}")]
    ConfigNotFound { path: std::path::PathBuf },

    #[error("Config inválida: {0}")]
    InvalidConfig(#[from] toml::de::Error),

    #[error("Erro de rede: {0}")]
    Network(#[from] reqwest::Error),

    #[error("{0}")]
    Custom(String),
}
```

### Etapa 4: Carregamento de arquivo de configuração

```rust
use serde::Deserialize;
use std::path::{Path, PathBuf};

#[derive(Deserialize, Debug, Default)]
pub struct Config {
    pub default_template: Option<String>,
    pub output_dir: Option<PathBuf>,
    // ... campos da entrevista
}

impl Config {
    pub fn load(explicit_path: Option<&Path>) -> anyhow::Result<Self> {
        let path = match explicit_path {
            Some(p) => p.to_path_buf(),
            None => Self::default_path(),
        };

        if !path.exists() {
            return Ok(Config::default());
        }

        let content = std::fs::read_to_string(&path)?;
        let config: Config = toml::from_str(&content)?;
        Ok(config)
    }

    fn default_path() -> PathBuf {
        dirs::config_dir()
            .unwrap_or_else(|| PathBuf::from("."))
            .join("toolname")
            .join("config.toml")
    }
}
```

### Etapa 5: Saída colorida e formatação

```rust
use colored::Colorize;

pub struct Output {
    format: OutputFormat,
    verbose: u8,
}

impl Output {
    pub fn new(format: OutputFormat, verbose: u8) -> Self {
        Self { format, verbose }
    }

    pub fn success(&self, msg: &str) {
        match self.format {
            OutputFormat::Text => eprintln!("{} {}", "✓".green().bold(), msg),
            OutputFormat::Json => {} // Saída JSON vai apenas para stdout
        }
    }

    pub fn error(&self, msg: &str) {
        match self.format {
            OutputFormat::Text => eprintln!("{} {}", "✗".red().bold(), msg),
            OutputFormat::Json => {
                let err = serde_json::json!({"error": msg});
                println!("{}", serde_json::to_string(&err).unwrap());
            }
        }
    }

    pub fn info(&self, msg: &str) {
        if self.verbose >= 1 {
            match self.format {
                OutputFormat::Text => eprintln!("{} {}", "ℹ".blue(), msg),
                OutputFormat::Json => {}
            }
        }
    }

    pub fn data<T: serde::Serialize>(&self, data: &T) {
        match self.format {
            OutputFormat::Text => {
                // Pretty print para humanos — customize por subcomando
                println!("{:#?}", data);
            }
            OutputFormat::Json => {
                println!("{}", serde_json::to_string_pretty(data).unwrap());
            }
        }
    }
}
```

### Etapa 6: Ponto de entrada principal

```rust
use clap::Parser;

fn main() -> anyhow::Result<()> {
    let cli = Cli::parse();
    let config = Config::load(cli.config.as_deref())?;
    let output = Output::new(cli.format.clone(), cli.verbose);

    match cli.command {
        Commands::Init { name, template } => {
            cmd_init(&name, &template, &config, &output)?;
        }
        Commands::Build { release, output_dir } => {
            let dir = output_dir
                .or(config.output_dir.clone())
                .unwrap_or_else(|| PathBuf::from("./dist"));
            cmd_build(release, &dir, &output)?;
        }
        Commands::Status => {
            cmd_status(&config, &output)?;
        }
    }

    Ok(())
}

// Se async (tokio):
// #[tokio::main]
// async fn main() -> anyhow::Result<()> { ... }
```

### Etapa 7: Implementações de subcomandos

```rust
fn cmd_init(name: &str, template: &str, config: &Config, out: &Output) -> anyhow::Result<()> {
    let template = if template == "default" {
        config.default_template.as_deref().unwrap_or("default")
    } else {
        template
    };

    out.info(&format!("Usando template: {}", template));

    let project_dir = Path::new(name);
    if project_dir.exists() {
        anyhow::bail!("Diretório '{}' já existe", name);
    }

    std::fs::create_dir_all(project_dir)?;
    // ... scaffold arquivos de projeto baseado em template

    out.success(&format!("Projeto '{}' criado com template '{}'", name, template));
    Ok(())
}
```

### Etapa 8: Testes

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_config_default() {
        let config = Config::default();
        assert!(config.default_template.is_none());
    }

    #[test]
    fn test_config_parse_toml() {
        let toml_str = r#"
            default_template = "react"
            output_dir = "./build"
        "#;
        let config: Config = toml::from_str(toml_str).unwrap();
        assert_eq!(config.default_template.unwrap(), "react");
    }
}

// Testes de integração (tests/cli.rs):
use assert_cmd::Command;
use predicates::prelude::*;

#[test]
fn test_help_flag() {
    Command::cargo_bin("toolname")
        .unwrap()
        .arg("--help")
        .assert()
        .success()
        .stdout(predicate::str::contains("Usage:"));
}

#[test]
fn test_version_flag() {
    Command::cargo_bin("toolname")
        .unwrap()
        .arg("--version")
        .assert()
        .success();
}

#[test]
fn test_init_creates_directory() {
    let dir = tempfile::tempdir().unwrap();
    let project_name = dir.path().join("test-project");

    Command::cargo_bin("toolname")
        .unwrap()
        .args(["init", project_name.to_str().unwrap()])
        .assert()
        .success();

    assert!(project_name.exists());
}

#[test]
fn test_init_existing_directory_fails() {
    let dir = tempfile::tempdir().unwrap();

    Command::cargo_bin("toolname")
        .unwrap()
        .args(["init", dir.path().to_str().unwrap()])
        .assert()
        .failure()
        .stderr(predicate::str::contains("já existe"));
}

#[test]
fn test_json_output_format() {
    Command::cargo_bin("toolname")
        .unwrap()
        .args(["--format", "json", "status"])
        .assert()
        .success()
        .stdout(predicate::str::starts_with("{"));
}
```

## Referência de estrutura de projeto

```
toolname/
├── Cargo.toml
├── src/
│   ├── main.rs          # Ponto de entrada, parsing de CLI, dispatch de comando
│   ├── cli.rs           # Structs de derivação clap (Cli, Commands, Args)
│   ├── config.rs        # Carregamento de arquivo de config e merge
│   ├── output.rs        # Formatação de saída (texto/JSON/colorida)
│   ├── error.rs         # Tipos de erro (se usando thiserror)
│   └── commands/
│       ├── mod.rs
│       ├── init.rs      # Lógica do subcomando init
│       ├── build.rs     # Lógica do subcomando build
│       └── status.rs    # Lógica do subcomando status
└── tests/
    └── cli.rs           # Testes de integração com assert_cmd
```

## Melhores práticas

### Separe CLI de lógica
Mantenha structs de clap e parsing de argumentos em `cli.rs`. Coloque lógica de negócios em `commands/`. Isso torna a lógica principal testável sem invocar a CLI.

### Use stderr para status, stdout para dados
Mensagens legíveis para humanos (progresso, sucesso, erros) vão para `stderr`. Dados legíveis para máquina vão para `stdout`. Isso permite aos usuários fazer pipe de saída perfeitamente: `toolname status --format json | jq '.items'`.

### Respeite NO_COLOR
Verifique a variável de ambiente `NO_COLOR` e desabilite cores quando ela estiver definida:
```rust
if std::env::var("NO_COLOR").is_ok() {
    colored::control::set_override(false);
}
```

### Códigos de saída
Use códigos de saída significativos: 0 para sucesso, 1 para erros gerais, 2 para erros de uso (clap lida automaticamente).

### Dependências de desenvolvimento para testes

```toml
[dev-dependencies]
assert_cmd = "2"
predicates = "3"
tempfile = "3"
```

## Checklist antes de terminar

- [ ] Structs de derivação `clap` têm comentários de documentação (viram texto de --help)
- [ ] Todos os subcomandos têm descrições curtas e longas
- [ ] Arquivo de config tem padrões sensatos e não gera erro quando ausente
- [ ] `--format json` emite JSON válido e analisável para stdout
- [ ] Erros mostram contexto (caminhos de arquivo, o que deu errado, como corrigir)
- [ ] Testes de integração verificam comportamento de CLI fim-a-fim
- [ ] `cargo clippy` passa sem avisos
- [ ] `cargo fmt` foi executado