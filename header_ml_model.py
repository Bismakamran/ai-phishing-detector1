#!/usr/bin/env python3
"""
Email Header ML Model
Machine learning model for phishing detection based on email headers.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import pickle
import os
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class HeaderMLModel:
    """Machine learning model for email header analysis"""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoder = LabelEncoder()
        self.feature_names = []
        self.is_trained = False
        
    def extract_features_from_headers(self, headers: Dict) -> Dict:
        """Extract features from email headers for ML model"""
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
    
    def prepare_dataset(self, dataset_path: str) -> Tuple[pd.DataFrame, pd.Series]:
        """Prepare dataset for training"""
        try:
            # Load dataset
            df = pd.read_csv(dataset_path)
            
            # Extract features from each email
            features_list = []
            labels = []
            
            for idx, row in df.iterrows():
                try:
                    # Assuming the dataset has 'email_content' and 'label' columns
                    email_content = row['email_content']
                    label = row['label']
                    
                    # Parse headers
                    from email import message_from_string
                    email_message = message_from_string(email_content)
                    headers = dict(email_message.items())
                    
                    # Extract features
                    features = self.extract_features_from_headers(headers)
                    features_list.append(features)
                    labels.append(label)
                    
                except Exception as e:
                    logger.error(f"Error processing row {idx}: {e}")
                    continue
            
            # Convert to DataFrame
            features_df = pd.DataFrame(features_list)
            labels_series = pd.Series(labels)
            
            return features_df, labels_series
            
        except Exception as e:
            logger.error(f"Error preparing dataset: {e}")
            return pd.DataFrame(), pd.Series()
    
    def train(self, dataset_path: str) -> Dict:
        """Train the model on the dataset"""
        try:
            # Prepare dataset
            X, y = self.prepare_dataset(dataset_path)
            
            if X.empty or y.empty:
                return {"success": False, "error": "No valid data found"}
            
            # Encode labels
            y_encoded = self.label_encoder.fit_transform(y)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
            )
            
            # Store feature names
            self.feature_names = X.columns.tolist()
            
            # Train model
            self.model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Generate classification report
            class_report = classification_report(y_test, y_pred, target_names=self.label_encoder.classes_)
            
            self.is_trained = True
            
            return {
                "success": True,
                "accuracy": accuracy,
                "classification_report": class_report,
                "feature_importance": dict(zip(self.feature_names, self.model.feature_importances_))
            }
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            return {"success": False, "error": str(e)}
    
    def predict(self, headers: Dict) -> Dict:
        """Predict phishing probability for given headers"""
        if not self.is_trained:
            return {"error": "Model not trained"}
        
        try:
            # Extract features
            features = self.extract_features_from_headers(headers)
            
            # Convert to DataFrame
            features_df = pd.DataFrame([features])
            
            # Ensure all expected features are present
            for feature in self.feature_names:
                if feature not in features_df.columns:
                    features_df[feature] = 0
            
            # Reorder columns to match training data
            features_df = features_df[self.feature_names]
            
            # Make prediction
            prediction = self.model.predict(features_df)[0]
            probability = self.model.predict_proba(features_df)[0]
            
            # Decode prediction
            predicted_label = self.label_encoder.inverse_transform([prediction])[0]
            
            return {
                "prediction": predicted_label,
                "probability": dict(zip(self.label_encoder.classes_, probability)),
                "features_used": features
            }
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return {"error": str(e)}
    
    def save_model(self, filepath: str):
        """Save the trained model"""
        if not self.is_trained:
            raise ValueError("Model not trained")
        
        model_data = {
            'model': self.model,
            'label_encoder': self.label_encoder,
            'feature_names': self.feature_names,
            'is_trained': self.is_trained
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, filepath: str):
        """Load a trained model"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.label_encoder = model_data['label_encoder']
        self.feature_names = model_data['feature_names']
        self.is_trained = model_data['is_trained']

# Global instance
header_ml_model = HeaderMLModel()

