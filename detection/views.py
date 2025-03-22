from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

from .utils import process_video
from .forms import ContactForm, MediaUploadForm
from PIL import Image
import cv2
import pytesseract
import os
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load mappings of state and district codes (this should be a dictionary or function you define)
state_district_map = {
    "KA": "Karnataka\nOWNER NAME:kumaran\nINSURANCE:ACTIVE",
    "MH": "Maharashtra\nOWNER NAME:RAJ\nINSURANCE:ACTIVE",
    "DL": "Delhi\nOWNER NAME:SIVA\nINSURANCE:ACTIVE",
    "TN": "Tamil Nadu\nOWNER NAME:RAJESH\nINSURANCE:NOT ACTIVE",
    "HR": "Haryana\nOWNER NAME:Harvinder Singh\nINSURANCE:ACTIVE",
    # Add other mappings as needed
}

# Function to extract state and district from the vehicle number
def extract_state_and_district(plate_text):
    state_code = plate_text[:2].upper()
    return state_district_map.get(state_code, "Unknown State")

# Function to process video frame-by-frame
def video_upload_view(request):
    if request.method == 'POST' and request.FILES.get('video'):
        video_file = request.FILES['video']
        fs = FileSystemStorage()
        filename = fs.save(video_file.name, video_file)
        video_path = os.path.join(fs.location, filename)  # Ensure correct file path

        # Call process_video with the file path (not the file object)
        plate_text = process_video(video_path)  

        os.remove(video_path)  # Clean up video file after processing

        return JsonResponse({"detected_text": plate_text if plate_text else "No text detected in video."})

    return JsonResponse({"error": "Invalid request. Please upload a video."}, status=400)
# Home view
def home_view(request):
    return render(request, 'base.html')

# Register view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('upload_image')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = UserCreationForm()
    return render(request, 'detection/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('upload_image')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid login details.")
    else:
        form = AuthenticationForm()
    return render(request, 'detection/login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')

# Upload Media view for vehicle number plate detection
def upload_media_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to upload media.")
        return redirect('login')

    if request.method == 'POST':
        form = MediaUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get('image')
            video = form.cleaned_data.get('video')
            try:
                if image:
                    # Process the uploaded image
                    img = Image.open(image)
                    plate_text = pytesseract.image_to_string(img, config='--psm 8').replace("\n", "").strip()
                elif video:
                    # Save the uploaded video temporarily
                    video_path = os.path.join("temp_videos", video.name)
                    os.makedirs("temp_videos", exist_ok=True)  # Ensure the temp_videos directory exists
                    with open(video_path, 'wb') as f:
                        for chunk in video.chunks():
                            f.write(chunk)
                    # Process the video
                    plate_text = process_video(video_path)
                    os.remove(video_path)  # Clean up the temporary file
                else:
                    plate_text = None

                if plate_text:
                    state = extract_state_and_district(plate_text)
                    result = f"Detected Vehicle Number: {plate_text}, State: {state}"
                else:
                    result = "No text detected. Please try again with a clearer media file."

                return render(request, 'detection/result.html', {'prediction': result})

            except Exception as e:
                messages.error(request, f"An error occurred while processing the media: {str(e)}")
                return redirect('upload_image')
        else:
            messages.error(request, "Please upload a valid image or video.")
    else:
        form = MediaUploadForm()

    return render(request, 'detection/upload_image.html', {'form': form})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactForm()
    
    return render(request, 'detection/contact.html', {'form': form})

# Services page view
def services_view(request):
    return render(request, 'detection/service.html')
