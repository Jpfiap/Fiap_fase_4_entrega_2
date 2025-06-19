import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
from models.irrigation_model import IrrigationModel
from utils.data_generator import SensorDataGenerator
from utils.sensor_data import SensorData

# Configuração da página
st.set_page_config(
    page_title="Sistema de Irrigação Automatizada - Milho",
    page_icon="🌽",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Inicialização de componentes
@st.cache_resource
def load_model():
    return IrrigationModel()


@st.cache_resource
def load_data_generator():
    return SensorDataGenerator()


@st.cache_resource
def load_sensor_data():
    return SensorData()


# Inicializar sessão
if 'irrigation_model' not in st.session_state:
    st.session_state.irrigation_model = load_model()
    st.session_state.data_generator = load_data_generator()
    st.session_state.sensor_data = load_sensor_data()
    st.session_state.pump_status = False
    st.session_state.auto_mode = True
    st.session_state.last_update = datetime.now()


def main():
    st.title("🌽 Sistema de Irrigação Automatizada - Milho")
    st.markdown("**Dashboard de Monitoramento e Controle Preditivo**")

    # Sidebar - Controles
    with st.sidebar:
        st.header("⚙️ Controles do Sistema")

        # Modo de operação
        auto_mode = st.toggle("Modo Automático", value=st.session_state.auto_mode)
        st.session_state.auto_mode = auto_mode

        # Controle manual da bomba
        if not auto_mode:
            manual_pump = st.button("🔄 Alternar Bomba")
            if manual_pump:
                st.session_state.pump_status = not st.session_state.pump_status

        # Configurações de alerta
        st.subheader("🚨 Configurações de Alerta")
        humidity_threshold = st.slider("Umidade Mínima (%)", 20, 80, 45)
        ph_min = st.slider("pH Mínimo", 5.0, 7.5, 6.0, 0.1)
        ph_max = st.slider("pH Máximo", 6.5, 8.5, 7.5, 0.1)

        # Atualizar dados
        if st.button("🔄 Atualizar Dados"):
            st.session_state.last_update = datetime.now()
            st.rerun()

    # Área principal
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        st.subheader("📊 Dados dos Sensores em Tempo Real")

        # Gerar dados atuais
        current_data = st.session_state.data_generator.generate_current_reading()

        # Métricas principais
        metric_cols = st.columns(4)
        with metric_cols[0]:
            st.metric("Umidade do Solo", f"{current_data['humidity']:.1f}%",
                      delta=f"{np.random.uniform(-2, 2):.1f}%")
        with metric_cols[1]:
            st.metric("pH do Solo", f"{current_data['ph']:.1f}",
                      delta=f"{np.random.uniform(-0.1, 0.1):.1f}")
        with metric_cols[2]:
            st.metric("Fósforo", f"{current_data['phosphorus']:.1f} ppm",
                      delta=f"{np.random.uniform(-5, 5):.1f} ppm")
        with metric_cols[3]:
            st.metric("Potássio", f"{current_data['potassium']:.1f} ppm",
                      delta=f"{np.random.uniform(-10, 10):.1f} ppm")

        # Gráfico de tendência
        st.subheader("📈 Tendência dos Sensores (24h)")
        historical_data = st.session_state.data_generator.generate_historical_data(hours=24)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=historical_data['timestamp'], y=historical_data['humidity'],
                                 mode='lines+markers', name='Umidade (%)', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=historical_data['timestamp'], y=historical_data['ph'] * 10,
                                 mode='lines+markers', name='pH (x10)', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=historical_data['timestamp'], y=historical_data['phosphorus'] / 10,
                                 mode='lines+markers', name='Fósforo (/10)', line=dict(color='orange')))
        fig.add_trace(go.Scatter(x=historical_data['timestamp'], y=historical_data['potassium'] / 10,
                                 mode='lines+markers', name='Potássio (/10)', line=dict(color='red')))

        fig.update_layout(
            title="Histórico de Sensores",
            xaxis_title="Tempo",
            yaxis_title="Valores",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🤖 Modelo Preditivo")

        # Predição do modelo
        features = np.array([[current_data['humidity'], current_data['ph'],
                              current_data['phosphorus'], current_data['potassium']]])

        prediction = st.session_state.irrigation_model.predict(features)
        irrigation_probability = st.session_state.irrigation_model.predict_proba(features)[0][1]

        # Mostrar predição
        pred_col1, pred_col2 = st.columns(2)
        with pred_col1:
            st.metric("Necessidade de Irrigação",
                      "SIM" if prediction[0] == 1 else "NÃO",
                      delta=f"{irrigation_probability:.1%} confiança")

        with pred_col2:
            st.metric("Probabilidade", f"{irrigation_probability:.1%}")

        # Gráfico de probabilidade
        fig_prob = go.Figure(go.Indicator(
            mode="gauge+number",
            value=irrigation_probability * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Probabilidade de Irrigação (%)"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgray"},
                    {'range': [30, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        fig_prob.update_layout(height=300)
        st.plotly_chart(fig_prob, use_container_width=True)

        # Importância das features
        st.subheader("📊 Importância dos Fatores")
        feature_importance = st.session_state.irrigation_model.get_feature_importance()

        fig_importance = px.bar(
            x=list(feature_importance.values()),
            y=list(feature_importance.keys()),
            orientation='h',
            title="Importância dos Fatores no Modelo"
        )
        fig_importance.update_layout(height=300)
        st.plotly_chart(fig_importance, use_container_width=True)

    with col3:
        st.subheader("💧 Status da Bomba")

        # Lógica de controle automático
        if st.session_state.auto_mode:
            if prediction[0] == 1 and irrigation_probability > 0.7:
                st.session_state.pump_status = True
            elif irrigation_probability < 0.3:
                st.session_state.pump_status = False

        # Status visual da bomba
        if st.session_state.pump_status:
            st.success("🟢 BOMBA LIGADA")
            st.image(
                "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgdmlld0JveD0iMCAwIDEwMCAxMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHg9IjIwIiB5PSI0MCIgd2lkdGg9IjYwIiBoZWlnaHQ9IjIwIiBmaWxsPSIjNGZhZjUwIiBzdHJva2U9IiMzOThhMzQiIHN0cm9rZS13aWR0aD0iMiIvPgo8Y2lyY2xlIGN4PSI1MCIgY3k9IjUwIiByPSI4IiBmaWxsPSIjMzk4YTM0Ii8+CjxwYXRoIGQ9Ik00MCAyMEw2MCAyMEw2MCA0MEw0MCA0MFoiIGZpbGw9IiM0ZmFmNTAiIHN0cm9rZT0iIzM5OGEzNCIgc3Ryb2tlLXdpZHRoPSIyIi8+CjxwYXRoIGQ9Ik00MCA2MEw2MCA2MEw2MCA4MEw0MCA4MFoiIGZpbGw9IiM0ZmFmNTAiIHN0cm9rZT0iIzM5OGEzNCIgc3Ryb2tlLXdpZHRoPSIyIi8+Cjx0ZXh0IHg9IjUwIiB5PSI5NSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEyIiBmaWxsPSIjMzk4YTM0Ij5PTjwvdGV4dD4KPC9zdmc+",
                width=100)
        else:
            st.error("🔴 BOMBA DESLIGADA")
            st.image(
                "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgdmlld0JveD0iMCAwIDEwMCAxMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHg9IjIwIiB5PSI0MCIgd2lkdGg9IjYwIiBoZWlnaHQ9IjIwIiBmaWxsPSIjZjQ0MzM2IiBzdHJva2U9IiNkMzI1MmEiIHN0cm9rZS13aWR0aD0iMiIvPgo8Y2lyY2xlIGN4PSI1MCIgY3k9IjUwIiByPSI4IiBmaWxsPSIjZDMyNTJhIi8+CjxwYXRoIGQ9Ik00MCAyMEw2MCAyMEw2MCA0MEw0MCA0MFoiIGZpbGw9IiNmNDQzMzYiIHN0cm9rZT0iI2QzMjUyYSIgc3Ryb2tlLXdpZHRoPSIyIi8+CjxwYXRoIGQ9Ik00MCA2MEw2MCA2MEw2MCA4MEw0MCA4MFoiIGZpbGw9IiNmNDQzMzYiIHN0cm9rZT0iI2QzMjUyYSIgc3Ryb2tlLXdpZHRoPSIyIi8+Cjx0ZXh0IHg9IjUwIiB5PSI5NSIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEyIiBmaWxsPSIjZDMyNTJhIj5PRkY8L3RleHQ+Cjwvc3ZnPg==",
                width=100)

        st.subheader("🚨 Alertas")

        # Sistema de alertas
        alerts = []
        if current_data['humidity'] < humidity_threshold:
            alerts.append("⚠️ Umidade baixa!")
        if current_data['ph'] < ph_min or current_data['ph'] > ph_max:
            alerts.append("⚠️ pH fora do range!")
        if current_data['phosphorus'] < 15:
            alerts.append("⚠️ Fósforo baixo!")
        if current_data['potassium'] < 120:
            alerts.append("⚠️ Potássio baixo!")

        if alerts:
            for alert in alerts:
                st.warning(alert)
        else:
            st.success("✅ Todos os parâmetros normais")

        # Recomendações
        st.subheader("💡 Recomendações")

        recommendations = st.session_state.irrigation_model.get_recommendations(current_data)
        for rec in recommendations:
            st.info(rec)

    # Seção inferior - Histórico e Métricas
    st.markdown("---")

    col_hist1, col_hist2 = st.columns(2)

    with col_hist1:
        st.subheader("📋 Histórico de Ações")

        # Simular histórico de ações
        actions_data = {
            'Timestamp': pd.date_range(start=datetime.now() - timedelta(days=7),
                                       end=datetime.now(), freq='6H'),
            'Ação': np.random.choice(['Irrigação Iniciada', 'Irrigação Finalizada',
                                      'Alerta de pH', 'Alerta de Umidade'],
                                     size=len(pd.date_range(start=datetime.now() - timedelta(days=7),
                                                            end=datetime.now(), freq='6H'))),
            'Status': np.random.choice(['Sucesso', 'Alerta', 'Erro'],
                                       size=len(pd.date_range(start=datetime.now() - timedelta(days=7),
                                                              end=datetime.now(), freq='6H')),
                                       p=[0.7, 0.2, 0.1])
        }

        actions_df = pd.DataFrame(actions_data)
        st.dataframe(actions_df.tail(10), use_container_width=True)

    with col_hist2:
        st.subheader("📈 Métricas de Desempenho")

        # Métricas do sistema
        metrics_cols = st.columns(2)
        with metrics_cols[0]:
            st.metric("Economia de Água", "32%", delta="5%")
            st.metric("Eficiência do Sistema", "94.2%", delta="2.1%")

        with metrics_cols[1]:
            st.metric("Uptime", "99.7%", delta="0.1%")
            st.metric("Precisão do Modelo", "87.3%", delta="1.2%")

    # Auto-refresh
    if st.session_state.auto_mode:
        time.sleep(0.1)  # Pequeno delay para evitar travamento
        if (datetime.now() - st.session_state.last_update).seconds > 30:
            st.session_state.last_update = datetime.now()
            st.rerun()


if __name__ == "__main__":
    main()
