import threading
import time
import serial
import pyautogui
import cv2
import mediapipe as mp
import math

# Set your Arduino's COM port here
# Replace 'COM7' with the appropriate COM port for your system
arduino_port = 'COM7'  
baud_rate = 9600  # Set the baud rate for serial communication

# Initialize serial connection
arduino = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # Wait for the serial connection to establish

# Initialize MediaPipe for hand detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)  # Detect a maximum of 1 hand
mp_drawing = mp.solutions.drawing_utils  # Utility to draw landmarks

# Initialize webcam for hand gesture control
cap = cv2.VideoCapture(0)  # Use default camera

# Variables for time tracking and position of the hand
previous_action_time = time.time()  # Track the time of the last action
previous_position = None  # Store the previous position of hand landmarks

# Function to handle button control from the Arduino
def button_control():
    try:
        while True:
            if arduino.in_waiting > 0:
                # Read the incoming data from the Arduino
                line = arduino.readline().decode('utf-8').strip()

                # Check the command sent from Arduino and trigger respective actions
                if line == "PLAY_PAUSE":
                    pyautogui.press('space')  # Play/Pause YouTube video
                    print("Play/Pause triggered")
                elif line == "MUTE_UNMUTE":
                    pyautogui.press('m')  # Mute/Unmute YouTube video
                    print("Mute/Unmute triggered")
                elif line == "FULL_SCREEN":
                    pyautogui.press('f')  # Toggle Full Screen in YouTube
                    print("Full Screen triggered")

    except KeyboardInterrupt:
        print("Exiting...")  # Handle keyboard interrupt to exit gracefully

    finally:
        arduino.close()  # Close the serial connection when exiting

# Function to calculate the Euclidean distance between two points
def euclidean_distance(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)

# Function to detect gestures based on hand landmarks
def detect_gesture(landmarks):
    global previous_action_time, previous_position

    # Get the X coordinates of key points (thumb, pinky, index finger, wrist)
    thumb_x = landmarks[mp_hands.HandLandmark.THUMB_TIP].x
    pinky_x = landmarks[mp_hands.HandLandmark.PINKY_TIP].x
    index_x = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
    wrist_x = landmarks[mp_hands.HandLandmark.WRIST].x

    current_time = time.time()  # Track the current time

    # Check if previous hand position is available
    if previous_position is not None:
        # Calculate hand movement based on the wrist's previous and current position
        hand_movement = euclidean_distance(landmarks[mp_hands.HandLandmark.WRIST], previous_position[mp_hands.HandLandmark.WRIST])

        # If hand movement is too small, skip gesture detection
        if hand_movement < 0.01:  # Threshold to ignore small movements
            return

    # Gesture detection logic:
    # 1. Short swipe gestures (for skipping video 5 seconds forward/backward)
    if pinky_x < thumb_x and abs(index_x - wrist_x) < 0.15 and current_time - previous_action_time > 1.5:
        pyautogui.press('right')  # Skip 5 seconds forward
        print("Skip 5 seconds forward")
        previous_action_time = current_time
    elif pinky_x > thumb_x and abs(index_x - wrist_x) < 0.15 and current_time - previous_action_time > 1.5:
        pyautogui.press('left')  # Skip 5 seconds backward
        print("Skip 5 seconds backward")
        previous_action_time = current_time

    # 2. Long swipe gestures (for next/previous video)
    elif pinky_x < thumb_x and abs(index_x - wrist_x) > 0.15 and current_time - previous_action_time > 1.5:
        pyautogui.hotkey('shift', 'n')  # Next video (shift + N)
        print("Next video")
        previous_action_time = current_time
    elif pinky_x > thumb_x and abs(index_x - wrist_x) > 0.15 and current_time - previous_action_time > 1.5:
        pyautogui.hotkey('shift', 'p')  # Previous video (shift + P)
        print("Previous video")
        previous_action_time = current_time

    # Store the current hand position for the next frame
    previous_position = landmarks

# Function to handle hand gesture control
def hand_gesture_control():
    while cap.isOpened():
        ret, frame = cap.read()  # Capture frame from webcam
        if not ret:
            print("Failed to grab frame")  # Handle failed frame capture
            break

        # Convert the frame to RGB format (required by MediaPipe)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)  # Process the frame to detect hands

        # If hand landmarks are detected, process them
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Detect gesture based on the hand landmarks
                detect_gesture(hand_landmarks.landmark)

                # Draw hand landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Display the frame with the drawn landmarks
        cv2.imshow("Hand Gesture Control", frame)

        # Exit the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources when done
    cap.release()
    cv2.destroyAllWindows()

# Create separate threads for button control and hand gesture control
button_control_thread = threading.Thread(target=button_control)
hand_gesture_control_thread = threading.Thread(target=hand_gesture_control)

# Start the threads
button_control_thread.start()
hand_gesture_control_thread.start()

# Wait for both threads to finish
button_control_thread.join()
hand_gesture_control_thread.join()
