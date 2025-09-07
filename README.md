PROJECT: Secure Check: A Python-SQL Digital Ledger for Police Post Logs
Description: This project focuses on maintaining comprehensive logs of individuals who have violated traffic rules. It records and organizes detailed information about each violation, including the type of offense, date and time of occurrence, location, associated penalties, halt time, vehicle information, gender and age of the offenders. The system helps authorities manage and review traffic violations efficiently.
Technologies Used: Python, SQL, Streamlit
Project Details:
•	Analyzed and preprocessed the dataset, removing redundant columns and finalizing the key attributes:
stop_date, stop_time, country_name, driver_gender, driver_age, driver_race, violation, search_conducted, stop_outcome, is_arrested, stop_duration, drugs_related_stop, vehicle_number.
•	Designed and implemented SQL queries to retrieve relevant records for reporting and predictions.
•	Built an interactive Streamlit application with the following modules:
	Home: Overview and introduction to the system.
	Summary: Displays the entire dataset for reference.
	Violation Details: Query-based exploration (Vehicle-based, Driver-based, Time-based, Violation-based, Location-based).
	Quick Lookups: Provides summarized insights across the dataset.
	Predict Outcomes: Allows officers to input driver/vehicle details and predicts likely outcomes using historical data.
