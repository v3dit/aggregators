import streamlit as st


#Config
st.set_page_config(layout="wide", page_icon="💬", page_title="Ettarra Chatbot🤖")


#Contact
# with st.sidebar.expander("📬 Contact"):

#     st.write("DODS")


#Title
st.markdown(
    """
    <h2 style='text-align: center;'>EttaraAI, your data-aware assistant 🤖</h1>
    """,
    unsafe_allow_html=True,)

st.markdown("---")


#Description
st.markdown(
    """ 
    <h5 style='text-align:center;'>This dashboard will help you analyse your sales data by conversing with it. It will help you identify item sales forecast trends based on seasonality. This platform will also help you understand where you stand in this Coffee Multiverse!!</h5>
    """,
    unsafe_allow_html=True)
st.markdown("---")


#Robby's Pages
st.subheader("🚀 Explore the platform to deep dive into CoffeeVerse")

