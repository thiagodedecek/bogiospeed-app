import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime

# Configurações da Página
st.set_page_config(page_title="BogioSpeed - Gestione Trasporti", page_icon="🚚", layout="centered")

# Estilo Personalizado para ficar com o "Layout Bonito"
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("🚚 BogioSpeed - Sistema de Invoices")
st.subheader("Inserimento Dati / Entrada de Dados")

# --- CONEXÃO COM GOOGLE SHEETS ---
# No Streamlit, as credenciais são colocadas em "Secrets"
def conecta_planilha():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    return client.open("Invoices BogioSpeed").worksheet("LANÇAMENTOS")

# --- LISTAS ---
lista_clientes = ["CASIT", "SOTRADE", "MAURICE WAND", "INVERAS", "OPTIMAL", "SANGALLI &", "INDUSTRY S", "CHIMICA CBR", "IL MUSEO IN ERBA ASSOCIAZIONE", "AMP", "SEVERINO ROBECCA", "M&H SOLAR", "SPEDIPRA SRL", "POWER X TECHNOLOGY", "GLOBAL AIR FREI", "T.S.T.", "GLOBAL AIR FREIGHT", "M&M", "2F TRANSPORTI", "D.P.S S.R.L", "ETC ULUSLARARASI TICARET VE DANISMANLIK LTD STI", "CARGILL SRL", "OLYMPUS SPORT AG", "DUCATI ENERGIA SPA", "ERREESSEE SRL", "STOPNOISE ENGINEERING", "OTTO'S AG", "KURT RYSLEY", "TECHNOFORM BAUTEC ITALA SPA", "COMPAGNA TECNICA MOTORI SPA", "SELTE SPA", "INTERBOX SA", "ETNA CARGO ROMANIA SRL", "RALUX SOLAR RACKING SYSTEM SRL", "ADVANCED DISTRIBUTION SPA", "L2 LEONI SRL", "DAVENIA TRADE S.E", "MAGSED AG", "BISELLO TECNOLOGY SYSTEM SRL", "Altro / Outro"]
lista_fornecedores = ["NOU TRANSPORT", "ALA", "SANARE/TEAM FOT", "CARO", "SOGEDIM", "LIGENTIA", "GIOBBIO SRL", "MOVEST", "NOSTA", "BOXLINE", "CONTESSA", "SPEEDY TRUCK", "JANINIA", "CONTESSI / SPEEDY", "SPEEDY, CONTE", "SPEEDY TROCK", "KONTISPED", "EVOLOG", "RONZIO", "TRANSMEC GROUP", "SPEDIPRA", "STANTE", "CASNATE-GRANDATE", "DESTINY PARZ", "TB LOG", "DRZYZGA", "COMBI LINE", "VAREDO", "TIREX", "DOGANALI", "RAOTRANS", "GABRIEL TRANSPORT", "GIORGIO OBRIZZI", "IN TIME EXPRESS", "CARBOX TARROS GRUP", "PTO LOGISTIC SOLUTIONS", "OP-SA LOGISTIKA D.O.O.", "RIGOTTO", "PORTUGALENCE", "NOLO RAOTRANS", "FOX LOGISTICS SA", "NARDO LOGISTICS Sp. zo.o.", "KONSOLIDA", "AUBERTRANS", "BERGWERFF", "MAGNUS LOGISTICS", "Altro / Outro"]

# --- FORMULÁRIO ---
with st.form("form_frete", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        num_nota = st.text_input("Numero della nota / Nº Nota")
        data_n = st.date_input("Data della nota / Data Nota")
        cliente = st.selectbox("Cliente", lista_clientes)
        cli_novo = st.text_input("Se 'Altro', nome do Cliente")
        placa = st.text_input("Plates Nº / Placa")

    with col2:
        fornecedor = st.selectbox("Fornitore / Fornecedor", lista_fornecedores)
        forn_novo = st.text_input("Se 'Altro', nome do Fornecedor")
        v_frete = st.number_input("Valore Frete (Entrada)", min_value=0.0, format="%.2f")
        f_contratado = st.number_input("Costo Frete (Saída)", min_value=0.0, format="%.2f")
        data_e = st.date_input("Esecuzione / Execução")
        invoice = st.text_input("Numero della fattura / Invoice")

    lucro = v_frete - f_contratado
    st.metric("Utile Stimato / Lucro Estimado", f"€ {lucro:.2f}")

    btn_enviar = st.form_submit_button("REGISTRA DATI / REGISTRAR DADOS")

if btn_enviar:
    try:
        ws = conecta_planilha()
        cli_final = cli_novo if cliente == "Altro / Outro" else cliente
        forn_final = forn_novo if fornecedor == "Altro / Outro" else fornecedor
        
        linha = [num_nota, str(data_n), cli_final, "Rodoviário", forn_final, 
                 v_frete, f_contratado, lucro, str(data_e), invoice, placa]
        
        ws.append_row(linha)
        st.success("✅ Registrato con successo! / Registrado com sucesso!")
    except Exception as e:
        st.error(f"Errore / Erro: {e}")
