import streamlit as st

# 1. PAGE CONFIG
st.set_page_config(page_title="Patna City Guide", page_icon="🏙️", layout="wide")

# 2. CUSTOM CSS (Design + Locked Effect)
st.markdown("""
<style>
    /* Background */
    .stApp {background-color: #f4f7f6;}
    
    /* Navbar */
    .navbar {
        background-color: #2c3e50; padding: 15px; color: white;
        text-align: center; font-size: 24px; font-weight: bold;
        border-bottom: 4px solid #e74c3c; margin-bottom: 20px; border-radius: 0 0 10px 10px;
    }
    
    /* Card Styles */
    .business-card {
        background-color: white; border-radius: 15px; padding: 0px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom: 20px; overflow: hidden;
    }
    .card-img {width: 100%; height: 200px; object-fit: cover;}
    .card-body {padding: 15px;}
    .card-title {font-size: 18px; font-weight: bold; color: #2c3e50; margin: 0;}
    .card-offer {color: #e74c3c; font-weight: bold; font-size: 14px;}
    
    /* BUTTON STYLES */
    .btn-container {display: flex; justify-content: space-between; padding: 15px; border-top: 1px solid #eee;}
    
    /* Premium Buttons (Working) */
    .btn-call {background-color: #3498db; color: white; padding: 8px 15px; border-radius: 5px; text-decoration: none; font-weight: bold;}
    .btn-wa {background-color: #27ae60; color: white; padding: 8px 15px; border-radius: 5px; text-decoration: none; font-weight: bold;}
    
    /* Locked Buttons (Not Working) */
    .btn-locked {
        background-color: #95a5a6; color: white; padding: 8px 15px; 
        border-radius: 5px; text-decoration: none; font-weight: bold; cursor: not-allowed;
    }
</style>
""", unsafe_allow_html=True)

# 3. DATABASE (Session State)
if 'businesses' not in st.session_state:
    st.session_state['businesses'] = [
        # Premium User (Buttons Khule hain)
        {"name": "Royal Furniture", "offer": "Sofa 40% Off", "cat": "Home", "img": "https://source.unsplash.com/600x400/?sofa", "phone": "9199999999", "premium": True},
        # Free User (Buttons Locked hain)
        {"name": "Raju Tea Stall", "offer": "Special Masala Chai", "cat": "Food", "img": "https://source.unsplash.com/600x400/?tea", "phone": "9188888888", "premium": False},
        # Premium User
        {"name": "Tech Master", "offer": "Mobile Repair @ 999", "cat": "Services", "img": "https://source.unsplash.com/600x400/?repair", "phone": "9177777777", "premium": True},
    ]

# 4. SIDEBAR MENU (Yahan se navigation hoga)
st.sidebar.title("Menu ☰")
menu = st.sidebar.radio("Go to:", ["🏠 Home (Customers)", "📝 List Your Business (Dukandaar)"])

# ==========================================
# PAGE 1: HOME (Customer View)
# ==========================================
if menu == "🏠 Home (Customers)":
    # Header
    st.markdown('<div class="navbar">🏙️ PATNA PRIME DIRECTORY</div>', unsafe_allow_html=True)
    
    # Filters
    col_s1, col_s2 = st.columns([3, 1])
    with col_s1:
        search = st.text_input("🔍 Search Offers...")
    with col_s2:
        cat_filter = st.selectbox("Category", ["All", "Food", "Services", "Home", "Fashion"])

    # Display Logic
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]
    
    for i, bus in enumerate(st.session_state['businesses']):
        if cat_filter == "All" or cat_filter == bus['cat']:
             if search.lower() in bus['name'].lower() or search.lower() in bus['offer'].lower():
                with cols[i % 3]:
                    
                    # Logic: Agar Premium hai to Link banega, nahi to '#' (kahin nahi jayega)
                    if bus['premium']:
                        call_btn = f'<a href="tel:{bus["phone"]}" class="btn-call">📞 Call Now</a>'
                        wa_btn = f'<a href="https://wa.me/{bus["phone"]}" class="btn-wa">💬 WhatsApp</a>'
                        badge = "⭐ Premium Verified"
                    else:
                        call_btn = f'<span class="btn-locked">🔒 Locked</span>'
                        wa_btn = f'<span class="btn-locked">🔒 Premium Only</span>'
                        badge = "Basic Listing"

                    # HTML Card
                    html = f"""
                    <div class="business-card">
                        <img src="{bus['img']}" class="card-img">
                        <div class="card-body">
                            <div class="card-title">{bus['name']}</div>
                            <div style="font-size:12px; color:gray;">{badge}</div>
                            <div class="card-offer">🔥 {bus['offer']}</div>
                        </div>
                        <div class="btn-container">
                            {call_btn}
                            {wa_btn}
                        </div>
                    </div>
                    """
                    st.markdown(html, unsafe_allow_html=True)

# ==========================================
# PAGE 2: LIST BUSINESS (Dukandaar Form)
# ==========================================
elif menu == "📝 List Your Business (Dukandaar)":
    st.title("🚀 Apna Business Online Karein")
    st.write("Apne dukan ki details niche bharein aur customers payein.")
    
    with st.form("add_biz_form"):
        name = st.text_input("Business Name")
        cat = st.selectbox("Category", ["Food", "Fashion", "Services", "Home"])
        offer = st.text_input("Aaj ka Offer (e.g., 50% Off)")
        phone = st.text_input("WhatsApp Number")
        img_url = "https://source.unsplash.com/600x400/?shop" # Auto image for demo
        
        st.markdown("---")
        st.subheader("Plan Chuniye 👇")
        plan = st.radio("Visibility Plan:", ["FREE (Contact Locked 🔒)", "PREMIUM (Contact Visible ⭐) - ₹99/month"])
        
        submitted = st.form_submit_button("Submit Listing")
        
        if submitted:
            is_premium = True if "PREMIUM" in plan else False
            
            new_biz = {
                "name": name,
                "offer": offer,
                "cat": cat,
                "img": img_url,
                "phone": phone,
                "premium": is_premium
            }
            st.session_state['businesses'].append(new_biz)
            
            if is_premium:
                st.balloons()
                st.success("✅ Payment Successful! Aapka Premium Ad Live ho gaya hai.")
            else:
                st.info("⚠️ Aapka Free Ad Live ho gaya. (Note: Customers apko call nahi kar payenge).")
