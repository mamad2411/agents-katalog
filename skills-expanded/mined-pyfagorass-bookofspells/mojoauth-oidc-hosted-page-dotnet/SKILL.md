---
name: mojoauth-oidc-hosted-page-dotnet
description: Implement passwordless authentication in ASP.NET Core applications using MojoAuth OIDC middleware.
---

# Implement MojoAuth OIDC (.NET Core)

This expert AI assistant guide walks you through integrating passwordless authentication into a .NET Core application using MojoAuth's Hosted Login Page as an OIDC identity provider. MojoAuth handles all authentication methods (Magic Links, Email OTP, SMS OTP, Social Login, Passkeys) through its hosted page.

## 1. Prerequisites

- An existing .NET Core 6+ application.
- Basic knowledge of ASP.NET Core MVC or Razor Pages.
- An active MojoAuth account.
- [MojoAuth OIDC Setup Guide](https://docs.mojoauth.com/hosted-login-page/)
- Required NuGet package: `Microsoft.AspNetCore.Authentication.OpenIdConnect`.

## 2. Implementation Steps

### Step 1: Configure Application in MojoAuth

1. Log in to the [MojoAuth Dashboard](https://mojoauth.com/dashboard).
2. Note your **MojoAuth Domain** (e.g., `your-app.mojoauth.com`).
3. Configure the **Redirect URI** (e.g., `http://localhost:5000/auth/callback`).
4. Retrieve **Client ID** and **Client Secret**.
5. Enable your preferred authentication methods.

### Step 2: Modify the Existing .NET Core Project

#### Substep 2.1: Install Dependencies

```bash
dotnet add package Microsoft.AspNetCore.Authentication.OpenIdConnect
```

#### Substep 2.2: Configure Environment Variables

Add the following to `appsettings.json`:

```json
{
  "MojoAuth": {
    "Domain": "your-app.mojoauth.com",
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
    var mojoauthConfig = builder.Configuration.GetSection("MojoAuth");

    options.Authority = $"https://{mojoauthConfig["Domain"]}";
    options.ClientId = mojoauthConfig["ClientId"];
    options.ClientSecret = mojoauthConfig["ClientSecret"];
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
        OnRemoteFailure = context =>
        {
            context.HandleResponse();
            context.Response.Redirect("/login?error=auth_failed");
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

Since MojoAuth handles all authentication on its Hosted Login Page, your login view only needs a **"Sign In" button**:

```html
<!-- Views/Account/Login.cshtml -->
@{
    ViewData["Title"] = "Sign In";
}

<div class="login-container">
    <h1>Welcome</h1>
    <p>Sign in with your preferred method — passwordless, social login, or passkeys.</p>

    @if (ViewBag.Error != null)
    {
        <p style="color: red;">@ViewBag.Error</p>
    }

    <form method="post" asp-action="Login" asp-controller="Account">
        <button type="submit" class="sign-in-button">Sign In with MojoAuth</button>
    </form>

    <p class="powered-by">Powered by MojoAuth — Passwordless Authentication</p>
</div>
```

#### Substep 2.5: Update Backend Logic

Create the `AccountController` to handle login:

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
            ViewBag.Error = "Authentication failed. Please try again.";
        }
        return View();
    }

    [HttpPost]
    public IActionResult Login()
    {
        // Trigger MojoAuth OIDC login
        var properties = new AuthenticationProperties
        {
            RedirectUri = "/dashboard",
        };

        return Challenge(properties, OpenIdConnectDefaults.AuthenticationScheme);
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

### Step 3: Test the Implementation

1. Start your application: `dotnet run`.
2. Navigate to `http://localhost:5000/login`.
3. Click **"Sign In with MojoAuth"**.
4. You should be redirected to the MojoAuth Hosted Login Page.
5. Authenticate using any available method.
6. After successful authentication, you should be redirected back to `/auth/callback` and then to `/dashboard`.

## 3. Additional Considerations

- **Error Handling**: Customize `OnRemoteFailure` and `OnAuthenticationFailed` events for granular error handling.
- **Styling**: Adapt the example HTML to match your application's design system (e.g., Bootstrap, MudBlazor).
- **Security**: Store `ClientSecret` using the .NET Secret Manager (`dotnet user-secrets`) or Azure Key Vault.
- **Environment Variables**: Use `appsettings.Development.json` for local overrides and never commit secrets to source control.

## 4. Support

- **MojoAuth Documentation**: [mojoauth.com/docs](https://mojoauth.com/docs)
- **Check application logs**: Use ASP.NET Core logging (`ILogger`) to debug OIDC flow issues.
- **Library Documentation**: Refer to the [Microsoft OIDC documentation](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/oidc) for advanced configuration.
