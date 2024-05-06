import streamlit as st
import datetime
import pandas as pd
 
# Sidebar for user input
st.sidebar.header('Datas do Contrato')
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
 
# Calculate remaining working days
remaining_working_days = total_working_days - working_days_so_far
 
# Convert remaining working days to months and hours
remaining_months = remaining_working_days / 30  # approximate conversion to months
remaining_hours = remaining_working_days * 8  # convert to hours assuming 8 hours per day
 
# Calculate total worked hours
total_worked_hours = total_working_days * 8  # convert to hours assuming 8 hours per day
 
# Calculate remaining hours
remaining_hours -= total_worked_hours
 
# Display results
st.header('Results')
st.write(f'Total de Dias de Trabalho: {total_working_days}')
st.write(f'Dias ja Trabalhados: {working_days_so_far}')
st.write(f'Dias Restantes de Trabalho: {remaining_working_days}')
st.write(f'Meses Restantes de Trabalho: {remaining_months:.1f}')
st.write(f'Total de horas ja Trabalhadas: {remaining_hours}')
st.write(f'Horas Restantes de Trabalho: {total_worked_hours}')
