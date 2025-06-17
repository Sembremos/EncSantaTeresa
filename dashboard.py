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

    # Métrica: total de encuestas
    total = len(df)
    st.metric("Total de encuestas recibidas", total)

    # Intentar convertir la primera columna a datetime
    ts_col = header[0]
    try:
        df[ts_col] = pd.to_datetime(df[ts_col], errors='coerce')
        df['date'] = df[ts_col].dt.date
    except Exception:
        df['date'] = None

   
