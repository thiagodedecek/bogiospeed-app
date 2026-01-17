import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# 1. CONFIGURAÇÃO DA PÁGINA (Título na aba do navegador)
st.set_page_config(page_title="BogioSpeed System", page_icon="🚚")

# 2. ESTILO VISUAL (Fundo Azul e Campos Brancos)
st.markdown("""
    <style>
    .stApp {
        background-color: #012e67; /* Azul BogioSpeed */
    }
    /* Estilo para todos os textos em branco */
    label, p, h1, h3, span, .stMarkdown {
        color: white !important;
    }
    /* Campos de entrada em branco com texto preto */
    input, select, textarea, div[data-baseweb="select"] > div {
        background-color: white !important;
        color: black !important;
        border-radius: 5px;
    }
    /* Ajuste para o texto dentro do seletor (dropdown) */
    div[data-testid="stMarkdownContainer"] p {
        color: white;
    }
    /* Botão de Salvar Amarelo para destaque */
    .stButton>button {
        background-color: #f1c40f;
        color: #012e67;
        font-weight: bold;
        border: None;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CONEXÃO COM A PLANILHA (Usando seus Secrets já salvos)
def conecta_planilha():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Aqui ele busca a chave que já está salva no seu Streamlit
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    # Abre a planilha pelo nome exato que você tem
    return client.open("Invoices BogioSpeed").worksheet("LANÇAMENTOS")

# 4. CABEÇALHO COM LOGO
# Se você subir o arquivo para o GitHub com o nome 'logo.png', ele aparece aqui
try:
    st.image("logo.png", width=350)
except:
    st.title("🚚 BOGIO SPEED")

st.markdown("### Inserimento Dati / Entrada de Dados")

# 5. LISTAS DE DADOS
lista_clientes = ["CASIT", "SOTRADE", "MAURICE WAND", "INVERAS", "OPTIMAL", "SANGALLI &", "INDUSTRY S", "CHIMICA CBR", "IL MUSEO IN ERBA ASSOCIAZIONE", "AMP", "SEVERINO ROBECCA", "M&H SOLAR", "SPEDIPRA SRL", "POWER X TECHNOLOGY", "GLOBAL AIR FREI", "T.S.T.", "GLOBAL AIR FREIGHT", "M&M", "2F TRANSPORTI", "D.P.S S.R.L", "ETC ULUSLARARASI TICARET VE DANISMANLIK LTD STI", "CARGILL SRL", "OLYMPUS SPORT AG", "DUCATI ENERGIA SPA", "ERREESSEE SRL", "STOPNOISE ENGINEERING", "OTTO'S AG", "KURT RYSLEY", "TECHNOFORM BAUTEC ITALA SPA", "COMPAGNA TECNICA MOTORI SPA", "SELTE SPA", "INTERBOX SA", "ETNA CARGO ROMANIA SRL", "RALUX SOLAR RACKING SYSTEM SRL", "ADVANCED DISTRIBUTION SPA", "L2 LEONI SRL", "DAVENIA TRADE S.E", "MAGSED AG", "BISELLO TECNOLOGY SYSTEM SRL", "Altro / Outro"]
lista_fornecedores = ["NOU TRANSPORT", "ALA", "SANARE/TEAM FOT", "CARO", "SOGEDIM", "LIGENTIA", "GIOBBIO SRL", "MOVEST", "NOSTA", "BOXLINE", "CONTESSA", "SPEEDY TRUCK", "JANINIA", "CONTESSI / SPEEDY", "SPEEDY, CONTE", "SPEEDY TROCK", "KONTISPED", "EVOLOG", "RONZIO", "TRANSMEC GROUP", "SPEDIPRA", "STANTE", "CASNATE-GRANDATE", "DESTINY PARZ", "TB LOG", "DRZYZGA", "COMBI LINE", "VAREDO", "TIREX", "DOGANALI", "RAOTRANS", "GABRIEL TRANSPORT", "GIORGIO OBRIZZI", "IN TIME EXPRESS", "CARBOX TARROS GRUP", "PTO LOGISTIC SOLUTIONS", "OP-SA LOGISTIKA D.O.O.", "RIGOTTO", "PORTUGALENCE", "NOLO RAOTRANS", "FOX LOGISTICS SA", "NARDO LOGISTICS Sp. zo.o.", "KONSOLIDA", "AUBERTRANS", "BERGWERFF", "MAGNUS LOGISTICS", "Altro / Outro"]

# 6. FORMULÁRIO
with st.form("form_bogio", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        nota = st.text_input("Numero della nota / Nº Nota")
        data_n = st.date_input("Data della nota / Data Nota")
        cliente = st.selectbox("Cliente", lista_clientes)
        placa = st.text_input("Plates Nº / Targa / Placa")
        
    with col2:
        fornecedor = st.selectbox("Fornitore / Fornecedor", lista_fornecedores)
        v_frete = st.number_input("Valore Frete (Entrada)", min_value=0.0, format="%.2f")
        f_contratado = st.number_input("Costo Frete (Saída)", min_value=0.0, format="%.2f")
        invoice = st.text_input("Numero Invoice")

    btn_salvar = st.form_submit_button("REGISTRA / SALVAR")

if btn_salvar:
    try:
        aba = conecta_planilha()
        lucro = v_frete - f_contratado
        # Linha para a planilha: Nota, Data, Cliente, Tipo, Fornecedor, Entrada, Saída, Lucro, Vazio, Invoice, Placa
        nova_linha = [nota, str(data_n), cliente, "Rodoviário", fornecedor, v_frete, f_contratado, lucro, "", invoice, placa]
        aba.append_row(nova_linha)
        st.success("✅ Salvato! Verifique sua planilha Google.")
    except Exception as e:
        st.error(f"Erro de Conexão: Verifique se a planilha foi compartilhada com o e-mail do JSON. Detalhe: {e}")
