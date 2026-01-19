import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# --- 1. CONFIGURAÇÃO VISUAL E IDENTIDADE ---
st.set_page_config(page_title="BogioSpeed System v2.3", page_icon="🚚", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #012e67; }
    label, p, h1, h3, span, .stMarkdown { color: white !important; }
    input, select, textarea, div[data-baseweb="select"] > div {
        background-color: white !important;
        color: black !important;
    }
    .stButton>button {
        background-color: #f1c40f;
        color: #012e67;
        font-weight: bold;
        width: 100%;
        height: 3em;
        border-radius: 10px;
    }
    hr { border-top: 1px solid #f1c40f !important; }
    </style>
    """, unsafe_allow_html=True)

# Exibição da Logo Oficial
try:
    st.image("logo.png", width=450)
except:
    st.title("🚚 BOGIO SPEED SYSTEM")

# --- 2. CONEXÃO SEGURA ---
def conecta_planilha():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = st.secrets["gcp_service_account"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    return client.open("Invoices BogioSpeed")

# --- 3. LISTAS DE DADOS ---
lista_clientes = ["CASIT", "SOTRADE", "MAURICE WAND", "INVERAS", "OPTIMAL", "SANGALLI &", "INDUSTRY S", "CHIMICA CBR", "IL MUSEO IN ERBA ASSOCIAZIONE", "AMP", "SEVERINO ROBECCA", "M&H SOLAR", "SPEDIPRA SRL", "POWER X TECHNOLOGY", "GLOBAL AIR FREI", "T.S.T.", "GLOBAL AIR FREIGHT", "M&M", "2F TRANSPORTI", "D.P.S S.R.L", "ETC ULUSLARARASI TICARET VE DANISMANLIK LTD STI", "CARGILL SRL", "OLYMPUS SPORT AG", "DUCATI ENERGIA SPA", "ERREESSEE SRL", "STOPNOISE ENGINEERING", "OTTO'S AG", "KURT RYSLEY", "TECHNOFORM BAUTEC ITALA SPA", "COMPAGNA TECNICA MOTORI SPA", "SELTE SPA", "INTERBOX SA", "ETNA CARGO ROMANIA SRL", "RALUX SOLAR RACKING SYSTEM SRL", "ADVANCED DISTRIBUTION SPA", "L2 LEONI SRL", "DAVENIA TRADE S.E", "MAGSED AG", "BISELLO TECNOLOGY SYSTEM SRL", "Altro / Outro"]
lista_fornecedores = ["Nessuno / Nenhum", "NOU TRANSPORT", "ALA", "SANARE/TEAM FOT", "CARO", "SOGEDIM", "LIGENTIA", "GIOBBIO SRL", "MOVEST", "NOSTA", "BOXLINE", "CONTESSA", "SPEEDY TRUCK", "JANINIA", "CONTESSI / SPEEDY", "SPEEDY, CONTE", "SPEEDY TROCK", "KONTISPED", "EVOLOG", "RONZIO", "TRANSMEC GROUP", "SPEDIPRA", "STANTE", "CASNATE-GRANDATE", "DESTINY PARZ", "TB LOG", "DRZYZGA", "COMBI LINE", "VAREDO", "TIREX", "DOGANALI", "RAOTRANS", "GABRIEL TRANSPORT", "GIORGIO OBRIZZI", "IN TIME EXPRESS", "CARBOX TARROS GRUP", "PTO LOGISTIC SOLUTIONS", "OP-SA LOGISTIKA D.O.O.", "RIGOTTO", "PORTUGALENCE", "NOLO RAOTRANS", "FOX LOGISTICS SA", "NARDO LOGISTICS Sp. zo.o.", "KONSOLIDA", "AUBERTRANS", "BERGWERFF", "MAGNUS LOGISTICS", "Altro / Outro"]

# --- 4. FORMULÁRIO (PROTEGIDO CONTRA ENVIO POR ENTER) ---
with st.form("form_bogio_v23", clear_on_submit=True):
    st.markdown("### 📝 Informazioni Generali")
    col1, col2 = st.columns(2)
    with col1:
        job_no = st.text_input("JOB Nº / Numero della nota")
        data_nota = st.date_input("DATE / Data della nota")
        cliente_sel = st.selectbox("CUSTOMER / Cliente", lista_clientes)
        cliente_novo = st.text_input("Se 'Altro', nome del cliente")
    with col2:
        kind_serv = st.text_input("KIND OF SERVICE", value="Rodoviário")
        data_closed = st.date_input("JOB CLOSED / Data Esecuzione")
        plate_no = st.text_input("PLATE Nº / Targa / Placa")

    st.markdown("---")
    
    # Seção Fornecedores
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.markdown("#### 🚚 Fornitore I")
        f1_sel = st.selectbox("Supplier I", lista_fornecedores[1:])
        f1_novo = st.text_input("Se 'Altro', nome Fornitore I")
        f1_custo = st.number_input("BUYER I (Custo I)", min_value=0.0, format="%.2f")
        f1_inv = st.text_input("INVOICE Nº I")
        
    with col_f2:
        st.markdown("#### 🚚 Fornitore II (Opzionale)")
        f2_sel = st.selectbox("Supplier II", lista_fornecedores)
        f2_novo = st.text_input("Se 'Altro', nome Fornitore II")
        f2_custo = st.number_input("BUYER II (Custo II)", min_value=0.0, format="%.2f")
        f2_inv = st.text_input("INVOICE Nº II")

    st.markdown("---")
    
    st.markdown("### 💰 Valori / Valores")
    sold_total = st.number_input("SOLD / Valore Frete TOTAL", min_value=0.0, format="%.2f")

    # BOTÃO DE ENVIO: Única forma de enviar os dados
    btn_salvar = st.form_submit_button("REGISTRA / SALVAR")

# --- 5. PROCESSAMENTO E ENVIO PARA GOOGLE SHEETS ---
if btn_salvar:
    try:
        # Tratamento de Nomes "Altro"
        final_customer = cliente_novo if cliente_sel == "Altro / Outro" else cliente_sel
        final_supp1 = f1_novo if f1_sel == "Altro / Outro" else f1_sel
        final_supp2 = ""
        if f2_sel != "Nessuno / Nenhum":
            final_supp2 = f2_novo if f2_sel == "Altro / Outro" else f2_sel
        
        # Cálculo do Lucro (PROFIT)
        profit = sold_total - f1_custo - f2_custo

        # Conectar e localizar aba
        sh = conecta_planilha()
        worksheets = [ws.title for ws in sh.worksheets()]
        target_ws = next((name for name in worksheets if name.upper() == "LANÇAMENTOS"), None)
        planilha = sh.worksheet(target_ws) if target_ws else sh.get_worksheet(0)

        # Montagem da Linha conforme sua imagem (A até N)
        nova_linha = [
            job_no, str(data_nota), final_customer, kind_serv, 
            final_supp1, final_supp2, sold_total, f1_custo, 
            f2_custo, profit, str(data_closed), f1_inv, 
            f2_inv, plate_no
        ]

        planilha.append_row(nova_linha)
        st.success(f"✅ REGISTRATO! Profit: {profit:.2f}")
    except Exception as e:
        st.error(f"❌ ERRO: {e}")
