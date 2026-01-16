import streamlit as st

# 1. Page Config (Sabse pehle ye line honi chahiye)
st.set_page_config(page_title="Patna City Guide", page_icon="🏙️", layout="wide")

# 2. Custom CSS (Makeover Kit)
st.markdown("""
<style>
    /* Background Color */
    .stApp {
        background-color: #f4f7f6;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Navbar Style */
    .navbar {
        background-color: #2c3e50;
        padding: 15px;
        color: white;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        border-bottom: 4px solid #e74c3c;
        margin-bottom: 20px;
        border-radius: 0 0 10px 10px;
    }
    
    /* Card Design (Pinterest Style) */
    .business-card {
        background-color: white;
        border-radius: 15px;
        padding: 0px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s;
        margin-bottom: 20px;
        overflow: hidden;
    }
    .business-card:hover {
        transform: translateY(-5px); /* Mouse aane par upar uthega */
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    /* Card Image */
    .card-img {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }
    
    /* Card Content */
    .card-body {
        padding: 15px;
    }
    .card-title {
        font-size: 18px;
        font-weight: bold;
        color: #2c3e50;
        margin: 0;
    }
    .card-offer {
        color: #e74c3c;
        font-weight: bold;
        font-size: 14px;
        margin-top: 5px;
    }
    .card-text {
        font-size: 13px;
        color: #7f8c8d;
        margin-top: 5px;
    }
    
    /* Action Buttons */
    .btn-container {
        display: flex;
        justify-content: space-between;
        padding: 15px;
        border-top: 1px solid #eee;
    }
    .btn-call {
        background-color: #3498db;
        color: white;
        text-decoration: none;
        padding: 8px 15px;
        border-radius: 5px;
        font-size: 14px;
        font-weight: bold;
    }
    .btn-wa {
        background-color: #27ae60;
        color: white;
        text-decoration: none;
        padding: 8px 15px;
        border-radius: 5px;
        font-size: 14px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 3. HTML Navbar
st.markdown('<div class="navbar">🏙️ PATNA PRIME DIRECTORY</div>', unsafe_allow_html=True)

# 4. Hero Section (Banner)
st.markdown("""
<div style="background-image: url('https://source.unsplash.com/1600x400/?market,shopping'); background-size: cover; padding: 60px; text-align: center; border-radius: 15px; color: white; margin-bottom: 30px; text-shadow: 2px 2px 4px #000;">
    <h1 style="margin:0; font-size: 50px;">Patna's Best Offers</h1>
    <p style="font-size: 20px;">Dukan wahi, offer naya!</p>
</div>
""", unsafe_allow_html=True)

# 5. Business Data (Database)
businesses = [
    {"name": "Royal Furniture House", "offer": "Dining Table par 40% Off", "cat": "Home", "img": "https://source.unsplash.com/600x400/?sofa", "phone": "9199999999"},
    {"name": "Patna Bakers Point", "offer": "Buy 1 Get 1 Free Pastry", "cat": "Food", "img": "https://source.unsplash.com/600x400/?cake", "phone": "9188888888"},
    {"name": "Tech Master Repair", "offer": "Mobile Screen @ ₹999", "cat": "Services", "img": "https://source.unsplash.com/600x400/?mobile,repair", "phone": "9177777777"},
    {"name": "Style Men's Wear", "offer": "Jeans + Shirt Combo ₹1200", "cat": "Fashion", "img": "https://source.unsplash.com/600x400/?jeans", "phone": "9166666666"},
    {"name": "Fit Gym & Spa", "offer": "Yearly Membership 50% Off", "cat": "Services", "img": "https://source.unsplash.com/600x400/?gym", "phone": "9155555555"},
    {"name": "Bihar Sweets", "offer": "Desi Ghee Ladoo Special", "cat": "Food", "img": "https://source.unsplash.com/600x400/?sweets", "phone": "9144444444"},
]

# 6. Filter Section
col_s1, col_s2 = st.columns([3, 1])
with col_s1:
    search = st.text_input("🔍 Search (e.g., Cake, Sofa)")
with col_s2:
    category = st.selectbox("Category", ["All", "Food", "Fashion", "Services", "Home"])

st.markdown("---")

# 7. MAIN GRID DISPLAY (HTML Injection for Style)
col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]

for i, bus in enumerate(businesses):
    if category == "All" or category == bus['cat']:
        if search.lower() in bus['name'].lower() or search.lower() in bus['offer'].lower():
            
            with cols[i % 3]:
                # HTML Card Creation
                html_card = f"""
                <div class="business-card">
                    <img src="{bus['img']}" class="card-img">
                    <div class="card-body">
                        <div class="card-title">{bus['name']}</div>
                        <div class="card-offer">🔥 {bus['offer']}</div>
                        <div class="card-text">📍 Patna • Verified Listing ✅</div>
                    </div>
                    <div class="btn-container">
                        <a href="tel:{bus['phone']}" class="btn-call">📞 Call Now</a>
                        <a href="https://wa.me/{bus['phone']}" class="btn-wa">💬 WhatsApp</a>
                    </div>
                </div>
                """
                st.markdown(html_card, unsafe_allow_html=True)
