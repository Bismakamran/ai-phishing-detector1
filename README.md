# MailGuard - AI Phishing Email Detector

A modern web application that uses AI-powered detection to identify phishing emails and protect users from cyber threats.

## Features

- 🔐 **Secure Authentication**: Multi-factor authentication with email OTP
- 🛡️ **Strong Password Policy**: Enforces complex password requirements
- 🤖 **AI-Powered Detection**: Uses Hugging Face models for email analysis
- 📧 **Email Header Analysis**: Comprehensive header parsing and security checks
- 🧠 **Machine Learning Model**: Random Forest classifier for header-based detection
- 🔍 **SMTP Server Verification**: Validates email server legitimacy
- 🛡️ **Security Record Checks**: SPF, DKIM, and DMARC validation
- 📊 **Multi-Layer Analysis**: Combines content, header, and ML analysis
- 📊 **Confidence Scoring**: Provides detailed analysis with confidence levels
- 📱 **Modern UI**: Responsive design with dark theme
- 📁 **File Upload**: Support for drag & drop email file uploads
- 📈 **Analysis History**: Track your previous email analyses
- 🔒 **Password Hashing**: Secure password storage using bcrypt

## Tech Stack

- **Backend**: Python Flask
- **Database**: MongoDB with PyMongo
- **AI/ML**: Hugging Face Transformers API
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Authentication**: Session-based with MFA
- **Email**: SMTP for OTP delivery

## Prerequisites

- Python 3.8 or higher
- MongoDB (local or cloud)
- Hugging Face API key
- Gmail account for OTP delivery

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd AI-Phishing-Detection
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   cp env_example.txt .env
   
   # Edit .env with your configuration
   ```

5. **Configure MongoDB**
   - Install MongoDB locally or use MongoDB Atlas
   - Update the `MONGO_URI` in your `.env` file

6. **Get Hugging Face API Key**
   - Sign up at [Hugging Face](https://huggingface.co/)
   - Create an API token
   - Add it to your `.env` file

7. **Configure Email (for OTP)**
   - The application uses Gmail for sending OTP emails
   - **IMPORTANT**: You need to set up Gmail App Password:
     1. Enable 2-factor authentication on your Gmail account
     2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
     3. Generate a new app password for "Mail"
     4. Use the 16-character app password in your `.env` file
   - For production, consider using a dedicated email service

## Configuration

Create a `.env` file with the following variables:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here-change-this-in-production

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017/mailguard

# Hugging Face API Configuration
HUGGINGFACE_API_KEY=your-huggingface-api-key-here

# Email Configuration (for OTP)
# IMPORTANT: Use Gmail App Password, not regular password
EMAIL_ADDRESS=mailguard849@gmail.com
EMAIL_PASSWORD=your-16-character-app-password-here
```

## Running the Application

1. **Train the ML Model (Optional but Recommended)**
   ```bash
   python train_header_model.py
   ```
   This will train a Random Forest model for header analysis. If you don't have a Kaggle dataset, it will create a sample dataset for testing.

2. **Start the Flask server**
   ```bash
   python app.py
   ```

3. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - The application will be available on port 5000

## Usage

### 1. User Registration
- Navigate to the signup page
- Create an account with a strong password
- Verify your email with the OTP sent to your inbox

### 2. User Login
- Login with your credentials
- Complete MFA verification if enabled
- Access the phishing detection dashboard

### 3. Email Analysis
- **For Best Results**: Paste the complete email including headers
  - Gmail: Click "Show original" in the email menu
  - Outlook: Right-click email → "View source"
  - Other clients: Look for "View source" or "Show original" option
- **Alternative**: Paste email content only (basic analysis)
- Optionally provide the URL from the email
- Click "Analyze Email" to get comprehensive results
- View detailed analysis breakdown including:
  - Header analysis results
  - Content analysis results
  - ML model predictions
  - Security feature checks (SPF, DKIM, etc.)
  - Overall risk assessment and recommendations

### 4. Results Interpretation
- **Low Risk (0-39%)**: Email appears safe
- **Medium Risk (40-69%)**: Exercise caution
- **High Risk (70-100%)**: Likely phishing attempt

## Security Features

### Password Policy
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

### Multi-Factor Authentication
- Email-based OTP verification
- 6-digit codes with 10-minute expiration
- Secure session management

### Data Protection
- Passwords hashed using Werkzeug's security functions
- Session-based authentication
- Input validation and sanitization

## API Endpoints

### Authentication
- `POST /api/signup` - User registration
- `POST /api/login` - User login
- `POST /api/verify_mfa` - MFA verification
- `GET /api/logout` - User logout

### Phishing Detection
- `POST /api/detect` - Analyze email for phishing

## Project Structure

```
AI-Phishing-Detection/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── env_example.txt        # Environment variables template
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── index.html        # Landing page
│   ├── login.html        # Login page
│   ├── signup.html       # Registration page
│   └── detector.html     # Phishing detection page
└── static/               # Static assets
    ├── style.css         # CSS styles
    └── script.js         # JavaScript functionality
```

## Phishing Detection Algorithm

The application uses a comprehensive multi-layer analysis approach:

### 1. Content Analysis
- **Urgent Language Detection**: Identifies pressure tactics
- **Sensitive Information Requests**: Detects requests for personal data
- **URL Analysis**: Checks for suspicious link structures
- **Content Length**: Analyzes email brevity
- **Security Protocol**: Validates HTTPS usage

### 2. Header Analysis
- **SMTP Server Verification**: Validates if the sending server is legitimate for the domain
- **Domain Consistency**: Checks if From, Return-Path, and Reply-To domains match
- **Security Records**: Validates SPF, DKIM, and DMARC records
- **Message-ID Validation**: Ensures proper Message-ID format
- **Received Header Analysis**: Tracks email routing path

### 3. Machine Learning Analysis
- **Feature Extraction**: Extracts 20+ features from email headers
- **Random Forest Classification**: Trained model for phishing detection
- **Probability Scoring**: Provides confidence levels for predictions

### 4. Comprehensive Scoring
- **Weighted Analysis**: Combines all three analysis methods
- **Risk Assessment**: Provides overall risk level and confidence
- **Detailed Recommendations**: Offers specific security advice

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team

## Disclaimer

This tool is for educational and security testing purposes. Always use responsibly and in accordance with applicable laws and regulations.

## Future Enhancements

- [ ] Real-time email scanning
- [ ] Advanced ML models
- [ ] Browser extension
- [ ] API rate limiting
- [ ] User analytics dashboard
- [ ] Integration with email clients
- [ ] Custom detection rules
- [ ] Threat intelligence feeds
