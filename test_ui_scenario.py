#!/usr/bin/env python3
"""
UI Test Scenario
Senin UI'daki parametrelerle test
"""

from interactive_calculator import InteractiveCalculator

def test_ui_parameters():
    """
    UI Parametreleri:
    - Time horizon: 1 year
    - Population size: 1,000
    - Gender: Male and Female
    - Perspective: Hospital Type A
    - Age: 20-29
    - BMI: 27-28
    - Weight change: -20%
    - Hypertension cost: 1,000 TL
    
    Beklenen Sonuclar:
    - RRR: %32.8 (veya %32.6)
    - Cases: 2 (veya 6)
    - Cost Saving: 1697 TL (veya 9063 TL)
    """
    
    print("="*70)
    print("UI TEST SCENARIO")
    print("="*70)
    
    calculator = InteractiveCalculator()
    
    # Test 1: Erkek
    print("\n--- TEST 1: ERKEK ---")
    user_data = {
        'age': 25,
        'bmi': 27.5,
        'weight_loss': -20,
        'gender': 1
    }
    
    analysis = calculator.calculate_comprehensive_analysis(user_data)
    
    print(f"\nSonuclar:")
    print(f"  RRR: %{analysis['rrr']:.1f}")
    print(f"  Risk Oncesi: {analysis['risk_before']:.4f}")
    print(f"  Risk Sonrası: {analysis['risk_after']:.4f}")
    print(f"  Maliyet: {analysis['cost_data']['annual_saving']:,.0f} TL")
    
    # Cases hesapla
    cases = (analysis['risk_before'] - analysis['risk_after']) * 1000
    print(f"  Cases: {cases:.1f}")
    
    # Test 2: Kadın
    print("\n--- TEST 2: KADIN ---")
    user_data = {
        'age': 25,
        'bmi': 27.5,
        'weight_loss': -20,
        'gender': 0
    }
    
    analysis = calculator.calculate_comprehensive_analysis(user_data)
    
    print(f"\nSonuclar:")
    print(f"  RRR: %{analysis['rrr']:.1f}")
    print(f"  Risk Oncesi: {analysis['risk_before']:.4f}")
    print(f"  Risk Sonrası: {analysis['risk_after']:.4f}")
    print(f"  Maliyet: {analysis['cost_data']['annual_saving']:,.0f} TL")
    
    # Cases hesapla
    cases = (analysis['risk_before'] - analysis['risk_after']) * 1000
    print(f"  Cases: {cases:.1f}")
    
    print("\n" + "="*70)
    print("HEDEF DEGERLER:")
    print("  RRR: %32.6 - %32.8")
    print("  Cases: 2 - 6")
    print("  Cost: 1697 - 9063 TL")
    print("="*70)

if __name__ == "__main__":
    test_ui_parameters()

