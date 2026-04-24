import streamlit as st
def inject_global_css():
    st.markdown("""
        <style>
        .main {background: linear-gradient(135deg,#e0ffff 0%,#00bcd4 100%)}
        button, .stButton>button {
            background-color:#00bcd4;
            color:white; border:none;
            border-radius:6px; padding:0.5em 1.2em;
            font-weight:bold;
        }
        button:hover {background-color:#0097a7;}
        </style>
    """, unsafe_allow_html=True)