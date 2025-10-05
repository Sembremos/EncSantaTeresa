import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# =======================
# CONFIGURACIÓN GOOGLE SHEETS
# =======================
SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPE)
client = gspread.authorize(creds)
sheet = client.open("Formulario Seguridad Sámara").sheet1  # Cambia al nombre exacto de tu hoja

# =======================
# ENCABEZADOS (solo si está vacía)
# =======================
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

# =======================
# FORMULARIO STREAMLIT
# =======================
st.title("Encuesta: Seguridad en Sámara")
st.markdown("Por favor complete este formulario de forma anónima. Sus respuestas serán confidenciales y utilizadas únicamente para fines de diagnóstico y mejora de la seguridad local.")

with st.form("formulario_samara"):

    st.subheader("Sección 1: Perfil de su Negocio")
    categoria = st.radio(
        "1. ¿Cuál de las siguientes categorías describe mejor su negocio?",
        ["Hotelería / Hospedaje", "Restaurante / Bar", "Tour Operador / Actividad Turística",
         "Tienda / Supermercado", "Otro (especifique)"]
    )
    años = st.radio(
        "2. ¿Hace cuántos años opera su negocio en Sámara?",
        ["Menos de 2 años", "Entre 2 y 5 años", "Entre 6 y 10 años", "Más de 10 años"]
    )
    clientes = st.radio(
        "3. ¿Quiénes son su principal tipo de cliente?",
        ["Principalmente turistas extranjeros", "Principalmente turistas nacionales",
         "Una mezcla equilibrada de turistas y residentes locales", "Principalmente residentes locales"]
    )

    st.subheader("Sección 2: Impacto en su Negocio")
    medidas = st.multiselect(
        "4. ¿Cuáles de las siguientes medidas de seguridad ha implementado o reforzado?",
        ["Seguridad privada", "Cámaras de vigilancia", "Sistema de alarmas", "Mejora de iluminación externa",
         "Reforzamiento de cerraduras", "No he implementado nuevas medidas", "Otra (especifique)"]
    )
    cambios = st.multiselect(
        "5. A raíz de la situación de seguridad, ¿ha realizado alguno de los siguientes cambios operativos?",
        ["Reducido horario de atención", "Modificado horarios del personal", "Acompañar a clientes/personal a vehículos",
         "Mayor rotación o dificultad para contratar", "No he realizado cambios", "Otro (especifique)"]
    )
    impacto = st.radio(
        "6. ¿Cómo calificaría el impacto de la inseguridad en sus ventas o ingresos del último año?",
        ["Impacto muy negativo", "Impacto negativo", "Poco o ningún impacto", "No estoy seguro/a"]
    )
    frecuencia = st.radio(
        "7. ¿Con qué frecuencia recibe comentarios o preguntas de sus clientes sobre la seguridad en Sámara?",
        ["Muy frecuentemente", "Frecuentemente", "Ocasionalmente", "Casi nunca"]
    )

    st.subheader("Sección 3: Caracterización del Delito")
    delito = st.radio(
        "8. Desde la perspectiva de su negocio, ¿cuál es el delito MÁS preocupante?",
        ["Hurtos a turistas por descuido", "Robos a locales comerciales", "Tachas o robos a vehículos",
         "Asaltos o arrebatos", "Venta de drogas en los alrededores"]
    )
    frecuencia_delito = st.radio(
        "9. En su opinión, la frecuencia de estos delitos en la zona comercial es...",
        ["Constante", "Frecuente", "Periódica", "Poco frecuente"]
    )
    riesgo = st.radio(
        "10. ¿En qué momento percibe que hay mayor riesgo?",
        ["Durante la noche", "Durante la madrugada", "Durante el día", "Constante a toda hora"]
    )

    st.subheader("Sección 4: Soluciones y Prioridades")
    urgencia1 = st.slider("Aumentar número de oficiales de Fuerza Pública", 1, 5, 3)
    urgencia2 = st.slider("Aumentar patrullaje a pie en zonas comerciales", 1, 5, 3)
    urgencia3 = st.slider("Mejorar significativamente la iluminación pública", 1, 5, 3)
    urgencia4 = st.slider("Instalar un sistema de cámaras monitoreadas", 1, 5, 3)
    urgencia5 = st.slider("Implementación de programas policiales efectivos", 1, 5, 3)

    efecto1 = st.slider("Mayor presencia policial visible (patrullaje a pie)", 1, 5, 3)
    efecto2 = st.slider("Investigaciones y detenciones efectivas por parte del OIJ", 1, 5, 3)
    efecto3 = st.slider("Cámaras de vigilancia en puntos estratégicos", 1, 5, 3)
    efecto4 = st.slider("Controles de carretera en entradas del pueblo", 1, 5, 3)
    efecto5 = st.slider("Programas sociales para jóvenes locales", 1, 5, 3)

    st.subheader("Percepción sobre la Fuerza Pública")
    p1 = st.radio("La presencia policial es suficiente para disuadir el delito", ["Muy en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Muy de acuerdo"])
    p2 = st.radio("El tiempo de respuesta de la policía es rápido", ["Muy en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Muy de acuerdo"])
    p3 = st.radio("Confío en que la policía tomará en serio una denuncia", ["Muy en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Muy de acuerdo"])
    p4 = st.radio("La policía trata al público con profesionalismo y respeto", ["Muy en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Muy de acuerdo"])
    p5 = st.radio("La policía cuenta con recursos suficientes", ["Muy en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Muy de acuerdo"])
    p6 = st.radio("Los programas policiales han sido efectivos", ["Muy en desacuerdo", "En desacuerdo", "Neutral", "De acuerdo", "Muy de acuerdo"])

    razones = st.multiselect(
        "Si ha dudado en denunciar, ¿cuál fue la razón principal?",
        ["Miedo a represalias", "Creencia de impunidad", "Proceso lento o complicado",
         "Falta de confidencialidad", "Incidente menor", "Alerto por canales informales",
         "No he dudado en denunciar", "Otra razón"]
    )
    confianza = st.radio(
        "¿Qué acción por parte de la policía aumentaría más su confianza?",
        ["Ver patrullajes a pie constantes", "Respuestas más rápidas", "Denuncias con resultados efectivos",
         "Reuniones periódicas con comerciantes", "Otra (especifique)"]
    )
    alianza = st.radio(
        "¿Estaría dispuesto a participar en una alianza público-privada para un proyecto de seguridad?",
        ["Sí, definitivamente", "Sí, dependiendo del costo", "Quizás, necesito más información", "No"]
    )

    enviado = st.form_submit_button("Enviar")

if enviado:
    datos = [
        categoria, años, clientes, ", ".join(medidas), ", ".join(cambios),
        impacto, frecuencia, delito, frecuencia_delito, riesgo,
        urgencia1, urgencia2, urgencia3, urgencia4, urgencia5,
        efecto1, efecto2, efecto3, efecto4, efecto5,
        p1, p2, p3, p4, p5, p6,
        ", ".join(razones), confianza, alianza
    ]
    sheet.append_row(datos)
    st.success("✅ ¡Gracias! Su respuesta se ha registrado correctamente.")
