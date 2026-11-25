---
name: Scripts Shell para Produção em Linux
description: Esta skill deve ser usada quando o usuário solicita "criar scripts bash", "automatizar tarefas do Linux", "monitorar recursos do sistema", "fazer backup de arquivos", "gerenciar usuários" ou "escrever scripts shell para produção". Fornece templates prontos para produção de scripts shell para administração de sistemas.
metadata:
  author: zebbern
  version: "1.1"
---

# Scripts Shell para Produção em Linux

## Propósito

Fornecer templates de scripts shell prontos para produção para tarefas comuns de administração de sistemas Linux, incluindo backups, monitoramento, gerenciamento de usuários, análise de logs e automação. Esses scripts servem como blocos de construção para operações de segurança e ambientes de testes de penetração.

## Pré-requisitos

### Ambiente Necessário
- Sistema Linux/Unix (shell bash)
- Permissões apropriadas para as tarefas
- Utilitários necessários instalados (rsync, openssl, etc.)

### Conhecimento Necessário
- Scripting bash básico
- Estrutura do sistema de arquivos Linux
- Conceitos de administração de sistemas

## Resultados e Entregas

1. **Soluções de Backup** - Backups automatizados de arquivos e bancos de dados
2. **Scripts de Monitoramento** - Rastreamento de uso de recursos
3. **Ferramentas de Automação** - Execução de tarefas agendadas
4. **Scripts de Segurança** - Gerenciamento de senhas, encriptação

## Fluxo de Trabalho Principal

### Fase 1: Scripts de Backup de Arquivos

**Backup Básico de Diretório**
```bash
#!/bin/bash
backup_dir="/path/to/backup"
source_dir="/path/to/source"

# Criar um backup com timestamp do diretório de origem
tar -czf "$backup_dir/backup_$(date +%Y%m%d_%H%M%S).tar.gz" "$source_dir"
echo "Backup completed: backup_$(date +%Y%m%d_%H%M%S).tar.gz"
```

**Backup para Servidor Remoto**
```bash
#!/bin/bash
source_dir="/path/to/source"
remote_server="user@remoteserver:/path/to/backup"

# Fazer backup de arquivos/diretórios para um servidor remoto usando rsync
rsync -avz --progress "$source_dir" "$remote_server"
echo "Files backed up to remote server."
```

**Script de Rotação de Backups**
```bash
#!/bin/bash
backup_dir="/path/to/backups"
max_backups=5

# Rotacionar backups deletando o mais antigo se exceder max_backups
while [ $(ls -1 "$backup_dir" | wc -l) -gt "$max_backups" ]; do
    oldest_backup=$(ls -1t "$backup_dir" | tail -n 1)
    rm -r "$backup_dir/$oldest_backup"
    echo "Removed old backup: $oldest_backup"
done
echo "Backup rotation completed."
```

**Script de Backup de Banco de Dados**
```bash
#!/bin/bash
database_name="your_database"
db_user="username"
db_pass="password"
output_file="database_backup_$(date +%Y%m%d).sql"

# Realizar backup do banco de dados usando mysqldump
mysqldump -u "$db_user" -p"$db_pass" "$database_name" > "$output_file"
gzip "$output_file"
echo "Database backup created: $output_file.gz"
```

### Fase 2: Scripts de Monitoramento do Sistema

**Monitor de Uso de CPU**
```bash
#!/bin/bash
threshold=90

# Monitorar uso de CPU e acionador alerta se limite excedido
cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d. -f1)

if [ "$cpu_usage" -gt "$threshold" ]; then
    echo "ALERT: High CPU usage detected: $cpu_usage%"
    # Adicionar lógica de notificação (email, slack, etc.)
    # mail -s "CPU Alert" admin@example.com <<< "CPU usage: $cpu_usage%"
fi
```

**Monitor de Espaço em Disco**
```bash
#!/bin/bash
threshold=90
partition="/dev/sda1"

# Monitorar uso de disco e acionar alerta se limite excedido
disk_usage=$(df -h | grep "$partition" | awk '{print $5}' | cut -d% -f1)

if [ "$disk_usage" -gt "$threshold" ]; then
    echo "ALERT: High disk usage detected: $disk_usage%"
    # Adicionar lógica de alerta/notificação aqui
fi
```

**Logger de Uso de CPU**
```bash
#!/bin/bash
output_file="cpu_usage_log.txt"

# Registrar uso de CPU atual em arquivo com timestamp
timestamp=$(date '+%Y-%m-%d %H:%M:%S')
cpu_usage=$(top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d. -f1)
echo "$timestamp - CPU Usage: $cpu_usage%" >> "$output_file"
echo "CPU usage logged."
```

**Verificação de Saúde do Sistema**
```bash
#!/bin/bash
output_file="system_health_check.txt"

# Realizar verificação de saúde do sistema e salvar resultados em arquivo
{
    echo "System Health Check - $(date)"
    echo "================================"
    echo ""
    echo "Uptime:"
    uptime
    echo ""
    echo "Load Average:"
    cat /proc/loadavg
    echo ""
    echo "Memory Usage:"
    free -h
    echo ""
    echo "Disk Usage:"
    df -h
    echo ""
    echo "Top Processes:"
    ps aux --sort=-%cpu | head -10
} > "$output_file"

echo "System health check saved to $output_file"
```

### Fase 3: Scripts de Gerenciamento de Usuários

**Criação de Conta de Usuário**
```bash
#!/bin/bash
username="newuser"

# Verificar se usuário existe; se não, criar novo usuário
if id "$username" &>/dev/null; then
    echo "User $username already exists."
else
    useradd -m -s /bin/bash "$username"
    echo "User $username created."
    
    # Definir senha interativamente
    passwd "$username"
fi
```

**Verificador de Expiração de Senha**
```bash
#!/bin/bash
output_file="password_expiry_report.txt"

# Verificar expiração de senha para usuários com shell bash
echo "Password Expiry Report - $(date)" > "$output_file"
echo "=================================" >> "$output_file"

IFS=$'\n'
for user in $(grep "/bin/bash" /etc/passwd | cut -d: -f1); do
    password_expires=$(chage -l "$user" 2>/dev/null | grep "Password expires" | awk -F: '{print $2}')
    echo "User: $user - Password Expires: $password_expires" >> "$output_file"
done
unset IFS

echo "Password expiry report saved to $output_file"
```

### Fase 4: Scripts de Segurança

**Gerador de Senha**
```bash
#!/bin/bash
length=${1:-16}

# Gerar uma senha aleatória
password=$(openssl rand -base64 48 | tr -dc 'a-zA-Z0-9!@#$%^&*' | head -c"$length")
echo "Generated password: $password"
```

**Script de Encriptação de Arquivo**
```bash
#!/bin/bash
file="$1"
action="${2:-encrypt}"

if [ -z "$file" ]; then
    echo "Usage: $0 <file> [encrypt|decrypt]"
    exit 1
fi

if [ "$action" == "encrypt" ]; then
    # Encriptar arquivo usando AES-256-CBC
    openssl enc -aes-256-cbc -salt -pbkdf2 -in "$file" -out "$file.enc"
    echo "File encrypted: $file.enc"
elif [ "$action" == "decrypt" ]; then
    # Descriptografar arquivo
    output_file="${file%.enc}"
    openssl enc -aes-256-cbc -d -pbkdf2 -in "$file" -out "$output_file"
    echo "File decrypted: $output_file"
fi
```

### Fase 5: Scripts de Análise de Logs

**Extrator de Log de Erro**
```bash
#!/bin/bash
logfile="${1:-/var/log/syslog}"
output_file="error_log_$(date +%Y%m%d).txt"

# Extrair linhas com "ERROR" do arquivo de log
grep -i "error\|fail\|critical" "$logfile" > "$output_file"
echo "Error log created: $output_file"
echo "Total errors found: $(wc -l < "$output_file")"
```

**Analisador de Log de Servidor Web**
```bash
#!/bin/bash
log_file="${1:-/var/log/apache2/access.log}"

echo "Web Server Log Analysis"
echo "========================"
echo ""
echo "Top 10 IP Addresses:"
awk '{print $1}' "$log_file" | sort | uniq -c | sort -rn | head -10
echo ""
echo "Top 10 Requested URLs:"
awk '{print $7}' "$log_file" | sort | uniq -c | sort -rn | head -10
echo ""
echo "HTTP Status Code Distribution:"
awk '{print $9}' "$log_file" | sort | uniq -c | sort -rn
```

### Fase 6: Scripts de Rede

**Verificador de Conectividade de Rede**
```bash
#!/bin/bash
hosts=("8.8.8.8" "1.1.1.1" "google.com")

echo "Network Connectivity Check"
echo "=========================="

for host in "${hosts[@]}"; do
    if ping -c 1 -W 2 "$host" &>/dev/null; then
        echo "[UP] $host is reachable"
    else
        echo "[DOWN] $host is unreachable"
    fi
done
```

**Verificador de Disponibilidade de Website**
```bash
#!/bin/bash
websites=("https://google.com" "https://github.com")
log_file="uptime_log.txt"

echo "Website Uptime Check - $(date)" >> "$log_file"

for website in "${websites[@]}"; do
    if curl --output /dev/null --silent --head --fail --max-time 10 "$website"; then
        echo "[UP] $website is accessible" | tee -a "$log_file"
    else
        echo "[DOWN] $website is inaccessible" | tee -a "$log_file"
    fi
done
```

**Informações de Interface de Rede**
```bash
#!/bin/bash
interface="${1:-eth0}"

echo "Network Interface Information: $interface"
echo "========================================="
ip addr show "$interface" 2>/dev/null || ifconfig "$interface" 2>/dev/null
echo ""
echo "Routing Table:"
ip route | grep "$interface"
```

### Fase 7: Scripts de Automação

**Instalação Automatizada de Pacotes**
```bash
#!/bin/bash
packages=("vim" "htop" "curl" "wget" "git")

echo "Installing packages..."

for package in "${packages[@]}"; do
    if dpkg -l | grep -q "^ii  $package"; then
        echo "[SKIP] $package is already installed"
    else
        sudo apt-get install -y "$package"
        echo "[INSTALLED] $package"
    fi
done

echo "Package installation completed."
```

**Agendador de Tarefas (Configuração de Cron)**
```bash
#!/bin/bash
scheduled_task="/path/to/your_script.sh"
schedule_time="0 2 * * *"  # Executar às 2 da manhã diariamente

# Adicionar tarefa ao crontab
(crontab -l 2>/dev/null; echo "$schedule_time $scheduled_task") | crontab -
echo "Task scheduled: $schedule_time $scheduled_task"
```

**Script de Reinicialização de Serviço**
```bash
#!/bin/bash
service_name="${1:-apache2}"

# Reiniciar um serviço especificado
if systemctl is-active --quiet "$service_name"; then
    echo "Restarting $service_name..."
    sudo systemctl restart "$service_name"
    echo "Service $service_name restarted."
else
    echo "Service $service_name is not running. Starting..."
    sudo systemctl start "$service_name"
    echo "Service $service_name started."
fi
```

### Fase 8: Operações de Arquivo

**Sincronização de Diretório**
```bash
#!/bin/bash
source_dir="/path/to/source"
destination_dir="/path/to/destination"

# Sincronizar diretórios usando rsync
rsync -avz --delete "$source_dir/" "$destination_dir/"
echo "Directories synchronized successfully."
```

**Script de Limpeza de Dados**
```bash
#!/bin/bash
directory="${1:-/tmp}"
days="${2:-7}"

echo "Cleaning files older than $days days in $directory"

# Remover arquivos mais antigos que o número especificado de dias
find "$directory" -type f -mtime +"$days" -exec rm -v {} \;
echo "Cleanup completed."
```

**Verificador de Tamanho de Pasta**
```bash
#!/bin/bash
folder_path="${1:-.}"

echo "Folder Size Analysis: $folder_path"
echo "===================================="

# Exibir tamanhos de subdiretórios ordenados por tamanho
du -sh "$folder_path"/* 2>/dev/null | sort -rh | head -20
echo ""
echo "Total size:"
du -sh "$folder_path"
```

### Fase 9: Informações do Sistema

**Coletor de Informações do Sistema**
```bash
#!/bin/bash
output_file="system_info_$(hostname)_$(date +%Y%m%d).txt"

{
    echo "System Information Report"
    echo "Generated: $(date)"
    echo "========================="
    echo ""
    echo "Hostname: $(hostname)"
    echo "OS: $(uname -a)"
    echo ""
    echo "CPU Info:"
    lscpu | grep -E "Model name|CPU\(s\)|Thread"
    echo ""
    echo "Memory:"
    free -h
    echo ""
    echo "Disk Space:"
    df -h
    echo ""
    echo "Network Interfaces:"
    ip -br addr
    echo ""
    echo "Logged In Users:"
    who
} > "$output_file"

echo "System info saved to $output_file"
```

### Fase 10: Git e Desenvolvimento

**Atualizador de Repositório Git**
```bash
#!/bin/bash
git_repos=("/path/to/repo1" "/path/to/repo2")

for repo in "${git_repos[@]}"; do
    if [ -d "$repo/.git" ]; then
        echo "Updating repository: $repo"
        cd "$repo"
        git fetch --all
        git pull origin "$(git branch --show-current)"
        echo "Updated: $repo"
    else
        echo "Not a git repository: $repo"
    fi
done

echo "All repositories updated."
```

**Execução de Script Remoto**
```bash
#!/bin/bash
remote_server="${1:-user@remote-server}"
remote_script="${2:-/path/to/remote/script.sh}"

# Executar um script em um servidor remoto via SSH
ssh "$remote_server" "bash -s" < "$remote_script"
echo "Remote script executed on $remote_server"
```

## Referência Rápida

### Padrões de Script Comuns

| Padrão | Propósito |
|--------|-----------|
| `#!/bin/bash` | Shebang para bash |
| `$(date +%Y%m%d)` | Formatação de data |
| `$((expression))` | Aritmética |
| `${var:-default}` | Valor padrão |
| `"$@"` | Todos os argumentos |

### Comandos Úteis

| Comando | Propósito |
|---------|-----------|
| `chmod +x script.sh` | Tornar executável |
| `./script.sh` | Executar script |
| `nohup ./script.sh &` | Executar em background |
| `crontab -e` | Editar tarefas cron |
| `source script.sh` | Executar no shell atual |

### Formato de Cron
Minuto(0-59) Hora(0-23) Dia(1-31) Mês(1-12) Dia da Semana(0-7, 0/7=Dom)

## Restrições e Limitações

- Sempre teste scripts em ambiente não-produção primeiro
- Use caminhos absolutos para evitar erros
- Coloque entre aspas as variáveis para lidar com espaços apropriadamente
- Muitos scripts requerem privilégios de root/sudo
- Use `bash -x script.sh` para depuração