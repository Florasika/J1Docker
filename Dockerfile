# ============================================================
#  JOUR 1 / 10 — Docker : Premier Conteneur
#  Image : Python 3.11 slim (légère, sans OS complet)
# ============================================================

# FROM : image de base — point de départ du conteneur
# python:3.11-slim = Python officiel, version légère (~45MB vs ~900MB)
FROM python:3.11-slim

# LABEL : métadonnées de l'image (optionnel mais bonne pratique)
LABEL maintainer="sung@email.com"
LABEL description="Jour 1 Docker — pipeline ETL simple"
LABEL version="1.0"

# WORKDIR : définit le dossier de travail dans le conteneur
# Toutes les commandes suivantes s'exécutent depuis /app
WORKDIR /app

# COPY requirements.txt en premier — optimisation du cache Docker
# Si requirements.txt ne change pas, Docker réutilise le cache de pip install
COPY requirements.txt .

# RUN : exécuter une commande pendant le build de l'image
# --no-cache-dir → ne pas stocker le cache pip (réduit la taille)
RUN pip install --no-cache-dir -r requirements.txt

# COPY le reste du code APRÈS pip install (optimisation cache)
COPY app/ ./app/

# ENV : variables d'environnement disponibles dans le conteneur
ENV PYTHONUNBUFFERED=1
ENV DATA_PATH=/app/data
ENV OUTPUT_PATH=/app/output

# RUN : créer les dossiers nécessaires
RUN mkdir -p /app/data /app/output

# EXPOSE : documenter le port utilisé (informatif, pas obligatoire)
# EXPOSE 8080

# CMD : commande lancée quand le conteneur démarre
# Forme JSON recommandée (évite les problèmes de signaux)
CMD ["python", "app/main.py"]
