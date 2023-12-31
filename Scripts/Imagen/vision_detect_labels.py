import time
# Imports the Google Cloud client library
from google.cloud import vision
import os
from google_search import retrieve_from_google


def detect_labels(path):
    """Detects labels in the file."""

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)

    labels = [label.description for label in response.label_annotations]
    query_Google = ' '.join(labels)
    print("Query: ", query_Google)

    retrieve_from_google(query_Google, 1)
    time.sleep(1)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )