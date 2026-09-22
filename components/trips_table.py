import streamlit as st
import datetime
import pandas as pd
from core.doc_generator import generate_crmd_statements_docx

def render_trips_input(calc_engine_func):
    """
    Отрисовка реестра ВНЖ, таблицы поездок, расчета сценариев 
    и блоков экспорта официальных документов CRMD.
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
        edited_visas = st.data_editor(visas_initial, num_rows="dynamic", width="stretch")
        
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
        st.write(f"**Дата отсчета (ARC):** {arc_date_val.strftime('%d.%m.%Y')}")
        st.write(f"**Старт списания 90 дней (BCS):** {bcs_date_val.strftime('%d.%m.%Y')}")
        st.write(f"**Требуемый ценз присутствия:** {req_presence_days} дней")

    st.write("---")
    st.subheader("Журнал поездок и непрерывного пребывания")
    st.caption("Формат ввода дат: ДД.ММ.ГГГГ")

    # -------------------------------------------------------------
    # 1. БЛОК ИМПОРТА EXCEL / CSV
    # -------------------------------------------------------------
    uploaded_file = st.file_uploader(
        "📥 Быстрый импорт поездок (Excel .xlsx или .csv):", 
        type=["xlsx", "csv"],
        help="Загрузите файл с колонками: Arrival (прибытие), Departure (выезд) и Country (страна)"
    )

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

    active_trips = default_trips

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df_up = pd.read_csv(uploaded_file)
            else:
                df_up = pd.read_excel(uploaded_file)
            
            arr_col = next((c for c in df_up.columns if "arriv" in c.lower() or "въезд" in c.lower() or "прибыт" in c.lower()), None)
            dep_col = next((c for c in df_up.columns if "depart" in c.lower() or "выезд" in c.lower() or "убыт" in c.lower()), None)
            country_col = next((c for c in df_up.columns if "countr" in c.lower() or "стран" in c.lower()), None)

            if arr_col and dep_col:
                imported = []
                for _, r in df_up.iterrows():
                    arr_val = pd.to_datetime(r[arr_col], errors="coerce")
                    dep_val = pd.to_datetime(r[dep_col], errors="coerce")
                    if pd.notnull(arr_val) and pd.notnull(dep_val):
                        imported.append({
                            "Arrival": arr_val.date(),
                            "Departure": dep_val.date(),
                            "Country": str(r[country_col]) if country_col and pd.notnull(r[country_col]) else "Cyprus"
                        })
                if imported:
                    active_trips = imported
                    st.success(f"✅ Успешно импортировано {len(imported)} поездок из файла!")
            else:
                st.error("В файле не найдены колонки Arrival/Въезд и Departure/Выезд.")
        except Exception as e:
            st.error(f"Ошибка при чтении файла: {e}")

    edited_trips = st.data_editor(
        active_trips, 
        num_rows="dynamic", 
        width="stretch",
        column_config={
            "Arrival": st.column_config.DateColumn("Дата прибытия", format="DD/MM/YYYY"),
            "Departure": st.column_config.DateColumn("Дата выезда", format="DD/MM/YYYY"),
            "Country": st.column_config.TextColumn("Страна")
        }
    )

    # -------------------------------------------------------------
    # 2. ВЫЗОВ МАТЕМАТИЧЕСКОГО ЯДРА
    # -------------------------------------------------------------
    result = calc_engine_func(target_sub_date, edited_trips, arc_date_val, bcs_date_val)
    
    if result:
        period_rows, presence_days, num_periods, excess_days, scen1_days = result

        st.write("---")
        st.markdown("#### Анализ стажа и готовности кейса")

        deficit = max(0, req_presence_days - presence_days)
        possible_date = target_sub_date + datetime.timedelta(days=deficit)
        safety_date = possible_date + datetime.timedelta(days=30)

        # Легкие минималистичные карточки
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        with col_m1:
            st.markdown(f"""
            <div class="minimal-card">
                <div class="minimal-card-label">Фактическое присутствие</div>
                <div class="minimal-card-value">{presence_days} <span style="font-size: 1rem; font-weight: 400; color: #6b7280;">дн.</span></div>
                <div class="minimal-card-sub" style="color: {'#059669' if presence_days >= req_presence_days else '#dc2626'};">
                    Цель: {req_presence_days} дн. ({'Выполнено' if presence_days >= req_presence_days else f'Дефицит {deficit} дн.'})
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_m2:
            st.markdown(f"""
            <div class="minimal-card">
                <div class="minimal-card-label">Сценарий 1 (с зачетом 90 дн)</div>
                <div class="minimal-card-value">{scen1_days} <span style="font-size: 1rem; font-weight: 400; color: #6b7280;">дн.</span></div>
                <div class="minimal-card-sub">Запас: +{scen1_days - req_presence_days} дн.</div>
            </div>
            """, unsafe_allow_html=True)

        with col_m3:
            badge_text_color = "#059669" if excess_days == 0 else "#dc2626"
            status_txt = "0 дн. (В норме)" if excess_days == 0 else f"+{excess_days} дн."
            st.markdown(f"""
            <div class="minimal-card">
                <div class="minimal-card-label">Превышения (&gt;90 дн/год)</div>
                <div class="minimal-card-value" style="color: {badge_text_color};">{status_txt}</div>
                <div class="minimal-card-sub">Лимит: строго &le; 90 дней</div>
            </div>
            """, unsafe_allow_html=True)

        with col_m4:
            st.markdown(f"""
            <div class="minimal-card">
                <div class="minimal-card-label">Буфер безопасности (+30 дн)</div>
                <div class="minimal-card-value">{safety_date.strftime('%d.%m.%Y')}</div>
                <div class="minimal-card-sub">Рекомендуемая дата подачи</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("##### Сценарии подачи")
        st.table([
            {
                "Сценарий": "Сценарий 1 (Зачет 90 дней отсутствия в год)", 
                "Дней": f"{scen1_days} дн.", 
                "Готовность": "✅ Условие выполнено" if scen1_days >= req_presence_days and excess_days == 0 else "⚠️ Проверить периоды", 
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
                "Готовность": "🛡️ Защита от споров с офицером", 
                "Рекомендуемая дата": safety_date.strftime("%d.%m.%Y")
            },
        ])

        st.markdown("##### Детализация 365-дневных окон")
        st.table(period_rows)

        # -------------------------------------------------------------
        # 3. БЛОК ЭКСПОРТА В МИНИМАЛИСТИЧНОМ СТИЛЕ
        # -------------------------------------------------------------
        st.write("---")
        st.markdown("#### Экспорт данных и официальных бланков")
        
        col_exp1, col_exp2 = st.columns(2)
        
        with col_exp1:
            st.markdown("**Таблица поездок (CSV)**")
            st.caption("Резервная копия поездок. Можно загрузить обратно в калькулятор в любой момент через кнопку импорта.")
            
            df_export = pd.DataFrame(edited_trips)
            csv_data = df_export.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="Скачать CSV",
                data=csv_data,
                file_name=f"cyprus_trips_{target_sub_date.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                width="stretch"
            )

        with col_exp2:
            st.markdown("**Официальные Statement 1 & 2 (.docx)**")
            st.caption("Формуляры по стандарту CRMD с рассчитанными днями присутствия для заявления M127.")
            
            with st.expander("Реквизиты заявителя (для шапки документа)"):
                app_name = st.text_input("Имя и фамилия (латиницей):", value="DENIS SKRYABIN")
                arc_number = st.text_input("Номер ARC:", value="XXX-XXXXX")
                mp_number = st.text_input("Номер папки (MP):", value="AXX-XXXXX")
            
            docx_file = generate_crmd_statements_docx(app_name, arc_number, mp_number, target_sub_date, edited_trips)
            
            st.download_button(
                label="Сгенерировать Statements 1 & 2 (.docx)",
                data=docx_file,
                file_name=f"CRMD_Statements_1_2_{app_name.replace(' ', '_')}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                width="stretch"
            )
        
        return edited_trips, target_sub_date, arc_date_val, bcs_date_val
    
    return None, target_sub_date, arc_date_val, bcs_date_val
