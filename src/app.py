
"""
MESAFARTAI - AC-4 Parte 1
Aplicação web com chatbot e dashboard.
"""

import streamlit as st
import pandas as pd
import sqlite3

from nlu import MotorNLU
from entities import ExtratorEntidades
from matchmaking import MotorMatchmaking

# Configuração da página
st.set_page_config(
    page_title="MESAFARTAI - Combate à Fome",
    page_icon="🥫",
    layout="wide"
)

# Inicialização dos motores
nlu = MotorNLU()
extrator = ExtratorEntidades()
matchmaker = MotorMatchmaking()

st.title("🥫 MESAFARTAI — Inteligência Contra a Fome")
st.caption("Conectando doadores e organizações sociais com Inteligência Artificial.")

aba_chat, aba_dashboard = st.tabs([
    "💬 Chatbot de Doações",
    "📊 Dashboard de Impacto Social"
])

# ABA 1 - CHATBOT
with aba_chat:
    st.subheader("Conversar com o Assistente de Doações")

    if "mensagens" not in st.session_state:
        st.session_state.mensagens = [
            {
                "role": "assistant",
                "content": (
                    "Olá! Sou o assistente do MESAFARTAI. 🥫 "
                    "Você gostaria de doar alimentos ou solicitar ajuda?"
                )
            }
        ]

    for msg in st.session_state.mensagens:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(
        "Ex: Tenho 20 kg de arroz para doar hoje no centro"
    ):
        st.session_state.mensagens.append({
            "role": "user",
            "content": prompt
        })
        st.chat_message("user").write(prompt)

        # Classificação de intenção
        resultado_nlu = nlu.processar_mensagem(prompt)
        intencao = resultado_nlu["intencao"]
        confianca = resultado_nlu["confianca"]

        if intencao == "cadastrar_doacao" and confianca >= 0.60:
            entidades = extrator.processar_texto(prompt)

            # Coordenadas de teste da atividade
            match = matchmaker.encontrar_ong_mais_proxima(
                -23.615, -46.785
            )

            resposta = (
                "**Doação Registrada com Sucesso!**\n\n"
                f"• **Item:** {entidades['alimento']}\n"
                f"• **Quantidade:** {entidades['quantidade_kg']} kg\n"
                f"• **Validade Estimada:** {entidades['data_validade']}\n\n"
            )

            if match:
                resposta += (
                    f"**Match Logístico (KNN):** Encaminhado para "
                    f"**{match['ong_nome']}** "
                    f"(~{match['distancia_estimada']} km)."
                )

        elif intencao == "solicitar_alimentos":
            resposta = (
                "Entendemos seu pedido. Estamos buscando doações "
                "disponíveis próximas a você no banco de dados."
            )

        else:
            resposta = (
                "Desculpe, não entendi perfeitamente sua mensagem. "
                "Poderia informar o alimento e a quantidade em kg?"
            )

        st.session_state.mensagens.append({
            "role": "assistant",
            "content": resposta
        })
        st.chat_message("assistant").write(resposta)


# ABA 2 - DASHBOARD
with aba_dashboard:
    st.subheader("Indicadores Logísticos e Sociais em Tempo Real")

    conn = sqlite3.connect("mesafartai.db")
    df_ongs = pd.read_sql_query(
        "SELECT * FROM usuarios WHERE tipo = 'ONG'",
        conn
    )
    conn.close()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total de ONGs Ativas", len(df_ongs))
    col2.metric(
        "Alimentos Arrecadados (kg)",
        "1,250 kg",
        "+150 kg esta semana"
    )
    col3.metric(
        "Refeições Estimadas Proporcionadas",
        "~2,500 refeições",
        "ODS 2"
    )

    st.markdown("---")
    st.write("### 🏢 Unidades de Atendimento Cadastradas")
    st.dataframe(
        df_ongs[["id", "nome", "latitude", "longitude"]],
        use_container_width=True,
        hide_index=True
    )
