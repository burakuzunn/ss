#!/usr/bin/env python3
"""
Interactive Hypertension Risk Calculator
Hipertansiyon risk hesaplama ve maliyet analizi için interaktif sistem
"""

import math
import json
from typing import Dict, List, Any

# ===== FORMÜL SABİTLERİ =====
# wl.py'den alınan optimize edilmiş katsayılar
HYPERTENSION_BASE_RISK = 0.0038      # Temel hipertansiyon riski
BMI_HYPERTENSION_COEFF = 0.0135      # BMI katsayısı
AGE_HYPERTENSION_COEFF = 0.0058      # Yaş katsayısı
WEIGHT_LOSS_BP_COEFF = 1.6           # 1 kg kilo kaybı = 1.6 mmHg sistolik düşüş
WEIGHT_LOSS_RISK_REDUCTION = 0.0155  # Her %1 kilo kaybı için risk azaltımı

# Simülasyon parametreleri
POPULATION = 1000            # Test popülasyonu
ANNUAL_COST = 1000           # Yıllık maliyet (TL)
TIME_HORIZON = 1          # 10 yıllık simülasyon

class InteractiveCalculator:
    def __init__(self):
        self.results = {}
        
    def get_user_input(self):
        """Kullanıcıdan parametreleri alır"""
        print("=" * 60)
        print("HİPERTANSİYON RİSK HESAPLAYICI")
        print("CPRD verisi ile optimize edilmiş sistem")
        print("=" * 60)
        
        # Yaş girişi
        while True:
            try:
                age = int(input("Yaşınızı girin (20-80): "))
                if 20 <= age <= 80:
                    break
                else:
                    print("Lütfen 20-80 arası bir yaş girin!")
            except ValueError:
                print("Lütfen geçerli bir sayı girin!")
        
        # BMI girişi
        while True:
            try:
                bmi = float(input("BMI değerinizi girin (18-50): "))
                if 18 <= bmi <= 50:
                    break
                else:
                    print("Lütfen 18-50 arası bir BMI değeri girin!")
            except ValueError:
                print("Lütfen geçerli bir sayı girin!")
        
        # Kilo kaybı hedefi
        while True:
            try:
                weight_loss = float(input("Hedeflediğiniz kilo kaybı yüzdesi (0-30): "))
                if 0 <= weight_loss <= 30:
                    break
                else:
                    print("Lütfen 0-30 arası bir yüzde girin!")
            except ValueError:
                print("Lütfen geçerli bir sayı girin!")
        
        # Cinsiyet (opsiyonel)
        gender = input("Cinsiyetiniz (E/K) - opsiyonel: ").upper()
        gender_code = 1 if gender in ['E', 'ERKEK'] else 0
        
        return {
            'age': age,
            'bmi': bmi,
            'weight_loss': weight_loss,
            'gender': gender_code
        }
    
    def calculate_risk(self, age, bmi, weight_loss_percent):
        """Risk hesaplama fonksiyonu"""
        # Kilo kaybı sonrası BMI hesaplama
        weight_loss_factor = 1 - weight_loss_percent/100.0
        new_bmi = bmi * weight_loss_factor
        
        # Risk hesaplama (wl.py formülü)
        age_risk = AGE_HYPERTENSION_COEFF * age
        bmi_risk = BMI_HYPERTENSION_COEFF * new_bmi
        weight_loss_benefit = weight_loss_percent * WEIGHT_LOSS_RISK_REDUCTION
        
        # Toplam risk
        total_risk = HYPERTENSION_BASE_RISK * math.exp(age_risk + bmi_risk - weight_loss_benefit)
        
        return total_risk
    
    def calculate_rrr(self, age, bmi, weight_loss_percent):
        """Relative Risk Reduction hesaplama"""
        risk_before = self.calculate_risk(age, bmi, 0)
        risk_after = self.calculate_risk(age, bmi, weight_loss_percent)
        
        if risk_before > 0:
            rrr = ((risk_before - risk_after) / risk_before) * 100
            return rrr
        return 0
    
    def calculate_cases_prevented(self, age, bmi, weight_loss_percent):
        """Önlenen vaka sayısı"""
        risk_before = self.calculate_risk(age, bmi, 0)
        risk_after = self.calculate_risk(age, bmi, weight_loss_percent)
        
        cases_prevented = (risk_before - risk_after) * POPULATION
        return cases_prevented
    
    def calculate_cost_savings(self, age, bmi, weight_loss_percent):
        """Maliyet tasarrufu hesaplama"""
        cases_prevented = self.calculate_cases_prevented(age, bmi, weight_loss_percent)
        
        annual_saving = cases_prevented * ANNUAL_COST
        total_10year_saving = annual_saving * TIME_HORIZON
        
        return {
            'annual_saving': annual_saving,
            'total_10year_saving': total_10year_saving,
            'cases_prevented': cases_prevented
        }
    
    def calculate_bp_reduction(self, weight_loss_percent):
        """Kan basıncı düşüşü hesaplama"""
        # Ortalama ağırlık varsayımı
        avg_weight_kg = 70
        weight_loss_kg = avg_weight_kg * weight_loss_percent / 100
        
        systolic_reduction = weight_loss_kg * WEIGHT_LOSS_BP_COEFF
        diastolic_reduction = weight_loss_kg * 1.3  # 1 kg = 1.3 mmHg diyastolik
        
        return {
            'systolic_reduction': systolic_reduction,
            'diastolic_reduction': diastolic_reduction,
            'weight_loss_kg': weight_loss_kg
        }
    
    def get_risk_category(self, risk):
        """Risk kategorisini belirler"""
        if risk < 0.01:
            return "Cok Dusuk Risk"
        elif risk < 0.02:
            return "Dusuk Risk"
        elif risk < 0.05:
            return "Orta Risk"
        elif risk < 0.1:
            return "Yuksek Risk"
        else:
            return "Cok Yuksek Risk"
    
    def get_bmi_category(self, bmi):
        """BMI kategorisini belirler"""
        if bmi < 18.5:
            return "Zayif"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Fazla Kilolu"
        elif bmi < 35:
            return "Obez (1. Derece)"
        elif bmi < 40:
            return "Obez (2. Derece)"
        else:
            return "Morbid Obez (3. Derece)"
    
    def calculate_comprehensive_analysis(self, user_data):
        """Kapsamlı analiz hesaplama"""
        age = user_data['age']
        bmi = user_data['bmi']
        weight_loss = user_data['weight_loss']
        
        # Risk hesaplamaları
        risk_before = self.calculate_risk(age, bmi, 0)
        risk_after = self.calculate_risk(age, bmi, weight_loss)
        
        # RRR hesaplama
        rrr = self.calculate_rrr(age, bmi, weight_loss)
        
        # Maliyet hesaplamaları
        cost_data = self.calculate_cost_savings(age, bmi, weight_loss)
        
        # Kan basıncı hesaplamaları
        bp_data = self.calculate_bp_reduction(weight_loss)
        
        # Risk kategorileri
        risk_category_before = self.get_risk_category(risk_before)
        risk_category_after = self.get_risk_category(risk_after)
        
        # BMI kategorileri
        bmi_category_before = self.get_bmi_category(bmi)
        new_bmi = bmi * (1 - weight_loss/100.0)
        bmi_category_after = self.get_bmi_category(new_bmi)
        
        return {
            'user_data': user_data,
            'risk_before': risk_before,
            'risk_after': risk_after,
            'rrr': rrr,
            'cost_data': cost_data,
            'bp_data': bp_data,
            'risk_category_before': risk_category_before,
            'risk_category_after': risk_category_after,
            'bmi_before': bmi,
            'bmi_after': new_bmi,
            'bmi_category_before': bmi_category_before,
            'bmi_category_after': bmi_category_after
        }
    
    def print_results(self, analysis):
        """Sonuçları güzel formatta yazdırır"""
        print("\n" + "=" * 60)
        print("HESAPLAMA SONUÇLARI")
        print("=" * 60)
        
        # Kisisel bilgiler
        user = analysis['user_data']
        print(f"KISISEL BILGILER:")
        print(f"   Yas: {user['age']}")
        print(f"   Cinsiyet: {'Erkek' if user['gender'] == 1 else 'Kadin'}")
        print(f"   Mevcut BMI: {analysis['bmi_before']:.1f} ({analysis['bmi_category_before']})")
        print(f"   Hedef BMI: {analysis['bmi_after']:.1f} ({analysis['bmi_category_after']})")
        print(f"   Hedef Kilo Kaybi: %{user['weight_loss']} ({analysis['bp_data']['weight_loss_kg']:.1f} kg)")
        
        # Risk analizi
        print(f"\nRISK ANALIZI:")
        print(f"   Mevcut Risk: {analysis['risk_before']:.4f} ({analysis['risk_category_before']})")
        print(f"   Kilo Kaybi Sonrasi Risk: {analysis['risk_after']:.4f} ({analysis['risk_category_after']})")
        print(f"   Relative Risk Reduction: %{analysis['rrr']:.1f}")
        
        # Maliyet analizi
        cost = analysis['cost_data']
        print(f"\nMALIYET ANALIZI:")
        print(f"   Onlenen Vaka Sayisi (1000 kisi): {cost['cases_prevented']:.1f}")
        print(f"   Yillik Maliyet Tasarrufu: {cost['annual_saving']:,.0f} TL")
        print(f"   10 Yillik Toplam Tasarruf: {cost['total_10year_saving']:,.0f} TL")
        
        # Kan basinci analizi
        bp = analysis['bp_data']
        print(f"\nKAN BASINCI ANALIZI:")
        print(f"   Tahmini Sistolik BP Dususu: {bp['systolic_reduction']:.1f} mmHg")
        print(f"   Tahmini Diyastolik BP Dususu: {bp['diastolic_reduction']:.1f} mmHg")
        
        # Oneriler
        print(f"\nONERILER:")
        if analysis['rrr'] > 30:
            print("   MUKEMmel! Bu kilo kaybi hipertansiyon riskinizi onemli olcude azaltacak!")
        elif analysis['rrr'] > 20:
            print("   Iyi! Bu kilo kaybi hipertansiyon riskinizi orta duzeyde azaltacak.")
        elif analysis['rrr'] > 10:
            print("   Orta! Bu kilo kaybi hipertansiyon riskinizi hafif azaltacak.")
        else:
            print("   Dusuk etki. Daha fazla kilo kaybi dusunebilirsiniz.")
        
        if bp['systolic_reduction'] > 10:
            print("   Kan basininizda onemli dusus bekleniyor!")
        elif bp['systolic_reduction'] > 5:
            print("   Kan basininizda orta duzeyde dusus bekleniyor.")
        else:
            print("   Kan basininizda hafif dusus bekleniyor.")
        
        # Maliyet onerisi
        if cost['annual_saving'] > 10000:
            print("   Yuksek maliyet tasarrufu bekleniyor!")
        elif cost['annual_saving'] > 5000:
            print("   Orta duzeyde maliyet tasarrufu bekleniyor.")
        else:
            print("   Dusuk maliyet tasarrufu bekleniyor.")
    
    def save_results(self, analysis, filename="risk_analysis_results.json"):
        """Sonuçları JSON dosyasına kaydet"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            print(f"\nSonuclar kaydedildi: {filename}")
        except Exception as e:
            print(f"\nKaydetme hatasi: {e}")
    
    def run_calculator(self):
        """Ana hesaplayıcı fonksiyonu"""
        try:
            # Kullanıcı girişi
            user_data = self.get_user_input()
            
            # Hesaplama
            print(f"\nHesaplama yapiliyor...")
            analysis = self.calculate_comprehensive_analysis(user_data)
            
            # Sonuçları yazdır
            self.print_results(analysis)
            
            # Sonuçları kaydet
            self.save_results(analysis)
            
            # Tekrar hesaplama seçeneği
            print(f"\n" + "=" * 60)
            while True:
                again = input("Başka bir hesaplama yapmak ister misiniz? (E/H): ").upper()
                if again in ['E', 'H', 'EVET', 'HAYIR']:
                    if again in ['E', 'EVET']:
                        print("\n" + "-" * 60)
                        self.run_calculator()
                    break
                else:
                    print("Lütfen E (Evet) veya H (Hayır) girin!")
            
        except KeyboardInterrupt:
            print(f"\n\nHesaplama iptal edildi. Iyi gunler!")
        except Exception as e:
            print(f"\nHata olustu: {e}")

def main():
    """Ana fonksiyon"""
    print("HIPERTANSIYON RISK HESAPLAYICI")
    print("CPRD verisi ile optimize edilmis interaktif sistem")
    print("=" * 60)
    
    calculator = InteractiveCalculator()
    calculator.run_calculator()
    
    print(f"\nHesaplayici kapatildi. Saglikli gunler!")

if __name__ == "__main__":
    main()
