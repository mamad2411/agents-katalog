---
name: azure-cloud-security-review
description: >
  Azure上にデプロイされたリソースのセキュリティ構成を評価し、Azure Security Benchmark v3およびCIS Benchmarksに準拠しているかを検証する。
  IAM、ネットワークセキュリティ、データ暗号化、Defender for Cloud、ログ監視、Azure Policyを確認する。
  「Azureのセキュリティ監査」「クラウドセキュリティ監査」「Azure監査」「IAM監査」「NSG監査」等のキーワードで使用する。
---

# Azureクラウド セキュリティレビュー

## 目的

Azure上にデプロイされたリソースのセキュリティ構成を評価し、Azure Security Benchmark v3およびCIS Benchmarksに準拠しているかを検証する。

## 前提条件

- Azure CLIがインストールされ、対象サブスクリプションにログイン済みであること
- 対象リソースグループへの読み取り権限（Reader以上）を持っていること

## 作業指示

1. **Azure環境の全体把握を行う**
   - 以下のコマンドでリソースの全体像を確認する：
     ```bash
     # サブスクリプション一覧
     az account list --output table

     # リソースグループ一覧
     az group list --output table

     # リソース一覧
     az resource list --resource-group <rg-name> --output table
     ```

2. **IAM（Identity and Access Management）を検証する**
   - 以下を確認する：
     ```bash
     # ロール割り当ての確認
     az role assignment list --all --output table

     # カスタムロールの確認
     az role definition list --custom-role-only true --output table
     ```
   - 検証項目：
     - マネージドID（Managed Identity）が使用されているか
     - サービスプリンシパルにパスワード認証ではなく証明書認証が使用されているか
     - 最小権限の原則が適用されているか（Owner権限の付与が最小限か）
     - ゲストユーザのアクセスが適切に制限されているか
     - Privileged Identity Management（PIM）が有効化されているか

3. **ネットワークセキュリティを検証する**
   - 以下を確認する：
     ```bash
     # NSGルールの確認
     az network nsg list --output table
     az network nsg rule list --nsg-name <nsg-name> --resource-group <rg-name> --output table

     # パブリックIPの確認
     az network public-ip list --output table

     # VNet構成の確認
     az network vnet list --output table
     ```
   - 検証項目：
     - 不要なインバウンドルール（0.0.0.0/0からのSSH/RDP）がないか
     - プライベートエンドポイントが使用されているか
     - WAF（Web Application Firewall）が適用されているか
     - DDoS Protection が有効化されているか

4. **データ保護・暗号化を検証する**
   - 以下を確認する：
     ```bash
     # Key Vaultの確認
     az keyvault list --output table
     az keyvault show --name <vault-name>

     # ストレージアカウントの確認
     az storage account list --output table
     az storage account show --name <account-name> --query "{httpsOnly:enableHttpsTrafficOnly,minimumTlsVersion:minimumTlsVersion,publicAccess:allowBlobPublicAccess}"
     ```
   - 検証項目：
     - ストレージアカウントのパブリックアクセスが無効化されているか
     - HTTPSのみの通信が強制されているか
     - TLS 1.2以上が最小バージョンとして設定されているか
     - Key Vaultでシークレットが管理されているか
     - Key Vaultのソフト削除と消去保護が有効化されているか

5. **Microsoft Defender for Cloudの状態を確認する**
   - 以下を確認する：
     ```bash
     # 全サブスクリプションを対象に確認する
     for sub in $(az account list --query '[].id' -o tsv); do
       echo "== subscription: $sub =="
       az security assessment list --subscription "$sub" --output table
       az security secure-score-controls list --subscription "$sub" --output table
       az security regulatory-compliance-standards list --subscription "$sub" --output table
     done
     ```
   - 検証項目：
     - Defender for Cloudが全サブスクリプションで有効化されているか
     - セキュアスコアが70%以上であるか
     - Critical/Highの推奨事項に未対応のものがないか

6. **ログ・監視・アラートの設定を検証する**
   - 以下を確認する：
     ```bash
     # 診断設定の確認
     az monitor diagnostic-settings list --resource <resource-id> --output table

     # Log Analytics ワークスペースの確認
     az monitor log-analytics workspace list --output table

     # アクティビティログアラートの確認
     az monitor activity-log alert list --output table
     ```
   - 検証項目：
     - 主要リソースの診断ログが有効化されているか
     - Log Analyticsワークスペースにログが集約されているか
     - セキュリティイベントに対するアラートが設定されているか
     - ログの保持期間が適切に設定されているか（最低90日推奨）

7. **Azure Policyによるガバナンスを確認する**
   - 以下を確認する：
     ```bash
     # ポリシー割り当ての確認
     az policy assignment list --output table

     # ポリシーコンプライアンス状態の確認
     az policy state summarize --output table
     ```
   - 検証項目：
     - セキュリティ関連のポリシーが割り当てられているか
     - 非準拠リソースの数と内容を確認し、改善を提案する
