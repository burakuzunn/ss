import json

with open('cprd-data.prettier_complete.json', encoding='utf-8') as f:
    data = json.load(f)

# 60 yaş, BMI 30, Erkek
age_bin, bmi, gender = 60, 30, 1

print("="*100)
print("CPRD YEAR-ON-YEAR: KİLO DEĞİŞİMİ VE HASTALIK İNCİDENCE KARŞILAŞTIRMASI")
print("="*100)
print(f"\nParametreler: Yaş={age_bin}, BMI={bmi}, Cinsiyet={'Erkek' if gender else 'Kadın'}")
print("\n" + "-"*100)

# Change değerlerine göre grupla
changes = {}
for r in data['cprdDataYearOnYear']:
    if r['age_bin'] == age_bin and r['bmi'] == bmi and r['gendermale'] == gender:
        change = r['change']
        if change not in changes:
            changes[change] = []
        changes[change].append(r)

# Sıralı göster
for change in sorted(changes.keys(), reverse=True):
    records = changes[change]
    if records:
        # İlk year'ı al (hepsi aynı olmalı)
        r = records[0]
        t2d_inc = (r['t2d'] / r['n'] * 100) if r['n'] > 0 else 0
        ht_inc = (r['hypertension'] / r['n'] * 100) if r['n'] > 0 else 0
        dyslip_inc = (r['dyslipidaemia'] / r['n'] * 100) if r['n'] > 0 else 0
        
        print(f"Kilo Değişimi: {change:+.0f}%")
        print(f"  T2D:         {t2d_inc:.3f}%")
        print(f"  Hypertension: {ht_inc:.3f}%")
        print(f"  Dyslipidemi:  {dyslip_inc:.3f}%")
        print()

# BASELINE vs -15% FARK HESAPLA
baseline = next((r for r in data['cprdDataYearOnYear'] 
                 if r['age_bin']==age_bin and r['bmi']==bmi and r['gendermale']==gender and r['change']==0), None)

intervention = next((r for r in data['cprdDataYearOnYear'] 
                     if r['age_bin']==age_bin and r['bmi']==bmi and r['gendermale']==gender and r['change']==-15), None)

if baseline and intervention and baseline['n'] > 0:
    print("="*100)
    print("KRİTİK KARŞILAŞTIRMA: Baseline (0%) vs Müdahale (-15%)")
    print("="*100)
    
    baseline_t2d = (baseline['t2d'] / baseline['n'])
    baseline_ht = (baseline['hypertension'] / baseline['n'])
    baseline_dyslip = (baseline['dyslipidaemia'] / baseline['n'])
    
    interv_t2d = (intervention['t2d'] / intervention['n'])
    interv_ht = (intervention['hypertension'] / intervention['n'])
    interv_dyslip = (intervention['dyslipidaemia'] / intervention['n'])
    
    print(f"\nBaseline (0% kilo değişimi):")
    print(f"  n = {baseline['n']:,}")
    print(f"  T2D:         {baseline_t2d*100:.3f}%")
    print(f"  Hypertension: {baseline_ht*100:.3f}%")
    print(f"  Dyslipidemi:  {baseline_dyslip*100:.3f}%")
    
    print(f"\nMüdahale (-15% kilo kaybı):")
    print(f"  n = {intervention['n']:,}")
    print(f"  T2D:         {interv_t2d*100:.3f}%")
    print(f"  Hypertension: {interv_ht*100:.3f}%")
    print(f"  Dyslipidemi:  {interv_dyslip*100:.3f}%")
    
    print(f"\n📉 İNCIDENCE AZALMASI (Baseline - Müdahale):")
    print(f"  T2D:         {(baseline_t2d - interv_t2d)*100:.3f}% puan azalma")
    print(f"  Hypertension: {(baseline_ht - interv_ht)*100:.3f}% puan azalma")
    print(f"  Dyslipidemi:  {(baseline_dyslip - interv_dyslip)*100:.3f}% puan azalma")
    
    # RRR hesapla
    rrr_t2d = ((baseline_t2d - interv_t2d) / baseline_t2d * 100) if baseline_t2d > 0 else 0
    rrr_ht = ((baseline_ht - interv_ht) / baseline_ht * 100) if baseline_ht > 0 else 0
    rrr_dyslip = ((baseline_dyslip - interv_dyslip) / baseline_dyslip * 100) if baseline_dyslip > 0 else 0
    
    print(f"\n📊 RELATIVE RISK REDUCTION (RRR):")
    print(f"  T2D:         {rrr_t2d:.1f}%")
    print(f"  Hypertension: {rrr_ht:.1f}%")
    print(f"  Dyslipidemi:  {rrr_dyslip:.1f}%")
    
    # 1000 kişi için önlenen vakalar
    pop = 1000
    print(f"\n🎯 1000 KİŞİ İÇİN ÖNLENEN VAKALAR (yıllık):")
    print(f"  T2D:         {(baseline_t2d - interv_t2d) * pop:.1f} vaka")
    print(f"  Hypertension: {(baseline_ht - interv_ht) * pop:.1f} vaka")
    print(f"  Dyslipidemi:  {(baseline_dyslip - interv_dyslip) * pop:.1f} vaka")
    
    # 6 yıl için (basit çarpma, waning/regain yok)
    print(f"\n💰 6 YIL İÇİN MALİYET TASARRUFU (1000 TL/vaka, discount/waning YOK):")
    t2d_6yr = (baseline_t2d - interv_t2d) * pop * 6 * 1000
    ht_6yr = (baseline_ht - interv_ht) * pop * 6 * 1000
    dyslip_6yr = (baseline_dyslip - interv_dyslip) * pop * 6 * 1000
    
    print(f"  T2D:         {t2d_6yr:,.0f} TL (Gerçek yazılım: 108,518 TL)")
    print(f"  Hypertension: {ht_6yr:,.0f} TL")
    print(f"  Dyslipidemi:  {dyslip_6yr:,.0f} TL")
    
    print("="*100)

