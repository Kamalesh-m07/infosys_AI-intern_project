import os
import django
import streamlit as st
from detection.models import YourModel  # Replace with an actual model from your app

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vehiclerecognition.settings')  # Use your project name
django.setup()

# Streamlit UI
st.title("Dynamic Vehicle Identification")
st.write("Welcome to the Vehicle Recognition Streamlit App!")
