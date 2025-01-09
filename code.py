import streamlit as st
import random
from datetime import datetime, timedelta
import pandas as pd

def add_minutes(start_time, minutes):
    start_time = datetime.strptime(start_time, "%H:%M")
    end_time = start_time + timedelta(minutes=minutes)
    return end_time.strftime("%H:%M")

def generate_schedule(num_days, periods, labs, ppt, smp, add_per, sp, remaining_classes, sub, start_time, period_length):
    result_list = []

    for i in range(1, num_days + 1):
        inner_list = []
        for j in range(1, 5):
            inner_list.append(j)
        inner_list.append("Break")
        for j in range(5, 8):
            inner_list.append(j)
        result_list.append(inner_list)

    for i in labs:
        day = random.randint(0, num_days - 1)
        while result_list[day][5] in labs:
            day = random.randint(0, num_days - 1)
        result_list[day][5] = result_list[day][6] = result_list[day][7] = i

    for i in ppt:
        day = random.randint(0, num_days - 1)
        while result_list[day][0] in ppt or result_list[day][5] in labs:
            day = random.randint(0, num_days - 1)
        result_list[day][0] = result_list[day][1] = i

    for i in smp:
        day = random.randint(0, num_days - 1)
        while result_list[day][2] in smp or result_list[day][5] in labs or result_list[day][0] in ppt:
            day = random.randint(0, num_days - 1)
        result_list[day][2] = result_list[day][3] = i

    for i in add_per:
        day = random.randint(0, num_days - 1)
        while result_list[day][3] in add_per or result_list[day][2] in smp:
            day = random.randint(0, num_days - 1)
        result_list[day][3] = i

    day = random.randint(0, num_days - 1)
    while result_list[day][7] in labs:
        day = random.randint(0, num_days - 1)
    result_list[day][7] = sp

    d = {}
    for i in range(5):
        a = sub[i]
        d[a] = 0

    for day in result_list:
        assigned_subjects = set()
        for index, period in enumerate(day):
            if period not in labs and period not in ppt and period not in smp and period not in add_per and period != sp and period != "Break":
                subject_key = sub[random.randint(0, 4)]

                while subject_key in assigned_subjects or d[subject_key] < 5:
                    subject_key = sub[random.randint(0, 4)]
                    d[subject_key] += 1

                day[index] = subject_key
                assigned_subjects.add(subject_key)

    columns = ["Day"] + [f"Period {i}" for i in range(1, periods + 1)]
    schedule_df = pd.DataFrame(columns=columns)

    #days = {i + 1: f"Day {i + 1}" for i in range(num_days)}
    days = {1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday", 5:"Friday", 6:"Saturday"}
    current_time = datetime.strptime(start_time, "%H:%M")
    time_columns = []
    for _ in range(periods):
        time_columns.append(f"{current_time.strftime('%H:%M')} - {add_minutes(current_time.strftime('%H:%M'), period_length)}")
        current_time = current_time + timedelta(minutes=period_length)

    schedule_df.loc[0] = ["Time/Day"] + time_columns

    for day_index, day in enumerate(result_list, start=1):
        day_data = [days[day_index]]
        for period in day:
            day_data.append(period)
        schedule_df.loc[day_index] = day_data

    excel_filename = "MLRIT_Time_Table.xlsx"
    schedule_df.to_excel(excel_filename, index=False, header=True)

    return f"Class details exported to {excel_filename}"

def main():
    st.title("MLRIT Time Table Generator")

    num_days = st.slider("Number of Working Days", min_value=1, max_value=7, value=6)
    periods = st.slider("Number of Periods per Day", min_value=1, max_value=10, value=8)

    labs = st.text_area("Labs (Enter lab names separated by space)").split()
    ppt = st.text_area("PPT Sessions (Enter PPT names separated by space)").split()
    smp = st.text_area("Seminar and Projects Sessions (Enter names separated by space)").split()
    add_per = st.text_area("Additional Subjects Sessions (Enter names separated by space)").split()
    sp = st.text_input("Sports Period")
    remaining_classes = st.slider("Number of Remaining Classes", min_value=1, max_value=30, value=24)
    sub = st.text_area("Subjects Sessions (Enter names separated by space)").split()

    start_time = st.text_input("Starting-Time(HH:MM)", value="09:20")
    period_length = st.slider("Period Length (in minutes)", min_value=1, max_value=120, value=50)

    if st.button("Generate Schedule"):
        result = generate_schedule(num_days, periods, labs, ppt, smp, add_per, sp, remaining_classes, sub, start_time, period_length)
        st.success(result)

if __name__ == "__main__":
    main()