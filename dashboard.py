import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Configuración de la página
TITLE = "📊 Cantidad de Encuestas – Santa Teresa"
st.set_page_config(page_title=TITLE, layout="wide")
st.title(TITLE)

# === Conexión a Google Sheets ===
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_dict(
    st.secrets["gcp_service_account"], scope
)
client = gspread.authorize(creds)
sheet = client.open_by_key(
    "1xmQOqnUJUHhLEcBSDAbZX3wNGYmSe34ec8RWaxAUI10"
).sheet1

# === Lectura de datos ===
raw = sheet.get_all_values()
if len(raw) <= 1:
    st.warning("No hay datos de encuestas para mostrar aún.")
else:
    header = raw[0]
    data = raw[1:]

    # Eliminar encabezados duplicados añadiendo sufijo numérico
    deduped = []
    counts = {}
    for col in header:
        if col in counts:
            counts[col] += 1
            deduped.append(f"{col}_{counts[col]}")
        else:
            counts[col] = 0
            deduped.append(col)
    header = deduped

    # Crear DataFrame con columnas únicas
    df = pd.DataFrame(data, columns=header)

  # Métrica personalizada: Total de encuestas recibidas (centrado y grande)
total = len(df)
st.markdown(f"""
    <div style="text-align: center; margin-top: 50px;">
        <h2 style="font-size: 28px;">Total de encuestas recibidas</h2>
        <p style="font-size: 72px; font-weight: bold; color: #2E8B57;">{total}</p>
    </div>
""", unsafe_allow_html=True)


    # Intentar convertir la primera columna a datetime
ts_col = header[0]
    try:
        df[ts_col] = pd.to_datetime(df[ts_col], errors='coerce')
        df['date'] = df[ts_col].dt.date
    except Exception:
        df['date'] = None

   
