import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from urllib.parse import quote
import streamlit as st

# --- 1. DATABASE LAYER (Configuration & Connection) ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "S@th!ya41195",
    "database": "metro",
    "port": "3306"
}

def get_engine():
    """Creates a reusable SQLAlchemy engine."""
    conn_str = f"mysql+pymysql://{DB_CONFIG['user']}:{quote(DB_CONFIG['password'])}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    return create_engine(conn_str)

# --- 2. SERVICE LAYER (Logic & Data Processing) ---

@st.cache_data
def load_and_clean_data(json_path):
    """Reads JSON and performs basic string cleaning."""
    data = pd.read_json(json_path)
    df = pd.DataFrame(data)
    # Fixed: 'str' to 'object' check for pandas dtype
    df = df.apply(lambda x: x.str.strip() if x.dtype == "str" else x)
    return df
def save_to_csv(df, csv_path):
    """Saves the cleaned dataframe to a CSV file."""
    df.to_csv(csv_path, index=False)

def upload_to_mysql(df, table_name, config):
    """Handles the database connection and data upload."""
    engine = get_engine()
    df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    return engine

def execute_query(query):
    """Executes a SQL query and returns a DataFrame."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(query, conn)

def get_queries():
    """Returns a dictionary of all predefined SQL queries for easy maintenance."""
    return {
        "highest_passenger_traffic": "SELECT `From_Station`, `To_Station`, SUM(passengers) AS traffic_count FROM delhi_metro_trips GROUP BY `From_Station`, `To_Station` order by 3 desc;",
        "highest_revenue_route": "SELECT `From_Station`, `To_Station`, SUM(Fare) AS Total_Revenue FROM delhi_metro_trips GROUP BY `From_Station`, `To_Station` order by 3 desc;",
        "average_fare_route": "SELECT `From_Station`, `To_Station`, AVG(Fare) AS Avg_Revenue FROM delhi_metro_trips GROUP BY `From_Station`, `To_Station` order by 3 desc;",
        "longest_travel_distance": "SELECT `From_Station`, `To_Station`, Max(`Distance_km`) AS Longest_distance FROM delhi_metro_trips GROUP BY `From_Station`, `To_Station` order by 3 desc;",
        "highest_departure": "SELECT `From_Station`,  SUM(passengers) AS High_departure FROM delhi_metro_trips GROUP BY `From_Station` order by 2 desc;",
        "highest_receiver": "SELECT To_Station,  SUM(Passengers) AS High_Receiver FROM delhi_metro_trips GROUP BY To_Station order by 2 desc;",
        "frequent_metro_station": "SELECT Station, SUM(Trip_count) AS Frequently_used_trips FROM (SELECT `From_Station` AS Station,  count(`TripID`) AS trip_count FROM delhi_metro_trips GROUP BY `From_Station` UNION SELECT To_Station,  count(`TripID`) AS trip_count FROM delhi_metro_trips GROUP BY To_Station ) AS trip_data GROUP BY Station order by 2 desc lIMIT 10;",
        "most_frequent_station_pairs": "SELECT `From_Station`,To_Station,  count(`TripID`) AS Frequently_used_count FROM delhi_metro_trips GROUP BY `From_Station`,To_Station order by 3 desc lIMIT 10;",
        "total_trip_revenue": "SELECT SUM(`Fare`) AS total_revenue FROM delhi_metro_trips;",
        "average_trip_fare": "SELECT AVG(`Fare`) AS average_revenue FROM delhi_metro_trips;",
        "highest_revenue_per_km": "SELECT `From_Station`, `To_Station`, SUM(`Fare`)/Sum(`Distance_km`) AS revenue_per_km FROM delhi_metro_trips GROUP BY `From_Station`, `To_Station` order by 3 desc;",
        "highest_revenue_tkt_type": "select Ticket_Type, SUM(Fare) AS Total_Revenue from delhi_metro_trips GROUP BY Ticket_Type order by 2 desc;",
        "avg_passenger_per_trip": "SELECT AVG(`Passengers`) AS average_passengers FROM delhi_metro_trips;",
        "highest_passenger_count": "SELECT `From_Station`,`To_Station`,Max(`passengers`) AS highest_passengers FROM delhi_metro_trips GROUP BY `From_Station`, `To_Station` order by 3 desc;",
        "tkt_type_distribution": "SELECT `Ticket_type`, SUM(`Passengers`) AS total_passengers FROM delhi_metro_trips GROUP BY `Ticket_type` order by 2 desc;",
        "passenger_count_by_station": "SELECT station, sum(Total_passenger) AS total_passengers FROM (SELECT `From_Station` AS station,  SUM(Passengers) AS Total_passenger FROM delhi_metro_trips GROUP BY `From_Station` UNION SELECT To_Station AS station,  SUM(Passengers) AS Total_passenger FROM delhi_metro_trips GROUP BY To_Station) AS passenger_data GROUP BY station order by 2 desc;",
        "condition_count": "SELECT `Remarks`, COUNT(`TripID`) AS trip_count FROM delhi_metro_trips WHERE `Remarks` in('festival', 'peak', 'off-peak', 'weekend') GROUP BY `Remarks` order by 2 desc;",
        "highest_revenue_by_condition": "SELECT `Remarks`, SUM(`Fare`) AS total_revenue FROM delhi_metro_trips GROUP BY `Remarks` order by 2 desc;",
        "monthly_passenger_trend": "SELECT DATE_FORMAT(`Date`, '%Y-%m') AS month, SUM(`passengers`) AS monthly_trend FROM delhi_metro_trips GROUP BY month order by 1 asc;",
        "avg_passenger_condition":"SELECT `Remarks`, AVG(`passengers`) AS Avg_revenue FROM delhi_metro_trips GROUP BY `Remarks` order by 2 desc;"     
  
    }

# --- 3. UI LAYER (Reusable Components) ---

def display_query_result(query_key, label):
    """Reusable UI component for a query button and its result table."""
    if st.button(label):
        try:
            queries = get_queries()
            with st.spinner(f"Analyzing {label}..."):
                df = execute_query(queries[query_key])
                st.subheader("Query Results")
                st.write(f"Returned {len(df)} rows:")
                st.dataframe(df, width='content', hide_index=True)
        except Exception as e:
            st.error(f"⚠️ SQL Error: {e}")

# --- MAIN APPLICATION ---

def main():
    st.set_page_config(page_title="Metro Pulse Delhi", layout="wide")
    st.header("🚇 Metro Pulse Delhi Analytics")

    # Path Setup
    current_dir = Path(__file__).parent
    json_path = (current_dir / '..' / 'source_data' / 'delhi_metro_trips.json').resolve()
    csv_path = (current_dir / '..' / 'cleaned_data' / 'delhi_metro_trips.csv').resolve()
    
    # Check for data  
    if json_path.exists():
        df = load_and_clean_data(json_path)
        st.success(f"Loaded data from: `{json_path.name}`")
        st.dataframe(df.head(), use_container_width=True, hide_index=True)    
    #save cleaned data to csv
    if st.button("Export Cleaned Data to CSV"):
        save_to_csv(df, csv_path)
        st.info(f"File saved to: `{csv_path}`")
        load_Tab = True;
    if st.button("Push to MySQL Database"):
        try:
            engine = upload_to_mysql(df, 'delhi_metro_trips', DB_CONFIG)
            st.success("Data successfully uploaded to the database.")            
        except Exception as e:
            st.error(f"Database Error: {e}")    
    # Sidebar Navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Route Analysis", "Station Analysis", "Revenue Analysis", "Passenger Analysis","Travel Pattern Analysis"])    
    with tab1:
        #st.header("Route Analysis")
        st.subheader("📍 Route & Traffic Analysis")
        display_query_result("highest_passenger_traffic", "1.Which metro routes have the highest passenger traffic?")
        display_query_result("highest_revenue_route", "2.Which routes generate the highest total revenue?")
        display_query_result("average_fare_route", "3.What is the average fare for each route?")
        display_query_result("longest_travel_distance", "4.Which routes have the longest travel distances?")
    with tab2:
        #st.header("Station Analysis")
        st.subheader("🚉 Station & Passenger Analysis")
        display_query_result("highest_departure", "5.Which stations have the highest number of trip departures?")
        display_query_result("highest_receiver", "6.Which stations receive the highest number of passengers?")
        display_query_result("frequent_metro_station", "7.What are the top 10 most frequently used metro stations?")
        display_query_result("most_frequent_station_pairs", "8.Which station pairs are most frequently used for travel?")
    with tab3:
        #st.header("Revenue Analysis")
        st.subheader("💰 Financial Insights")
        display_query_result("total_trip_revenue", "9.What is the total revenue generated from all trips?")
        display_query_result("average_trip_fare", "10.What is the average fare per trip?")
        display_query_result("highest_revenue_per_km","11.Which routes generate the highest revenue per kilometer?")
        display_query_result("highest_revenue_tkt_type", "12.Which ticket type generates the highest revenue?")
    with tab4:
        #st.header("Passenger Analysis")
        st.subheader("👥 Passenger Insights")
        display_query_result("avg_passenger_per_trip" ,"13.What is the average number of passengers per trip?")
        display_query_result("highest_passenger_count", "14.Which trips recorded the highest passenger counts?")
        display_query_result("tkt_type_distribution", "15.What is the passenger distribution by ticket type?")
        display_query_result("passenger_count_by_station" ,"16.What is the total passenger count for each station?")
    with tab5:
        #st.header("Travel Pattern Analysis")
        st.subheader("📊 Travel Patterns & Trends")
        display_query_result("condition_count", "17.How many trips occur during peak, off-peak, festival, and weekend conditions?")
        display_query_result("highest_revenue_by_condition", "18.Which travel condition generates the highest revenue?")
        display_query_result("monthly_passenger_trend", "19.What is the monthly passenger trend across the dataset?")
        display_query_result("avg_passenger_condition", "20.Which travel condition has the highest average passenger count per trip?")

if __name__ == "__main__":
    main()