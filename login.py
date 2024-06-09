import streamlit as st

def main():
    st.set_page_config(page_title="Legal Document Analysis", layout="wide")
    # Other setup code here
    login()

def check_login(username, password):
    return username == "admin" and password == "pass"

def login():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        st.markdown(
            f"""
            <style>
            .main {{
                background-image: url('https://photo-store-ws1.cvs.com/resources/images/cvs/store/2015/global/980x640/print-services-980x640.jpg');
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
                }}
            .stTextInput {{
                background-color: rgba(255,255,0,0.4);
                color: white;
                border-radius: 5px;
                padding: 0.5rem;
                border: 1px solid rgba(255, 255, 255, 0.3);
                }}
            </style>
            <div class="main">
            """,
            unsafe_allow_html=True
        )
        st.title("Login :key:")
        col1, col2 = st.columns([1, 3])
        with col2:
            st.image("logo.png", width=100)
            username = st.text_input("Username", key="username_input")
            password = st.text_input("Password", type="password", key="password_input")
            if st.button("Login", key="login_btn"):
                if check_login(username, password):
                    st.success("Login successful! :tada:")
                    st.session_state['logged_in'] = True
                else:
                    st.error("Invalid username or password :x:")
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
