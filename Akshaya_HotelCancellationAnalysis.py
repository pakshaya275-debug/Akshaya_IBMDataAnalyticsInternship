import pandas as pd
import numpy as np
import plotly.express as px

print("--- IBM SkillsBuild Internship: Hotel Booking Attrition Analysis ---")

# 1. Secured Data Ingestion Path
data_path = "c:/Users/AKSHAYA/Downloads/archive/hotel_bookings.csv"
try:
    df = pd.read_csv(data_path)
    print(f"Dataset Ingested Successfully! Row Count: {len(df):,}\n")
except FileNotFoundError:
    print(f"Critical Error: Could not locate dataset file at {data_path}")
    exit()

# 2. Advanced Data Preprocessing & Cleaning
df_clean = df.dropna(subset=['country']).copy()
df_clean['children'] = df_clean['children'].fillna(0)
df_clean['total_stay_nights'] = df_clean['stays_in_weekend_nights'] + df_clean['stays_in_week_nights']
df_clean['total_guests'] = df_clean['adults'] + df_clean['children'] + df_clean['babies']
df_clean = df_clean[df_clean['total_guests'] > 0]

# 3. Core Corporate KPI Computations
total_orders = len(df_clean)
cancellations = df_clean['is_canceled'].sum()
cancellation_rate = (cancellations / total_orders) * 100
avg_adr = df_clean['adr'].mean()

print(f"Executive Performance Indicators Summary:")
print(f"   - Total Evaluated Records: {total_orders:,}")
print(f"   - Total Canceled Iterations: {cancellations:,}")
print(f"   - Global Attrition Rate: {cancellation_rate:.2f}%")
print(f"   - Average Daily Room Revenue Rate (ADR): ${avg_adr:.2f}\n")

# 4. Property Domain Slicing Analysis
print("[Domain Evaluation: Property Type Attrition Focus]")
hotel_type = df_clean.groupby('hotel')['is_canceled'].mean() * 100
for hotel, rate in hotel_type.items():
    print(f"   - {hotel} Properties: {rate:.2f}% Cancellation Propensity")

# 5. Risk Window Exposure Mapping
print("\n[Risk Vector Mapping: Lead Time Window Correlation]")
bins = [-1, 7, 30, 90, 180, 800]
labels = ['0-7 Days (Last-Minute)', '8-30 Days (Short-Term)', '31-90 Days (Mid-Term)', '91-180 Days (Long-Term)', '181+ Days (Extreme Risk)']
df_clean['lead_time_bucket'] = pd.cut(df_clean['lead_time'], bins=bins, labels=labels)

lead_trend = df_clean.groupby('lead_time_bucket', observed=False)['is_canceled'].mean() * 100
for bracket, rate in lead_trend.items():
    print(f"   - Booking Range [{bracket}]: Attrition Rate {rate:.2f}%")

# 6. Presentation Visual Graphics Engine Initializer
print("\nInitializing Display Engine Context via Web Browser Host...")
lead_data = pd.DataFrame({
    'Booking Window': list(lead_trend.index),
    'Cancellation Rate (%)': list(lead_trend.values)
})

fig = px.bar(
    lead_data, 
    x='Booking Window', 
    y='Cancellation Rate (%)',
    text=lead_data['Cancellation Rate (%)'].apply(lambda x: f"{x:.1f}%"),
    title='<b>Risk Escalation Matrix: Booking Lead Time vs Attrition Propensity</b>',
    labels={'Booking Window': 'Time Booked in Advance', 'Cancellation Rate (%)': 'Cancellation Rate (%)'},
    color='Cancellation Rate (%)',
    color_continuous_scale='Reds'
)
fig.update_layout(template='plotly_dark', showlegend=False)
fig.update_traces(textposition='outside')
fig.show()

print("Data Pipeline Run Terminal Complete.")
