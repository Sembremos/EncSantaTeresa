import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# --- CONFIGURACIÓN DE CONEXIÓN A GOOGLE SHEETS ---
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file("credenciales.json", scopes=SCOPE)
client = gspread.authorize(creds)
sheet = client.open_by_key("1xmQOqnUJUHhLEcBSDAbZX3wNGYmSe34ec8RWaxAUI10").sheet1

st.title("Formulario con encabezados automáticos")

# --- ENCABEZADOS ESPERADOS ---
HEADERS = ["Nombre", "Edad", "Correo", "Factores de riesgo", "Comentarios"]

# --- VERIFICAR SI LA HOJA ESTÁ VACÍA Y CREAR ENCABEZADOS ---
if len(sheet.get_all_values()) == 0:
    sheet.insert_row(HEADERS, 1)
    st.info("🔧 Se crearon los encabezados automáticamente en la hoja.")

# --- FORMULARIO ---
with st.form("mi_formulario"):
    nombre = st.text_input("Nombre completo")
    edad = st.number_input("Edad", min_value=0, max_value=120, step=1)
    correo = st.text_input("Correo electrónico")
    factores = st.multiselect(
        "Factores de riesgo",
        ["Robo a comercio", "Hurto", "Asalto a vivienda", "Otros"]
    )
    comentarios = st.text_area("Comentarios adicionales")

    enviar = st.form_submit_button("Enviar")

# --- PROCESAMIENTO ---
if enviar:
    # Convertir listas a texto con punto y coma
    factores_str = "; ".join(factores) if factores else ""

    # Asegurar que todos los datos sean texto
    datos = [
        str(nombre),
        str(edad),
        str(correo),
        str(factores_str),
        str(comentarios)
    ]

    # Insertar nueva fila después de los encabezados
    next_row = len(sheet.get_all_values()) + 1
    sheet.insert_row(datos, next_row)

    st.success("✅ Respuesta enviada correctamente y alineada.")
