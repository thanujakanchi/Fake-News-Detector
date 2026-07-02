"""
Machine Learning model for news classification.
Handles training, prediction, and model management.
"""

import pickle
import logging
from pathlib import Path
from typing import Dict, Tuple, Optional, Any

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsClassifier:
    """
    A classifier for detecting fake news using TF-IDF and Passive Aggressive algorithm.
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the news classifier with configuration parameters.
        
        Args:
            config: Configuration dictionary for model parameters.
        """
        self.config = config or {}
        self.vectorizer = None
        self.model = None
        self.is_trained = False
        
    def load_data(self, fake_path: Path, true_path: Path) -> pd.DataFrame:
        """
        Load and preprocess the training datasets.
        
        Args:
            fake_path: Path to the fake news dataset.
            true_path: Path to the true news dataset.
            
        Returns:
            DataFrame with combined and preprocessed data.
        """
        try:
            fake_df = pd.read_csv(fake_path)
            true_df = pd.read_csv(true_path)
            
            logger.info(f"Loaded fake news: {len(fake_df)} samples")
            logger.info(f"Loaded true news: {len(true_df)} samples")
            
            # Add labels
            fake_df['label'] = 0  # Fake
            true_df['label'] = 1   # True
            
            # Combine datasets
            data = pd.concat([fake_df, true_df], axis=0, ignore_index=True)
            
            # Remove empty values
            data = data.dropna()
            
            # Combine title and text for better context
            data['content'] = data['title'].fillna('') + " " + data['text'].fillna('')
            
            # Remove duplicates
            data = data.drop_duplicates(subset=['content'])
            
            # Shuffle
            data = data.sample(frac=1, random_state=42).reset_index(drop=True)
            
            logger.info(f"Total samples after preprocessing: {len(data)}")
            return data
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def train(self, fake_path: Path, true_path: Path) -> Dict[str, Any]:
        """
        Train the news classifier model.
        
        Args:
            fake_path: Path to fake news dataset.
            true_path: Path to true news dataset.
            
        Returns:
            Dictionary containing training metrics.
        """
        # Load data
        data = self.load_data(fake_path, true_path)
        
        # Features and labels
        X = data['content']
        y = data['label']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=self.config.get('test_size', 0.25),
            random_state=self.config.get('random_state', 42)
        )
        
        # Initialize vectorizer
        vectorizer_params = self.config.get('vectorizer_params', {})
        self.vectorizer = TfidfVectorizer(**vectorizer_params)
        
        # Transform training data
        X_train_vectorized = self.vectorizer.fit_transform(X_train)
        X_test_vectorized = self.vectorizer.transform(X_test)
        
        # Initialize and train model
        model_params = self.config.get('model_params', {})
        self.model = PassiveAggressiveClassifier(**model_params)
        
        logger.info("Training model...")
        self.model.fit(X_train_vectorized, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_vectorized)
        accuracy = accuracy_score(y_test, y_pred)
        
        metrics = {
            'accuracy': accuracy,
            'classification_report': classification_report(y_test, y_pred),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'train_size': len(X_train),
            'test_size': len(X_test),
        }
        
        logger.info(f"Model training complete. Accuracy: {accuracy:.4f}")
        self.is_trained = True
        
        return metrics
    
    def predict(self, text: str) -> Tuple[int, float]:
        """
        Predict whether a given text is real (1) or fake (0).
        
        Args:
            text: Input text to classify.
            
        Returns:
            Tuple of (prediction, confidence_score)
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        
        if not text or not text.strip():
            return 0, 0.0
            
        # Transform text
        text_vectorized = self.vectorizer.transform([text])
        
        # Predict
        prediction = self.model.predict(text_vectorized)[0]
        
        # Get confidence (using decision function)
        try:
            confidence = abs(self.model.decision_function(text_vectorized)[0])
            # Normalize confidence to 0-1 range
            confidence = min(1.0, confidence / 5.0)
        except:
            confidence = 0.8
        
        return prediction, confidence
    
    def save(self, model_path: Path, vectorizer_path: Path) -> None:
        """
        Save the trained model and vectorizer to disk.
        
        Args:
            model_path: Path to save the model.
            vectorizer_path: Path to save the vectorizer.
        """
        if not self.is_trained:
            raise ValueError("Model not trained. Call train() first.")
        
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
            
        logger.info(f"Model saved to {model_path}")
        logger.info(f"Vectorizer saved to {vectorizer_path}")
    
    def load(self, model_path: Path, vectorizer_path: Path) -> None:
        """
        Load a trained model and vectorizer from disk.
        
        Args:
            model_path: Path to the saved model.
            vectorizer_path: Path to the saved vectorizer.
        """
        with open(model_path, 'rb') as f:
            self.model = pickle.load(f)
        
        with open(vectorizer_path, 'rb') as f:
            self.vectorizer = pickle.load(f)
            
        self.is_trained = True
        logger.info(f"Model loaded from {model_path}")
        logger.info(f"Vectorizer loaded from {vectorizer_path}")


def create_classifier() -> NewsClassifier:
    """
    Factory function to create a NewsClassifier with default configuration.
    
    Returns:
        Configured NewsClassifier instance.
    """
    from config import TFIDF_PARAMS, CLASSIFIER_PARAMS, TEST_SIZE, RANDOM_STATE
    
    config = {
        'vectorizer_params': TFIDF_PARAMS,
        'model_params': CLASSIFIER_PARAMS,
        'test_size': TEST_SIZE,
        'random_state': RANDOM_STATE,
    }
    
    return NewsClassifier(config)