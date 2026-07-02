"""
Fake News Detection Web Application with Groq AI
"""

import os
import logging
import traceback
from pathlib import Path

from flask import Flask, render_template, request, jsonify, session, flash
from flask_session import Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from config import (
    MODEL_PATH, VECTORIZER_PATH, 
    FAKE_DATASET_PATH, TRUE_DATASET_PATH,
    CATEGORY_KEYWORDS,
    KNOWN_TRUE_FACTS, KNOWN_FAKE_FACTS,
    APP_CONFIG
)
from models.news_classifier import create_classifier
from utils import (
    clean_text, detect_category, check_known_facts,
    get_prediction_reason, NewsAnalytics, 
    simple_rule_based_detection,
    detect_math_equation,
    detect_with_groq
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = APP_CONFIG.get('secret_key', 'dev-secret-key')

# Initialize classifier
classifier = create_classifier()

# Initialize analytics
analytics = NewsAnalytics()


def initialize_model():
    """Initialize the model - load if exists, otherwise train."""
    try:
        if MODEL_PATH.exists() and VECTORIZER_PATH.exists():
            logger.info("Loading existing model...")
            classifier.load(MODEL_PATH, VECTORIZER_PATH)
        else:
            logger.info("Model not found. Training new model...")
            metrics = classifier.train(FAKE_DATASET_PATH, TRUE_DATASET_PATH)
            classifier.save(MODEL_PATH, VECTORIZER_PATH)
            logger.info(f"Training completed with accuracy: {metrics['accuracy']:.4f}")
    except Exception as e:
        logger.error(f"Error initializing model: {e}")
        raise


def validate_input(text: str) -> tuple:
    """Validate if the input is a proper news article."""
    if not text or len(text.strip()) < 3:
        return False, "Please enter some text (minimum 3 characters).", None
    
    cleaned = clean_text(text)
    word_count = len(cleaned.split())
    
    if word_count < 1:
        return False, "Please enter more text for better analysis.", None
    
    return True, None, cleaned


# Initialize model on startup
initialize_model()


@app.route('/')
def home():
    """Home page route."""
    return render_template('index.html')


@app.route('/detector', methods=['GET', 'POST'])
def detector():
    """News detector page with Groq AI integration."""
    prediction = ""
    category = ""
    reason = ""
    confidence = 0.0
    input_text = ""
    error = None
    sources = []
    groq_used = False
    groq_response = ""

    if request.method == 'POST':
        input_text = request.form.get('news', '').strip()
        use_groq = request.form.get('use_groq', 'off') == 'on'
        
        is_valid, error_message, cleaned_text = validate_input(input_text)
        
        if not is_valid:
            error = error_message
            flash(error_message, 'warning')
            return render_template('detector.html', input_text=input_text, error=error)

        try:
            # ===== STEP 1: CHECK MATH EQUATIONS =====
            math_result = detect_math_equation(cleaned_text)
            if math_result:
                if math_result['prediction'] == 'REAL':
                    prediction = "✅ Real News"
                else:
                    prediction = "❌ Fake News"
                confidence = math_result['confidence'] * 100
                reason = math_result['reason']
                category = math_result['category']
                prediction_value = 1 if math_result['prediction'] == 'REAL' else 0
                
                analytics.record_prediction(prediction_value, category)
                
                return render_template(
                    'detector.html',
                    prediction=prediction,
                    category=category,
                    reason=reason,
                    confidence=confidence,
                    input_text=input_text,
                    error=error,
                    groq_used=False
                )
            
            # ===== STEP 2: GROQ AI WEB SEARCH (IF ENABLED) =====
            if use_groq:
                logger.info(f"Using Groq AI to verify: {cleaned_text}")
                groq_result = detect_with_groq(cleaned_text)
                
                if groq_result['success']:
                    groq_used = True
                    groq_response = groq_result['full_response']
                    sources = groq_result.get('sources', [])
                    
                    verdict = groq_result.get('verdict', 'UNCERTAIN')
                    confidence = groq_result.get('confidence', 50)
                    
                    if verdict == 'REAL':
                        prediction = f"✅ Real News (AI Verified)"
                        prediction_value = 1
                    elif verdict == 'FAKE':
                        prediction = f"❌ Fake News (AI Verified)"
                        prediction_value = 0
                    else:
                        prediction = f"⚠️ Uncertain (AI Analysis)"
                        prediction_value = 0
                    
                    reason = groq_result.get('reasoning', 'AI analysis complete. See full response below.')
                    category = detect_category(cleaned_text, CATEGORY_KEYWORDS)
                    
                    analytics.record_prediction(prediction_value, category)
                    
                    return render_template(
                        'detector.html',
                        prediction=prediction,
                        category=category,
                        reason=reason,
                        confidence=confidence,
                        input_text=input_text,
                        error=error,
                        groq_used=groq_used,
                        groq_response=groq_response,
                        sources=sources
                    )
                else:
                    flash(f'Groq API Error: {groq_result.get("error", "Unknown error")}', 'danger')
            
            # ===== STEP 3: CHECK KNOWN FACTS =====
            category = detect_category(cleaned_text, CATEGORY_KEYWORDS)
            is_true, matched_fact, match_type = check_known_facts(
                cleaned_text, 
                KNOWN_TRUE_FACTS, 
                KNOWN_FAKE_FACTS
            )
            
            if is_true is not None:
                if is_true:
                    prediction = "✅ Real News"
                    confidence = 99.0
                    reason = f"This matches a verified fact: '{matched_fact}'"
                else:
                    prediction = "❌ Fake News"
                    confidence = 99.0
                    reason = f"This matches a known false claim: '{matched_fact}'"
                prediction_value = 1 if is_true else 0
                
                analytics.record_prediction(prediction_value, category)
                
                return render_template(
                    'detector.html',
                    prediction=prediction,
                    category=category,
                    reason=reason,
                    confidence=confidence,
                    input_text=input_text,
                    error=error,
                    groq_used=False
                )
            
            # ===== STEP 4: ML MODEL =====
            try:
                prediction_value, confidence = classifier.predict(cleaned_text)
                
                if prediction_value == 1:
                    prediction = f"✅ Real News (Confidence: {confidence:.2%})"
                else:
                    prediction = f"❌ Fake News (Confidence: {confidence:.2%})"
                
                reason = get_prediction_reason(
                    prediction_value, 
                    confidence, 
                    category
                )
            except Exception as ml_error:
                # ===== STEP 5: FALLBACK =====
                logger.warning(f"ML prediction failed: {ml_error}. Using fallback.")
                
                prediction_value, confidence, fallback_reason = simple_rule_based_detection(cleaned_text)
                
                if prediction_value == 1:
                    prediction = f"✅ Real News (Confidence: {confidence:.2%})"
                else:
                    prediction = f"❌ Fake News (Confidence: {confidence:.2%})"
                
                reason = fallback_reason
            
            # Record analytics
            analytics.record_prediction(prediction_value, category)
            
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            logger.error(traceback.format_exc())
            
            # Use rule-based as last resort
            try:
                prediction_value, confidence, fallback_reason = simple_rule_based_detection(cleaned_text)
                
                if prediction_value == 1:
                    prediction = f"✅ Real News (Confidence: {confidence:.2%})"
                else:
                    prediction = f"❌ Fake News (Confidence: {confidence:.2%})"
                
                reason = fallback_reason + " (Fallback mode)"
                category = "General"
                
                analytics.record_prediction(prediction_value, category)
                
            except Exception as final_error:
                logger.error(f"Final fallback failed: {final_error}")
                flash('An error occurred during prediction. Please try again.', 'danger')
                return render_template('detector.html', input_text=input_text)

    return render_template(
        'detector.html',
        prediction=prediction,
        category=category,
        reason=reason,
        confidence=confidence,
        input_text=input_text,
        error=error,
        groq_used=groq_used,
        groq_response=groq_response,
        sources=sources
    )


@app.route('/features')
def features():
    """Features page route."""
    return render_template('features.html')


@app.route('/about')
def about():
    """About page route."""
    return render_template('about.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard page with analytics."""
    stats = analytics.get_statistics()
    return render_template('dashboard.html', stats=stats)


@app.route('/api/stats', methods=['GET'])
def api_stats():
    """API endpoint to get analytics statistics."""
    try:
        stats = analytics.get_statistics()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """404 error handler."""
    return render_template('error.html', error="Page not found"), 404


@app.errorhandler(500)
def server_error(error):
    """500 error handler."""
    logger.error(f"Server error: {error}")
    return render_template('error.html', error="Internal server error"), 500


if __name__ == "__main__":
    app.run(
        debug=APP_CONFIG.get('debug', True),
        host=APP_CONFIG.get('host', '0.0.0.0'),
        port=APP_CONFIG.get('port', 5000)
    )