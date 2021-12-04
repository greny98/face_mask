import time

import cv2
import numpy as np

from detection import utils, predict


def execute(frame, model):
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

    return frame


path_dict = {
    'checkpoint': 'configs/my_ckpt/ckpt-5',
    'pipeline': 'configs/custom.config',
    'label_map': 'configs/label_map.pbtxt'
}
model = utils.load_model(path_dict)
cap = cv2.VideoCapture(0)
while cap.isOpened():
    start_time = time.time()
    ret, frame = cap.read()
    if not ret:
        break
    frame = execute(frame, model)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow("frame", frame)
    print("====", 1 / (time.time() - start_time))
    key = cv2.waitKey(3) & 0xFF
    if key & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
