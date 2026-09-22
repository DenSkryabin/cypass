import streamlit as st
import datetime

# Импорт модулей ядра и компонентов
from core.calculator import compute_engine
from components.checklist import render_checklist
from components.trips_table import render_trips_input
from components.optimizer import render_optimizer

st.set_page_config(
    page_title="CyPass — Cyprus Naturalization Hub",
    page_icon="🇨🇾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------------------
# МИНИМАЛИСТИЧНЫЙ CSS (В СТИЛЕ TREBOIT / CLEAN SAAS)
# -------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    /* Базовая типографика */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1f2937;
    }

    /* Чистый белый фон без темных подложек */
    .stApp {
        background-color: #ffffff;
    }

    /* Убираем лишние верхние отступы Streamlit */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }

    /* Лаконичный заголовок */
    .brand-header {
        margin-bottom: 1.5rem;
        padding-bottom: 1.25rem;
        border-bottom: 1px solid #f3f4f6;
    }
    .brand-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #111827;
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 0;
    }
    .brand-subtitle {
        font-size: 0.92rem;
        color: #6b7280;
        margin-top: 4px;
        margin-bottom: 0;
    }

    /* Минималистичные плоские карточки с тонкой рамкой */
    .minimal-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .minimal-card-label {
        font-size: 0.78rem;
        font-weight: 500;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .minimal-card-value {
        font-size: 1.6rem;
        font-weight: 600;
        color: #111827;
        margin: 2px 0;
    }
    .minimal-card-sub {
        font-size: 0.82rem;
        color: #9ca3af;
    }

    /* Вкладки (Tabs): ультра-лаконичные, плоские */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
        border-bottom: 1px solid #e5e7eb;
        padding: 0;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 4px 12px 4px;
        font-size: 0.95rem;
        font-weight: 500;
        color: #6b7280;
        background-color: transparent;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0;
    }
    .stTabs [aria-selected="true"] {
        color: #111827 !important;
        border-bottom: 2px solid #2563eb !important;
        background-color: transparent !important;
        font-weight: 600;
    }

    /* Таблицы: чистые линии без лишней заливки */
    table {
        border-collapse: collapse;
        width: 100%;
        font-size: 0.9rem;
    }
    th {
        border-bottom: 1px solid #e5e7eb !important;
        color: #4b5563 !important;
        font-weight: 600 !important;
        padding: 10px !important;
        background: #f9fafb !important;
    }
    td {
        border-bottom: 1px solid #f3f4f6 !important;
        padding: 10px !important;
        color: #1f2937 !important;
    }

    /* Кнопки: плоский чистый стиль */
    .stButton>button, .stDownloadButton>button {
        background-color: #111827;
        color: #ffffff;
        border: 1px solid #111827;
        border-radius: 6px;
        font-size: 0.88rem;
        font-weight: 500;
        padding: 7px 16px;
        transition: all 0.15s ease;
        box-shadow: none;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        background-color: #374151;
        border-color: #374151;
        color: #ffffff;
    }

    /* Убираем служебные элементы Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# ХЕДЕР В СТИЛЕ МИНИМАЛИЗМА
# -------------------------------------------------------------
st.markdown("""
<div class="brand-header">
    <div class="brand-title">
        <span>🇨🇾 CyPass.cy</span>
        <span style="font-size: 0.8rem; font-weight: 500; background: #eff6ff; color: #2563eb; padding: 2px 8px; border-radius: 4px;">M127 / Art. 111B</span>
    </div>
    <div class="brand-subtitle">Калькулятор периодов проживания на Кипре и генератор официальных заявлений в CRMD.</div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# ТАБЫ
# -------------------------------------------------------------
tab_calc, tab_check, tab_opt = st.tabs([
    "Калькулятор стажа",
    "Чек-лист документов", 
    "Оптимизатор даты"
])

with tab_calc:
    trips_data, target_date, arc_date, bcs_date = render_trips_input(compute_engine)

with tab_check:
    render_checklist()

with tab_opt:
    if trips_data is not None:
        render_optimizer(compute_engine, trips_data, target_date, arc_date, bcs_date)
    else:
        st.info("Сначала настройте параметры дат во вкладке калькулятора.")
