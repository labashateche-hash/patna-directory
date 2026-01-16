import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 1. PAGE CONFIG
st.set_page_config(page_title="Patna City Guide", page_icon="🏙️", layout="wide")

# 2. DATABASE CONNECTION (Secrets wala part)
def get_db():
    try:
        # Secrets se connect karna
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
        client = gspread.authorize(creds)
        sheet = client.open("PatnaDB").sheet1
        return sheet
    except Exception as e:
        st.error(f"Database Error: {e}")
        return None

def load_data():
    sheet = get_db()
    if sheet:
        return sheet.get_all_records()
    return []

def add_to_db(entry):
    sheet = get_db()
    if sheet:
        row = [entry['Name'], entry['Category'], entry['Offer'], entry['Phone'], entry['Address'], entry['Premium'], entry['Image']]
        sheet.append_row(row)

# 3. CUSTOM CSS (Design Fixes)
st.markdown("""
<style>
    /* Clean UI */
    .stApp {background-color: #f8f9fa;}
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Card Design */
    .business-card {
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        overflow: hidden;
        border: 1px solid #eee;
        transition: transform 0.2s;
    }
    .business-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    .card-img {
        width: 100%;
        height: 180px;
        object-fit: cover;
    }
    .card-content {
        padding: 15px;
    }
    .card-title {
        font-size: 18px;
        font-weight: bold;
        color: #333;
        margin-bottom: 5px;
    }
    .card-offer {
        background-color: #fff5f5;
        color: #e74c3c;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 13px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    .btn-row {
        display: flex;
        gap: 10px;
        margin-top: 10px;
    }
    /* Buttons */
    .btn {
        flex: 1;
        text-align: center;
        padding: 8px;
        border-radius: 6px;
        text-decoration: none;
        font-size: 14px;
        font-weight: bold;
        color: white !important;
    }
    .btn-call {background-color: #3498db;}
    .btn-wa {background-color: #27ae60;}
    .btn-lock {background-color: #bdc3c7; cursor: not-allowed;}
    
    /* Navbar Button */
    .nav-btn {
        background-color: #ff4b4b;
        color: white;
        padding: 8px 15px;
        border-radius: 5px;
        text-decoration: none;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 4. SESSION STATE
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# 5. NAVBAR
c1, c2, c3 = st.columns([1, 4, 1])
with c1:
    st.markdown("### 🏙️ PatnaGuide")
with c3:
    if st.session_state['page'] == 'home':
        if st.button("➕ List Business"):
            st.session_state['page'] = 'add'
            st.rerun()
    else:
        if st.button("🏠 Home"):
            st.session_state['page'] = 'home'
            st.rerun()
st.markdown("---")

# 6. PAGE LOGIC
if st.session_state['page'] == 'home':
    
    # --- HOME PAGE ---
    data = load_data()
    
    if not data:
        st.info("Loading Data... (Agar der lag rahi hai to refresh karein)")
    else:
        # Categories
        categories = list(set([d['Category'] for d in data]))
        
        for cat in categories:
            st.markdown(f"#### {cat}")
            cat_data = [d for d in data if d['Category'] == cat]
            
            # Grid of 3
            cols = st.columns(3)
            for i, item in enumerate(cat_data):
                with cols[i % 3]:
                    # Logic for Premium Buttons
                    is_prem = str(item['Premium']).lower() == 'true'
                    
                    if is_prem:
                        btns = f"""<a href="tel:{item['Phone']}" class="btn btn-call">📞 Call</a>
<a href="https://wa.me/{item['Phone']}" class="btn btn-wa">💬 Chat</a>"""
                    else:
                        btns = f"""<div class="btn btn-lock">🔒 Phone</div>
<div class="btn btn-lock">🔒 Chat</div>"""

                    # HTML Card (Indentation Removed to fix display bug)
                    card_html = f"""
<div class="business-card">
<img src="{item['Image']}" class="card-img">
<div class="card-content">
<div class="card-title">{item['Name']}</div>
<div style="font-size:12px; color:#666; margin-bottom:5px;">📍 {item['Address']}</div>
<div class="card-offer">🔥 {item['Offer']}</div>
<div class="btn-row">
{btns}
</div>
</div>
</div>
"""
                    st.markdown(card_html, unsafe_allow_html=True)

elif st.session_state['page'] == 'add':
    
    # --- ADD LISTING PAGE ---
    st.title("📝 List Your Business")
    st.info("Apni dukan ko online layein. Form bharein:")
    
    with st.form("add_form"):
        col1, col2 = st.columns(2)
        name = col1.text_input("Business Name *")
        cat = col2.selectbox("Category *", ["Food", "Fashion", "Services", "Education", "Real Estate"])
        
        offer = st.text_input("Aaj ka Offer / Tagline *")
        
        c3, c4 = st.columns(2)
        phone = c3.text_input("Mobile Number *")
        address = c4.text_input("Short Address (Area)")
        
        st.markdown("---")
        st.write("📸 **Business Image**")
        
        # Image Logic: Auto or Link
        img_option = st.radio("Image kaise lagani hai?", ["Auto-Generate (Best for Speed)", "Image Link (URL)"])
        
        final_img_url = ""
        if img_option == "Auto-Generate (Best for Speed)":
            st.caption(f"Hum '{cat}' category ke hisab se ek badhiya photo laga denge.")
            final_img_url = "https://source.unsplash.com/800x600/?" + cat
        else:
            final_img_url = st.text_input("Apni Photo ka Link yahan paste karein:")
            
        st.markdown("---")
        plan = st.radio("Visibility Plan", ["Free (Locked Contacts)", "Premium (Visible Contacts - ₹499)"])
        
        submit = st.form_submit_button("🚀 Submit Listing")
        
        if submit:
            if name and phone and offer:
                # Prepare Data
                new_entry = {
                    "Name": name,
                    "Category": cat,
                    "Offer": offer,
                    "Phone": phone,
                    "Address": address,
                    "Premium": "TRUE" if "Premium" in plan else "FALSE",
                    "Image": final_img_url if final_img_url else "https://source.unsplash.com/800x600/?shop"
                }
                
                with st.spinner("Saving..."):
                    add_to_db(new_entry)
                    st.success("Business List Ho Gaya! 🎉")
                    st.session_state['page'] = 'home'
                    st.rerun()
            else:
                st.error("Please * wale fields zaroor bharein.")
