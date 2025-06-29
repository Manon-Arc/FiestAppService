FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier la structure des fichiers
COPY src/ /app/src/
COPY data/ /app/data/
COPY model/ /app/model/
COPY app.py /app/
COPY model.py /app/
COPY train.py /app/
COPY types_custom.py /app/
COPY utils.py /app/

# Créer un utilisateur non-root
RUN adduser --disabled-password --gecos '' fiestappuser && \
    chown -R fiestappuser:fiestappuser /app
USER fiestappuser

# Exposer le port
EXPOSE 8000

# Commande par défaut (app.py est à la racine)
CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
