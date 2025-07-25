import streamlit as st

def inject_ga(tracking_id):
    st.markdown(f"""
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={tracking_id}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{tracking_id}');
    </script>
    """, unsafe_allow_html=True)
