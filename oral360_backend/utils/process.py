import base64
import cv2
import numpy as np
from ultralytics import YOLO

# Load YOLO model
model = YOLO("models/best.pt")

# Class labels used by your model
CLASS_NAMES = {
    0: "Caries",
    1: "Missing Tooth",
    2: "Plaque",
    3: "Gum Recession"
}

# Confidence threshold (can be adjusted for testing)
CONFIDENCE_THRESHOLD = 0.1
SAVE_DEBUG_IMAGE = True
DEBUG_IMAGE_PATH = "detection_debug.jpg"

def run_detection(base64_image, tooth_number):
    try:
        # Decode base64 to OpenCV image
        img_bytes = base64.b64decode(base64_image)
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            print("❌ Failed to decode image.", flush=True)
            return {"status": "error", "message": "Image decode failed"}

        # Run YOLOv8 detection
        results = model(img, verbose=False)[0]
        detections = []

        for r in results.boxes.data.tolist():
            x1, y1, x2, y2, conf, cls = r
            cls = int(cls)
            conf = float(conf)

            label = CLASS_NAMES.get(cls, "Unknown")
            print(f"🔍 Detected: {label} with {conf:.2f} confidence", flush=True)

            if conf >= CONFIDENCE_THRESHOLD:
                detections.append({
                    "tooth": tooth_number,
                    "issue": label,
                    "confidence": round(conf, 2)
                })

                # Draw box if needed
                if SAVE_DEBUG_IMAGE:
                    cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                    cv2.putText(
                        img,
                        f"{label} {conf:.2f}",
                        (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 255),
                        2
                    )

        # Save debug image
        if SAVE_DEBUG_IMAGE:
            cv2.imwrite(DEBUG_IMAGE_PATH, img)
            print(f"🖼️ Debug image saved to {DEBUG_IMAGE_PATH}", flush=True)

        # Final result
        return {
            "status": "success",
            "tooth": tooth_number,
            "detections": detections
        }

    except Exception as e:
        print(f"❌ Error during detection: {e}", flush=True)
        return {
            "status": "error",
            "message": str(e)
        }
