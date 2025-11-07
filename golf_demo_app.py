import streamlit as st
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import re

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
    if any(word in description.lower() for word in ['rain', 'storm', 'thunder', 'showers']):
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

def fetch_weather_from_weather_com(city):
    """Fetch weather data from Weather.com"""
    try:
        # Format city for URL
        city_slug = city.lower().replace(',', '').replace(' ', '-')
        
        # Try to search for the location first
        search_url = f"https://weather.com/weather/tenday/l/{city_slug}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return None, "Unable to fetch weather data. Please check the city name."
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract location name
        location_elem = soup.find('h1', {'class': re.compile('.*Location.*')})
        location_name = location_elem.text.strip() if location_elem else city
        
        # Find daily forecast cards
        forecast_days = []
        
        # Look for forecast data in the page
        details_section = soup.find_all('details', {'class': re.compile('.*DaypartDetails.*')})
        
        if not details_section:
            # Try alternative parsing
            summary_elements = soup.find_all('summary', {'class': re.compile('.*Disclosure.*')})
            
            for i, summary in enumerate(summary_elements[:5]):
                try:
                    # Extract day
                    day_elem = summary.find('h3')
                    day = day_elem.text.strip() if day_elem else f"Day {i+1}"
                    
                    # Extract temperature
                    temp_elems = summary.find_all('span', {'data-testid': 'TemperatureValue'})
                    temp_high = 75
                    temp_low = 55
                    if len(temp_elems) >= 2:
                        temp_high = int(temp_elems[0].text.replace('°', ''))
                        temp_low = int(temp_elems[1].text.replace('°', ''))
                    
                    # Extract precipitation
                    precip_elem = summary.find('span', {'data-testid': 'PercentageValue'})
                    precip_prob = int(precip_elem.text.replace('%', '')) if precip_elem else 0
                    
                    # Extract wind
                    wind_elem = summary.find('span', {'data-testid': 'Wind'})
                    wind_speed = 5
                    if wind_elem:
                        wind_text = wind_elem.text
                        wind_match = re.search(r'(\d+)', wind_text)
                        if wind_match:
                            wind_speed = int(wind_match.group(1))
                    
                    # Extract description
                    desc_elem = summary.find('span', {'data-testid': 'wxPhrase'})
                    description = desc_elem.text.strip() if desc_elem else "Partly Cloudy"
                    
                    forecast_days.append({
                        'day': day,
                        'temp_high': temp_high,
                        'temp_low': temp_low,
                        'precip_prob': precip_prob,
                        'wind_speed': wind_speed,
                        'description': description
                    })
                except Exception as e:
                    continue
        
        if len(forecast_days) == 0:
            return None, "Unable to parse weather data from Weather.com. Please try again."
        
        return forecast_days, location_name
        
    except Exception as e:
        return None, f"Error fetching weather: {str(e)}"

if search_button or city:
    with st.spinner("Fetching weather data from Weather.com..."):
        forecast_data, location = fetch_weather_from_weather_com(city)
        
        if forecast_data is None:
            st.error(location)
            st.info("💡 Tip: Try entering your city in this format: 'Nashville, TN' or 'Phoenix, AZ'")
        else:
            st.success(f"📍 Showing forecast for: **{location}**")
            st.caption("Data from Weather.com")
            st.write("")
            
            # Display forecast
            for day_data in forecast_data[:5]:
                temp_max = day_data['temp_high']
                temp_min = day_data['temp_low']
                wind_speed = day_data['wind_speed']
                precip_prob = day_data['precip_prob']
                description = day_data['description']
                
                score = get_weather_score(temp_max, wind_speed, precip_prob, description)
                rating, emoji = get_rating(score)
                
                # Create card for each day
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
                    
                    with col1:
                        st.markdown(f"**{day_data['day']}**")
                    
                    with col2:
                        st.write(f"🌡️ {temp_min}°F - {temp_max}°F")
                    
                    with col3:
                        st.write(f"💨 {wind_speed} mph")
                    
                    with col4:
                        st.write(f"💧 {precip_prob}% rain")
                    
                    with col5:
                        st.markdown(f"### {emoji}")
                    
                    st.markdown(f"*{description}* • **{rating}** for golf (Score: {score:.0f}/100)")
                    st.divider()

st.markdown("---")
st.caption("Data scraped from Weather.com • Best conditions: 65-80°F, low wind, no precipitation")
