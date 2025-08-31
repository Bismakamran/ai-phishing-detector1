#!/usr/bin/env python3
"""
Comprehensive Email Analyzer
Combines content analysis and header analysis for comprehensive phishing detection.
"""

import requests
import json
from typing import Dict, List, Tuple
import logging
from email_header_analyzer import header_analyzer
from header_ml_model import header_ml_model

logger = logging.getLogger(__name__)

class ComprehensiveEmailAnalyzer:
    """Comprehensive email analyzer combining content and header analysis"""
    
    def __init__(self, huggingface_api_key: str, huggingface_api_url: str):
        self.huggingface_api_key = huggingface_api_key
        self.huggingface_api_url = huggingface_api_url
        
    def analyze_email_comprehensive(self, email_content: str, url: str = "") -> Dict:
        """Perform comprehensive email analysis including content and headers"""
        
        try:
            # Step 1: Header Analysis
            header_result = header_analyzer.analyze_headers(email_content)
            
            # Step 2: Content Analysis (using existing Hugging Face model)
            content_result = self._analyze_content(email_content, url)
            
            # Step 3: ML Model Analysis (if available)
            ml_result = self._analyze_with_ml_model(email_content)
            
            # Step 4: Combine results
            combined_result = self._combine_analysis_results(header_result, content_result, ml_result)
            
            return combined_result
            
        except Exception as e:
            logger.error(f"Error in comprehensive analysis: {e}")
            return {
                "result": f"❌ Error: {str(e)}",
                "confidence": 0,
                "indicators": [],
                "analysis_type": "comprehensive"
            }
    
    def _analyze_content(self, email_content: str, url: str) -> Dict:
        """Analyze email content using Hugging Face model"""
        try:
            # Prepare the text for analysis
            analysis_text = f"Email content: {email_content}\nURL: {url}"
            
            headers = {
                "Authorization": f"Bearer {self.huggingface_api_key}",
                "Content-Type": "application/json"
            }
            
            # Use BART model for zero-shot classification
            payload = {
                "inputs": analysis_text,
                "parameters": {
                    "candidate_labels": ["phishing", "legitimate", "suspicious"]
                }
            }
            
            response = requests.post(self.huggingface_api_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                # BART zero-shot classification returns format: {"labels": [...], "scores": [...]}
                if isinstance(result, dict) and 'labels' in result and 'scores' in result:
                    labels = result['labels']
                    scores = result['scores']
                    
                    # Get the highest scoring label
                    max_score_index = scores.index(max(scores))
                    label = labels[max_score_index]
                    confidence_score = scores[max_score_index]
                    
                    # Convert confidence score to percentage
                    confidence_percentage = int(confidence_score * 100)
                    
                    # Determine result based on model prediction
                    if label.lower() == 'phishing' or confidence_percentage > 70:
                        result_text = f"⚠️ HIGH RISK - Content analysis detected phishing ({confidence_percentage}% confidence)"
                    elif label.lower() == 'suspicious' or confidence_percentage > 40:
                        result_text = f"⚠️ MEDIUM RISK - Suspicious content detected ({confidence_percentage}% confidence)"
                    else:
                        result_text = f"✅ LOW RISK - Content appears safe ({confidence_percentage}% confidence)"
                    
                    return {
                        "result": result_text,
                        "confidence": confidence_percentage,
                        "indicators": [f"Content analysis: {label}"],
                        "analysis_type": "content"
                    }
                else:
                    return {
                        "result": "❌ Error: Unexpected content analysis response format",
                        "confidence": 0,
                        "indicators": [],
                        "analysis_type": "content"
                    }
            else:
                return {
                    "result": f"❌ Error: Content analysis failed (Status: {response.status_code})",
                    "confidence": 0,
                    "indicators": [],
                    "analysis_type": "content"
                }
                
        except Exception as e:
            logger.error(f"Error in content analysis: {e}")
            return {
                "result": f"❌ Error: Content analysis failed - {str(e)}",
                "confidence": 0,
                "indicators": [],
                "analysis_type": "content"
            }
    
    def _analyze_with_ml_model(self, email_content: str) -> Dict:
        """Analyze email using trained ML model"""
        try:
            if not header_ml_model.is_trained:
                return {
                    "result": "⚠️ ML model not trained - using fallback analysis",
                    "confidence": 0,
                    "indicators": ["ML model not available"],
                    "analysis_type": "ml_model"
                }
            
            # Parse headers for ML model
            from email import message_from_string
            email_message = message_from_string(email_content)
            headers = dict(email_message.items())
            
            # Make prediction
            prediction_result = header_ml_model.predict(headers)
            
            if "error" in prediction_result:
                return {
                    "result": f"❌ Error: ML model prediction failed - {prediction_result['error']}",
                    "confidence": 0,
                    "indicators": [],
                    "analysis_type": "ml_model"
                }
            
            # Extract prediction and probability
            prediction = prediction_result["prediction"]
            probabilities = prediction_result["probability"]
            
            # Calculate confidence based on highest probability
            max_prob = max(probabilities.values())
            confidence_percentage = int(max_prob * 100)
            
            # Determine result
            if prediction.lower() in ['phishing', 'malicious'] or confidence_percentage > 70:
                result_text = f"⚠️ HIGH RISK - ML model detected phishing ({confidence_percentage}% confidence)"
            elif confidence_percentage > 40:
                result_text = f"⚠️ MEDIUM RISK - ML model detected suspicious patterns ({confidence_percentage}% confidence)"
            else:
                result_text = f"✅ LOW RISK - ML model indicates legitimate email ({confidence_percentage}% confidence)"
            
            return {
                "result": result_text,
                "confidence": confidence_percentage,
                "indicators": [f"ML prediction: {prediction}"],
                "analysis_type": "ml_model"
            }
            
        except Exception as e:
            logger.error(f"Error in ML model analysis: {e}")
            return {
                "result": f"❌ Error: ML model analysis failed - {str(e)}",
                "confidence": 0,
                "indicators": [],
                "analysis_type": "ml_model"
            }
    
    def _combine_analysis_results(self, header_result: Dict, content_result: Dict, ml_result: Dict) -> Dict:
        """Combine results from different analysis methods"""
        
        # Collect all indicators
        all_indicators = []
        all_indicators.extend(header_result.get("indicators", []))
        all_indicators.extend(content_result.get("indicators", []))
        all_indicators.extend(ml_result.get("indicators", []))
        
        # Calculate weighted confidence score
        header_confidence = header_result.get("confidence", 0)
        content_confidence = content_result.get("confidence", 0)
        ml_confidence = ml_result.get("confidence", 0)
        
        # Weight the different analysis methods
        # Header analysis: 40%, Content analysis: 40%, ML model: 20%
        weighted_confidence = (
            header_confidence * 0.4 +
            content_confidence * 0.4 +
            ml_confidence * 0.2
        )
        
        # Determine overall risk level
        if weighted_confidence >= 70:
            result_text = f"⚠️ HIGH RISK - Comprehensive analysis detected phishing ({int(weighted_confidence)}% confidence)"
        elif weighted_confidence >= 40:
            result_text = f"⚠️ MEDIUM RISK - Suspicious patterns detected ({int(weighted_confidence)}% confidence)"
        else:
            result_text = f"✅ LOW RISK - Email appears legitimate ({int(weighted_confidence)}% confidence)"
        
        # Prepare detailed analysis breakdown
        analysis_breakdown = {
            "header_analysis": {
                "result": header_result.get("result", ""),
                "confidence": header_confidence,
                "security_features": header_result.get("security_features", {})
            },
            "content_analysis": {
                "result": content_result.get("result", ""),
                "confidence": content_confidence
            },
            "ml_model_analysis": {
                "result": ml_result.get("result", ""),
                "confidence": ml_confidence
            }
        }
        
        return {
            "result": result_text,
            "confidence": int(weighted_confidence),
            "indicators": all_indicators,
            "analysis_type": "comprehensive",
            "analysis_breakdown": analysis_breakdown,
            "recommendations": self._generate_recommendations(header_result, content_result, ml_result)
        }
    
    def _generate_recommendations(self, header_result: Dict, content_result: Dict, ml_result: Dict) -> List[str]:
        """Generate security recommendations based on analysis results"""
        recommendations = []
        
        # Header-based recommendations
        security_features = header_result.get("security_features", {})
        
        if not security_features.get("spf", {}).get("exists", False):
            recommendations.append("Enable SPF records for the sending domain")
        
        if not security_features.get("dkim", {}).get("exists", False):
            recommendations.append("Enable DKIM authentication for the sending domain")
        
        if not security_features.get("domain_consistency", True):
            recommendations.append("Ensure From, Return-Path, and Reply-To domains are consistent")
        
        if not security_features.get("smtp_legitimacy", True):
            recommendations.append("Verify SMTP server legitimacy for the sending domain")
        
        # Content-based recommendations
        if content_result.get("confidence", 0) > 50:
            recommendations.append("Exercise caution with email content - verify sender authenticity")
        
        # General recommendations
        recommendations.append("Always verify sender email addresses before clicking links")
        recommendations.append("Check for HTTPS in URLs and avoid suspicious domains")
        recommendations.append("Be cautious of urgent language and requests for sensitive information")
        
        return recommendations

# Global instance
comprehensive_analyzer = None

