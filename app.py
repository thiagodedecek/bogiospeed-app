import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# --- 1. CONFIGURAÇÃO VISUAL (Fundo Azul e Logo) ---
st.set_page_config(page_title="BogioSpeed v2.1", page_icon="🚚")

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
    }
    </style>
    """, unsafe_allow_html=True)

# Exibição da Logo
try:
    st.image("logo.png", width=400)
except:
    st.title("🚚 BogioSpeed v2.1")

# --- 2. CONEXÃO (Lógica do Colab adaptada para Site) ---
def conecta_planilha():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Aqui usamos a Service Account que você configurou nos Secrets
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    return client.open("Invoices BogioSpeed")

# --- 3. LISTAS (Exatamente como no seu Colab) ---
lista_clientes = ["CASIT", "SOTRADE", "MAURICE WAND", "INVERAS", "OPTIMAL", "SANGALLI &", "INDUSTRY S", "CHIMICA CBR", "IL MUSEO IN ERBA ASSOCIAZIONE", "AMP", "SEVERINO ROBECCA", "M&H SOLAR", "SPEDIPRA SRL", "POWER X TECHNOLOGY", "GLOBAL AIR FREI", "T.S.T.", "GLOBAL AIR FREIGHT", "M&M", "2F TRANSPORTI", "D.P.S S.R.L", "ETC ULUSLARARASI TICARET VE DANISMANLIK LTD STI", "CARGILL SRL", "OLYMPUS SPORT AG", "DUCATI ENERGIA SPA", "ERREESSEE SRL", "STOPNOISE ENGINEERING", "OTTO'S AG", "KURT RYSLEY", "TECHNOFORM BAUTEC ITALA SPA", "COMPAGNA TECNICA MOTORI SPA", "SELTE SPA", "INTERBOX SA", "ETNA CARGO ROMANIA SRL", "RALUX SOLAR RACKING SYSTEM SRL", "ADVANCED DISTRIBUTION SPA", "L2 LEONI SRL", "DAVENIA TRADE S.E", "MAGSED AG", "BISELLO TECNOLOGY SYSTEM SRL", "Altro / Outro"]
lista_fornecedores = ["NOU TRANSPORT", "ALA", "SANARE/TEAM FOT", "CARO", "SOGEDIM", "LIGENTIA", "GIOBBIO SRL", "MOVEST", "NOSTA", "BOXLINE", "CONTESSA", "SPEEDY TRUCK", "JANINIA", "CONTESSI / SPEEDY", "SPEEDY, CONTE", "SPEEDY TROCK", "KONTISPED", "EVOLOG", "RONZIO", "TRANSMEC GROUP", "SPEDIPRA", "STANTE", "CASNATE-GRANDATE", "DESTINY PARZ", "TB LOG", "DRZYZGA", "COMBI LINE", "VAREDO", "TIREX", "DOGANALI", "RAOTRANS", "GABRIEL TRANSPORT", "GIORGIO OBRIZZI", "IN TIME EXPRESS", "CARBOX TARROS GRUP", "PTO LOGISTIC SOLUTIONS", "OP-SA LOGISTIKA D.O.O.", "RIGOTTO", "PORTUGALENCE", "NOLO RAOTRANS", "FOX LOGISTICS SA", "NARDO LOGISTICS Sp. zo.o.", "KONSOLIDA", "AUBERTRANS", "BERGWERFF", "MAGNUS LOGISTICS", "Altro / Outro"]

# --- 4. CAMPOS DO FORMULÁRIO (Interface do Streamlit) ---
st.markdown("### 📝 Informazioni Generali / Informações Gerais")

with st.form("form_v21", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        numero_nota = st.text_input("Numero della nota / Nº Nota")
        data_nota = st.date_input("Data della nota / Data Nota")
        cliente_selecionado = st.selectbox("Cliente", lista_clientes)
        cliente_novo = st.text_input("Se 'Altro', nome del cliente")
    
    with col2:
        fornecedor_selecionado = st.selectbox("Fornitore / Fornecedor", lista_fornecedores)
        fornecedor_novo = st.text_input("Se 'Altro', nome del fornitore")
        placa_veiculo = st.text_input("Plates Nº / Targa / Placa")

    st.markdown("### 💰 Valori e Finanze / Valores e Finanças")
    col3, col4 = st.columns(2)
    with col3:
        valor_frete = st.number_input("Valore Frete (Entrada)", min_value=0.0, format="%.2f")
    with col4:
        frete_contratado = st.number_input("Costo Frete (Saída)", min_value=0.0, format="%.2f")

    st.markdown("### 📂 Esecução")
    col5, col6 = st.columns(2)
    with col5:
        data_execucao = st.date_input("Data Esecuzione / Execução")
    with col6:
        numero_invoice = st.text_input("Numero Invoice")

    # Botão de Enviar
    enviar_agora = st.form_submit_button("REGISTRA / SALVAR")

# --- 5. LÓGICA DE ENVIO (Igual ao seu Colab) ---
if enviar_agora:
    final_cliente = cliente_novo if cliente_selecionado == "Altro / Outro" else cliente_selecionado
    final_fornecedor = fornecedor_novo if fornecedor_selecionado == "Altro / Outro" else fornecedor_selecionado
    lucro = valor_frete - frete_contratado

    try:
        sh = conecta_planilha()
        # Lógica de busca de aba flexível que você criou
        worksheets = [ws.title for ws in sh.worksheets()]
        target_ws = next((name for name in worksheets if name.upper() == "LANÇAMENTOS"), None)

        if not target_ws:
            planilha = sh.get_worksheet(len(worksheets)-1)
        else:
            planilha = sh.worksheet(target_ws)

        nova_linha = [numero_nota, str(data_nota), final_cliente, "Rodoviário",
                      final_fornecedor, valor_frete, frete_contratado,
                      lucro, str(data_execucao), numero_invoice, placa_veiculo]

        planilha.append_row(nova_linha)
        st.success(f"✅ REGISTRATO! (Tab: {planilha.title})")
    except Exception as e:
        st.error(f"❌ ERRO: {e}")
