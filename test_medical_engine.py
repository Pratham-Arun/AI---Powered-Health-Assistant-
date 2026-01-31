from medical_engine import engine
import re

def test_emergency():
    response = engine.process_query("I have severe chest pain")
    print("Testing Emergency...")
    assert "🚨" in response
    assert re.search(r"emergency", response, re.IGNORECASE)
    print("✅ test_emergency passed")

def test_condition_explanation():
    print("Testing Explanation...")
    response = engine.process_query("What is a headache?")
    assert re.search(r"headache", response, re.IGNORECASE)
    assert re.search(r"what it is|explanation", response, re.IGNORECASE)
    print("✅ test_condition_explanation passed")

def test_consultation_guidance():
    print("Testing Consultation Guidance...")
    response = engine.process_query("fever")
    assert re.search(r"consult a doctor", response, re.IGNORECASE)
    print("✅ test_consultation_guidance passed")

def test_fatigue_and_tests():
    print("Testing Fatigue and Tests...")
    # Test for fatigue keyword
    response = engine.process_query("chronic fatigue")
    assert re.search(r"fatigue", response, re.IGNORECASE)
    assert re.search(r"consult a doctor", response, re.IGNORECASE)
    
    # Test for anemia/blood loss (diagnostic tests)
    response = engine.process_query("I think I have anemia and blood loss")
    assert re.search(r"anemia", response, re.IGNORECASE)
    assert re.search(r"tests to get|recommended tests", response, re.IGNORECASE)
    assert "Complete Blood Count (CBC)" in response
    print("✅ test_fatigue_and_tests passed")

def test_otc_meds():
    print("Testing OTC Medications...")
    response = engine.process_query("headache relief")
    assert "Common Over-the-Counter (OTC) Relief" in response
    assert "Paracetamol" in response
    assert "CAUTION" in response
    print("✅ test_otc_meds passed")

def test_blood_profiles():
    print("Testing Blood Profiles...")
    response = engine.process_query("what are common blood tests")
    assert "Common Diagnostic Profiles" in response
    assert "Lipid Profile" in response
    assert "Liver Function Test" in response
    print("✅ test_blood_profiles passed")

def test_greeting():
    print("Testing Greeting...")
    response = engine.process_query("Hello")
    assert re.search(r"health assistant", response, re.IGNORECASE)
    print("✅ test_greeting passed")

if __name__ == "__main__":
    print("Running Full Diagnostic Tests...\n")
    try:
        test_emergency()
        test_condition_explanation()
        test_consultation_guidance()
        test_fatigue_and_tests()
        test_otc_meds()
        test_blood_profiles()
        test_greeting()
        print("\n🎉 All tests passed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        # Print the response that failed the test for debugging
        print("\nLast Response Output:")
        print("-" * 20)
        # We don't have the last response here easily, but the print above helps
        import traceback
        traceback.print_exc()
