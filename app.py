import streamlit as st
import pandas as pd
from datetime import datetime
import folium
from streamlit_folium import st_folium
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from PIL import Image

# === PARTE 0: CONFIGURACIÓN INICIAL Y SESIÓN ===
if "ubicacion" not in st.session_state:
    st.session_state.ubicacion = None
if "enviado" not in st.session_state:
    st.session_state.enviado = False

# Valores por defecto para variables de preguntas retiradas
escolaridad = ""
tipo_local = ""
falta_de_inversion = []
consumo_drogas = []
bunker = []
venta_drogas = []
delitos_vida = []
estafas = []
observacion_control = ""
descripcion_control = []
exigencia_cuota = ""
descripcion_cuota = ""

# === PARTE 1: IMPORTACIONES Y CONEXIÓN A GOOGLE SHEETS ===
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

# === PARTE 2: ESTILOS Y BANNER ===
st.markdown("""
    <style>
    html, body, .stApp {
        color-scheme: light !important;
        background-color: #2C517A !important;
        color: #ffffff !important;
        font-weight: bold !important;
    }
    h1, h2, h3 { color: #FAFEF3; }
    .expander-title { background-color: #347A59; color: #ffffff; font-size:18px;
                      font-weight:bold; border-radius:10px; padding:15px 20px;
                      margin-bottom:-20px; text-align:left; }
    summary::marker { display:none; }
    div[data-testid="stExpander"] > div {
        background-color:#ffffff; border:2px solid #ff4b4b;
        border-radius:12px; padding:10px;
    }
    .stSelectbox > div, .stRadio > div, .stMultiSelect > div, .stTextArea > div {
        background-color:#51924b; border:2px solid #51924b;
        border-radius:10px; padding:10px; color:#2C517A !important;
    }
    .stButton > button {
        background-color:#DF912F; color:#ffffff; border:none;
        border-radius:10px; padding:10px 24px; font-size:16px;
    }
    .stButton > button:hover { background-color:#DF912F; color:white; }
    div[role="radiogroup"] label[data-selected="true"],
    div[role="listbox"] div[data-selected="true"] {
        color:#ffffff !important; border-radius:8px !important; font-weight:bold !important;
    }
    div[role="radiogroup"] label[data-selected="true"]::after,
    div[role="listbox"] div[data-selected="true"]::after {
        content:" ✅"; margin-left:6px;
    }
    label, .stMarkdown p { color:#ffffff !important; font-weight:600; }
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
**Con el objetivo de fortalecer la seguridad en nuestro entorno comercial, nos enfocamos en abordar las principales preocupaciones de seguridad.**
La información que nos suministras es completamente confidencial y se emplea exclusivamente con el propósito de mejorar la seguridad en nuestra área comercial.
""", unsafe_allow_html=True)

# === PARTE 3: DATOS DEMOGRÁFICOS Y MAPA ===
st.markdown("<div class='expander-title'>Datos Demográficos</div>", unsafe_allow_html=True)
with st.expander("", expanded=False):
    distrito = st.selectbox("Distrito:", ["", "Santa Teresa"])
    if distrito == "Santa Teresa":
        barrio = st.selectbox("Barrio", [
            "Playa Carmen", "Santa Teresa", "Malpaís", "Manzanillo Bello Horizonte"
        ])
    else:
        barrio = ""
    edad = st.number_input("Edad:", min_value=12, max_value=120, format="%d")
    sexo = st.selectbox("Sexo:", ["","Hombre","Mujer","LGBTQ+","Otro / Prefiero No decirlo"])

st.markdown("### Seleccione su ubicación en el mapa:")
mapa = folium.Map(location=[9.6425, -85.1490], zoom_start=14)
if st.session_state.ubicacion:
    folium.Marker(
        location=st.session_state.ubicacion,
        tooltip="Ubicación seleccionada",
        icon=folium.Icon(color="blue", icon="map-marker")
    ).add_to(mapa)
map_click = st_folium(mapa, width=700, height=500)
if map_click and map_click.get("last_clicked"):
    st.session_state.ubicacion = [
        map_click["last_clicked"]["lat"],
        map_click["last_clicked"]["lng"]
    ]

# === PARTE 4: PERCEPCIÓN DE SEGURIDAD ===
st.markdown("<div class='expander-title'>Percepción de Seguridad</div>", unsafe_allow_html=True)
with st.expander("", expanded=False):
    percepcion_seguridad = st.radio(
        "¿Qué tan seguro(a) se siente en esta zona?",
        ["Muy seguro(a)","Seguro(a)","Ni seguro(a) Ni inseguro(a)","Inseguro(a)","Muy inseguro(a)"]
    )
    st.caption("Nota: respuesta de selección única.")

    FIXED_FACTORES = [
        "Presencia de personas desconocidas o comportamientos inusuales",
        "Poca iluminación en la zona",
        "Escasa presencia policial",
        "Robos frecuentes",
        "Consumo de sustancias en la vía pública",
        "Horarios considerados peligrosos (Entre las 6:00pm y las 5:00am)",
        "Disturbios o riñas cercanas",
        "Otro"
    ]
    ordered_factores = []
    if percepcion_seguridad in ["Inseguro(a)", "Muy inseguro(a)"]:
        seleccion = st.multiselect("¿Por qué se siente inseguro(a)?", FIXED_FACTORES)
        if "Otro" in seleccion:
            otro_text = st.text_input("Especifique otro motivo", key="otro_inseguridad")
            if otro_text:
                seleccion.append(f"Otro: {otro_text}")
        ordered_factores = [f for f in FIXED_FACTORES if f in seleccion]
        otros_extra = [f for f in seleccion if f.startswith("Otro:")]
        if otros_extra:
            ordered_factores += otros_extra

# === PARTE 5: FACTORES DE RIESGO SOCIAL ===
st.markdown("<div class='expander-title'>Factores de Riesgo Social</div>", unsafe_allow_html=True)
with st.expander("", expanded=False):
    factores_sociales = st.multiselect(
        "¿Cuáles de los siguientes factores afectan la seguridad en su zona comercial?", [
            "Falta de oportunidades laborales","Problemas vecinales","Asentamientos ilegales",
            "Personas en situación de calle","Zona de prostitución","Consumo de alcohol en vía pública",
            "Personas con exceso de tiempo de ocio","Cuarterías","Lotes baldíos","Ventas informales",
            "Pérdida de espacios públicos","Otro"
        ]
    )
    # Las demás variables ya tienen valores por defecto si no se completan

# === PARTE 6: SITUACIONES RELACIONADAS A DELITOS ===
st.markdown("<div class='expander-title'>Situaciones Relacionadas a Delitos</div>", unsafe_allow_html=True)
with st.expander("", expanded=False):
    delitos_zona = st.multiselect(
        "¿Seleccine los delitos que considere que ocurren en la zona?", [
            "Disturbios en vía pública","Daños a la propiedad","Intimidación o amenazas con fines de lucro","Estafas",
            "Hurto(Sustracción de artículos mediante el descuido)","Receptación","Contrabando","Venta de droga"
        ]
    )
    delitos_sexuales = st.multiselect(
        "¿Qué delitos sexuales ha percibido que existen en la zona?", [
            "Abuso sexual","Acoso sexual","Violación"
        ]
    )
    asaltos = st.multiselect(
        "¿Qué tipos de asaltos hay en la zona?", [
            "Asalto a personas","Asalto a comercio","Asalto a vivienda","Asalto a transporte público"
        ]
    )
    robos = st.multiselect(
        "¿Qué tipos de robos ha identificado?", [
            "Tacha a comercio","Tacha a edificaciones","Tacha a vivienda",
            "Tacha de vehículos","Robo de vehículos"
        ]
    )

# === PARTE 7: INFORMACIÓN ADICIONAL Y VICTIMIZACIÓN ===
st.markdown("<div class='expander-title'>Información Adicional</div>", unsafe_allow_html=True)
with st.expander("", expanded=False):
    victima = st.radio(
        "¿Usted ha sido víctima de algún delito en los últimos 12 meses?",[
            "Sí, y presenté la denuncia","Sí, pero no presenté la denuncia","No","Prefiero no responder"
        ]
    )
    motivo_no_denuncia = []
    tipo_delito = []
    horario_delito = ""
    modo_operar = []
    if victima == "Sí, pero no presenté la denuncia":
        motivo_no_denuncia = st.multiselect(
            "¿Por qué no denunció?", [
                "Distancia","Miedo a represalias","Falta de respuesta","Experiencias previas fallidas",
                "Complejidad al denunciar","Desconocimiento de dónde denunciar","Consejo policial","Falta de tiempo"
            ]
        )
    elif victima in ["Sí, y presenté la denuncia","Sí, pero no presenté la denuncia"]:
        tipo_delito = st.multiselect(
            "¿Cuál fue el delito?", [
                "Hurto","Asalto","Cobro por protección","Estafa","Daños a la propiedad",
                "Venta o consumo de drogas","Amenazas","Cobros periódicos","Otro"
            ]
        )
    if victima in ["Sí, y presenté la denuncia","Sí, pero no presenté la denuncia"]:
        horario_delito = st.selectbox(
            "¿Conoce el horario en el que ocurrió el hecho?", [
                "","00:00-02:59","03:00-05:59","06:00-08:59","09:00-11:59",
                "12:00-14:59","15:00-17:59","18:00-20:59","21:00-23:59","Desconocido"
            ]
        )
        modo_operar = st.multiselect(
            "¿Cómo operaban los responsables?", [
                "Arma blanca","Arma de fuego","Amenazas","Cobros/cuotas","Arrebato",
                "Boquete","Ganzúa","Engaño","No sé","Otro"
            ]
        )
    opinion_fp = st.radio("¿Cómo califica el servicio policial?", ["Excelente","Bueno","Regular","Mala","Muy mala"]);
    cambio_servicio = st.radio("¿Ha cambiado el servicio en 12 meses?", ["Ha mejorado mucho","Ha mejorado","Igual","Ha empeorado","Ha empeorado mucho"]);
    conocimiento_policias = st.radio("¿Conoce policías que patrullan su zona?", ["Sí","No"]);
    participacion_programa = st.radio("¿Conoce/participa en Programa de Seguridad Comercial?", [
        "No lo conozco","Lo conozco, pero no participo","Lo conozco y participo","Me gustaría participar","Prefiero no responder"
    ]);
    deseo_participar = ""
    if participacion_programa in ["No lo conozco","Lo conozco, pero no participo","Me gustaría participar"]:
        deseo_participar = st.text_area("Si desea contactar, indique nombre, correo y teléfono:")
    medidas_fp = st.text_area("¿Qué medidas considera usted que debe implementar la Fuerza Pública?")
    medidas_muni = st.text_area("¿Qué medidas considera usted que debe implementar la Municipalidad?")
    info_adicional = st.text_area("¿Otra información que desee añadir?")

# === PARTE 8: ENVÍO Y VALIDACIÓN ===
if not st.session_state.enviado:
    if st.button("Enviar formulario"):
        errores = []
        if not st.session_state.ubicacion: errores.append("Ubicación en mapa")
        if not distrito:               errores.append("Distrito")
        if not sexo:                   errores.append("Sexo")
        if not percepcion_seguridad:   errores.append("Percepción de seguridad")
        if not victima:                errores.append("Victimización")
        if not opinion_fp:             errores.append("Opinión sobre FP")
        if not cambio_servicio:        errores.append("Cambio de servicio")
        if not conocimiento_policias:  errores.append("Conocimiento de policías")
        if not participacion_programa: errores.append("Participación en programa")

        if errores:
            st.error("⚠️ Faltan campos obligatorios: " + ", ".join(errores))
        else:
            lat, lon = st.session_state.ubicacion
            ubic_url = f"https://www.google.com/maps?q={lat},{lon}"
            datos = [
                datetime.now().isoformat(),
                distrito, barrio, edad, sexo, escolaridad, tipo_local,
                ubic_url,
                percepcion_seguridad,
                ", ".join(ordered_factores),
                ", ".join(factores_sociales),
                ", ".join(falta_de_inversion),
                ", ".join(consumo_drogas),
                ", ".join(bunker),
                ", ".join(delitos_zona),
                ", ".join(venta_drogas),
                ", ".join(delitos_vida),
                ", ".join(delitos_sexuales),
                ", ".join(asaltos),
                ", ".join(estafas),
                ", ".join(robos),
                observacion_control,
                ", ".join(descripcion_control),
                victima,
                ", ".join(motivo_no_denuncia),
                ", ".join(tipo_delito),
                horario_delito,
                ", ".join(modo_operar),
                exigencia_cuota,
                descripcion_cuota,
                opinion_fp,
                cambio_servicio,
                conocimiento_policias,
                participacion_programa,
                deseo_participar,
                medidas_fp,
                medidas_muni,
                info_adicional
            ]
            sheet = conectar_google_sheets()
            if sheet:
                try:
                    sheet.append_row(datos)
                    st.session_state.enviado = True
                    st.success("✅ ¡Formulario enviado correctamente!")
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
