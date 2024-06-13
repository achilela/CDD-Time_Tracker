import streamlit as st
from datetime import datetime, date, timedelta
import pandas as pd
import time

# Streamlit app configuration
st.set_page_config(page_title="Contrato de Duração Determinada - CDD", layout="wide")

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

def display_clock(remaining_days, remaining_hours):
    total_seconds = remaining_hours * 3600
    days = remaining_days
    ph = st.sidebar.empty()
    while total_seconds > 0:
        hours, rem = divmod(total_seconds, 3600)
        mins, secs = divmod(rem, 60)
        clock_str = f"""
        <div style="display: flex; justify-content: center; align-items: center; font-size: 18px; font-weight: bold;">
            <div style="text-align: center; margin: 0 10px;">
                <div style="font-size: 27px;">{days:02d}</div>
                <div style="font-size: 12px;">Dias</div>
            </div>
            <div style="text-align: center; margin: 0 10px;">
                <div style="font-size: 27px;">{hours:02d}</div>
                <div style="font-size: 12px;">Horas</div>
            </div>
            <div style="text-align: center; margin: 0 10px;">
                <div style="font-size: 27px;">{mins:02d}</div>
                <div style="font-size: 12px;">Minutos</div>
            </div>
            <div style="text-align: center; margin: 0 10px;">
                <div style="font-size: 27px;">{secs:02d}</div>
                <div style="font-size: 12px;">Segundos</div>
            </div>
        </div>
        """
        ph.markdown(clock_str, unsafe_allow_html=True)
        time.sleep(1)
        total_seconds -= 1
        if hours == 0 and mins == 0 and secs == 0:
            days -= 1

# Sidebar inputs
st.sidebar.markdown("### Data do Contrato")
start_date = st.sidebar.date_input("Data de Início", date(2024, 3, 22))
end_date = st.sidebar.date_input("Data de Término", date(2029, 3, 22))

# Use the current date as today's date
today_date = date.today()

# Calculate the working days, months, and hours
total_working_days = calculate_working_days(start_date, end_date)
total_working_months = days_to_months(total_working_days)
total_working_hours = days_to_hours(total_working_days)
worked_days = calculate_worked_days(start_date, today_date)
worked_hours = days_to_hours(worked_days)
worked_months = days_to_months(worked_days)

remaining_days = total_working_days - worked_days
remaining_months = days_to_months(remaining_days)
remaining_hours = days_to_hours(remaining_days)

data = {
    'Categoria': ['Duração', 'Dias Trabalhados', 'Dias Restantes'],
    'Dias': [total_working_days, worked_days, remaining_days],
    'Meses': [total_working_months, worked_months, remaining_months],
    'Horas': [total_working_hours, worked_hours, remaining_hours],
}

df = pd.DataFrame(data)
df = df[['Categoria', 'Dias', 'Meses', 'Horas']]

# Center the table on the main canvas and reduce the width
st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
st.table(df.style.set_table_styles([
    {'selector': 'th', 'props': [('text-align', 'center'), ('font-size', '16px')]},
    {'selector': 'td', 'props': [('text-align', 'center'), ('font-size', '16px')]}
]))
st.markdown("</div>", unsafe_allow_html=True)

# Start the countdown clock automatically
display_clock(remaining_days, remaining_hours)

# Chatbot Interface
st.markdown("<h2 style='font-size: 24px;'>Assistente de Contratos</h2>", unsafe_allow_html=True)
user_input = st.text_input("Insira a dúvida que pretendes esclarecer...")
if user_input:
    # Process the user input and generate a response
    # You can add your chatbot logic here
    response = "Esta é uma resposta automática, não leve em consideração."
    st.write(response)

# Custom CSS style to limit the width of the chat window
st.markdown(
    """
    <style>
    .stContainer {
        max-width: 200px;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)