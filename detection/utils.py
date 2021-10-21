import tensorflow as tf
from object_detection.utils import config_util
from object_detection.builders import model_builder


def load_model(path_dict):
    config = config_util.get_configs_from_pipeline_file(path_dict['pipeline'])
    model = model_builder.build(config['model'], is_training=False)
    ckpt = tf.compat.v2.train.Checkpoint(model=model)
    ckpt.restore(path_dict['checkpoint']).expect_partial()
    return model


@tf.function
def detect_fn(image_np, model):
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = tf.expand_dims(input_tensor, axis=0)
    input_tensor = tf.cast(input_tensor, tf.float32)
    preprocessed_tensor, shape = model.preprocess(input_tensor)
    prediction_dict = model.predict(preprocessed_tensor, shape)
    results = model.postprocess(prediction_dict, shape)
    return results


def check_need_mask(results, threshold=0.75):
    need_mask = False
    scores = tf.convert_to_tensor(results['detection_scores'])
    boxes = tf.convert_to_tensor(results['detection_boxes'])
    labels = tf.convert_to_tensor(results['detection_classes'])
    selected_indices = tf.image.non_max_suppression(boxes, scores, max_output_size=10, score_threshold=threshold)
    boxes = tf.gather(boxes, selected_indices)
    labels = tf.gather(labels, selected_indices)

    # Find without mask
    results = []
    for label, bbox in zip(labels.numpy().astype(int), boxes.numpy()):
        if label != 1:
            need_mask = True
        results.append((label, bbox))
    return need_mask, results
