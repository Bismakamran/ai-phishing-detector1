#!/usr/bin/env python3
"""
Email Header Analyzer
Analyzes email headers for phishing indicators and extracts security features.
"""

import re
import socket
import dns.resolver
import dns.reversename
from email import message_from_string
from email.parser import HeaderParser
from urllib.parse import urlparse
import requests
import time
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailHeaderAnalyzer:
    """Analyzes email headers for phishing indicators"""
    
    def __init__(self):
        self.suspicious_indicators = []
        self.security_features = {}
        self.confidence_score = 0
        
    def parse_email_headers(self, email_content: str) -> Dict:
        """Parse email content and extract headers"""
        try:
            # Parse the email
            email_message = message_from_string(email_content)
            
            # Extract headers
            headers = {}
            for header_name, header_value in email_message.items():
                headers[header_name.lower()] = header_value
            
            return headers
        except Exception as e:
            logger.error(f"Error parsing email headers: {e}")
            return {}
    
    def extract_from_domain(self, from_header: str) -> Optional[str]:
        """Extract domain from From header"""
        try:
            # Extract email from "Name <email@domain.com>" or "email@domain.com"
            email_match = re.search(r'<(.+?)>|([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', from_header)
            if email_match:
                email = email_match.group(1) or email_match.group(2)
                return email.split('@')[1] if '@' in email else None
        except Exception as e:
            logger.error(f"Error extracting from domain: {e}")
        return None
    
    def extract_received_servers(self, headers: Dict) -> List[Dict]:
        """Extract information from Received headers"""
        received_servers = []
        
        for header_name, header_value in headers.items():
            if header_name.lower() == 'received':
                if isinstance(header_value, list):
                    for value in header_value:
                        received_servers.append(self._parse_received_header(value))
                else:
                    received_servers.append(self._parse_received_header(header_value))
        
        return received_servers
    
    def _parse_received_header(self, received_header: str) -> Dict:
        """Parse a single Received header"""
        server_info = {
            'from_server': None,
            'from_ip': None,
            'by_server': None,
            'timestamp': None
        }
        
        try:
            # Extract "from" server and IP
            from_match = re.search(r'from\s+([^\s]+)\s+\(([^)]+)\)', received_header, re.IGNORECASE)
            if from_match:
                server_info['from_server'] = from_match.group(1)
                server_info['from_ip'] = from_match.group(2)
            
            # Extract "by" server
            by_match = re.search(r'by\s+([^\s]+)', received_header, re.IGNORECASE)
            if by_match:
                server_info['by_server'] = by_match.group(1)
            
            # Extract timestamp
            timestamp_match = re.search(r';\s+(.+)', received_header)
            if timestamp_match:
                server_info['timestamp'] = timestamp_match.group(1).strip()
                
        except Exception as e:
            logger.error(f"Error parsing received header: {e}")
        
        return server_info
    
    def check_domain_ip_consistency(self, domain: str, expected_ip: str) -> bool:
        """Check if domain resolves to the expected IP"""
        try:
            # Resolve domain to IP
            answers = dns.resolver.resolve(domain, 'A')
            domain_ips = [str(answer) for answer in answers]
            
            # Check if expected IP is in the resolved IPs
            return expected_ip in domain_ips
        except Exception as e:
            logger.error(f"Error checking domain-IP consistency: {e}")
            return False
    
    def check_spf_record(self, domain: str) -> Dict:
        """Check SPF record for domain"""
        try:
            answers = dns.resolver.resolve(domain, 'TXT')
            for answer in answers:
                txt_record = str(answer)
                if txt_record.startswith('"v=spf1'):
                    return {
                        'exists': True,
                        'record': txt_record,
                        'valid': '~all' in txt_record or '-all' in txt_record
                    }
        except Exception as e:
            logger.error(f"Error checking SPF record: {e}")
        
        return {'exists': False, 'record': None, 'valid': False}
    
    def check_dkim_record(self, domain: str, selector: str = 'default') -> Dict:
        """Check DKIM record for domain"""
        try:
            dkim_domain = f"{selector}._domainkey.{domain}"
            answers = dns.resolver.resolve(dkim_domain, 'TXT')
            for answer in answers:
                txt_record = str(answer)
                if 'v=DKIM1' in txt_record:
                    return {
                        'exists': True,
                        'record': txt_record,
                        'valid': True
                    }
        except Exception as e:
            logger.error(f"Error checking DKIM record: {e}")
        
        return {'exists': False, 'record': None, 'valid': False}
    
    def analyze_headers(self, email_content: str) -> Dict:
        """Main method to analyze email headers"""
        self.suspicious_indicators = []
        self.security_features = {}
        self.confidence_score = 0
        
        # Parse headers
        headers = self.parse_email_headers(email_content)
        if not headers:
            return self._get_analysis_result("Error parsing email headers")
        
        # Extract key headers
        from_header = headers.get('from', '')
        return_path = headers.get('return-path', '')
        reply_to = headers.get('reply-to', '')
        message_id = headers.get('message-id', '')
        
        # Extract domains
        from_domain = self.extract_from_domain(from_header)
        return_path_domain = self.extract_from_domain(return_path) if return_path else None
        reply_to_domain = self.extract_from_domain(reply_to) if reply_to else None
        
        # Analyze received headers
        received_servers = self.extract_received_servers(headers)
        
        # Security checks
        self._check_domain_consistency(from_domain, return_path_domain, reply_to_domain)
        self._check_smtp_server_legitimacy(from_domain, received_servers)
        self._check_security_records(from_domain)
        self._check_suspicious_patterns(headers)
        
        # Calculate confidence score
        self._calculate_confidence_score()
        
        return self._get_analysis_result()
    
    def _check_domain_consistency(self, from_domain: str, return_path_domain: str, reply_to_domain: str):
        """Check if From, Return-Path, and Reply-To domains are consistent"""
        domains = [d for d in [from_domain, return_path_domain, reply_to_domain] if d]
        
        if len(set(domains)) > 1:
            self.suspicious_indicators.append("Domain mismatch between From, Return-Path, and Reply-To headers")
            self.confidence_score += 25
        
        self.security_features['domain_consistency'] = len(set(domains)) == 1
    
    def _check_smtp_server_legitimacy(self, from_domain: str, received_servers: List[Dict]):
        """Check if SMTP server is legitimate for the sending domain"""
        if not from_domain or not received_servers:
            return
        
        # Get the first received server (closest to sender)
        first_server = received_servers[0]
        from_ip = first_server.get('from_ip')
        
        if from_ip and from_domain:
            # Check if the IP is consistent with the domain
            is_consistent = self.check_domain_ip_consistency(from_domain, from_ip)
            
            if not is_consistent:
                self.suspicious_indicators.append(f"SMTP server IP ({from_ip}) not consistent with domain ({from_domain})")
                self.confidence_score += 30
            
            self.security_features['smtp_legitimacy'] = is_consistent
    
    def _check_security_records(self, domain: str):
        """Check SPF and DKIM records"""
        if not domain:
            return
        
        # Check SPF
        spf_result = self.check_spf_record(domain)
        if not spf_result['exists']:
            self.suspicious_indicators.append(f"No SPF record found for domain: {domain}")
            self.confidence_score += 15
        elif not spf_result['valid']:
            self.suspicious_indicators.append(f"Weak SPF record for domain: {domain}")
            self.confidence_score += 10
        
        # Check DKIM
        dkim_result = self.check_dkim_record(domain)
        if not dkim_result['exists']:
            self.suspicious_indicators.append(f"No DKIM record found for domain: {domain}")
            self.confidence_score += 15
        
        self.security_features['spf'] = spf_result
        self.security_features['dkim'] = dkim_result
    
    def _check_suspicious_patterns(self, headers: Dict):
        """Check for suspicious patterns in headers"""
        # Check for suspicious subject patterns
        subject = headers.get('subject', '').lower()
        suspicious_subject_keywords = ['urgent', 'account suspended', 'verify now', 'security alert', 'immediate action']
        if any(keyword in subject for keyword in suspicious_subject_keywords):
            self.suspicious_indicators.append("Suspicious subject line with urgent language")
            self.confidence_score += 10
        
        # Check for missing or suspicious Message-ID
        message_id = headers.get('message-id', '')
        if not message_id:
            self.suspicious_indicators.append("Missing Message-ID header")
            self.confidence_score += 10
        elif not re.match(r'<[^>]+@[^>]+>', message_id):
            self.suspicious_indicators.append("Invalid Message-ID format")
            self.confidence_score += 10
        
        # Check for suspicious X-headers
        for header_name, header_value in headers.items():
            if header_name.startswith('x-') and 'spam' in header_value.lower():
                self.suspicious_indicators.append(f"Suspicious X-header: {header_name}")
                self.confidence_score += 5
    
    def _calculate_confidence_score(self):
        """Calculate final confidence score"""
        # Cap the score at 100
        self.confidence_score = min(self.confidence_score, 100)
    
    def _get_analysis_result(self, error_message: str = None) -> Dict:
        """Get the final analysis result"""
        if error_message:
            return {
                "result": f"❌ Error: {error_message}",
                "confidence": 0,
                "indicators": [],
                "security_features": {},
                "analysis_type": "header"
            }
        
        # Determine risk level
        if self.confidence_score >= 70:
            result_text = f"⚠️ HIGH RISK - Header analysis detected phishing indicators ({self.confidence_score}% confidence)"
        elif self.confidence_score >= 40:
            result_text = f"⚠️ MEDIUM RISK - Suspicious header patterns detected ({self.confidence_score}% confidence)"
        else:
            result_text = f"✅ LOW RISK - Headers appear legitimate ({self.confidence_score}% confidence)"
        
        return {
            "result": result_text,
            "confidence": self.confidence_score,
            "indicators": self.suspicious_indicators,
            "security_features": self.security_features,
            "analysis_type": "header"
        }

# Global instance
header_analyzer = EmailHeaderAnalyzer()

