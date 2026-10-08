
# CURSOR PROJECT INSTRUCTIONS

## 🤖 HER PROMPT İÇİN OTOMATİK DAVRANIŞLAR

### HER YANITTAN ÖNCE ZORUNLU OLARAK:
1. **Proje context'ini oku**: Her zaman `memory.md`, `memorybank/development-rules.md`, ve `memorybank/common-patterns.md` dosyalarını okuyarak başla
2. **Anlayışı onayla**: Yanıtlara şu şekilde başla: "✅ Proje bellek dosyalarını okudum. [GÖREV] üzerinde çalışıyorum, [İLGİLİ_PATTERN] takip ediyorum"
3. **Standartları uygula**: Memorybank dosyalarındaki pattern'leri kullan, açıklama olmadan sapma
4. **Türkçe yanıt ver**: Kullanıcı rule'ına göre tüm yanıtları Türkçe olarak ver

## 📋 PROJE DURUMU
- **İsim**: İş Sağlığı Güvenliği Kıyafetleri E-Ticaret Platformu
- **Tip**: B2B (Bayiler) + B2C (Müşteriler) Hibrit Platform
- **Mevcut Faz**: Phase 1 - Çekirdek Altyapı
- **Teknoloji**: Laravel 11 + Filament 3 + PHP 8.2 + MySQL 8.0

## 🔧 ZORUNLU KOD STANDARTLARI
```php
<?php
declare(strict_types=1); // HER ZAMAN dahil et

// HER ZAMAN uygun namespace kullan
namespace App\Services;

// HER ZAMAN type hint kullan
public function calculatePrice(Product $product, User $user): float
{
    // HER ZAMAN error handling dahil et
    try {
        return $this->pricingService->calculate($product, $user);
    } catch (\Exception $e) {
        Log::error('Pricing calculation failed', ['error' => $e->getMessage()]);
        throw new PricingException('Unable to calculate price');
    }
}
```

## 📊 FİLAMENT RESOURCE PATTERN
```php
class ProductResource extends Resource
{
    protected static ?string $model = Product::class;
    protected static ?string $navigationIcon = 'heroicon-o-shopping-bag';
    protected static ?string $navigationGroup = 'Catalog';

    public static function table(Table $table): Table
    {
        return $table
            ->modifyQueryUsing(fn ($query) => $query->with(['currency', 'categories'])) // HER ZAMAN eager load
            ->columns([
                TextColumn::make('name')->searchable()->sortable(),
                TextColumn::make('base_price')->money('TRY')->sortable(),
                IconColumn::make('is_active')->boolean(),
            ]);
    }
}
```

## 🏗️ SERVICE LAYER PATTERN
```php
// HER ZAMAN business logic için service oluştur
class ProductPricingService
{
    public function __construct(
        private ExchangeRateService $exchangeRateService,
        private DiscountService $discountService
    ) {}

    public function calculateFinalPrice(Product $product, User $user): float
    {
        // Business logic burada
    }
}
```

## 🗄️ VERİTABANI KURALLARI
- Tablolar: snake_case çoğul (`products`, `dealer_applications`)
- Foreign key'ler: `{table}_id` (`product_id`, `user_id`)
- Para alanları: `decimal(10,2)`
- Boolean'lar: `is_active`, `has_stock`
- Timestamps: her zaman `created_at`, `updated_at` dahil et

## 🔐 YETKİLENDİRME PATTERN
```php
// HER ZAMAN policy oluştur
class ProductPolicy
{
    public function viewAny(User $user): bool
    {
        return $user->hasPermissionTo('product.view');
    }

    public function create(User $user): bool
    {
        return $user->hasPermissionTo('product.create');
    }
}

// AuthServiceProvider'da HER ZAMAN kaydet
protected $policies = [
    Product::class => ProductPolicy::class,
];
```

## ⚠️ HATA YÖNETİMİ PATTERN
```php
// Harici servisler için HER ZAMAN try-catch kullan
try {
    $response = Http::get('external-api.com/data');
    return $response->json();
} catch (\Exception $e) {
    Log::error('External API failed', [
        'error' => $e->getMessage(),
        'trace' => $e->getTraceAsString()
    ]);
    throw new ExternalServiceException('Service unavailable');
}
```

## 🧪 TEST PATTERN
```php
// Yeni özellikler için HER ZAMAN test dahil et
class ProductTest extends TestCase
{
    use RefreshDatabase;

    public function test_admin_can_create_product(): void
    {
        $admin = User::factory()->create();
        $admin->assignRole('admin');

        $response = $this->actingAs($admin)
            ->post('/admin/products', $this->validProductData());

        $response->assertRedirect();
        $this->assertDatabaseHas('products', ['name' => 'Test Product']);
    }
}
```

## 📚 KONTROL EDİLECEK REFERANS DOSYALAR

### Her Geliştirme İçin:
- `memory.md` - Mevcut proje durumu
- `memorybank/development-rules.md` - Kodlama standartları
- `memorybank/common-patterns.md` - Implementasyon örnekleri

### Belirli Alanlar İçin:
- **Ürünler**: `app/Models/Product.php`, `app/Filament/Resources/ProductResource.php`
- **Kullanıcılar/Bayiler**: `app/Models/User.php`, `app/Models/DealerApplication.php`
- **Fiyatlandırma**: `app/Services/ExchangeRateService.php`, `app/Models/Currency.php`
- **Admin**: `app/Filament/Resources/` içindeki Filament kaynakları

### Sorun Giderme İçin:
- `memorybank/troubleshooting.md` - Yaygın sorunlar ve çözümler

## 🎯 YANIT FORMATI

### HER ZAMAN ŞU ŞEKİLDE BAŞLA:
```
✅ Proje bellek dosyalarını okudum
🎯 Görev: [KISA_AÇIKLAMA]
📋 Takip edilen pattern: [MEMORYBANK_PATTERN]
🔧 Teknolojiler: Laravel 11 + Filament 3 + PHP 8.2
```

### SONRA SAĞLA:
1. Pattern'leri takip eden kod implementasyonu
2. Hata yönetimi ve validasyon
3. Varsa testler
4. Gerekirse dokümantasyon güncellemeleri

### HER ZAMAN ŞU ŞEKİLDE BİTİR:
```
📝 Yapılan değişiklikler:
- [DEĞİŞİKLİK_LİSTESİ]

🔍 Sonraki adımlar:
- [ÖNERİLEN_TAKIP_ADIMLARI]
```

## 🚫 ASLA YAPMA:
- Bellek dosyalarını okumadan kod yazma
- Hata yönetimini atlama
- Type hint'leri veya strict typing'i unutma
- Mevcut pattern'leri görmezden gelme
- Uygun yetkilendirme olmadan kod oluşturma
- Input validasyonunu atlama
- Yanıtlarda hassas veri gösterme

## ✅ HER ZAMAN YAP:
- Yanıt vermeden önce bellek dosyalarını oku
- Memorybank'tan pattern'leri takip et
- Business logic için service layer kullan
- Uygun yetkilendirme uygula
- Kapsamlı hata yönetimi ekle
- Uygun type hint'leri dahil et
- Sık erişilen verileri cache'le
- Filament kaynaklarında eager loading kullan
- Türkçe yanıt ver ve model adını belirt

## 🌐 DİL DESTEĞİ
- **Yanıt Dili**: Türkçe (zorunlu)
- **Kod Yorumları**: Türkçe
- **Değişken Adları**: İngilizce (Laravel konvansiyonu)
- **Dokümantasyon**: Türkçe

## 📋 PHASE 1 ÖZELLİKLERİ (MEVCUT)
✅ Kullanıcı yönetimi + bayi başvuruları
✅ Varyantlı ürün kataloğu
✅ Para birimi + döviz kurları (TCMB)
✅ Filament admin paneli
✅ Yetkilendirme politikaları

## 🔄 GÜNCEL PROJE DURUMU
- **Tamamlanan**: Çekirdek altyapı, model'ler, basic CRUD
- **Devam Eden**: Dealer application sistemi
- **Bekleyen**: Gelişmiş ürün yönetimi, frontend, ödeme entegrasyonu
- Include proper type hints
- Cache frequently accessed data
- Use eager loading in Filament resources