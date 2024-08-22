import os
import cv2

class Camera():
    def __init__(self) -> None:
        self.transaction_id = ''
        camera_username = os.getenv('CAMERA_USERNAME')
        camera_password = os.getenv('CAMERA_PASSWORD')
        camera_ip = os.getenv('CAMERA_IP')
        camera_api = os.getenv('CAMERA_API')

        self.camear_url = f"http:/{camera_username}:{camera_password}@{camera_ip}/{camera_api}"

    def capture(self, transaction_id):
        self.transaction_id = transaction_id

        # Connect to the IP camera
        cap = cv2.VideoCapture(self.camear_url)

        if not cap.isOpened():
            print("Cannot connect to the IP camera")
            return False

        # Capture a single frame
        ret, frame = cap.read()

        if ret:
            # Save the captured image to a file
            cv2.imwrite(f'public/images/{transaction_id}.jpg', frame)
            print(f"Image captured and saved on images")

        else:
            print("Failed to capture image")

        # Release the camera
        cap.release()
        cv2.destroyAllWindows()
        return True