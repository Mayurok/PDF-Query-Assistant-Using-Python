import pyrebase
import streamlit as st
# Firebase Configuration
firebaseConfig = {
 'apiKey': "",
 'authDomain': "",
 'projectId': "",
 'databaseURL': "",
 'storageBucket': "",
 'messagingSenderId': "",
 'appId': "",
 'measurementId': ""
}
# Firebase Initialization
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
# Login function
def login(email, password):
 try:
 user = auth.sign_in_with_email_and_password(email, password)
 handle = db.child(user['localId']).child("Handle").get().val()
 if handle is not None:
 st.subheader('Welcome ' + handle)
 st.info('Navigate using the menu on the left.')
 st.session_state.username = user['localId']
 st.session_state.usermail = user['email']
 st.session_state.signout = True
 st.session_state.selectbox = False

 except :
 st.error("Login Failed. Error: ")
def logout():
 st.session_state.signout = False
 st.session_state.username = False #''
 st.session_state.usermail = ''

def app():
 st.title("Welcome to PDF-Query-Assistant")
 if 'username' not in st.session_state:
 st.session_state.username = ""
 if 'usermail' not in st.session_state:
 st.session_state.usermail = "None"
 if 'signout' not in st.session_state:
 st.session_state.signout = False
 if not st.session_state.signout:
 choice = st.selectbox("Login/Signup", ['Login', 'Signup'])
 email = st.text_input("Please enter your email")
 password = st.text_input("Please enter your password", type='password')
 if choice == 'Signup':
 handle = st.text_input("Enter a unique username", value='Default')
 submit = st.button("Signup")
 if submit:
 try:
 user = auth.create_user_with_email_and_password(email, password)
 db.child(user['localId']).child("Handle").set(handle)
 st.success("Your account is created successfully")
 st.balloons()
 except :
 st.error("Signup Failed. Error: " )
 if choice == 'Login':
 if st.button("Login"):
 login(email, password)
 if st.session_state.signout:
 if st.button('Signout'):
 logout()
app()