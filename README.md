# 🏥 Scientific Health Economics Calculator

Kanıt-bazlı sağlık ekonomisi analiz sistemi - Kilo kaybı müdahalelerinin maliyet etkisi (Time Horizon: 1-10 yıl)

## ✅ Özellikler

- ✨ **İnsidans-Bazlı Model**: Prevalans yerine yeni vaka riski (CDC standardı)
- 📉 **Waning Effect**: DPP 10-year follow-up verilerine kalibre
- ⚖️ **Weight Regain**: Meta-analiz bazlı gerçekçi kilo geri kazanımı
- 💰 **NICE Standards**: %3.5 discount rate, reel maliyet yaklaşımı
- 📊 **CPRD Data**: Gerçek prevalence verileri (yaş, BMI, cinsiyet bazlı)

## 🚀 Hızlı Başlangıç

```python
python scientific_calculator.py
```

### Parametreleri Düzenle:

```python
params = {
    'age_range': (60, 69),
    'bmi_range': (27, 34),
    'weight_loss_percent': -15,    # -15% kilo kaybı
    'gender': 'male',
    'time_horizon': 5,             # 5 yıl
    'cost_per_case': 1000
}
```

## 📈 Örnek Sonuçlar

| Time Horizon | Toplam Vaka Önlendi | Maliyet Tasarrufu (NPV) |
|--------------|---------------------|------------------------|
| 1 yıl        | 22.3                | 22,319 TL             |
| 4 yıl        | 36.6                | 35,381 TL             |
| 10 yıl       | 43.0                | 40,645 TL             |

> **Not**: 10 yıla kadar sadece +20 vaka (22→43) artış - waning + weight regain nedeniyle gerçekçi!

## 🔬 Bilimsel Temeller

1. **DPP Study** ([PMC3135022](https://pmc.ncbi.nlm.nih.gov/articles/PMC3135022/)): 10-year waning effect
2. **Weight Regain Meta-Analysis** ([PMC5764193](https://pmc.ncbi.nlm.nih.gov/articles/PMC5764193/)): 5 yılda %80 geri
3. **NICE Guidelines** ([pmg36](https://www.nice.org.uk/process/pmg36/chapter/economic-evaluation-2)): Economic evaluation standards
4. **CPRD**: Clinical Practice Research Datalink

## 📚 Detaylı Dokümantasyon

Tüm metodoloji, kullanım örnekleri ve bilimsel kaynaklar için:

👉 [METODOLOJI_VE_KULLANIM.md](METODOLOJI_VE_KULLANIM.md)

## 🎯 Hastalıklar

- **Hipertansiyon** (RRR katsayı: 1.54, incidence: 2.2%)
- **Tip 2 Diyabet** (RRR katsayı: 2.9, incidence: 1.2%)
- **Dislipidemi** (RRR katsayı: 1.3, incidence: 1.8%)

## ⚙️ Sistem Gereksinimleri

- Python 3.7+
- Kütüphaneler: `json`, `math` (standart kütüphane)
- CPRD Data: `cprd-data.prettier_complete.json`

## 📊 Output Format

```json
{
  "methodology": {
    "model_type": "Incidence-based",
    "waning_effect": "DPP 10-year follow-up kalibreli",
    "weight_regain": "Meta-analiz bazlı"
  },
  "results": {
    "hypertension": {
      "rrr_year1_percent": 23.1,
      "cases_prevented_total": 43.0,
      "cost_saving_npv": 40645,
      "yearly_breakdown": [...]
    }
  }
}
```

## 🔄 Versiyon Geçmişi

### v2.0 (2025-10-13) - **Mevcut**
- ✅ İnsidans-bazlı model (prevalans yerine)
- ✅ DPP-kalibreli waning effect
- ✅ Meta-analiz bazlı weight regain
- ✅ NICE standardı discount (3.5%)
- ✅ Gerçekçi time horizon sonuçları (şişme yok!)

### v1.0 (Eski)
- ❌ Prevalans-bazlı (şişme sorunu)
- ❌ Basit linear growth
- ❌ İyimser retention (%92/yıl)

## 🤝 Katkıda Bulunma

Bilimsel kaynaklar, iyileştirme önerileri veya bug reports için issue açabilirsiniz.

## 📄 Lisans

Bu proje bilimsel araştırma amaçlıdır. Kullanırken kaynak gösteriniz.

---

**Geliştirici**: Scientific Health Economics Team  
**Son Güncelleme**: 2025-10-13  
**Model**: Incidence-based Time Horizon (1-10 yıl)

