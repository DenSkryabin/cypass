import streamlit as st
import datetime

# -------------------------------------------------------------
# Импорт модулей
# -------------------------------------------------------------
from core.calculator import compute_engine
from components.checklist import render_checklist
from components.trips_table import render_trips_input
from components.optimizer import render_optimizer

# Конфигурация страницы
st.set_page_config(
    page_title="CyPass.cy — Гражданство и статус резидента Кипра",
    page_icon="🇨🇾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------------------
# СОВРЕМЕННЫЙ ДИЗАЙН И КАСТОМНЫЙ CSS
# -------------------------------------------------------------
st.markdown("""
<style>
    /* Подключение чистого шрифта Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Фон рабочей области */
    .stApp {
        background-color: #f8fafc;
    }

    /* Главный хедер */
    .hero-header {
        background: linear-gradient(135deg, #0d3b66 0%, #00509d 100%);
        padding: 32px 36px;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(13, 59, 102, 0.15);
    }
    .hero-header h1 {
        color: white !important;
        font-size: 2.1rem !important;
        font-weight: 700 !important;
        margin-bottom: 8px !important;
    }
    .hero-header p {
        color: #e0eafc !important;
        font-size: 1.05rem !important;
        margin: 0 !important;
    }

    /* Карточки метрик и блоков */
    .custom-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 22px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
        margin-bottom: 18px;
    }

    /* Стилизация табов (вкладок) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #edf2f7;
        padding: 6px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 500;
        color: #4a5568;
        background-color: transparent;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: #00509d !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
        font-weight: 600;
    }

    /* Бейджи статусов */
    .badge-success {
        background-color: #def7ec;
        color: #03543f;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    .badge-warning {
        background-color: #fef08a;
        color: #713f12;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }

    /* Кнопки */
    .stButton>button {
        background: linear-gradient(180deg, #0066cc 0%, #0052a3 100%);
        color: white;
        font-weight: 600;
        border-radius: 10px;
        padding: 10px 24px;
        border: none;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0,102,204,0.2);
    }
    .stButton>button:hover {
        background: linear-gradient(180deg, #0052a3 0%, #003d7a 100%);
        color: white;
        box-shadow: 0 4px 8px rgba(0,102,204,0.3);
        transform: translateY(-1px);
    }

    /* Скрытие стандартного меню Streamlit для чистого вида */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# ВЕРХНИЙ ХЕДЕР В СТИЛЕ СОВРЕМЕННОГО САЙТА
# -------------------------------------------------------------
st.markdown("""
<div class="hero-header">
    <h1>🇨🇾 CyPass.cy — Калькулятор и аудит натурализации</h1>
    <p>Проверка соответствия ст. 111B Закона о населении Кипра (M127), расчет 365-дневных окон и генерация официальных документов.</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# НАВИГАЦИЯ ПО РАЗДЕЛАМ
# -------------------------------------------------------------
tab_calc, tab_check, tab_opt = st.tabs([
    "📅 Калькулятор стажа и документы",
    "📋 Чек-лист соответствия M127", 
    "🎯 Оптимизатор «зеленых окон»"
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
