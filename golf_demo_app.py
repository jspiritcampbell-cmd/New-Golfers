import streamlit as st
import requests
from datetime import datetime, timedelta

st.set_page_config(page_title="Golf Weather Forecast", page_icon="⛳", layout="wide")

st.title("⛳ Golf Weather Forecast")
st.subheader("Find the Best Days to Hit the Range")

# Get user location
col1, col2 = st.columns([2, 1])
with col1:
    city = st.text_input("Enter your city:", value="Franklin, TN")
with col2:
    st.write("")
    st.write("")
    search_button = st.button("Get Forecast", type="primary")

def get_weather_score(temp, wind_speed, precipitation_prob, description):
    """Calculate weather score for golfing (0-100)"""
    score = 100
    
    # Temperature scoring (ideal: 65-80°F)
    if temp < 50:
        score -= (50 - temp) * 2
    elif temp > 85:
        score -= (temp - 85) * 1.5
    elif temp < 65:
        score -= (65 - temp) * 0.5
    elif temp > 80:
        score -= (temp - 80) * 0.5
    
    # Wind scoring (penalty for high winds)
    if wind_speed > 20:
        score -= 30
    elif wind_speed > 15:
        score -= 20
    elif wind_speed > 10:
        score -= 10
    
    # Precipitation scoring
    score -= precipitation_prob * 0.5
    
    # Weather condition penalties
    if any(word in description.lower() for word in ['rain', 'storm', 'thunder']):
        score -= 40
    elif 'snow' in description.lower():
        score -= 50
    
    return max(0, min(100, score))

def get_rating(score):
    """Convert score to rating"""
    if score >= 85:
        return "Excellent", "🟢"
    elif score >= 70:
        return "Good", "🟡"
    elif score >= 50:
        return "Fair", "🟠"
    else:
        return "Poor", "🔴"

def fetch_weather(city):
    """Fetch weather data from Open-Meteo API"""
    try:
        # Geocoding to get coordinates
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()
        
        if 'results' not in geo_data or len(geo_data['results']) == 0:
            return None, "City not found. Please try again."
        
        lat = geo_data['results'][0]['latitude']
        lon = geo_data['results'][0]['longitude']
        location_name = geo_data['results'][0]['name']
        
        # Weather forecast
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max,windspeed_10m_max,weathercode&temperature_unit=fahrenheit&windspeed_unit=mph&timezone=America/Chicago"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        
        return weather_data, location_name
    except Exception as e:
        return None, f"Error fetching weather: {str(e)}"

def get_weather_description(code):
    """Convert weather code to description"""
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Foggy",
        51: "Light drizzle",
        61: "Light rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Light snow",
        80: "Rain showers",
        95: "Thunderstorm"
    }
    return weather_codes.get(code, "Unknown")

if search_button or city:
    with st.spinner("Fetching weather data..."):
        weather_data, location = fetch_weather(city)
        
        if weather_data is None:
            st.error(location)
        else:
            st.success(f"📍 Showing forecast for: **{location}**")
            st.write("")
            
            # Display 5-day forecast
            daily = weather_data['daily']
            
            for i in range(5):
                date = datetime.fromisoformat(daily['time'][i])
                temp_max = daily['temperature_2m_max'][i]
                temp_min = daily['temperature_2m_min'][i]
                wind_speed = daily['windspeed_10m_max'][i]
                precip_prob = daily['precipitation_probability_max'][i]
                weather_code = daily['weathercode'][i]
                description = get_weather_description(weather_code)
                
                score = get_weather_score(temp_max, wind_speed, precip_prob, description)
                rating, emoji = get_rating(score)
                
                # Create card for each day
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
                    
                    with col1:
                        st.markdown(f"**{date.strftime('%A, %b %d')}**")
                    
                    with col2:
                        st.write(f"🌡️ {temp_min:.0f}°F - {temp_max:.0f}°F")
                    
                    with col3:
                        st.write(f"💨 {wind_speed:.0f} mph")
                    
                    with col4:
                        st.write(f"💧 {precip_prob:.0f}% rain")
                    
                    with col5:
                        st.markdown(f"### {emoji}")
                    
                    st.markdown(f"*{description}* • **{rating}** for golf (Score: {score:.0f}/100)")
                    st.divider()

st.markdown("---")
st.caption("Data provided by Open-Meteo API • Best conditions: 65-80°F, low wind, no precipitation")
