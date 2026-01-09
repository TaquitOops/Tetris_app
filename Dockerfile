FROM python:3.12-slim

WORKDIR /app

# Copiamos el proyecto real
COPY project/ ./project/

# Instalamos dependencias
RUN pip install --no-cache-dir -r project/requirements.txt

ENV PORT=8080
EXPOSE 8080

CMD ["python", "project/src/main.py"]
