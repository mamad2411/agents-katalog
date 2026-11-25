---
name: oidc-hosted-page-dotnet
description: Implement "Sign in with SSO" in ASP.NET Core applications using SSOJet OIDC middleware.
---

# Implement SSOJet OIDC (.NET Core)

This expert AI assistant guide walks you through integrating "Sign in with SSO" functionality into an existing login page in a .NET Core application using SSOJet as an OIDC identity provider. The goal is to modify the existing login flow to add SSO support without disrupting the current traditional login functionality (e.g., email/password).

## 1. Prerequisites

- An existing .NET Core 6+ application with a login page.
- Basic knowledge of ASP.NET Core MVC or Razor Pages.
- An active SSOJet account.
- [SSO Connection Setup Guide](https://docs.ssojet.com/en/how-to-guides/integrations//)
- Required NuGet package: `Microsoft.AspNetCore.Authentication.OpenIdConnect`.

## 2. Implementation Steps

### Step 1: Create Application in SSOJet

1. Log in to the SSOJet Dashboard.
2. Navigate to **Applications**.
3. Create a new application (e.g., "MyDotNetApp", type **Regular Web App**).
4. Configure the callback URI (e.g., `http://localhost:5000/auth/callback`).
5. Retrieve **Client ID** and **Client Secret**.
6. Copy the **Issuer URL** from the **Advanced > Endpoints** section.

### Step 2: Modify the Existing .NET Core Project

#### Substep 2.1: Install Dependencies

Run the following command to install the required NuGet package:

```bash
dotnet add package Microsoft.AspNetCore.Authentication.OpenIdConnect
```

#### Substep 2.2: Configure Environment Variables

Add the following to `appsettings.json`:

```json
{
  "SSOJet": {
    "IssuerUrl": "https://auth.ssojet.com",
    "ClientId": "your_client_id",
    "ClientSecret": "your_client_secret",
    "RedirectUri": "http://localhost:5000/auth/callback"
  }
}
```

#### Substep 2.3: Configure OIDC Middleware

Update your `Program.cs` (or `Startup.cs`) to register the OIDC authentication scheme:

```csharp
// Program.cs
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Authentication.OpenIdConnect;
using Microsoft.IdentityModel.Protocols.OpenIdConnect;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllersWithViews();

builder.Services.AddAuthentication(options =>
{
    options.DefaultScheme = CookieAuthenticationDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = OpenIdConnectDefaults.AuthenticationScheme;
})
.AddCookie()
.AddOpenIdConnect(options =>
{
    var ssojetConfig = builder.Configuration.GetSection("SSOJet");

    options.Authority = ssojetConfig["IssuerUrl"];
    options.ClientId = ssojetConfig["ClientId"];
    options.ClientSecret = ssojetConfig["ClientSecret"];
    options.ResponseType = OpenIdConnectResponseType.Code;
    options.CallbackPath = "/auth/callback";

    options.Scope.Clear();
    options.Scope.Add("openid");
    options.Scope.Add("profile");
    options.Scope.Add("email");

    options.SaveTokens = true;
    options.GetClaimsFromUserInfoEndpoint = true;

    options.Events = new OpenIdConnectEvents
    {
        OnRedirectToIdentityProvider = context =>
        {
            // Pass login_hint if available
            var loginHint = context.Properties.GetParameter<string>("login_hint");
            if (!string.IsNullOrEmpty(loginHint))
            {
                context.ProtocolMessage.LoginHint = loginHint;
            }
            return Task.CompletedTask;
        },
        OnRemoteFailure = context =>
        {
            context.HandleResponse();
            context.Response.Redirect("/login?error=oidc_failed");
            return Task.CompletedTask;
        }
    };
});

var app = builder.Build();

app.UseStaticFiles();
app.UseRouting();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllerRoute(name: "default", pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();
```

#### Substep 2.4: Update Login Page/UI

Modify your existing login view (e.g., `Views/Account/Login.cshtml`) to include the "Sign in with SSO" toggle:

```html
<!-- Views/Account/Login.cshtml -->
@{
    ViewData["Title"] = "Sign In";
}

<div class="login-container">
    <h1>Sign In</h1>

    @if (ViewBag.Error != null)
    {
        <p style="color: red;">@ViewBag.Error</p>
    }

    <form id="loginForm" method="post" asp-action="Login" asp-controller="Account">
        <div>
            <label for="email">Email</label>
            <input type="email" id="email" name="email" required />
        </div>

        <div id="passwordField">
            <label for="password">Password</label>
            <input type="password" id="password" name="password" required />
        </div>

        <input type="hidden" id="isSSO" name="isSSO" value="false" />

        <button type="submit" id="submitBtn">Sign In</button>
    </form>

    <button type="button" id="ssoToggle" onclick="toggleSSO()">
        Sign in with SSO
    </button>
</div>

<script>
    function toggleSSO() {
        const isSSO = document.getElementById('isSSO');
        const passwordField = document.getElementById('passwordField');
        const submitBtn = document.getElementById('submitBtn');
        const ssoToggle = document.getElementById('ssoToggle');

        if (isSSO.value === 'false') {
            isSSO.value = 'true';
            passwordField.style.display = 'none';
            document.getElementById('password').removeAttribute('required');
            submitBtn.textContent = 'Continue with SSO';
            ssoToggle.textContent = 'Back to Password Login';
        } else {
            isSSO.value = 'false';
            passwordField.style.display = 'block';
            document.getElementById('password').setAttribute('required', 'true');
            submitBtn.textContent = 'Sign In';
            ssoToggle.textContent = 'Sign in with SSO';
        }
    }
</script>
```

#### Substep 2.5: Update Backend Logic

Create the `AccountController` to handle login and SSO:

```csharp
// Controllers/AccountController.cs
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Authentication.OpenIdConnect;
using Microsoft.AspNetCore.Mvc;

public class AccountController : Controller
{
    [HttpGet]
    public IActionResult Login(string error = null)
    {
        if (!string.IsNullOrEmpty(error))
        {
            ViewBag.Error = "SSO authentication failed. Please try again.";
        }
        return View();
    }

    [HttpPost]
    public IActionResult Login(string email, string password, string isSSO)
    {
        if (isSSO == "true")
        {
            // Trigger SSO login with login_hint
            var properties = new AuthenticationProperties
            {
                RedirectUri = "/dashboard",
            };
            properties.SetParameter("login_hint", email);

            return Challenge(properties, OpenIdConnectDefaults.AuthenticationScheme);
        }

        // Existing password login logic here
        Console.WriteLine("Processing traditional login...");
        return Redirect("/dashboard");
    }

    [HttpGet]
    public async Task<IActionResult> Logout()
    {
        await HttpContext.SignOutAsync(CookieAuthenticationDefaults.AuthenticationScheme);
        return Redirect("/login");
    }
}
```

**Dashboard Controller** (`Controllers/DashboardController.cs`):

```csharp
// Controllers/DashboardController.cs
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

[Authorize]
public class DashboardController : Controller
{
    public IActionResult Index()
    {
        var claims = User.Claims.Select(c => new { c.Type, c.Value });
        return View(claims);
    }
}
```

### Step 3: Test the Modified Connection

1. Start your application: `dotnet run`.
2. Navigate to your login page (e.g., `http://localhost:5000/login`).
3. Verify that the traditional login form (Email + Password) is visible by default.
4. Click **"Sign in with SSO"** and ensure:
   - The password field disappears.
   - The submit button changes to "Continue with SSO".
5. Enter a test email and submit.
   - You should be redirected to the SSOJet login page.
6. Authenticate with SSOJet.
   - You should be redirected back to `/auth/callback` and then to `/dashboard`.

## 3. Additional Considerations

- **Error Handling**: Customize `OnRemoteFailure` and `OnAuthenticationFailed` events for granular error handling.
- **Styling**: Adapt the example HTML to match your application's design system (e.g., Bootstrap, MudBlazor).
- **Security**: Store `ClientSecret` using the .NET Secret Manager (`dotnet user-secrets`) or Azure Key Vault.
- **Environment Variables**: Use `appsettings.Development.json` for local overrides and never commit secrets to source control.

## 4. Support

- **Contact SSOJet support**: Reach out if you have integration questions.
- **Check application logs**: Use ASP.NET Core logging (`ILogger`) to debug OIDC flow issues.
- **Library Documentation**: Refer to the [Microsoft OIDC documentation](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/oidc) for advanced configuration.
