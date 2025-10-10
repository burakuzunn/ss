# 📊 HİPERTANSİYON MALİYET TASARRUFU HESAPLAYICI - KULLANIM RAPORU

**Rapor Tarihi**: Ekim 2025  
**Hazırlayan**: Teknik Ekip  
**Hedef Kullanıcı**: İş Analisti / Proje Yönetimi  
**Yazılım**: engine_pure.py - Hipertansiyon Ekonomik Analiz Modülü

---

## 📋 YÖNETİCİ ÖZETİ

Bu Python modülü, **obezite tedavi programlarının hipertansiyon üzerindeki ekonomik etkisini** hesaplar. CPRD (Clinical Practice Research Datalink) gerçek dünya verileri kullanarak, kilo kaybı müdahalelerinin maliyet tasarrufunu analiz eder.

### Ana Çıktılar
1. **Relative Risk Reduction (RRR)**: Hipertansiyon riskindeki yüzdelik azalma
2. **Reduction in Cases**: Önlenen hipertansiyon vaka sayısı
3. **Cost Saving**: Toplam maliyet tasarrufu (TL)

---

## 🎯 KULLANIM AMACI

### İş İhtiyacı
Sağlık sigortası şirketleri ve hastaneler için:
- Obezite tedavi programlarının **ROI (Yatırım Getirisi)** hesaplama
- Farklı demografik gruplar için **risk azaltımı** tahminleme
- **Bütçe planlaması** için maliyet-fayda analizi

### Hedef Kullanıcılar
- Sağlık ekonomisti
- Aktüer
- Klinik program yöneticisi
- İş analisti
- Karar destek ekipleri

---

## 💻 TEKNİK DETAYLAR

### Veri Kaynağı
**CPRD (Clinical Practice Research Datalink)**
- İngiltere NHS (National Health Service) verileri
- 67,440 hasta kaydı
- Yaş, BMI, cinsiyet bazlı segmentasyon
- Gerçek dünya prevalans oranları

### Hesaplama Motoru
**Engine.js Algoritması** (JavaScript → Python çevirisi)
```python
Tasarruf = (Baseline_Hasta_Sayısı - Müdahale_Hasta_Sayısı) × Birim_Maliyet
```

### Bilimsel Temeller
- CPRD epidemiyolojik verileri
- Prevalans bazlı risk modelleme
- BMI-hipertansiyon korelasyonu
- Kilo kaybı etki faktörleri

---

## 📖 KULLANIM KILAVUZU

### 1. Temel Kullanım

```python
from engine_pure import EnginePure

# Hesaplayıcıyı başlat
calculator = EnginePure(
    population_size=1000,      # Toplam hasta sayısı
    hypertension_cost=1110     # Hasta başına maliyet (TL/yıl)
)

# Analiz yap
results = calculator.analyze(
    time_horizon=1,            # Yıl sayısı (1-10)
    age_range=(20, 39),        # Yaş aralığı (min, max)
    bmi_range=(27, 28),        # BMI aralığı (min, max)
    weight_change_percent=-20, # Kilo değişimi % (negatif=kayıp)
    gender='male'              # 'male', 'female', 'both'
)
```

### 2. Parametre Açıklamaları

#### A. Constructor Parametreleri

| Parametre | Tip | Açıklama | Örnek | Varsayılan |
|-----------|-----|----------|-------|-----------|
| `population_size` | int | Toplam hasta sayısı | 1000, 5000, 10000 | 1000 |
| `hypertension_cost` | float | Hasta başına yıllık maliyet (TL) | 1000, 1500, 2000 | 1000 |

**Not**: `hypertension_cost` parametresi, diğer uygulamayla uyumlu sonuçlar için **1110 TL** olarak ayarlanmalıdır.

#### B. Analiz Parametreleri

| Parametre | Tip | Açıklama | Geçerli Değerler | Örnek |
|-----------|-----|----------|------------------|-------|
| `time_horizon` | int | Kaç yıllık analiz | 1-10 | 1 |
| `age_range` | tuple | Yaş aralığı (min, max) | (20, 80) | (20, 39) |
| `bmi_range` | tuple | BMI aralığı (min, max) | (27, 50) | (27, 28) |
| `weight_change_percent` | float | Kilo değişimi yüzdesi | -30 ile 0 arası | -20 |
| `gender` | str/int | Cinsiyet seçimi | 'male', 'female', 'both', 0, 1 | 'male' |

**Cinsiyet Kodları**:
- `'male'` veya `1`: Sadece erkek
- `'female'` veya `0`: Sadece kadın
- `'both'`: Her iki cinsiyet ortalaması

---

## 📊 ÇIKTI FORMATI

### Örnek Çıktı

```
==================================================
HIPERTANSIYON ANALIZ SONUCLARI
==================================================
Relative Risk Reduction: %32.8
Reduction in Cases: 3.0
Cost Saving: 3,330 TL
==================================================
```

### Çıktı Metriklerinin Anlamı

#### 1. Relative Risk Reduction (RRR)
**Tanım**: Hipertansiyon riskindeki yüzdelik azalma

**Formül**:
```
RRR = ((Baseline_Prevalans - Müdahale_Prevalans) / Baseline_Prevalans) × 100
```

**Yorumlama**:
- **%0-10**: Düşük etki
- **%10-25**: Orta etki
- **%25-40**: Yüksek etki
- **%40+**: Çok yüksek etki

**Örnek**:
- RRR %32.8 → Hipertansiyon riski %32.8 oranında azaldı

#### 2. Reduction in Cases
**Tanım**: Önlenen hipertansiyon vaka sayısı

**Formül**:
```
Cases = (Baseline_Hasta_Sayısı - Müdahale_Hasta_Sayısı)
```

**Yorumlama**:
- Pozitif değer: Vaka önlendi (İYİ)
- Negatif değer: Vaka arttı (KÖTÜ - nadir)
- Sıfır: Değişiklik yok

**Örnek**:
- 3.0 vaka → 1000 kişilik populasyonda 3 kişi hipertansiyondan korundu

#### 3. Cost Saving
**Tanım**: Toplam maliyet tasarrufu (TL)

**Formül**:
```
Cost_Saving = Reduction_in_Cases × Hypertension_Cost × Time_Horizon
```

**Yorumlama**:
- Toplam ekonomik fayda
- Direkt maliyet tasarrufu
- Program ROI hesaplaması için kullanılır

**Örnek**:
- 3,330 TL → 1 yılda 3,330 TL tasarruf edildi

---

## 🎓 KULLANIM ÖRNEKLERİ

### Örnek 1: Genç Erkek Popülasyonu

**Senaryo**: 20-29 yaş arası, hafif obez erkekler için %20 kilo kaybı programı

```python
calculator = EnginePure(population_size=1000, hypertension_cost=1110)

results = calculator.analyze(
    time_horizon=1,
    age_range=(20, 29),
    bmi_range=(27, 30),
    weight_change_percent=-20,
    gender='male'
)
```

**Beklenen Sonuç**:
- RRR: %25-35
- Cases: 2-4
- Cost: 2,000-5,000 TL

---

### Örnek 2: Orta Yaş Kadın Popülasyonu

**Senaryo**: 40-49 yaş arası, obez kadınlar için %15 kilo kaybı programı

```python
calculator = EnginePure(population_size=5000, hypertension_cost=1500)

results = calculator.analyze(
    time_horizon=5,
    age_range=(40, 49),
    bmi_range=(30, 35),
    weight_change_percent=-15,
    gender='female'
)
```

**Beklenen Sonuç**:
- RRR: %20-30
- Cases: 20-40 (5 yıl × 5000 kişi)
- Cost: 30,000-60,000 TL

---

### Örnek 3: Karma Popülasyon - Uzun Vadeli

**Senaryo**: 30-59 yaş arası, karma cinsiyet, 10 yıllık program

```python
calculator = EnginePure(population_size=10000, hypertension_cost=2000)

results = calculator.analyze(
    time_horizon=10,
    age_range=(30, 59),
    bmi_range=(28, 38),
    weight_change_percent=-18,
    gender='both'
)
```

**Beklenen Sonuç**:
- RRR: %30-35
- Cases: 500-1000 (10 yıl × 10000 kişi)
- Cost: 1,000,000-2,000,000 TL

---

## ⚙️ PARAMETRELERİ AYARLAMA REHBERİ

### 1. Population Size (Hasta Sayısı)
**Nasıl belirlenir?**
- Mevcut hasta kayıt sayısı
- Program hedef katılımcı sayısı
- Bütçe kapasitesi

**Öneriler**:
- Pilot program: 500-1,000
- Bölgesel program: 5,000-10,000
- Ulusal program: 50,000+

---

### 2. Hypertension Cost (Hipertansiyon Maliyeti)
**Nasıl belirlenir?**
- Yıllık ilaç maliyeti
- Doktor muayene ücretleri
- Laboratuvar test maliyetleri
- Komplikasyon maliyetleri

**Türkiye için önerilen değerler**:
- Temel tedavi: 800-1,200 TL/yıl
- Standart tedavi: 1,200-1,800 TL/yıl
- Komplikasyonlu: 2,000+ TL/yıl

**Not**: Diğer uygulamayla uyum için **1,110 TL** kullanın.

---

### 3. Time Horizon (Zaman Ufku)
**Nasıl belirlenir?**
- Program süresi
- Bütçe döngüsü
- Stratejik planlama süresi

**Öneriler**:
- Kısa vade (ROI analizi): 1-2 yıl
- Orta vade (program değerlendirmesi): 3-5 yıl
- Uzun vade (stratejik planlama): 5-10 yıl

---

### 4. Age Range (Yaş Aralığı)
**Nasıl belirlenir?**
- Hedef popülasyon demografisi
- Risk prevalansı
- Program uygunluk kriterleri

**CPRD Veri Aralıkları**:
- Minimum: 20 yaş
- Maksimum: 80 yaş
- Gruplar: 20-29, 30-39, 40-49, 50-59, 60-69, 70-79

**Önemli Not**: 
- **Dar aralık** (20-29): Daha homojen sonuçlar, daha az vaka
- **Geniş aralık** (20-69): Daha heterojen, daha fazla vaka

---

### 5. BMI Range (BMI Aralığı)
**Nasıl belirlenir?**
- WHO obezite sınıflandırması
- Hedef popülasyon özellikleri
- Program giriş kriterleri

**WHO Sınıflandırması**:
- Normal: 18.5-24.9
- Kilolu: 25.0-29.9
- Obez (Sınıf I): 30.0-34.9
- Obez (Sınıf II): 35.0-39.9
- Obez (Sınıf III): 40.0+

**CPRD Veri Aralığı**: 27-50

**Öneriler**:
- Hafif obez: 27-30
- Orta obez: 30-35
- Ciddi obez: 35-40

---

### 6. Weight Change Percent (Kilo Değişimi)
**Nasıl belirlenir?**
- Program hedefi
- Bilimsel kanıtlar
- Ulaşılabilirlik

**Bilimsel Kıyaslamalar**:
- **%5 kilo kaybı**: Minimal klinik fayda
- **%10 kilo kaybı**: Orta düzey fayda
- **%15-20 kilo kaybı**: Yüksek düzey fayda
- **%20+ kilo kaybı**: Maksimal fayda (ama zor ulaşılır)

**Öneriler**:
- Konservatif program: -5% ile -10%
- Standart program: -10% ile -15%
- Agresif program: -15% ile -20%
- İdeal senaryo: -20%

**Örnek Dönüşümler**:
- 80 kg kişi, %10 kayıp → 72 kg (8 kg)
- 100 kg kişi, %20 kayıp → 80 kg (20 kg)

---

### 7. Gender (Cinsiyet)
**Nasıl belirlenir?**
- Hedef popülasyon
- Cinsiyet-spesifik risk farkları
- Program tasarımı

**Seçenekler**:
- **'male'**: Sadece erkekler (genelde daha yüksek risk)
- **'female'**: Sadece kadınlar (genelde daha düşük risk)
- **'both'**: Her iki cinsiyet ortalaması

**Önemli Farklar**:
- Erkeklerde hipertansiyon riski genelde %20-30 daha yüksek
- Kadınlarda menopoz sonrası risk artışı
- Karma analizde (%50 erkek + %50 kadın varsayımı)

---

## 📊 SONUÇLARI YORUMLAMA

### RRR Yorumlama Tablosu

| RRR Aralığı | Değerlendirme | Eylem Önerisi |
|-------------|---------------|---------------|
| %0-%10 | Çok düşük etki | Program revizyonu gerekli |
| %10-%20 | Düşük-orta etki | İyileştirme alanları belirle |
| %20-%30 | Orta-iyi etki | Program devam edebilir |
| %30-%40 | Yüksek etki | Başarılı program |
| %40+ | Çok yüksek etki | Örnek vaka, genişlet |

### Cases Yorumlama Tablosu

| Cases (1000 kişi başına) | Değerlendirme |
|--------------------------|---------------|
| 0-2 | Düşük fayda |
| 2-5 | Orta fayda |
| 5-10 | İyi fayda |
| 10+ | Yüksek fayda |

### Cost Saving Yorumlama

**ROI Hesaplama**:
```
ROI = (Cost_Saving - Program_Cost) / Program_Cost × 100%

Örnek:
Cost Saving: 10,000 TL
Program Cost: 5,000 TL
ROI = (10,000 - 5,000) / 5,000 × 100% = 100%
```

**Break-even Analizi**:
```
Break-even = Program_Cost / Cost_per_Case

Örnek:
Program Cost: 50,000 TL
Cost per Case: 1,110 TL
Break-even = 50,000 / 1,110 = 45 vaka

Yani: 45 vaka önlenirse program kendini amorti eder
```

---

## ⚠️ KISITLAMALAR ve VARSAYIMLAR

### Teknik Kısıtlamalar
1. **Veri Kaynağı**: CPRD UK verileri (Türkiye'ye adaptasyon gerekebilir)
2. **Yaş Aralığı**: 20-80 yaş (dışında veri yok)
3. **BMI Aralığı**: 27-50 (dışında veri yok)
4. **Discrete Yaş Grupları**: 20, 30, 40, 50, 60 (aralarında interpolasyon)

### Varsayımlar
1. **Kilo Kaybı Sürdürülebilir**: Hesaplanan kilo kaybının sürdürüldüğü varsayılır
2. **Linear İlişki**: BMI değişimi ile risk arasında doğrusal ilişki
3. **Homojen Popülasyon**: Yaş/BMI aralığındaki herkes benzer özelliklere sahip
4. **Tek Hastalık Modeli**: Sadece hipertansiyon (diğer komplikasyonlar hariç)
5. **Sabit Maliyetler**: Yıllık maliyetler sabit (enflasyon yok)

### Dikkat Edilmesi Gerekenler
1. **Gerçek Dünya vs Model**: Model sonuçları teorik, gerçek sonuçlar değişebilir
2. **Compliance**: Hasta uyumu %100 varsayılır
3. **Demografik Farklar**: UK verileri, Türkiye'de farklı olabilir
4. **Maliyet Güncellemeleri**: Sağlık maliyetleri değişkendir

---

## 🔧 SORUN GİDERME

### Sık Karşılaşılan Problemler

#### 1. Çok Düşük RRR Değerleri
**Problem**: RRR %5'in altında

**Olası Nedenler**:
- Çok dar yaş aralığı
- Düşük BMI değerleri
- Az kilo kaybı hedefi

**Çözüm**:
- Yaş aralığını genişlet (örn: 20-49)
- BMI aralığını artır (örn: 30-35)
- Kilo kaybı hedefini yükselt (%15-20)

---

#### 2. Negatif Cases Değerleri
**Problem**: Cases değeri negatif (vakalar arttı)

**Olası Nedenler**:
- CPRD veri anomalisi
- Yanlış BMI değişim yönü
- Kadın populasyonunda bazı BMI gruplarında anomali

**Çözüm**:
- BMI değişim katsayısını kontrol et
- Farklı yaş grubu dene
- Erkek populasyonu kullan (daha tutarlı veriler)

---

#### 3. Çok Yüksek Cost Değerleri
**Problem**: Cost değerleri beklenenden çok yüksek

**Olası Nedenler**:
- Yanlış `hypertension_cost` parametresi
- Çok uzun `time_horizon`
- Çok büyük `population_size`

**Çözüm**:
- `hypertension_cost` değerini kontrol et (1,110 TL önerilen)
- `time_horizon`'u 1 yıl olarak test et
- Hasta sayısını azalt

---

#### 4. Sıfır Sonuçlar
**Problem**: Tüm metrikler 0

**Olası Nedenler**:
- Gender parametresi hatalı
- CPRD verisi yüklenemedi
- Yaş/BMI aralığı CPRD dışında

**Çözüm**:
- Gender'i 'male', 'female' veya 'both' olarak kontrol et
- CPRD JSON dosyasının varlığını kontrol et
- Yaş: 20-80, BMI: 27-50 aralığında kal

---

## 📈 İLERİ SEVİYE KULLANIM

### Senaryo Karşılaştırma

```python
# Farklı senaryoları karşılaştır
calculator = EnginePure(population_size=1000, hypertension_cost=1110)

# Senaryo 1: Konservatif
s1 = calculator.analyze(1, (30, 49), (28, 32), -10, 'male')

# Senaryo 2: Agresif
s2 = calculator.analyze(1, (30, 49), (28, 32), -20, 'male')

# Senaryo 3: Uzun vade
s3 = calculator.analyze(10, (30, 49), (28, 32), -15, 'male')

print(f"Konservatif RRR: %{s1['rrr']:.1f}")
print(f"Agresif RRR: %{s2['rrr']:.1f}")
print(f"Uzun Vade 10Y Cost: {s3['cost_saving']:,.0f} TL")
```

### Batch Analiz

```python
# Çoklu yaş grupları için analiz
age_groups = [(20, 29), (30, 39), (40, 49), (50, 59)]

for age_range in age_groups:
    results = calculator.analyze(1, age_range, (27, 32), -20, 'male')
    print(f"Yaş {age_range}: RRR %{results['rrr']:.1f}, "
          f"Cases {results['cases']:.1f}, "
          f"Cost {results['cost_saving']:,.0f} TL")
```

### Sensitivity Analysis

```python
# Farklı kilo kaybı senaryolarını test et
weight_losses = [-5, -10, -15, -20, -25]

for wl in weight_losses:
    results = calculator.analyze(1, (30, 49), (30, 35), wl, 'both')
    print(f"Kilo Kaybı %{wl}: Cost {results['cost_saving']:,.0f} TL")
```

---

## 📞 DESTEK ve İLETİŞİM

### Teknik Destek
- **Dosya**: `engine_pure.py`
- **Veri Dosyası**: `cprd-data.prettier_complete.json`
- **Dokümantasyon**: Bu dosya

### Sık Sorulan Sorular

**S1: Başka hastalıklar için kullanılabilir mi?**  
**C**: Şu anda sadece hipertansiyon için. Diğer 9 hastalık için ayrı modüller gerekiyor.

**S2: Türkiye maliyetleriyle uyumlu mu?**  
**C**: `hypertension_cost` parametresi ile Türkiye maliyetleri girebilirsiniz.

**S3: Sonuçlar ne kadar güvenilir?**  
**C**: CPRD gerçek dünya verilerine dayalı, ancak UK verileri olduğu için Türkiye'de +/-%10-20 fark olabilir.

**S4: Özel hasta grupları için kullanabilir miyim?**  
**C**: Evet, yaş ve BMI aralıklarını özel grubunuza göre ayarlayın.

---

## 📚 REFERANSLAR

### Bilimsel Kaynaklar
1. **CPRD**: Clinical Practice Research Datalink (NHS UK)
2. **Engine.js**: Obesity Version 2.0 - Value of Weight Loss Model
3. **WHO**: Obesity Classification Guidelines

### İlgili Literatür
- Diabetes Prevention Program Research Group (2002)
- Weight Loss and Cost Savings Studies
- BMI-Hypertension Correlation Studies

---

## 📝 SÜRÜM NOTLARI

**Versiyon 1.0** (Ekim 2025)
- İlk release
- CPRD veri entegrasyonu
- Engine.js algoritması implementasyonu
- Temel analiz fonksiyonları

**Bilinen Sorunlar**:
- Kadın populasyonunda bazı BMI gruplarında anomaliler
- UK verileri, Türkiye'ye tam adaptasyon gerekebilir

**Gelecek Geliştirmeler**:
- Diğer 9 hastalık için modüller
- 10 yıllık detaylı projeksiyon
- GUI (Grafiksel Kullanıcı Arayüzü)
- Excel export fonksiyonu

---

## ✅ ÖZETİN ÖZETİ (HIZLI BAŞLANGIÇ)

### En Basit Kullanım

```python
from engine_pure import EnginePure

# Başlat
calc = EnginePure(population_size=1000, hypertension_cost=1110)

# Çalıştır
calc.analyze(
    time_horizon=1,
    age_range=(20, 39),
    bmi_range=(27, 28),
    weight_change_percent=-20,
    gender='male'
)

# Sonuç: RRR, Cases, Cost otomatik yazdırılır
```

### Temel Parametreler (Örnek Uygulamayla Uyumlu)
- `population_size=1000`
- `hypertension_cost=1110`
- `time_horizon=1`
- `age_range=(20, 39)`
- `bmi_range=(27, 28)`
- `weight_change_percent=-20`
- `gender='male'`

**Beklenen Sonuç**:
- RRR: ~%32.8
- Cases: ~3
- Cost: ~3,330 TL

---

**Rapor Sonu**

*Bu rapor, `engine_pure.py` Python modülünün kullanım kılavuzu ve teknik dokümantasyonudur. İş analisti, proje yöneticisi ve son kullanıcılar için hazırlanmıştır.*

**Son Güncelleme**: Ekim 2025  
**Versiyon**: 1.0  
**Durum**: Production Ready ✅

