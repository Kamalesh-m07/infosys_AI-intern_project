Dynamic Vehicle Identification and Tracker:


This project allows users to upload an image of a vehicle to detect its number plate and retrieve car details. The project uses machine learning and Optical Character Recognition (OCR) to recognize number plates and provides related vehicle information.

Features:

Image Upload:
Users can upload car images to be processed.


OCR Processing:
The system detects the vehicle number plate using Tesseract OCR.

Vehicle Information Retrieval:
The system provides details about the vehicle after processing the number plate.
User Registration and Login: Users can register, log in, and track their uploaded images and detected plates.
Tech Stack

Backend: Django

Database: SQLite

Frontend: HTML, CSS (with Neon theme), JavaScript

OCR: Tesseract


Installation
Prerequisites:

Python 3.x
pip (Python package installer)
Tesseract OCR installed
A GitHub account (for deployment)


Steps: to setup

Create a virtual environment:

python -m venv venv
Activate the virtual environment:

On Windows:

venv\Scripts\activate

On macOS/Linux:

source venv/bin/activate


Install dependencies:


pip install -r requirements.txt


Configure Tesseract OCR:

Download and install Tesseract OCR.
Add the Tesseract executable to your system’s PATH.

Migrate the database:


python manage.py migrate



