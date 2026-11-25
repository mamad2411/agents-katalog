---
name: "IntraWeb Framework Patterns"
description: "Padrões de desenvolvimento web stateful usando IntraWeb com FreePascal/Lazarus — UserSession, TIWAppForm, thread safety, e design."
alwaysApply: false
---

# IntraWeb Framework — Skill

Use esta skill ao desenvolver ou modernizar aplicações Web usando o framework **IntraWeb** em projetos **FreePascal / Lazarus**.

## 1. Contexto e Aplicação
- **IntraWeb** é um framework stateful para Web, amplamente compatível com Lazarus.
- Cada usuário conectado possui uma sessão dedicada que reside em memória no servidor.
- O paradigma de desenvolvimento é muito similar ao desenvolvimento desktop tradicional (arrastar e soltar componentes), mas rodando no browser ("Web VCL/LCL").

## 2. Padrões Obrigatórios

### Acesso a Dados e Variáveis Globais (Proibido)
O IntraWeb é nativamente multithread (uma thread por requisição) e stateful (uma sessão contínua por usuário). 
- ❌ **NUNCA** declare ou acesse Instâncias de Banco de Dados (`TSQLConnection`, `TSQLQuery`), Conexões REST ou variáveis de contexto em unidades de formulário (`unit`) como globais na seção `var`. 
- Isso causa cruzamento de estado (Cross-Session Data Leak) onde um usuário altera e enxerga os dados do outro.
- ✅ **SEMPRE** utilize o objeto global `UserSession` (geralmente provido pela unit `UnitUserSession` ou via método `UserSession()`) para guardar propriedades relativas ao usuário logado, como `UserId`, `Role`, ou `TenantId`.
- Crie instâncias isoladas de `DataModule` (ex: `TdmDatabase`) no momento de uso na thread, ou amarre um exclusivo no escopo da `UserSession`.

### Formulários
- ❌ **NUNCA** faça herança LCL (`TForm`) quando construir uma tela para a Web.
- ✅ Todos os forms no projeto devem herdar de `TIWAppForm`.

## 3. Instanciação e Limpeza
Formulários no IntraWeb são criados associados à aplicação web chamando `.Create(WebApplication)`.
Evite liberar forms "cegamente" usando `.Free` no code-behind a menos que se trate de uma arquitetura popup estritamente isolada. O gerenciador de ciclo de vida do próprio servidor IntraWeb fará a coleta quando a sessão ou form for descartado via método `Release`.

## Exemplo de Boa Prática de Login e Sessão

```pascal
procedure TIWFormLogin.IWButtonLoginClick(Sender: TObject);
var
  LUserService: IUserService;
  LUser: TUser;
begin
  LUserService := TUserService.Create(TThreadDBFactory.GetConnection);
  
  LUser := LUserService.Authenticate(IWEditUser.Text, IWEditPass.Text);
  if Assigned(LUser) then
  begin
    // Salva na UserSession para que o estado seja retido entre requests
    UserSession.LoggedUserID := LUser.Id;
    UserSession.TenantID := LUser.TenantId;
    
    // Libera a tela de login
    TIWFormDashboard.Create(WebApplication).Show;
    Release;
  end
  else
    WebApplication.ShowMessage('Acesso Negado');
end;
```
