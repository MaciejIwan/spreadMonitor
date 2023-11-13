# Użyj oficjalnego obrazu Pythona jako bazowego
FROM python:3.8-slim

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj pliki aplikacji do katalogu roboczego w kontenerze
COPY . /app

# Zainstaluj wymagane pakiety Pythona
RUN pip install fastapi uvicorn mysql-connector-python jinja2 requests SQLAlchemy

# Odkryj port, na którym uruchomiona jest aplikacja
EXPOSE 8000

# Zdefiniuj polecenie do uruchomienia aplikacji
#CMD ["python", "./main.py", "&"]
#CMD ["uvicorn", "webAccess:app", "--host", "0.0.0.0", "--port", "8000"]

