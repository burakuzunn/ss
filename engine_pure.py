#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ENGINE PURE
===========

Engine.js'in TAM algoritmasini kullanir
CPRD verilerini dogru sekilde okur
KALIBRASYON YOK - SADECE GERCEK ALGORITMA
"""

import json
import math

class EnginePure:
    def __init__(self, population_size=1000, hypertension_cost=1000):
        self.population_size = population_size
        self.hypertension_cost = hypertension_cost
        
        # CPRD verilerini yukle
        self.cprd = self._load_cprd()
        
    def _load_cprd(self):
        """CPRD verilerini yukle"""
        try:
            with open('cprd-data.prettier_complete.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {'cprdDataBaseline': [], 'cprdDataYearOnYear': []}
    
    def get_prevalence_from_cprd(self, age, bmi, gender, weight_change=0, year=0):
        """
        CPRD'den hipertansiyon prevalansi al
        
        Args:
            age: Yas (20-60)
            bmi: BMI (27-50)
            gender: Cinsiyet (0=kadin, 1=erkek)
            weight_change: Kilo degisimi % (baseline icin 0)
            year: Yil (baseline icin 0)
        
        Returns:
            Prevalans orani (0-1 arasi)
        """
        # En yakin yas grubu (20, 30, 40, 50, 60)
        age_bins = [20, 30, 40, 50, 60]
        closest_age = min(age_bins, key=lambda x: abs(x - age))
        
        # BMI yuvarla
        bmi_int = round(bmi)
        if bmi_int < 27:
            bmi_int = 27
        elif bmi_int > 50:
            bmi_int = 50
        
        if weight_change == 0:
            # BASELINE: cprdDataBaseline kullan
            baseline = self.cprd.get('cprdDataBaseline', [])
            
            for record in baseline:
                if (record.get('age_bin') == closest_age and
                    record.get('bmi') == bmi_int and
                    record.get('gendermale') == gender):
                    
                    n_total = record.get('n', 1)
                    n_ht = record.get('hypertension', 0)
                    
                    if n_total > 0:
                        return n_ht / n_total
        else:
            # MUDAHALE: cprdDataYearOnYear kullan
            year_on_year = self.cprd.get('cprdDataYearOnYear', [])
            
            # Change degerini yuvarla
            change_int = round(weight_change)
            
            for record in year_on_year:
                if (record.get('age_bin') == closest_age and
                    record.get('bmi') == bmi_int and
                    record.get('gendermale') == gender and
                    record.get('change') == change_int and
                    record.get('year') == year):
                    
                    n_total = record.get('n', 1)
                    n_ht = record.get('hypertension', 0)
                    
                    if n_total > 0:
                        return n_ht / n_total
        
        # Eslesme bulunamazsa varsayilan
        return 0.15
    
    def calculate_hypertension(self, age, bmi, weight_loss_percent, gender=1):
        """
        Hipertansiyon hesaplama - ENGINE.JS ALGORITMASI
        
        Algoritma (engine.js satir 15409-15411):
        arr13xJ287J296[yil][0] = 
          (col13xW53AF53[6] - col13xM53V53[6]) *  
          ((c8C32 ? arr7xF25F34[6][0] : 0) + (c8C33 ? row7xG25G34[6] : 0))
        
        Yani:
        Tasarruf = (Baseline_Hasta - Mudahale_Hasta) × Birim_Maliyet
        """
        
        # BASELINE (kilo kaybi OLMADAN)
        baseline_prevalence = self.get_prevalence_from_cprd(age, bmi, gender, weight_change=0, year=0)
        baseline_patients = self.population_size * baseline_prevalence
        
        # MUDAHALE (kilo kaybi ILE)
        # cprdDataYearOnYear'dan weight_change parametresiyle direkt ara!
        intervention_prevalence = self.get_prevalence_from_cprd(
            age, bmi, gender, 
            weight_change=weight_loss_percent,  # Direkt kilo kaybi %
            year=1  # Yil 1
        )
        intervention_patients = self.population_size * intervention_prevalence
        
        # HASTA FARKI (kacinilan vakalar)
        cases_prevented = baseline_patients - intervention_patients
        
        # RRR hesapla
        if baseline_prevalence > 0:
            rrr = ((baseline_prevalence - intervention_prevalence) / baseline_prevalence) * 100
        else:
            rrr = 0
        
        # MALIYET TASARRUFU
        # Engine.js formulu: Hasta_Farki × Birim_Maliyet
        cost_saving = cases_prevented * self.hypertension_cost
        
        return {
            'rrr': rrr,
            'cases': cases_prevented,
            'cost_saving': cost_saving,
            'baseline_prevalence': baseline_prevalence,
            'intervention_prevalence': intervention_prevalence,
            'baseline_patients': baseline_patients,
            'intervention_patients': intervention_patients
        }
    
    def analyze(self, age_range, bmi_range, weight_change_percent, gender, time_horizon=1):
        """
        Analiz yap - Disardan parametreler al
        
        Args:
            age_range: tuple (min_age, max_age) ornegin (20, 29)
            bmi_range: tuple (min_bmi, max_bmi) ornegin (27, 28)
            weight_change_percent: Kilo degisimi % (negatif = kayip)
            gender: 0=kadin, 1=erkek, 'both'=ikisi
            time_horizon: Yil sayisi (varsayilan=1)
        """
        # Yas ve BMI ortalamasi al
        age_avg = sum(age_range) / 2
        bmi_avg = sum(bmi_range) / 2
        
        if gender == 'both':
            # Hem erkek hem kadin icin hesapla ve ortala
            results_male = self.calculate_hypertension(age_avg, bmi_avg, weight_change_percent, gender=1)
            results_female = self.calculate_hypertension(age_avg, bmi_avg, weight_change_percent, gender=0)
            
            # Ortalama al
            results = {
                'rrr': (results_male['rrr'] + results_female['rrr']) / 2,
                'cases': (results_male['cases'] + results_female['cases']) / 2,
                'cost_saving': (results_male['cost_saving'] + results_female['cost_saving']) / 2
            }
        elif gender == 'male' or gender == 1:
            results = self.calculate_hypertension(age_avg, bmi_avg, weight_change_percent, gender=1)
        elif gender == 'female' or gender == 0:
            results = self.calculate_hypertension(age_avg, bmi_avg, weight_change_percent, gender=0)
        else:
            results = self.calculate_hypertension(age_avg, bmi_avg, weight_change_percent, gender=gender)
        
        # Time horizon ile carpim (cok yillik)
        if time_horizon > 1:
            results['cases'] = results['cases'] * time_horizon
            results['cost_saving'] = results['cost_saving'] * time_horizon
        
        # Print
        print("="*50)
        print("HIPERTANSIYON ANALIZ SONUCLARI")
        print("="*50)
        print(f"Relative Risk Reduction: %{results['rrr']:.1f}")
        print(f"Reduction in Cases: {results['cases']:.1f}")
        print(f"Cost Saving: {results['cost_saving']:,.0f} TL")
        print("="*50)
        
        return results

if __name__ == "__main__":
    # Ornek kullanim
    calculator = EnginePure(population_size=1000, hypertension_cost=1000)
    
  
    
    print("\n=== TEST 2: Age 40-49, BMI 30-35 ===")
    results2 = calculator.analyze(
        time_horizon=1,
        age_range=(40, 49),
        bmi_range=(30, 35),
        weight_change_percent=-20,
        gender='male'
    )

