import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Dashboard de Encuestas", layout="wide")
st.title("📊 Dashboard de Encuestas – Santa Teresa")

# --- Conexión a Google Sheets ---
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

# --- Carga de datos con fallback ---
try:
    records = sheet.get_all_records()
except Exception:
    raw = sheet.get_all_values()
    if len(raw) > 1:
        header = raw[0]
        data_rows = raw[1:]
        records = [dict(zip(header, row)) for row in data_rows]
    else:
        records = []

# Convertir a DataFrame
df = pd.DataFrame.from_records(records)

# Mostrar alerta si no hay datos
if df.empty:
    st.warning("No hay datos de encuestas para mostrar aún.")
else:
    # Métrica: total de encuestas
    total = len(df)
    st.metric("Total de encuestas recibidas", total)

    # Asumir que la primera columna es timestamp
    ts_col = df.columns[0]
    df[ts_col] = pd.to_datetime(df[ts_col], errors='coerce')
    df['date'] = df[ts_col].dt.date

    # Gráfica: encuestas por día
    st.subheader("Encuestas por día")
    daily = df.groupby("date").size()
    st.bar_chart(daily)

    # Distribución de percepción de seguridad
    st.subheader("Distribución de percepción de seguridad")
    seguridad_cols = [c for c in df.columns if 'seguridad' in c.lower()]
    if seguridad_cols:
        col = seguridad_cols[0]
        freq = df[col].value_counts()
        st.bar_chart(freq)
    else:
        st.info("No se encontró columna de percepción de seguridad.")

    # Mostrar tabla de datos completa
    st.subheader("Detalle de todas las respuestas")
    st.dataframe(df)

# Pie de página
st.markdown(
    "<p style='text-align:center; color:#88E145; font-size:10px'>Sembremos Seguridad – 2025</p>",
    unsafe_allow_html=True
)

