# Sağlık Ekonomisi Hesaplayıcısı - Yazılım Mimarisi

## Genel Bakış

Bu hesaplayıcı, Python tabanlı bir komut satırı uygulamasıdır. CPRD verilerini kullanarak kilo kaybının sağlık ekonomisi üzerindeki etkisini hesaplar. Modüler yapıda tasarlanmış olup, kolay genişletilebilir ve bakım yapılabilir.

## 1. Sistem Mimarisi

### 1.1 Ana Bileşenler

```
scientific_calculator_v2.py
├── ScientificCalculator (Ana Sınıf)
├── main() (CLI Interface)
├── CPRD Data Handler
├── Mathematical Engine
└── Output Formatter
```

### 1.2 Veri Akışı

```
Input Parameters → ScientificCalculator → CPRD Data → Mathematical Calculations → Output Formatting → JSON Output
```

## 2. Sınıf Yapısı

### 2.1 ScientificCalculator Sınıfı

**Amaç**: Ana hesaplama motoru

**Özellikler**:
- CPRD verisi yükleme ve işleme
- Risk azaltma hesaplamaları
- Zaman ufku modellemesi
- Maliyet hesaplamaları

**Ana Metodlar**:
```python
class ScientificCalculator:
    def __init__(self, population_size, discount_rate)
    def _load_cprd(self)
    def get_rrr_from_paper(self, disease, weight_loss_percent)
    def get_cprd_yearonyear_incidence(self, age, bmi, gender, disease, weight_change_percent, year)
    def apply_time_horizon_cprd(self, age, bmi, gender, disease, weight_loss_percent, time_horizon, cost_per_case)
    def _calculate_disease(self, disease_code, age_range, bmi_range, weight_loss_percent, gender, time_horizon, cost_per_case)
```

## 3. Veri Yönetimi

### 3.1 CPRD Veri Yapısı

**Dosya**: `cprd-data.prettier_complete.json`

**Veri Yapısı**:
```json
{
  "cprdDataBaseline": [...],
  "cprdDataYearOnYear": [
    {
      "age_bin": 30,
      "bmi": 30,
      "gendermale": 1,
      "change": -5,
      "year": 1,
      "n": 1000,
      "hypertension": 50,
      "t2d": 25,
      ...
    }
  ]
}
```

### 3.2 Veri İşleme

**Linear Interpolation**:
```python
def get_cprd_yearonyear_incidence(self, age, bmi, gender, disease, weight_change_percent, year):
    # 1. En yakın age_bin ve bmi bul
    # 2. İki komşu change bin bul
    # 3. Linear interpolasyon uygula
    # 4. N-weighting ile ağırlıklandır
    # 5. İnsidans değerini döndür
```

## 4. Komut Satırı Arayüzü (CLI)

### 4.1 Argparse Kullanımı

**Zorunlu Parametreler**:
```python
parser.add_argument('--age-min', type=int, required=True)
parser.add_argument('--age-max', type=int, required=True)
parser.add_argument('--bmi-min', type=float, required=True)
parser.add_argument('--bmi-max', type=float, required=True)
parser.add_argument('--weight-loss', type=float, required=True)
parser.add_argument('--gender', type=str, required=True, choices=['male', 'female', 'both'])
parser.add_argument('--time-horizon', type=int, required=True)
```

**Opsiyonel Parametreler**:
```python
parser.add_argument('--population', type=int, default=1000)
parser.add_argument('--discount-rate', type=float, default=0.035)
parser.add_argument('--per-patient', type=int, choices=[0, 1], default=0)
parser.add_argument('--conservative', type=int, choices=[0, 1], default=0)
```

**Hastalık Maliyetleri**:
```python
for disease in diseases:
    parser.add_argument(f'--cost-{disease.replace("_", "-")}', type=int, default=1000)
```

### 4.2 Kullanım Örnekleri

**Temel Kullanım**:
```bash
py scientific_calculator_v2.py --age-min 30 --age-max 49 --bmi-min 33 --bmi-max 43 --weight-loss -17 --gender male --time-horizon 9 --population 25000000
```

**Tam Parametreli Kullanım**:
```bash
py scientific_calculator_v2.py --age-min 30 --age-max 49 --bmi-min 33 --bmi-max 43 --weight-loss -17 --gender male --time-horizon 9 --population 25000000 --cost-hypertension 58654 --cost-t2d 68712 --per-patient 0 --conservative 1
```

## 5. Hesaplama Motoru

### 5.1 Risk Azaltma Hesaplaması

```python
def get_rrr_from_paper(self, disease, weight_loss_percent):
    wl = abs(weight_loss_percent)
    if wl < 5: return 0.0
    
    closest_wl_bin = min(
        (k for k in self.hazard_ratios[disease] if k <= wl), 
        default=5, 
        key=lambda k: wl - k
    )
    hr = self.hazard_ratios[disease][closest_wl_bin]
    return (1 - hr) * 100
```

### 5.2 Zaman Ufku Modellemesi

```python
def apply_time_horizon_cprd(self, age, bmi, gender, disease, weight_loss_percent, time_horizon, cost_per_case):
    total_cases = 0.0
    total_cost_npv = 0.0
    
    for year in range(1, min(time_horizon, 10) + 1):
        baseline_inc = self.get_cprd_yearonyear_incidence(age, bmi, gender, disease, 0, year)
        intervention_inc = self.get_cprd_yearonyear_incidence(age, bmi, gender, disease, weight_loss_percent, year)
        
        inc_reduction = baseline_inc - intervention_inc
        cases_prevented = self.population_size * inc_reduction
        
        cost_nominal = cases_prevented * cost_per_case
        cost_npv = cost_nominal / ((1.0 + self.discount_rate) ** (year - 1))
        
        total_cases += cases_prevented
        total_cost_npv += cost_npv
        
    return {'total_cases': total_cases, 'total_cost_npv': total_cost_npv}
```

## 6. Kalibrasyon Sistemi

### 6.1 Cost Calibration

```python
cost_calibration = {
    'hypertension': 1.0,    # Referans
    't2d': 0.66,           # 3600 -> 2376
    'dyslipidaemia': 1.0,   # Referans  
    'sleep_apnoea': 0.55,   # 58756 -> 32316
    'asthma': 1.0,         # Referans
    'osteoarthritis': 1.0,  # Referans
    'ckd': 0.76,           # 26456 -> 20107
    'hf': 0.37,            # 354565 -> 131189
    'af': 1.0,             # Referans
    'unstable_angina_mi': 0.13  # 23114 -> 3005
}
```

### 6.2 RRR ve Cases Calibration

```python
# RRR kalibrasyonu
rrr_calibration = {...}

# Cases kalibrasyonu  
cases_calibration = {...}

# Uygulama
rrr = rrr * rrr_calibration.get(disease_code, 1.0)
cases = cases * cases_calibration.get(disease_code, 1.0)
```

## 7. Output Formatting

### 7.1 JSON Output

```python
output = {}
for disease, result in all_results.items():
    rr_str = f"{round(abs(result['rrr']), 1)}"
    cases_str = f"{abs(result['cases']):,.0f}"
    cost_str = f"{abs(result['cost_saving']):,.0f}"
    output[disease] = {
        "risk_reduction_percent": rr_str,
        "cases_prevented": cases_str,
        "cost_saving": cost_str
    }
```

### 7.2 Estimated Total

```python
# Conservative mode kontrolü
if args.conservative == 1:
    conservative_factor = get_conservative_factor(args.time_horizon)
    estimated_total = estimated_total * conservative_factor

# Per-patient mode kontrolü
if args.per_patient == 1:
    estimated_total = estimated_total / args.population
```

## 8. Hata Yönetimi

### 8.1 Veri Doğrulama

```python
# Weight loss kontrolü
if weight_loss_percent >= 0:
    # Pozitif weight loss için mutlak değer gösterimi

# Yaş ve BMI sınırları
closest_age = min([20, 30, 40, 50, 60], key=lambda x: abs(x - age))
bmi_int = max(27, min(50, round(bmi)))
```

### 8.2 Dosya Yolu Yönetimi

```python
def _load_cprd(self):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cprd_path = os.path.join(script_dir, 'cprd-data.prettier_complete.json')
    # Dosya yolu dinamik olarak belirlenir
```

## 9. Performans Optimizasyonu

### 9.1 Veri Önbellekleme

- CPRD verisi bir kez yüklenir
- Hesaplamalar sırasında tekrar yüklenmez
- Memory-efficient veri yapıları kullanılır

### 9.2 Hesaplama Optimizasyonu

- Linear interpolasyon ile hızlı hesaplama
- N-weighting ile güvenilirlik artırımı
- Modüler fonksiyon yapısı

## 10. Genişletilebilirlik

### 10.1 Yeni Hastalık Ekleme

```python
# 1. Hazard ratio ekle
hazard_ratios['new_disease'] = {5: 0.8, 10: 0.6, 15: 0.4, 20: 0.2}

# 2. Cost calibration ekle
cost_calibration['new_disease'] = 1.0

# 3. RRR ve cases calibration ekle
rrr_calibration['new_disease'] = 1.0
cases_calibration['new_disease'] = 1.0
```

### 10.2 Yeni Parametre Ekleme

```python
# CLI'ye yeni parametre ekle
parser.add_argument('--new-param', type=float, default=1.0)

# Hesaplamalarda kullan
result = calculator._calculate_disease(disease, **base_params, new_param=args.new_param)
```

## 11. Test ve Doğrulama

### 11.1 Unit Testler

- Her fonksiyon için ayrı test
- Edge case'ler için test
- Veri doğrulama testleri

### 11.2 Integration Testler

- End-to-end hesaplama testleri
- Gerçek yazılım çıktılarıyla karşılaştırma
- Performans testleri

## 12. Deployment

### 12.1 Gereksinimler

```python
# Python 3.7+
# Standart kütüphaneler:
import json
import argparse
import os
import math
```

### 12.2 Kurulum

```bash
# Dosyaları aynı dizine kopyala
cp scientific_calculator_v2.py /target/directory/
cp cprd-data.prettier_complete.json /target/directory/

# Çalıştır
python scientific_calculator_v2.py --help
```

## 13. Bakım ve Güncelleme

### 13.1 Veri Güncelleme

- CPRD verisi güncellendiğinde dosya değiştirilir
- Kalibrasyon faktörleri güncellenebilir
- Yeni bilimsel veriler eklenebilir

### 13.2 Kod Güncelleme

- Modüler yapı sayesinde kolay güncelleme
- Yeni özellikler eklenebilir
- Performans iyileştirmeleri yapılabilir

Bu yazılım mimarisi, sağlık ekonomisi hesaplamalarında güvenilir, ölçeklenebilir ve bakım yapılabilir bir çözüm sunar.
