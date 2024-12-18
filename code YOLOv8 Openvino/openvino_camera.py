import cv2
from ultralytics import YOLO
import time
import ipywidgets as widgets
import openvino.runtime as ov

# Initialize OpenVINO Core
model =  YOLO('yolov8n.pt')
model.export(format='openvino',dynamic=True,imgsz=(640,640),half=False)

core = ov.Core()

device = widgets.Dropdown(
    options=core.available_devices + ["GPU"],
    value='GPU',
    description='Device:',
    disabled=False,
)
device

# Load OpenVINO YOLOv8 model
ov_model = YOLO('yolov8n_openvino_model')

# Video source (0 for webcam or provide video file path)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    # Measure inference time
    start_time = time.time()
    results = ov_model(frame)
    end_time = time.time()

    print(f"Inference time: {end_time - start_time:.3f} seconds")

    # Annotate frame
    annotated_frame = results[0].plot()

    # Display the results
    cv2.imshow("YOLOv8 Inference", annotated_frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("Exiting...")
        break
        
# Release resources
cap.release()
cv2.destroyAllWindows()
print("Resources released. Program terminated.")
