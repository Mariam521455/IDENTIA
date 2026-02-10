# IDENTIA
**Plateforme de reconnaissance faciale pour la gestion des présences – Projet Institutionnel**

IDENTIA est une solution métier robuste, traçable et auditable conçue pour l'automatisation du pointage des étudiants dans les établissements d'enseignement supérieur.

---

## 🚀 Guide d'Installation (Windows)

### 1. Configuration de l'environnement
Ouvrez votre terminal dans le dossier `IDENTIA` et exécutez :

```powershell
# Définir la politique d'exécution (nécessaire une seule fois)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Créer et activer l'environnement virtuel
python -m venv venv
.\venv\Scripts\activate

# Installer les dépendances (Flask, IA, DB)
pip install -r requirements.txt
```

### 2. Initialisation du Système
Créez la base de données et le compte administrateur par défaut :
```powershell
flask init-db
```

### 3. Lancement de la Plateforme
```powershell
python run.py
```

---

## 🔑 Accès Par Défaut
- **URL** : `http://127.0.0.1:5000`
- **Username** : `admin`
- **Password** : `admin123`

---

## 🏗️ Architecture & Sécurité
- **Backend** : Flask / SQLAlchemy (Architecture en couches)
- **Base de données** : SQLite (Mode offline-first avec audit complet)
- **IA** : OpenCV + face_recognition (Modèle HOG/CNN)
- **Sécurité** : RBAC (SuperAdmin, Admin, TechUser), Protection CSRF, Audit Logging
- **Frontend** : Tailwind CSS / UI Institutionnelle premium
