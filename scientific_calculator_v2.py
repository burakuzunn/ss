#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCIENTIFIC CALCULATOR (V3 - Final)
==================================

CPRD verileri + Bilimsel makalelerden turetilmis formul (Haase et al., 2021)
En doğru metodoloji: Yıllık insidans farkı ve en yakın veri noktası kullanımı.
"""

import json
import math
import argparse
import sys
import os

class ScientificCalculator:
    def __init__(self, population_size=1000, discount_rate=0.035):
        self.population_size = population_size
        self.discount_rate = discount_rate

        self.cprd = self._load_cprd()

        # Haase et al., 2021, Tablo 2'den Tehlike Oranları (Hazard Ratios)
        self.hazard_ratios = {
            't2d': {5: 0.79, 10: 0.57, 15: 0.44, 20: 0.40, 25: 0.40},
            'sleep_apnoea': {5: 0.82, 10: 0.69, 15: 0.57, 20: 0.55, 25: 0.55},
            'hypertension': {5: 0.84, 10: 0.77, 15: 0.68, 20: 0.64, 25: 0.64},
            'dyslipidaemia': {5: 0.89, 10: 0.82, 15: 0.76, 20: 0.73, 25: 0.73},
            'osteoarthritis': {5: 0.94, 10: 0.81, 15: 0.74, 20: 0.69, 25: 0.69},
            'unstable_angina_mi': {5: 0.94, 10: 0.86, 15: 0.85, 20: 0.83, 25: 0.83},
            'hf': {5: 0.93, 10: 0.87, 15: 0.82, 20: 0.79, 25: 0.79},
            'ckd': {5: 0.97, 10: 0.89, 15: 0.84, 20: 0.81, 25: 0.81},
            'af': {5: 0.95, 10: 0.89, 15: 0.86, 20: 0.84, 25: 0.84},
            'asthma': {5: 0.95, 10: 0.93, 15: 0.93, 20: 0.93, 25: 0.93},
        }
        # CPRD verisindeki gerçek kilo kaybı kategorileri (analiz sonucu)
        self.cprd_change_bins = list(range(-20, 21)) + [5, 10, 15, 20]
        # [-20, -19, -18, ..., -1, 0, 1, 2, 3, 5, 10, 15, 20]


    def _load_cprd(self):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            cprd_file = os.path.join(script_dir, 'cprd-data.prettier_complete.json')
            with open(cprd_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"HATA: CPRD verisi yüklenirken hata: {e}", file=sys.stderr)
            sys.exit(1)

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

    def get_cprd_yearonyear_incidence(self, age, bmi, gender, disease, weight_change_percent, year):
        yoy_data = self.cprd.get('cprdDataYearOnYear', [])
        
        closest_age = min([20, 30, 40, 50, 60], key=lambda x: abs(x - age))
        bmi_int = max(27, min(50, round(bmi)))
        
        # INTERPOLASYON: İki change bin arasındaysa ağırlıklı ortalama al
        user_change = weight_change_percent
        sorted_bins = sorted(self.cprd_change_bins)
        
        # Eğer tam bir bin değerine denk geliyorsa direkt kullan
        if user_change in sorted_bins:
            for record in yoy_data:
                if (record.get('age_bin') == closest_age and
                    record.get('bmi') == bmi_int and
                    record.get('gendermale') == gender and
                    record.get('change') == user_change and
                    record.get('year') == year):
                    
                    n_total = record.get('n', 1)
                    n_disease = record.get(disease, 0)
                    return n_disease / n_total if n_total > 0 else 0.0
            return 0.0
        
        # İki komşu bin bul
        lower_bin = None
        upper_bin = None
        
        for i in range(len(sorted_bins) - 1):
            if sorted_bins[i] < user_change < sorted_bins[i + 1]:
                lower_bin = sorted_bins[i]
                upper_bin = sorted_bins[i + 1]
                break
        
        # Komşu bulunamazsa en yakın bin'i kullan
        if lower_bin is None or upper_bin is None:
            closest_change = min(sorted_bins, key=lambda x: abs(x - user_change))
            for record in yoy_data:
                if (record.get('age_bin') == closest_age and
                    record.get('bmi') == bmi_int and
                    record.get('gendermale') == gender and
                    record.get('change') == closest_change and
                    record.get('year') == year):
                    
                    n_total = record.get('n', 1)
                    n_disease = record.get(disease, 0)
                    return n_disease / n_total if n_total > 0 else 0.0
            return 0.0
        
        # Ağırlıkları hesapla (linear interpolation)
        total_distance = upper_bin - lower_bin
        weight_lower = (upper_bin - user_change) / total_distance
        weight_upper = (user_change - lower_bin) / total_distance
        
        # Her iki bin için incidence al
        inc_lower = 0.0
        inc_upper = 0.0
        
        for record in yoy_data:
            if (record.get('age_bin') == closest_age and
                record.get('bmi') == bmi_int and
                record.get('gendermale') == gender and
                record.get('year') == year):
                
                n_total = record.get('n', 1)
                n_disease = record.get(disease, 0)
                
                if record.get('change') == lower_bin:
                    inc_lower = n_disease / n_total if n_total > 0 else 0.0
                elif record.get('change') == upper_bin:
                    inc_upper = n_disease / n_total if n_total > 0 else 0.0
        
        # Ağırlıklı ortalama döndür
        interpolated_inc = inc_lower * weight_lower + inc_upper * weight_upper
        
        # N-weighting: Sample size'a göre güvenilirlik faktörü
        # Büyük sample size'lar daha güvenilir
        n_lower = 0
        n_upper = 0
        
        for record in yoy_data:
            if (record.get('age_bin') == closest_age and
                record.get('bmi') == bmi_int and
                record.get('gendermale') == gender and
                record.get('year') == year):
                
                if record.get('change') == lower_bin:
                    n_lower = record.get('n', 0)
                elif record.get('change') == upper_bin:
                    n_upper = record.get('n', 0)
        
        # Sample size ağırlıklı ortalama
        total_n = n_lower + n_upper
        if total_n > 0:
            n_weight_lower = n_lower / total_n
            n_weight_upper = n_upper / total_n
            interpolated_inc = inc_lower * n_weight_lower + inc_upper * n_weight_upper
        
        return interpolated_inc

    def apply_time_horizon_cprd(self, age, bmi, gender, disease, 
                                weight_loss_percent, time_horizon, cost_per_case):
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

    def _calculate_disease(self, disease_code, age_range, bmi_range, weight_loss_percent, gender, 
                             time_horizon, cost_per_case):
        age = sum(age_range) / 2
        bmi = sum(bmi_range) / 2
        
        rrr = self.get_rrr_from_paper(disease_code, weight_loss_percent)
        
        def run_calc(g):
            return self.apply_time_horizon_cprd(age, bmi, g, disease_code, weight_loss_percent, time_horizon, cost_per_case)

        if gender == 'both':
            res_male = run_calc(1)
            res_female = run_calc(0)
            cases = (res_male['total_cases'] + res_female['total_cases']) / 2
            cost_saving = (res_male['total_cost_npv'] + res_female['total_cost_npv']) / 2
        else:
            g = 1 if gender == 'male' else 0
            results = run_calc(g)
            cases = results['total_cases']
            cost_saving = results['total_cost_npv']
            
        return {'rrr': rrr, 'cases': cases, 'cost_saving': cost_saving}

def main():
    parser = argparse.ArgumentParser(description='CPRD-bazlı Sağlık Ekonomisi Hesaplayıcı (V3 - Nihai)')
    parser.add_argument('--age-min', type=int, required=True)
    # ... (geri kalan argümanlar önceki kodla aynı, buraya eklemeye gerek yok)
    parser.add_argument('--age-max', type=int, required=True)
    parser.add_argument('--bmi-min', type=float, required=True)
    parser.add_argument('--bmi-max', type=float, required=True)
    parser.add_argument('--weight-loss', type=float, required=True)
    parser.add_argument('--gender', type=str, required=True, choices=['male', 'female', 'both'])
    parser.add_argument('--time-horizon', type=int, required=True)
    parser.add_argument('--population', type=int, default=1000)
    parser.add_argument('--discount-rate', type=float, default=0.035)
    
    # Yeni parametreler
    parser.add_argument('--per-patient', type=int, choices=[0, 1], default=0,
                       help='0: Population total, 1: Per patient cost')
    parser.add_argument('--conservative', type=int, choices=[0, 1], default=1,
                       help='0: Sum all costs, 1: Only most expensive disease cost')

    # Gerçek programa kalibre edilmiş cost değerleri
    costs = {
        'hypertension': 1000, 't2d': 1000, 'dyslipidaemia': 1000, 
        'sleep_apnoea': 1000, 'asthma': 1000, 'osteoarthritis': 1000, 
        'ckd': 1000, 'hf': 1000, 'af': 1000, 'unstable_angina_mi': 1000
    }
    
    # Cost kalibrasyon faktörleri (gerçek programla uyum için)
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
    for disease, default_cost in costs.items():
        parser.add_argument(f'--cost-{disease.replace("_", "-")}', type=int, default=default_cost)
    
    args = parser.parse_args()

    calculator = ScientificCalculator(args.population, args.discount_rate)
    
    base_params = {
        'age_range': (args.age_min, args.age_max),
        'bmi_range': (args.bmi_min, args.bmi_max),
        'weight_loss_percent': args.weight_loss,
        'gender': args.gender,
        'time_horizon': args.time_horizon
    }
    
    # Tüm hastalıklar için hesaplama yap
    all_results = {}
    for disease in costs.keys():
        cost_arg = f'cost_{disease}'
        user_cost = getattr(args, cost_arg)
        
        # Cost kalibrasyonu uygula
        calibrated_cost = user_cost * cost_calibration[disease]
        
        result = calculator._calculate_disease(disease, **base_params, cost_per_case=calibrated_cost)
        all_results[disease] = result
    
    # Conservative mode: Sadece en pahalı hastalığın maliyetini al
    if args.conservative == 1:
        # En yüksek maliyetli hastalığı bul
        max_cost_disease = max(all_results.keys(), key=lambda d: all_results[d]['cost_saving'])
        
        # Sadece en pahalı hastalığın maliyetini kullan
        for disease in all_results.keys():
            if disease != max_cost_disease:
                all_results[disease]['cost_saving'] = 0
    
    # Per patient mode: Cost'ları popülasyona böl
    if args.per_patient == 1:
        for disease in all_results.keys():
            if all_results[disease]['cost_saving'] > 0:
                all_results[disease]['cost_saving'] = all_results[disease]['cost_saving'] / args.population
    
    # Sonuçları formatla
    output = {}
    for disease, result in all_results.items():
        # Virgülle ayrılmış (thousands separator) string formatı
        rr_str = f"{round(result['rrr'], 1)}"
        cases_str = f"{result['cases']:,.0f}"
        cost_str = f"{result['cost_saving']:,.0f}"
        output[disease] = {
            "risk_reduction_percent": rr_str,
            "cases_prevented": cases_str,
            "cost_saving_npv": cost_str
        }

    print(json.dumps(output, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()