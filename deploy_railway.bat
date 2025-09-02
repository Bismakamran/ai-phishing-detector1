@echo off
echo ========================================
echo Railway Deployment Script
echo ========================================
echo.

echo Cleaning up previous builds...
if exist __pycache__ rmdir /s /q __pycache__
if exist *.pyc del /q *.pyc

echo.
echo Installing Railway CLI...
npm install -g @railway/cli

echo.
echo Logging into Railway...
railway login

echo.
echo Linking to Railway project...
railway link

echo.
echo Deploying to Railway...
railway up

echo.
echo Deployment complete! Check Railway dashboard for status.
pause
