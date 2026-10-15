---
name: aspnet-deployment
description: Publicación y despliegue de aplicaciones ASP.NET Core. Cubre IIS, Docker, Azure App Service, reverse proxy (YARP, nginx), HTTPS, certificados, variables de entorno, CI/CD con GitHub Actions y Azure DevOps, migraciones en producción, y hardening. Actívala al preparar una aplicación para producción, configurar CI/CD, o migrar entre entornos de hosting.
disable-model-invocation: true
---

# Deployment de ASP.NET Core

Guía de publicación y despliegue en entornos de producción. .NET 9/10.

---

## Publicación

### dotnet publish

```bash
# Release con recorte (trimming) para reducir tamaño
dotnet publish -c Release -o ./publish

# Self-contained (incluye runtime .NET)
dotnet publish -c Release -r win-x64 --self-contained true -o ./publish

# Framework-dependent (requiere .NET instalado en servidor)
dotnet publish -c Release --no-self-contained -o ./publish

# AOT (NativeAOT) — arranque instantáneo, sin JIT
dotnet publish -c Release -p:PublishAot=true -o ./publish

# Trim + single file + ReadyToRun
dotnet publish -c Release \
    -p:PublishTrimmed=true \
    -p:PublishSingleFile=true \
    -p:PublishReadyToRun=true \
    -r linux-x64 \
    -o ./publish

# Configurar en .csproj
# <PublishAot>true</PublishAot>
# <PublishTrimmed>true</PublishTrimmed>
# <PublishSingleFile>true</PublishSingleFile>
```

---

## Docker

### Dockerfile multi-stage

```dockerfile
# Stage 1: Build
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

# Restore
COPY *.sln .
COPY src/MiApp.Web/*.csproj src/MiApp.Web/
COPY src/MiApp.Application/*.csproj src/MiApp.Application/
COPY src/MiApp.Domain/*.csproj src/MiApp.Domain/
COPY src/MiApp.Infrastructure/*.csproj src/MiApp.Infrastructure/
RUN dotnet restore

# Build
COPY . .
RUN dotnet publish src/MiApp.Web/MiApp.Web.csproj -c Release -o /app/publish

# Stage 2: Runtime
FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS runtime
WORKDIR /app

# Usuario no-root
USER app

COPY --from=build /app/publish .

ENV ASPNETCORE_ENVIRONMENT=Production
ENV ASPNETCORE_URLS=http://+:8080

EXPOSE 8080

ENTRYPOINT ["dotnet", "MiApp.Web.dll"]
```

### Docker Compose

```yaml
# docker-compose.yml
services:
  web:
    build: .
    ports:
      - "8080:8080"
    environment:
      - ASPNETCORE_ENVIRONMENT=Production
      - ConnectionStrings__Default=Server=db;Database=MiApp;User=sa;Password=${DB_PASSWORD}
      - Stripe__ApiKey=${STRIPE_API_KEY}
    depends_on:
      - db
      - redis

  db:
    image: mcr.microsoft.com/mssql/server:2022-latest
    environment:
      - ACCEPT_EULA=Y
      - MSSQL_SA_PASSWORD=${DB_PASSWORD}
    volumes:
      - sqldata:/var/opt/mssql

  redis:
    image: redis:7-alpine
    volumes:
      - redisdata:/data

volumes:
  sqldata:
  redisdata:
```

### Docker Healthcheck

```dockerfile
# En Dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl --fail http://localhost:8080/health || exit 1

# O en docker-compose
healthcheck:
  test: ["CMD", "curl", "--fail", "http://localhost:8080/health"]
  interval: 30s
  timeout: 5s
  retries: 3
```

---

## IIS

### Configuración

```xml
<!-- web.config en la raíz del publish -->
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <location path="." inheritInChildApplications="false">
    <system.webServer>
      <handlers>
        <add name="aspNetCore" path="*" verb="*"
             modules="AspNetCoreModuleV2" resourceType="Unspecified" />
      </handlers>
      <aspNetCore processPath="dotnet"
                  arguments=".\MiApp.Web.dll"
                  stdoutLogEnabled="false"
                  stdoutLogFile=".\logs\stdout"
                  hostingModel="inprocess">
        <environmentVariables>
          <environmentVariable name="ASPNETCORE_ENVIRONMENT" value="Production" />
        </environmentVariables>
      </aspNetCore>
    </system.webServer>
  </location>
</configuration>
```

### IIS Hosting

1. Instalar .NET Hosting Bundle en el servidor IIS
2. Crear Application Pool: `No Managed Code`, Integrated pipeline
3. Crear sitio web apuntando a la carpeta `publish/`
4. Configurar HTTPS binding con certificado

---

## Azure App Service

### Deploy con AZ CLI

```bash
# Crear App Service
az webapp up --name miapp --resource-group rg-miapp --runtime "DOTNET:10.0"

# Deploy
dotnet publish -c Release -o ./publish
cd publish && zip -r ../deploy.zip . && cd ..
az webapp deploy --resource-group rg-miapp --name miapp --src-path deploy.zip --type zip

# Configurar variables de entorno
az webapp config appsettings set \
    --resource-group rg-miapp \
    --name miapp \
    --settings \
        ASPNETCORE_ENVIRONMENT=Production \
        ConnectionStrings__Default="Server=..." \
        Stripe__ApiKey="sk_live_..."
```

### App Service Linux

```bash
az webapp up --name miapp --resource-group rg-miapp \
    --runtime "DOTNET:10.0" \
    --os-type Linux \
    --sku B1
```

---

## Reverse Proxy

### YARP (Yet Another Reverse Proxy)

```csharp
// NuGet: Yarp.ReverseProxy
builder.Services.AddReverseProxy()
    .LoadFromConfig(builder.Configuration.GetSection("ReverseProxy"));

app.MapReverseProxy();

// appsettings.json
{
  "ReverseProxy": {
    "Routes": {
      "api-route": {
        "ClusterId": "api-cluster",
        "Match": { "Path": "/api/{**catch-all}" }
      },
      "blazor-route": {
        "ClusterId": "blazor-cluster",
        "Match": { "Path": "{**catch-all}" }
      }
    },
    "Clusters": {
      "api-cluster": {
        "Destinations": {
          "api1": { "Address": "https://localhost:5001" },
          "api2": { "Address": "https://localhost:5002" }
        }
      },
      "blazor-cluster": {
        "Destinations": {
          "blazor1": { "Address": "https://localhost:6001" }
        }
      }
    }
  }
}
```

### nginx (Linux)

```nginx
server {
    listen 80;
    server_name miapp.com;

    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name miapp.com;

    ssl_certificate /etc/letsencrypt/live/miapp.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/miapp.com/privkey.pem;

    # Security headers
    add_header X-Frame-Options "DENY";
    add_header X-Content-Type-Options "nosniff";
    add_header X-XSS-Protection "0";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";

    # Proxy to ASP.NET Core
    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
    }

    # Static files directly from nginx (cache)
    location /static/ {
        alias /var/www/miapp/wwwroot/;
        expires 1y;
        add_header Cache-Control "public,immutable";
    }

    # WebSocket (SignalR, Blazor Server)
    location /hubs/ {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    # Client max body size
    client_max_body_size 10M;
}
```

### Forwarded Headers (detrás de reverse proxy)

```csharp
// Program.cs — ANTES de cualquier middleware
builder.Services.Configure<ForwardedHeadersOptions>(options =>
{
    options.ForwardedHeaders = ForwardedHeaders.XForwardedFor |
                                ForwardedHeaders.XForwardedProto;
    options.KnownNetworks.Clear();
    options.KnownProxies.Clear();
});

app.UseForwardedHeaders();
```

---

## HTTPS y Certificados

### En producción

```bash
# Let's Encrypt (Linux)
sudo certbot certonly --standalone -d miapp.com -d www.miapp.com

# Auto-renovación
sudo certbot renew --dry-run

# En ASP.NET Core: configurar certificado
builder.WebHost.ConfigureKestrel(options =>
{
    options.Listen(IPAddress.Any, 443, listenOptions =>
    {
        listenOptions.UseHttps(
            "/etc/letsencrypt/live/miapp.com/fullchain.pem",
            "/etc/letsencrypt/live/miapp.com/privkey.pem");
    });
});
```

### Azure App Service: HTTPS automático

La capa gratuita de App Service incluye certificado administrado. No se requiere configuración adicional en la app.

---

## Variables de entorno

```bash
# Windows
set ASPNETCORE_ENVIRONMENT=Production
set ConnectionStrings__Default=Server=...

# Linux / Mac
export ASPNETCORE_ENVIRONMENT=Production
export ConnectionStrings__Default="Server=..."

# Docker
docker run -e ASPNETCORE_ENVIRONMENT=Production -e ConnectionStrings__Default="..." miapp

# Convención: doble underscore __ mapea a jerarquía JSON
# ConnectionStrings__Default → { "ConnectionStrings": { "Default": "..." } }
# Stripe__ApiKey → { "Stripe": { "ApiKey": "..." } }
```

---

## CI/CD

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '10.0.x'

      - run: dotnet restore
      - run: dotnet build --configuration Release --no-restore
      - run: dotnet test --configuration Release --no-build
      - run: dotnet publish src/MiApp.Web/MiApp.Web.csproj -c Release -o publish

      # Deploy to Azure App Service
      - uses: azure/webapps-deploy@v3
        with:
          app-name: miapp
          publish-profile: ${{ secrets.AZURE_PUBLISH_PROFILE }}
          package: ./publish

      # O deploy via Docker
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:latest
```

### Azure DevOps

```yaml
# azure-pipelines.yml
trigger:
  - main

pool:
  vmImage: ubuntu-latest

steps:
  - task: UseDotNet@2
    inputs:
      packageType: sdk
      version: '10.0.x'

  - script: dotnet build --configuration Release
  - script: dotnet test --configuration Release --no-build
  - script: dotnet publish --configuration Release --no-build -o $(Build.ArtifactStagingDirectory)

  - task: PublishBuildArtifacts@1
    inputs:
      pathToPublish: $(Build.ArtifactStagingDirectory)
      artifactName: drop
```

---

## Migraciones en producción

```csharp
// Aplicar migraciones en startup (apps pequeñas/medianas)
var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    await db.Database.MigrateAsync();
}

// Para producción grande: generar script y aplicar con CI/CD
// dotnet ef migrations script --idempotent --output migrate.sql
// Ejecutar migrate.sql como parte del deployment pipeline
```

---

## Health checks en orquestadores

```csharp
// Kubernetes probes
app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false // Solo verifica que la app responde
});

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});

// k8s deployment.yaml
// livenessProbe:
//   httpGet:
//     path: /health/live
//     port: 8080
// readinessProbe:
//   httpGet:
//     path: /health/ready
//     port: 8080
```

---

## Hardening final

```csharp
// Program.cs — checklist de producción
var app = builder.Build();

// 1. Forwarded headers (detrás de reverse proxy)
app.UseForwardedHeaders();

// 2. Security headers
if (!app.Environment.IsDevelopment())
{
    app.UseHsts();
}

app.Use(async (context, next) =>
{
    var headers = context.Response.Headers;
    headers["X-Content-Type-Options"] = "nosniff";
    headers["X-Frame-Options"] = "DENY";
    headers["Referrer-Policy"] = "strict-origin-when-cross-origin";
    await next();
});

// 3. No Swagger en producción
if (app.Environment.IsDevelopment())
    app.MapOpenApi();

// 4. Response compression
app.UseResponseCompression();

// 5. HTTPS
app.UseHttpsRedirection();

// 6. Static files
app.UseStaticFiles();

app.UseRouting();
app.UseCors();
app.UseAuthentication();
app.UseAuthorization();
app.MapEndpoints();
app.MapHealthChecks("/health");

app.Run();
```

---

## Checklist de deployment

- [ ] Publicación en Release, no Debug
- [ ] Forwarded headers configurado (detrás de reverse proxy)
- [ ] HTTPS con certificado válido
- [ ] HSTS habilitado en producción
- [ ] Security headers configurados
- [ ] Response compression habilitada
- [ ] Static files con cache headers
- [ ] Health checks en `/health`, `/health/live`, `/health/ready`
- [ ] Migraciones automatizadas o script SQL preparado
- [ ] Variables de entorno, no secretos en código
- [ ] User Secrets no se publican
- [ ] Logs a Application Insights / Serilog sink externo
- [ ] Kestrel configurado con límites de producción
- [ ] Escalado horizontal con Redis/SQL Server para SignalR y sesiones
- [ ] CI/CD configurado (GitHub Actions, Azure DevOps)
- [ ] Monitoreo configurado (Application Insights, Prometheus)
