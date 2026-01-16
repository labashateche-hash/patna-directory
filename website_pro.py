import streamlit as st

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Patna City Guide", page_icon="🏙️", layout="wide")

# 2. SESSION STATE (Database)
if 'page' not in st.session_state:
    st.session_state['page'] = 'home' # Default page

if 'businesses' not in st.session_state:
    st.session_state['businesses'] = [
        {"name": "Royal Furniture", "cat": "Home Decor", "offer": "Sofa Set Flat 40% Off", "img": "https://source.unsplash.com/800x400/?furniture", "phone": "9199999999", "premium": True, "address": "Kankarbagh, Patna"},
        {"name": "Patna Rasoi", "cat": "Food & Dining", "offer": "Unlimited Thali @ ₹199", "img": "https://source.unsplash.com/800x400/?restaurant,food", "phone": "9188888888", "premium": True, "address": "Boring Road"},
        {"name": "Raju Tea Stall", "cat": "Food & Dining", "offer": "Special Kulhad Chai", "img": "https://source.unsplash.com/800x400/?tea", "phone": "9177777777", "premium": False, "address": "Gandhi Maidan"},
        {"name": "Style Men", "cat": "Fashion", "offer": "Jeans + Shirt @ ₹999", "img": "https://source.unsplash.com/800x400/?clothes,shop", "phone": "9166666666", "premium": False, "address": "P&M Mall"},
        {"name": "Tech Care", "cat": "Services", "offer": "Laptop Service @ ₹499", "img": "https://source.unsplash.com/800x400/?laptop,repair", "phone": "9155555555", "premium": False, "address": "Dak Bunglow"},
    ]

# 3. CUSTOM CSS (Design)
st.markdown("""
<style>
    /* Hide Streamlit Default Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Navbar Button Style */
    .nav-btn {
        display: inline-block;
        padding: 10px 20px;
        background-color: #ff4b4b;
        color: white !important;
        text-decoration: none;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
    }
    
    /* Section Headers */
    .category-header {
        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 20px;
        border-bottom: 2px solid #ff4b4b;
        padding-bottom: 5px;
        margin-bottom: 15px;
    }

    /* Card Design */
    .business-card {
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        overflow: hidden;
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .business-card:hover {transform: scale(1.02);}
    
    .card-img {width: 100%; height: 180px; object-fit: cover;}
    .card-content {padding: 15px;}
    .card-title {font-size: 18px; font-weight: bold; margin: 0;}
    .card-loc {font-size: 12px; color: gray; margin-bottom: 5px;}
    .card-offer {color: #e74c3c; font-weight: bold; font-size: 14px;}
    
    /* Button Styles */
    .btn-row {display: flex; justify-content: space-between; margin-top: 10px;}
    .btn-call {background: #3498db; color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none; font-size: 13px;}
    .btn-wa {background: #27ae60; color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none; font-size: 13px;}
    .btn-locked {background: #bdc3c7; color: white; padding: 5px 10px; border-radius: 5px; cursor: not-allowed; font-size: 13px;}
</style>
""", unsafe_allow_html=True)

# 4. HEADER / NAVBAR FUNCTION
def navbar():
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        st.markdown("## 🏙️ PatnaGuide")
    with col2:
        # Search Bar in Header
        st.text_input("🔍 Search...", placeholder="Pizza, Gym, Plumber...", label_visibility="collapsed")
    with col3:
        # Navigation Button Logic
        if st.session_state['page'] == 'home':
            if st.button("➕ List Business"):
                st.session_state['page'] = 'list_business'
                st.rerun()
        else:
            if st.button("🏠 Back to Home"):
                st.session_state['page'] = 'home'
                st.rerun()
    st.markdown("---")

# CALL NAVBAR
navbar()

# ==========================================
# PAGE VIEW LOGIC
# ==========================================

# --- VIEW 1: HOME PAGE ---
if st.session_state['page'] == 'home':
    
    # --- HERO SECTION (Featured/Premium) ---
    st.markdown("### 🔥 Featured Offers (Top Picks)")
    
    # Filter Premium Businesses
    premium_ads = [b for b in st.session_state['businesses'] if b['premium']]
    
    if premium_ads:
        # Featured ko bada dikhayenge (2 columns)
        p_col1, p_col2 = st.columns(2)
        for i, ad in enumerate(premium_ads[:2]): # Show max 2 top ads
            with (p_col1 if i == 0 else p_col2):
                st.image(ad['img'], use_column_width=True)
                st.markdown(f"### {ad['name']} ⭐")
                st.caption(f"📍 {ad['address']}")
                st.info(f"Offer: {ad['offer']}")
                
                # Action Buttons
                c1, c2 = st.columns(2)
                with c1: st.markdown(f"[📞 Call Now](tel:{ad['phone']})", unsafe_allow_html=True)
                with c2: st.markdown(f"[💬 WhatsApp](https://wa.me/{ad['phone']})", unsafe_allow_html=True)

    # --- CATEGORY WISE LISTING (Niche wale sections) ---
    
    # 1. Categories ki list nikalo
    all_cats = list(set([b['cat'] for b in st.session_state['businesses']]))
    
    for category in all_cats:
        st.markdown(f'<div class="category-header">{category}</div>', unsafe_allow_html=True)
        
        # Get businesses for this category
        cat_businesses = [b for b in st.session_state['businesses'] if b['cat'] == category]
        
        # Grid Layout (3 items per row)
        cols = st.columns(3)
        for idx, bus in enumerate(cat_businesses):
            with cols[idx % 3]:
                # Determine Buttons (Lock vs Unlock)
                if bus['premium']:
                    btns = f"""
                    <a href="tel:{bus['phone']}" class="btn-call">📞 Call</a>
                    <a href="https://wa.me/{bus['phone']}" class="btn-wa">💬 WhatsApp</a>
                    """
                else:
                    btns = f"""
                    <span class="btn-locked">🔒 Phone</span>
                    <span class="btn-locked">🔒 Chat</span>
                    """

                # HTML Card
                html_card = f"""
                <div class="business-card">
                    <img src="{bus['img']}" class="card-img">
                    <div class="card-content">
                        <div class="card-title">{bus['name']}</div>
                        <div class="card-loc">📍 {bus['address']}</div>
                        <div class="card-offer">🔥 {bus['offer']}</div>
                        <div class="btn-row">
                            {btns}
                        </div>
                    </div>
                </div>
                """
                st.markdown(html_card, unsafe_allow_html=True)

# --- VIEW 2: LIST YOUR BUSINESS PAGE ---
elif st.session_state['page'] == 'list_business':
    st.title("📝 List Your Business")
    st.write("Niche diye gaye form ko bharein. Aapka ad turant live ho jayega.")
    
    with st.container(border=True):
        st.subheader("1. Business Details")
        c1, c2 = st.columns(2)
        b_name = c1.text_input("Business Name *")
        b_owner = c2.text_input("Owner Name")
        
        b_cat = st.selectbox("Category *", ["Food & Dining", "Fashion", "Home Decor", "Services", "Education", "Real Estate"])
        
        st.subheader("2. Contact & Location")
        c3, c4 = st.columns(2)
        b_phone = c3.text_input("Mobile Number (10 Digit) *")
        b_addr = c4.text_input("Short Address (e.g. Boring Road)")
        b_map = st.text_input("Google Maps Link (Optional)")
        
        st.subheader("3. Offer & Visuals")
        b_offer = st.text_input("Aaj ka Offer / Tagline *")
        b_desc = st.text_area("Full Description")
        uploaded_img = st.file_uploader("Shop/Product Image Upload", type=['png', 'jpg'])
        
        st.markdown("---")
        st.subheader("4. Select Plan")
        plan = st.radio("Visibility Plan", ["FREE (Locked Contacts 🔒)", "PREMIUM (Visible Contacts ⭐) - ₹499/mo"])
        
        if st.button("🚀 Submit Listing", type="primary"):
            if b_name and b_phone and b_offer:
                # Add logic
                is_premium = True if "PREMIUM" in plan else False
                new_entry = {
                    "name": b_name,
                    "cat": b_cat,
                    "offer": b_offer,
                    "img": "https://source.unsplash.com/800x400/?shop", # Placeholder if no image
                    "phone": b_phone,
                    "premium": is_premium,
                    "address": b_addr
                }
                st.session_state['businesses'].append(new_entry)
                st.success("Listing Added Successfully! Home page par redirect ho rahe hain...")
                st.session_state['page'] = 'home'
                st.rerun()
            else:
                st.error("Please fill all required (*) fields.")
