import json
import statistics

with open('cprd-data.prettier_complete.json', encoding='utf-8') as f:
    data = json.load(f)

yoy_data = data['cprdDataYearOnYear']

print("="*100)
print("YEAR 1 BAZLI ANALIZ - GERCEK YAZILIM METODOLOJISI")
print("="*100)

# YEAR 1: Baseline (change=0) vs Intervention (change=-15)
baseline_y1 = [r for r in yoy_data if r['change'] == 0 and r['year'] == 1 and r['n'] > 100]
intervention_y1 = [r for r in yoy_data if r['change'] == -15 and r['year'] == 1 and r['n'] > 100]

print(f"\nYear 1 Baseline kayitlari (change=0): {len(baseline_y1):,}")
print(f"Year 1 Intervention kayitlari (change=-15): {len(intervention_y1):,}")

# T2D, HT, Dyslipidaemia için hesaplama
diseases = ['t2d', 'hypertension', 'dyslipidaemia']
disease_names = {'t2d': 'T2D', 'hypertension': 'Hypertension', 'dyslipidaemia': 'Dyslipidaemia'}

print("\n" + "="*100)
print("YEAR 1 INCIDENCE KARSILASTIRMASI")
print("="*100)

results = {}
for disease in diseases:
    base_inc = [r[disease]/r['n'] for r in baseline_y1 if r['n'] > 0]
    interv_inc = [r[disease]/r['n'] for r in intervention_y1 if r['n'] > 0]
    
    if base_inc and interv_inc:
        avg_base = statistics.mean(base_inc)
        avg_interv = statistics.mean(interv_inc)
        reduction = avg_base - avg_interv
        rrr = (reduction / avg_base * 100) if avg_base > 0 else 0
        
        results[disease] = {
            'baseline': avg_base,
            'intervention': avg_interv,
            'reduction': reduction,
            'rrr': rrr
        }
        
        print(f"\n{disease_names[disease]}:")
        print(f"  Baseline (Year 1, change=0):  {avg_base*100:.3f}%")
        print(f"  Intervention (Year 1, -15%):  {avg_interv*100:.3f}%")
        print(f"  Reduction:                     {reduction*100:.3f}% puan")
        print(f"  RRR:                           {rrr:.1f}%")

# 1000 kisi icin 6 yillik hesaplama (farkli senaryolar)
print("\n" + "="*100)
print("1000 KISI, 6 YIL ICIN MALIYET TASARRUFU HESAPLAMALARI")
print("="*100)

population = 1000
cost_per_case = 1000
time_horizon = 6

print(f"\nParametreler: Pop={population:,}, Cost/vaka={cost_per_case:,} TL, Horizon={time_horizon} yil")

if 't2d' in results:
    t2d = results['t2d']
    yearly_cases_y1 = t2d['reduction'] * population
    
    print(f"\nT2D YEAR 1 INCIDENCE BAZLI:")
    print(f"  Yillik onlenen vaka (Year 1 incidence): {yearly_cases_y1:.1f}")
    
    # Senaryo 1: Basit carpma (waning/discount yok)
    cost_simple = yearly_cases_y1 * time_horizon * cost_per_case
    print(f"\n  Senaryo 1 - Basit carpma (waning/discount YOK):")
    print(f"    6 yil vaka: {yearly_cases_y1 * time_horizon:.1f}")
    print(f"    Maliyet: {cost_simple:,.0f} TL")
    print(f"    Gercek: 108,518 TL | Fark: {108518 - cost_simple:,.0f} TL")
    
    # Senaryo 2: Discount var (%3.5)
    discount_rate = 0.035
    total_npv = 0
    for y in range(1, time_horizon + 1):
        df = 1.0 / ((1 + discount_rate) ** (y - 1))
        total_npv += yearly_cases_y1 * cost_per_case * df
    
    print(f"\n  Senaryo 2 - Discount var (%3.5 NPV):")
    print(f"    Maliyet NPV: {total_npv:,.0f} TL")
    print(f"    Gercek: 108,518 TL | Fark: {108518 - total_npv:,.0f} TL")
    
    # Senaryo 3: Yillik incidence artisi var (CPRD'deki gibi)
    # Year 1: 0.911%, Year 2: 1.960%, ... Year 6: 6.049%
    # Ama baseline'dan fark alinmali
    
    # Baseline Year 1-6 ortalama
    baseline_years = {}
    intervention_years = {}
    for y in range(1, 7):
        b_y = [r['t2d']/r['n'] for r in yoy_data if r['change']==0 and r['year']==y and r['n']>100]
        i_y = [r['t2d']/r['n'] for r in yoy_data if r['change']==-15 and r['year']==y and r['n']>100]
        if b_y and i_y:
            baseline_years[y] = statistics.mean(b_y)
            intervention_years[y] = statistics.mean(i_y)
    
    print(f"\n  Senaryo 3 - Her yil farkli incidence (CPRD year-by-year):")
    total_cases_yearly = 0
    total_cost_yearly = 0
    for y in range(1, 7):
        if y in baseline_years and y in intervention_years:
            reduction_y = baseline_years[y] - intervention_years[y]
            cases_y = reduction_y * population
            cost_y = cases_y * cost_per_case
            total_cases_yearly += cases_y
            total_cost_yearly += cost_y
            print(f"    Year {y}: Baseline={baseline_years[y]*100:.3f}%, -15%={intervention_years[y]*100:.3f}%, "
                  f"Reduction={reduction_y*100:.3f}%, Vakalar={cases_y:.1f}, Cost={cost_y:,.0f} TL")
    
    print(f"\n    TOPLAM 6 yil:")
    print(f"      Vakalar: {total_cases_yearly:.1f}")
    print(f"      Maliyet: {total_cost_yearly:,.0f} TL")
    print(f"      Gercek: 108,518 TL | Fark: {108518 - total_cost_yearly:,.0f} TL")
    
    # Senaryo 4: Year-by-year + Discount
    total_cost_yearly_npv = 0
    for y in range(1, 7):
        if y in baseline_years and y in intervention_years:
            reduction_y = baseline_years[y] - intervention_years[y]
            cases_y = reduction_y * population
            df = 1.0 / ((1 + discount_rate) ** (y - 1))
            cost_y_npv = cases_y * cost_per_case * df
            total_cost_yearly_npv += cost_y_npv
    
    print(f"\n  Senaryo 4 - Year-by-year + Discount (%3.5):")
    print(f"    Maliyet NPV: {total_cost_yearly_npv:,.0f} TL")
    print(f"    Gercek: 108,518 TL | Fark: {108518 - total_cost_yearly_npv:,.0f} TL")
    
    # Senaryo 5: Ters hesaplama - 108,518'e ulasmak icin ne gerekli?
    print(f"\n  >>> TERS HESAPLAMA: 108,518 TL'ye ulasmak icin:")
    
    # Basit carpma ile
    required_yearly = 108518 / (time_horizon * cost_per_case)
    required_inc = required_yearly / population
    print(f"    Basit model: Yillik {required_yearly:.1f} vaka = {required_inc*100:.3f}% incidence reduction gerekli")
    print(f"    Mevcut Year 1 reduction: {t2d['reduction']*100:.3f}%")
    
    # Cost/vaka ile
    required_cost = 108518 / (yearly_cases_y1 * time_horizon)
    print(f"    VEYA vaka basi maliyet: {required_cost:,.0f} TL olmali (mevcut: 1,000 TL)")
    
    # Populasyon ile
    required_pop = 108518 / (t2d['reduction'] * time_horizon * cost_per_case)
    print(f"    VEYA populasyon: {required_pop:,.0f} kisi olmali (mevcut: 1,000)")

print("\n" + "="*100)
print("ANALIZ TAMAMLANDI!")
print("="*100)

