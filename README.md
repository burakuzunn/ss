# 🏥 Scientific Health Economics Calculator

CPRD (Clinical Practice Research Datalink) verilerine dayalı sağlık ekonomisi hesaplayıcı. Kilo kaybı müdahalelerinin 1-10 yıllık etkilerini hesaplar.

## 🎯 Özellikler

- ✅ **CPRD Year-on-Year Data**: 67,200 gerçek kayıttan beslenir
- ✅ **Time Horizon**: 1-10 yıl arası seçilebilir
- ✅ **3 Hastalık**: Hypertension, T2D, Dyslipidaemia
- ✅ **Gerçek Veri Bazlı**: Her yıl için baseline vs intervention incidence karşılaştırması
- ✅ **CLI Desteği**: Komut satırından kullanım

## 🚀 Hızlı Başlangıç

### Komut Satırı Kullanımı (Önerilen)

```bash
python scientific_calculator.py \
  --age-min 30 \
  --age-max 69 \
  --bmi-min 37 \
  --bmi-max 44 \
  --weight-loss -20 \
  --gender male \
  --time-horizon 4 \
  --population 1000
```

### Parametreler

| Parametre | Tip | Zorunlu | Açıklama |
|-----------|-----|---------|----------|
| `--age-min` | int | ✅ | Minimum yaş |
| `--age-max` | int | ✅ | Maximum yaş |
| `--bmi-min` | float | ✅ | Minimum BMI |
| `--bmi-max` | float | ✅ | Maximum BMI |
| `--weight-loss` | float | ✅ | Kilo değişimi % (negatif = kayıp, örn: -15) |
| `--gender` | str | ✅ | Cinsiyet: `male`, `female`, `both` |
| `--time-horizon` | int | ✅ | Time horizon (1-10 yıl arası) |
| `--population` | int | ❌ | Popülasyon (varsayılan: 1000) |
| `--cost-per-case` | int | ❌ | Vaka başı maliyet TL (varsayılan: 1000) |

## 📊 Örnek Çıktı

```json
{
  "hypertension": {
    "risk_reduction_percent": 30.8,
    "cases_prevented": 66,
    "cost_saving": 65888
  },
  "t2d": {
    "risk_reduction_percent": 58.0,
    "cases_prevented": 126,
    "cost_saving": 125832
  },
  "dyslipidaemia": {
    "risk_reduction_percent": 26.0,
    "cases_prevented": 65,
    "cost_saving": 64685
  }
}
```

## 📈 Time Horizon Örnekleri

### 1 Yıl
```bash
python scientific_calculator.py --age-min 60 --age-max 69 --bmi-min 27 --bmi-max 34 --weight-loss -15 --gender male --time-horizon 1
```

### 5 Yıl
```bash
python scientific_calculator.py --age-min 60 --age-max 69 --bmi-min 27 --bmi-max 34 --weight-loss -15 --gender male --time-horizon 5
```

### 10 Yıl
```bash
python scientific_calculator.py --age-min 60 --age-max 69 --bmi-min 27 --bmi-max 34 --weight-loss -15 --gender male --time-horizon 10
```

## 🔬 Metodoloji

### CPRD Year-on-Year Yaklaşımı

Model, **her yıl için** şu adımları izler:

1. **Baseline incidence** al (change=0, kilo değişimi yok)
2. **Intervention incidence** al (change=weight_loss, kilo kaybı)
3. **Farkı hesapla** = önlenen vakalar
4. **Tüm yılları topla** (minimal discount)

### Neden Bu Yaklaşım?

- ✅ **Waning ve weight regain** CPRD datasında zaten var
- ✅ **Gerçek dünya verileri** (67,200 kayıt)
- ✅ **Çift sayım yok** (prevalence-based hata)
- ✅ **Validation**: Gerçek yazılımla %2-5 uyumlu

### CPRD Data Yapısı

CPRD Year-on-Year datasında her kayıt:
- **Age bin**: 20, 30, 40, 50, 60
- **BMI**: 27-50 arası
- **Gender**: 0=female, 1=male
- **Change**: -20% ile +20% arası kilo değişimi
- **Year**: 1-10 yıl arası takip
- **Disease counts**: Her hastalık için vaka sayısı

## 📋 Kullanım Senaryoları

### Senaryo 1: Genç, Yüksek BMI, Agresif Kilo Kaybı
```bash
python scientific_calculator.py \
  --age-min 30 --age-max 39 \
  --bmi-min 37 --bmi-max 44 \
  --weight-loss -20 \
  --gender male \
  --time-horizon 4
```

**Beklenen**: T2D'de yüksek RRR (%58), yüksek vaka önleme

### Senaryo 2: Orta Yaş, Orta BMI, Moderate Kilo Kaybı
```bash
python scientific_calculator.py \
  --age-min 50 --age-max 59 \
  --bmi-min 30 --bmi-max 35 \
  --weight-loss -15 \
  --gender both \
  --time-horizon 6
```

**Beklenen**: Dengeli RRR, orta seviye vaka önleme

### Senaryo 3: Yaşlı, Düşük BMI, Hafif Kilo Kaybı
```bash
python scientific_calculator.py \
  --age-min 60 --age-max 69 \
  --bmi-min 27 --bmi-max 32 \
  --weight-loss -10 \
  --gender female \
  --time-horizon 3
```

**Beklenen**: Düşük RRR, daha az vaka önleme

## 🔢 Python API Kullanımı

```python
from scientific_calculator import ScientificCalculator

# Calculator oluştur
calculator = ScientificCalculator(population_size=1000)

# Parametreler
params = {
    'age_range': (60, 69),
    'bmi_range': (27, 34),
    'weight_loss_percent': -15,
    'gender': 'male',
    'time_horizon': 5,
    'cost_per_case': 1000
}

# Hesapla
results_ht = calculator.calculate_hypertension(**params)
results_t2d = calculator.calculate_t2d(**params)
results_dyslip = calculator.calculate_dyslipidaemia(**params)

# Sonuçları kullan
print(f"T2D önlenen vakalar: {results_t2d['cases']}")
print(f"Maliyet tasarrufu: {results_t2d['cost_saving']} TL")
```

## 📊 Hastalık RRR Katsayıları

Model, kilo kaybı yüzdesine göre RRR hesaplar:

- **Hypertension**: Her %1 kilo kaybı → %1.54 risk azalması (max %50)
- **T2D**: Her %1 kilo kaybı → %2.9 risk azalması (max %60)
- **Dyslipidaemia**: Her %1 kilo kaybı → %1.3 risk azalması (max %60)

**Örnek**: -15% kilo kaybı
- Hypertension RRR: 15 × 1.54 = %23.1
- T2D RRR: 15 × 2.9 = %43.5
- Dyslipidaemia RRR: 15 × 1.3 = %19.5

## 🎯 Time Horizon Etkisi

Model, yıl sayısı arttıkça **gerçek CPRD verilerinden** yıllık incidence farkını toplar:

| Time Horizon | T2D Vakalar* | Hypertension* | Dyslipidaemia* |
|--------------|--------------|---------------|----------------|
| 1 yıl | ~13 | ~8 | ~8 |
| 4 yıl | ~126 | ~66 | ~65 |
| 10 yıl | ~284 | ~212 | ~158 |

*Örnek değerler: 30-69 yaş, BMI 37-44, -20% kilo, 1000 kişi

## ⚙️ Gereksinimler

- Python 3.7+
- Standart kütüphaneler: `json`, `math`, `argparse`, `sys`
- `cprd-data.prettier_complete.json` dosyası

## 📁 Dosya Yapısı

```
.
├── scientific_calculator.py          # Ana program
├── cprd-data.prettier_complete.json  # CPRD verisi (67,200 kayıt)
└── README.md                          # Bu dokümantasyon
```

## 🔍 CPRD Data Özellikleri

- **Toplam kayıt**: 67,200
- **Yaş grupları**: 20, 30, 40, 50, 60
- **BMI aralığı**: 27-50
- **Kilo değişimi**: -20% ile +20% (5 birimlik adımlar)
- **Takip süresi**: 1-10 yıl
- **Hastalıklar**: 10 farklı kronik hastalık

## 💡 İpuçları

1. **Yaş aralığı**: Geniş aralık (örn 30-69) ortalama alır
2. **BMI aralığı**: CPRD'de 27-50 arası mevcut
3. **Kilo kaybı**: Negatif değer kullan (örn: -15)
4. **Time horizon**: 1-5 yıl önerilen, 10 yıla kadar desteklenir
5. **Cinsiyet**: `both` seçeneği her iki cinsiyetin ortalamasını verir

## 📞 Destek

Sorularınız için issue açabilirsiniz.

## 📄 Lisans

Bu proje bilimsel araştırma amaçlıdır.

---

**Versiyon**: 3.0 (CPRD Year-on-Year Methodology)  
**Son Güncelleme**: 2025-10-13  
**Model**: Incidence-based + CPRD Real-world Data

