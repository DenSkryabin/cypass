import streamlit as st
import datetime

# -------------------------------------------------------------
# Импорт изолированных модулей приложения
# -------------------------------------------------------------
from core.calculator import compute_engine
from components.checklist import render_checklist
from components.trips_table import render_trips_input
from components.optimizer import render_optimizer

# Конфигурация страницы Streamlit
st.set_page_config(
    page_title="Cyprus Naturalization Platform (M127 / BCS)",
    page_icon="🇨🇾",
    layout="wide"
)

# Заголовок приложения
st.title("🇨🇾 Аудит готовности к гражданству Кипра (ст. 111B / M127)")
st.caption("Официальные критерии Civil Registry and Migration Department для специалистов BCS и членов их семей.")

# Создание основных вкладок
tab_check, tab_calc, tab_opt = st.tabs([
    "📋 Комплексный чек-лист M127", 
    "📅 Калькулятор стажа и 365-дневных окон", 
    "🎯 Оптимизатор даты подачи"
])

# Вкладка 1: Интерактивный чек-лист
with tab_check:
    render_checklist()

# Вкладка 2: Таблицы дат, расчет сценариев
with tab_calc:
    trips_data, target_date, arc_date, bcs_date = render_trips_input(compute_engine)

# Вкладка 3: Оптимизатор окон
with tab_opt:
    if trips_data is not None:
        render_optimizer(compute_engine, trips_data, target_date, arc_date, bcs_date)
    else:
        st.info("Сначала настройте поездки на вкладке калькулятора.")