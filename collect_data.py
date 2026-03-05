import cv2
import mediapipe as mp
import csv
import os
import sys

# Initialize Mediapipe Hand solution
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Get the label from command line (e.g., 'A', 'B', 'C')
if len(sys.argv) < 2:
    print("Usage: python collect_data.py <LABEL>")
    sys.exit()
label = sys.argv[1]

# Create dataset directory
if not os.path.exists('asl_dataset.csv'):
    with open('asl_dataset.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        # 21 points * (x,y,z) + 1 label = 64 columns
        header = [f'p{i}_{coord}' for i in range(21) for coord in ['x', 'y', 'z']] + ['label']
        writer.writerow(header)

cap = cv2.VideoCapture(0)
count = 0

print(f"Collecting data for label: {label}. Press 'q' to stop.")

while count < 500: # Collect 500 frames per gesture
    ret, frame = cap.read()
    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extract the 63 coordinates
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])
            
            # Save to CSV
            with open('asl_dataset.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(landmarks + [label])
            
            # Draw on screen for feedback
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            count += 1

    cv2.putText(frame, f"Collected: {count}/500", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Data Collection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
