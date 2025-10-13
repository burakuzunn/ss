import json

# CPRD year-on-year datasını oku
with open('cprd-data.prettier_complete.json', encoding='utf-8') as f:
    data = json.load(f)

# 60-69 yaş, BMI 30, Erkek için incidence'lara bak
print("="*80)
print("CPRD YEAR-ON-YEAR DATA - GERÇEK İNCIDENCE ORANLARI")
print("="*80)
print("\n60 yaş, BMI 30, Erkek:")
print("-"*80)

yoy = [r for r in data['cprdDataYearOnYear'] 
       if r['age_bin']==60 and r['bmi']==30 and r['gendermale']==1]

for r in yoy[:6]:
    t2d_inc = (r['t2d'] / r['n'] * 100) if r['n'] > 0 else 0
    ht_inc = (r['hypertension'] / r['n'] * 100) if r['n'] > 0 else 0
    dyslip_inc = (r['dyslipidaemia'] / r['n'] * 100) if r['n'] > 0 else 0
    
    print(f"Year {r['year']}: n={r['n']:,}")
    print(f"  T2D:         {r['t2d']:4d} / {r['n']:,} = {t2d_inc:.3f}%")
    print(f"  HT:          {r['hypertension']:4d} / {r['n']:,} = {ht_inc:.3f}%")
    print(f"  Dyslipidemi: {r['dyslipidaemia']:4d} / {r['n']:,} = {dyslip_inc:.3f}%")
    print(f"  Change:      {r['change']:.1f}%")
    print()

# Ortalama incidence hesapla (ilk 6 yıl)
if yoy:
    avg_t2d = sum(r['t2d']/r['n'] for r in yoy[:6]) / min(6, len(yoy))
    avg_ht = sum(r['hypertension']/r['n'] for r in yoy[:6]) / min(6, len(yoy))
    avg_dyslip = sum(r['dyslipidaemia']/r['n'] for r in yoy[:6]) / min(6, len(yoy))
    
    print("="*80)
    print("ORTALAMA ANNUAL INCIDENCE (İlk 6 yıl):")
    print("-"*80)
    print(f"T2D:         {avg_t2d*100:.3f}% (mevcut kullandığımız: 1.32%)")
    print(f"Hypertension: {avg_ht*100:.3f}% (mevcut kullandığımız: 2.42%)")
    print(f"Dyslipidemi:  {avg_dyslip*100:.3f}% (mevcut kullandığımız: 1.98%)")
    print("="*80)

# Farklı BMI'lar için karşılaştır
print("\n\nFARKLI BMI GRUPLARI (60 yaş, Erkek, Year 1):")
print("-"*80)
for bmi in [27, 30, 35, 40]:
    rec = next((r for r in data['cprdDataYearOnYear'] 
                if r['age_bin']==60 and r['bmi']==bmi and r['gendermale']==1 and r['year']==1), None)
    if rec and rec['n'] > 0:
        t2d_inc = rec['t2d'] / rec['n'] * 100
        ht_inc = rec['hypertension'] / rec['n'] * 100
        print(f"BMI {bmi}: T2D={t2d_inc:.3f}%, HT={ht_inc:.3f}%, n={rec['n']:,}")

