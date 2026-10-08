---
name: m1on1-send-email
description: >
  Guía completa para enviar emails por SMTP en Marketing1on1. Cubre el paquete MailKit,
  SmtpEmailService, ISmtpEmailService, SmtpEmailMessage, ClientCustomerEmailSmtp (BD),
  registro DI, lógica de TLS (puerto 465 vs 587), y cómo usarlo desde un job Hangfire.
  Usar SIEMPRE que se agregue un nuevo tipo de email, se modifique el servicio SMTP,
  se trabaje con templates HTML de email, o se encole un job de envio de correo.
applyTo:
  - "src/MarketingOneOnOneApi/Services/SmtpEmailService.cs"
  - "src/MarketingOneOnOneApi/Services/Interfaces/ISmtpEmailService.cs"
  - "src/MarketingOneOnOneApi/DTOs/SmtpDtos.cs"
  - "src/MarketingOneOnOneApi/Models/ClientCustomerEmailSmtp.cs"
  - "src/MarketingOneOnOneApi/Extensions/ApplicationServicesExtensions.cs"
  - "src/MarketingOneOnOneApi/Templates/Email/**"
  - "src/MarketingOneOnOneApi/Jobs/**"
---

# m1on1-send-email

## 1. Paquete

**MailKit 4.x** (no usar `System.Net.Mail.SmtpClient` — está deprecado y falla con TLS moderno de SendGrid).

```xml
<!-- MarketingOneOnOneApi.csproj -->
<PackageReference Include="MailKit" Version="4.15.1" />
```

MimeKit se instala automáticamente como dependencia de MailKit.

---

## 2. Archivos clave

| Archivo | Rol |
|---|---|
| `Services/SmtpEmailService.cs` | Implementación concreta con MailKit |
| `Services/Interfaces/ISmtpEmailService.cs` | Interfaz inyectable |
| `DTOs/SmtpDtos.cs` | Record `SmtpEmailMessage` |
| `Models/ClientCustomerEmailSmtp.cs` | Config SMTP por customer (viene de BD) |
| `Extensions/ApplicationServicesExtensions.cs` | Registro DI |
| `Templates/Email/` | Plantillas HTML de los correos |

---

## 3. Contratos

### SmtpEmailMessage (DTO)

```csharp
// DTOs/SmtpDtos.cs
public record SmtpEmailMessage(
    string ToEmail,
    string ToName,
    string Subject,
    string HtmlBody
);
```

### ISmtpEmailService

```csharp
// Services/Interfaces/ISmtpEmailService.cs
public interface ISmtpEmailService
{
    Task SendAsync(SmtpEmailMessage message, ClientCustomerEmailSmtp config);
}
```

### ClientCustomerEmailSmtp (Modelo BD — tabla `tbClientCustomerEmailSMTP`)

| Propiedad | Columna | Tipo | Notas |
|---|---|---|---|
| `IdClientCustomerEmailSmtp` | `idClientCustomerEmailSMTP` | int | PK |
| `IdClientCustomer` | `idClientCustomer` | int | FK del customer |
| `Host` | `host` | string | ej. `smtp.sendgrid.net` |
| `Port` | `port` | string | ej. `"587"` o `"465"` |
| `Username` | `username` | string | ej. `apikey` para SendGrid |
| `Password` | `password` | string | API key o contraseña |
| `EmailFrom` | `emailFrom` | string | Dirección remitente |
| `NameFrom` | `nameFrom` | string | Nombre visible remitente |
| `SslEnabled` | `sslEnabled` | bool | true activa STARTTLS (puerto 587) |

---

## 4. SmtpEmailService — implementación completa

```csharp
using MailKit.Net.Smtp;
using MailKit.Security;
using MarketingOneOnOneApi.DTOs;
using MarketingOneOnOneApi.Models;
using MarketingOneOnOneApi.Services.Interfaces;
using MimeKit;
using MimeKit.Text;

namespace MarketingOneOnOneApi.Services;

public class SmtpEmailService : ISmtpEmailService
{
    private readonly ILogger<SmtpEmailService> _logger;

    public SmtpEmailService(ILogger<SmtpEmailService> logger)
    {
        _logger = logger;
    }

    public async Task SendAsync(SmtpEmailMessage message, ClientCustomerEmailSmtp config)
    {
        if (!int.TryParse(config.Port, out var port))
            throw new InvalidOperationException(
                $"Puerto SMTP invalido para customer {config.IdClientCustomer}: {config.Port}");

        var mimeMessage = new MimeMessage();
        mimeMessage.From.Add(new MailboxAddress(config.NameFrom, config.EmailFrom));
        mimeMessage.To.Add(new MailboxAddress(message.ToName, message.ToEmail));
        mimeMessage.Subject = message.Subject;
        mimeMessage.Body = new TextPart(TextFormat.Html) { Text = message.HtmlBody };

        // Puerto 465 = SSL implícito | 587 sslEnabled=true = STARTTLS | sin SSL = None
        var secureSocketOptions = port == 465
            ? SecureSocketOptions.SslOnConnect
            : config.SslEnabled
                ? SecureSocketOptions.StartTls
                : SecureSocketOptions.None;

        using var smtpClient = new SmtpClient();
        await smtpClient.ConnectAsync(config.Host, port, secureSocketOptions);
        await smtpClient.AuthenticateAsync(config.Username, config.Password);
        await smtpClient.SendAsync(mimeMessage);
        await smtpClient.DisconnectAsync(quit: true);

        _logger.LogInformation(
            "Email SMTP enviado a {ToEmail} para IdClientCustomer={IdClientCustomer}",
            message.ToEmail, config.IdClientCustomer);
    }
}
```

---

## 5. Registro DI

```csharp
// Extensions/ApplicationServicesExtensions.cs
services.AddTransient<ISmtpEmailService, SmtpEmailService>();
```

`AddTransient` es correcto porque `SmtpClient` de MailKit es `IDisposable` y se crea/destruye por envío.

---

## 6. Cómo obtener la config SMTP desde BD

```csharp
var smtpConfig = await _db.ClientCustomerEmailSmtps
    .AsNoTracking()
    .FirstOrDefaultAsync(c => c.IdClientCustomer == idClientCustomer);

if (smtpConfig == null)
{
    _logger.LogError("No existe config SMTP para IdClientCustomer={Id}", idClientCustomer);
    return;
}
```

---

## 7. Patrón de job Hangfire para envio de email

```csharp
public interface IMyEmailJob
{
    [AutomaticRetry(Attempts = 0, OnAttemptsExceeded = AttemptsExceededAction.Fail)]
    Task SendAsync(int idLogin, int idClientCustomer /*, ...params */);
}

public class MyEmailJob : IMyEmailJob
{
    private readonly AppDbContext _db;
    private readonly ISmtpEmailService _smtpEmailService;

    public MyEmailJob(AppDbContext db, ISmtpEmailService smtpEmailService) { ... }

    [Queue("auth")]              // o la queue que corresponda
    [AutomaticRetry(Attempts = 0)]
    public async Task SendAsync(int idLogin, int idClientCustomer)
    {
        // 1. Cargar config SMTP
        var smtpConfig = await _db.ClientCustomerEmailSmtps
            .AsNoTracking()
            .FirstOrDefaultAsync(c => c.IdClientCustomer == idClientCustomer)
            ?? throw new InvalidOperationException("Sin config SMTP");

        // 2. Cargar datos del usuario
        var user = await _db.Logins.AsNoTracking()
            .FirstOrDefaultAsync(l => l.IdLogin == idLogin)
            ?? throw new InvalidOperationException($"IdLogin={idLogin} no existe");

        // 3. Leer template HTML
        var templatePath = Path.Combine(AppContext.BaseDirectory, "Templates", "Email", "mi-template.html");
        var html = await File.ReadAllTextAsync(templatePath);
        html = html.Replace("{{VARIABLE}}", WebUtility.HtmlEncode(valor), StringComparison.Ordinal);

        // 4. Construir mensaje y enviar
        var message = new SmtpEmailMessage(user.EmailLogin!, user.NameLogin, "Asunto", html);
        await _smtpEmailService.SendAsync(message, smtpConfig);
    }
}
```

Registrar el job en `ApplicationServicesExtensions`:

```csharp
services.AddTransient<IMyEmailJob, MyEmailJob>();
```

---

## 8. Templates HTML

- Ubicación: `src/MarketingOneOnOneApi/Templates/Email/`
- Se copian al output con:

```xml
<!-- .csproj -->
<Content Include="Templates/**/*">
  <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
  <CopyToPublishDirectory>PreserveNewest</CopyToPublishDirectory>
</Content>
```

- Variables en el template con `{{NOMBRE_VARIABLE}}` — reemplazadas con `String.Replace(..., StringComparison.Ordinal)`.
- Siempre sanitizar con `WebUtility.HtmlEncode()` antes de inyectar valores en el HTML.

---

## 9. Lógica TLS — tabla de decisión

| Host | Puerto | sslEnabled | SecureSocketOptions usado |
|---|---|---|---|
| smtp.sendgrid.net | 587 | true | `StartTls` ✓ |
| smtp.sendgrid.net | 465 | true/false | `SslOnConnect` |
| smtp propio | 587 | false | `None` |
| smtp propio | 465 | - | `SslOnConnect` |

> **NUNCA** usar `System.Net.Mail.SmtpClient`. Falla con TLS moderno (SendGrid, Gmail, etc.)
> con `IOException: The connection was closed`.

---

## 10. Anti-patrones

- ❌ `new System.Net.Mail.SmtpClient(host, port) { EnableSsl = true }` — no soporta TLS moderno.
- ❌ Hardcodear credenciales SMTP — siempre cargar desde `tbClientCustomerEmailSMTP`.
- ❌ No sanitizar con `HtmlEncode` al inyectar datos de usuario en el template.
- ❌ Registrar `SmtpEmailService` como `Singleton` — el `SmtpClient` de MailKit es `IDisposable`.
