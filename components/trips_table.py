import streamlit as st
import datetime

def render_trips_input(calc_engine_func):
    """
    Отрисовка реестра ВНЖ, таблицы поездок и расчет результатов.
    
    Параметр calc_engine_func передает функцию compute_engine из calculator.py.
    """
    st.subheader("Реестр разрешений на проживание (Титулы / ВНЖ)")
    
    visas_initial = [
        {"Статус": "ARC (Первая регистрация)", "Выдано": datetime.date(2022, 5, 6), "Истекает": datetime.date(2023, 5, 5), "Категория": "Visitor"},
        {"Статус": "Visitor Permit (Продление)", "Выдано": datetime.date(2023, 5, 6), "Истекает": datetime.date(2024, 5, 5), "Категория": "Visitor"},
        {"Статус": "Visitor Permit (3-й год)", "Выдано": datetime.date(2024, 5, 6), "Истекает": datetime.date(2024, 10, 24), "Категория": "Visitor"},
        {"Статус": "Receipt MBCS (Старт BCS)", "Выдано": datetime.date(2024, 10, 25), "Истекает": datetime.date(2025, 4, 25), "Категория": "BCS Work"},
        {"Статус": "BCS Work Permit", "Выдано": datetime.date(2025, 4, 26), "Истекает": datetime.date(2027, 4, 25), "Категория": "BCS Work"},
    ]

    col_v1, col_v2 = st.columns([3, 2])
    with col_v1:
        edited_visas = st.data_editor(visas_initial, num_rows="dynamic", use_container_width=True)
    with col_v2:
        st.markdown("#### Параметры заявителя")
        arc_date_val = datetime.date(2022, 5, 6)
        bcs_date_val = datetime.date(2024, 10, 25)
        
        target_sub_date = st.date_input(
            "Планируемая дата подачи (E56):", 
            value=datetime.date(2027, 7, 5),
            format="DD/MM/YYYY"
        )
        req_presence_days = 1460 # 4 года суммарно (3 BCS + 1 год) при сертификате B1
        st.write(f"**Дата ARC:** {arc_date_val.strftime('%d.%m.%Y')}")
        st.write(f"**Старт списания 90 дней (BCS):** {bcs_date_val.strftime('%d.%m.%Y')}")
        st.write(f"**Требуемый ценз присутствия:** {req_presence_days} дней")

    st.write("---")
    st.subheader("Журнал поездок и непрерывного пребывания")
    st.caption("Формат ввода дат: ДД.ММ.ГГГГ")

    default_trips = [
        {"Arrival": datetime.date(2022, 5, 6), "Departure": datetime.date(2022, 5, 12), "Country": "Cyprus"},
        {"Arrival": datetime.date(2022, 8, 8), "Departure": datetime.date(2022, 11, 12), "Country": "Cyprus"},
        {"Arrival": datetime.date(2022, 11, 15), "Departure": datetime.date(2022, 12, 2), "Country": "Cyprus"},
        {"Arrival": datetime.date(2022, 12, 8), "Departure": datetime.date(2022, 12, 26), "Country": "Cyprus"},
        {"Arrival": datetime.date(2022, 12, 29), "Departure": datetime.date(2023, 1, 3), "Country": "Cyprus"},
        {"Arrival": datetime.date(2023, 1, 12), "Departure": datetime.date(2023, 1, 15), "Country": "Cyprus"},
        {"Arrival": datetime.date(2023, 1, 18), "Departure": datetime.date(2023, 4, 3), "Country": "Cyprus"},
        {"Arrival": datetime.date(2023, 4, 5), "Departure": datetime.date(2023, 5, 2), "Country": "Cyprus"},
        {"Arrival": datetime.date(2023, 5, 4), "Departure": datetime.date(2023, 5, 24), "Country": "Cyprus"},
        {"Arrival": datetime.date(2023, 5, 28), "Departure": datetime.date(2023, 6, 1), "Country": "Cyprus"},
        {"Arrival": datetime.date(2023, 6, 4), "Departure": datetime.date(2023, 6, 8), "Country": "Cyprus"},
        {"Arrival": datetime.date(2023, 6, 12), "Departure": datetime.date(2023, 6, 24), "Country": "Cyprus"},
        {"Arrival": datetime.date(2023, 6, 25), "Departure": datetime.date(2023, 7, 17), "Country": "Cyprus"},
        {"Arrival": datetime.date(2023, 7, 23), "Departure": datetime.date(2023, 8, 30), "Country": "Cyprus"},
        {"Arrival": datetime.date(2023, 9, 3), "Departure": datetime.date(2023, 9, 26), "Country": "Cyprus"},
        {"Arrival": datetime.date(2023, 10, 3), "Departure": datetime.date(2023, 11, 9), "Country": "Cyprus"},
        {"Arrival": datetime.date(2023, 11, 18), "Departure": datetime.date(2023, 12, 17), "Country": "Cyprus"},
        {"Arrival": datetime.date(2023, 12, 21), "Departure": datetime.date(2024, 1, 8), "Country": "Cyprus"},
        {"Arrival": datetime.date(2024, 1, 29), "Departure": datetime.date(2024, 3, 12), "Country": "Cyprus"},
        {"Arrival": datetime.date(2024, 3, 22), "Departure": datetime.date(2024, 5, 5), "Country": "Cyprus"},
        {"Arrival": datetime.date(2024, 5, 6), "Departure": datetime.date(2024, 5, 6), "Country": "Cyprus"},
        {"Arrival": datetime.date(2024, 5, 9), "Departure": datetime.date(2024, 5, 18), "Country": "Cyprus"},
        {"Arrival": datetime.date(2024, 5, 21), "Departure": datetime.date(2024, 5, 30), "Country": "Cyprus"},
        {"Arrival": datetime.date(2024, 5, 31), "Departure": datetime.date(2024, 7, 4), "Country": "Cyprus"},
        {"Arrival": datetime.date(2024, 7, 30), "Departure": datetime.date(2024, 8, 21), "Country": "Cyprus"},
        {"Arrival": datetime.date(2024, 9, 5), "Departure": datetime.date(2024, 10, 4), "Country": "Cyprus"},
        {"Arrival": datetime.date(2024, 10, 7), "Departure": datetime.date(2024, 10, 21), "Country": "Cyprus"},
        {"Arrival": datetime.date(2024, 10, 24), "Departure": datetime.date(2024, 11, 8), "Country": "Cyprus"},
        {"Arrival": datetime.date(2024, 11, 29), "Departure": datetime.date(2024, 12, 28), "Country": "Cyprus"},
        {"Arrival": datetime.date(2025, 1, 5), "Departure": datetime.date(2025, 1, 23), "Country": "Cyprus"},
        {"Arrival": datetime.date(2025, 1, 28), "Departure": datetime.date(2025, 2, 14), "Country": "Cyprus"},
        {"Arrival": datetime.date(2025, 2, 19), "Departure": datetime.date(2025, 4, 9), "Country": "Cyprus"},
        {"Arrival": datetime.date(2025, 5, 5), "Departure": datetime.date(2025, 7, 18), "Country": "Cyprus"},
        {"Arrival": datetime.date(2025, 8, 26), "Departure": datetime.date(2025, 11, 12), "Country": "Cyprus"},
        {"Arrival": datetime.date(2025, 11, 16), "Departure": datetime.date(2025, 11, 20), "Country": "Cyprus"},
        {"Arrival": datetime.date(2025, 11, 22), "Departure": datetime.date(2026, 3, 30), "Country": "Cyprus"},
        {"Arrival": datetime.date(2026, 4, 1), "Departure": datetime.date(2026, 5, 20), "Country": "Cyprus"},
        {"Arrival": datetime.date(2026, 5, 21), "Departure": datetime.date(2026, 6, 11), "Country": "Cyprus"},
        {"Arrival": datetime.date(2026, 6, 13), "Departure": datetime.date(2026, 6, 27), "Country": "Cyprus"},
        {"Arrival": datetime.date(2026, 7, 1), "Departure": datetime.date(2026, 8, 1), "Country": "Cyprus"},
        {"Arrival": datetime.date(2026, 8, 25), "Departure": datetime.date(2026, 8, 29), "Country": "Cyprus"},
        {"Arrival": datetime.date(2026, 9, 5), "Departure": datetime.date(2026, 9, 19), "Country": "Cyprus"},
        {"Arrival": datetime.date(2026, 9, 20), "Departure": target_sub_date, "Country": "Cyprus"},
    ]

    edited_trips = st.data_editor(
        default_trips, 
        num_rows="dynamic", 
        use_container_width=True,
        column_config={
            "Arrival": st.column_config.DateColumn("Дата прибытия", format="DD/MM/YYYY"),
            "Departure": st.column_config.DateColumn("Дата выезда", format="DD/MM/YYYY"),
            "Country": st.column_config.TextColumn("Страна")
        }
    )

    # Запуск расчёта через ядро
    result = calc_engine_func(target_sub_date, edited_trips, arc_date_val, bcs_date_val)
    
    if result:
        period_rows, presence_days, num_periods, excess_days, scen1_days = result

        st.write("---")
        st.subheader("Сценарии готовности к подаче (строки 68–74 Excel)")

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Фактическое присутствие", f"{presence_days} дн.", f"Норма: {req_presence_days} дн.")
        col_m2.metric("Сценарий 1 (с зачетом 90 дн)", f"{scen1_days} дн.", f"Дельта: {scen1_days - req_presence_days} дн.")
        col_m3.metric("Штрафные дни (>90 дн/год)", f"{excess_days} дн.")
        
        # Расчет дефицита дней и защитного интервала (+30 дней)
        deficit = max(0, req_presence_days - presence_days)
        possible_date = target_sub_date + datetime.timedelta(days=deficit)
        safety_date = possible_date + datetime.timedelta(days=30)
        col_m4.metric("Дата с запасом (+30 дней)", safety_date.strftime("%d.%m.%Y"))

        st.table([
            {
                "Сценарий": "Сценарий 1 (Зачет 90 дней отсутствия в год)", 
                "Дней": f"{scen1_days} дн.", 
                "Готовность": "✅ Условие выполнено" if scen1_days >= req_presence_days and excess_days == 0 else "⚠️ Требуется проверка периодов", 
                "Рекомендуемая дата": target_sub_date.strftime("%d.%m.%Y")
            },
            {
                "Сценарий": "Сценарий 2 (Строгое физическое присутствие)", 
                "Дней": f"{presence_days} дн.", 
                "Готовность": f"Не хватает {deficit} дн." if deficit > 0 else "✅ Выполнено", 
                "Рекомендуемая дата": possible_date.strftime("%d.%m.%Y")
            },
            {
                "Сценарий": "Сценарий с запасом безопасности (+30 дней)", 
                "Дней": f"{presence_days + deficit + 30} дн.", 
                "Готовность": "🛡️ Защита от разночтений с офицером миграции", 
                "Рекомендуемая дата": safety_date.strftime("%d.%m.%Y")
            },
        ])

        st.markdown("#### Разбор 365-дневных окон:")
        st.table(period_rows)
        
        return edited_trips, target_sub_date, arc_date_val, bcs_date_val
    
    return None, target_sub_date, arc_date_val, bcs_date_val