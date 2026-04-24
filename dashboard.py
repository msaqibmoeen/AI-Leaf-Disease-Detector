import streamlit as st, base64, requests, io
from utils import inject_global_css

def dashboard_page():
    inject_global_css()
    st.title("Leaf Disease Detection Dashboard 🌿")
    st.write("Upload a leaf image to analyze its health.")

    file = st.file_uploader("Upload Leaf Image",type=["jpg","jpeg","png"])
    if file:
        st.image(file,caption="Preview",use_column_width=True)
        if st.button("🔍Detect Disease"):
            with st.spinner("Analyzing…"):
                b64 = base64.b64encode(file.read()).decode()
                response = requests.post(
                    "http://localhost:8000/disease-detection-file",
                    files={"file": bytes(file.getvalue())})
                if response.ok:
                    res = response.json()
                    st.success(f"Disease: {res['disease_name']}")
                    st.write(f"Type: {res['disease_type']}")
                    st.progress(int(res['confidence']))
                    with st.expander("Symptoms"):
                        st.write("\n".join(res["symptoms"]))
                    with st.expander("Treatment"):
                        st.write("\n".join(res["treatment"]))
                else:
                    st.error("Error from backend.")