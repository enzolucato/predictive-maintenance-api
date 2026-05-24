## Predictive Maintenance API ##

Visão Geral do Projeto (Business Overview)

A manutenção reativa e paradas não programadas geram prejuízos milionários para o setor industrial. Este projeto implementa uma solução End-to-End de Machine Learning para prever falhas em equipamentos mecânicos com base em telemetria em tempo real, permitindo a transição para uma estratégia de Manutenção Preditiva.

O modelo matemático analisa padrões anômalos de sensores físicos e expõe os seus diagnósticos através de uma API RESTful de alta performance, pronta para ser integrada a dashboards de monitorização ou sistemas de controlo fabril.

Arquitetura e Modelagem (MLOps Core)

O Desafio dos Dados: O cenário industrial apresenta um grave desbalanceamento de classes (máquinas operam normalmente em >96% do tempo).

A Solução: Foi utilizado um algoritmo de Random Forest Classifier com parâmetro class_weight='balanced' para mitigar falsos negativos, garantindo foco em eventos de quebra.

Ciclo de Vida (MLflow): O rastreamento de experimentos, versionamento de hiperparâmetros (n_estimators, class_weight) e métricas de validação (F1-Score, Accuracy) são integralmente gerenciados pelo MLflow.

Conteinerização (Docker): A aplicação é totalmente isolada em um container estável, garantindo a mesma performance em ambiente local ou cloud deploy.

Estrutura do Repositório
```
predictive-maintenance-api/
│
├── data/               # Diretório ignorado pelo Git (armazena os CSVs brutos)
├── models/             # Artefatos do modelo treinado (.joblib)
├── notebooks/          # Jupyter Notebooks para EDA e treinamento com MLflow
├── mlruns/             # Logs e métricas rastreadas pelo MLflow (local)
├── src/                # Código-fonte principal
│   └── main.py                 # Servidor FastAPI e rotas de predição
├── .dockerignore       # Arquivos excluídos do build do container
├── .gitignore          # Regras de exclusão de ficheiros do Git
├── Dockerfile          # Instruções de build da imagem Docker
├── README.md           # Documentação do projeto
└── requirements.txt    # Dependências e bibliotecas do ecossistema
```

Como Executar Localmente (Setup Guide)

Opção A: Execução Nativa (Ambiente Virtual)

1. Clone o repositório e acesse a pasta:
```
git clone https://github.com/enzolucato/predictive-maintenance-api.git
cd predictive-maintenance-api
```

2. Crie a venv e instale as dependências:
```
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Inicie a API e a UI do MLflow:
```
# Para rodar a API
uvicorn src.main:app --reload
```
## Para visualizar os experimentos no MLflow (em outro terminal) ##

mlflow ui 

Acesse a API e o Swagger em: http://127.0.0.1:8000/docs

Acesse o Dashboard do MLflow em: http://127.0.0.1:5000

Opção B: Execução via Docker (Production Mode)

Se você possui o Docker instalado, pode construir a imagem e rodar o container sem precisar instalar o Python localmente:

1. Construa a imagem Docker:
```
docker build -t predictive-maintenance-api .
```

2. Execute o container mapeando as portas:
```
docker run -p 8000:8000 predictive-maintenance-api
```

A API estará pronta para receber requisições de produção na porta 8000.

Uso da API (Endpoints)

Exemplo de Requisição POST /predict:
```
{
  "Type": 0,
  "Air_temperature": 305.0,
  "Process_temperature": 315.0,
  "Rotational_speed": 1150,
  "Torque": 75.0,
  "Tool_wear": 220
}
```

Resposta Esperada:
```
{
  "status_maquina": "Risco de Falha Detectado!",
  "probabilidade_de_falha": "62.00%"
}
```
