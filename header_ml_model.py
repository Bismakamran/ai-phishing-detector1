#!/usr/bin/env python3
"""
Email Header ML Model - Lightweight Version
API-based phishing detection without local model files.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class HeaderMLModel:
    """Lightweight header analysis without local ML models"""
    
    def __init__(self):
        self.feature_names = []
        self.is_trained = False
        
    def extract_features_from_headers(self, headers: Dict) -> Dict:
        """Extract features from email headers for analysis"""
        features = {}
        
        # Basic header features
        features['has_from'] = 1 if headers.get('from') else 0
        features['has_return_path'] = 1 if headers.get('return-path') else 0
        features['has_reply_to'] = 1 if headers.get('reply-to') else 0
        features['has_message_id'] = 1 if headers.get('message-id') else 0
        features['has_date'] = 1 if headers.get('date') else 0
        
        # Count features
        features['num_received_headers'] = len([h for h in headers.keys() if h.lower() == 'received'])
        features['num_x_headers'] = len([h for h in headers.keys() if h.lower().startswith('x-')])
        
        # Domain consistency features
        from_domain = self._extract_domain(headers.get('from', ''))
        return_path_domain = self._extract_domain(headers.get('return-path', ''))
        reply_to_domain = self._extract_domain(headers.get('reply-to', ''))
        
        features['domains_match'] = 1 if len(set([d for d in [from_domain, return_path_domain, reply_to_domain] if d])) == 1 else 0
        features['num_unique_domains'] = len(set([d for d in [from_domain, return_path_domain, reply_to_domain] if d]))
        
        # Subject line features
        subject = headers.get('subject', '').lower()
        features['subject_length'] = len(subject)
        features['subject_has_urgent_words'] = 1 if any(word in subject for word in ['urgent', 'immediate', 'suspended', 'verify']) else 0
        features['subject_has_special_chars'] = 1 if any(char in subject for char in ['!', '?', '$', '%']) else 0
        
        # Message-ID features
        message_id = headers.get('message-id', '')
        features['message_id_valid_format'] = 1 if message_id and '<' in message_id and '>' in message_id else 0
        
        # Received header features
        received_headers = [h for h in headers.keys() if h.lower() == 'received']
        features['avg_received_header_length'] = np.mean([len(str(headers[h])) for h in received_headers]) if received_headers else 0
        
        # Security header features
        features['has_spf_header'] = 1 if any('spf' in h.lower() for h in headers.keys()) else 0
        features['has_dkim_header'] = 1 if any('dkim' in h.lower() for h in headers.keys()) else 0
        features['has_dmarc_header'] = 1 if any('dmarc' in h.lower() for h in headers.keys()) else 0
        
        return features
    
    def _extract_domain(self, header_value: str) -> str:
        """Extract domain from header value"""
        try:
            import re
            email_match = re.search(r'<(.+?)>|([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', header_value)
            if email_match:
                email = email_match.group(1) or email_match.group(2)
                return email.split('@')[1] if '@' in email else ''
        except:
            pass
        return ''
    
    def analyze_headers_lightweight(self, headers: Dict) -> Dict:
        """Analyze headers using rule-based approach instead of ML model"""
        try:
            features = self.extract_features_from_headers(headers)
            
            # Rule-based scoring system
            risk_score = 0
            indicators = []
            
            # High risk indicators
            if features['num_unique_domains'] > 2:
                risk_score += 30
                indicators.append("Multiple sender domains detected")
            
            if features['subject_has_urgent_words']:
                risk_score += 25
                indicators.append("Urgent language in subject")
            
            if features['subject_has_special_chars']:
                risk_score += 15
                indicators.append("Suspicious characters in subject")
            
            if not features['has_spf_header'] and not features['has_dkim_header']:
                risk_score += 20
                indicators.append("Missing security headers (SPF/DKIM)")
            
            if features['num_x_headers'] > 3:
                risk_score += 10
                indicators.append("Multiple custom headers")
            
            # Determine risk level
            if risk_score >= 60:
                risk_level = "HIGH"
                result = "⚠️ HIGH RISK - Multiple suspicious indicators detected"
            elif risk_score >= 30:
                risk_level = "MEDIUM"
                result = "⚠️ MEDIUM RISK - Some suspicious indicators detected"
            else:
                risk_level = "LOW"
                result = "✅ LOW RISK - Headers appear legitimate"
            
            return {
                "result": result,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "indicators": indicators,
                "features": features,
                "analysis_type": "header_lightweight"
            }
            
        except Exception as e:
            logger.error(f"Error in lightweight header analysis: {e}")
            return {
                "result": f"❌ Error: {str(e)}",
                "risk_score": 0,
                "risk_level": "ERROR",
                "indicators": [],
                "analysis_type": "header_lightweight"
            }
    
    def save_model(self, filepath: str):
        """Placeholder - no local model saving in lightweight version"""
        logger.info("Lightweight version - no local model saving")
        pass
    
    def load_model(self, filepath: str):
        """Placeholder - no local model loading in lightweight version"""
        logger.info("Lightweight version - no local model loading")
        pass

# Global instance
header_ml_model = HeaderMLModel()
