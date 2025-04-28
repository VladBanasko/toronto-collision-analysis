import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import os

# Create folders if they don't exist
os.makedirs('plots', exist_ok=True)

# Load data
file_path = 'data/traffic_collisions_data.csv'
df = pd.read_csv(file_path)
print(f"Initial shape: {df.shape}")

# Convert date column from milliseconds to datetime (UTC → Toronto local time)
df['OCC_DATE'] = pd.to_datetime(df['OCC_DATE'], unit='ms', errors='coerce', utc=True)
df['OCC_DATE'] = df['OCC_DATE'].dt.tz_convert('America/Toronto')
df.dropna(subset=['OCC_DATE'], inplace=True)

# Use OCC_HOUR instead of extracting from OCC_DATE
df['Hour'] = pd.to_numeric(df['OCC_HOUR'], errors='coerce')
df.dropna(subset=['Hour'], inplace=True)
df['Hour'] = df['Hour'].astype(int)

# Additional datetime features
df['Weekday'] = df['OCC_DATE'].dt.day_name()
df['Month'] = df['OCC_DATE'].dt.month_name()
df['Year'] = df['OCC_DATE'].dt.year
df['is_weekend'] = df['Weekday'].isin(['Saturday', 'Sunday'])

# --- Plot 1: Collisions by Hour ---
plt.figure(figsize=(10, 6))
sns.countplot(data=df, x='Hour', color='skyblue')
plt.title('Collisions by Hour of Day')
plt.xlabel('Hour')
plt.ylabel('Number of Collisions')
plt.xticks(range(0, 24))
plt.tight_layout()
plt.savefig('plots/collisions_by_hour.png')
plt.close()

# --- Plot 2: Collisions by Weekday ---
plt.figure(figsize=(10, 6))
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
sns.countplot(data=df, x='Weekday', order=weekday_order, color='salmon')
plt.title('Collisions by Day of the Week')
plt.xlabel('Day')
plt.ylabel('Number of Collisions')
plt.tight_layout()
plt.savefig('plots/collisions_by_weekday.png')
plt.close()

# --- Map: Basic Collision Heat Map ---
toronto_map = folium.Map(location=[43.7, -79.42], zoom_start=11)

# Try to extract coordinates
def extract_coords(geom):
    try:
        coords = eval(geom)['coordinates'][0]
        if isinstance(coords[0], list):  # if it's a polygon or nested
            coords = coords[0]
        return coords[1], coords[0]  # lat, lon
    except:
        return None

sample = df['geometry'].dropna().sample(n=500, random_state=42)
for geom in sample:
    coords = extract_coords(geom)
    if coords:
        folium.CircleMarker(location=coords, radius=1, color='red', fill=True).add_to(toronto_map)

toronto_map.save('plots/toronto_collision_map.html')

print("✔️ Analysis complete. Plots saved to 'plots/' folder.")