"""
Script to train and save the fake news detection model.
Can be run independently for model training.
"""

import sys
import logging
from pathlib import Path

from config import FAKE_DATASET_PATH, TRUE_DATASET_PATH, MODEL_PATH, VECTORIZER_PATH
from models.news_classifier import create_classifier

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def train_model():
    """Train and save the model."""
    try:
        # Create classifier with default config
        classifier = create_classifier()
        
        # Train the model
        logger.info("Starting model training...")
        metrics = classifier.train(FAKE_DATASET_PATH, TRUE_DATASET_PATH)
        
        # Save the model
        logger.info("Saving model...")
        classifier.save(MODEL_PATH, VECTORIZER_PATH)
        
        # Print results
        logger.info("\n" + "="*50)
        logger.info("TRAINING COMPLETE")
        logger.info("="*50)
        logger.info(f"Accuracy: {metrics['accuracy']:.4f}")
        logger.info(f"Training samples: {metrics['train_size']}")
        logger.info(f"Testing samples: {metrics['test_size']}")
        logger.info("\nClassification Report:")
        logger.info(metrics['classification_report'])
        logger.info("\nConfusion Matrix:")
        logger.info(metrics['confusion_matrix'])
        logger.info(f"\nModel saved to: {MODEL_PATH}")
        logger.info(f"Vectorizer saved to: {VECTORIZER_PATH}")
        
    except Exception as e:
        logger.error(f"Error during training: {e}")
        sys.exit(1)


if __name__ == "__main__":
    train_model()