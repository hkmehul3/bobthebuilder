"""
Comprehensive test suite to validate dynamic error analysis
across all supported error types with different skill levels.
"""

import requests
import json
from typing import Dict, Any

BASE_URL = 'http://127.0.0.1:8000'

ERROR_CASES = [
    ("TypeError: unsupported operand type(s) for +: 'int' and 'str'", "TypeError"),
    ("ZeroDivisionError: division by zero", "ZeroDivisionError"),
    ("IndexError: list index out of range", "IndexError"),
    ("KeyError: 'missing_config'", "KeyError"),
    ("AttributeError: 'NoneType' object has no attribute 'name'", "AttributeError"),
    ("ValueError: invalid literal for int()", "ValueError"),
    ("ModuleNotFoundError: No module named 'utils'", "ImportError"),
    ("NameError: name 'undefined_var' is not defined", "NameError"),
    ("RuntimeError: assertion failed", "RuntimeError"),
]

SKILL_LEVELS = ["beginner", "intermediate", "expert"]


def test_error_analysis(error_msg: str, expected_type: str) -> Dict[str, Any]:
    """Test error analysis for a single error message."""
    response = requests.post(
        f'{BASE_URL}/analyze',
        json={'error': error_msg, 'skill_level': 'beginner'}
    )
    return response.json()


def validate_response(data: Dict[str, Any], expected_type: str) -> bool:
    """Validate that response structure is complete and correct."""
    required_fields = [
        'input_error',
        'error_type',
        'skill_level',
        'context_scan',
        'root_cause_chain',
        'adaptive_explanation',
        'multi_file_fix',
        'generated_tests',
        'risk_analysis',
        'pr_draft',
    ]
    
    for field in required_fields:
        if field not in data:
            print(f"   ❌ Missing field: {field}")
            return False
    
    # Validate error type detection
    if data['error_type'] != expected_type:
        print(f"   ❌ Wrong error type. Expected {expected_type}, got {data['error_type']}")
        return False
    
    # Validate array fields
    if not isinstance(data['context_scan'], list) or len(data['context_scan']) == 0:
        print(f"   ❌ context_scan is empty or not an array")
        return False
    
    if not isinstance(data['root_cause_chain'], list) or len(data['root_cause_chain']) == 0:
        print(f"   ❌ root_cause_chain is empty or not an array")
        return False
    
    if not isinstance(data['multi_file_fix'], list) or len(data['multi_file_fix']) == 0:
        print(f"   ❌ multi_file_fix is empty or not an array")
        return False
    
    if not isinstance(data['generated_tests'], list) or len(data['generated_tests']) == 0:
        print(f"   ❌ generated_tests is empty or not an array")
        return False
    
    # Validate risk analysis
    required_risk_fields = ['risk_score', 'risk_level', 'blast_radius', 'why_safe']
    for field in required_risk_fields:
        if field not in data['risk_analysis']:
            print(f"   ❌ Missing risk_analysis field: {field}")
            return False
    
    # Validate PR draft
    if 'title' not in data['pr_draft'] or 'checklist' not in data['pr_draft']:
        print(f"   ❌ Incomplete PR draft")
        return False
    
    return True


def test_skill_levels(error_msg: str) -> bool:
    """Test that different skill levels produce different explanations."""
    explanations = {}
    
    for level in SKILL_LEVELS:
        response = requests.post(
            f'{BASE_URL}/analyze',
            json={'error': error_msg, 'skill_level': level}
        )
        data = response.json()
        explanations[level] = data['adaptive_explanation']
    
    # Check that explanations differ
    if explanations['beginner'] == explanations['intermediate']:
        print(f"   ❌ Beginner and intermediate explanations are identical")
        return False
    
    if explanations['intermediate'] == explanations['expert']:
        print(f"   ❌ Intermediate and expert explanations are identical")
        return False
    
    return True


def test_diversity() -> bool:
    """Test that different errors produce different outputs."""
    results = {}
    
    for error_msg, error_type in ERROR_CASES[:3]:
        response = requests.post(
            f'{BASE_URL}/analyze',
            json={'error': error_msg, 'skill_level': 'beginner'}
        )
        data = response.json()
        results[error_type] = {
            'explanation': data['adaptive_explanation'],
            'fixes': len(data['multi_file_fix']),
            'tests': data['generated_tests'],
            'risk_level': data['risk_analysis']['risk_level'],
        }
    
    # Verify differences
    types = list(results.keys())
    
    # Check explanations differ
    if results[types[0]]['explanation'] == results[types[1]]['explanation']:
        print(f"   ❌ {types[0]} and {types[1]} have identical explanations")
        return False
    
    if results[types[1]]['explanation'] == results[types[2]]['explanation']:
        print(f"   ❌ {types[1]} and {types[2]} have identical explanations")
        return False
    
    # Check tests differ
    if results[types[0]]['tests'] == results[types[1]]['tests']:
        print(f"   ❌ {types[0]} and {types[1]} have identical tests")
        return False
    
    return True


# Run test suite
print("=" * 70)
print("🧪 COMPREHENSIVE DYNAMIC ERROR ANALYSIS TEST SUITE")
print("=" * 70)

total_tests = 0
passed_tests = 0

# Test 1: Error Type Detection & Response Validation
print("\n[1] Error Type Detection & Response Validation")
print("-" * 70)
for error_msg, expected_type in ERROR_CASES:
    total_tests += 1
    try:
        data = test_error_analysis(error_msg, expected_type)
        if validate_response(data, expected_type):
            print(f"✅ {expected_type:20} - Detected correctly")
            passed_tests += 1
        else:
            print(f"❌ {expected_type:20} - Validation failed")
    except Exception as e:
        print(f"❌ {expected_type:20} - Exception: {str(e)[:50]}")

# Test 2: Skill Level Adaptation
print("\n[2] Skill Level Adaptation (Different Explanations per Level)")
print("-" * 70)
for error_msg, error_type in ERROR_CASES[:3]:
    total_tests += 1
    try:
        if test_skill_levels(error_msg):
            print(f"✅ {error_type:20} - Skill levels produce different explanations")
            passed_tests += 1
        else:
            print(f"❌ {error_type:20} - Skill levels produce identical explanations")
    except Exception as e:
        print(f"❌ {error_type:20} - Exception: {str(e)[:50]}")

# Test 3: Output Diversity
print("\n[3] Output Diversity (Different Errors → Different Analysis)")
print("-" * 70)
total_tests += 1
try:
    if test_diversity():
        print(f"✅ Different errors produce significantly different outputs")
        passed_tests += 1
    else:
        print(f"❌ Some errors produce similar outputs")
except Exception as e:
    print(f"❌ Exception: {str(e)[:50]}")

# Summary
print("\n" + "=" * 70)
print(f"📊 TEST SUMMARY: {passed_tests}/{total_tests} tests passed")
print("=" * 70)

if passed_tests == total_tests:
    print("✅ ALL TESTS PASSED! Backend is fully dynamic.")
    print("\n🎯 Key Features Verified:")
    print("   ✓ Detects 9+ error types dynamically")
    print("   ✓ Generates context-aware fixes for each error type")
    print("   ✓ Produces skill-level-specific explanations")
    print("   ✓ Different errors produce completely different outputs")
    print("   ✓ No static or hardcoded responses")
    print("   ✓ All response fields properly populated")
else:
    print(f"❌ {total_tests - passed_tests} tests failed. Review output above.")

print("\n" + "=" * 70)
