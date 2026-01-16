import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests # Image upload ke liye

# 1. PAGE CONFIG
st.set_page_config(page_title="Patna City Guide", page_icon="🏙️", layout="wide")

# --- CONFIGURATION (Yahan Apni Details Dalein) ---
IMGBB_API_KEY = "YAHAN_APNI_IMGBB_KEY_DALEIN"  # <-- Step 2 wali key yahan dalein

# 2. DATABASE CONNECTION
def get_db(sheet_name):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
        client = gspread.authorize(creds)
        # Sheet ka naam wahi hona chahiye
        return client.open("PatnaDB").worksheet(sheet_name)
    except Exception as e:
        return None

# --- HELPER FUNCTIONS ---

# Function: Image ko ImgBB par upload karke Link layega
def upload_image(image_file):
    if not image_file: return "https://source.unsplash.com/800x600/?shop"
    try:
        url = "https://api.imgbb.com/1/upload"
        payload = {"key": IMGBB_API_KEY}
        files = {"image": image_file.getvalue()}
        response = requests.post(url, data=payload, files=files)
        data = response.json()
        return data['data']['url'] # Return the web link of the image
    except:
        return "https://source.unsplash.com/800x600/?error"

# Function: Login Check
def check_login(username, password):
    sheet = get_db("Users")
    if not sheet: return False
    users = sheet.get_all_records()
    for user in users:
        if str(user['Username']) == str(username) and str(user['Password']) == str(password):
            return True
    return False

# Function: Sign Up
def sign_up(username, password, phone):
    sheet = get_db("Users")
    if not sheet: return False
    # Check duplicate
    users = sheet.col_values(1) # Column 1 is Username
    if username in users:
        return False # User already exists
    sheet.append_row([username, password, phone])
    return True

# 3. CSS DESIGN
st.markdown("""
<style>
    .stApp {background-color: #f8f9fa;}
    #MainMenu, footer, header {visibility: hidden;}
    .business-card {background: white; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px; overflow: hidden; border: 1px solid #eee;}
    .card-img {width: 100%; height: 180px; object-fit: cover;}
    .card-content {padding: 15px;}
    .card-title {font-size: 18px; font-weight: bold; color: #333;}
    .nav-btn {background-color: #ff4b4b; color: white; padding: 8px 15px; border-radius: 5px; text-decoration: none; font-weight: bold;}
    .auth-box {background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); max-width: 400px; margin: auto;}
</style>
""", unsafe_allow_html=True)

# 4. SESSION MANAGEMENT
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False
if 'user' not in st.session_state: st.session_state['user'] = None
if 'page' not in st.session_state: st.session_state['page'] = 'home'

# 5. NAVBAR
c1, c2, c3 = st.columns([1, 4, 1])
with c1: st.markdown("### 🏙️ PatnaGuide")
with c3:
    if st.session_state['logged_in']:
        st.write(f"👤 {st.session_state['user']}")
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['user'] = None
            st.rerun()
    else:
        if st.button("🔐 Login / Join"):
            st.session_state['page'] = 'login'
            st.rerun()
st.markdown("---")

# ==========================================
# PAGE LOGIC
# ==========================================

# --- PAGE: PUBLIC HOME ---
if st.session_state['page'] == 'home':
    if st.session_state['logged_in']:
        st.info("👋 Welcome to your Dashboard! Niche 'Manage Listings' par click karein.")
        if st.button("Go to My Dashboard 🚀", type="primary"):
            st.session_state['page'] = 'dashboard'
            st.rerun()

    # Public Listings Show karo
    sheet = get_db("sheet1")
    if sheet:
        data = sheet.get_all_records()
        if data:
            # Filter Logic (Optional)
            cat = st.selectbox("Browse Category", ["All", "Food", "Fashion", "Services", "Education"])
            
            cols = st.columns(3)
            for i, item in enumerate(data):
                if cat == "All" or item['Category'] == cat:
                    with cols[i % 3]:
                        is_prem = str(item['Premium']).lower() == 'true'
                        btns = f"""<a href="tel:{item['Phone']}" style="background:#3498db;color:white;padding:5px;border-radius:4px;text-decoration:none;">📞 Call</a>""" if is_prem else "🔒 Locked"
                        
                        st.markdown(f"""
                        <div class="business-card">
                        <img src="{item['Image']}" class="card-img">
                        <div class="card-content">
                        <div class="card-title">{item['Name']}</div>
                        <div style="font-size:12px; color:gray;">{item['Offer']}</div>
                        <div style="margin-top:10px;">{btns}</div>
                        </div></div>
                        """, unsafe_allow_html=True)

# --- PAGE: AUTHENTICATION (Login/Signup) ---
elif st.session_state['page'] == 'login':
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div class='auth-box'>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            l_user = st.text_input("Username", key="l_u")
            l_pass = st.text_input("Password", type="password", key="l_p")
            if st.button("Login"):
                if check_login(l_user, l_pass):
                    st.session_state['logged_in'] = True
                    st.session_state['user'] = l_user
                    st.success("Login Successful!")
                    st.session_state['page'] = 'dashboard'
                    st.rerun()
                else:
                    st.error("Wrong Username or Password")

        with tab2:
            s_user = st.text_input("New Username", key="s_u")
            s_pass = st.text_input("New Password", type="password", key="s_p")
            s_phone = st.text_input("Phone Number")
            if st.button("Create Account"):
                if sign_up(s_user, s_pass, s_phone):
                    st.success("Account Created! Please Login.")
                else:
                    st.error("Username already taken!")
        st.markdown("</div>", unsafe_allow_html=True)
        if st.button("Back to Home"):
            st.session_state['page'] = 'home'
            st.rerun()

# --- PAGE: USER DASHBOARD (Private) ---
elif st.session_state['page'] == 'dashboard':
    if not st.session_state['logged_in']:
        st.session_state['page'] = 'login'
        st.rerun()
        
    st.title(f"👋 {st.session_state['user']}'s Dashboard")
    st.write("Yahan aap apni listing add kar sakte hain.")
    
    with st.expander("➕ Add New Listing", expanded=True):
        with st.form("add_list_form"):
            c1, c2 = st.columns(2)
            name = c1.text_input("Business Name")
            cat = c2.selectbox("Category", ["Food", "Fashion", "Services", "Education"])
            offer = st.text_input("Offer Text")
            phone = st.text_input("Phone")
            address = st.text_input("Address")
            
            # REAL IMAGE UPLOAD
            uploaded_file = st.file_uploader("Upload Shop Image", type=['jpg', 'png', 'jpeg'])
            
            plan = st.radio("Select Plan", ["Free", "Premium"])
            
            if st.form_submit_button("Submit Listing"):
                if name and phone:
                    with st.spinner("Uploading Image & Saving..."):
                        # 1. Upload Image to ImgBB
                        img_url = upload_image(uploaded_file)
                        
                        # 2. Save to Google Sheet (Added Username column at end)
                        sheet = get_db("sheet1")
                        # Format: Name, Category, Offer, Phone, Address, Premium, Image, OWNER_USERNAME
                        row = [name, cat, offer, phone, address, "TRUE" if plan=="Premium" else "FALSE", img_url, st.session_state['user']]
                        sheet.append_row(row)
                        
                        st.success("Listing Added Successfully!")
                        st.balloons()
                else:
                    st.error("Details fill karein.")

    st.markdown("---")
    st.subheader("📋 Your Active Listings")
    # Logic to show only THIS user's listing
    sheet = get_db("sheet1")
    if sheet:
        all_data = sheet.get_all_records()
        # Filter: Jiska 'OWNER_USERNAME' match kare current user se
        # Note: Humein assume karna hoga ki last column Owner hai. 
        # Agar naya sheet banaya hai to Row 1 mein 'Owner' header zaroor dalein.
        
        my_listings = [d for d in all_data if str(d.get('Owner')) == str(st.session_state['user']) or str(d.get('Image')) == str(st.session_state['user'])] 
        # (Fix: Google Sheet headers mein 'Owner' column add karna zaroori hai)
        
        if not my_listings:
            st.info("Aapne abhi tak koi business add nahi kiya.")
        else:
            for item in my_listings:
                st.markdown(f"**{item['Name']}** - {item['Offer']} ({item.get('Premium')})")
