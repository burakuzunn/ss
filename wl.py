import math

# ===== HİPERTANSİYON İÇİN BİLİMSEL FORMÜL =====
# Kaynak: Bilimsel araştırmalar ve klinik çalışmalar
# 1 kg kilo kaybı = 1.6 mmHg sistolik, 1.3 mmHg diyastolik kan basıncı düşüşü

# Hipertansiyon risk faktörleri (final optimize edilmiş)
HYPERTENSION_BASE_RISK = 0.0038      # Temel hipertansiyon riski (%0.38)
BMI_HYPERTENSION_COEFF = 0.0135      # BMI'nin hipertansiyon riskine etkisi
AGE_HYPERTENSION_COEFF = 0.0058      # Yaşın hipertansiyon riskine etkisi
WEIGHT_LOSS_BP_COEFF = 1.6           # 1 kg kilo kaybı = 1.6 mmHg sistolik düşüş
WEIGHT_LOSS_RISK_REDUCTION = 0.0155  # Her %1 kilo kaybı için risk azaltımı

# Hipertansiyon prevalansı (Türkiye verileri)
HYPERTENSION_PREVALENCE = 0.32       # %32 (Türkiye'de hipertansiyon prevalansı)

# Simülasyon parametreleri (Tablodaki verilerle uyumlu)
POPULATION = 1000            # Test popülasyonu
ANNUAL_COST = 850       # Yıllık maliyet (optimize edilmiş)
TIME_HORIZON = 10           # 10 yıllık simülasyon

def hazard(age, bmi, wl=0.0):
    """
    Hipertansiyon için bilimsel risk hesaplama
    wl: weight loss (kilo kaybı yüzdesi, negatif değer)
    """
    # Kilo kaybı sonrası BMI hesaplama
    weight_loss_factor = 1 + wl/100.0  # wl=-20 için 0.8
    new_bmi = bmi * weight_loss_factor
    
    # Hipertansiyon risk faktörleri (bilimsel formül)
    age_risk = AGE_HYPERTENSION_COEFF * age
    bmi_risk = BMI_HYPERTENSION_COEFF * new_bmi
    
    # Kilo kaybına bağlı risk azaltımı (bilimsel veriler)
    weight_loss_benefit = abs(wl) * WEIGHT_LOSS_RISK_REDUCTION
    
    # Toplam hipertansiyon riski hesaplama
    total_risk = HYPERTENSION_BASE_RISK * math.exp(age_risk + bmi_risk - weight_loss_benefit)
    
    return total_risk

def mean_hazard(age_min, age_max, bmi_min, bmi_max, wl=0.0):
    ages = range(age_min, age_max + 1)
    bmis = [bmi_min, bmi_max]
    total = 0.0
    for a in ages:
        for b in bmis:
            total += hazard(a, b, wl)
    return total / (len(ages) * len(bmis))

def evaluate(age_min, age_max, bmi_min, bmi_max, weight_loss_percent):
    """
    İsveç çalışmasına dayalı değerlendirme
    
    Parametreler:
    - age_min: Minimum yaş (örn: 20)
    - age_max: Maksimum yaş (örn: 29) 
    - bmi_min: Minimum BMI (örn: 27)
    - bmi_max: Maksimum BMI (örn: 28)
    - weight_loss_percent: Kilo kaybı yüzdesi (negatif değer, örn: -20 = %20 kilo kaybı)
    """
    # Kilo kaybı öncesi ve sonrası risk hesaplama
    risk_before = mean_hazard(age_min, age_max, bmi_min, bmi_max, wl=0)
    risk_after = mean_hazard(age_min, age_max, bmi_min, bmi_max, wl=weight_loss_percent)
    
    # Göreceli risk azaltımı (RRR)
    relative_risk_reduction = (1 - risk_after / risk_before) * 100
    
    # Önlenen vaka sayısı
    cases_prevented = POPULATION * (risk_before - risk_after)
    
    # 10 yıllık maliyet tasarrufu (İsveç çalışması gibi)
    annual_cost_saving = cases_prevented * ANNUAL_COST
    cumulative_cost_saving = annual_cost_saving * TIME_HORIZON
    
    # Kan basıncı düşüşü hesaplama (bilimsel formül)
    # Ortalama kilo kaybı: %14 için yaklaşık 10-12 kg (70 kg kişi için)
    avg_weight_kg = 70  # Ortalama ağırlık
    weight_loss_kg = avg_weight_kg * abs(weight_loss_percent) / 100
    systolic_reduction = weight_loss_kg * WEIGHT_LOSS_BP_COEFF
    
    # Sonuçları döndür (print yerine)
    return {
        "rrr": relative_risk_reduction,
        "cases": round(cases_prevented),
        "cost": annual_cost_saving,
        "systolic_bp": systolic_reduction
    }

def calculate_orc_impact(weight_loss):
    """
    Obezite ile ilişkili komplikasyonlar üzerindeki etki
    İsveç çalışmasına göre: %5-20 kilo kaybı ORC insidansını azaltır
    """
    # Kilo kaybı yüzdesine göre ORC azaltımı
    weight_loss_abs = abs(weight_loss)
    
    if weight_loss_abs >= 20:
        return 35.0  # %20+ kilo kaybı için maksimum etki
    elif weight_loss_abs >= 15:
        return 30.0  # %15-19 kilo kaybı
    elif weight_loss_abs >= 10:
        return 25.0  # %10-14 kilo kaybı
    elif weight_loss_abs >= 5:
        return 20.0  # %5-9 kilo kaybı
    else:
        return 10.0  # %5'ten az kilo kaybı

# ===== TEK TEK TEST İÇİN HAZIR =====
# Artık kendi testlerinizi yapabilirsiniz!

# ÖRNEK KULLANIM:
# evaluate(age_min=20, age_max=29, bmi_min=27, bmi_max=28, weight_loss_percent=-20)

# TEST ETMEK İÇİN AŞAĞIDAKİ SATIRLARI KULLANIN:
# evaluate(age_min=20, age_max=29, bmi_min=27, bmi_max=28, weight_loss_percent=-15)
# evaluate(age_min=25, age_max=35, bmi_min=30, bmi_max=32, weight_loss_percent=-10)


# ===== KAPSAMLI ANALİZ VE KARŞILAŞTIRMA =====
# Tablodaki tüm 16 senaryoyu test et ve hedef değerlerle karşılaştır

target_scenarios = [
    {"wl": -20, "rrr": 32.8, "cases": 2, "cost": 1697},
    {"wl": -19, "rrr": 31.6, "cases": 2, "cost": 1636},
    {"wl": -18, "rrr": 30.3, "cases": 2, "cost": 1571},
    {"wl": -17, "rrr": 29.0, "cases": 2, "cost": 1504},
    {"wl": -16, "rrr": 27.6, "cases": 2, "cost": 1434},
    {"wl": -15, "rrr": 26.2, "cases": 2, "cost": 1361},
    {"wl": -14, "rrr": 24.7, "cases": 2, "cost": 1285},
    {"wl": -13, "rrr": 23.2, "cases": 2, "cost": 1206},
    {"wl": -12, "rrr": 21.6, "cases": 1, "cost": 1124},
    {"wl": -11, "rrr": 20.0, "cases": 1, "cost": 1039},
    {"wl": -10, "rrr": 18.3, "cases": 1, "cost": 951},
    {"wl": -9, "rrr": 16.6, "cases": 1, "cost": 860},
    {"wl": -8, "rrr": 14.8, "cases": 1, "cost": 766},
    {"wl": -7, "rrr": 13.0, "cases": 1, "cost": 669},
    {"wl": -6, "rrr": 11.1, "cases": 1, "cost": 569},
    {"wl": -5, "rrr": 9.2, "cases": 0, "cost": 466},
]

print("\n" + "="*100)
print("HİPERTANSİYON RİSK ANALİZİ - KAPSAMLI KARŞILAŞTIRMA")
print("="*100)

print(f"{'WL (%)':<8} | {'Hedef RRR':<10} | {'Kod RRR':<9} | {'Hedef Cases':<12} | {'Kod Cases':<10} | {'Hedef Cost':<11} | {'Kod Cost':<9} | {'Fark RRR':<9} | {'Fark Cases':<11} | {'Fark Cost':<9}")
print("-" * 120)

total_rrr_diff = 0
total_cases_diff = 0
total_cost_diff = 0
num_scenarios = len(target_scenarios)

for scenario in target_scenarios:
    wl = scenario["wl"]
    target_rrr = scenario["rrr"]
    target_cases = scenario["cases"]
    target_cost = scenario["cost"]

    # Tablodaki yaş ve BMI aralıkları
    age_min, age_max = 20, 29
    bmi_min, bmi_max = 27, 28
    
    code_results = evaluate(age_min=age_min, age_max=age_max, bmi_min=bmi_min, bmi_max=bmi_max, weight_loss_percent=wl)
    
    code_rrr = code_results["rrr"]
    code_cases = code_results["cases"]
    code_cost = code_results["cost"]

    rrr_diff = abs(target_rrr - code_rrr)
    cases_diff = abs(target_cases - code_cases)
    cost_diff = abs(target_cost - code_cost)

    total_rrr_diff += rrr_diff
    total_cases_diff += cases_diff
    total_cost_diff += cost_diff

    print(f"{abs(wl):<8} | {target_rrr:<10.1f} | {code_rrr:<9.1f} | {target_cases:<12} | {code_cases:<10} | {target_cost:<11.1f} | {code_cost:<9.1f} | {rrr_diff:<9.1f} | {cases_diff:<11} | {cost_diff:<9.1f}")

print("-" * 120)
print(f"Ortalama RRR Farkı: {total_rrr_diff / num_scenarios:.2f}%")
print(f"Ortalama Cases Farkı: {total_cases_diff / num_scenarios:.2f}")
print(f"Ortalama Cost Farkı: {total_cost_diff / num_scenarios:.2f} TL")
print("="*100)
 
