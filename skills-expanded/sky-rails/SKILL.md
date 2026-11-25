---
name: sky-rails
description: >-
  Ruby on Rails: konvansiyonlar, Active Record ilişkileri ve N+1 (includes, strict_loading),
  migration ve DB kısıtları, strong parameters, servis nesneleri, Hotwire (Turbo + Stimulus),
  Active Job + Solid Queue, Action Mailer, Rails 8 auth generator ve Pundit, RSpec/Minitest,
  RuboCop, Brakeman ve Kamal ile dağıtım. Rails projesinde kullan.
disable-model-invocation: true
---

# Sky · Rails

## Başlangıç

```bash
rails new app --database=postgresql --css=tailwind
bin/rails generate authentication        # Rails 8: oturum tabanlı auth iskeleti
```
Rails 8 "Solid" üçlüsü: **Solid Queue**, **Solid Cache**, **Solid Cable** — Redis'siz başlangıç. Dağıtım: **Kamal**.
`config.time_zone = "Istanbul"`, `config.i18n.default_locale = :tr` (rails-i18n gem'i).

## Active Record

```ruby
class Booking < ApplicationRecord
  belongs_to :client
  belongs_to :org
  enum :status, { pending: "pending", confirmed: "confirmed", cancelled: "cancelled" }, validate: true
  validates :starts_at, presence: true
  scope :upcoming, -> { where(starts_at: Time.current..).order(:starts_at) }
end
```
- N+1: `Booking.includes(:client, :service)`; geliştirmede `strict_loading` (model veya varsayılan) → lazy yükleme hatası; Bullet gem'i.
- `counter_cache: true`, `insert_all`/`upsert_all`, `find_each`.
- Atomik: `update_counters`, `with_lock`, `transaction`.
- **Kısıtlar DB'de de**: `null: false`, `add_foreign_key`, unique index — uygulama doğrulaması yarışa açık.
- Kiracı: `current_org.bookings.find(params[:id])` — IDOR'u yapısal olarak önler.

## Controller

```ruby
class BookingsController < ApplicationController
  def create
    @booking = current_org.bookings.build(booking_params)
    authorize @booking
    if @booking.save
      redirect_to @booking, notice: "Randevu oluşturuldu."
    else
      render :new, status: :unprocessable_entity
    end
  end

  private

  def booking_params = params.expect(booking: [:client_id, :service_id, :starts_at])   # Rails 8; eski: require.permit
end
```
Karmaşık akışlar `app/services/` (PORO, `call`) veya form nesneleri.

## Hotwire

- **Turbo Drive** geçişler, **Turbo Frames** parça güncelleme (satır içi düzenleme, modal), **Turbo Streams** canlı güncelleme
  (`broadcasts_to` ile model değişince açık sayfalar güncellenir — insanların "vay" dediği kısım).
- **Stimulus** küçük JS davranışları.

## İşler ve e-posta

`ApplicationJob` (Solid Queue/Sidekiq), `retry_on`, `discard_on`, idempotent; `after_commit` ile kuyruğa at.
Action Mailer + `deliver_later`, önizleme sınıfları. Tekrarlayan işler `config/recurring.yml`.

## Yetki, test, kalite

- Pundit politikaları + `verify_authorized` (unutmayı önler).
- RSpec (+ FactoryBot) veya Minitest (fixtures); sistem testleri (Capybara) kritik akışlarda, istek testleri yetki matrisi için.
- `rubocop-rails-omakase`, **Brakeman**, `bundler-audit`; CSRF açık, `html_safe`/`raw` dikkat.
- Kamal: `kamal setup`, `kamal deploy` — Docker + herhangi bir VPS, sıfır kesinti.
