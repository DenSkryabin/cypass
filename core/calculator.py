import datetime

def compute_engine(end_d, trips_list, start_d, bcs_d):
    """
    Основной алгоритмический движок расчёта периодов натурализации.
    
    Параметры:
    - end_d: планируемая дата подачи (E56)
    - trips_list: список поездок со столбцами Arrival, Departure, Country
    - start_d: дата первой легальной регистрации / ARC (I9)
    - bcs_d: дата перехода на рабочий статус BCS (I18)
    """
    # -------------------------------------------------------------
    # БЛОК 1: Очистка входных данных от пустых строк
    # -------------------------------------------------------------
    clean_trips = []
    for row in trips_list:
        arr = row.get("Arrival")
        dep = row.get("Departure")
        # Пропускаем пустые или незаполненные строки
        if not arr or not dep:
            continue
        clean_trips.append({
            "arr": arr, 
            "dep": dep, 
            "country": row.get("Country", "Cyprus")
        })
    
    # Если поездок нет, возвращаем пустой результат
    if not clean_trips:
        return None

    # Сортируем поездки в хронологическом порядке по дате прилета
    clean_trips.sort(key=lambda x: x["arr"])
    
    # Фиксируем окончание последней поездки датой подачи
    clean_trips[-1]["dep"] = end_d

    # -------------------------------------------------------------
    # БЛОК 2: Склеивание смежных интервалов пребывания
    # -------------------------------------------------------------
    # Если предыдущая дата выезда совпадает со следующей датой въезда,
    # объединяем их в единый непрерывный интервал проживания
    merged = []
    for t in clean_trips:
        if merged and merged[-1]["dep"] == t["arr"] and merged[-1]["country"] == t["country"]:
            merged[-1]["dep"] = t["dep"]
        else:
            merged.append(dict(t))

    # Вычисляем количество полных 365-дневных периодов от даты ARC
    total_days_span = (end_d - start_d).days
    num_periods = max(1, total_days_span // 365)

    # -------------------------------------------------------------
    # БЛОК 3: Нарезка интервалов пребывания на 365-дневные окна
    # -------------------------------------------------------------
    split_trips = [dict(t) for t in merged]
    # Формируем список контрольных дат отсечки назад во времени
    cut_dates = [end_d - datetime.timedelta(days=k * 365) for k in range(1, num_periods + 1)]
    
    for cd in cut_dates:
        temp_splits = []
        for t in split_trips:
            # Если граница года падает внутрь пребывания на Кипре — режем интервал
            if t["arr"] < cd < t["dep"]:
                temp_splits.append({"arr": t["arr"], "dep": cd, "country": t["country"]})
                temp_splits.append({"arr": cd, "dep": t["dep"], "country": t["country"]})
            else:
                temp_splits.append(t)
        split_trips = temp_splits

    # -------------------------------------------------------------
    # БЛОК 4: Подсчет дней отсутствия между поездками (Столбец B)
    # -------------------------------------------------------------
    for i in range(len(split_trips)):
        if i == 0:
            split_trips[i]["absence"] = 0
        else:
            # Дни отсутствия = разница между въездом текущей поездки и выездом предыдущей
            split_trips[i]["absence"] = (split_trips[i]["arr"] - split_trips[i-1]["dep"]).days

    # -------------------------------------------------------------
    # БЛОК 5: Агрегация данных по каждому 365-дневному периоду
    # -------------------------------------------------------------
    period_rows = []
    total_excess_days = 0

    for p in range(1, num_periods + 1):
        p_end = end_d - datetime.timedelta(days=(p - 1) * 365)
        p_start = end_d - datetime.timedelta(days=p * 365)

        start_idx = None
        end_idx = None
        
        # Находим строки, попадающие в текущее 365-дневное окно
        for idx, t in enumerate(split_trips):
            if t["arr"] >= p_start and start_idx is None:
                start_idx = idx
            if t["dep"] <= p_end:
                end_idx = idx

        # Суммируем дни отсутствия в окне (аналог формулы СУММ(B...:B...) в Excel)
        if start_idx is not None and end_idx is not None and end_idx >= start_idx:
            abs_sum = sum(split_trips[k]["absence"] for k in range(start_idx + 1, end_idx + 1))
        else:
            abs_sum = 0

        # Вычисляем превышение лимита 90 дней (аналог формулы ЕСЛИ(F>90; F-90; 0))
        excess = max(0, abs_sum - 90)
        total_excess_days += excess

        period_rows.append({
            "Период": f"Год {p} ({(p-1)*12}–{p*12} мес назад)",
            "Даты периода": f"{p_start.strftime('%d.%m.%Y')} — {p_end.strftime('%d.%m.%Y')}",
            "Дней отсутствия (F)": abs_sum,
            "Превышение 90 дней (G)": excess,
            "Статус": "✅ В норме" if excess == 0 else f"⚠️ Превышение на {excess} дн."
        })

    # Фактическое суммарное физическое присутствие на Кипре
    presence_days = sum(
        (min(t["dep"], end_d) - max(t["arr"], start_d)).days 
        for t in merged 
        if min(t["dep"], end_d) > max(t["arr"], start_d)
    )

    # Сценарий 1: Учет списания разрешенных 90 дней в год как присутствие (строка 70 Excel)
    days_scenario1 = presence_days + min(num_periods * 90, 450)
    
    return period_rows, presence_days, num_periods, total_excess_days, days_scenario1