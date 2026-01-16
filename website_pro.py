import streamlit as st
from PIL import Image

# 1. PAGE SETUP (Wide Layout)
st.set_page_config(page_title="Patna City Guide", page_icon="🏙️", layout="wide")

# 2. HIDING STREAMLIT STYLE (Magic CSS)
# Ye code Streamlit ke default menu aur footer ko chupa dega taaki ye 'Real Website' lage.
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .block-container {padding-top: 0rem;}
            
            /* Custom Navbar Design */
            .navbar {
                background-color: #0E1117;
                padding: 15px;
                text-align: center;
                font-size: 20px;
                color: white;
                font-family: sans-serif;
                margin-bottom: 20px;
                border-bottom: 2px solid #FF4B4B;
            }
            .navbar a {
                color: white;
                margin: 0 15px;
                text-decoration: none;
            }
            .navbar a:hover {
                color: #FF4B4B;
                font-weight: bold;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. CUSTOM NAVBAR (HTML Injection)
st.markdown("""
<div class="navbar">
    <b>🏙️ PATNA DIGITAL WALL</b> &nbsp;|&nbsp; 
    <a href="#">Home</a>
    <a href="#">Categories</a>
    <a href="#">List Business</a>
    <a href="#">Contact</a>
</div>
""", unsafe_allow_html=True)

# 4. HERO SECTION (Banner)
st.image("https://source.unsplash.com/1600x400/?city,night,lights", use_column_width=True)

# 5. DUMMY DATA (Business Database)
if 'businesses' not in st.session_state:
    st.session_state['businesses'] = [
        {"name": "Royal Furniture", "offer": "Sofa Set 40% Off", "cat": "Home", "img": "https://source.unsplash.com/400x300/?furniture"},
        {"name": "Patna Bakers", "offer": "Buy 1 Get 1 Pastry", "cat": "Food", "img": "https://source.unsplash.com/400x300/?cake"},
        {"name": "Tech World", "offer": "Laptop Repair @ 499", "cat": "Services", "img": "https://source.unsplash.com/400x300/?laptop"},
        {"name": "Style Men", "offer": "Shirt + Jeans Combo", "cat": "Fashion", "img": "https://source.unsplash.com/400x300/?fashion,men"},
    ]

# 6. MAIN CONTENT
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("### 🔥 Trending Offers in Patna")
    
    # Grid Layout (2 Cards per row)
    c1, c2 = st.columns(2)
    
    for i, bus in enumerate(st.session_state['businesses']):
        with (c1 if i % 2 == 0 else c2):
            st.image(bus['img'], use_column_width=True, output_format="JPEG")
            st.markdown(f"**{bus['name']}**")
            st.caption(bus['offer'])
            st.button(f"📞 Contact {bus['name']}", key=i)
            st.divider()

with col2:
    st.markdown("### 📢 Advertise Here")
    st.info("Apna business list karne ke liye form bharein.")
    with st.form("quick_add"):
        st.text_input("Business Name")
        st.text_input("Mobile No")
        st.form_submit_button("Request Call Back")
    
    st.markdown("---")
    st.markdown("### 📍 Categories")
    st.button("🍔 Food & Cafe")
    st.button("👗 Fashion & Wear")
    st.button("💻 Electronics")

# 7. PROFESSIONAL FOOTER
st.markdown("""
<div style="background-color:#f0f2f6; padding:20px; text-align:center; margin-top:50px;">
    <p>© 2026 Patna Digital Wall Pvt Ltd. | Made with ❤️ in Bihar</p>
    <small>Privacy Policy | Terms of Service</small>
</div>
""", unsafe_allow_html=True)