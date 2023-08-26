import threading
from eyes_controller import EyesController
from cam import WebcamStream

def main():
    # Create an instance of EyesController
    eyes_controller = EyesController()

    # Create an instance of WebcamStream with the EyesController instance
    webcam_stream = WebcamStream(eyes_controller=eyes_controller, frame_rate=5)  # Adjust frame rate if needed

    # Start the threads
    eyes_controller.eyes_thread_instance.start()
    webcam_stream.start()

    try:
        while True:
            pass  # Keep the main thread alive
    except KeyboardInterrupt:
        # Stop both threads when the main program is stopped
        webcam_stream.stop()
        eyes_controller.eyes_thread_instance.join()  # Wait for the eyes thread to finish
        print("\nMain program stopped.")

if __name__ == "__main__":
    main()
