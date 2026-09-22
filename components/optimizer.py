import streamlit as st
import datetime

def render_optimizer(calc_engine_func, trips_list, target_d, arc_d, bcs_d):
    """
    Сканирование дат подачи и нахождение непрерывных окон без превышений.
    """
    st.subheader("Автоматический подбор даты подачи без превышений")
    st.write("Алгоритм сканирует окно ±180 дней вокруг выбранной даты и группирует периоды, где **в каждом из годов отсутствие строго ≤ 90 дней**:")

    if st.button("🔍 Начать поиск безопасных окон подачи"):
        with st.spinner("Анализ календаря и нарезка интервалов..."):
            valid_dates = []
            
            # Перебор смещений от -180 до +180 дней
            for offset in range(-180, 181):
                test_date = target_d + datetime.timedelta(days=offset)
                res = calc_engine_func(test_date, trips_list, arc_d, bcs_d)
                # Если суммарное превышение (индекс 3) равно 0 — дата подходит
                if res and res[3] == 0:
                    valid_dates.append(test_date)

            if valid_dates:
                # Группировка отдельных дат в непрерывные временные интервалы
                corridors = []
                c_start = valid_dates[0]
                c_prev = valid_dates[0]
                for d in valid_dates[1:]:
                    if (d - c_prev).days == 1:
                        c_prev = d
                    else:
                        corridors.append((c_start, c_prev))
                        c_start = d
                        c_prev = d
                corridors.append((c_start, c_prev))

                st.success(f"Найдено {len(corridors)} безопасных «зеленых коридоров» для подачи документов!")
                
                for idx, (ws, we) in enumerate(corridors, 1):
                    days_length = (we - ws).days + 1
                    with st.expander(f"🟢 Коридор #{idx}: с {ws.strftime('%d.%m.%Y')} по {we.strftime('%d.%m.%Y')} (всего {days_length} дн.)", expanded=True):
                        st.write(f"При выборе любой даты в этом интервале превышение лимита 90 дней во всех периодах равно **0**.")
            else:
                st.warning("В диапазоне ±180 дней полностью безопасных дат не обнаружено.")