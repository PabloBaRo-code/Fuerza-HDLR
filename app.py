# =============================================================================
# BIBLIOTECA DE FUERZA - HIJOS DE LA RESISTENCIA
# =============================================================================
# Instalación de dependencias (ejecutar en terminal):
# pip install streamlit pandas openpyxl thefuzz python-Levenshtein
# 
# Para ejecutar la aplicación:
# streamlit run app.py
# =============================================================================

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import re
from thefuzz import fuzz, process

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Biblioteca de Fuerza - HDLR",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# ESTILOS CSS - BRANDING HDLR (Naranja / Negro - Minimalista)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* Importar fuente moderna Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* =============================================================================
       HDLR BRANDING SYSTEM
       ============================================================================= */
    :root {
        --hdlr-black: #000000;
        --hdlr-dark-gray: #121212;
        --hdlr-blue: #0045fd;
        --hdlr-light-blue: #009bf7;
        --hdlr-white: #ffffff;
        --hdlr-gray: #888888;
        --hdlr-border: #333333;
    }

    /* Fondo general - Negro Puro */
    .stApp {
        background-color: var(--hdlr-black);
    }
    
    /* =============================================================================
       TYPOGRAPHY
       ============================================================================= */
    h1, h2, h3 {
        color: var(--hdlr-white);
        font-weight: 800;
        letter-spacing: -0.02em;
        text-transform: uppercase;
    }

    .main-header-container {
        text-align: center;
        padding: 2rem 0 3rem 0;
        border-bottom: 1px solid var(--hdlr-border);
        margin-bottom: 2rem;
        background: linear-gradient(180deg, rgba(0,69,253,0.1) 0%, rgba(0,0,0,0) 100%);
    }

    .brand-title {
        font-size: 3rem;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(90deg, #fff, #888);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
    }

    .brand-subtitle {
        font-size: 1.2rem;
        color: var(--hdlr-blue);
        font-weight: 700;
        letter-spacing: 0.2em;
        margin-top: 0.5rem;
        text-transform: uppercase;
    }

    /* =============================================================================
       COMPONENTS
       ============================================================================= */
    
    /* Exercise Cards */
    .exercise-card {
        background: var(--hdlr-dark-gray);
        border: 1px solid var(--hdlr-border);
        border-left: 4px solid var(--hdlr-border);
        border-radius: 4px; /* Más cuadrado, más técnico */
        padding: 1.5rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .exercise-card:hover {
        border-left-color: var(--hdlr-blue);
        transform: translateX(5px);
        box-shadow: -10px 0 20px -10px rgba(0, 69, 253, 0.2);
    }
    
    .exercise-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--hdlr-white);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Tags */
    .tags-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        margin-bottom: 1.2rem;
    }
    
    .tag {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        padding: 0.3rem 0.8rem;
        border-radius: 2px;
        letter-spacing: 0.05em;
    }
    
    .tag-grupo { background: var(--hdlr-blue); color: white; border: 1px solid var(--hdlr-blue); }
    .tag-subgrupo { background: transparent; color: var(--hdlr-light-blue); border: 1px solid var(--hdlr-light-blue); }
    .tag-implicacion { background: #222; color: #ccc; border: 1px solid #333; }
    .tag-material { background: #222; color: #888; border: 1px solid #333; font-style: italic; }

    /* Inputs & Selects */
    .stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
        background-color: var(--hdlr-dark-gray) !important;
        border: 1px solid var(--hdlr-border) !important;
        color: white !important;
        border-radius: 4px !important;
    }
    
    .stTextInput input:focus, .stSelectbox div[data-baseweb="select"] > div:focus-within {
        border-color: var(--hdlr-blue) !important;
        box-shadow: 0 0 0 1px var(--hdlr-blue) !important;
    }

    /* Buttons */
    .stButton > button {
        background: transparent !important;
        border: 2px solid var(--hdlr-blue) !important;
        color: var(--hdlr-blue) !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        border-radius: 0 !important; /* Botones cuadrados estilo técnico */
        padding: 0.5rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: var(--hdlr-blue) !important;
        color: white !important;
        box-shadow: 0 0 15px rgba(0, 69, 253, 0.5) !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #050505;
        border-right: 1px solid #22c55e; /* Cambiado a verde sutil o mantener gris? El usuario pidió azul */
    }
    
    [data-testid="stSidebar"] {
        border-right: 1px solid #222;
    }

    /* Forzar color azul en sidebar */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] .stMetric div,
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: var(--hdlr-blue) !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: var(--hdlr-blue) !important;
        opacity: 0.3;
    }
    
    hr { border-color: #333 !important; }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #000; }
    ::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--hdlr-blue); }
    
    /* Footer & Hidden Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# FUNCIONES DE CARGA DE DATOS
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    """
    Carga el archivo Excel con la estructura de 6 columnas.
    """
    try:
        df = pd.read_excel("Librería HdlR.xlsx")
        
        # Limpiar nombres de columnas
        df.columns = df.columns.str.strip()
        
        # Mapear columnas
        column_mapping = {
            'Implicación ': 'Implicacion',
            'Implicación': 'Implicacion',
            'Enlace ': 'Enlace',
        }
        df = df.rename(columns=column_mapping)
        
        # Asegurar columnas necesarias
        required_cols = ['Grupo', 'Subgrupo', 'Implicacion', 'Ejercicio', 'Enlace', 'Material']
        for col in required_cols:
            if col not in df.columns:
                df[col] = ""
        
        # Limpiar datos
        df = df.fillna("")
        for col in df.columns:
            if df[col].dtype == object:
                df[col] = df[col].astype(str).str.strip()
        
        # Filtrar filas vacías
        df = df[df['Ejercicio'].str.len() > 0]
        
        return df, True
        
    except FileNotFoundError:
        mock_data = {
            'Grupo': ['Fuerza MMII', 'Fuerza MMSS', 'Core'],
            'Subgrupo': ['Sentadilla', 'Empuje', 'Antiextensión'],
            'Implicacion': ['Bilateral', 'Bilateral', 'Bilateral'],
            'Ejercicio': ['Sentadilla Trasera', 'Press Banca', 'Plancha'],
            'Enlace': ['https://youtu.be/example1', 'https://youtu.be/example2', 'https://youtu.be/example3'],
            'Material': ['Barra', 'Barra', 'Sin material']
        }
        return pd.DataFrame(mock_data), False

# -----------------------------------------------------------------------------
# FUNCIONES DE UTILIDAD
# -----------------------------------------------------------------------------
def extract_youtube_id(url):
    """Extrae el ID del video de YouTube."""
    if not url or not isinstance(url, str) or url == "":
        return None
    
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def fuzzy_search(query, df, threshold=50):
    """Búsqueda difusa en el DataFrame."""
    if not query or query.strip() == "":
        return df
    
    query = query.strip().lower()
    results = []
    
    for idx, row in df.iterrows():
        scores = [
            fuzz.partial_ratio(query, str(row['Ejercicio']).lower()),
            fuzz.partial_ratio(query, str(row['Grupo']).lower()),
            fuzz.partial_ratio(query, str(row['Subgrupo']).lower()),
            fuzz.partial_ratio(query, str(row['Material']).lower())
        ]
        max_score = max(scores)
        
        if max_score >= threshold:
            results.append((idx, max_score))
    
    results.sort(key=lambda x: x[1], reverse=True)
    
    if results:
        return df.loc[[r[0] for r in results]]
    return pd.DataFrame()

def get_suggestions(query, df, limit=5):
    """Genera sugerencias de autocompletado."""
    if not query or len(query) < 2:
        return []
    
    all_terms = set()
    all_terms.update(df['Ejercicio'].unique())
    all_terms.update(df['Grupo'].unique())
    all_terms.update(df['Subgrupo'].unique())
    all_terms = [t for t in all_terms if t and str(t).strip()]
    
    matches = process.extract(query, all_terms, scorer=fuzz.partial_ratio, limit=limit)
    return [match[0] for match in matches if match[1] >= 50]

def render_exercise_buttons(exercise_name, video_url, unique_id):
    """
    Renderiza los botones de copiar usando components.html.
    """
    # Escapar caracteres especiales para JavaScript
    escaped_name = exercise_name.replace('\\', '\\\\').replace("'", "\\'").replace('"', '&quot;').replace('`', '\\`')
    escaped_url = video_url.replace('\\', '\\\\').replace("'", "\\'").replace('"', '&quot;').replace('`', '\\`') if video_url else ""
    
    btn_name_id = f"btn_name_{unique_id}"
    btn_url_id = f"btn_url_{unique_id}"
    
    # HTML simplificado solo con los botones de copiar
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', -apple-system, sans-serif; }}
            body {{ background: transparent; overflow: hidden; }}
            .container {{ display: flex; flex-direction: column; gap: 0.5rem; }}
            .btn-row {{ display: flex; gap: 0.5rem; flex-wrap: wrap; }}
            .copy-btn {{
                background: #0045fd; color: white; border: none; padding: 0.5rem 0.8rem;
                border-radius: 6px; cursor: pointer; font-size: 0.7rem; font-weight: 600;
                transition: all 0.2s ease; display: inline-flex; align-items: center; gap: 0.3rem;
                text-transform: uppercase; letter-spacing: 0.02em;
            }}
            .copy-btn:hover {{ background: #009bf7; transform: translateY(-1px); }}
            .copy-btn.copied {{ background: #22c55e !important; }}
            .link-btn {{
                background: transparent; color: #009bf7; border: 1px solid #0045fd;
                padding: 0.5rem 0.8rem; border-radius: 6px; cursor: pointer; font-size: 0.7rem;
                font-weight: 600; transition: all 0.2s ease; text-decoration: none;
                display: inline-flex; align-items: center; gap: 0.3rem;
                text-transform: uppercase; letter-spacing: 0.02em;
            }}
            .link-btn:hover {{ background: #0045fd; color: white; }}
            .link-btn.copied {{ background: #22c55e !important; color: white !important; border-color: #22c55e !important; }}
            .url-display {{
                margin-top: 0.2rem; font-family: monospace; font-size: 0.65rem;
                color: #666; word-break: break-all; max-width: 100%;
                white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="btn-row">
                <button id="{btn_name_id}" class="copy-btn" onclick="copyText('{escaped_name}', '{btn_name_id}')">
                    📋 Copiar nombre
                </button>
                <button id="{btn_url_id}" class="link-btn" onclick="copyText('{escaped_url}', '{btn_url_id}')">
                    🔗 Copiar enlace
                </button>
            </div>
            <div class="url-display">{video_url}</div>
        </div>
        <script>
            function copyText(text, btnId) {{
                const btn = document.getElementById(btnId);
                const originalText = btn.innerHTML;
                
                if (navigator.clipboard && navigator.clipboard.writeText) {{
                    navigator.clipboard.writeText(text).then(function() {{
                        btn.innerHTML = '✅ Copiado!';
                        btn.classList.add('copied');
                        setTimeout(function() {{ 
                            btn.innerHTML = originalText; 
                            btn.classList.remove('copied');
                        }}, 1500);
                    }}).catch(function() {{
                        fallbackCopy(text, btn, originalText);
                    }});
                }} else {{
                    fallbackCopy(text, btn, originalText);
                }}
            }}
            
            function fallbackCopy(text, btn, originalText) {{
                const textArea = document.createElement('textarea');
                textArea.value = text;
                textArea.style.position = 'fixed';
                textArea.style.left = '-9999px';
                document.body.appendChild(textArea);
                textArea.focus();
                textArea.select();
                try {{
                    document.execCommand('copy');
                    btn.innerHTML = '✅ Copiado!';
                    btn.classList.add('copied');
                    setTimeout(function() {{ 
                        btn.innerHTML = originalText;
                        btn.classList.remove('copied');
                    }}, 1500);
                }} catch (err) {{
                    btn.innerHTML = '❌ Error';
                    setTimeout(function() {{ btn.innerHTML = originalText; }}, 1500);
                }}
                document.body.removeChild(textArea);
            }}
        </script>
    </body>
    </html>
    '''
    return html_content

# -----------------------------------------------------------------------------
# INTERFAZ PRINCIPAL
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# GESTIÓN DE ESTADO (RUTINA)
# -----------------------------------------------------------------------------
if 'routine' not in st.session_state:
    st.session_state.routine = []

def add_to_routine(exercise_row):
    """Añade un ejercicio a la rutina evitando duplicados exactos."""
    # Convertir row a dict para serialización
    exercise_data = exercise_row.to_dict()
    # Chequear duplicados por nombre
    names = [e['Ejercicio'] for e in st.session_state.routine]
    if exercise_data['Ejercicio'] not in names:
        st.session_state.routine.append(exercise_data)
        st.toast(f"✅ Añadido: {exercise_data['Ejercicio']}", icon="💪")
    else:
        st.toast(f"⚠️ Ya está en la rutina: {exercise_data['Ejercicio']}", icon="👀")

def remove_from_routine(index):
    """Elimina un ejercicio de la rutina por índice."""
    if 0 <= index < len(st.session_state.routine):
        removed = st.session_state.routine.pop(index)
        st.toast(f"🗑️ Eliminado: {removed['Ejercicio']}", icon="👋")

# -----------------------------------------------------------------------------
# INTERFAZ PRINCIPAL
# -----------------------------------------------------------------------------
def main():
    df, from_excel = load_data()
    
    # Título principal - HDLR Branding
    # Cabecera con Logo o Texto Estilizado
    st.markdown('''
        <div class="main-header-container">
            <!-- Poner aquí <img src="URL_DEL_LOGO" width="200" style="margin-bottom: 1rem;"> si se tiene el logo -->
            <h1 class="brand-title">HIJOS DE LA<br>RESISTENCIA</h1>
            <div class="brand-subtitle">BIBLIOTECA DE FUERZA</div>
        </div>
    ''', unsafe_allow_html=True)
    
    # Botón para mostrar filtros (útil cuando el sidebar está colapsado)
    col_spacer, col_btn, col_spacer2 = st.columns([2, 1, 2])
    with col_btn:
        if st.button("🎯 Mostrar Filtros", help="Abre el panel de filtros", use_container_width=True):
            # Mostrar instrucción clara
            st.toast("👆 Haz clic en '>' en la esquina superior izquierda", icon="🎯")
            
            # Intentar abrir con JavaScript
            components.html('''
                <script>
                (function() {
                    var parent = window.parent.document;
                    
                    // Buscar el botón de expandir sidebar
                    var selectors = [
                        '[data-testid="collapsedControl"]',
                        '[data-testid="stSidebarCollapsedControl"]', 
                        'button[aria-label="Open sidebar"]',
                        '[data-testid="stSidebarNav"] button',
                        '.stSidebar button'
                    ];
                    
                    for (var i = 0; i < selectors.length; i++) {
                        var el = parent.querySelector(selectors[i]);
                        if (el) {
                            el.click();
                            return;
                        }
                    }
                    
                    // Fallback: buscar por posición (esquina superior izquierda)
                    var allBtns = parent.querySelectorAll('button');
                    for (var j = 0; j < allBtns.length; j++) {
                        var btn = allBtns[j];
                        var rect = btn.getBoundingClientRect();
                        if (rect.left < 60 && rect.top < 80) {
                            btn.click();
                            return;
                        }
                    }
                })();
                </script>
            ''', height=0, width=0)
    
    # Mostrar tip de atajo de teclado
    st.markdown('<p style="text-align: center; color: #6b7280; font-size: 0.75rem;">💡 Tip: Usa el icono <strong>></strong> en la esquina superior izquierda para mostrar/ocultar filtros</p>', unsafe_allow_html=True)
    
    if not from_excel:
        st.warning("⚠️ Archivo 'Librería HdlR.xlsx' no encontrado. Mostrando datos de ejemplo.")
    
    # -------------------------------------------------------------------------
    # SIDEBAR - FILTROS
    # -------------------------------------------------------------------------
    with st.sidebar:
        st.markdown("### 🎯 Filtros")
        st.markdown("---")
        
        # Filtro de Grupo
        grupos = ["Todos"] + sorted([g for g in df['Grupo'].unique() if g])
        selected_grupo = st.selectbox("📁 Grupo", grupos, index=0)
        
        # Filtro de Subgrupo (dinámico)
        if selected_grupo != "Todos":
            subgrupos_disponibles = df[df['Grupo'] == selected_grupo]['Subgrupo'].unique()
            subgrupos = ["Todos"] + sorted([s for s in subgrupos_disponibles if s])
        else:
            subgrupos = ["Todos"] + sorted([s for s in df['Subgrupo'].unique() if s])
        selected_subgrupo = st.selectbox("📂 Subgrupo", subgrupos, index=0)
        
        # Filtro de Implicación
        implicaciones = ["Todos"] + sorted([i for i in df['Implicacion'].unique() if i])
        selected_implicacion = st.selectbox("↔️ Implicación", implicaciones, index=0)
        
        # Filtro de Material
        materiales = ["Todos"] + sorted([m for m in df['Material'].unique() if m])
        selected_material = st.selectbox("🏋️ Material", materiales, index=0)
        
        st.markdown("---")
        
        # Paginación - OPTIMIZACIÓN DE RENDIMIENTO
        st.markdown("### 📄 Resultados por página")
        results_per_page = st.select_slider(
            "Cantidad",
            options=[10, 20, 30, 50],
            value=20,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### 📊 Estadísticas")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total", len(df))
        with col2:
            st.metric("Grupos", len([g for g in df['Grupo'].unique() if g]))
        
        st.markdown("---")
        st.markdown("##### 💪 Powered by")
        st.markdown("*Hijos de la Resistencia*")
    
    # -------------------------------------------------------------------------
    # LAYOUT 2 COLUMNAS (RESULTADOS vs RUTINA)
    # -------------------------------------------------------------------------
    col_results, col_routine_spacer, col_routine = st.columns([0.65, 0.05, 0.3])
    
    with col_results:
        # -------------------------------------------------------------------------
        # BARRA DE BÚSQUEDA
        # -------------------------------------------------------------------------
        search_query = st.text_input(
            "🔍 Buscar ejercicio...",
            placeholder="Escribe nombre, grupo, subgrupo o material...",
            label_visibility="collapsed"
        )
        
        # Sugerencias
        if search_query and len(search_query) >= 2:
            suggestions = get_suggestions(search_query, df)
            if suggestions:
                st.markdown(f"**💡 Sugerencias:** {' • '.join(suggestions[:4])}")
        
        st.markdown("---")
        
        # -------------------------------------------------------------------------
        # APLICAR FILTROS
        # -------------------------------------------------------------------------
        filtered_df = df.copy()
        
        if selected_grupo != "Todos":
            filtered_df = filtered_df[filtered_df['Grupo'] == selected_grupo]
        
        if selected_subgrupo != "Todos":
            filtered_df = filtered_df[filtered_df['Subgrupo'] == selected_subgrupo]
        
        if selected_implicacion != "Todos":
            filtered_df = filtered_df[filtered_df['Implicacion'] == selected_implicacion]
        
        if selected_material != "Todos":
            filtered_df = filtered_df[filtered_df['Material'] == selected_material]
        
        if search_query:
            filtered_df = fuzzy_search(search_query, filtered_df)
        
        # -------------------------------------------------------------------------
        # PAGINACIÓN
        # -------------------------------------------------------------------------
        total_results = len(filtered_df)
        total_pages = max(1, (total_results + results_per_page - 1) // results_per_page)
        
        # Estado de la página
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 1
        
        # Resetear página si cambian filtros
        if total_results > 0:
            st.session_state.current_page = min(st.session_state.current_page, total_pages)
        
        # -------------------------------------------------------------------------
        # RESULTADOS
        # -------------------------------------------------------------------------
        if total_results == 0:
            st.markdown("""
            <div class="no-results">
                <div class="no-results-icon">🔍</div>
                <h3>No se encontraron resultados</h3>
                <p>Intenta con otra búsqueda o ajusta los filtros</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Header con paginación
            col_info, col_prev, col_page, col_next = st.columns([3, 1, 1, 1])
            
            with col_info:
                st.markdown(f"### 📋 Resultados ({total_results})")
            
            with col_prev:
                if st.button("◀️", disabled=st.session_state.current_page <= 1):
                    st.session_state.current_page -= 1
                    st.rerun()
            
            with col_page:
                st.markdown(f"<div style='text-align:center;'><strong>{st.session_state.current_page}/{total_pages}</strong></div>", unsafe_allow_html=True)
            
            with col_next:
                if st.button("▶️", disabled=st.session_state.current_page >= total_pages):
                    st.session_state.current_page += 1
                    st.rerun()
            
            # Calcular rango de resultados a mostrar
            start_idx = (st.session_state.current_page - 1) * results_per_page
            end_idx = start_idx + results_per_page
            page_df = filtered_df.iloc[start_idx:end_idx]
            
            # Mostrar ejercicios
            for idx, row in page_df.iterrows():
                exercise_name = row['Ejercicio']
                video_url = row['Enlace']
                video_id = extract_youtube_id(video_url)
                unique_id = f"ex_{idx}"
                
                # Tarjeta Container
                st.markdown('<div class="exercise-card">', unsafe_allow_html=True)
                
                # Fila Header: Título + Botón Añadir
                c_head_title, c_head_add = st.columns([0.85, 0.15])
                with c_head_title:
                     st.markdown(f'<div class="exercise-title">💪 {exercise_name}</div>', unsafe_allow_html=True)
                with c_head_add:
                    if st.button("➕", key=f"add_{unique_id}", help="Añadir a mi Rutina"):
                        add_to_routine(row)
                
                # Tags (Opcional: mover debajo del video o mantener arriba)
                tags_html = '<div class="tags-container">'
                if row['Grupo']:
                    tags_html += f'<span class="tag tag-grupo">{row["Grupo"]}</span>'
                if row['Subgrupo']:
                    tags_html += f'<span class="tag tag-subgrupo">{row["Subgrupo"]}</span>'
                if row['Implicacion']:
                    tags_html += f'<span class="tag tag-implicacion">{row["Implicacion"]}</span>'
                if row['Material']:
                    tags_html += f'<span class="tag tag-material">{row["Material"]}</span>'
                tags_html += '</div>'
                st.markdown(tags_html, unsafe_allow_html=True)
                
                # Contenido principal: Video y Botones
                col_vid, col_btns = st.columns([1.2, 1])
                
                with col_vid:
                    if video_url:
                        st.video(video_url)
                    else:
                        st.markdown('<div style="height: 150px; background: #1a1a1a; display: flex; align-items: center; justify-content: center; color: #666; border-radius: 8px;">📹 Sin video</div>', unsafe_allow_html=True)
                
                with col_btns:
                    # Renderizar botones de copiar
                    html_content = render_exercise_buttons(exercise_name, video_url, unique_id)
                    components.html(html_content, height=100, scrolling=False)
                
                st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # COLUMNA DERECHA: CONSTRUCTOR DE RUTINA
    # -------------------------------------------------------------------------
    with col_routine:
        st.markdown("""
        <div style="background: #121212; border: 1px solid #333; border-radius: 8px; padding: 1rem; position: sticky; top: 2rem;">
            <h3 style="color: #0045fd; margin-bottom: 1rem; border-bottom: 1px solid #333; padding-bottom: 0.5rem;">
                📝 Mi Rutina
            </h3>
        """, unsafe_allow_html=True)
        
        routine_len = len(st.session_state.routine)
        
        if routine_len == 0:
            st.info("Añade ejercicios pulsando el botón ➕ en las tarjetas.")
        else:
            st.markdown(f"**Total: {routine_len} ejercicios**")
            
            # Lista de ejercicios en la rutina
            for i, item in enumerate(st.session_state.routine):
                with st.expander(f"{i+1}. {item['Ejercicio']}", expanded=False):
                    st.caption(f"{item['Grupo']} - {item['Subgrupo']}")
                    if st.button("🗑️ Quitar", key=f"rm_{i}"):
                        remove_from_routine(i)
                        st.rerun()
            
            st.markdown("---")
            if st.button("Limpiar Rutina", type="primary", use_container_width=True):
                st.session_state.routine = []
                st.rerun()
            
            # Generar texto para copiar
            routine_text = f"MI RUTINA HDLR ({routine_len} ejercicios):\n\n"
            for i, item in enumerate(st.session_state.routine):
                routine_text += f"{i+1}. {item['Ejercicio']} ({item['Subgrupo']})\n{item['Enlace']}\n\n"
            
            st.text_area("Copiar lista:", value=routine_text, height=150, help="Copia esto para WhatsApp o Notas")
        
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# EJECUTAR APLICACIÓN
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
