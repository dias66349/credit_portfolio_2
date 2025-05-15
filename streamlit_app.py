import streamlit as st
import pandas as pd




credit_df=pd.read_excel(r"credit products.xlsx")


zalog_codes=credit_df[credit_df['product_type']=='Залоговый кредит']['product_code'].to_list()
ipoteka_codes=credit_df[credit_df['product_type']=='Ипотека']['product_code'].to_list()
nn_codes=credit_df[credit_df['product_type']=='НН']['product_code'].to_list()
auto_codes=credit_df[credit_df['product_type']=='Автокредит']['product_code'].to_list()
express_codes=credit_df[credit_df['product_type']=='Экспресс кредит']['product_code'].to_list()
tovar_codes=credit_df[credit_df['product_type']=='Товарный кредит']['product_code'].to_list()

import openai  

client_api = openai.OpenAI(api_key=st.secrets['OPENAI_API_KEY']) 


# Streamlit интерфейс
st.title("Генератор SQL по таблице credit_portfolio")

user_text = st.text_area("Введите запрос на естественном языке:", "Выведи топ 10 тех у кого был наибольший платёж по авто кредиту в марте 2024 года")

if st.button("Сгенерировать SQL"):

    final_prompt = f"""
    Ты — генератор SQL-запросов по таблице credit_portfolio, которая ежедневно обновляется в ForteBank.

    Описание таблицы credit_portfolio:
    - Каждая строка отражает статус одного и того же контракта **на определённую дату** (act_date).
    - Если контракт открыт, он будет присутствовать **в каждой дате** от open_date до закрытия (close_date или liquidate_date), даже если уже погашен.
    - Таким образом, в таблице ежедневно представлены все кредиты: открытые и уже закрытые — с их актуальными статусами.

    Столбцы таблицы:
    • act_date (date) — дата записи; каждый контракт появляется в каждой дате от open_date до coalesce(liquidate_date,close_date), даже если уже закрыт  
    • contract_number (varchar) — номер контракта; у одного bin_iin может быть несколько контрактов  
    • bin_iin (varchar) — БИН/ИИН клиента  
    • agreem_state (varchar) — статус (Например, «Погашен», «Актуален», «Отказ Банком» и т.д.)  
    • contract_amount (numeric) —  это изначальная сумма кредита, она одинакова для всех дат одного и того же контракта, поэтому если нужно агрегировать по contract_amount, используй только одну строку на контракт
    • open_date (date) — дата открытия  
    • close_date (date) — дата закрытия 
    • liquidate_date (date) — дата досрочной ликвидации (может быть NULL)  
    • currency (varchar) — валюта  
    • sign_restructing (varchar) — была ли реструктуризация (1/0)  
    • branch_code (varchar) — код филиала  
    • branch_name (varchar) — название филиала  
    • loan_purpose_code (varchar) — код цели кредита  
    • loan_purpose_name (varchar) — название цели (покупка, строительство и т.д.)  
    • collector_company (varchar) — коллекторская компания  
    • product_code (varchar) — код продукта  
    • product_name (varchar) — название продукта  
    • interest_rate (numeric) — ставка  
    • eff_interest_rate (numeric) — эффективная ставка  
    • delay_count_main (integer) — просрочка по телу (дней), 
    • delay_count_percent (integer) — просрочка по процентам (дней)  
    • balance_main_dbt_amt_in_lcl_ccy (numeric) — остаток долга в тенге  
    • balance_int_amt_in_lcl_ccy (numeric) — сумма последнего платежа в тенге  
    • next_payment_date (date) — дата следующего платежа  
    • z_good (varchar) — сегмент клиента: Good_bank, Heritage, Stressful  

    product_code для каждого кредитного продукта
    – Экспресс кредиты = {express_codes} 
    – Авто кредиты= {auto_codes}
    – Залоговые кредиты = {zalog_codes}
    – Ипотечные кредиты = {ipoteka_codes}
    – Товарные кредиты = {tovar_codes}

    Типы agreem_state: (
        "Продан (закрыт)", "Отказ заемщика от займа", "Клиент отказался от кредита",
        "Отказ Банком", "Передан на совершение испол.надписи", "Актуален",
        "Передан в суд", "Списан долг", "Договор завершен",
        "Отсутствует на источнике", "Прощен", "Продан", "Погашен",
        "Отказ от кредита", "Списан", "Погашен по решению суда",
        "Удалён физически", "Реф по ГП", "Погашен ГП", "Завершение",
        "Удален", "Договор введен", "Отказ Заемщиком", "Списаны проценты",
        "Отказ заемщиком", "Зарегистрирован", "Графики рассчитаны", "Введен"
    )

    ВСЕ branch_name: (
        'Филиал АО "ForteBank" в г. Атырау',
        'Филиал АО "ForteBank" в г. Караганда',
        'Филиал АО "ForteBank" в г.Уральск',
        'Филиал АО "ForteBank" в г. Екибастуз',
        'Филиал Акционерного Общества ForteBank в городе Астана',
        'Филиал АО "ForteBank" в г. Шымкент',
        'Филиал АО "ForteBank" в г. Талдыкорган',
        'Филиал АО "ForteBank" в г. Кызылорда',
        'Филиал АО "ForteBank" в г. Каскелен',
        'Филиал АО  "ForteBank" в г. Алматы',
        'Филиал АО "ForteBank" в г. Туркестан',
        'Филиал АО "ForteBank" в г. Усть-Каменогорск',
        'Филиал АО "ForteBank" г. Актау',
        'Филиал АО "ForteBank" в г. Семей',
        'Филиал АО "ForteBank" в г. Павлодар',
        'Филиал АО "ForteBank" в г. Тараз',
        'Акционерное общество "ForteBank"',
        'Филиал АО "ForteBank" в г. Актобе',
        'Филиал АО "ForteBank" в г. Костанай',
        'Филиал АО "ForteBank" в г. Кокшетау',
        'Филиал АО "ForteBank" в г. Петропавловск'
    )

    Правила генерации SQL:
    - Всегда используй act_date для фильтрации по дате (например, `act_date BETWEEN '2025-03-01' AND '2025-03-31'`)
    - Учитывай, что одни и те же контракты появляются в таблице ежедневно с их текущим статусом
    - Чтобы не дублировать контракты, всегда используй `COUNT(DISTINCT contract_number)` или `DISTINCT` там, где нужно
    - Если не говориться а каком-то определённом виде кредита то не фильтруй по  product_code
    - **Сделай всё в одном SQL-запросе**
    -Если указано "максимальная просрочка N дней", то нужно: взять максимальное из delay_count_main и delay_count_percent
    - если нужно вытащить сумму оставшегося долга за какой то период то надо брать минимум 
    - в столбцах delay_count_main, delay_count_percent null значит просрочки нет,а просрочка начинается с 0  

    Теперь подумай хорошо и ответь на данный вопрос: {user_text}
    """


    final_response = client_api.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an NLP-to-SQL generator for a daily-updated credit_portfolio table in ForteBank. "},
            {"role": "user", "content": final_prompt}
        ],
        temperature=0
    )
    final_result = final_response.choices[0].message.content.strip()


    st.code(final_result, language="sql")
