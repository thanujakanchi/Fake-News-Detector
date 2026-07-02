# test_math.py
from utils import solve_math, detect_math_equation

test_cases = [
    "2+3=5",
    "2+3=6",
    "10-5=5",
    "10-5=4",
    "5*4=20",
    "5*4=21",
    "20/4=5",
    "20/4=6",
    "2 plus 3 equals 5",
    "2 plus 3 equals 6",
    "What is 2+3? Answer: 5",
    "What is 2+3? Answer: 6",
]

print("=" * 60)
print("MATH DETECTION TEST")
print("=" * 60)

for test in test_cases:
    result = detect_math_equation(test)
    if result:
        print(f"\n✅ Input: {test}")
        print(f"   Prediction: {result['prediction']}")
        print(f"   Confidence: {result['confidence']*100:.0f}%")
        print(f"   Reason: {result['reason']}")
    else:
        print(f"\n❌ Input: {test} - NOT DETECTED AS MATH")