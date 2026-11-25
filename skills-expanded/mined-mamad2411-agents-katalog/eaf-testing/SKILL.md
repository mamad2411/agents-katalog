---
name: eaf-testing
description: Expert guidance for testing EAF (Enterprise Application Foundation) modules using xUnit, Shouldly, NSubstitute, and coverlet. Covers unit tests, integration tests, test coverage, BDD patterns in Portuguese, and EAF-specific testing patterns. Use this skill when writing tests for EAF modules, improving test coverage, debugging test failures, or setting up test infrastructure. Do NOT use for production code, non-test code, or non-EAF projects.
---

# EAF Testing Skill

You are an expert in testing EAF (Enterprise Application Foundation) modules using xUnit, Shouldly assertions, and NSubstitute mocking. You write functional, maintainable, and comprehensive tests following EAF and .NET testing best practices.

## Project Context

EAF is an open source middleware platform built on ASP.NET Boilerplate (ABP). Testing is critical for ensuring code quality and maintaining ~90% coverage across modules.

### Technology Stack
- **.NET Version**: 10.0
- **Test Framework**: xUnit 2.4+
- **Assertions**: Shouldly 4.x
- **Mocking**: NSubstitute 5.x
- **Coverage**: coverlet.collector 6.x
- **ABP Testing**: Abp.TestBase, Abp.EntityFramework.TestBase

## Test Project Structure

```
test/
├── Eaf.ModuleName.Tests/
│   ├── EafModuleNameTestModule.cs
│   ├── ModuleName/
│   │   ├── EntityName_Tests.cs
│   │   └── ServiceName_Tests.cs
│   └── Eaf.ModuleName.Tests.csproj
```

## Test Base Classes

### Integrated Test Base

```csharp
public class EafMyModule_Tests : AbpIntegratedTestBase<EafMyModuleTestModule>
{
    protected override void PreInitialize()
    {
        base.PreInitialize();
    }
    
    protected override void PostInitialize()
    {
        base.PostInitialize();
    }
}
```

### Test Module

```csharp
[DependsOn(
    typeof(EafMyModule),
    typeof(AbpTestBaseModule)
)]
public class EafMyModuleTestModule : AbpModule
{
    public override void Initialize()
    {
        IocManager.RegisterAssemblyByConvention(Assembly.GetExecutingAssembly());
        
        ServiceCollectionRegistrar.Register(IocManager);
    }
}
```

## BDD Pattern in Portuguese

Use the BDD pattern for test naming:

```csharp
[Fact]
public void Dado_ParametroValido_Quando_ChamarMetodo_Entao_DeveRetornarSucesso()
{
    // Dado (Given)
    var parametro = "valor_valido";
    
    // Quando (When)
    var resultado = _service.ProcessarParametro(parametro);
    
    // Então (Then)
    resultado.ShouldNotBeNull();
    resultado.Sucesso.ShouldBe(true);
}
```

## Entity Tests

### Entity Creation Test

```csharp
public class User_Tests : EafMiddlewareCore_Tests
{
    [Fact]
    public void Dado_ParametrosValidos_Quando_CriarUsuario_Entao_DeveCriarComSucesso()
    {
        // Arrange
        var nome = "John Doe";
        var email = "john@example.com";
        
        // Act
        var usuario = new User
        {
            Name = nome,
            Email = email
        };
        
        // Assert
        usuario.ShouldNotBeNull();
        usuario.Name.ShouldBe(nome);
        usuario.Email.ShouldBe(email);
    }
}
```

### Entity Validation Test

```csharp
[Fact]
public void Dado_EmailInvalido_Quando_CriarUsuario_Entao_DeveFalharValidacao()
{
    // Arrange
    var usuario = new User
    {
        Name = "John Doe",
        Email = "email_invalido"
    };
    
    // Act & Assert
    Should.Throw<AbpValidationException>(() => 
        _userRepository.Insert(usuario)
    );
}
```

## Service Tests

### Application Service Test

```csharp
public class UserAppService_Tests : AbpIntegratedTestBase
{
    private readonly IUserAppService _userAppService;
    private readonly IRepository<User, Guid> _userRepository;
    
    public UserAppService_Tests()
    {
        _userAppService = Resolve<IUserAppService>();
        _userRepository = Resolve<IRepository<User, Guid>>();
    }
    
    [Fact]
    public async Task Dado_InputValido_Quando_CriarUsuario_Entao_DeveCriarComSucesso()
    {
        // Arrange
        var input = new CreateUserDto
        {
            Name = "John Doe",
            Email = "john@example.com",
            Password = "123456"
        };
        
        // Act
        var result = await _userAppService.CreateUser(input);
        
        // Assert
        result.ShouldNotBeNull();
        result.Name.ShouldBe("John Doe");
        result.Email.ShouldBe("john@example.com");
    }
}
```

### Service with Mocking

```csharp
public class MyService_Tests
{
    private readonly MyService _service;
    private readonly IRepository<User, Guid> _userRepository;
    
    public MyService_Tests()
    {
        _userRepository = Substitute.For<IRepository<User, Guid>>();
        _service = new MyService(_userRepository);
    }
    
    [Fact]
    public async Task Dado_UsuarioExistente_Quando_ObterUsuario_Entao_DeveRetornarUsuario()
    {
        // Arrange
        var userId = Guid.NewGuid();
        var usuarioEsperado = new User { Id = userId, Name = "John Doe" };
        _userRepository.GetAsync(userId).Returns(usuarioEsperado);
        
        // Act
        var resultado = await _service.GetUserAsync(userId);
        
        // Assert
        resultado.ShouldNotBeNull();
        resultado.Name.ShouldBe("John Doe");
        await _userRepository.Received(1).GetAsync(userId);
    }
}
```

## Repository Tests

### Custom Repository Test

```csharp
public class UserRepository_Tests : AbpIntegratedTestBase
{
    private readonly IUserRepository _userRepository;
    
    public UserRepository_Tests()
    {
        _userRepository = Resolve<IUserRepository>();
    }
    
    [Fact]
    public async Task Dado_EmailValido_Quando_ObterPorEmail_Entao_DeveRetornarUsuario()
    {
        // Arrange
        var email = "john@example.com";
        
        // Act
        var usuario = await _userRepository.GetByEmailAsync(email);
        
        // Assert
        usuario.ShouldNotBeNull();
        usuario.Email.ShouldBe(email);
    }
}
```

## Middleware Module Tests

### KeyVault Module Test

```csharp
public class EafKeyVaultManager_Tests : AbpIntegratedTestBase
{
    private readonly IEafKeyVaultManager _keyVaultManager;
    
    public EafKeyVaultManager_Tests()
    {
        _keyVaultManager = Resolve<IEafKeyVaultManager>();
    }
    
    [Fact]
    public async Task Dado_NomeSecretoValido_Quando_ObterSecreto_Entao_DeveRetornarValor()
    {
        // Arrange
        var secretName = "my-secret";
        
        // Act
        var secret = await _keyVaultManager.GetSecretAsync(secretName);
        
        // Assert
        secret.ShouldNotBeNull();
        secret.Value.ShouldNotBeNullOrEmpty();
    }
}
```

### OpenTelemetry Module Test

```csharp
public class EafOpenTelemetryModule_Tests : AbpIntegratedTestBase
{
    [Fact]
    public void Dado_ModuloInicializado_Quando_ChecarConfiguracao_Entao_DeveEstarConfigurado()
    {
        // Act
        var configuration = Resolve<IConfiguration>();
        
        // Assert
        configuration.ShouldNotBeNull();
        configuration["OpenTelemetry:Enabled"].ShouldBe("true");
    }
}
```

## Test Coverage

### Running Tests with Coverage

```bash
dotnet test --collect:"XPlat Code Coverage"
```

### Coverage Configuration (coverlet.runsettings)

```xml
<?xml version="1.0" encoding="utf-8" ?>
<RunSettings>
  <DataCollectionRunSettings>
    <DataCollectors>
      <DataCollector friendlyName="XPlat Code Coverage">
        <Configuration>
          <Format>opencover,cobertura</Format>
          <Exclude>[Eaf.*Tests]*,[*.Module]*</Exclude>
        </Configuration>
      </DataCollector>
    </DataCollectors>
  </DataCollectionRunSettings>
</RunSettings>
```

## Common Test Patterns

### Arrange-Act-Assert Pattern

```csharp
[Fact]
public void Test_Scenario()
{
    // Arrange
    var input = "test";
    var expected = "TEST";
    
    // Act
    var result = _service.Process(input);
    
    // Assert
    result.ShouldBe(expected);
}
```

### Testing Async Methods

```csharp
[Fact]
public async Task Test_AsyncMethod()
{
    // Arrange
    var input = "test";
    
    // Act
    var result = await _service.ProcessAsync(input);
    
    // Assert
    result.ShouldNotBeNull();
}
```

### Testing Exceptions

```csharp
[Fact]
public void Dado_InputInvalido_Quando_ChamarMetodo_Entao_DeveLancarExcecao()
{
    // Arrange
    var input = "";
    
    // Act & Assert
    Should.Throw<ArgumentException>(() => 
        _service.Process(input)
    );
}

[Fact]
public async Task Dado_InputInvalido_Quando_ChamarMetodoAsync_Entao_DeveLancarExcecao()
{
    // Arrange
    var input = "";
    
    // Act & Assert
    await Should.ThrowAsync<ArgumentException>(async () => 
        await _service.ProcessAsync(input)
    );
}
```

### Testing with Data

```csharp
[Theory]
[InlineData("test", "TEST")]
[InlineData("hello", "HELLO")]
[InlineData("world", "WORLD")]
public void Dado_InputValido_Quando_Processar_Entao_DeveRetornarUppercase(string input, string expected)
{
    // Act
    var result = _service.Process(input);
    
    // Assert
    result.ShouldBe(expected);
}
```

## Shouldly Assertions

### Common Assertions

```csharp
// Equality
result.ShouldBe(expected);
result.ShouldNotBe(unexpected);

// Null checks
result.ShouldNotBeNull();
result.ShouldBeNull();

// Boolean
result.ShouldBeTrue();
result.ShouldBeFalse();

// Collections
result.Count.ShouldBe(3);
result.ShouldContain(item);
result.ShouldNotContain(item);

// Exceptions
Should.Throw<Exception>(() => method());
```

## NSubstitute Mocking

### Setting Up Returns

```csharp
_repository.GetAsync(id).Returns(user);
_repository.GetAll().Returns(users.AsQueryable());
```

### Verifying Calls

```csharp
await _repository.Received(1).GetAsync(id);
_repository.DidNotReceive().Delete(id);
```

### Argument Matching

```csharp
_repository.GetAsync(Arg.Any<Guid>()).Returns(user);
_repository.GetAsync(Arg.Is<Guid>(x => x != Guid.Empty)).Returns(user);
```

## Test Best Practices

### Naming Conventions
- Use BDD pattern in Portuguese: `Dado_Quando_Entao`
- Be descriptive about what is being tested
- Include the scenario being tested

### Test Independence
- Each test should be independent
- Don't rely on execution order
- Clean up after each test

### Test Readability
- Keep tests simple and focused
- Use descriptive variable names
- One assertion per test when possible

### Test Speed
- Use mocks for external dependencies
- Avoid slow operations in tests
- Run tests in parallel when possible

## Common Issues and Solutions

### Test Initialization Issues

```csharp
public class MyTest : AbpIntegratedTestBase
{
    public MyTest()
    {
        // Resolve dependencies in constructor
        _service = Resolve<IMyService>();
    }
}
```

### Database Context Issues

```csharp
protected override void PreInitialize()
{
    base.PreInitialize();
    
    // Use in-memory database for tests
    UseInMemoryDatabase();
}
```

### Permission Issues in Tests

```csharp
protected override void PostInitialize()
{
    base.PostInitialize();
    
    // Grant permissions for testing
    UsingDbContext(context =>
    {
        context.PermissionGrants.Add(
            new PermissionGrant
            {
                Name = "Pages.Users",
                RoleId = StaticRoleNames.Admin
            }
        );
    });
}
```

## When in Doubt

- Follow ABP testing conventions
- Use BDD pattern in Portuguese
- Keep tests simple and focused
- Mock external dependencies
- Test both success and failure scenarios
- Aim for high coverage (>90%)
- Run tests before committing
