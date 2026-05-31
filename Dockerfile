# 1. Usamos una imagen oficial de Python ligera basada en Debian Linux
FROM python:3.11-slim

# 2. Evita que Python escriba los archivos .pyc en el disco y asegura que los logs salgan directo a la consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalamos las dependencias del sistema necesarias (para compilar librerías o conectar PostgreSQL en el futuro)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copiamos el archivo de requerimientos primero para aprovechar la caché de Docker
COPY requirements.txt /app/

# 6. Actualizamos pip e instalamos las librerías de Python de tu ERP
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 7. Copiamos todo el resto del código de tu ERP dentro del contenedor
COPY . /app/

# 8. Exponemos el puerto 8000 que es donde corre Django por defecto
EXPOSE 8000

# 9. El comando para arrancar el servidor de Django en producción
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]