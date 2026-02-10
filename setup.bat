@echo off
echo ==========================================
echo   IDENTIA - Initialisation du Systeme
echo ==========================================

echo [1/4] Creation de l'environnement virtuel...
python -m venv venv

echo [2/4] Activation de l'environnement...
call venv\Scripts\activate

echo [3/4] Installation des dependances (cela peut prendre du temps)...
pip install -r requirements.txt

echo [4/4] Initialisation de la base de données...
flask init-db

echo ==========================================
echo   Installation terminee !
echo   Pour lancer IDENTIA : python run.py
echo ==========================================
pause
