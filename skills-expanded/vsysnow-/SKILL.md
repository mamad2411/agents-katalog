# Regras do Cursor para o Projeto SysNow

## Contexto do Projeto
SysNow é um aplicativo CLI desenvolvido em V (Vlang) para gerenciar tickets entre SysAid e ServiceNow. O projeto integra duas APIs REST, formatando e migrando dados entre os sistemas.

## Linguagem e Framework
- **Linguagem**: V (Vlang)
- **Gerenciamento de dependências**: v.mod
- **Configuração**: TOML (config.toml)
- **Estrutura**: Modular, com módulos separados por funcionalidade

## Convenções de Código

### Estrutura e Organização
- Manter estrutura modular: cada funcionalidade em seu próprio módulo
- Módulos devem estar em diretórios separados (config/, sysaid/, servicenow/, json/, utils/)
- Usar `module nome_modulo` no início de cada arquivo .v
- Funções públicas devem usar `pub fn`
- Structs públicas devem usar `pub struct` com campos `pub:`

### Nomenclatura
- **Variáveis e funções**: português (ex: `senha`, `login`, `list_tickets`)
- **Structs**: PascalCase em inglês (ex: `Config`, `SysAidConfig`)
- **Módulos**: lowercase (ex: `config`, `sysaid`, `servicenow`)
- **Constantes**: UPPER_SNAKE_CASE se necessário

### Tratamento de Erros
- Sempre usar `!` para funções que podem retornar erros
- Usar `or {}` para ignorar erros quando apropriado
- Usar `or { return error('mensagem') }` para propagar erros com contexto
- Mensagens de erro em português
- Sempre limpar arquivos temporários mesmo em caso de erro

### Variáveis
- Variáveis são imutáveis por padrão
- Usar `mut` apenas quando necessário modificar a variável
- Preferir variáveis locais sobre globais

### Comentários
- Comentários em português
- Comentários descritivos para funções complexas
- Comentários inline para explicar lógica não óbvia

### APIs e Requisições HTTP
- Usar `os.execute()` com curl para requisições HTTP
- Sempre salvar cookies em `cookies.txt` para autenticação
- Limpar arquivos temporários após uso (login_data.json, response.json, etc.)
- Validar JSON recebido antes de processar

### Configuração
- Carregar configuração do arquivo `config.toml`
- Validar ambientes: dev, prod, sandbox
- Nunca commitar `config.toml` (já está no .gitignore)
- Usar `config_template.toml` como template

### Validação e Segurança
- Validar environment antes de usar
- Validar JSON antes de processar
- Verificar existência de arquivos antes de ler
- Limpar arquivos sensíveis (cookies, credenciais temporárias)

### Logs e Saída
- Usar `println()` para logs e saída do programa
- Mensagens de erro claras e descritivas
- Logs em português
- Exibir informações úteis (ex: JSESSIONID após login)

### Estrutura de Arquivos Temporários
- `cookies.txt`: cookies de sessão do SysAid
- `response.json`: resposta JSON das APIs
- `login_data.json`: dados temporários de login (deve ser removido imediatamente)
- Todos os arquivos temporários devem ser limpos por `utils.cleanup_files()`

## Padrões Específicos do Projeto

### Módulo config
- Structs com tags `@[toml: nome_campo]` para deserialização TOML
- Função `load_config() !Config` para carregar configuração
- Função `is_valid_environment(env string) bool` para validar ambientes

### Módulo sysaid
- Função `login()` que retorna `!` (pode falhar)
- Função `list_tickets()` que retorna `!string` (JSON como string)
- Usar cookies para autenticação em requisições subsequentes

### Módulo servicenow
- Enviar tickets formatados para ServiceNow
- Validar se ServiceNow está configurado antes de tentar enviar

### Módulo json
- Validar JSON recebido
- Formatar e exibir tickets
- Processar apenas campos úteis do SysAid

### Módulo utils
- Função `cleanup_files()` para limpar arquivos temporários
- Função `show_help()` para exibir ajuda

## Boas Práticas

1. **Sempre** limpar arquivos temporários, mesmo em caso de erro
2. **Sempre** validar entrada antes de processar
3. **Sempre** tratar erros adequadamente
4. **Nunca** commitar credenciais ou arquivos de configuração com dados sensíveis
5. **Sempre** usar tratamento de erros com `!` e `or {}`
6. **Sempre** validar JSON antes de processar
7. **Sempre** verificar se arquivos existem antes de ler/escrever
8. Preferir funções pequenas e focadas
9. Manter código legível e bem comentado
10. Seguir a estrutura modular existente

## Quando Adicionar Código

- Adicionar novas funcionalidades em módulos apropriados
- Manter compatibilidade com a estrutura existente
- Adicionar validações quando necessário
- Documentar funções públicas
- Manter consistência com o estilo existente

## Quando Modificar Código Existente

- Manter a mesma estrutura de tratamento de erros
- Manter os mesmos padrões de nomenclatura
- Não quebrar funcionalidades existentes
- Adicionar comentários se a lógica mudar significativamente

## Observações Importantes

- O projeto usa chamadas de sistema (curl, jq) via `os.execute()`
- Arquivos temporários são criados durante a execução e devem ser limpos
- A autenticação usa cookies armazenados em arquivo
- O projeto suporta múltiplos ambientes (dev, prod, sandbox)
- Logs são enviados via stdout padrão

