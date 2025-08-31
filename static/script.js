// Global variables
let usernameForMFA = '';
let currentUsername = '';

// Password validation function
function validatePassword(password) {
    const requirements = {
        length: password.length >= 8,
        uppercase: /[A-Z]/.test(password),
        lowercase: /[a-z]/.test(password),
        number: /\d/.test(password),
        special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
    };
    
    return requirements;
}

// Update password requirements UI
function updatePasswordRequirements(password) {
    const requirements = validatePassword(password);
    const requirementElements = document.querySelectorAll('.requirement');
    
    requirementElements.forEach(element => {
        const requirement = element.dataset.requirement;
        const icon = element.querySelector('.requirement-icon');
        
        if (requirements[requirement]) {
            element.classList.add('met');
            icon.textContent = '✅';
        } else {
            element.classList.remove('met');
            icon.textContent = '⚪';
        }
    });
    
    return Object.values(requirements).every(Boolean);
}

// Show loading state
function showLoading(button) {
    const btnText = button.querySelector('.btn-text');
    const btnLoading = button.querySelector('.btn-loading');
    
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline';
    button.disabled = true;
}

// Hide loading state
function hideLoading(button) {
    const btnText = button.querySelector('.btn-text');
    const btnLoading = button.querySelector('.btn-loading');
    
    btnText.style.display = 'inline';
    btnLoading.style.display = 'none';
    button.disabled = false;
}

// Show message
function showMessage(element, message, type = 'error') {
    element.textContent = message;
    element.className = `message ${type}`;
    element.style.display = 'block';
}

// Clear message
function clearMessage(element) {
    element.textContent = '';
    element.style.display = 'none';
}

// ---------- INDEX PAGE ----------
document.addEventListener('DOMContentLoaded', function() {
    const scanBtn = document.getElementById("start-scan-btn");
    const demoBtn = document.getElementById("demo-btn");
    
    if (scanBtn) {
        scanBtn.addEventListener("click", () => {
            // Check if user is logged in
            const isLoggedIn = sessionStorage.getItem('isLoggedIn');
            
            if (isLoggedIn === 'true') {
                window.location.href = "/detector.html";
            } else {
                window.location.href = "/login.html";
            }
        });
    }
    
    if (demoBtn) {
        demoBtn.addEventListener("click", () => {
            // Show demo modal or redirect to demo page
            showDemoModal();
        });
    }
});

function showDemoModal() {
    // Create demo modal
    const modal = document.createElement('div');
    modal.className = 'demo-modal';
    modal.innerHTML = `
        <div class="demo-modal-content">
            <div class="demo-modal-header">
                <h3>🎯 Try MailGuard Demo</h3>
                <button class="close-btn" onclick="this.parentElement.parentElement.parentElement.remove()">×</button>
            </div>
            <div class="demo-modal-body">
                <p>Experience MailGuard's phishing detection capabilities with our interactive demo.</p>
                <div class="demo-options">
                    <button class="demo-option" onclick="runDemo('phishing')">
                        <span class="demo-icon">⚠️</span>
                        <span>Phishing Email</span>
                    </button>
                    <button class="demo-option" onclick="runDemo('safe')">
                        <span class="demo-icon">✅</span>
                        <span>Safe Email</span>
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Add CSS for modal
    const style = document.createElement('style');
    style.textContent = `
        .demo-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            backdrop-filter: blur(10px);
        }
        .demo-modal-content {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 2rem;
            max-width: 500px;
            width: 90%;
            backdrop-filter: blur(10px);
        }
        .demo-modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        .demo-modal-header h3 {
            margin: 0;
            font-size: 1.5rem;
        }
        .close-btn {
            background: none;
            border: none;
            color: #a0a0a0;
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            transition: all 0.3s ease;
        }
        .close-btn:hover {
            background: rgba(255, 255, 255, 0.1);
            color: white;
        }
        .demo-options {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-top: 1.5rem;
        }
        .demo-option {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.5rem;
            padding: 1.5rem;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .demo-option:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-2px);
        }
        .demo-icon {
            font-size: 2rem;
        }
    `;
    document.head.appendChild(style);
}

function runDemo(type) {
    // Remove modal
    document.querySelector('.demo-modal').remove();
    
    // Show demo results
    const demoResults = {
        phishing: {
            email: "Subject: Your account has been suspended\nFrom: security@bank-verify.com\n\nDear Customer,\n\nYour account has been suspended due to suspicious activity. Click here immediately to verify your identity: http://bank-verify.com/login\n\nThis is urgent - your account will be permanently closed in 24 hours.",
            url: "http://bank-verify.com/login",
            confidence: 85,
            result: "⚠️ HIGH RISK - Phishing detected (85% confidence)",
            indicators: ["Contains urgent language", "Requests sensitive information", "Uses HTTP instead of HTTPS", "Suspicious URL structure"]
        },
        safe: {
            email: "Subject: Your order confirmation\nFrom: orders@amazon.com\n\nDear Customer,\n\nThank you for your recent order #12345. Your package has been shipped and will arrive on Tuesday.\n\nTrack your package: https://amazon.com/track/12345\n\nBest regards,\nAmazon Customer Service",
            url: "https://amazon.com/track/12345",
            confidence: 15,
            result: "✅ LOW RISK - Email appears safe (15% confidence)",
            indicators: []
        }
    };
    
    const data = demoResults[type];
    
    // Show demo results modal
    const modal = document.createElement('div');
    modal.className = 'demo-modal';
    modal.innerHTML = `
        <div class="demo-modal-content">
            <div class="demo-modal-header">
                <h3>🎯 Demo Results</h3>
                <button class="close-btn" onclick="this.parentElement.parentElement.parentElement.remove()">×</button>
            </div>
            <div class="demo-modal-body">
                <div class="demo-result">
                    <div class="result-status ${data.confidence > 50 ? 'danger' : 'safe'}">${data.result}</div>
                    <div class="confidence-meter">
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: ${data.confidence}%; background: ${data.confidence > 50 ? 'linear-gradient(45deg, #ff6b6b, #ee5a52)' : 'linear-gradient(45deg, #4caf50, #45a049)'};"></div>
                        </div>
                        <div class="confidence-text">${data.confidence}% confidence</div>
                    </div>
                    ${data.indicators.length > 0 ? `
                        <div class="indicators-section">
                            <h4>Suspicious Indicators:</h4>
                            <div class="indicators-list">
                                ${data.indicators.map(indicator => `<div class="indicator"><span class="indicator-icon">⚠️</span><span>${indicator}</span></div>`).join('')}
                            </div>
                        </div>
                    ` : '<p style="color: #4caf50; text-align: center;">✅ No suspicious indicators found</p>'}
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
}

// ---------- SIGNUP PAGE ----------
document.addEventListener('DOMContentLoaded', function() {
    const signupBtn = document.getElementById("signupBtn");
    const passwordInput = document.getElementById("newPassword");
    const messageElement = document.getElementById("signupMessage");
    
    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            updatePasswordRequirements(this.value);
        });
    }
    
    if (signupBtn) {
        signupBtn.addEventListener("click", async () => {
            const username = document.getElementById("newUsername").value.trim();
            const password = document.getElementById("newPassword").value.trim();
            const email = document.getElementById("email").value.trim();
            
            // Clear previous messages
            clearMessage(messageElement);
            
            // Validation
            if (!username || !password || !email) {
                showMessage(messageElement, "All fields are required", "error");
                return;
            }
            
            if (username.length < 4) {
                showMessage(messageElement, "Username must be at least 4 characters", "error");
                return;
            }
            
            if (!email.includes('@')) {
                showMessage(messageElement, "Please enter a valid email address", "error");
                return;
            }
            
            const isPasswordValid = updatePasswordRequirements(password);
            if (!isPasswordValid) {
                showMessage(messageElement, "Please meet all password requirements", "error");
                return;
            }
            
            // Show loading
            showLoading(signupBtn);
            
            try {
                const response = await fetch('/api/signup', {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password, email })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // Show success message and redirect to MFA setup
                    const signupForm = document.getElementById("signup-form");
                    const mfaSetup = document.getElementById("mfa-setup");
                    
                    signupForm.style.display = 'none';
                    mfaSetup.style.display = 'block';
                } else {
                    showMessage(messageElement, data.message, "error");
                }
            } catch (error) {
                showMessage(messageElement, "Network error. Please try again.", "error");
            } finally {
                hideLoading(signupBtn);
            }
        });
    }
});

// ---------- LOGIN PAGE ----------
document.addEventListener('DOMContentLoaded', function() {
    const loginBtn = document.getElementById("loginBtn");
    const mfaBtn = document.getElementById("mfaBtn");
    const loginForm = document.getElementById("login-form");
    const mfaForm = document.getElementById("mfa-form");
    const resendOtpBtn = document.getElementById("resend-otp");
    
    if (loginBtn) {
        loginBtn.addEventListener("click", async () => {
            const username = document.getElementById("username").value.trim();
            const password = document.getElementById("password").value.trim();
            const errorElement = document.getElementById("loginError");
            
            // Clear previous messages
            clearMessage(errorElement);
            
            // Validation
            if (!username || !password) {
                showMessage(errorElement, "Username and password are required", "error");
                return;
            }
            
            usernameForMFA = username;
            showLoading(loginBtn);
            
            try {
                const response = await fetch('/api/login', {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username, password })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    if (data.mfa_required) {
                        // Show MFA form
                        loginForm.style.display = 'none';
                        mfaForm.style.display = 'block';
                        showMessage(errorElement, "OTP sent to your email", "success");
                    } else {
                        // Login successful
                        sessionStorage.setItem('isLoggedIn', 'true');
                        sessionStorage.setItem('username', username);
                        window.location.href = "/detector.html";
                    }
                } else {
                    showMessage(errorElement, data.message, "error");
                }
            } catch (error) {
                showMessage(errorElement, "Network error. Please try again.", "error");
            } finally {
                hideLoading(loginBtn);
            }
        });
    }
    
    if (mfaBtn) {
        mfaBtn.addEventListener("click", async () => {
            const mfaCode = document.getElementById("mfaCode").value.trim();
            const mfaError = document.getElementById("mfaError");
            
            // Clear previous messages
            clearMessage(mfaError);
            
            // Validation
            if (!mfaCode) {
                showMessage(mfaError, "Please enter the verification code", "error");
                return;
            }
            
            if (mfaCode.length !== 6) {
                showMessage(mfaError, "Please enter a 6-digit code", "error");
                return;
            }
            
            showLoading(mfaBtn);
            
            try {
                const response = await fetch('/api/verify_mfa', {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username: usernameForMFA, mfa_code: mfaCode })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // MFA verification successful
                    sessionStorage.setItem('isLoggedIn', 'true');
                    sessionStorage.setItem('username', usernameForMFA);
                    window.location.href = "/detector.html";
                } else {
                    showMessage(mfaError, data.message, "error");
                }
            } catch (error) {
                showMessage(mfaError, "Network error. Please try again.", "error");
            } finally {
                hideLoading(mfaBtn);
            }
        });
    }
    
    if (resendOtpBtn) {
        resendOtpBtn.addEventListener("click", async (e) => {
            e.preventDefault();
            
            if (!usernameForMFA) {
                return;
            }
            
            try {
                const response = await fetch('/api/resend_otp', {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ username: usernameForMFA })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    showMessage(document.getElementById("mfaError"), "New OTP sent to your email", "success");
                } else {
                    showMessage(document.getElementById("mfaError"), data.message, "error");
                }
            } catch (error) {
                showMessage(document.getElementById("mfaError"), "Failed to resend OTP", "error");
            }
        });
    }
});

// ---------- DETECTOR PAGE ----------
document.addEventListener('DOMContentLoaded', function() {
    // Only run this block on the detector page to avoid redirect loops on other pages
    if (window.location.pathname !== '/detector.html') {
        return;
    }

    // Check if user is logged in
    const isLoggedIn = sessionStorage.getItem('isLoggedIn');
    if (!isLoggedIn || isLoggedIn !== 'true') {
        window.location.href = "/login.html";
        return;
    }
    
    currentUsername = sessionStorage.getItem('username');
    
    const checkBtn = document.getElementById("checkBtn");
    const emailInput = document.getElementById("emailInput");
    const urlInput = document.getElementById("urlInput");
    const resultCard = document.getElementById("result");
    
    // Analyze button
    if (checkBtn) {
        checkBtn.addEventListener("click", async () => {
            const emailText = emailInput.value.trim();
            const url = urlInput.value.trim();
            
            if (!emailText) {
                alert("Please enter email content to analyze");
                return;
            }
            
            showLoading(checkBtn);
            
            try {
                const response = await fetch('/api/detect', {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ emailText, url })
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    displayResults(data);
                } else {
                    alert("Analysis failed: " + data.message);
                }
            } catch (error) {
                alert("Network error. Please try again.");
            } finally {
                hideLoading(checkBtn);
            }
        });
    }
    
    // Load analysis history and user info
    loadAnalysisHistory();
    loadUserInfo();
    
    // Initialize scroll effects for history section
    initializeScrollEffects();
});



// Display analysis results
function displayResults(data) {
    const resultCard = document.getElementById("result");
    const resultStatus = document.getElementById("resultStatus");
    const confidenceFill = document.getElementById("confidenceFill");
    const confidenceText = document.getElementById("confidenceText");
    const indicatorsList = document.getElementById("indicatorsList");
    const recommendationsList = document.getElementById("recommendationsList");
    
    // Show result card
    resultCard.style.display = 'block';
    
    // Set status
    let statusClass = 'safe';
    if (data.result.includes('HIGH RISK')) {
        statusClass = 'danger';
    } else if (data.result.includes('MEDIUM RISK')) {
        statusClass = 'warning';
    }
    
    resultStatus.textContent = data.result;
    resultStatus.className = `result-status ${statusClass}`;
    
    // Set confidence meter
    const confidence = data.confidence || 0;
    confidenceFill.style.width = `${confidence}%`;
    confidenceText.textContent = `${confidence}% confidence`;
    
    // Display indicators
    indicatorsList.innerHTML = '';
    if (data.indicators && data.indicators.length > 0) {
        data.indicators.forEach(indicator => {
            const indicatorElement = document.createElement('div');
            indicatorElement.className = 'indicator';
            indicatorElement.innerHTML = `
                <span class="indicator-icon">⚠️</span>
                <span>${indicator}</span>
            `;
            indicatorsList.appendChild(indicatorElement);
        });
    } else {
        indicatorsList.innerHTML = '<p style="color: #a0a0a0;">No suspicious indicators found</p>';
    }
    
    // Display comprehensive analysis breakdown if available
    if (data.analysis_breakdown) {
        displayAnalysisBreakdown(data.analysis_breakdown);
    }
    
    // Display recommendations (use comprehensive recommendations if available)
    recommendationsList.innerHTML = '';
    const recommendations = data.recommendations || getRecommendations(data.confidence, data.indicators);
    recommendations.forEach(recommendation => {
        const recommendationElement = document.createElement('div');
        recommendationElement.className = 'recommendation';
        recommendationElement.innerHTML = `
            <span class="recommendation-icon">💡</span>
            <span>${recommendation}</span>
        `;
        recommendationsList.appendChild(recommendationElement);
    });
    
    // Add to history and refresh display
    addToHistory(data);
    // Refresh the history display from database
    setTimeout(() => loadAnalysisHistory(), 500);
}

// Display analysis breakdown for comprehensive analysis
function displayAnalysisBreakdown(breakdown) {
    const indicatorsList = document.getElementById("indicatorsList");
    
    // Add analysis type indicators
    const analysisTypes = [];
    
    if (breakdown.header_analysis) {
        analysisTypes.push(`📧 Header Analysis: ${breakdown.header_analysis.confidence}% confidence`);
    }
    
    if (breakdown.content_analysis) {
        analysisTypes.push(`🤖 Content Analysis: ${breakdown.content_analysis.confidence}% confidence`);
    }
    
    if (breakdown.ml_model_analysis) {
        analysisTypes.push(`🧠 ML Model: ${breakdown.ml_model_analysis.confidence}% confidence`);
    }
    
    // Add analysis breakdown to indicators
    analysisTypes.forEach(type => {
        const indicatorElement = document.createElement('div');
        indicatorElement.className = 'indicator analysis-type';
        indicatorElement.innerHTML = `
            <span class="indicator-icon">📊</span>
            <span>${type}</span>
        `;
        indicatorsList.appendChild(indicatorElement);
    });
    
    // Add security features if available
    if (breakdown.header_analysis && breakdown.header_analysis.security_features) {
        const securityFeatures = breakdown.header_analysis.security_features;
        
        if (securityFeatures.spf) {
            const spfStatus = securityFeatures.spf.exists ? '✅' : '❌';
            const spfElement = document.createElement('div');
            spfElement.className = 'indicator security-feature';
            spfElement.innerHTML = `
                <span class="indicator-icon">${spfStatus}</span>
                <span>SPF Record: ${securityFeatures.spf.exists ? 'Found' : 'Missing'}</span>
            `;
            indicatorsList.appendChild(spfElement);
        }
        
        if (securityFeatures.dkim) {
            const dkimStatus = securityFeatures.dkim.exists ? '✅' : '❌';
            const dkimElement = document.createElement('div');
            dkimElement.className = 'indicator security-feature';
            dkimElement.innerHTML = `
                <span class="indicator-icon">${dkimStatus}</span>
                <span>DKIM Record: ${securityFeatures.dkim.exists ? 'Found' : 'Missing'}</span>
            `;
            indicatorsList.appendChild(dkimElement);
        }
        
        if (securityFeatures.domain_consistency !== undefined) {
            const consistencyStatus = securityFeatures.domain_consistency ? '✅' : '❌';
            const consistencyElement = document.createElement('div');
            consistencyElement.className = 'indicator security-feature';
            consistencyElement.innerHTML = `
                <span class="indicator-icon">${consistencyStatus}</span>
                <span>Domain Consistency: ${securityFeatures.domain_consistency ? 'Good' : 'Mismatch detected'}</span>
            `;
            indicatorsList.appendChild(consistencyElement);
        }
        
        if (securityFeatures.smtp_legitimacy !== undefined) {
            const smtpStatus = securityFeatures.smtp_legitimacy ? '✅' : '❌';
            const smtpElement = document.createElement('div');
            smtpElement.className = 'indicator security-feature';
            smtpElement.innerHTML = `
                <span class="indicator-icon">${smtpStatus}</span>
                <span>SMTP Server Legitimacy: ${securityFeatures.smtp_legitimacy ? 'Verified' : 'Suspicious'}</span>
            `;
            indicatorsList.appendChild(smtpElement);
        }
    }
}

// Get recommendations based on analysis
function getRecommendations(confidence, indicators) {
    const recommendations = [];
    
    if (confidence >= 70) {
        recommendations.push("Do not click any links in this email");
        recommendations.push("Do not provide any personal information");
        recommendations.push("Delete this email immediately");
        recommendations.push("Report this email to your IT department");
    } else if (confidence >= 40) {
        recommendations.push("Be cautious with this email");
        recommendations.push("Verify the sender's identity");
        recommendations.push("Check the URL carefully before clicking");
    } else {
        recommendations.push("This email appears to be safe");
        recommendations.push("Continue with normal email practices");
    }
    
    return recommendations;
}

// Add analysis to history
function addToHistory(data) {
    const historyList = document.getElementById("analysisHistory");
    const placeholder = document.querySelector(".history-placeholder");
    
    if (placeholder) {
        placeholder.remove();
    }
    
    const historyItem = document.createElement('div');
    historyItem.className = 'history-item';
    
    const emailPreview = document.getElementById("emailInput").value.substring(0, 50) + '...';
    const timestamp = new Date().toLocaleTimeString();
    
    historyItem.innerHTML = `
        <div class="history-content">
            <div class="history-email">${emailPreview}</div>
            <div class="history-result">${data.result}</div>
        </div>
        <div class="history-time">${timestamp}</div>
    `;
    
    historyList.insertBefore(historyItem, historyList.firstChild);
    
    // Keep only last 10 items
    const items = historyList.querySelectorAll('.history-item');
    if (items.length > 10) {
        items[items.length - 1].remove();
    }
}

    // Load user info and display username
    async function loadUserInfo() {
        try {
            const response = await fetch('/api/user_info', {
                method: 'GET',
                headers: { "Content-Type": "application/json" }
            });
            
            if (response.ok) {
                const data = await response.json();
                const userInfoElement = document.getElementById('userInfo');
                if (userInfoElement) {
                    userInfoElement.textContent = `👤 ${data.username}`;
                    userInfoElement.className = 'user-info';
                }
            } else {
                console.error('Failed to load user info');
            }
        } catch (error) {
            console.error('Error loading user info:', error);
        }
    }

    // Load analysis history from database
    async function loadAnalysisHistory() {
        try {
            const response = await fetch('/api/analysis_history', {
                method: 'GET',
                headers: { "Content-Type": "application/json" }
            });
            
            if (response.ok) {
                const data = await response.json();
                displayAnalysisHistory(data.history);
            } else {
                console.error('Failed to load analysis history');
            }
        } catch (error) {
            console.error('Error loading analysis history:', error);
        }
    }



// Logout functionality
document.addEventListener('DOMContentLoaded', function() {
    const logoutBtn = document.querySelector('.logout-btn');
    
    if (logoutBtn) {
        logoutBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            
            try {
                await fetch('/api/logout', { method: 'GET' });
            } catch (error) {
                console.log('Logout error:', error);
            }
            
            // Clear session storage
            sessionStorage.removeItem('isLoggedIn');
            sessionStorage.removeItem('username');
            
            // Redirect to home
            window.location.href = "/";
        });
    }
});

// Auto-resize textarea
document.addEventListener('DOMContentLoaded', function() {
    const emailInput = document.getElementById("emailInput");
    
    if (emailInput) {
        emailInput.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 300) + 'px';
        });
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl+Enter to analyze email
    if (e.ctrlKey && e.key === 'Enter') {
        const checkBtn = document.getElementById("checkBtn");
        if (checkBtn && !checkBtn.disabled) {
            checkBtn.click();
        }
    }
    
    // Escape to clear form
    if (e.key === 'Escape') {
        const emailInput = document.getElementById("emailInput");
        const urlInput = document.getElementById("urlInput");
        
        if (emailInput) emailInput.value = '';
        if (urlInput) urlInput.value = '';
    }
});

// Scroll effects for history section
function initializeScrollEffects() {
    const historyList = document.getElementById("analysisHistory");
    const scrollIndicator = document.getElementById("scrollIndicator");
    
    if (!historyList) return;
    
    // Show/hide scroll indicator based on content
    function updateScrollIndicator() {
        const hasScroll = historyList.scrollHeight > historyList.clientHeight;
        const isScrolled = historyList.scrollTop > 0;
        
        if (hasScroll) {
            scrollIndicator.classList.remove('hidden');
            updateScrollDots();
        } else {
            scrollIndicator.classList.add('hidden');
        }
    }
    
    // Update scroll dots based on scroll position
    function updateScrollDots() {
        const dots = scrollIndicator.querySelectorAll('.scroll-dot');
        const scrollPercentage = historyList.scrollTop / (historyList.scrollHeight - historyList.clientHeight);
        
        dots.forEach((dot, index) => {
            const dotThreshold = index / (dots.length - 1);
            if (scrollPercentage >= dotThreshold) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    }
    
    // Smooth scroll to specific item
    function scrollToItem(index) {
        const items = historyList.querySelectorAll('.history-item');
        if (items[index]) {
            const itemTop = items[index].offsetTop;
            const containerTop = historyList.offsetTop;
            const scrollTop = itemTop - containerTop - 20; // 20px offset
            
            historyList.scrollTo({
                top: scrollTop,
                behavior: 'smooth'
            });
        }
    }
    
    // Add click handlers to scroll dots
    const dots = scrollIndicator.querySelectorAll('.scroll-dot');
    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            const items = historyList.querySelectorAll('.history-item');
            const itemIndex = Math.floor((index / (dots.length - 1)) * (items.length - 1));
            scrollToItem(itemIndex);
        });
    });
    
    // Add scroll event listener
    historyList.addEventListener('scroll', () => {
        updateScrollDots();
    });
    
    // Add resize event listener
    window.addEventListener('resize', () => {
        updateScrollIndicator();
    });
    
    // Initial update
    updateScrollIndicator();
    
    // Update after content loads
    setTimeout(updateScrollIndicator, 1000);
    
    // Add hover effect for scroll indicator
    scrollIndicator.addEventListener('mouseenter', () => {
        scrollIndicator.style.opacity = '1';
    });
    
    scrollIndicator.addEventListener('mouseleave', () => {
        scrollIndicator.style.opacity = '0.6';
    });
}

// Enhanced history display with scroll effects
function displayAnalysisHistory(history) {
    const historyList = document.getElementById("analysisHistory");
    const placeholder = document.querySelector(".history-placeholder");
    
    if (placeholder) {
        placeholder.remove();
    }
    
    if (!history || history.length === 0) {
        historyList.innerHTML = `
            <div class="history-placeholder">
                <p>No recent analyses yet</p>
                <p class="small-text">Your analysis history will appear here</p>
            </div>
        `;
        // Update scroll indicator after showing placeholder
        setTimeout(() => {
            if (typeof initializeScrollEffects === 'function') {
                initializeScrollEffects();
            }
        }, 100);
        return;
    }
    
    historyList.innerHTML = '';
    
    history.forEach((item, index) => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        historyItem.style.animationDelay = `${(index + 1) * 0.1}s`;
        
        const emailPreview = item.email_preview || 'No content';
        const timestamp = item.timestamp || 'Unknown time';
        const result = item.result || 'No result';
        const confidence = item.confidence || 0;
        
        // Determine status class based on confidence
        let statusClass = 'safe';
        if (confidence >= 70) {
            statusClass = 'danger';
        } else if (confidence >= 40) {
            statusClass = 'warning';
        }
        
        historyItem.innerHTML = `
            <div class="history-content">
                <div class="history-email">${emailPreview}</div>
                <div class="history-result ${statusClass}">${result}</div>
            </div>
            <div class="history-time">${timestamp}</div>
        `;
        
        historyList.appendChild(historyItem);
    });
    
    // Update scroll indicator after adding items
    setTimeout(() => {
        if (typeof initializeScrollEffects === 'function') {
            initializeScrollEffects();
        }
    }, 100);
}
