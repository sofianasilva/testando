FROM python:3.10-slim-bullseye

# Variáveis de ambiente
ENV DJANGO_SETTINGS_MODULE=zeppelin.settings.local
#ENV PYTHONPATH=/app
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV DEBUG=true

# Define o diretório de trabalho
WORKDIR /app

# Copia tudo do projeto (raiz, onde está o docker-compose.yml)
COPY ./src/ ./src/
COPY .env .
COPY supervisord.conf .

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    netcat \
    gcc \
    libpq-dev \
    libffi-dev \
    musl-dev \
    python3-dev \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Muda para o diretório src onde o Django deve rodar
WORKDIR /app/src

# Instala dependências Python
RUN pip install -r requirements.txt

# Cria o diretório de logs no local correto (relativo ao working dir atual)
RUN mkdir -p logs

RUN python manage.py collectstatic --noinput --no-post-process

# Volta para /app para copiar arquivos de configuração
WORKDIR /app

COPY supervisord.conf /etc/supervisord.conf

# Fix line endings and copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

# Define working directory final
WORKDIR /app/src

ENTRYPOINT ["/entrypoint.sh"]

CMD ["supervisord", "-c", "/etc/supervisord.conf"]