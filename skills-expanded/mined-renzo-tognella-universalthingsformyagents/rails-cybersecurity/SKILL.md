---
name: Rails Cybersecurity
description: Guia de segurança para aplicações Ruby on Rails baseado no Rails Security Guide e OWASP
---

# Rails Cybersecurity

Guia completo de segurança para desenvolvimento Rails seguro, baseado no [Rails Security Guide](https://guides.rubyonrails.org/security.html) e [OWASP Ruby on Rails Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Ruby_on_Rails_Cheat_Sheet.html).

---

## Princípios Fundamentais

1. **Never trust user input** — Todo input do usuário é potencialmente malicioso
2. **Defense in depth** — Múltiplas camadas de segurança
3. **Least privilege** — Mínimo acesso necessário
4. **Fail securely** — Erros devem negar acesso, não permitir
5. **Keep it simple** — Complexidade é inimiga da segurança
6. **Minimal changes** — Altere o mínimo possível; pesquise padrões antes de implementar

> **Zero Gambiarra**: Se parece hack, é hack. Busque na web a solução idiomática.

---

## SQL Injection

### ❌ Vulnerável

```ruby
# NUNCA faça isso!
User.where("email = '#{params[:email]}'")
Project.where("name LIKE '%" + params[:name] + "%'")
User.find_by("login = '#{params[:name]}' AND password = '#{params[:password]}'")
```

### ✅ Seguro

```ruby
# Use placeholders (?)
User.where("email = ?", params[:email])
Project.where("name LIKE ?", "%#{ActiveRecord::Base.sanitize_sql_like(params[:name])}%")

# Use hash syntax (preferido)
User.where(email: params[:email])

# Para queries complexas, use sanitize
User.where("role IN (?)", User.sanitize_sql_array(params[:roles]))
```

### Ferramentas de Detecção

```bash
# Brakeman - scanner de segurança para Rails
gem install brakeman
brakeman -A  # Modo agressivo

# rails-sqli.org - referência de padrões vulneráveis
```

---

## Command Injection

### ❌ Métodos Perigosos

```ruby
# Todos estes executam comandos do sistema!
eval("ruby code")
system("command")
`backticks`
exec("command")
spawn("command")
open("| command")
IO.popen("command")
IO.read("| command")
Process.exec("command")
```

### ✅ Seguro

```ruby
# Use array syntax para evitar shell interpolation
system("ls", "-la", user_provided_path)

# Valide inputs com allowlist
ALLOWED_FORMATS = %w[pdf png jpg].freeze
raise "Invalid format" unless ALLOWED_FORMATS.include?(params[:format])

# Para operações de arquivo, use métodos Ruby nativos
FileUtils.rm(path) # ao invés de system("rm #{path}")
```

---

## Cross-Site Scripting (XSS)

### ❌ Vulnerável

```erb
<%# NUNCA faça isso! %>
<%= raw @user.bio %>
<%== @comment.body %>
<%= @post.content.html_safe %>
<a href="<%= @user.website %>">Site</a>  <%# javascript: URLs! %>
```

### ✅ Seguro

```erb
<%# Rails escapa automaticamente %>
<%= @user.bio %>
<%= @comment.body %>

<%# Para rich text, use sanitize com allowlist %>
<%= sanitize @post.content, tags: %w[p br strong em], attributes: %w[class] %>

<%# Valide URLs %>
<%= link_to "Site", @user.website if URI.parse(@user.website).scheme.in?(%w[http https]) %>
```

### Content Security Policy (CSP)

```ruby
# config/initializers/content_security_policy.rb
Rails.application.configure do
  config.content_security_policy do |policy|
    policy.default_src :self
    policy.script_src  :self
    policy.style_src   :self, :unsafe_inline
    policy.img_src     :self, :data, "https:"
    policy.font_src    :self
    policy.connect_src :self
    policy.frame_ancestors :none
    policy.base_uri    :self
  end

  config.content_security_policy_nonce_generator = ->(request) { SecureRandom.base64(16) }
end
```

---

## Cross-Site Request Forgery (CSRF)

### Como Funciona

1. Usuário está autenticado em `app.com`
2. Usuário visita `malicious.com`
3. `malicious.com` faz request para `app.com` (cookies enviados automaticamente!)
4. `app.com` executa ação pensando que usuário iniciou

### ✅ Proteção

```ruby
# ApplicationController - já habilitado por padrão
class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception
end

# Para APIs com token auth (sem cookies), desabilite
class Api::BaseController < ActionController::API
  # Sem protect_from_forgery porque não usa cookies
end

# Em formulários, Rails adiciona automaticamente
<%= form_with model: @user do |f| %>
  <%# authenticity_token incluído automaticamente %>
<% end %>
```

> **Nota**: Se usar JWT/tokens ao invés de cookies, CSRF não é necessário.

---

## Sessions

### Vulnerabilidades

| Ataque | Descrição |
|--------|-----------|
| **Session Hijacking** | Roubo do session ID via XSS ou network sniffing |
| **Session Fixation** | Atacante define session ID antes do login |
| **Replay Attack** | Reutilização de session antiga |

### ✅ Configuração Segura

```ruby
# config/initializers/session_store.rb
Rails.application.config.session_store :cookie_store,
  key: '_myapp_session',
  secure: Rails.env.production?,     # Apenas HTTPS
  httponly: true,                    # Não acessível via JS
  same_site: :strict                 # Proteção CSRF adicional

# Para aplicações sensíveis, use database sessions
Rails.application.config.session_store :active_record_store
```

### Renovar Session após Login

```ruby
# Previne session fixation
def create
  user = User.authenticate(params[:email], params[:password])
  if user
    reset_session  # IMPORTANTE: renova session ID
    session[:user_id] = user.id
    redirect_to dashboard_path
  end
end
```

### Expiração de Session

```ruby
# Expire sessions inativas
class ApplicationController < ActionController::Base
  before_action :check_session_expiry

  private

  def check_session_expiry
    if session[:last_seen_at].present? && session[:last_seen_at] < 30.minutes.ago
      reset_session
      redirect_to login_path, alert: "Sessão expirada"
    else
      session[:last_seen_at] = Time.current
    end
  end
end
```

---

## Authentication

### Force SSL

```ruby
# config/environments/production.rb
config.force_ssl = true  # SEMPRE em produção!
```

### Devise com Password Complexity

```ruby
# Gemfile
gem 'devise'
gem 'devise_zxcvbn'  # Validação de força de senha

# app/models/user.rb
class User < ApplicationRecord
  devise :database_authenticatable,
         :registerable,
         :recoverable,
         :validatable,
         :lockable,           # Bloqueia após N tentativas
         :trackable,          # Rastreia logins
         :timeoutable,        # Sessão expira
         :zxcvbnable          # Força de senha

  # Configurações adicionais
  def password_complexity
    return if password.blank? || password =~ /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,70}$/
    errors.add :password, 'deve incluir maiúscula, minúscula, número e caractere especial'
  end
end

# config/initializers/devise.rb
Devise.setup do |config|
  config.min_password_score = 4        # zxcvbn score (0-4)
  config.lock_strategy = :failed_attempts
  config.maximum_attempts = 5
  config.unlock_in = 1.hour
  config.timeout_in = 30.minutes
  config.stretches = Rails.env.test? ? 1 : 12  # bcrypt rounds
end
```

### JWT Token Security

```ruby
# app/services/jwt_service.rb
class JwtService
  SECRET_KEY = Rails.application.credentials.jwt_secret_key!
  ALGORITHM = 'HS256'.freeze
  EXPIRATION = 2.hours

  def self.encode(user_id)
    payload = {
      user_id: user_id,
      exp: EXPIRATION.from_now.to_i,
      iat: Time.current.to_i,
      jti: SecureRandom.uuid  # Unique token ID para revogação
    }
    JWT.encode(payload, SECRET_KEY, ALGORITHM)
  end

  def self.decode(token)
    JWT.decode(token, SECRET_KEY, true, algorithm: ALGORITHM).first
  rescue JWT::DecodeError
    nil
  end
end
```

### Devise JWT com HttpOnly Cookies

> **Lição Aprendida**: O Devise/Warden não retorna HTTP 401 automaticamente em falhas de login. Sobrescreva o método `create` para controle total.

#### SessionsController Customizado

```ruby
# app/controllers/api/v1/users/sessions_controller.rb
class SessionsController < Devise::SessionsController
  respond_to :json
  skip_before_action :require_no_authentication, only: [:create]

  # Sobrescrever create para controle total do fluxo
  def create
    user = User.find_by(email: sign_in_params[:email]&.downcase)

    if user&.valid_password?(sign_in_params[:password])
      return render_inactive_error unless user.active?

      sign_in(resource_name, user)
      token = request.env['warden-jwt_auth.token']
      set_auth_cookies(user, token)

      render json: { success: true, data: UserSerializer.new(user) }, status: :ok
    else
      # CRÍTICO: Retornar 401, não 200 com success=false
      render json: {
        success: false,
        error: { code: 'invalid_credentials', message: 'Email ou senha inválidos' }
      }, status: :unauthorized
    end
  end

  private

  def set_auth_cookies(user, token)
    # SEMPRE use cookies.signed para tokens sensíveis
    cookies.signed[:access_token] = {
      value: token,
      httponly: true,
      same_site: :lax,
      secure: Rails.env.production?,
      expires: 15.minutes.from_now
    }

    # Cookie legível para o frontend (apenas dados públicos)
    cookies[:user_data] = {
      value: UserSerializer.new(user).to_json,
      same_site: :lax,
      secure: Rails.env.production?,
      expires: 7.days.from_now
    }
  end
end
```

#### Cookies Signed vs Unsigned

```ruby
# ❌ INSEGURO - Cookie pode ser manipulado pelo cliente
cookies[:access_token] = token

# ✅ SEGURO - Cookie assinado com secret_key_base
cookies.signed[:access_token] = token

# Ao ler, também use signed:
token = cookies.signed[:access_token]  # ✅
token = cookies[:access_token]         # ❌ Retorna valor assinado ilegível
```

#### Attach JWT from Cookie

```ruby
# ApplicationController
before_action :attach_jwt_from_cookie

def attach_jwt_from_cookie
  return if request.headers['Authorization'].present?

  token = cookies.signed[:access_token]
  return if token.blank?

  request.headers['Authorization'] = "Bearer #{token}"
end
```

## Authorization (Pundit)

### ❌ Vulnerável (IDOR)

```ruby
# Insecure Direct Object Reference
def show
  @account = Account.find(params[:id])  # Qualquer usuário pode acessar!
end
```

### ✅ Seguro

```ruby
# app/controllers/accounts_controller.rb
class AccountsController < ApplicationController
  def show
    @account = current_user.accounts.find(params[:id])  # Escopo por usuário
    authorize @account  # Pundit verifica permissões
  end
end

# app/policies/account_policy.rb
class AccountPolicy < ApplicationPolicy
  def show?
    record.user_id == user.id
  end

  class Scope < Scope
    def resolve
      scope.where(user_id: user.id)
    end
  end
end
```

---

## HTTP Security Headers

```ruby
# config/application.rb
config.action_dispatch.default_headers = {
  'X-Frame-Options' => 'DENY',                    # Previne clickjacking
  'X-Content-Type-Options' => 'nosniff',          # Previne MIME sniffing
  'X-XSS-Protection' => '1; mode=block',          # XSS filter (legacy)
  'X-Download-Options' => 'noopen',               # IE download protection
  'X-Permitted-Cross-Domain-Policies' => 'none',  # Flash/PDF policies
  'Referrer-Policy' => 'strict-origin-when-cross-origin'
}

# Para HSTS (Strict Transport Security)
# config/environments/production.rb
config.ssl_options = { hsts: { subdomains: true, preload: true, expires: 1.year } }
```

---

## Sensitive Files

**Nunca commite esses arquivos:**

| Arquivo | Conteúdo Sensível |
|---------|-------------------|
| `config/master.key` | Chave de criptografia das credentials |
| `config/credentials.yml.enc` | Credentials descriptografadas |
| `.env` | Variáveis de ambiente |
| `db/development.sqlite3` | Pode conter dados reais |
| `config/database.yml` | Pode ter senhas de produção |
| `/tmp/`, `/log/` | Podem conter dados sensíveis |

### .gitignore Essencial

```gitignore
/config/master.key
/.env*
/db/*.sqlite3
/log/*
/tmp/*
/storage/*
```

---

## Credentials Seguras

```bash
# Editar credentials (production)
EDITOR="code --wait" rails credentials:edit --environment production

# Estrutura recomendada
# config/credentials/production.yml.enc
secret_key_base: xxx
pluggy:
  client_id: xxx
  client_secret: xxx
jwt:
  secret_key: xxx
database:
  password: xxx
```

```ruby
# Uso no código
Rails.application.credentials.pluggy[:client_id]
Rails.application.credentials.jwt[:secret_key]
```

---

## File Uploads

```ruby
# Validar tipo de arquivo
class Document < ApplicationRecord
  has_one_attached :file

  validate :acceptable_file

  private

  def acceptable_file
    return unless file.attached?

    # Validar por content type, NÃO extensão
    acceptable_types = ['application/pdf', 'image/png', 'image/jpeg']
    unless file.content_type.in?(acceptable_types)
      errors.add(:file, 'tipo não permitido')
    end

    # Limitar tamanho
    if file.byte_size > 10.megabytes
      errors.add(:file, 'muito grande (max 10MB)')
    end
  end
end

# NUNCA execute arquivos enviados por usuários
# Armazene fora do diretório público
```

---

## Brute Force Protection

> **OWASP 2025**: Credential stuffing e brute force são vetores de ataque principais contra SaaS.

### Account Lockout (Devise)

```ruby
# app/models/user.rb
class User < ApplicationRecord
  devise :database_authenticatable, :lockable

  # Configura lockout após N tentativas
  # config/initializers/devise.rb
  # config.lock_strategy = :failed_attempts
  # config.maximum_attempts = 5
  # config.unlock_strategy = :time
  # config.unlock_in = 1.hour
end
```

### Prevent User Enumeration

> **Regra de Ouro**: O atacante NUNCA deve descobrir se um email existe no sistema.

```ruby
# ❌ VULNERÁVEL - Revela existência do email
# "Email não encontrado" vs "Senha incorreta" = atacante sabe se email existe

# ✅ SEGURO - Sempre a mesma mensagem
def render_auth_error
  render json: {
    success: false,
    error: {
      code: 'invalid_credentials',
      message: 'Email ou senha inválidos'  # SEMPRE esta mensagem
    }
  }, status: :unauthorized
end

# Aplicar em TODOS os casos de falha:
# - Email não existe
# - Senha errada
# - Conta inativa
# - Conta bloqueada
```

### Progressive Delays

```ruby
# Aumenta delay a cada tentativa falha
class LoginAttemptsService
  DELAYS = [0, 0.5, 1, 2, 4, 8, 16, 30].freeze

  def self.delay_for(ip)
    attempts = count_recent_attempts(ip)
    DELAYS.fetch(attempts, 30)
  end

  def self.count_recent_attempts(ip)
    Rails.cache.fetch("login_attempts:#{ip}", expires_in: 10.minutes) { 0 }
  end

  def self.record_failure(ip)
    count = count_recent_attempts(ip)
    Rails.cache.write("login_attempts:#{ip}", count + 1, expires_in: 10.minutes)
  end

  def self.reset(ip)
    Rails.cache.delete("login_attempts:#{ip}")
  end
end

# No controller
def create
  sleep(LoginAttemptsService.delay_for(request.ip))

  if authenticated_successfully?
    LoginAttemptsService.reset(request.ip)
    # ... sucesso
  else
    LoginAttemptsService.record_failure(request.ip)
    render_auth_error
  end
end
```

---

## Rate Limiting

```ruby
# Gemfile
gem 'rack-attack'

# config/initializers/rack_attack.rb
class Rack::Attack
  # Limite global
  throttle('req/ip', limit: 300, period: 5.minutes) do |req|
    req.ip
  end

  # Limite para login
  throttle('logins/ip', limit: 5, period: 20.seconds) do |req|
    req.ip if req.path == '/users/sign_in' && req.post?
  end

  # Limite para API
  throttle('api/ip', limit: 100, period: 1.minute) do |req|
    req.ip if req.path.start_with?('/api/')
  end

  # Bloquear IPs suspeitos
  blocklist('block bad IPs') do |req|
    Rack::Attack::Fail2Ban.filter("pentest-#{req.ip}", maxretry: 3, findtime: 10.minutes, bantime: 1.hour) do
      req.path.include?('/wp-admin') || req.path.include?('.php')
    end
  end
end
```

---

## Logging Seguro

```ruby
# config/initializers/filter_parameter_logging.rb
Rails.application.config.filter_parameters += [
  :password,
  :password_confirmation,
  :credit_card,
  :cvv,
  :cpf,
  :token,
  :secret,
  :api_key,
  :authorization
]

# Para dados muito sensíveis, use [FILTERED] customizado
config.filter_parameters << lambda do |key, value|
  value.replace('[CREDIT_CARD_FILTERED]') if key =~ /credit_card/i
end
```

---

## Dependency Management

```bash
# Verificar vulnerabilidades conhecidas
gem install bundler-audit
bundle audit check --update

# Atualizar gems regularmente
bundle outdated --strict

# Ferramentas de CI
# .github/workflows/security.yml
- name: Security audit
  run: |
    gem install bundler-audit brakeman
    bundle audit check --update
    brakeman -q -w2
```

---

## Checklist de Segurança

### Antes de Deploy

- [ ] `config.force_ssl = true` em production
- [ ] Credentials em `rails credentials:edit`, não em ENV
- [ ] `master.key` no `.gitignore`
- [ ] `bundle audit` sem vulnerabilidades
- [ ] `brakeman` sem warnings críticos
- [ ] Rate limiting configurado
- [ ] Logs filtram dados sensíveis

### Em Cada Feature

- [ ] Input do usuário validado/sanitizado
- [ ] Queries usam placeholders ou hash syntax
- [ ] Authorization verificada (Pundit)
- [ ] Uploads validados por content type
- [ ] XSS: nenhum uso de `raw`, `html_safe`, `<%==`

---

## Links Úteis

- [Rails Security Guide](https://guides.rubyonrails.org/security.html)
- [OWASP Rails Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Ruby_on_Rails_Cheat_Sheet.html)
- [Brakeman Scanner](https://brakemanscanner.org/)
- [rails-sqli.org](https://rails-sqli.org)
- [bundler-audit](https://github.com/rubysec/bundler-audit)
