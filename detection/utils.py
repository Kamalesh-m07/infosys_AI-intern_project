import cv2
import numpy as np
import joblib
import pytesseract  # For OCR on the detected number plate
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

# Load the number plate detection model (replace with your model path)
model_path = 'detection/svm_model.pkl'
plate_model = joblib.load(model_path)

# Function to preprocess the uploaded image
def preprocess_image(image_path):
    img = cv2.imread(image_path)  # Load image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Reduce noise
    edged = cv2.Canny(blurred, 50, 200)  # Edge detection
    
    return img, gray, edged

def detect_number_plate(image_path):
    img, gray, edged = preprocess_image(image_path)

    # Find contours in the edged image
    contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        
        # Filter based on the number of corners (license plates are usually rectangular)
        if len(approx) == 4:  
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / h

            # Filter based on aspect ratio (license plates usually have a width > height)
            if 2 < aspect_ratio < 6 and w > 50:
                plate_img = gray[y:y+h, x:x+w]
                
                # Apply thresholding to improve OCR accuracy
                _, plate_img = cv2.threshold(plate_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # Save cropped number plate (optional)
                cv2.imwrite("extracted_number_plate.jpg", plate_img)

                # Perform OCR
                plate_text = pytesseract.image_to_string(plate_img, config='--psm 7').strip()

                return plate_text, plate_img

    return "Number plate not detected", None
# Process video for number plate detection
def process_video(video_path):
    results = []
    try:
        cap = cv2.VideoCapture(video_path)
        frame_counter = 0
        frame_interval = 30  # Process every 30th frame

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_counter % frame_interval == 0:
                # Convert frame to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Apply Gaussian Blur to reduce noise
                blurred = cv2.GaussianBlur(gray, (5, 5), 0)

                # Apply Adaptive Thresholding to highlight text
                thresholded = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

                # Convert to PIL image for Tesseract OCR
                pil_frame = Image.fromarray(thresholded)

                # Perform OCR
                plate_text = pytesseract.image_to_string(pil_frame, config='--psm 5 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789').strip()

                if plate_text:
                    results.append(plate_text)

            frame_counter += 1

        cap.release()
    except Exception as e:
        return f"An error occurred while processing the video: {str(e)}"

    return " | ".join(results) if results else "No text detected in the video."

# Example usage in a Django view
def handle_uploaded_image(image: InMemoryUploadedFile):
    state, district = detect_number_plate(image)
    if state == "Unknown":
        return "Number plate could not be classified"
    else:
        return f"Vehicle belongs to {state}, {district}"

def handle_uploaded_video(video: InMemoryUploadedFile):
    results = process_video(video)
    return results if results else ["No plates detected in the video."]
