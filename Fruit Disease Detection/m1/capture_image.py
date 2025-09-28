import cv2

# Open the camera (0 is the default webcam, change if using an external camera)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()  # Read frame from the camera
    cv2.imshow("Press 's' to Save, 'q' to Quit", frame)  # Show the frame

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):  # Press 's' to save the image
        cv2.imwrite("captured_images/fruit.jpg", frame)  # Save image to a specific folder
        print("Image saved successfully!")
    elif key == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
