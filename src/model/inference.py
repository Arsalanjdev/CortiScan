from pathlib import Path

import onnxruntime as ort

session = ort.InferenceSession(Path(__file__).parent.parent / "brain_model.onnx")
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name


def infer(img_batch):
    """
    Performs inference on a preprocessed image batch using a loaded ONNX model.

    The function runs the ONNX model on the input batch, retrieves the raw output
    scores, determines the predicted class index, maps it to a human-readable label,
    and returns the confidence score of the predicted class.

    :param img_batch: NumPy array of shape (batch_size, H, W, C), preprocessed
                      and ready to be fed into the model. Typically normalized
                      to [0,1] and with dtype float32.
    :type img_batch: np.ndarray

    :return: A tuple containing:
        - predicted_label (str): The human-readable class label ("no_tumor" or "tumor")
                                 of the first image in the batch.
        - confidence (float): The confidence score of the predicted class for the first image.
    :rtype: Tuple[str, float]
    """

    # Run ONNX inference
    outputs = session.run([output_name], {input_name: img_batch})
    pred = outputs[0]  # Raw output scores (logits or probabilities)

    pred_idx = pred.argmax(axis=1)[0]
    classes = ["No Tumor", "Tumor"]

    # Confidence of the predicted class for the first image
    confidence = pred[0, pred_idx]

    return classes[pred_idx], confidence
