import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time

# ==========================================
# CONFIGURAÇÕES DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Guard IoT - Painel de Segurança",
    page_icon="🚨",
    layout="wide"
)

# ==========================================
# INTERFACE DO CABEÇALHO
# ==========================================
st.title("🚨 TCC: Guard IoT - Monitorização Industrial")
st.markdown("Painel de telemetria em tempo real. Dispositivo: **BitDogLab (Pico W)**")
st.markdown("---")

# ==========================================
# SIMULAÇÃO DE DADOS (Até termos a Base de Dados)
# ==========================================
# Para o TCC ficar impressionante, o Streamlit gera gráficos maravilhosos.
# Aqui criamos dados iniciais falsos só para a página não abrir vazia.
if 'historico' not in st.session_state:
    st.session_state['historico'] = pd.DataFrame(columns=["Hora", "Ruído (ADC)", "Status"])

# ==========================================
# LAYOUT DOS INDICADORES (Métricas)
# ==========================================
col1, col2, col3 = st.columns(3)

# Valores temporários de demonstração
ultimo_ruido = 1200
status_atual = "SEGURO"
cor_delta = "normal"

with col1:
    st.metric(label="Último Ruído Captado", value=f"{ultimo_ruido} ADC")
with col2:
    st.metric(label="Status do Ambiente", value=status_atual)
with col3:
    st.metric(label="Última Atualização", value=datetime.now().strftime("%H:%M:%S"))

st.markdown("---")

# ==========================================
# GRÁFICOS
# ==========================================
st.subheader("📊 Gráfico de Tendência (Histórico Recente)")

# Se houver dados no histórico, mostra o gráfico. Se não, mostra uma mensagem.
if not st.session_state['historico'].empty:
    fig = px.line(st.session_state['historico'], x="Hora", y="Ruído (ADC)", 
                  title="Variação de Ruído no Laboratório",
                  markers=True, line_shape='spline')
    # Linha vermelha mostrando o limite que configurámos no C/C++ (2500)
    fig.add_hline(y=2500, line_dash="dash", line_color="red", annotation_text="Limite de Risco (2500)")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("A aguardar os primeiros dados da BitDogLab...")

# ==========================================
# TABELA DE LOGS
# ==========================================
st.subheader("📋 Tabela de Registos (Logs)")
if not st.session_state['historico'].empty:
    st.dataframe(st.session_state['historico'], use_container_width=True)
else:
    st.write("Sem registos de alertas no momento.")

# ==========================================
# AUTO-REFRESH (Opcional)
# ==========================================
# Adiciona um botão no menu lateral para atualizar a página a cada X segundos
st.sidebar.title("Configurações")
if st.sidebar.button("Atualizar Painel 🔄"):
    st.rerun()