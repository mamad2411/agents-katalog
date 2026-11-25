---
name: gcp-patterns
description: "Google Cloud patterns: full GKE Workload Identity setup, Cloud Run with VPC access and secrets, keyless GitHub Actions OIDC to GCP, VPC and subnet design, and Cloud SQL Proxy for local development. Use when provisioning or connecting workloads on Google Cloud."
---

# GCP Patterns

GKE Workload Identity, Cloud Run deployment, Cloud SQL private IP, Terraform Google provider, and Cloud Armor patterns.

## GKE Workload Identity (Full Setup)

```hcl
# 1. Enable Workload Identity on cluster (already in cluster config)
# workload_identity_config { workload_pool = "${project}.svc.id.goog" }

# 2. Create GCP Service Account
resource "google_service_account" "app" {
  account_id   = "myapp-${var.env}"
  display_name = "MyApp ${var.env} workload identity SA"
}

# 3. Grant permissions to the GCP SA
resource "google_project_iam_member" "app_sql" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.app.email}"
}

resource "google_secret_manager_secret_iam_member" "app_secrets" {
  secret_id = google_secret_manager_secret.db_password.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.app.email}"
}

# 4. Allow K8s SA to impersonate GCP SA (the binding)
resource "google_service_account_iam_member" "wi_binding" {
  service_account_id = google_service_account.app.name
  role               = "roles/iam.workloadIdentityUser"
  # Format: serviceAccount:{project}.svc.id.goog[{namespace}/{k8s-sa-name}]
  member             = "serviceAccount:${var.project_id}.svc.id.goog[${var.namespace}/${var.k8s_sa_name}]"
}
```

```yaml
# 5. Kubernetes ServiceAccount with annotation
apiVersion: v1
kind: ServiceAccount
metadata:
  name: myapp-sa
  namespace: myapp
  annotations:
    iam.gke.io/gcp-service-account: myapp-prod@myproject.iam.gserviceaccount.com

---
# 6. Deployment using the annotated service account
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      serviceAccountName: myapp-sa
      containers:
        - name: app
          image: us-central1-docker.pkg.dev/myproject/myapp:v1.0.0
          # App uses google.auth.default() / Application Default Credentials
          # GKE automatically injects projected tokens
```

## Cloud Run with VPC and Secrets

```hcl
# VPC Access for Cloud Run (reach Cloud SQL via private IP)
resource "google_vpc_access_connector" "connector" {
  name          = "myapp-connector"
  region        = "us-central1"
  ip_cidr_range = "10.8.0.0/28"   # /28 required
  network       = google_compute_network.main.name
  min_instances = 2
  max_instances = 10
  machine_type  = "e2-micro"
}

# Secret Manager secret
resource "google_secret_manager_secret" "db_password" {
  secret_id = "myapp-db-password"
  replication {
    auto {}   # Automatic global replication
  }
}

resource "google_secret_manager_secret_version" "db_password" {
  secret      = google_secret_manager_secret.db_password.id
  secret_data = var.db_password
}

# Cloud Run service
resource "google_cloud_run_v2_service" "app" {
  name     = "myapp"
  location = "us-central1"

  template {
    service_account = google_service_account.app.email

    scaling {
      min_instance_count = 0    # Scale to zero (cold start)
      max_instance_count = 10
    }

    containers {
      image = "us-central1-docker.pkg.dev/${var.project_id}/myapp:${var.image_tag}"

      env {
        name  = "DB_HOST"
        value = google_sql_database_instance.postgres.private_ip_address
      }

      env {
        name = "DB_PASSWORD"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.db_password.secret_id
            version = "latest"
          }
        }
      }

      resources {
        limits = { cpu = "1", memory = "512Mi" }
      }
    }

    vpc_access {
      connector = google_vpc_access_connector.connector.id
      egress    = "PRIVATE_RANGES_ONLY"
    }
  }
}

# Allow public traffic (unauthenticated)
resource "google_cloud_run_v2_service_iam_member" "public" {
  location = google_cloud_run_v2_service.app.location
  name     = google_cloud_run_v2_service.app.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
```

## GitHub Actions OIDC for GCP (No Keys)

```yaml
# .github/workflows/deploy.yml
name: Deploy to GCP
on:
  push:
    branches: [main]

permissions:
  contents: read
  id-token: write    # Required for OIDC token

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - id: auth
        name: Authenticate to GCP via OIDC
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-pool/providers/github-provider
          service_account: deploy-sa@myproject.iam.gserviceaccount.com

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      - name: Build and push to Artifact Registry
        run: |
          gcloud auth configure-docker us-central1-docker.pkg.dev
          docker build -t us-central1-docker.pkg.dev/$PROJECT_ID/myapp:$GITHUB_SHA .
          docker push us-central1-docker.pkg.dev/$PROJECT_ID/myapp:$GITHUB_SHA

      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy myapp \
            --image us-central1-docker.pkg.dev/$PROJECT_ID/myapp:$GITHUB_SHA \
            --region us-central1 \
            --platform managed
```

```hcl
# Terraform: Workload Identity Pool for GitHub Actions
resource "google_iam_workload_identity_pool" "github" {
  workload_identity_pool_id = "github-pool"
  display_name              = "GitHub Actions"
}

resource "google_iam_workload_identity_pool_provider" "github" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-provider"

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.actor"      = "assertion.actor"
    "attribute.repository" = "assertion.repository"
  }

  attribute_condition = "assertion.repository == 'myorg/myrepo'"
}

resource "google_service_account_iam_member" "github_wi" {
  service_account_id = google_service_account.deploy.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository/myorg/myrepo"
}
```

## GCP Networking (VPC and Subnets)

```hcl
resource "google_compute_network" "main" {
  name                    = "main-vpc"
  auto_create_subnetworks = false  # Manual subnets for full control
}

resource "google_compute_subnetwork" "main" {
  name          = "main-subnet"
  region        = "us-central1"
  network       = google_compute_network.main.id
  ip_cidr_range = "10.0.0.0/20"

  # Secondary ranges for GKE pods and services
  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = "100.64.0.0/14"
  }
  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = "100.68.0.0/20"
  }

  private_ip_google_access = true  # Access Google APIs without external IP
  log_config {
    aggregation_interval = "INTERVAL_5_SEC"
    flow_sampling        = 0.5
    metadata             = "INCLUDE_ALL_METADATA"
  }
}

# Cloud NAT for private instances to reach internet
resource "google_compute_router_nat" "main" {
  name   = "main-nat"
  router = google_compute_router.main.name
  region = "us-central1"

  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"

  log_config {
    enable = true
    filter = "ERRORS_ONLY"
  }
}
```

## Cloud SQL Proxy (Local Development)

```bash
# Download Cloud SQL Proxy
curl -Lo cloud-sql-proxy https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.7.0/cloud-sql-proxy.linux.amd64
chmod +x cloud-sql-proxy

# Connect to Cloud SQL via proxy (uses ADC credentials)
./cloud-sql-proxy --port 5432 \
  myproject:us-central1:prod-postgres &

# Then connect normally
psql -h 127.0.0.1 -U myapp -d myapp

# Using Cloud SQL Auth Proxy in Kubernetes sidecar
# (alternative to private IP + VPC connector)
```
