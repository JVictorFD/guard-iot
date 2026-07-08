import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# ==========================================
# 1. CONFIGURAÇÕES DO SUPABASE (A PONTE)
# ==========================================
# Substitua com os dados exatos da tela do Supabase que você me enviou:
SUPABASE_URL = "https://egymsmfiadgnfjllrsha.supabase.co" # Ex: https://xyz123.supabase.co
SUPABASE_KEY = "sb_publishable_woAi3LU260U19LWruaAopQ_zkWXJCpb"

st.set_page_config(page_title="Guard IoT", page_icon="🚨", layout="wide")
st.title("🚨 TCC: Guard IoT - Monitorização Industrial")
st.markdown("Painel de telemetria em tempo real lendo diretamente do **Supabase**.")
st.markdown("---")

# ==========================================
# 2. FUNÇÃO PARA LER O BANCO DE DADOS
# ==========================================
def buscar_dados():
    # URL da API REST do Supabase apontando para a sua tabela 'alertas_ruido'
    url = f"{SUPABASE_URL}/rest/v1/alertas_ruido?select=*"
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    
    try:
        resposta = requests.get(url, headers=headers)
        if resposta.status_code == 200:
            dados = resposta.json()
            if dados: # Se a tabela não estiver vazia
                df = pd.DataFrame(dados)
                # Converte a coluna de data para o formato correto do Pandas
                df['created_at'] = pd.to_datetime(df['created_at'])
                return df
    except Exception as e:
        st.error(f"Erro ao conectar com o Supabase: {e}")
        
    return pd.DataFrame()

# ==========================================
# 3. INTERFACE E GRÁFICOS
# ==========================================
df_historico = buscar_dados()

if not df_historico.empty:
    # Pega a última linha da tabela (o alerta mais recente)
    ultimo_registro = df_historico.iloc[-1]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Último Ruído Captado", value=f"{ultimo_registro['nivel_ruido']} ADC")
    with col2:
        st.metric(label="Status do Ambiente", value=ultimo_registro['status'])
    with col3:
        hora_formatada = ultimo_registro['created_at'].strftime("%H:%M:%S")
        st.metric(label="Hora do Alerta", value=hora_formatada)

    st.markdown("---")
    
    # Gráfico
    st.subheader("📊 Histórico de Alertas")
    fig = px.line(df_historico, x="created_at", y="nivel_ruido", 
                  title="Variação de Ruído no Laboratório",
                  markers=True, line_shape='spline')
    fig.add_hline(y=2500, line_dash="dash", line_color="red", annotation_text="Limite de Risco (2500)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela Bruta
    st.subheader("📋 Tabela de Logs Brutos")
    st.dataframe(df_historico[['created_at', 'dispositivo', 'nivel_ruido', 'status']].sort_values(by="created_at", ascending=False), use_container_width=True)
    
else:
    st.info("O Banco de Dados está vazio. Aguardando os primeiros alertas da BitDogLab...")

# Menu lateral para atualizar
st.sidebar.title("Comandos")
if st.sidebar.button("Buscar Novos Dados 🔄"):
    st.rerun()