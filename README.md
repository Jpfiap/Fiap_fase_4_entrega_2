## Atualizações da FASE 4

### Machine Learning com Scikit-learn
- **Modelo**: Random Forest Regressor
- **Funcionalidade**: Previsão de necessidade de irrigação
- **Features**:
  - Histórico de umidade
  - Níveis de pH
  - Presença de nutrientes
  - Dados meteorológicos

### Dashboard Streamlit
- **Interface**: Web interativa
- **Funcionalidades**:
  - Monitoramento em tempo real
  - Gráficos de tendências
  - Previsões de umidade
  - Recomendações de irrigação
  - Análise de dados históricos

### Nova Tabela: previsao_irrigacao
```sql
CREATE TABLE previsao_irrigacao (
    id_previsao SERIAL PRIMARY KEY,
    id_lote INT REFERENCES lote(id_lote),
    timestamp TIMESTAMP NOT NULL,
    umidade_prevista NUMERIC(5,2),
    probabilidade_irrigacao NUMERIC(5,2),
    confianca_modelo NUMERIC(5,2)
);
```

### Requisitos Adicionais
```bash
streamlit==1.32.0
scikit-learn==1.4.0
plotly==5.18.0
```
# Farmtech Solution Fase 4 - Dashboard

Este projeto contém o dashboard da Farmtech Solution, desenvolvido com Streamlit.

## Pré-requisitos

Certifique-se de ter o Python 3.8+ instalado em seu sistema.

## Configuração do Ambiente

Siga os passos abaixo para configurar o ambiente e instalar as dependências necessárias.

1.  **Navegue até o diretório do projeto:**

    Abra seu terminal (Prompt de Comando ou PowerShell no Windows) e navegue até a pasta raiz do projeto:

    ```bash
    cd C:\Users\Jp\Desktop\Farmtech Solution Fase 4
    ```

2.  **Crie um Ambiente Virtual (se ainda não tiver feito):**

    É altamente recomendável usar um ambiente virtual para isolar as dependências do projeto. Execute o seguinte comando no diretório raiz do projeto:

    ```bash
    python -m venv venv
    ```

3.  **Ative o Ambiente Virtual:**

    No Windows, ative o ambiente virtual com o seguinte comando:

    ```bash
    .\venv\Scripts\activate
    ```

    Você saberá que o ambiente virtual está ativado quando `(venv)` aparecer no início da linha de comando.

4.  **Instale as Dependências:**

    Com o ambiente virtual ativado, instale as bibliotecas necessárias (incluindo o Streamlit):

    ```bash
    pip install streamlit numpy pandas matplotlib scikit-learn
    ```
    *(Nota: Adicione quaisquer outras bibliotecas que seu projeto utilize aqui.)*

5.  **Crie a Estrutura de Módulos (se necessário):**

    Se você encontrar um erro como `ModuleNotFoundError: No module named 'models'`, significa que a estrutura de pacotes não foi criada. Para corrigir isso, crie uma pasta chamada `models` na raiz do projeto e, dentro dela, crie um arquivo vazio chamado `__init__.py`.

    ```
    # Estrutura esperada:
    Farmtech Solution Fase 4/
    ├── app.py
    ├── models/
    │   └── __init__.py  # Este arquivo pode estar vazio
    ├── data_generator.py
    ├── irrigation_model.py
    ├── sensor_data.py
    └── venv/
        └── ...
    ```

## Como Executar o Dashboard

Com o ambiente virtual ativado e todas as dependências instaladas, você pode iniciar o dashboard:

1.  **Certifique-se de estar no diretório raiz do projeto** (`C:\Users\Jp\Desktop\Farmtech Solution Fase 4`).

2.  **Execute o aplicativo Streamlit:**

    ```bash
    python -m streamlit run app.py
    ```

    Após executar este comando, o Streamlit abrirá automaticamente o dashboard no seu navegador padrão. Se não abrir, ele fornecerá um URL (geralmente `http://localhost:8501`) que você pode copiar e colar no seu navegador.