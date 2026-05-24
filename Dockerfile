# Utiliza uma imagem oficial leve do Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do contentor
WORKDIR /app

# Evita que o Python escreva ficheiros .pyc no disco
ENV PYTHONDONTWRITEBYTECODE=1
# Garante que as saídas da consola sejam exibidas em tempo real
ENV PYTHONUNBUFFERED=1

# Copia apenas o requirements primeiro para aproveitar a cache do Docker
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto para dentro do contentor
COPY . .

# Expõe a porta que o FastAPI utiliza
EXPOSE 8000

# Comando para iniciar a API em modo de produção
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]