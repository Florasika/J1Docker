# 🐳 Jour 1 / 10 — Docker : Introduction & Premier Conteneur

> **Série : 10 Days of Docker** · Jour 1/10  
> Concepts : Image · Conteneur · Dockerfile · docker build · docker run · Volumes

---

## 📁 Fichiers du projet

```
day-01-introduction/
│
├── Dockerfile         ← Instructions pour construire l'image
├── requirements.txt   ← Dépendances Python
├── app/
│   └── main.py        ← Pipeline ETL qui tourne dans le conteneur
└── README.md
```

---

## 🧠 Image vs Conteneur

```
Image     = la recette (lecture seule, comme un template)
Conteneur = l'instance en cours d'exécution de l'image

Une image peut lancer N conteneurs simultanément.
Construire une image → docker build
Lancer un conteneur  → docker run
```

---

## 🚀 ÉTAPE 1 — Installer Docker

```bash
# Windows / Mac : télécharger Docker Desktop
https://www.docker.com/products/docker-desktop/

# Linux (Ubuntu)
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

# Vérifier l'installation
docker --version
docker run hello-world
```

---

## 🚀 ÉTAPE 2 — Préparer les fichiers

```
Créer la structure suivante :
jour1-docker/
    ├── Dockerfile
    ├── requirements.txt
    └── app/
        └── main.py

Copier les fichiers du dépôt dans ce dossier.
```

---

## 🚀 ÉTAPE 3 — Construire l'image

```bash
# Se placer dans le dossier du projet
cd jour1-docker/

# Construire l'image
# -t = tag (nom:version)
# .  = contexte de build (dossier courant)
docker build -t etl-jour1:1.0 .

# Observer les étapes du build :
# Step 1/10 : FROM python:3.11-slim     ← télécharge l'image de base
# Step 2/10 : LABEL ...
# Step 3/10 : WORKDIR /app
# Step 4/10 : COPY requirements.txt .
# Step 5/10 : RUN pip install ...       ← installe les dépendances
# Step 6/10 : COPY app/ ./app/
# ...
# Successfully built abc123def456
# Successfully tagged etl-jour1:1.0
```

---

## 🚀 ÉTAPE 4 — Lister les images

```bash
# Voir les images disponibles localement
docker images

# Résultat :
# REPOSITORY   TAG   IMAGE ID       CREATED        SIZE
# etl-jour1    1.0   abc123def456   2 minutes ago  180MB
# python       3.11-slim  ...
```

---

## 🚀 ÉTAPE 5 — Lancer le conteneur

```bash
# Lancer le conteneur (simple)
docker run etl-jour1:1.0

# Lancer avec un volume monté (pour récupérer les fichiers output)
# -v chemin_hote:chemin_conteneur
mkdir -p ./output
docker run -v $(pwd)/output:/app/output etl-jour1:1.0

# Windows (PowerShell)
docker run -v ${PWD}/output:/app/output etl-jour1:1.0

# Résultat attendu :
# ========================================
#   Pipeline ETL — Jour 1 Docker
# ========================================
# [EXTRACT] 30 lignes extraites
# [TRANSFORM] Marge ajoutée — CA: 18600€
# [LOAD] CSV  → /app/output/ventes_20240101_120000.csv
# [LOAD] KPIs → /app/output/kpis_20240101_120000.json
# === KPIs ===
#   date            : 2024-01-01T12:00:00
#   ca_total        : 18600.0
#   ...
# ✓ Pipeline terminé avec succès
```

---

## 🚀 ÉTAPE 6 — Inspecter le conteneur

```bash
# Voir les conteneurs en cours (aucun car notre conteneur s'arrête)
docker ps

# Voir TOUS les conteneurs (y compris arrêtés)
docker ps -a

# Résultat :
# CONTAINER ID  IMAGE          COMMAND            STATUS    NAMES
# f3a1b2c3d4e5  etl-jour1:1.0  "python app/mai…"  Exited    hopeful_tesla

# Voir les logs d'un conteneur (par ID ou nom)
docker logs f3a1b2c3d4e5

# Entrer dans un conteneur en cours (mode interactif)
docker run -it etl-jour1:1.0 /bin/bash
# → ouvre un shell dans le conteneur
# → ls, cd /app, python app/main.py...
# → exit pour quitter
```

---

## 🚀 ÉTAPE 7 — Variables d'environnement

```bash
# Passer des variables d'environnement au conteneur
docker run \
    -e DATA_PATH=/app/data \
    -e OUTPUT_PATH=/app/output \
    -v $(pwd)/output:/app/output \
    etl-jour1:1.0

# Depuis un fichier .env
cat > .env << 'ENV'
DATA_PATH=/app/data
OUTPUT_PATH=/app/output
ENV

docker run --env-file .env -v $(pwd)/output:/app/output etl-jour1:1.0
```

---

## 🚀 ÉTAPE 8 — Nettoyer

```bash
# Supprimer un conteneur arrêté
docker rm f3a1b2c3d4e5

# Supprimer tous les conteneurs arrêtés
docker container prune

# Supprimer une image
docker rmi etl-jour1:1.0

# Supprimer toutes les images non utilisées
docker image prune -a

# Tout nettoyer (conteneurs + images + cache)
docker system prune -a
```

---

## 🔑 Structure du Dockerfile expliquée

```dockerfile
# Image de base — point de départ
FROM python:3.11-slim

# Dossier de travail dans le conteneur
WORKDIR /app

# Copier requirements AVANT le code → optimisation du cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code APRÈS pip install
COPY app/ ./app/

# Variables d'environnement
ENV PYTHONUNBUFFERED=1

# Commande par défaut au démarrage
CMD ["python", "app/main.py"]
```

**Pourquoi COPY requirements.txt avant COPY app/ ?**

Docker met en cache chaque couche. Si le code change mais pas les dépendances, Docker réutilise le cache de `pip install`. Le build est ainsi beaucoup plus rapide.

---

## 💡 Commandes Docker essentielles

| Commande | Description |
|----------|-------------|
| `docker build -t nom:tag .` | Construire une image |
| `docker run nom:tag` | Lancer un conteneur |
| `docker run -it nom:tag /bin/bash` | Shell interactif |
| `docker run -v hote:conteneur` | Monter un volume |
| `docker run -e VAR=val` | Variable d'environnement |
| `docker ps` | Conteneurs en cours |
| `docker ps -a` | Tous les conteneurs |
| `docker images` | Images locales |
| `docker logs <id>` | Logs d'un conteneur |
| `docker rm <id>` | Supprimer un conteneur |
| `docker rmi <image>` | Supprimer une image |
| `docker system prune` | Tout nettoyer |

---


---

⭐ **Si ce projet t'aide, mets une étoile !**
