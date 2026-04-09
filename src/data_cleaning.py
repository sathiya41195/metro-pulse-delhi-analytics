import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from urllib.parse import quote
import streamlit as st

host="localhost"
user="root"
password="S@th!ya41195"
database="metro"
port='3306'

st.header("Metro Pulse Delhi Analytics")
current_dir = Path(__file__).parent
json_path = (current_dir / '..' / 'source_data' / 'delhi_metro_trips.json').resolve()
st.write(f"Reading data from: {json_path}")
data = pd.read_json(json_path)
df = pd.DataFrame(data)
df = df.apply(lambda x: x.str.strip() if x.dtype == "str" else x)
st.write("DataFrame after stripping whitespace:")
st.dataframe(df.head(),width='stretch')
csv_path = (current_dir / '..' / 'cleaned_data' / 'delhi_metro_trips.csv').resolve()
s = df.to_csv(csv_path, index=False)
st.write(f"Cleaned data saved to: {csv_path}")
df.info()
cursor = create_engine(f"mysql+pymysql://{user}:{quote(password)}@{host}:{port}/{database}")
st.write(f"Database connection established: {cursor}")
df.to_sql(name='delhi_metro_trips', con=cursor, if_exists='replace', index=False)
st.success("Data successfully uploaded to the database.")
st.write("Data upload complete. You can now query the database to verify the entries.")
st.write("Example query: SELECT * FROM delhi_metro_trips LIMIT 5;")