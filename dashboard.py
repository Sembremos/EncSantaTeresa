import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Configuración de la página
TITLE = "📊 Dashboard de Encuestas – Santa Teresa"
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

    # Gráfica: encuestas por día
    st.subheader("Encuestas por día")
    if 'date' in df.columns and df['date'].notna().any():
        daily = df.groupby('date').size()
        st.bar_chart(daily)
    else:
        st.info("No hay datos de fecha válidos para graficar")

    # Distribución de percepción de seguridad
    st.subheader("Distribución de percepción de seguridad")
    seguridad_col = next((c for c in df.columns if 'seguridad' in c.lower()), None)
    if seguridad_col:
        freq = df[seguridad_col].value_counts()
        st.bar_chart(freq)
    else:
        st.info("No se encontró columna de percepción de seguridad.")

    # Encuestas por Barrio (columna C)
    st.subheader("Encuestas por Barrio")
    serie_barrio = df.iloc[:, 2]
    counts_barrio = serie_barrio.dropna().value_counts()
    st.bar_chart(counts_barrio)

    # Mostrar tabla de datos completa
    st.subheader("Detalle de todas las respuestas")
    st.dataframe(df)

# Pie de página
st.markdown(
    "<p style='text-align:center; color:#88E145; font-size:10px'>Sembremos Seguridad – 2025</p>",
    unsafe_allow_html=True
)
