import streamlit as st
from PIL import Image
import io
import base64

# Page configuration
st.set_page_config(
    page_title="Golf Basics for Beginners",
    page_icon="⛳",
    layout="wide"
)

# Title and introduction
st.title("⛳ Golf Basics for New Golfers")
st.markdown("---")

# Create tabs for different aspects
tab1, tab2, tab3, tab4 = st.tabs(["Grip", "Stance", "Swing", "Tips"])

with tab1:
    st.header("🤝 Proper Grip Techniques")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Overlapping Grip (Vardon Grip)")
        st.write("""
        - Most common grip used by professionals
        - Pinky of trailing hand overlaps index finger of lead hand
        - Provides good control and feel
        """)
        st.info("💡 The 'V' formed by your thumb and index finger should point toward your trailing shoulder")
    
    with col2:
        st.subheader("Interlocking Grip")
        st.write("""
        - Pinky of trailing hand interlocks with index finger of lead hand
        - Good for players with smaller hands
        - Used by many tour professionals
        """)
        st.info("💡 Keep grip pressure light - like holding a bird")

with tab2:
    st.header("👣 Proper Stance & Posture")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Stance Basics")
        st.write("""
        - Feet shoulder-width apart
        - Weight balanced on balls of feet
        - Knees slightly flexed
        - Back straight with slight bend at hips
        """)
        
    with col2:
        st.subheader("Ball Position")
        st.write("""
        - Driver: Off inside of lead heel
        - Irons: Center of stance
        - Short irons: Slightly back of center
        """)

with tab3:
    st.header("🏌️ The Golf Swing")
    
    st.subheader("Swing Sequence")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 1️⃣ Backswing")
        st.write("""
        - Start with shoulders, not hands
        - Keep lead arm straight
        - Turn shoulders 90 degrees
        - Maintain spine angle
        """)
    
    with col2:
        st.markdown("### 2️⃣ Downswing")
        st.write("""
        - Start with lower body
        - Shift weight to lead foot
        - Keep head behind ball
        - Release through impact
        """)
    
    with col3:
        st.markdown("### 3️⃣ Follow Through")
        st.write("""
        - Full rotation to target
        - Belt buckle faces target
        - Balanced finish position
        - Hold finish for 2 seconds
        """)

with tab4:
    st.header("📚 Essential Tips for Beginners")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Practice Priorities")
        st.write("""
        1. **Start with short game** - Putting and chipping
        2. **Take lessons** - Get professional instruction early
        3. **Practice with purpose** - Focus on one thing at a time
        4. **Use proper equipment** - Get fitted for clubs
        5. **Play executive courses** - Build confidence on shorter courses
        """)
    
    with col2:
        st.subheader("Common Mistakes to Avoid")
        st.write("""
        - ❌ Gripping too tightly
        - ❌ Standing too far/close to ball
        - ❌ Swinging too hard
        - ❌ Lifting head during swing
        - ❌ Not following through
        """)

# Sidebar with additional resources
st.sidebar.header("Quick Reference")
st.sidebar.markdown("""
### Key Reminders
- 🎯 Aim is everything
- 💪 Tempo over power
- 🧘 Stay relaxed
- 📏 Consistent setup
- 🎓 Learn rules & etiquette

### Golf Etiquette
- Repair divots
- Fix ball marks
- Keep pace of play
- Be quiet during shots
- Safety first
""")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Remember: Golf is a game of patience and practice. Enjoy the journey! ⛳</p>
    <p><em>Tip: Consider taking lessons from a PGA professional to build proper fundamentals.</em></p>
</div>
""", unsafe_allow_html=True)