import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Configuración de Google Sheets
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPE)
client = gspread.authorize(creds)
sheet = client.open("Formulario Seguridad Sámara").sheet1  # Cambia el nombre según tu hoja

# ========================
# Crear encabezados si no existen
# ========================
headers = [
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
    "Urgencia: Cámaras monitoreadas",
    "Urgencia: Programas policiales",
    "Efecto disuasorio: Mayor presencia policial",
    "Efecto disuasorio: OIJ efectivo",
    "Efecto disuasorio: Cámaras estratégicas",
    "Efecto disuasorio: Controles de carretera",
    "Efecto disuasorio: Programas sociales",
    "Percepción: Presencia policial suficiente",
    "Percepción: Tiempo de respuesta rápido",
    "Percepción: Confianza en denuncias",
    "Percepción: Profesionalismo policial",
    "Percepción: Recursos suficientes",
    "Percepción: Programas efectivos",
    "Razones para no denunciar",
    "Acción que aumentaría confianza",
    "Disposición para alianza público-privada"
]

if len(sheet.get_all_values()) == 0:
    sheet.append_row(headers)

st.title("Encuesta: Seguridad en Sámara")
st.markdown("Por favor, complete el siguiente formulario de manera anónima. Sus respuestas son confidenciales.")

with st.form("formulario_samara"):
    st.subheader("Sección 1: Perfil de su Negocio")
    categoria = st.radio("1. ¿Cuál de las siguientes categorías describe mejor su negocio?", 
                         ["Hotelería / Hospedaje", "Restaurante / Bar", "Tour Operador / Actividad Turística", 
                          "Tienda / Supermercado", "Otro (especifique)"])
    
    años = st.radio("2. ¿Hace cuántos años opera su negocio en Sámara?", 
                    ["Menos de 2 años", "Entre 2 y 5 años", "Entre 6 y 10 años", "Más de 10 años"])
    
    clientes = st.radio("3. ¿Quiénes son su principal tipo de cliente?", 
                        ["Principalmente turistas extranjeros", "Principalmente turistas nacionales", 
                         "Una mezcla equilibrada de turistas y residentes locales", "Principalmente residentes locales"])

    st.subheader("Sección 2: Impacto en su Negocio")
    medidas = st.multiselect("4. ¿Cuáles medidas de seguridad ha implementado o reforzado?", 
                             ["Seguridad privada / guarda", "Cámaras de vigilancia", "Sistema de alarmas", 
                              "Mejora de iluminación", "Reforzamiento de cerraduras", "No he implementado nuevas medidas", "Otra"])
    
    cambios = st.multiselect("5. ¿Ha realizado alguno de los siguientes cambios operativos?", 
                             ["Reducido horario", "Modificado horarios de personal", "Acompañar clientes/personal", 
                              "Mayor rotación o dificultad para contratar", "No he realizado cambios", "Otro"])
    
    impacto = st.radio("6. ¿Cómo calificaría el impacto de la inseguridad en sus ventas?", 
                       ["Muy negativo", "Negativo", "Poco o ningún impacto", "No estoy seguro/a"])
    
    frecuencia = st.radio("7. ¿Con qué frecuencia recibe comentarios de clientes sobre seguridad?", 
                          ["Muy frecuentemente", "Frecuentemente", "Ocasionalmente", "Casi nunca"])

    st.subheader("Sección 3: Caracterización del Delito")
    delito = st.radio("8. ¿Cuál es el delito más preocupante?", 
                      ["Hurtos a turistas", "Robos a locales comerciales", "Tachas o robos a vehículos", 
                       "Asaltos o arrebatos en vía pública", "Venta de drogas"])
    
    frecuencia_delito = st.radio("9. Frecuencia de estos delitos:", 
                                 ["Constante", "Frecuente", "Periódica", "Poco frecuente"])
    
    riesgo = st.radio("10. ¿Cuándo hay mayor riesgo?", 
                      ["Durante la noche", "Durante la madrugada", "Durante el día", "Constante a toda hora"])

    st.subheader("Sección 4: Soluciones y Prioridades")
    urgencia1 = st.slider("11a. Aumentar oficiales de Fuerza Pública", 1, 5, 3)
    urgencia2 = st.slider("11b. Aumentar patrullaje a pie", 1, 5, 3)
    urgencia3 = st.slider("11c. Mejorar iluminación pública", 1, 5, 3)
    urgencia4 = st.slider("11d. Instalar cámaras monitoreadas", 1, 5, 3)
    urgencia5 = st.slider("11e. Implementar programas policiales efectivos", 1, 5, 3)

    efecto1 = st.slider("12a. Mayor presencia policial visible", 1, 5, 3)
    efecto2 = st.slider("12b. OIJ efectivo", 1, 5, 3)
    efecto3 = st.slider("12c. Cámaras estratégicas", 1, 5, 3)
    efecto4 = st.slider("12d. Controles de carretera", 1, 5, 3)
    efecto5 = st.slider("12e. Programas sociales para jóvenes", 1, 5, 3)

    st.subheader("Percepción sobre la Fuerza Pública")
    p1 = st.radio("13a. Presencia policial suficiente", ["Muy en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Muy de acuerdo"])
    p2 = st.radio("13b. Tiempo de respuesta rápido", ["Muy en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Muy de acuerdo"])
    p3 = st.radio("13c. Confianza en denuncias", ["Muy en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Muy de acuerdo"])
    p4 = st.radio("13d. Profesionalismo policial", ["Muy en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Muy de acuerdo"])
    p5 = st.radio("13e. Recursos suficientes", ["Muy en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Muy de acuerdo"])
    p6 = st.radio("13f. Programas policiales efectivos", ["Muy en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Muy de acuerdo"])

    razones = st.multiselect("14. Razones para no denunciar", 
                             ["Miedo a represalias", "Creencia de impunidad", "Proceso lento", "Falta de confidencialidad", 
                              "Incidente menor", "Alerto por canales informales", "No he dudado en denunciar", "Otra razón"])

    confianza = st.radio("15. ¿Qué acción aumentaría su confianza?", 
                         ["Patrullajes a pie constantes", "Respuestas rápidas", "Denuncias con resultados", 
                          "Reuniones periódicas con comerciantes", "Otra"])

    alianza = st.radio("16. ¿Participaría en una alianza público-privada?", 
                       ["Sí, definitivamente", "Sí, dependiendo del costo y plan", "Quizás, necesitaría más información", "No"])

    enviado = st.form_submit_button("Enviar respuestas")

if enviado:
    datos = [
        categoria, años, clientes, ", ".join(medidas), ", ".join(cambios), impacto, frecuencia, delito, 
        frecuencia_delito, riesgo, urgencia1, urgencia2, urgencia3, urgencia4, urgencia5,
        efecto1, efecto2, efecto3, efecto4, efecto5,
        p1, p2, p3, p4, p5, p6, ", ".join(razones), confianza, alianza
    ]
    sheet.append_row(datos)
    st.success("✅ ¡Gracias! Su respuesta ha sido registrada correctamente.")


