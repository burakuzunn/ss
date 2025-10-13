import json
import statistics

print("CPRD Year-on-Year Datası Yükleniyor...")
with open('cprd-data.prettier_complete.json', encoding='utf-8') as f:
    data = json.load(f)

yoy_data = data['cprdDataYearOnYear']
baseline_data = data['cprdDataBaseline']

print(f"OK Toplam Year-on-Year kayit: {len(yoy_data):,}")
print(f"OK Toplam Baseline kayit: {len(baseline_data):,}")

# =====================================================================
# 1. YEAR-ON-YEAR: Kilo değişimi ve hastalık incidence ilişkisi
# =====================================================================
print("\n" + "="*100)
print("BÖLÜM 1: KİLO DEĞİŞİMİ VE HASTALIK İNCİDENCE İLİŞKİSİ (TÜM VERİ)")
print("="*100)

# Yaş grupları
age_groups = {}
for record in yoy_data:
    age = record['age_bin']
    if age not in age_groups:
        age_groups[age] = {'records': [], 'changes': {}}
    age_groups[age]['records'].append(record)
    
    change = record['change']
    if change not in age_groups[age]['changes']:
        age_groups[age]['changes'][change] = []
    age_groups[age]['changes'][change].append(record)

print(f"\nYaş grupları: {sorted(age_groups.keys())}")
print(f"Toplam farklı 'change' değeri: {len(set(r['change'] for r in yoy_data))}")

# Her change değeri için ortalama incidence
change_values = sorted(set(r['change'] for r in yoy_data))
print(f"\nKilo değişimi aralığı: {min(change_values):.1f}% ile {max(change_values):.1f}%")

# =====================================================================
# 2. BASELINE (change=0) ORTALAMA İNCIDENCE
# =====================================================================
print("\n" + "="*100)
print("BÖLÜM 2: BASELINE (Change=0) ORTALAMA İNCİDENCE")
print("="*100)

baseline_records = [r for r in yoy_data if r['change'] == 0 and r['n'] > 100]
print(f"\nBaseline kayıtları (change=0, n>100): {len(baseline_records):,}")

if baseline_records:
    diseases = ['t2d', 'hypertension', 'dyslipidaemia', 'asthma', 'sleep_apnoea', 
                'osteoarthritis', 'hf', 'ckd', 'af', 'unstable_angina_mi']
    
    print(f"\n{'Hastalık':<20} {'Ort. Incidence':<15} {'Min-Max':<20} {'Kayıt Sayısı'}")
    print("-"*80)
    
    baseline_incidences = {}
    for disease in diseases:
        incidences = [(r[disease] / r['n']) for r in baseline_records if r['n'] > 0]
        if incidences:
            avg = statistics.mean(incidences)
            min_val = min(incidences)
            max_val = max(incidences)
            baseline_incidences[disease] = avg
            print(f"{disease:<20} {avg*100:>6.3f}%       {min_val*100:>5.3f}%-{max_val*100:>5.3f}%    {len(incidences):>6,}")

# =====================================================================
# 3. -15% KİLO KAYBI İLE KARŞILAŞTIRMA
# =====================================================================
print("\n" + "="*100)
print("BÖLÜM 3: -15% KİLO KAYBI İLE İNCİDENCE KARŞILAŞTIRMASI")
print("="*100)

intervention_records = [r for r in yoy_data if r['change'] == -15 and r['n'] > 100]
print(f"\nMüdahale kayıtları (change=-15, n>100): {len(intervention_records):,}")

if intervention_records and baseline_records:
    print(f"\n{'Hastalık':<20} {'Baseline':<12} {'Müdahale':<12} {'Azalma':<12} {'RRR %'}")
    print("-"*80)
    
    disease_reductions = {}
    for disease in diseases:
        base_inc = [r[disease]/r['n'] for r in baseline_records if r['n'] > 0 and disease in r]
        interv_inc = [r[disease]/r['n'] for r in intervention_records if r['n'] > 0 and disease in r]
        
        if base_inc and interv_inc:
            avg_base = statistics.mean(base_inc)
            avg_interv = statistics.mean(interv_inc)
            reduction = avg_base - avg_interv
            rrr = (reduction / avg_base * 100) if avg_base > 0 else 0
            
            disease_reductions[disease] = {
                'baseline': avg_base,
                'intervention': avg_interv,
                'reduction': reduction,
                'rrr': rrr
            }
            
            print(f"{disease:<20} {avg_base*100:>6.3f}%    {avg_interv*100:>6.3f}%    {reduction*100:>6.3f}%    {rrr:>6.1f}%")

# =====================================================================
# 4. POPÜLASYON 1000 İÇİN COST HESAPLAMA (6 YIL)
# =====================================================================
print("\n" + "="*100)
print("BÖLÜM 4: 1000 KİŞİ İÇİN 6 YILLIK MALİYET TASARRUFU HESAPLAMA")
print("="*100)

population = 1000
cost_per_case = 1000
time_horizon = 6

print(f"\nParametreler:")
print(f"  - Popülasyon: {population:,} kişi")
print(f"  - Vaka başı maliyet: {cost_per_case:,} TL")
print(f"  - Time horizon: {time_horizon} yıl")
print(f"  - Varsayım: Waning/discount/weight regain YOK (basit çarpma)")

print(f"\n{'Hastalık':<20} {'Yıllık Vaka':<15} {'6 Yıl Vaka':<15} {'Maliyet (6 yıl)':<20}")
print("-"*90)

for disease in diseases:
    if disease in disease_reductions:
        yearly_cases = disease_reductions[disease]['reduction'] * population
        total_cases = yearly_cases * time_horizon
        total_cost = total_cases * cost_per_case
        
        print(f"{disease:<20} {yearly_cases:>8.1f}       {total_cases:>8.1f}        {total_cost:>15,.0f} TL")

# =====================================================================
# 5. T2D İÇİN DETAYLI ANALİZ
# =====================================================================
print("\n" + "="*100)
print("BÖLÜM 5: T2D İÇİN DETAYLI ANALİZ - GERÇEK YAZILIM KARŞILAŞTIRMASI")
print("="*100)

if 't2d' in disease_reductions:
    t2d_data = disease_reductions['t2d']
    
    print(f"\nT2D CPRD Verileri:")
    print(f"  Baseline incidence: {t2d_data['baseline']*100:.3f}%")
    print(f"  -15% kilo kaybı sonrası: {t2d_data['intervention']*100:.3f}%")
    print(f"  Azalma: {t2d_data['reduction']*100:.3f}% puan")
    print(f"  RRR: {t2d_data['rrr']:.1f}%")
    
    # Basit model (waning/discount yok)
    yearly_cases = t2d_data['reduction'] * population
    cost_6yr_simple = yearly_cases * time_horizon * cost_per_case
    
    print(f"\nBASİT MODEL (Waning/Discount YOK):")
    print(f"  Yıllık önlenen vaka: {yearly_cases:.1f}")
    print(f"  6 yıl toplam vaka: {yearly_cases * time_horizon:.1f}")
    print(f"  6 yıl maliyet tasarrufu: {cost_6yr_simple:,.0f} TL")
    print(f"\n  >>> GERCEK YAZILIM: 108,518 TL")
    print(f"  >>> FARK: {108518 - cost_6yr_simple:,.0f} TL")
    
    if cost_6yr_simple > 0:
        ratio = 108518 / cost_6yr_simple
        print(f"  >>> CARPAN: {ratio:.2f}x")
        
        print(f"\n  Bu farkı kapatmak için:")
        print(f"    - Vaka başı maliyet: {cost_per_case * ratio:,.0f} TL olmalı")
        print(f"    - VEYA popülasyon: {population * ratio:,.0f} kişi olmalı")
        print(f"    - VEYA başka faktörler var (discount kapalı, nominal büyüme, vs.)")

# =====================================================================
# 6. YEAR BY YEAR İNCİDENCE TRENDİ
# =====================================================================
print("\n" + "="*100)
print("BÖLÜM 6: YILLAR ARASI İNCİDENCE TRENDİ (-15% kilo kaybı)")
print("="*100)

# -15% için yıllık trend
intervention_by_year = {}
for r in intervention_records:
    year = r['year']
    if year not in intervention_by_year:
        intervention_by_year[year] = []
    intervention_by_year[year].append(r)

print(f"\n{'Year':<8} {'T2D Avg %':<12} {'HT Avg %':<12} {'Dyslip Avg %':<12} {'Kayıt'}")
print("-"*70)

for year in sorted(intervention_by_year.keys()):
    records = intervention_by_year[year]
    t2d_avg = statistics.mean([r['t2d']/r['n'] for r in records if r['n'] > 0]) * 100
    ht_avg = statistics.mean([r['hypertension']/r['n'] for r in records if r['n'] > 0]) * 100
    dyslip_avg = statistics.mean([r['dyslipidaemia']/r['n'] for r in records if r['n'] > 0]) * 100
    
    print(f"{year:<8} {t2d_avg:>8.3f}%    {ht_avg:>8.3f}%    {dyslip_avg:>8.3f}%    {len(records):>6,}")

print("\n" + "="*100)
print("ANALİZ TAMAMLANDI!")
print("="*100)

