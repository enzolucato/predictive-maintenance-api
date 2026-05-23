from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# 1. Iniciando a nossa API
app = FastAPI(
    title="API de Manutenção Preditiva",
    description="API para prever falhas em equipamentos industriais com base em telemetria.",
    version="1.0"
)

# 2. Carregando o "Cérebro" que treinamos no Dia 3
# Atenção ao caminho: a API vai rodar a partir da pasta raiz do projeto
modelo = joblib.load('./models/predictive_maintenance_model.joblib')

# 3. Definindo o formato dos dados que a API vai receber (Os Sensores)
class DadosSensores(BaseModel):
    Type: int  # 0 (Low), 1 (Medium), 2 (High)
    Air_temperature: float
    Process_temperature: float
    Rotational_speed: int
    Torque: float
    Tool_wear: int

# 4. Criando a Rota de Previsão
@app.post("/predict")
def prever_falha(dados: DadosSensores):
    # Traduzindo os dados recebidos para o formato exato que a IA aprendeu
    df_input = pd.DataFrame([{
        'Type': dados.Type,
        'Air temperature [K]': dados.Air_temperature,
        'Process temperature [K]': dados.Process_temperature,
        'Rotational speed [rpm]': dados.Rotational_speed,
        'Torque [Nm]': dados.Torque,
        'Tool wear [min]': dados.Tool_wear
    }])
    
    # Pedindo para a IA fazer o diagnóstico
    previsao = modelo.predict(df_input)[0]
    probabilidade = modelo.predict_proba(df_input)[0][1] # Pega a chance da classe 1 (Falha)
    
    # Retornando a resposta para a fábrica
    return {
        "status_maquina": "Risco de Falha Detectado!" if previsao == 1 else "Operação Normal",
        "probabilidade_de_falha": f"{probabilidade * 100:.2f}%"
    }