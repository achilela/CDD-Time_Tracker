import streamlit as st
from datetime import datetime, date
import pandas as pd
import time
import threading

def calculate_working_days(start_date, end_date):
    date_range = pd.date_range(start=start_date, end=end_date, freq='B')
    total_working_days = len(date_range)
    return total_working_days

def calculate_worked_days(start_date, today_date):
    date_range = pd.date_range(start=start_date, end=today_date, freq='B')
    worked_days = len(date_range)
    return worked_days

def days_to_months(days):
    return round(days / 30.44, 2)

def days_to_hours(days):
    return days * 8

def countdown_timer(remaining_days, text_placeholder):
    remaining_seconds = remaining_days * 24 * 60 * 60

    def update_text():
        while remaining_seconds > 0:
            days = remaining_seconds // (24 * 60 * 60)
            hours = (remaining_seconds % (24 * 60 * 60)) // (60 * 60)
            minutes = (remaining_seconds % (60 * 60)) // 60
            seconds = remaining_seconds % 60

            timer_str = f"Time remaining: {days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}"
            text_placeholder.markdown(f"<h2 style='text-align:center;'>{timer_str}</h2>", unsafe_allow_html=True)

            time.sleep(1)  # Delay for 1 second
            remaining_seconds -= 1

        text_placeholder.markdown("<h2 style='text-align:center;'>Time's up!</h2>", unsafe_allow_html=True)

    thread = threading.Thread(target=update_text)
    thread.start()

# Streamlit app
st.set_page_config(page_title="Calculadora de Dias de Trabalho", layout="wide")

# Sidebar
st.sidebar.title("Dados do Contrato")
start_date = st.sidebar.date_input("Data de Início", value=date(2023, 1, 1))
end_date = st.sidebar.date_input("Data de Término", value=date(2023, 12, 31))
today_date = date.today()

# Main content
st.markdown("<h1 style='text-align:center;'>Calculadora de Dias de Trabalho</h1>", unsafe_allow_html=True)

total_working_days = calculate_working_days(start_date, end_date)
total_working_months = days_to_months(total_working_days)
total_working_hours = days_to_hours(total_working_days)

worked_days = calculate_worked_days(start_date, today_date)
worked_hours = days_to_hours(worked_days)

remaining_days = total_working_days - worked_days
remaining_months = days_to_months(remaining_days)
remaining_hours = days_to_hours(remaining_days)

data = {
    'Category': ['Total de Dias de Trabalho', 'Dias Trabalhados', 'Dias Restantes'],
    'Dias': [total_working_days, worked_days, remaining_days],
    'Meses': [total_working_months, '', remaining_months],
    'Horas': [total_working_hours, worked_hours, remaining_hours],
}

df = pd.DataFrame(data)
df = df.reset_index()
df = df[['Category', 'Dias', 'Meses', 'Horas']]
st.table(df)

col1, col2 = st.columns(2)

with col2:
    if st.button("Start Countdown"):
        text_placeholder = st.empty()
        countdown_timer(remaining_days, text_placeholder)
