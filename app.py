import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from streamlit import secrets

# 0) Inicializar flag para evitar duplicados
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# 1) Autenticación Google Sheets via secrets.toml
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(
    secrets["gcp_service_account"], scope
)
client = gspread.authorize(creds)
sheet = client.open_by_key("1xmQOqnUJUHhLEcBSDAbZX3wNGYmSe34ec8RWaxAUI10").sheet1

# 2) Título
st.title("Encuesta de Seguridad – Santa Teresa")

# 3) Preguntas
barrio   = st.text_input("1. Barrio")
edad     = st.number_input("2. Edad", min_value=0, max_value=120, step=1)
sexo     = st.radio("3. Sexo", ["Hombre", "Mujer", "LGBTQ+", "Prefiero no decirlo"])
seguridad = st.radio(
    "4. ¿Qué tan seguro(a) se siente?",
    ["Muy seguro(a)", "Seguro(a)", "Ni seguro(a)/Ni inseguro(a)", "Inseguro(a)", "Muy inseguro(a)"]
)

FIX_MOTIVOS =[
    "Poca iluminación",
    "Presencia desconocidos",
    "Escasa presencia policial",
    "Robos",
    "Drogas",
    "Otro"
]

# Motivos
motivos = st.multiselect("4.1 Indique motivo(s):", FIXED_MOTIVOS)

# Si “Otro” está en la selección, pedimos el texto
if "Otro" in motivos:
    otro = st.text_input("Especifique otro motivo")
    if otro:
        motivos.append(f"Otro: {otro}")

ordered_motivos = [m for m in FIXED_MOTIVOS if m in motivos]

# Y si “Otro: …” fue añadido, añadirlo al final:
otros = [m for m in motivos if m.startswith("Otro: ")]
if otros:
    ordered_motivos += otros

fila = [
    # … tus otros campos …,
    ";".join(ordered_motivos)
]
sheet.append_row(fila)

# … aquí repites la lógica para preguntas 5–20 …

# 4) Botón de envío
if st.button("Enviar encuesta") and not st.session_state.submitted:
    # Prepara la fila con todas las respuestas (añade tus campos 5–20)
    fila = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        barrio,
        edad,
        sexo,
        seguridad,
        ";".join(motivos),
        # … resto de respuestas en el mismo orden …
    ]

    # Guarda en Google Sheets
    sheet.append_row(fila)

    # Marca como enviado para no duplicar
    st.session_state.submitted = True

    st.success("¡Respuesta registrada! Gracias por tu participación.")
elif st.session_state.submitted:
    st.info("Ya has enviado tu encuesta. ¡Gracias!")

