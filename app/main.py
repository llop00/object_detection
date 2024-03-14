from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import io
from PIL import Image

app = FastAPI()

# Load the YOLO model
model_path = 'yolov9c.pt'  # Model to use
model = YOLO(model_path)

@app.post("/detect/")
async def detect_objects(file: UploadFile = File(...)):
    try:
        # Read the uploaded image file directly into a bytes stream
        image_bytes = await file.read()
        
        # Convert bytes to a PIL Image
        image = Image.open(io.BytesIO(image_bytes))

        # Make a prediction
        results = model.predict(source=image, save=False, classes=[0, 2])

        # Convert results to JSON
        results_json = results[0].tojson()

        return JSONResponse(content=results_json)

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": f"An error occurred: {str(e)}"})