@echo off
echo 🚀 AI Phishing Email Detection - Render Deployment Helper
echo ========================================================

echo.
echo 📋 Pre-deployment Checklist:
echo.

echo ✅ 1. Git repository initialized
echo ✅ 2. All files committed
echo ✅ 3. Deployment files created
echo.

echo 📝 Next Steps:
echo.
echo 1. Create GitHub repository:
echo    - Go to github.com
echo    - Click "New repository"
echo    - Name: ai-phishing-detector
echo    - Make it PUBLIC
echo    - Don't initialize with README
echo.

echo 2. Push to GitHub (run these commands):
echo    git remote add origin https://github.com/YOUR_USERNAME/ai-phishing-detector.git
echo    git branch -M main
echo    git push -u origin main
echo.

echo 3. Set up MongoDB Atlas:
echo    - Go to mongodb.com/atlas
echo    - Create free account
echo    - Create M0 cluster
echo    - Configure database access
echo    - Get connection string
echo.

echo 4. Deploy to Render:
echo    - Go to render.com
echo    - Sign up with GitHub
echo    - Create new Web Service
echo    - Connect your repository
echo    - Set environment variables
echo    - Deploy!
echo.

echo 📖 For detailed instructions, see: DEPLOY_TO_RENDER.md
echo.

echo 🔗 Useful Links:
echo - GitHub: https://github.com
echo - MongoDB Atlas: https://mongodb.com/atlas
echo - Render: https://render.com
echo.

echo 🎯 Ready to deploy? Follow the steps above!
echo.
pause
