import numpy as np
import cv2
from playsound import playsound
import threading
from detection import utils
import pyttsx3



def remind(engine):
    import time
    global is_reminding
    is_reminding = True
    engine.say("Please Wear Face Mask")
    engine.runAndWait()
    time.sleep(1)
    is_reminding = False


is_reminding = False


def execute(frame, model,engine):
    # Convert to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # Predict
    img_np = np.array(image)
    results = utils.detect_fn(img_np, model)
    num_detections = int(results.pop('num_detections'))
    results = {key: value[0, :num_detections].numpy()
               for key, value in results.items()}
    results['num_detections'] = num_detections
    # Check need mask
    need_mask, results = utils.check_need_mask(results, 0.8)

    cmap = [(25, 25, 182), (0, 255, 0), (11, 94, 235)]

    fh, fw, fc = image.shape
    for label, bbox in results:
        y1, x1, y2, x2 = bbox
        y1 = int(y1 * fh)
        x1 = int(x1 * fw)
        y2 = int(y2 * fh)
        x2 = int(x2 * fw)
        cv2.rectangle(frame, (x1, y1), (x2, y2), cmap[label], 4)

    # Check from without mask to with mask
    if need_mask and (not is_reminding):
        t1 = threading.Thread(target=remind, args=[engine])
        t1.start()
    return frame
