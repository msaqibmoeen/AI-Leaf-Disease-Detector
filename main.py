import streamlit as st
import time
import base64, requests
from auth import init_db, register_user, authenticate_user

init_db()

API_URL = "http://127.0.0.1:8000/disease-detection-file"

# CSS Theme - light green classic look
st.markdown("""
<style>
body, .main {
    background-color: #F3FFF3;
    color: #003300;
    font-family: 'Segoe UI', sans-serif;
}

/* Headings */
h1, h2, h3, h4 {
    color: #006400;
    font-weight: 700;
}

/* Buttons */
div.stButton > button {
    background-color: #008000;
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: bold;
    padding: 0.4em 2em;
    min-width: 140px;
}
div.stButton > button:hover {
    background-color: #006400;
}

/* Links */
a {
    color: #008000;
    font-weight: 600;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)


# Session State
if "page" not in st.session_state:
    st.session_state.page = "signup"
if "user" not in st.session_state:
    st.session_state.user = None

# Signup Page
def signup_page():
    st.title("Create Your Account 🌿")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    pw = st.text_input("Password", type="password")
    cpw = st.text_input("Confirm Password", type="password")
    
    colA, colB, colC = st.columns([1, 1, 0.7])
    with colA:
        signup_clicked = st.button("Sign Up")
    with colB:
        st.markdown(
            "<p style='text-align:center;margin-top:7px;'><b>Already have an account?</b></p>",
            unsafe_allow_html=True
        )
    with colC:
        go_login = st.button("Go to Login ➜")

    if signup_clicked:
        if not name or not email or not pw:
            st.warning("All fields required.")
        elif pw != cpw:
            st.error("Passwords do not match.")
        else:
            try:
                register_user(name, email, pw)
                st.success("Account created successfully! Redirecting to login...")
                time.sleep(1.5)
                st.session_state.page = "login"
                st.rerun()
            except Exception as e:
                if "UNIQUE constraint failed" in str(e):
                    st.error("Email already registered. Please log in instead.")
                else:
                    st.error(f"Error: {e}")

    if go_login:
        st.session_state.page = "login"
        st.rerun()

# Login Page
def login_page():
    st.title("Welcome Back 🔐")
    email = st.text_input("Email")
    pw = st.text_input("Password", type="password")
    
    colA, colB, colC = st.columns([1, 0.9, 0.7])
    with colA:
        login_clicked = st.button("Login")
    with colB:
        st.markdown(
            "<p style='text-align:center;margin-top:8px;'><b>Don't have an account?</b></p>",
            unsafe_allow_html=True
        )
    with colC:
        go_signup = st.button("Go to SignUp ➜")

    if login_clicked:
        ok, username = authenticate_user(email, pw)
        if ok:
            st.success(f"Welcome back, {username}!")
            st.session_state.user = username
            time.sleep(1)
            st.session_state.page = "welcome"
            st.rerun()
        else:
            st.error("Invalid credentials")

    if go_signup:
        st.session_state.page = "signup"
        st.rerun()

# Welcome Page
def welcome_page():
    st.title(f"Welcome, {st.session_state.user}! 🌱")
    st.write("Your AI-powered leaf-disease detector is ready to use.")
    if st.button("Continue ➜"):
        st.session_state.page = "main"
        st.rerun()

# Main Detection Page 
def main_page():
    st.title("Leaf Disease Detector 🍃")
    st.write("Upload a leaf image to detect its health status using AI.")

    file = st.file_uploader("Upload Leaf Image", type=["jpg", "jpeg", "png"])

    if file:
        st.image(file, caption="Preview", use_column_width=True)

        if st.button("🔍 Detect Disease"):
            with st.spinner("Analyzing leaf image with AI..."):
                try:
                    
                    res = requests.post(
                        API_URL,
                        files={"file": file.getvalue()},
                        timeout=120,
                    )

                    if res.status_code == 200:
                        result = res.json()
                        
                        col1, col2 = st.columns([2, 1])
                        with col1:
                            st.subheader("Diagnosis Summary")
                        with col2:
                            st.metric(
                                label="Model Confidence",
                                value=f"{result.get('confidence', 0)}%"
                            )

                        st.markdown("---")

                        plant_name_raw = (result.get("plant_name") or "").strip()
                        if not plant_name_raw:
                            plant_name_raw = "Unknown"

                        plant_name = plant_name_raw
                        if plant_name_raw.lower() == "unknown":
                            plant_name = "Not clearly identifiable (leaf-only image)"

                        disease_name = result.get("disease_name") or "Healthy Leaf"

                        st.markdown(f"**Plant:** {plant_name}")
                        st.markdown(f"**Disease:** {disease_name}")
                        st.markdown(f"**Type:** {result.get('disease_type', 'N/A')}")
                        st.markdown(f"**Severity:** {result.get('severity', 'N/A')}")
                    
                        tab1, tab2, tab3, tab4 = st.tabs(
                            ["🩺 Symptoms", "⚠ Possible Causes", "💊 Treatment", "🛡 Prevention"]
                        )

                        with tab1:
                            symptoms = result.get("symptoms", [])
                            if symptoms:
                                for s in symptoms:
                                    st.markdown(f"- {s}")
                            else:
                                st.write("No specific symptoms reported.")

                        with tab2:
                            causes = result.get("possible_causes", [])
                            if causes:
                                for c in causes:
                                    st.markdown(f"- {c}")
                            else:
                                st.write("No specific causes reported.")

                        with tab3:
                            treatment = result.get("treatment", [])
                            if treatment:
                                for t in treatment:
                                    st.markdown(f"- {t}")
                            else:
                                st.write("No treatment required (possibly healthy leaf).")

                        with tab4:
                            prevention = result.get("prevention", [])
                            if prevention:
                                for p in prevention:
                                    st.markdown(f"- {p}")
                            else:
                                st.write("General preventive care: maintain hygiene, proper spacing, and balanced nutrients.")

                    else:
                        st.error(f"Model API error (status {res.status_code}).")
                        try:
                            st.write(res.json())
                        except Exception:
                            st.write(res.text)

                except Exception as e:
                    st.error(f"Error while calling model API: {e}")
    
    st.write("")
    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()

page = st.session_state.page
if page == "signup":
    signup_page()
elif page == "login":
    login_page()
elif page == "welcome":
    welcome_page()
elif page == "main":
    main_page()