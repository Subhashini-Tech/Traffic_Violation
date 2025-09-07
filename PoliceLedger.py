import pandas as pd
import streamlit as st
import mysql.connector as db
import matplotlib.pyplot as plt
import seaborn as sns
import base64


side = st.sidebar.radio(
    "Navigation",
    ["HOME", "SUMMARY", "VIOLATION DETAILS", "QUICK LOOKUPS","PREDICT OUTCOMES"]
)

# Data file
data = pd.read_csv(r"C:\Users\Admin\traffic_ledger.csv")
new_data = data
new_data.drop(['driver_age_raw','violation_raw','search_type'], axis = 1,inplace = True)

val = [tuple(x) for x in new_data.values]

# Connect to the data base
connection = db.connect(

                host = "localhost",
                user = "root",
                password = "root123",
                autocommit = True
                )
# Create currsor
cur = connection.cursor()
# Query - Create DB
db = """
    create database if NOT EXISTS new_proj
"""
tab = """
    create table if NOT EXISTS new_proj.newtab (
    stop_date date,
    stop_time time,
    country_name varchar (40),
    driver_gender varchar(10),
    driver_age int(3),
    driver_race varchar(20),
    violation varchar(30),
    search_conducted Boolean,
    stop_outcome varchar(30),
    is_arrested Boolean,
    stop_duration varchar(60),
    drugs_related_stop Boolean,
    vehicle_number varchar(25)
    )
"""
s1 = """
    select * from new_proj.newtab
"""
ins = """
    insert into new_proj.newtab (
        stop_date, stop_time, country_name, driver_gender,
        driver_age, driver_race, violation, search_conducted,
        stop_outcome, is_arrested, stop_duration,
        drugs_related_stop, vehicle_number
    )
    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
# Execute Query
cur.execute(db)
cur.execute(tab)
#cur.executemany(ins,val)

# Back ground image
def set_bg(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# On choosing sidebar navigation
if side == "HOME":
    set_bg("D:/Project1/tp-3.jpg")
    st.markdown("""
    <h1 style="text-align: center;">TRAFFIC VIOLATION LEDGER</h1>
    <h2 style="text-align: center;"> WELCOME!</h2>   
    <h3 style="text-align: center;">This application focuses on maintaining comprehensive logs of individuals who have violated traffic rules.
                 It records and organizes detailed information about each violation, including the type of offense, date and time of occurrence, location, associated penalties, halt time, vehicle information, gender and age of the offenders.
                 The system helps authorities manage and review traffic violations efficiently. </h3> 
    
    </style>               
    """,unsafe_allow_html=True)
elif side == "SUMMARY":
    set_bg("D:/Project1/tp-3.jpg")
    st.markdown("""<h3 style="text-align: center;">SUMMARY OF TRAFFIC VIOLATION</h3>""",unsafe_allow_html=True)
    v1 = pd.read_sql(s1, con = connection)
    v1
elif side == "VIOLATION DETAILS":
    set_bg("D:/Project1/tp-3.jpg")
    st.markdown("""<h3 style="text-align: center;">VIOLATION DETAILS</h3>""",unsafe_allow_html=True)
# Vehicle Based
    vd = st.selectbox("Vehicle Based", [
        "Select the required",
        "What are the top 10 vehicle_Number involved in drug-related stops?",
        "Which vehicles were most frequently searched?"
    ])
    if vd == "What are the top 10 vehicle_Number involved in drug-related stops?":
        query1 = """
            SELECT vehicle_number 
            FROM new_proj.newtab 
            WHERE drugs_related_stop = 1 
              AND stop_outcome = "Arrest" 
              AND stop_duration = "30+ Min" 
              AND search_conducted = 1 
              AND is_arrested = 1 
            ORDER BY stop_date DESC 
            LIMIT 10;
        """
        result1 = pd.read_sql(query1, con = connection)
        result1
    elif vd == "Which vehicles were most frequently searched?":
        query2 = """
            SELECT vehicle_number
            FROM new_proj.newtab
            GROUP BY vehicle_number 
            ORDER BY COUNT(*) DESC
            LIMIT 1;
        """
        result2 = pd.read_sql(query2, con = connection)
        result2
# Driver Based
    drb = st.selectbox("Driver Based", [
        "Select the required",
        "Which driver age group had the highest arrest rate?",
        "What is the gender distribution of drivers stopped in each country?",
        "Which race and gender combination has the highest search rate?"
    ])
    if drb == "Which driver age group had the highest arrest rate?":
        query3 = """
            SELECT age_group, COUNT(*) AS total_arrests
            FROM (
                SELECT 
                    driver_age,
                    IF(driver_age BETWEEN 18 AND 25, '18 to 25',
                        IF(driver_age BETWEEN 26 AND 40, '26 to 40',
                            IF(driver_age BETWEEN 41 AND 60, '41 to 60',
                                IF(driver_age BETWEEN 61 AND 80, '61 to 80', '81+')
                            )
                        )
                    ) AS age_group
                FROM new_proj.newtab
                WHERE is_arrested = 1
            ) AS Q1
            GROUP BY age_group
            ORDER BY total_arrests DESC
            LIMIT 1;
        """
        result3 = pd.read_sql(query3, con = connection)
        result3

    elif drb == "What is the gender distribution of drivers stopped in each country?":
        query4 = """
            SELECT country_name, driver_gender, COUNT(*) AS Driver_Count 
            FROM new_proj.newtab 
            GROUP BY driver_gender, country_name 
            ORDER BY Driver_Count DESC;
        """
        result4 = pd.read_sql(query4, con = connection)
        result4

    elif drb == "Which race and gender combination has the highest search rate?":
        query5 = """
            SELECT driver_race, driver_gender, COUNT(*) AS Driver_Count 
            FROM new_proj.newtab 
            WHERE search_conducted = 1 
            GROUP BY driver_gender, driver_race 
            ORDER BY Driver_Count DESC;
        """
        result5 = pd.read_sql(query5, con = connection)
        result5
# Time Based
    tb = st.selectbox("Time Based", [
        "Select the required",
        "What time of day sees the most traffic stops?",
        "What is the average stop duration for different violations?",
        "Are stops during the night more likely to lead to arrests?"
    ])
    if tb == "What time of day sees the most traffic stops?":
        query6 = """
            SELECT COUNT(*) AS NoOf_Stops, stop_time 
            FROM new_proj.newtab 
            GROUP BY stop_time 
            ORDER BY NoOf_Stops DESC 
            LIMIT 1;
        """
        result6 = pd.read_sql(query6, con = connection)
        result6
    elif tb == "What is the average stop duration for different violations?":
        query7 = """
            SELECT violation, AVG(stop_duration) AS Avg_Stop_Duration 
            FROM new_proj.newtab 
            GROUP BY violation 
            ORDER BY Avg_Stop_Duration DESC;
        """
        result7 = pd.read_sql(query7, con = connection)
        result7
    elif tb == "Are stops during the night more likely to lead to arrests?":
        query8 = """
            SELECT
                CASE 
                    WHEN stop_time BETWEEN '04:00:00' AND '18:00:00' THEN 'DAY'
                    ELSE 'NIGHT'
                END AS Timings,
                COUNT(*) AS total_Stops
            FROM new_proj.newtab
            WHERE is_arrested = 1
            GROUP BY Timings
            ORDER BY total_Stops DESC;
        """
        result8 = pd.read_sql(query8, con = connection)
        result8
# Violation Based
    vb = st.selectbox("Violation Based", [
        "Select the required",
        "Most common violation among searched or arrested drivers",
        "Most common violation among drivers under 25",
        "Least common violation among drivers neither searched nor arrested"
    ])
    if vb == "Most common violation among searched or arrested drivers":
        query9 = """
            SELECT violation, COUNT(violation) AS Occurance 
            FROM new_proj.newtab
            WHERE search_conducted = 1 OR is_arrested = 1 
            GROUP BY violation 
            ORDER BY Occurance DESC 
            LIMIT 1;
        """
        result9 = pd.read_sql(query9, con = connection)
        result9
    elif vb == "Most common violation among drivers under 25":
        query10 = """
            SELECT violation, COUNT(violation) AS Occurance 
            FROM new_proj.newtab
            WHERE driver_age < 25 
            GROUP BY violation 
            ORDER BY Occurance DESC 
            LIMIT 1;
        """
        result10 = pd.read_sql(query10, con = connection)
        result10
    elif vb == "Least common violation among drivers neither searched nor arrested":
        query11 = """
            SELECT violation, COUNT(violation) AS Occurance 
            FROM new_proj.newtab
            WHERE search_conducted = 0 AND is_arrested = 0 
            GROUP BY violation 
            ORDER BY Occurance ASC 
            LIMIT 1;
        """
        result11 = pd.read_sql(query11, con = connection)
        result11
# Location Based
    lb = st.selectbox("Location Based", [
        "Select the required",
        "Which countries report the highest rate of drug-related stops?",
        "What is the arrest rate by country and violation?",
        "Which country has the most stops with search conducted?"
    ])
    if lb == "Which countries report the highest rate of drug-related stops?":
        query12 = """
            SELECT country_name, COUNT(country_name) AS Occurance 
            FROM new_proj.newtab
            WHERE drugs_related_stop = 1 
            GROUP BY country_name 
            ORDER BY Occurance DESC 
            LIMIT 1;
        """
        result12 = pd.read_sql(query12, con = connection)
        result12
    elif lb == "What is the arrest rate by country and violation?":
        query13 = """
            SELECT country_name, violation, COUNT(violation) AS No_Of_People,
                   ROUND(100.0 * SUM(is_arrested) / COUNT(*), 2) AS Arrest_rate_percent 
            FROM new_proj.newtab
            GROUP BY country_name, violation 
            ORDER BY country_name ASC, Arrest_rate_percent DESC;
        """
        result13 = pd.read_sql(query13, con = connection)
        result13
    elif lb == "Which country has the most stops with search conducted?":
        query14 = """
            SELECT country_name, COUNT(country_name) AS No_Of_Stops  
            FROM new_proj.newtab 
            WHERE search_conducted = 1 
            GROUP BY country_name 
            ORDER BY No_Of_Stops DESC 
            LIMIT 1;
        """
        result14 = pd.read_sql(query14, con = connection)
        result14

elif side == "QUICK LOOKUPS":
    set_bg("D:/Project1/tp-3.jpg")
    st.markdown("""<h3 style="text-align: center;">QUICK LOOKUPS</h3>""",unsafe_allow_html=True)
    ql = st.selectbox("Choose a Quick Lookup", [
        "Select the required",
        "Yearly Breakdown of Stops and Arrests by Country",
        "Driver Violation Trends Based on Age and Race",
        "Time Period Analysis of Stops by Year - Month - Hour of the Day",
        "Violations with High Search and Arrest Rates",
        "Driver Demographics by Country (Age, Gender, and Race)",
        "Top 5 Violations with Highest Arrest Rates"
    ])
    if ql == "Yearly Breakdown of Stops and Arrests by Country":
        query15 = """
            SELECT stop_year, country_name, No_of_Arrests,
                   RANK() OVER (PARTITION BY stop_year ORDER BY No_of_Arrests DESC) AS Rank_of_Arrests 
            FROM (
                SELECT country_name, DATE_FORMAT(stop_date,'%Y') AS stop_year, COUNT(*) AS No_of_Arrests 
                FROM new_proj.newtab
                WHERE is_arrested = 1 
                GROUP BY DATE_FORMAT(stop_date,'%Y'), country_name
            ) AS y1 
            ORDER BY Rank_of_Arrests ASC;
        """
        result15 = pd.read_sql(query15, con = connection)
        result15
    elif ql == "Driver Violation Trends Based on Age and Race":
        query16 = """
            SELECT sq.age_group, sq.driver_race, t1.violation, COUNT(t1.violation) AS No_of_People 
            FROM (
                SELECT *,
                    IF(driver_age BETWEEN 18 AND 25, '18 to 25',
                        IF(driver_age BETWEEN 26 AND 40, '26 to 40',
                            IF(driver_age BETWEEN 41 AND 60, '41 to 60',
                                IF(driver_age BETWEEN 61 AND 80, '61 to 80', '81+')
                            )
                        )
                    ) AS age_group
                FROM new_proj.newtab
                WHERE is_arrested = 1
            ) AS sq
            INNER JOIN new_proj.newtab t1
                ON sq.vehicle_number = t1.vehicle_number
            GROUP BY sq.age_group, sq.driver_race, t1.violation
            ORDER BY age_group;
        """
        result16 = pd.read_sql(query16, con = connection)
        result16
    elif ql == "Time Period Analysis of Stops by Year - Month - Hour of the Day":
        query17 = """
            SELECT 
                y.year_detail,
                y.No_of_Stops AS year_stops,
                m.month_detail,
                m.No_of_Stops AS month_stops,
                h.hour_detail,
                h.No_of_Stops AS hour_stops 
            FROM (
                SELECT DATE_FORMAT(stop_date, '%Y') AS year_detail, COUNT(*) AS No_of_Stops
                FROM new_proj.newtab
                GROUP BY DATE_FORMAT(stop_date, '%Y')
            ) y
            LEFT JOIN (
                SELECT DATE_FORMAT(stop_date, '%M') AS month_detail, COUNT(*) AS No_of_Stops
                FROM new_proj.newtab
                GROUP BY DATE_FORMAT(stop_date, '%M')
            ) m ON 1=1
            LEFT JOIN (
                SELECT DATE_FORMAT(stop_time, '%H') AS hour_detail, COUNT(*) AS No_of_Stops
                FROM new_proj.newtab
                GROUP BY DATE_FORMAT(stop_time, '%H')
            ) h ON 1=1
            ORDER BY year_detail ASC, month_detail DESC, hour_detail ASC;
        """
        result17 = pd.read_sql(query17, con = connection)
        result17
    elif ql == "Violations with High Search and Arrest Rates":
        query18 = """
            SELECT violation 
            FROM (
                SELECT DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS DENSE_RANK_WINDOW, violation 
                FROM new_proj.newtab
                WHERE search_conducted = 1 AND is_arrested = 1 
                GROUP BY violation
            ) AS DR
            WHERE DENSE_RANK_WINDOW = 1;
        """
        result18 = pd.read_sql(query18, con = connection)
        result18
    elif ql == "Driver Demographics by Country (Age, Gender, and Race)":
        query19 = """
            SELECT age_group, driver_gender, driver_race, COUNT(*) AS No_of_Drivers
            FROM (
                SELECT *,
                    IF(driver_age BETWEEN 18 AND 25, '18 to 25',
                        IF(driver_age BETWEEN 26 AND 40, '26 to 40',
                            IF(driver_age BETWEEN 41 AND 60, '41 to 60',
                                IF(driver_age BETWEEN 61 AND 80, '61 to 80', '81+')
                            )
                        )
                    ) AS age_group
                FROM new_proj.newtab
            ) AS Q1
            GROUP BY age_group, driver_gender, driver_race
            ORDER BY age_group ASC;
        """
        result19 = pd.read_sql(query19, con = connection)
        result19
    elif ql == "Top 5 Violations with Highest Arrest Rates":
        query20 = """
            SELECT violation,
                   SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END) AS arrested_count,
                   COUNT(*) AS total_count, 
                   SUM(CASE WHEN is_arrested = 1 THEN 1 ELSE 0 END)/COUNT(*) *100 AS Rate_of_arrest
            FROM new_proj.newtab
            GROUP BY violation 
            ORDER BY Rate_of_arrest DESC 
            LIMIT 5;
        """
        result20 = pd.read_sql(query20, con = connection)
        result20
elif side == "PREDICT OUTCOMES":
    set_bg("D:/Project1/tp-3.jpg")
    st.markdown(
        """<h3 style="text-align: center;">PREDICT OUTCOMES - VIOLATIONS</h3>""",
        unsafe_allow_html=True
    )

    # --- Inputs ---
    country_query = "SELECT DISTINCT country_name FROM new_proj.newtab ORDER BY country_name;"
    countries_df = pd.read_sql(country_query, con=connection)
    countries = countries_df["country_name"].tolist()
    country = st.selectbox("Select Country", countries)

    vehiclenumber = st.text_input("Enter Vehicle Number")
    gender = st.radio("Select Gender", ["Male", "Female"])
    age = st.number_input("Enter Driver Age", min_value=18, max_value=90, value=27)

    if st.button("Predict Outcome"):
        # Normalize inputs
        vehiclenumber = vehiclenumber.strip().upper()
        country_norm = country.strip()
        
        # ✅ Map Male/Female → M/F
        gender_map = {"Male": "M", "Female": "F"}
        gender_norm = gender_map.get(gender, gender)

        query_exact = """
        SELECT violation, stop_date, stop_time, driver_gender, driver_age,
               search_conducted, stop_outcome, is_arrested, stop_duration, drugs_related_stop,
               vehicle_number, country_name
        FROM new_proj.newtab
        WHERE TRIM(LOWER(country_name)) = TRIM(LOWER(%s))
          AND driver_gender = %s
          AND REPLACE(UPPER(TRIM(vehicle_number)), '-', '') = REPLACE(%s, '-', '')
          AND driver_age = %s
        ORDER BY stop_date DESC
        LIMIT 1;
        """
        params_exact = (country_norm, gender_norm, vehiclenumber,age)
        violation_df = pd.read_sql(query_exact, con=connection, params=params_exact)

        if not violation_df.empty:
            row = violation_df.iloc[0]

            # Build narrative sentence
            gender_full = "male" if row["driver_gender"] == "M" else "female"
            search_status = "a search was conducted" if row["search_conducted"] else "no search was conducted"
            drug_status = "drug-related" if row["drugs_related_stop"] else "not drug-related"

            narrative = f"""
            🚔 A {row['driver_age']}-year-old {gender_full} driver was stopped  
            for **{row['violation']}** at {row['stop_time']}.  
            {search_status.capitalize()}, and he received **{row['stop_outcome'].lower()}**.  
            The stop lasted {row['stop_duration']} and was {drug_status}.
            """
            st.success(narrative)

        else:
            st.warning("No records available to predict an outcome.")