# OpenCV Müşteri Analiz Sistemi - Cursor Kuralları

## Proje Genel Kuralları

### 🎯 Proje Amacı
Gümüş takı ve saat dükkânı için OpenCV ve YOLOv8 kullanarak müşteri analiz sistemi geliştirmek

### 📋 Kodlama Standartları

#### Python Kodlama Kuralları
- **PEP 8** standartlarına uygun kod yazımı
- Türkçe yorumlar ve değişken açıklamaları kullan
- Fonksiyon ve sınıf isimleri İngilizce, yorumlar Türkçe
- Her fonksiyonun başında docstring bulundur

#### Dosya Organizasyonu
```
src/
├── core/           # Ana işlem modülleri
├── models/         # ML modelleri ve weights
├── utils/          # Yardımcı fonksiyonlar
├── config/         # Konfigürasyon dosyaları
├── data/           # Veri depolama
└── ui/             # Kullanıcı arayüzü
```

#### Kod Yazım Kuralları
- Sabitler BÜYÜK_HARFLE yazılsın
- Değişkenler snake_case formatında
- Sınıflar PascalCase formatında
- Her modül için __init__.py dosyası oluştur

### 🔧 Teknoloji Kuralları

#### Gerekli Kütüphaneler
- **OpenCV**: Görüntü işleme ve kamera erişimi
- **YOLOv8/Ultralytics**: İnsan tespiti
- **MediaPipe**: Alternatif tespit sistemi (opsiyonel)
- **face_recognition**: Yüz tanıma (opsiyonel)
- **pandas**: Veri analizi
- **matplotlib/seaborn**: Görselleştirme
- **sqlite3**: Veri depolama

#### Performans Kuralları
- FPS değeri minimum 15, ideal 30
- Memory leak kontrolü yap
- Tkinter timer sistemi kullan (threading yerine)
- Thread-safe UI güncellemeleri

### 📊 Veri Yönetimi

#### Veri Saklama
- SQLite veritabanı kullan (üretim için)
- CSV backup dosyaları oluştur
- Kişisel veri koruma kurallarına uy
- Yüz verileri hash'lenmiş şekilde sakla

#### Log Sistemi
- Her işlem için timestamp
- Error logging mecburi
- Daily log rotation
- Debug modunda detaylı log

### 🚀 Geliştirme Aşamaları

#### Aşama 1: Temel Sistem ✅
- Kamera girişi
- İnsan tespiti
- Temel UI
- Thread-safe görüntü güncellemesi

#### Aşama 2: Veri Kayıt 🔄
- Ziyaretçi sayımı
- Zaman damgası
- CSV export
- SQLite entegrasyonu

#### Aşama 3: Çalışan Tanıma
- Yüz veritabanı
- Face recognition
- Filtreleme

#### Aşama 4: Demografik Analiz
- Yaş tahmini
- Cinsiyet tespiti
- İstatistik

#### Aşama 5: Analytics
- Yoğunluk analizi
- Görselleştirme
- Raporlama

#### Aşama 6: İleri Özellikler
- Geri gelen müşteri tespiti
- Dashboard
- Uyarı sistemi

### ⚡ Optimizasyon Kuralları

#### Görüntü İşleme
- Frame resize ile performans artırımı (640x480 işlem boyutu)
- ROI (Region of Interest) kullanımı
- Timer-based UI güncellemeleri (33ms = 30 FPS)
- Memory management ve image referans temizliği

#### ML Model Optimizasyonu
- YOLOv8n kullanımı (nano model - hızlı)
- CPU/GPU otomatik algılama
- Model caching
- Batch inference (gelecek sürümlerde)

### 🔒 Güvenlik ve Gizlilik

#### Veri Güvenliği
- Yüz verilerini hash'le
- Local storage kullan
- Network erişimi minimize et
- GDPR uyumlu veri işleme

#### Sistem Güvenliği
- Input validation
- Exception handling
- Graceful shutdown
- Backup mekanizması

### 📱 UI/UX Kuralları

#### Arayüz Tasarımı
- Türkçe arayüz
- Kolay kullanım
- Real-time güncellemeler
- Thread-safe widget güncellemeleri
- Responsive design

#### Kullanıcı Deneyimi
- Loading indicators
- Error mesajları
- Status bar güncellemeleri
- Screenshot alma özelliği
- Dark mode friendly renkler

### 🔄 Thread Safety Kuralları

#### UI Thread Management
- **ASLA** background thread'lerden widget güncelleme yapma
- `root.after()` kullanarak timer-based güncellemeler
- Frame processing'i background'da, UI güncellemeyi main thread'de
- Image reference'ları düzgün yönet (`self.video_label.image = photo`)

#### Camera Thread Safety
- Frame callback'leri güvenli şekilde ekle/çıkar
- `current_image` thread-safe şekilde sakla
- Exception handling ile sistem kararlılığını sağla

### 🧪 Test Kuralları

#### System Testing
- `test_requirements.py` ile kütüphane kontrolü
- Kamera erişim testleri
- YOLOv8 model yükleme testleri
- UI responsiveness testleri

#### Integration Testing
- End-to-end workflow
- Database işlemleri
- Screenshot alma
- Sistem başlatma/durdurma

### 📝 Dokümantasyon

#### Kod Dokümantasyonu
- Türkçe yorumlar
- Fonksiyon açıklamaları
- Thread safety notları
- Performance ipuçları

#### Kullanıcı Rehberi
- Kurulum rehberi (quick_setup.ps1)
- Troubleshooting guide
- Kamera konfigürasyonu
- Performance tuning

### 🔧 Kurulum ve Dağıtım

#### Requirements Management
- `requirements.txt` - tam kurulum
- `requirements_minimal.txt` - Windows-friendly
- Dlib olmadan çalışma desteği
- Visual Studio C++ build tools notları

#### Platform Uyumluluk
- Windows 10/11 primary support
- Python 3.8-3.10 compatibility
- USB kamera desteği
- Built-in webcam desteği

### 🐛 Debug ve Sorun Giderme

#### Common Issues
- Kamera indeksi problemleri (0,1,2 test)
- Thread safety UI donmaları
- Memory leak'ler (image references)
- Model yükleme hataları

#### Performance Monitoring
- FPS tracking
- Memory usage monitoring
- Detection confidence tuning
- UI responsiveness metrics

### 🔄 Commit Kuralları

#### Git Workflow
```
feat: Yeni özellik ekleme
fix: Bug düzeltme
docs: Dokümantasyon güncelleme
style: Kod formatı düzenleme
refactor: Kod refactoring
test: Test ekleme/düzeltme
chore: Proje bakım işleri
```

#### Commit Mesajları
- Türkçe commit mesajları
- Açıklayıcı başlıklar
- Thread safety düzeltmeleri belirt
- Performance iyileştirmelerini vurgula

### 📊 Current System Status

#### ✅ Working Features
- Real-time camera capture (1280x720@30fps)
- YOLOv8 human detection
- Thread-safe UI updates
- Screenshot functionality
- System start/stop controls
- FPS monitoring
- Status tracking

#### 🔄 In Progress
- Visitor counting logic
- Data persistence (SQLite)
- Analytics dashboard
- Employee face recognition

#### ❌ Known Limitations
- Dlib not installed (Windows C++ compiler issues)
- No duplicate visitor prevention yet
- Basic analytics only

---

**Not**: Bu kurallar proje gelişimi sırasında güncellenebilir. Sistemin mevcut çalışma durumu mükemmel - kamera çalışıyor, YOLOv8 aktif, thread-safe UI güncellemeleri başarılı. 