FROM python:3.9-slim

WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances système
COPY requirements.txt /app/

RUN apt update && apt upgrade -y && \
    apt install -y git ffmpeg build-essential libffi-dev python3-dev

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application
COPY . .

CMD ["python", "bot.py"]
