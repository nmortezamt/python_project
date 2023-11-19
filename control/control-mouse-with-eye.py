import cv2
import dlib
import pyautogui

# Initialize the webcam and dlib's face detector and facial landmarks predictor
cap = cv2.VideoCapture(0)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Function to get the coordinates of the left and right eyes
def get_eye_coordinates(shape, eye_indices):
    eye_coords = []
    for i in eye_indices:
        x, y = shape.part(i).x, shape.part(i).y
        eye_coords.append((x, y))
    return eye_coords

while True:
    ret, frame = cap.read()
    
    # Convert the frame to grayscale for dlib processing
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = detector(gray)

    for face in faces:
        # Get facial landmarks
        shape = predictor(gray, face)
        
        # Get the coordinates of the left and right eyes
        left_eye_coords = get_eye_coordinates(shape, range(42, 48))
        right_eye_coords = get_eye_coordinates(shape, range(36, 42))

        # Calculate the midpoint of each eye
        left_eye_midpoint = (
            sum([x for x, y in left_eye_coords]) // len(left_eye_coords),
            sum([y for x, y in left_eye_coords]) // len(left_eye_coords)
        )
        right_eye_midpoint = (
            sum([x for x, y in right_eye_coords]) // len(right_eye_coords),
            sum([y for x, y in right_eye_coords]) // len(right_eye_coords)
        )

        # Perform mouse control based on eye position
        pyautogui.click(left_eye_midpoint[0], left_eye_midpoint[1])  # Left eye click
        pyautogui.move(right_eye_midpoint[0], right_eye_midpoint[1])  # Right eye controls mouse movement

    # Display the frame
    cv2.imshow("Eye Tracking", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
