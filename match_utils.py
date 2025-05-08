import cv2
import numpy as np
import cloudinary.uploader
import os
from tempfile import NamedTemporaryFile

template_path = "static/mickey_template.png"
mickey_template = cv2.imread(template_path, 0)
mickey_template = cv2.threshold(mickey_template, 127, 255, cv2.THRESH_BINARY)[1]
template_contours, _ = cv2.findContours(mickey_template, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

def match_mickey(uploaded_file):
    with NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        uploaded_file.save(tmp.name)
        img_path = tmp.name

    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    best_score = float("inf")
    best_contour = None
    for c in contours:
        score = cv2.matchShapes(template_contours[0], c, 1, 0.0)
        if score < best_score:
            best_score = score
            best_contour = c

    match_score = max(0, 100 - (best_score * 1000))
    output_img = img.copy()
    if best_contour is not None:
        cv2.drawContours(output_img, [best_contour], -1, (0, 255, 0), 3)

    result_img_path = img_path.replace(".jpg", "_result.jpg")
    cv2.imwrite(result_img_path, output_img)

    cloud_result = cloudinary.uploader.upload(result_img_path, folder="hiddenmickey/")
    return {
        "score": round(match_score, 2),
        "image_url": cloud_result["secure_url"]
    }
