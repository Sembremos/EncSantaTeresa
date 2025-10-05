import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from PIL import Image

# === PARTE 0: CONFIGURACIÓN INICIAL Y SESIÓN ===
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
        # Obtener credenciales desde st.secrets
        creds_dict = st.secrets.get("gcp_service_account")
        if not creds_dict:
            st.error("❌ No se encontró 'gcp_service_account' en st.secrets.")
            return None

        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)

        # Abre la hoja por key (asegúrate que la key esté correcta)
        SPREADSHEET_KEY = "1xmQOqnUJUHhLEcBSDAbZX3wNGYmSe34ec8RWaxAUI10"
        try:
            sheet = client.open_by_key(SPREADSHEET_KEY).sheet1
        except Exception as e:
            st.error(f"❌ No se pudo abrir el spreadsheet con la key indicada: {e}")
            return None

        # --- Crear encabezados si la hoja está vacía ---
        try:
            current = sheet.get_all_values()  # lista de filas con valores
        except Exception as e:
            st.error(f"❌ Error al leer valores de la hoja: {e}")
            return sheet

        if not current or len(current) == 0:
            headers = [
                "Fecha y hora",
                "Categoría del negocio",
                "Años de operación",
                "Tipo de cliente principal",
                "Medidas de seguridad implementadas",
                "Cambios operativos realizados",
                "Impacto en las ventas",
                "Frecuencia de comentarios sobre seguridad",
                "Delito más preocupante",
                "Frecuencia de delitos",
                "Momento de mayor riesgo",
                "Urgencia: Aumentar oficiales",
                "Urgencia: Aumentar patrullaje a pie",
                "Urgencia: Mejorar iluminación",
                "Urgencia: Instalar cámaras monitoreadas",
                "Urgencia: Implementación programas policiales",
                "Efecto disuasorio: Mayor presencia policial",
                "Efecto disuasorio: OIJ efectivo",
                "Efecto disuasorio: Cámaras estratégicas",
                "Efecto disuasorio: Controles de carretera",
                "Efecto disuasorio: Programas sociales",
                "Percepción: Presencia policial suficiente",
                "Percepción: Tiempo de respuesta",
                "Percepción: Confianza en denuncias",
                "Percepción: Profesionalismo policial",
                "Percepción: Recursos suficientes",
                "Percepción: Programas efectivos",
                "Razones para no denunciar",
                "Acción que aumentaría confianza",
                "Disposición para alianza público-privada"
            ]
            try:
                # insert_row pone los encabezados en la fila 1
                sheet.insert_row(headers, 1)
                st.info("🔧 Encabezados creados automáticamente en la hoja.")
            except Exception as e:
                st.error(f"❌ No se pudieron crear encabezados: {e}")

        return sheet
    except Exception as e:
        st.error(f"❌ Error general al conectar con Google Sheets: {e}")
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
.expander-title {
    background-color: #347A59;
    color: #ffffff;
    font-size:18px;
    font-weight:bold;
    border-radius:10px;
    padding:15px 20px;
    margin-bottom:-20px;
    text-align:left;
}
summary::marker { display:none; }
div[data-testid="stExpander"] > div {
    background-color:#ffffff;
    border:2px solid #ff4b4b;
    border-radius:12px;
    padding:10px;
}
.stSelectbox > div, .stRadio > div, .stMultiSelect > div, .stTextArea > div {
    background-color:#51924b;
    border:2px solid #51924b;
    border-radius:10px;
    padding:10px;
    color:#2C517A !important;
}
.stButton > button {
    background-color:#DF912F;
    color:#ffffff;
    border:none;
    border-radius:10px;
    padding:10px 24px;
    font-size:16px;
}
.stButton > button:hover {
    background-color:#DF912F;
    color:white;
}
div[role="radiogroup"] label[data-selected="true"],
div[role="listbox"] div[data-selected="true"] {
    color:#ffffff !important;
    border-radius:8px !important;
    font-weight:bold !important;
}
div[role="radiogroup"] label[data-selected="true"]::after,
div[role="listbox"] div[data-selected="true"]::after {
    content:" ✅";
    margin-left:6px;
}
label, .stMarkdown p {
    color:#ffffff !important;
    font-weight:600;
}
@media only screen and (max-width:768px) {
    iframe { height:300px !important; max-height:300px !important; }
}
</style>
""", unsafe_allow_html=True)

# Si tu banner no está disponible, comentalo temporalmente para evitar errores
try:
    banner = Image.open("baner.png")
    st.markdown('<div class="banner-container">', unsafe_allow_html=True)
    st.image(banner, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
except Exception:
    # no interrumpe la app si la imagen no está disponible
    pass

st.markdown("""
**Con el objetivo de fortalecer la seguridad en nuestro entorno comercial, nos enfocamos en abordar las principales preocupaciones de seguridad.**
La información que nos suministras es completamente confidencial y se emplea exclusivamente con el propósito de mejorar la seguridad en nuestra área comercial.
""", unsafe_allow_html=True)

# === NUEVO FORMULARIO (16 preguntas solicitadas) ===
st.title("Encuesta: Seguridad en Sámara")
st.markdown("Por favor complete este formulario de forma anónima. Sus respuestas serán confidenciales y utilizadas únicamente para fines de diagnóstico y mejora de la seguridad local.")

# === PARTE 3..7: reemplazadas por las nuevas secciones solicitadas ===
with st.expander("Sección 1: Perfil de su Negocio", expanded=True):
    categoria = st.radio(
        "1. ¿Cuál de las siguientes categorías describe mejor su negocio?",
        ["Hotelería / Hospedaje", "Restaurante / Bar", "Tour Operador / Actividad Turística",
         "Tienda / Supermercado", "Otro (especifique)"]
    )
    if categoria == "Otro (especifique)":
        categoria_otro = st.text_input("Especifique otra categoría:")
        if categoria_otro:
            categoria = f"Otro: {categoria_otro}"

    años = st.radio(
        "2. ¿Hace cuántos años opera su negocio en Sámara?",
        ["Menos de 2 años", "Entre 2 y 5 años", "Entre 6 y 10 años", "Más de 10 años"]
    )

    clientes = st.radio(
        "3. ¿Quiénes son su principal tipo de cliente?",
        ["Principalmente turistas extranjeros", "Principalmente turistas nacionales",
         "Una mezcla equilibrada de turistas y residentes locales", "Principalmente residentes locales"]
    )

with st.expander("Sección 2: Impacto en su Negocio", expanded=False):
    medidas = st.multiselect(
        "4. En el último año, ¿cuáles de las siguientes medidas de seguridad ha implementado o reforzado? (Marque todos los que apliquen)",
        ["Contratación de seguridad privada / guarda", "Instalación o mejora de cámaras de vigilancia",
         "Instalación de sistema de alarmas", "Mejora de la iluminación externa", "Reforzamiento de cerraduras, puertas o ventanas",
         "No he implementado nuevas medidas", "Otra (especifique)"]
    )
    medidas_otro = ""
    if "Otra (especifique)" in medidas:
        medidas_otro = st.text_input("Especifique otra medida de seguridad:")
        if medidas_otro:
            # sustituimos la opción genérica por la versión con texto
            medidas = [m for m in medidas if m != "Otra (especifique)"] + [f"Otro: {medidas_otro}"]

    cambios = st.multiselect(
        "5. A raíz de la situación de seguridad, ¿ha realizado alguno de los siguientes cambios operativos? (Marque todos los que apliquen)",
        ["He reducido el horario de atención al público", "He modificado los horarios de mi personal por su seguridad",
         "He tenido que acompañar a clientes o personal a sus vehículos", "He experimentado mayor rotación de personal o dificultad para contratar",
         "No he realizado cambios operativos", "Otro (especifique)"]
    )
    cambios_otro = ""
    if "Otro (especifique)" in cambios:
        cambios_otro = st.text_input("Especifique otro cambio operativo:")
        if cambios_otro:
            cambios = [c for c in cambios if c != "Otro (especifique)"] + [f"Otro: {cambios_otro}"]

    impacto = st.radio(
        "6. ¿Cómo calificaría el impacto de la inseguridad en sus ventas o ingresos del último año?",
        ["Impacto muy negativo (pérdidas significativas)", "Impacto negativo (pérdidas moderadas)",
         "Poco o ningún impacto", "No estoy seguro/a"]
    )

    frecuencia_clientes = st.radio(
        "7. ¿Con qué frecuencia recibe comentarios o preguntas de sus clientes sobre la seguridad en Sámara?",
        ["Muy frecuentemente (casi todos los días)", "Frecuentemente (varias veces a la semana)",
         "Ocasionalmente (algunas veces al mes)", "Casi nunca"]
    )

with st.expander("Sección 3: Caracterización del Delito", expanded=False):
    delito = st.radio(
        "8. Desde la perspectiva de su negocio y sus alrededores, ¿cuál es el delito MÁS PREOCUPANTE?",
        ["Hurtos a turistas por descuido (en la playa, restaurante, etc.)", "Robos a locales comerciales (cuando están cerrados)",
         "Tachas o robos a vehículos de clientes", "Asaltos o arrebatos en la vía pública", "Venta de drogas en los alrededores"]
    )

    frecuencia_delito = st.radio(
        "9. En su opinión, la frecuencia de estos delitos en la zona comercial es...",
        ["Constante, ocurre casi a diario.", "Frecuente, ocurre varias veces por semana.",
         "Periódica, ocurre en rachas o algunas veces al mes.", "Poco frecuente."]
    )

    momento_riesgo = st.radio(
        "10. ¿En qué momento percibe que hay MAYOR RIESGO en la zona comercial?",
        ["Durante la noche (después de las 9 p.m.)", "Durante la madrugada", "Durante el día, por el descuido de los turistas",
         "El riesgo es constante a toda hora"]
    )

with st.expander("Sección 4: Soluciones y Prioridades", expanded=False):
    st.markdown("11. Valore de 1 a 5 la URGENCIA de las siguientes acciones (1 = Poco urgente, 5 = Máxima urgencia).")
    urgencia1 = st.slider("Aumentar el número de oficiales de Fuerza Pública", 1, 5, 3)
    urgencia2 = st.slider("Aumentar el patrullaje a pie en zonas comerciales", 1, 5, 3)
    urgencia3 = st.slider("Mejorar significativamente la iluminación pública", 1, 5, 3)
    urgencia4 = st.slider("Instalar un sistema de cámaras de vigilancia monitoreado", 1, 5, 3)
    urgencia5 = st.slider("Implementación de Programas Policiales efectivos", 1, 5, 3)

    st.markdown("12. Valore de 1 a 5 la URGENCIA de las siguientes acciones que tendrían EFECTO DISUASORIO.")
    efecto1 = st.slider("Mayor presencia policial visible (patrullaje a pie)", 1, 5, 3)
    efecto2 = st.slider("Investigaciones y detenciones efectivas por parte del OIJ", 1, 5, 3)
    efecto3 = st.slider("Cámaras de vigilancia en puntos estratégicos", 1, 5, 3)
    efecto4 = st.slider("Controles de carretera (retenes) en las entradas del pueblo", 1, 5, 3)
    efecto5 = st.slider("Programas sociales para jóvenes locales", 1, 5, 3)

with st.expander("Percepción sobre la Fuerza Pública", expanded=False):
    st.markdown("13. Indique su nivel de acuerdo o desacuerdo (Muy en desacuerdo ... Muy de acuerdo).")
    p1 = st.radio("La presencia policial actual en la zona comercial es suficiente para disuadir el delito.", ["Muy en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Muy de acuerdo"])
    p2 = st.radio("El tiempo de respuesta de la policía cuando se reporta un incidente es rápido.", ["Muy en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Muy de acuerdo"])
    p3 = st.radio("Confío en que la policía tomará en serio una denuncia si la presento.", ["Muy en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Muy de acuerdo"])
    p4 = st.radio("La policía trata a los comerciantes y al público con profesionalismo y respeto.", ["Muy en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Muy de acuerdo"])
    p5 = st.radio("Siento que la policía cuenta con los recursos necesarios para ser efectiva.", ["Muy en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Muy de acuerdo"])
    p6 = st.radio("Los programas policiales implementados han sido efectivos en la zona.", ["Muy en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Muy de acuerdo"])

with st.expander("Razones y confianza", expanded=False):
    razones = st.multiselect(
        "14. Si alguna vez usted o alguien de su entorno ha dudado en presentar una denuncia formal a la policía, ¿cuál ha sido la razón principal? (Marque todas las que apliquen)",
        ["Miedo a represalias por parte de los delincuentes", "Creencia de que la denuncia no llevará a ningún resultado (impunidad)",
         "El proceso para denunciar es demasiado lento o complicado", "Falta de confianza en la confidencialidad de la denuncia",
         "El incidente se consideró 'menor' y no valía la pena el esfuerzo", "Prefiero alertar por canales informales (chats de vecinos/comerciantes)",
         "No he dudado en denunciar", "Otra razón (especifique)"]
    )
    otra_razon = ""
    if "Otra razón (especifique)" in razones:
        otra_razon = st.text_input("Especifique otra razón:")
        if otra_razon:
            razones = [r for r in razones if r != "Otra razón (especifique)"] + [f"Otro: {otra_razon}"]

    confianza = st.radio(
        "15. Desde su perspectiva como comerciante, ¿qué acción por parte de la policía aumentaría MÁS su confianza en la institución?",
        ["Ver patrullajes a pie de forma constante en la zona comercial", "Obtener respuestas mucho más rápidas cuando se les llama",
         "Ver que las denuncias resultan en detenciones y procesos judiciales efectivos", "Tener reuniones periódicas y una comunicación más abierta con el sector comercial",
         "Otra (especifique)"]
    )
    if confianza == "Otra (especifique)":
        confianza_otro = st.text_input("Especifique otra acción que aumentaría su confianza:")
        if confianza_otro:
            confianza = f"Otro: {confianza_otro}"

    alianza = st.radio(
        "16. ¿Estaría su negocio dispuesto a participar en una alianza público-privada para cofinanciar un proyecto de seguridad (ej. sistema de cámaras centralizado)?",
        ["Sí, definitivamente", "Sí, dependiendo del costo y el plan", "Quizás, necesitaría más información", "No"]
    )

# === PARTE 8: ENVÍO Y VALIDACIÓN (manteniendo la estructura original) ===
if not st.session_state.enviado:
    if st.button("Enviar formulario"):
        errores = []
        # Validaciones mínimas: requerir las 3 preguntas iniciales (puedes ampliar si lo deseas)
        if not categoria:
            errores.append("Categoría del negocio")
        if not años:
            errores.append("Años de operación")
        if not clientes:
            errores.append("Tipo de cliente principal")

        if errores:
            st.error("⚠️ Faltan campos obligatorios: " + ", ".join(errores))
        else:
            # Armar datos en el mismo orden que los encabezados
            datos = [
                datetime.now().isoformat(),
                categoria,
                años,
                clientes,
                "; ".join(medidas) if medidas else "",
                "; ".join(cambios) if cambios else "",
                impacto,
                frecuencia_clientes,
                delito,
                frecuencia_delito,
                momento_riesgo,
                urgencia1, urgencia2, urgencia3, urgencia4, urgencia5,
                efecto1, efecto2, efecto3, efecto4, efecto5,
                p1, p2, p3, p4, p5, p6,
                "; ".join(razones) if razones else "",
                confianza,
                alianza
            ]

            sheet = conectar_google_sheets()
            if sheet:
                try:
                    # Asegurar consistencia con encabezados actuales
                    headers_row = sheet.row_values(1)
                    headers_len = len(headers_row)

                    # Si por alguna razón la fila de encabezados está vacía, forzamos creación
                    if headers_len == 0:
                        st.warning("La fila de encabezados está vacía — intentando crear encabezados por seguridad.")
                        default_headers = [f"Col_{i+1}" for i in range(len(datos))]
                        sheet.insert_row(default_headers, 1)
                        headers_row = default_headers
                        headers_len = len(headers_row)

                    # Si enviás más datos que encabezados, ampliamos encabezados con "Extra_X"
                    if len(datos) > headers_len:
                        extra = len(datos) - headers_len
                        new_headers = headers_row + [f"Extra_{i+1}" for i in range(extra)]
                        sheet.update('A1', [new_headers])
                        headers_row = new_headers
                        headers_len = len(new_headers)
                        st.info(f"🔧 Se ampliaron los encabezados (+{extra}).")

                    # Si enviás menos datos, rellenamos con cadenas vacías
                    if len(datos) < headers_len:
                        datos += [""] * (headers_len - len(datos))

                    # Convertir todo a string (evita None)
                    datos = [str(d) if d is not None else "" for d in datos]

                    # Append la fila al final
                    sheet.append_row(datos, value_input_option='USER_ENTERED')

                    st.session_state.enviado = True
                    st.success("✅ ¡Formulario enviado correctamente!")
                    if st.button("📝 Enviar otra respuesta"):
                        st.session_state.enviado = False
                        st.experimental_rerun()
                except Exception as e:
                    st.error(f"❌ Error al guardar: {e}")
            else:
                st.error("❌ No se pudo conectar con Google Sheets.")
else:
    st.info("Ya completaste la encuesta. ¡Gracias!")

st.markdown("<p style='text-align:center;color:#88E145;font-size:10px'>Sembremos Seguridad - 2025</p>", unsafe_allow_html=True)
