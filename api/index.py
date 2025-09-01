from app import app

# Vercel serverless function handler
app.debug = False

# Export the Flask app for Vercel
handler = app
