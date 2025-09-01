
#!/bin/bash

echo "🚀 AI Phishing Email Detection - Deployment Script"
echo "=================================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if all required files exist
echo "📋 Checking required files..."
required_files=("app.py" "requirements.txt" "render.yaml" "Procfile" "runtime.txt")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file is missing"
        exit 1
    fi
done

# Check if .env file exists
if [ -f ".env" ]; then
    echo "✅ .env file exists"
else
    echo "⚠️  .env file not found. You'll need to set environment variables in your deployment platform."
fi

# Check git status
echo "📊 Git status:"
git status --porcelain

# Check if there are uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  You have uncommitted changes. Consider committing them before deployment."
    read -p "Do you want to commit changes? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        git commit -m "Prepare for deployment"
        echo "✅ Changes committed"
    fi
fi

echo ""
echo "🎯 Deployment Options:"
echo "1. Render (Recommended - Free)"
echo "2. Railway (Free)"
echo "3. Heroku (Paid)"
echo "4. AWS (Production)"

echo ""
echo "📝 Next Steps:"
echo "1. Choose your deployment platform"
echo "2. Follow the instructions in DEPLOYMENT_GUIDE.md"
echo "3. Set up MongoDB Atlas for database"
echo "4. Configure environment variables"
echo "5. Deploy!"

echo ""
echo "🔗 Useful Links:"
echo "- Render: https://render.com"
echo "- Railway: https://railway.app"
echo "- MongoDB Atlas: https://mongodb.com/atlas"
echo "- Heroku: https://heroku.com"

echo ""
echo "✅ Deployment preparation complete!"
