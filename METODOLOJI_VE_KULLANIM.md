# 📊 Kanıt-Bazlı Sağlık Ekonomisi Analizi - Kullanım Kılavuzu

## 🎯 Özet

Bu model, kilo kaybı müdahalelerinin sağlık maliyetleri üzerindeki etkisini **bilimsel kanıtlara dayalı** olarak hesaplar. Time horizon (1-10 yıl) seçeneği ile gerçekçi, şişme olmayan sonuçlar üretir.

## 🔬 Bilimsel Metodoloji

### 1. **İnsidans-Bazlı Model** (Prevalans değil!)
- Her yıl için **yeni vaka riski** (annual incidence) kullanılır
- Prevalans-bazlı modellerin aksine, vakalar çift sayılmaz
- CDC ve sağlık ekonomisi standartlarına uygun

### 2. **Waning Effect** (Müdahale Etkisinin Azalması)
- **Kaynak**: DPP 10-year follow-up (PMC3135022)
- İlk yıl: %100 etki
- 10. yıl: ~%40'a düşer
- Formül: `RRR_t = RRR_year1 × exp(-k×(t-1))`

### 3. **Weight Regain** (Kilo Geri Kazanımı)
- **Kaynak**: Meta-analiz (PMC5764193)
- Gerçekçi sürdürülebilirlik profili:
  - Yıl 1: 100%
  - Yıl 2: 70%
  - Yıl 3: 55%
  - Yıl 4: 45%
  - Yıl 5: 20% (5 yılda %80 geri)
  - Yıl 6-10: 15-10% (minimal etki)

### 4. **Ekonomik Değerlendirme**
- **Standart**: NICE HTA Guidelines (pmg36)
- **Discount Rate**: %3.5 (NICE referans)
- **Maliyet Yaklaşımı**: Reel (enflasyondan arındırılmış)
- **NPV**: Net Present Value (bugünkü değer)

### 5. **CPRD Data**
- Baseline prevalence: Clinical Practice Research Datalink
- Yaş, BMI, cinsiyet bazlı gerçek veriler

## 📈 Time Horizon Sonuçları (Karşılaştırma)

### Parametre Örneği:
- Yaş: 60-69
- BMI: 27-34
- Kilo kaybı: -15%
- Cinsiyet: Erkek
- Popülasyon: 1000 kişi

### Sonuçlar:

| Time Horizon | Toplam Vaka | Maliyet Tasarrufu (NPV) |
|--------------|-------------|------------------------|
| **1 yıl**    | 22.3        | 22,319 TL             |
| **4 yıl**    | 36.6        | 35,381 TL             |
| **10 yıl**   | 43.0        | 40,645 TL             |

### 💡 Kritik Gözlemler:

1. **Lineer Olmayan Büyüme**: 4→10 yıl sadece +6.4 vaka ekler (waning + weight regain etkisi)
2. **5. Yıldan Sonra Minimal Kazanç**: Kilo geri kazanımı nedeniyle
3. **Gerçekçi Projeksiyonlar**: Eski prevalans-bazlı modelde 10 yıl için 150+ vaka görülürdü

## 🛠️ Kullanım

### Temel Kullanım:

```python
from scientific_calculator import ScientificCalculator

# Hesap makinesi oluştur
calculator = ScientificCalculator(
    population_size=1000,
    hypertension_cost=1000,
    discount_rate=0.035,      # %3.5 NICE standardı
    cost_growth_rate=0.0      # Reel maliyet
)

# Parametreler
params = {
    'age_range': (60, 69),
    'bmi_range': (27, 34),
    'weight_loss_percent': -15,    # Negatif = kilo kaybı
    'gender': 'male',              # 'male', 'female', 'both'
    'time_horizon': 5,             # 1-10 yıl
    'cost_per_case': 1000
}

# Hesaplama
results_ht = calculator.calculate_hypertension(**params)
results_t2d = calculator.calculate_t2d(**params)
results_dyslip = calculator.calculate_dyslipidaemia(**params)
```

### Hastalık-Spesifik Incidence Ayarları:

```python
# Hipertansiyon (varsayılan 2.2%)
calculator.calculate_hypertension(..., annual_incidence=0.022)

# T2D (varsayılan 1.2%)
calculator.calculate_t2d(..., annual_incidence=0.012)

# Dislipidemi (varsayılan 1.8%)
calculator.calculate_dyslipidaemia(..., annual_incidence=0.018)
```

### Nominal vs Reel Maliyet:

```python
# Reel maliyet (önerilen - NICE standardı)
calculator = ScientificCalculator(
    discount_rate=0.035,
    cost_growth_rate=0.0       # Reel
)

# Nominal maliyet (enflasyon dahil)
calculator = ScientificCalculator(
    discount_rate=0.035,
    cost_growth_rate=0.05      # %5 yıllık artış
)
```

## 📊 Output Formatı

```json
{
  "methodology": {
    "model_type": "Incidence-based (yeni vaka bazlı)",
    "waning_effect": "DPP 10-year follow-up kalibreli (PMC3135022)",
    "weight_regain": "Meta-analiz bazlı (PMC5764193)",
    ...
  },
  "results": {
    "hypertension": {
      "rrr_year1_percent": 23.1,
      "cases_prevented_total": 43.0,
      "cost_saving_npv": 40645,
      "yearly_breakdown": [
        {
          "year": 1,
          "annual_incidence": 0.0242,
          "waning_factor": 1.0,
          "weight_retention": 1.0,
          "rrr_effective_percent": 23.1,
          "cases_prevented": 5.59,
          "cost_npv": 5590
        },
        ...
      ]
    }
  }
}
```

## 🔑 Önemli Parametreler

### Time Horizon Aralığı: **1-10 yıl**
- 1 yıl: Kısa dönem etki
- 3-5 yıl: Orta dönem (weight regain belirginleşir)
- 10 yıl: Uzun dönem (minimal etki kalır)

### Weight Loss Percent:
- Negatif değer = Kilo kaybı (örn: -15%)
- Pozitif değer = Kilo artışı (RRR = 0)

### Gender:
- `'male'` veya `1`: Erkek
- `'female'` veya `0`: Kadın
- `'both'`: Her iki cinsiyetin ortalaması

## 📚 Kaynaklar

1. **DPP Study**: [PMC3135022](https://pmc.ncbi.nlm.nih.gov/articles/PMC3135022/) - 10-year follow-up of diabetes incidence and weight loss
2. **Weight Regain Meta-Analysis**: [PMC5764193](https://pmc.ncbi.nlm.nih.gov/articles/PMC5764193/) - Maintenance of lost weight and long-term management
3. **NICE Guidelines**: [pmg36](https://www.nice.org.uk/process/pmg36/chapter/economic-evaluation-2) - NICE health technology evaluations
4. **CPRD**: Clinical Practice Research Datalink - Baseline prevalence data

## ⚠️ Sınırlamalar ve Varsayımlar

1. **Annual Incidence**: CPRD year-on-year veriniz yoksa, literatür bazlı varsayılan değerler kullanılır
2. **Waning Schedule**: DPP'ye kalibre edilmiştir, farklı müdahaleler için ayarlanabilir
3. **Weight Retention**: Meta-analiz ortalaması, bireysel varyasyon vardır
4. **Linear RRR**: Kilo kaybı-RRR ilişkisi lineer kabul edilir (literatür destekli)

## 🚀 Gelecek Geliştirmeler

- [ ] CPRD year-on-year veriden otomatik incidence çıkarma
- [ ] Müdahale-spesifik weight retention profilleri
- [ ] Sensitivity analysis (duyarlılık analizi) modülü
- [ ] Probabilistic sensitivity analysis (PSA)
- [ ] QALY (Quality-Adjusted Life Years) hesaplaması

---

**Son Güncelleme**: 2025-10-13  
**Model Versiyonu**: 2.0 (Incidence-based)  
**Bilimsel Standart**: NICE HTA + DPP + Meta-analiz

