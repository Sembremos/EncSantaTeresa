import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from streamlit import secrets

# 0) Inicializar flag para evitar duplicados
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# 1) Conexión a Google Sheets vía secrets.toml
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(secrets["gcp_service_account"], scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1xmQOqnUJUHhLEcBSDAbZX3wNGYmSe34ec8RWaxAUI10").sheet1

# 2) Título de la app
st.title("Encuesta de Seguridad – Santa Teresa")

# 3) Preguntas
barrio   = st.text_input("1. ¿En qué barrio vive?")
edad     = st.number_input("2. Edad", min_value=0, max_value=120, step=1)
sexo     = st.radio("3. Sexo", ["Hombre", "Mujer", "LGBTQ+", "Prefiero no decirlo"])
seguridad = st.radio(
    "4. ¿Qué tan seguro(a) se siente?",
    ["Muy seguro(a)", "Seguro(a)", "Ni seguro(a)/Ni inseguro(a)", "Inseguro(a)", "Muy inseguro(a)"]
)

# 4.1) Selección de motivos con orden fijo
FIXED_MOTIVOS = [
    "Poca iluminación",
    "Presencia desconocidos",
    "Escasa presencia policial",
    "Robos",
    "Drogas",
    "Otro"
]

ordered_motivos = []
if seguridad in ["Inseguro(a)", "Muy inseguro(a)"]:
    motivos = st.multiselect("4.1 Indique motivo(s):", FIXED_MOTIVOS)
    # si marca "Otro", pide texto
    if "Otro" in motivos:
        otro = st.text_input("Especifique otro motivo")
        if otro:
            motivos.append(f"Otro: {otro}")
    # reordenar según FIXED_MOTIVOS
    ordered_motivos = [m for m in FIXED_MOTIVOS if m in motivos]
    # poner los ítems “Otro: …” al final
    otros = [m for m in motivos if m.startswith("Otro: ")]
    if otros:
        ordered_motivos += otros

# … aquí repite la lógica de preguntas 5–20 …

# 4) Botón de envío
if st.button("Enviar encuesta") and not st.session_state.submitted:
    # prepara la fila en el orden de columnas de tu hoja
    fila = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        barrio,
        edad,
        sexo,
        seguridad,
        ";".join(ordered_motivos),
        # … añade aquí las respuestas 5–20 …
    ]
    # guarda en Google Sheets
    sheet.append_row(fila)
    st.session_state.submitted = True
    st.success("¡Respuesta registrada! Gracias por participar.")
elif st.session_state.submitted:
    st.info("Ya has enviado la encuesta. ¡Muchas gracias!")


