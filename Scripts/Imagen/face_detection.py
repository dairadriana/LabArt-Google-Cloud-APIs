from google.cloud import vision
import cv2
from google.protobuf.json_format import MessageToDict
from google.cloud import vision_v1p3beta1 as vision
from PIL import Image, ImageDraw

# [START vision_face_detection_tutorial_send_request]
def detect_face(face_file, max_results=4):
    """Uses the Vision API to detect faces in the given file.

    Args:
        face_file: A file-like object containing an image with faces.

    Returns:
        An array of Face objects with information about the picture.
    """
    # [START vision_face_detection_tutorial_client]
    client = vision.ImageAnnotatorClient()
    # [END vision_face_detection_tutorial_client]

    content = face_file.read()
    image = vision.Image(content=content)

    return client.face_detection(image=image, max_results=max_results).face_annotations

# [START vision_face_detection_tutorial_process_response]
def highlight_faces(image, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.

    Args:
      image: a file containing the image with the faces.
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    # Sepecify the font-family and the font-size
    for face in faces:
        box = [(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices]
        draw.line(box + [box[0]], width=5, fill="#00ff00")
        # Place the confidence value/score of the detected faces above the
        # detection box in the output image
        draw.text(
            (
                (face.bounding_poly.vertices)[0].x,
                (face.bounding_poly.vertices)[0].y - 30,
            ),
            str(format(face.detection_confidence, ".3f")) + "%",
            fill="#FF0000",
        )
    im.save(output_filename)

def detect_face_in_realtime():
    # Inicializa el cliente de Vision
    client = vision.ImageAnnotatorClient()

    # Inicializa la webcam
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convierte el marco de la cámara a un formato que Cloud Vision pueda entender
        _, img_encoded = cv2.imencode(".jpg", frame)
        image = vision.Image(content=img_encoded.tostring())

        # Detecta caras en la imagen
        response = client.face_detection(image=image)
        faces = response.face_annotations

        for face in faces:
            detection_confidence = face.detection_confidence
            vertices = face.bounding_poly.vertices
            for i in range(3):
                cv2.line(
                    frame,
                    (vertices[i].x, vertices[i].y),
                    (vertices[i + 1].x, vertices[i + 1].y),
                    (0, 255, 0),
                    2,
                )
            cv2.line(
                frame,
                (vertices[3].x, vertices[3].y),
                (vertices[0].x, vertices[0].y),
                (0, 255, 0),
                2,
            )

            cv2.putText(
                frame,
                f"Confianza: {detection_confidence:.2f}",
                (vertices[0].x, vertices[0].y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (0, 255, 0),
                1,
            )

        # Muestra el marco de la webcam
        cv2.imshow("Webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Libera la cámara y cierra todas las ventanas
    cap.release()
    cv2.destroyAllWindows()