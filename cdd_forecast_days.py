import streamlit as st
from datetime import datetime, date
import pandas as pd
import time

# Streamlit app configuration
st.set_page_config(page_title="CDD Duraçao Contractual", layout="wide")

# Functions
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

def countdown_timer(end_date, end_time, ph):
    end_datetime = datetime.combine(end_date, end_time)
    current_datetime = datetime.now()

    if end_datetime > current_datetime:
        difference = end_datetime - current_datetime
        total_seconds = difference.total_seconds()

        for secs in range(int(total_seconds), 0, -1):
            days, rem = divmod(secs, 86400)
            hours, rem = divmod(rem, 3600)
            mins, secs = divmod(rem, 60)

            countdown_str = f"""
            <div style="display: flex; justify-content: center; align-items: center; font-size: 36px; font-weight: bold;">
                <div style="text-align: center; margin: 0 10px;">
                    <div style="font-size: 24px;">Dias</div>
                    <div>{days:02d}</div>
                </div>
                <div style="text-align: center; margin: 0 10px;">
                    <div style="font-size: 24px;">Horas</div>
                    <div>{hours:02d}</div>
                </div>
                <div style="text-align: center; margin: 0 10px;">
                    <div style="font-size: 24px;">Minutos</div>
                    <div>{mins:02d}</div>
                </div>
                <div style="text-align: center; margin: 0 10px;">
                    <div style="font-size: 24px;">Segundos</div>
                    <div>{secs:02d}</div>
                </div>
            </div>
            """

            ph.markdown(countdown_str, unsafe_allow_html=True)
            time.sleep(1)

        st.success("Countdown finished!")
    else:
        st.error("Please select a future date and time.")

# Sidebar
st.sidebar.title("Datas do Contrato")
start_date = st.sidebar.date_input("Data de Início", value=date(2024, 3, 22))
end_date = st.sidebar.date_input("Data de Término", value=date(2029, 3, 22))
today_date = date.today()

# Main content
st.markdown("<h1 style='text-align:center;'>CDD Duraçao Contractual</h1>", unsafe_allow_html=True)

total_working_days = calculate_working_days(start_date, end_date)
total_working_months = days_to_months(total_working_days)
total_working_hours = days_to_hours(total_working_days)

worked_days = calculate_worked_days(start_date, today_date)
worked_hours = days_to_hours(worked_days)

remaining_days = total_working_days - worked_days
remaining_months = days_to_months(remaining_days)
remaining_hours = days_to_hours(remaining_days)

data = {
    'Categoria': ['Duracao', 'Dias Trabalhados', 'Dias Restantes'],
    'Dias': [total_working_days, worked_days, remaining_days],
    'Meses': [total_working_months, '', remaining_months],
    'Horas': [total_working_hours, worked_hours, remaining_hours],
}

df = pd.DataFrame(data)
df = df.reset_index()
df = df[['Categoria', 'Dias', 'Meses', 'Horas']]
st.table(df)

col1, col2 = st.columns(2)

with col2:
    end_time = st.time_input("Select the time on the future date:", value=datetime.now().time())
    if st.button("Start Countdown"):
        text_placeholder = st.empty()
        countdown_timer(end_date, end_time, text_placeholder)