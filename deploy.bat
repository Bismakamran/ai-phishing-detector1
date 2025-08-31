@echo off
echo 🚀 AI Phishing Email Detection - Deployment Preparation
echo ======================================================

echo.
echo 📋 Checking required files...

if exist "app.py" (
    echo ✅ app.py exists
) else (
    echo ❌ app.py is missing
    goto :error
)

if exist "requirements.txt" (
    echo ✅ requirements.txt exists
) else (
    echo ❌ requirements.txt is missing
    goto :error
)

if exist "render.yaml" (
    echo ✅ render.yaml exists
) else (
    echo ❌ render.yaml is missing
    goto :error
)

if exist "Procfile" (
    echo ✅ Procfile exists
) else (
    echo ❌ Procfile is missing
    goto :error
)

if exist "runtime.txt" (
    echo ✅ runtime.txt exists
) else (
    echo ❌ runtime.txt is missing
    goto :error
)

if exist ".env" (
    echo ✅ .env file exists
) else (
    echo ⚠️  .env file not found. You'll need to set environment variables in your deployment platform.
)

echo.
echo 📊 Checking database connection...
python view_database.py

echo.
echo 🎯 Deployment Options:
echo 1. Render (Recommended - Free)
echo 2. Railway (Free)
echo 3. Heroku (Paid)
echo 4. AWS (Production)

echo.
echo 📝 Next Steps:
echo 1. Choose your deployment platform
echo 2. Follow the instructions in DEPLOYMENT_GUIDE.md
echo 3. Set up MongoDB Atlas for database
echo 4. Configure environment variables
echo 5. Deploy!

echo.
echo 🔗 Useful Links:
echo - Render: https://render.com
echo - Railway: https://railway.app
echo - MongoDB Atlas: https://mongodb.com/atlas
echo - Heroku: https://heroku.com

echo.
echo ✅ Deployment preparation complete!
pause
goto :end

:error
echo.
echo ❌ Deployment preparation failed. Please fix the missing files.
pause
exit /b 1

:end
