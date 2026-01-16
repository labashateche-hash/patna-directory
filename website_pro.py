import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. PAGE CONFIG
st.set_page_config(page_title="Patna City Guide", page_icon="🏙️", layout="wide")

# 2. CONNECT TO GOOGLE SHEET (Database Function)
def get_db():
    # Streamlit Secrets se Key nikalna (Cloud par ye secure hota hai)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    # Sheet ka naam 'PatnaDB' hona chahiye
    sheet = client.open("PatnaDB").sheet1 
    return sheet

# Data Load karna (Cache use karte hain taaki website slow na ho)
def load_data():
    try:
        sheet = get_db()
        data = sheet.get_all_records()
        return data
    except Exception as e:
        return []

# Data Save karna
def add_to_db(entry):
    sheet = get_db()
    # List format mein data append karna
    row = [entry['Name'], entry['Category'], entry['Offer'], entry['Phone'], entry['Address'], entry['Premium'], entry['Image']]
    sheet.append_row(row)

# 3. CSS & SESSION SETUP
if 'page' not in st.session_state: st.session_state['page'] = 'home'

st.markdown("""
<style>
    /* Same Professional CSS */
    .stApp {background-color: #f8f9fa;}
    #MainMenu, footer, header {visibility: hidden;}
    .business-card {background: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); overflow: hidden; margin-bottom: 20px; border: 1px solid #eee;}
    .card-img {width: 100%; height: 180px; object-fit: cover;}
    .card-content {padding: 15px;}
    .card-title {font-size: 18px; font-weight: 700; color: #333; margin-bottom: 5px;}
    .card-offer {color: #e74c3c; font-weight: 600; font-size: 14px; background: #fff5f5; padding: 4px 8px; border-radius: 4px; display: inline-block;}
    .btn-row {display: flex; gap: 10px; margin-top: 15px;}
    .btn {flex: 1; text-align: center; padding: 8px; border-radius: 6px; font-size: 14px; font-weight: 600; text-decoration: none;}
    .btn-call {background: #3498db; color: white !important;}
    .btn-wa {background: #27ae60; color: white !important;}
    .btn-lock {background: #e0e0e0; color: #999 !important; cursor: not-allowed;}
    .premium-badge {float: right; font-size: 12px; background: #ffd700; padding: 2px 6px; border-radius: 4px; color: #333;}
</style>
""", unsafe_allow_html=True)

# 4. NAVBAR
col1, col2, col3 = st.columns([1, 4, 1])
with col1: st.markdown("### 🏙️ PatnaGuide")
with col3:
    if st.session_state['page'] == 'home':
        if st.button("➕ List Business"): st.session_state['page'] = 'add'
    else:
        if st.button("🏠 Home"): st.session_state['page'] = 'home'
st.markdown("---")

# 5. PAGE LOGIC
if st.session_state['page'] == 'home':
    # Data load karein
    data = load_data()
    
    if not data:
        st.info("Abhi koi listing nahi hai. 'List Business' par click karke pehli listing dalein!")
    
    else:
        # Hero Section (Sirf TRUE Premium wale)
        st.markdown("### 🔥 Featured Spots")
        premium_ads = [d for d in data if str(d.get('Premium')).lower() == 'true']
        
        if premium_ads:
            cols = st.columns(len(premium_ads) if len(premium_ads) < 3 else 3)
            for i, ad in enumerate(premium_ads[:3]):
                with cols[i]:
                    st.image(ad['Image'], use_column_width=True)
                    st.markdown(f"**{ad['Name']}**")
                    st.caption(ad['Offer'])
        
        # Category Listing
        categories = list(set([d['Category'] for d in data]))
        for cat in categories:
            st.markdown(f"#### {cat}")
            cat_data = [d for d in data if d['Category'] == cat]
            
            c1, c2, c3 = st.columns(3)
            rows = [c1, c2, c3]
            
            for idx, item in enumerate(cat_data):
                with rows[idx % 3]:
                    # Check Premium Status
                    is_prem = str(item.get('Premium')).lower() == 'true'
                    
                    if is_prem:
                        btns = f"""
                        <a href="tel:{item['Phone']}" class="btn btn-call">📞 Call</a>
                        <a href="https://wa.me/{item['Phone']}" class="btn btn-wa">💬 Chat</a>
                        """
                    else:
                        btns = f"""
                        <div class="btn btn-lock">🔒 Phone</div>
                        <div class="btn btn-lock">🔒 Chat</div>
                        """
                    
                    html = f"""
                    <div class="business-card">
                        <img src="{item['Image']}" class="card-img">
                        <div class="card-content">
                            {'<span class="premium-badge">⭐ PRO</span>' if is_prem else ''}
                            <div class="card-title">{item['Name']}</div>
                            <div style="font-size:12px; color:#666; margin-bottom:8px;">📍 {item['Address']}</div>
                            <div class="card-offer">{item['Offer']}</div>
                            <div class="btn-row">{btns}</div>
                        </div>
                    </div>
                    """
                    st.markdown(html, unsafe_allow_html=True)

elif st.session_state['page'] == 'add':
    st.title("📝 Business List Karein")
    with st.form("biz_form"):
        name = st.text_input("Business Name")
        cat = st.selectbox("Category", ["Food", "Fashion", "Services", "Education", "Real Estate"])
        offer = st.text_input("Offer / Tagline")
        phone = st.text_input("Mobile Number")
        address = st.text_input("Area/Location")
        img = "https://source.unsplash.com/800x600/?" + cat # Auto image
        
        plan = st.radio("Plan", ["Free (Locked)", "Premium (Unlocked - Paid)"])
        
        if st.form_submit_button("🚀 Submit"):
            if name and phone:
                # Prepare Data for Google Sheet
                new_data = {
                    "Name": name, "Category": cat, "Offer": offer,
                    "Phone": phone, "Address": address,
                    "Premium": "TRUE" if "Premium" in plan else "FALSE",
                    "Image": img
                }
                
                with st.spinner("Saving to Database..."):
                    try:
                        add_to_db(new_data)
                        st.success("Listing Save Ho Gayi! Home page par jaa rahe hain...")
                        st.session_state['page'] = 'home'
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}. (Shayad Secrets set nahi hain)")
