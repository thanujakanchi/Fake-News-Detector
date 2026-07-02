"""
Models package for Fake News Detection
"""
from .news_classifier import NewsClassifier, create_classifier

__all__ = ['NewsClassifier', 'create_classifier']