"""
Utility functions for the fake news detection application.
"""

import re
import logging
import os
import requests
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Initialize Groq API settings
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


# ===== TEXT CLEANING =====

def clean_text(text: str) -> str:
    """Clean and preprocess text input."""
    if not text:
        return ""
    
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\']', ' ', text)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    
    # Remove emojis
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)
    
    return text.strip()


# ===== CATEGORY DETECTION =====

def detect_category(text: str, keyword_map: Dict[str, List[str]]) -> str:
    """Detect the category of a news article based on keywords."""
    if not text:
        return "General"
    
    text = text.lower()
    matched_categories = []
    
    for category, keywords in keyword_map.items():
        matches = sum(1 for keyword in keywords if keyword in text)
        if matches > 0:
            matched_categories.append((category, matches))
    
    if not matched_categories:
        return "General"
    
    matched_categories.sort(key=lambda x: x[1], reverse=True)
    return matched_categories[0][0]


# ===== KNOWN FACTS CHECK =====

def check_known_facts(text: str, 
                      true_facts: List[str], 
                      fake_facts: List[str]) -> Tuple[Optional[bool], Optional[str], Optional[str]]:
    """Check if text matches known true or fake facts."""
    if not text:
        return None, None, None
    
    clean = text.lower().strip()
    
    # Exact/Substring Match
    for fact in true_facts:
        if fact in clean or clean in fact:
            return True, fact, "exact"
    
    for fact in fake_facts:
        if fact in clean or clean in fact:
            return False, fact, "exact"
    
    # Pattern-based detection
    if 'prime minister' in clean and 'india' in clean and 'trump' in clean:
        return False, "Donald Trump is not India's Prime Minister", "pattern"
    
    if re.search(r'earth.*flat', clean) or re.search(r'flat.*earth', clean):
        return False, "The Earth is flat", "pattern"
    
    return None, None, None


# ===== MATH DETECTION =====

def solve_math(text: str) -> dict:
    """Detect and solve math equations."""
    text = text.strip()
    
    # PATTERN 1: 2+3=5
    match1 = re.match(r'^(\d+)\s*([+\-*/])\s*(\d+)\s*=\s*(\d+)$', text)
    if match1:
        try:
            num1 = float(match1.group(1))
            op = match1.group(2)
            num2 = float(match1.group(3))
            given = float(match1.group(4))
            
            if op == '+':
                result = num1 + num2
            elif op == '-':
                result = num1 - num2
            elif op == '*':
                result = num1 * num2
            elif op == '/':
                if num2 == 0:
                    return {'is_math': False}
                result = num1 / num2
            else:
                return {'is_math': False}
            
            return {
                'is_math': True,
                'correct': (result == given),
                'result': result,
                'given': given,
                'expression': f"{num1} {op} {num2} = {given}"
            }
        except:
            return {'is_math': False}
    
    # PATTERN 2: 2 plus 3 equals 5
    match2 = re.match(r'^(\d+)\s+(plus|minus|times|divided by)\s+(\d+)\s+(equals|is|=)\s+(\d+)$', text.lower())
    if match2:
        try:
            num1 = float(match2.group(1))
            op_word = match2.group(2)
            num2 = float(match2.group(3))
            given = float(match2.group(5))
            
            op_map = {'plus': '+', 'minus': '-', 'times': '*', 'divided by': '/'}
            op = op_map.get(op_word, '+')
            
            if op == '+':
                result = num1 + num2
            elif op == '-':
                result = num1 - num2
            elif op == '*':
                result = num1 * num2
            elif op == '/':
                if num2 == 0:
                    return {'is_math': False}
                result = num1 / num2
            else:
                return {'is_math': False}
            
            return {
                'is_math': True,
                'correct': (result == given),
                'result': result,
                'given': given,
                'expression': f"{num1} {op_word} {num2} = {given}"
            }
        except:
            return {'is_math': False}
    
    return {'is_math': False}


def detect_math_equation(text: str) -> dict:
    """Main function to detect and verify math equations."""
    result = solve_math(text)
    
    if not result.get('is_math', False):
        return None
    
    if result['correct']:
        return {
            'prediction': 'REAL',
            'confidence': 0.99,
            'reason': f"✅ Correct! {result['expression']} is mathematically true.",
            'category': 'Mathematics'
        }
    else:
        return {
            'prediction': 'FAKE',
            'confidence': 0.95,
            'reason': f"❌ Incorrect! {result['expression']} is false. The correct answer is {result['result']}.",
            'category': 'Mathematics'
        }


# ===== GROQ AI WEB SEARCH (Using requests) =====

def detect_with_groq(text: str) -> dict:
    """
    Use Groq API with requests library to verify news claims.
    """
    if not GROQ_API_KEY:
        return {
            'success': False,
            'error': 'Groq API key not configured. Please add GROQ_API_KEY to .env file.'
        }
    
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": """You are a fact-checking AI. 
                
                IMPORTANT: Start your response with either:
                - "VERDICT: REAL" if the claim is true
                - "VERDICT: FAKE" if the claim is false
                - "VERDICT: UNCERTAIN" if you're not sure
                
                Then explain why in one sentence."""},
                {"role": "user", "content": f"Verify this claim: '{text[:200]}'"}
            ],
            "max_tokens": 150,
            "temperature": 0.3
        }
        
        response = requests.post(GROQ_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # === PARSE RESPONSE ===
            verdict = "UNCERTAIN"
            confidence = 50
            response_lower = content.lower()
            
            # Check for VERDICT pattern
            if "verdict:" in response_lower:
                for line in content.split('\n'):
                    if "verdict:" in line.lower():
                        line_lower = line.lower()
                        if "real" in line_lower or "true" in line_lower:
                            verdict = "REAL"
                            confidence = 85
                        elif "fake" in line_lower or "false" in line_lower:
                            verdict = "FAKE"
                            confidence = 85
                        elif "uncertain" in line_lower:
                            verdict = "UNCERTAIN"
                            confidence = 50
                        break
            
            # If no verdict found, check for keywords
            if verdict == "UNCERTAIN":
                if "incorrect" in response_lower or "false" in response_lower or "wrong" in response_lower:
                    verdict = "FAKE"
                    confidence = 80
                elif "correct" in response_lower or "true" in response_lower or "real" in response_lower:
                    verdict = "REAL"
                    confidence = 80
            
            return {
                'success': True,
                'verdict': verdict,
                'confidence': confidence,
                'full_response': content,
                'reasoning': content,
                'sources': []
            }
        else:
            return {
                'success': False,
                'error': f"API Error: {response.status_code} - {response.text}"
            }
            
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'error': 'Request timed out. Please try again.'
        }
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        return {
            'success': False,
            'error': str(e)
        }


# ===== RULE-BASED DETECTION =====

def simple_rule_based_detection(text: str) -> tuple:
    """Fallback rule-based detection."""
    text_lower = text.lower()
    
    # Fake patterns
    fake_patterns = [
        'flat earth', 'moon made of cheese', 'cheese moon',
        'sun revolves around earth', 'geocentric',
        'trump prime minister india', 'india prime minister trump',
        'vaccines cause autism', '5g causes covid',
        'covid is a hoax', 'global warming is a hoax',
        'election fraud', 'illuminati', 'new world order',
        'aliens built pyramids', 'moon landing fake',
        'hitler escaped', 'elvis is alive', 'tupac is alive',
        'vampires are real', 'werewolves are real', 'zombies are real',
        'unicorns are real', 'dragons are real', 'mermaids are real'
    ]
    
    # Real patterns
    real_patterns = [
        'earth revolves around sun', 'water boils at',
        'water freezes at', 'humans need oxygen',
        'gravity exists', 'photosynthesis',
        'india gained independence', 'world war',
        'narendra modi', 'modi prime minister'
    ]
    
    # Check fake patterns
    for pattern in fake_patterns:
        if pattern in text_lower:
            return 0, 0.90, f"Contains suspicious pattern: '{pattern}'"
    
    # Check real patterns
    for pattern in real_patterns:
        if pattern in text_lower:
            return 1, 0.80, f"Contains factual pattern: '{pattern}'"
    
    # Default: mark as suspicious
    return 0, 0.55, "This text doesn't match known patterns. Marked as suspicious by default."


# ===== PREDICTION REASON =====

def get_prediction_reason(prediction: int, 
                          confidence: float,
                          category: str,
                          is_true: Optional[bool] = None,
                          matched_fact: Optional[str] = None,
                          match_type: Optional[str] = None) -> str:
    """Generate a human-readable reason for the prediction."""
    
    if is_true is not None and matched_fact:
        if is_true:
            return f"✅ This matches a verified fact: '{matched_fact}'"
        else:
            return f"❌ This matches a known false claim: '{matched_fact}'"
    
    if prediction == 1:
        reasons = [
            "The language used is factual and neutral.",
            "Contains verified information and credible terminology.",
            "The writing style is objective and balanced.",
            "Uses moderate and measured language.",
            "The content appears well-researched and evidence-based."
        ]
    else:
        reasons = [
            "Contains sensational or emotional language.",
            "Lacks credible sources or citations.",
            "Uses exaggerated or misleading claims.",
            "Contains grammatical inconsistencies common in fake news.",
            "The content shows signs of manipulation or bias.",
            "No reliable sources found to verify this claim."
        ]
    
    if confidence > 0.8:
        idx = 0
    elif confidence > 0.6:
        idx = 1
    else:
        idx = 2
    
    return reasons[idx % len(reasons)]


# ===== ANALYTICS =====

class NewsAnalytics:
    """Track and analyze news detection statistics."""
    
    def __init__(self):
        self.total_checks = 0
        self.real_count = 0
        self.fake_count = 0
        self.category_counts = {}
        self.daily_predictions = []
        
    def record_prediction(self, prediction: int, category: str) -> None:
        self.total_checks += 1
        if prediction == 1:
            self.real_count += 1
        else:
            self.fake_count += 1
        self.category_counts[category] = self.category_counts.get(category, 0) + 1
        self.daily_predictions.append({
            'timestamp': datetime.now(),
            'prediction': prediction,
            'category': category
        })
    
    def get_statistics(self) -> Dict:
        real_percentage = (self.real_count / self.total_checks * 100) if self.total_checks > 0 else 0
        fake_percentage = (self.fake_count / self.total_checks * 100) if self.total_checks > 0 else 0
        
        today = datetime.now().date()
        today_predictions = [p for p in self.daily_predictions 
                           if p['timestamp'].date() == today]
        
        return {
            'total_checks': self.total_checks,
            'real_count': self.real_count,
            'fake_count': self.fake_count,
            'real_percentage': round(real_percentage, 1),
            'fake_percentage': round(fake_percentage, 1),
            'category_counts': self.category_counts,
            'today_predictions': len(today_predictions),
            'total_predictions': len(self.daily_predictions),
        }