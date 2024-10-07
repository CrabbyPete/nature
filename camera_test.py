from picamera2 import Picamera2
from libcamera import controls

def main():
    picam2 = Picamera2()
    picam2.start(show_preview=False)
    picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous,
                         "AfSpeed": controls.AfSpeedEnum.Fast})

    picam2.start_and_capture_files("./fastfocus-test{:d}.jpg", num_files=1, delay=0)

if __name__ == "__main__":
    main()