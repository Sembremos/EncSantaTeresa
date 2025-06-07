import streamlit as st
import folium
from streamlit_folium import st_folium
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from PIL import Image
from datetime import datetime

# === SESIÓN ===
if "ubicacion" not in st.session_state:
    st.session_state.ubicacion = None
if "enviado" not in st.session_state:
    st.session_state.enviado = False

# === CONEXIÓN A GOOGLE SHEETS ===
def conectar_google_sheets():
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(
            "1xmQOqnUJUHhLEcBSDAbZX3wNGYmSe34ec8RWaxAUI10"
        ).sheet1
        return sheet
    except Exception:
        return None

# === ESTILOS Y BANNER ===
st.markdown("""
<style>
html, body, .stApp { background-color:#2C517A; color:#ffffff; font-weight:bold; }
h1,h2,h3 { color:#FAFEF3; }
.expander-title { background:#347A59; color:#fff; font-size:18px; font-weight:bold;
                 border-radius:10px; padding:15px 20px; margin-bottom:-20px; }
summary::marker { display:none; }
div[data-testid="stExpander"] > div { background:#fff; border:2px solid #ff4b4b;
                                     border-radius:12px; padding:10px; }
.stSelectbox > div, .stRadio > div, .stMultiSelect > div, .stTextArea > div {
    background:#51924b; border:2px solid #51924b; border-radius:10px;
    padding:10px; color:#2C517A !important;
}
.stButton > button { background:#DF912F; color:#fff; border:none; border-radius:10px;
                    padding:10px 24px; font-size:16px; }
.stButton > button:hover { background:#DF912F; color:white; }
label, .stMarkdown p { color:#fff !important; font-weight:600; }
@media only screen and (max-width:768px) {
    iframe { height:300px !important; max-height:300px !important; }
}
</style>
""", unsafe_allow_html=True)

banner = Image.open("baner.png")
st.markdown('<div class="banner-container">', unsafe_allow_html=True)
st.image(banner, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    """
**Con el objetivo de fortalecer la seguridad en nuestro entorno comercial...**
La información que nos suministras es confidencial y se emplea exclusivamente con el propósito de mejorar la seguridad.
    """,
    unsafe_allow_html=True
)

# === DATOS DEMOGRÁFICOS ===
st.markdown("<div class='expander-title'>Datos Demográficos</div>", unsafe_allow_html=True)
with st.expander("", expanded=False):
    distrito = st.selectbox("Distrito:", ["", "Santa Teresa"])
    if distrito == "Santa Teresa":
        barrio = st.selectbox(
            "Barrio:",
            ["Playa Carmen", "Santa Teresa", "Malpaís", "Manzanillo Bello Horizonte"]
        )
    else:
        barrio = ""
    edad = st.number_input("Edad:", min_value=12, max_value=120)
    sexo = st.selectbox(
        "Sexo:", ["", "Hombre", "Mujer", "LGBTQ+", "Otro / Prefiero No decirlo"]
    )

# === MAPA ===
st.markdown("### Seleccione su ubicación en el mapa:")
mapa = folium.Map(location=[9.6425, -85.1490], zoom_start=14)
if st.session_state.ubicacion:
    folium.Marker(
        location=st.session_state.ubicacion,
        tooltip="Ubicación seleccionada",
        icon=folium.Icon(color="blue", icon="map-marker")
    ).add_to(mapa)
click = st_folium(mapa, width=700, height=500)
if click and click.get("last_clicked"):
    st.session_state.ubicacion = [
        click["last_clicked"]["lat"], click["last_clicked"]["lng"]
    ]

# === PERCEPCIÓN DE SEGURIDAD ===
st.markdown("<div class='expander-title'>Percepción de Seguridad</div>", unsafe_allow_html=True)
with st.expander("", expanded=False):
    percepcion = st.radio(
        "¿Qué tan seguro(a) se siente?",
        ["Muy seguro(a)", "Seguro(a)", "Ni seguro(a)/Ni inseguro(a)", "Inseguro(a)", "Muy inseguro(a)"]
    )
    FIXED_FACTORES = [
        "Presencia de personas desconocidas o comportamientos inusuales",
        "Poca iluminación en la zona",
        "Escasa presencia policial",
        "Robos frecuentes",
        "Otro"
    ]
    ordered_fact = []
    if percepcion in ["Inseguro(a)", "Muy inseguro(a)"]:
        sel = st.multiselect("¿Por qué se siente inseguro(a)?", FIXED_FACTORES)
        if "Otro" in sel:
            otro = st.text_input("Especifique otro motivo", key="otro_inseg"); sel.append(f"Otro: {otro}")
        ordered_fact = [f for f in FIXED_FACTORES if f in sel] + [f for f in sel if f.startswith("Otro:")]

# === FACTORES SOCIALES ===
st.markdown("<div class='expander-title'>Factores de Riesgo Social</div>", unsafe_allow_html=True)
with st.expander("", expanded=False):
    factores_social = st.multiselect("Factores que afectan la seguridad:", [
        "Falta de oportunidades laborales","Problemas vecinales","Asentamientos ilegales",
        "Personas en situación de calle","Zona de prostitución","Consumo de alcohol",
        "Otro"
    ])

# === SITUACIONES RELACIONADAS A DELITOS ===
st.markdown("<div class='expander-title'>Situaciones Relacionadas a Delitos</div>", unsafe_allow_html=True)
with st.expander("", expanded=False):
    delitos_zona = st.multiselect("Delitos en la zona:", [
        "Disturbios en vía pública","Daños a la propiedad",
        "Intimidación con fines de lucro","Hurto","Receptación","Contrabando","Otro"
    ])
    robos = st.multiselect("Tipos de robos:", [
        "Tacha a comercio","Tacha a edificaciones","Tacha a vivienda",
        "Tacha de vehículos","Robo de vehículos"
    ])

# === VICTIMIZACIÓN Y CIERRE ===
if not st.session_state.enviado:
    if st.button("Enviar formulario"):
        errores = []
        if not st.session_state.ubicacion: errores.append("Ubicación en mapa")
        if not distrito:               errores.append("Distrito")
        if not sexo:                   errores.append("Sexo")
        if not percepcion:             errores.append("Percepción de seguridad")
        if errores:
            st.error("⚠️ Faltan campos: " + ", ".join(errores))
        else:
            lat, lon = st.session_state.ubicacion
            datos = [
                datetime.now().isoformat(), distrito, barrio, edad, sexo,
                f"https://www.google.com/maps?q={lat},{lon}", percepcion,
                ", ".join(ordered_fact),
                ", ".join(factores_social),
                ", ".join(delitos_zona),
                ", ".join(robos)
            ]
            sheet = conectar_google_sheets()
            if sheet:
                try:
                    sheet.append_row(datos)
                    st.session_state.enviado = True
                    st.success("✅ Formulario enviado correctamente")
                    if st.button("📝 Enviar otra respuesta"):
                        st.session_state.enviado = False
                        st.experimental_rerun()
                except Exception:
                    st.error("❌ Error al guardar. Intente de nuevo.")
else:
    st.info("Ya completaste la encuesta. ¡Gracias!")

st.markdown(
    "<p style='text-align:center;color:#88E145;font-size:10px'>Sembremos Seguridad - 2025</p>",
    unsafe_allow_html=True
)

