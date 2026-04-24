import streamlit as st

def onboarding_pages():
    slides = [
        ("Detect leaf diseases in seconds","Upload images & get instant AI analysis."),
        ("Understand symptoms & causes","Learn the signs before damage spreads."),
        ("Get expert treatment tips","Evidence-based suggestions for farmers."),
        ("Track results","Keep history of scans&improvements.")
    ]
    if "slide" not in st.session_state: st.session_state.slide = 0
    title,desc = slides[st.session_state.slide]
    st.markdown(f"### {title}")
    st.info(desc)
    col1,col2 = st.columns([1,6])
    with col1:
        if st.button("⬅ Prev",disabled=st.session_state.slide==0):
            st.session_state.slide -= 1
    with col2:
        next_label="Let's Start" if st.session_state.slide==len(slides)-1 else "Next ➜"
        if st.button(next_label):
            if st.session_state.slide==len(slides)-1:
                st.session_state.page="dashboard"
            else:
                st.session_state.slide+=1