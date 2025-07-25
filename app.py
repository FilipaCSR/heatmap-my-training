import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
from io import BytesIO
import numpy as np
from heatmap_design import plot_training_heatmap
from analytics_injector import inject_ga

inject_ga("G-SL663FRXR7")

st.markdown("""
<iframe src="https://www.googletagmanager.com/ns.html?id=GTM-567CF8XR"
height="0" width="0" style="display:none;visibility:hidden"></iframe>
""", unsafe_allow_html=True)


# --- Data Cleaning Functions ---

@st.cache_data
def parse_xml(uploaded_file):
    tree = ET.parse(uploaded_file)
    root = tree.getroot()

    records = []
    for record in root.findall("Record"):
        rec = record.attrib
        records.append(rec)

    df_raw = pd.DataFrame(records)
    df_raw['startDate'] = pd.to_datetime(df_raw['startDate'])
    df_raw['endDate'] = pd.to_datetime(df_raw['endDate'])
    df_raw['creationDate'] = pd.to_datetime(df_raw['creationDate'])
    df_raw['value'] = pd.to_numeric(df_raw['value'], errors='coerce')

    return df_raw

@st.cache_data
def load_filtered_csv(uploaded_file):
    df_raw = pd.read_csv(uploaded_file, parse_dates=['startDate', 'endDate', 'creationDate'])
    df_raw['value'] = pd.to_numeric(df_raw['value'], errors='coerce')
    return df_raw

def extract_exercise(df_raw, selected_year):
    df_ex = df_raw[df_raw['type'] == 'HKQuantityTypeIdentifierAppleExerciseTime'].copy()
    df_ex['date'] = pd.to_datetime(df_ex['startDate'], utc=True).dt.tz_convert(None).dt.normalize()
    df_ex['value'] = pd.to_numeric(df_ex['value'], errors='coerce')
    df_ex = df_ex.groupby('date')['value'].sum().reset_index()
    df_ex.columns = ['date', 'n']

    all_dates = pd.date_range(start=df_ex['date'].min(), end=df_ex['date'].max())
    df_ex = pd.merge(pd.DataFrame({'date': all_dates}), df_ex, on='date', how='left')
    df_ex['n'] = df_ex['n'].fillna(0)

    df_ex['year'] = df_ex['date'].dt.year
    df_ex['month'] = df_ex['date'].dt.strftime('%b')
    df_ex['day'] = df_ex['date'].dt.day

    start_date = pd.to_datetime(f'{selected_year}-01-01')
    end_date = pd.to_datetime(f'{selected_year}-12-31')
    df_ex = df_ex[(df_ex['date'] >= start_date) & (df_ex['date'] <= end_date)]

    return df_ex

# --- STREAMLIT UI ---

st.set_page_config(page_title="Heatmap by Training", layout="wide")
st.title("📊 Heatmap my Training")
st.markdown("Upload your `export.xml` or a filtered `.csv` file to visualize your daily training data.")

st.markdown("Need help exporting your Apple Health data? [Read this guide](https://medium.com/@filipacsr/how-to-extract-and-analyze-apple-health-data-with-r-7d28029d22bd) ✨")

uploaded_file = st.file_uploader("📤 Upload your Apple Health file (`export.xml` or filtered `.csv`)", type=['xml', 'csv'])

if uploaded_file:
    if uploaded_file.name.endswith('.xml'):
        df_raw = parse_xml(uploaded_file)
    else:
        df_raw = load_filtered_csv(uploaded_file)

    years = df_raw['startDate'].dt.year.dropna().unique()
    years = np.sort(years)[::-1]

    st.sidebar.title("Settings")
    normalize = st.sidebar.checkbox("Normalize color scale across years", value=True)
    selected_years = st.sidebar.multiselect(
        "Select years to visualize:",
        years,
        default=years[:2] if len(years) >= 2 else years
    )

    max_val = None
    if normalize and selected_years:
        df_all = pd.concat([extract_exercise(df_raw, y) for y in selected_years])
        max_val = df_all['n'].max()

    for year in selected_years:
        df_exercise = extract_exercise(df_raw, year)

        if df_exercise.empty:
            st.warning(f"⚠️ No exercise data available for {year}.")
        else:
            st.subheader(f"🕛 Exercise Heatmap for {year}")
            fig = plot_training_heatmap(df_exercise, year = year, vmin = 0, vmax = max_val if normalize else None)
            st.pyplot(fig)

            # Download as PNG
            img_buffer = BytesIO()
            fig.savefig(img_buffer, format = 'png', dpi = 300, bbox_inches = 'tight')
            img_buffer.seek(0)

            st.download_button(
                label=f"📅  Download {year} Heatmap as PNG",
                data=img_buffer,
                file_name=f"training_heatmap_{year}.png",
                mime="image/png"
            )

    st.markdown("---")
    st.markdown("Made with ❤️ by Filipa — [Buy me a coffee](https://www.buymeacoffee.com/filipacsr)")
else:
    st.info("Please upload an Apple Health XML or CSV file to get started.")