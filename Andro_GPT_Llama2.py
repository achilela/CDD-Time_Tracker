import streamlit as st
import datetime
import pandas as pd
 
# Sidebar for user input
st.sidebar.header('Insira as Datas do Contracto')
start_date = st.sidebar.text_input('Start Date', '2022-01-01')
end_date = st.sidebar.text_input('End Date', '2022-12-31')
 
# Convert input to datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
today = pd.Timestamp.today().normalize()  # use today's date as reference
 
# Function to calculate working days excluding weekends
def calculate_working_days(start_date, end_date):
    days = (end_date - start_date).days + 1
    weeks = days // 7
    remaining_days = days % 7
    working_days = weeks * 5
    if remaining_days > 0:
        if start_date.weekday() <= end_date.weekday():
            working_days += remaining_days
        else:
            working_days += end_date.weekday() - start_date.weekday()
    return working_days
 
# Calculate total working days
total_working_days = calculate_working_days(start_date, end_date)
 
# Calculate working days worked so far
working_days_so_far = calculate_working_days(start_date, today)
 
# Calculate remaining time
remaining_days = (end_date - today).days
remaining_hours = (end_date - today).seconds // 3600
remaining_months = (end_date.year - today.year) * 12 + (end_date.month - today.month)
 
# Display results
st.header('CDD - Forecast Dias Trabalhados')
st.write(f'Total de Dias de Trabalho: {total_working_days}')
st.write(f'Dias Trabalhados: {working_days_so_far}')
st.write(f'Meses por Completar: {remaining_months}')
st.write(f'Dias por Completar: {remaining_days}')
st.write(f'Horas por Completar: {remaining_hours}')
