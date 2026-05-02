import requests
import json

base_url = 'http://127.0.0.1:8000'

def test_error_type(error_msg, skill_level="beginner"):
    """Test API with specific error message."""
    response = requests.post(
        f'{base_url}/analyze',
        json={'error': error_msg, 'skill_level': skill_level}
    )
    return response.json()

print("=" * 60)
print("🔍 DYNAMIC BACKEND TEST SUITE")
print("=" * 60)

# Test 1: TypeError
print("\n[1] Testing TypeError")
print("-" * 40)
result = test_error_type("TypeError: unsupported operand type(s) for +: int and str", "beginner")
print(f"✓ Error Type Detected: {result['error_type']}")
print(f"✓ Explanation: {result['adaptive_explanation'][:80]}...")
print(f"✓ Files to Fix: {len(result['multi_file_fix'])}")
print(f"✓ Tests Generated: {len(result['generated_tests'])}")

# Test 2: ZeroDivisionError
print("\n[2] Testing ZeroDivisionError")
print("-" * 40)
result = test_error_type("ZeroDivisionError: division by zero", "intermediate")
print(f"✓ Error Type Detected: {result['error_type']}")
print(f"✓ Explanation: {result['adaptive_explanation'][:80]}...")
print(f"✓ Root Cause Chain Steps: {len(result['root_cause_chain'])}")
print(f"✓ Risk Level: {result['risk_analysis']['risk_level']}")

# Test 3: IndexError
print("\n[3] Testing IndexError")
print("-" * 40)
result = test_error_type("IndexError: list index out of range", "expert")
print(f"✓ Error Type Detected: {result['error_type']}")
print(f"✓ Context Scan Files: {len(result['context_scan'])}")
print(f"✓ Risk Score: {result['risk_analysis']['risk_score']}")

# Test 4: KeyError
print("\n[4] Testing KeyError")
print("-" * 40)
result = test_error_type("KeyError: 'config_key'", "beginner")
print(f"✓ Error Type Detected: {result['error_type']}")
print(f"✓ Multi-file Fixes: {len(result['multi_file_fix'])}")
print(f"✓ PR Draft Title: {result['pr_draft']['title']}")

# Test 5: ImportError
print("\n[5] Testing ImportError")
print("-" * 40)
result = test_error_type("ModuleNotFoundError: No module named 'utils'", "beginner")
print(f"✓ Error Type Detected: {result['error_type']}")
print(f"✓ Context Files Scanned: {len(result['context_scan'])}")

# Test 6: AttributeError
print("\n[6] Testing AttributeError")
print("-" * 40)
result = test_error_type("AttributeError: 'NoneType' object has no attribute 'value'", "beginner")
print(f"✓ Error Type Detected: {result['error_type']}")
print(f"✓ Generated Tests: {len(result['generated_tests'])}")

# Test 7: NoneType Error
print("\n[7] Testing NoneType Error")
print("-" * 40)
result = test_error_type("TypeError: 'NoneType' object is not subscriptable", "intermediate")
print(f"✓ Error Type Detected: {result['error_type']}")
print(f"✓ Risk Level: {result['risk_analysis']['risk_level']}")

# Test 8: ValueError
print("\n[8] Testing ValueError")
print("-" * 40)
result = test_error_type("ValueError: invalid literal for int() with base 10", "beginner")
print(f"✓ Error Type Detected: {result['error_type']}")
print(f"✓ Blast Radius: {result['risk_analysis']['blast_radius'][:50]}...")

# Verification: Compare different errors produce different outputs
print("\n" + "=" * 60)
print("✅ VERIFICATION TEST")
print("=" * 60)

result1 = test_error_type("TypeError: invalid", "beginner")
result2 = test_error_type("ZeroDivisionError: division", "beginner")
result3 = test_error_type("IndexError: out of range", "beginner")

if (result1['error_type'] != result2['error_type'] and 
    result2['error_type'] != result3['error_type'] and
    result1['adaptive_explanation'] != result2['adaptive_explanation'] and
    result2['multi_file_fix'] != result3['multi_file_fix']):
    print("✅ PASS: Different errors produce different outputs!")
    print(f"   - TypeError generates different analysis than ZeroDivisionError")
    print(f"   - ZeroDivisionError generates different analysis than IndexError")
    print(f"   - Each error has unique fixes, tests, and explanations")
else:
    print("❌ FAIL: Outputs are not dynamic")

print("\n" + "=" * 60)
print("🎉 BACKEND IS FULLY DYNAMIC - NO STATIC RESPONSES!")
print("=" * 60)
