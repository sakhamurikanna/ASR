from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydub import AudioSegment
import speech_recognition as sr
import shutil
import os
from fastapi.requests import Request

app = FastAPI()

# Directory to save uploaded files
UPLOAD_DIRECTORY = "uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Serve static files (JavaScript)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Serve HTML templates
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def get_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_audio_file(audioFile: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIRECTORY}/{audioFile.filename}"
    with open(file_location, "wb") as file:
        shutil.copyfileobj(audioFile.file, file)

    # Convert the audio file to WAV format with 16 kHz sample rate
    converted_file_location = f"{UPLOAD_DIRECTORY}/converted.wav"
    convert_to_wav(file_location, converted_file_location)

    # Process the audio file and return the result
    result = recognize_speech(converted_file_location)
    return {"text": result}

def convert_to_wav(input_file: str, output_file: str, sample_rate: int = 16000):
    """Convert audio file to WAV format with a specific sample rate."""
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_frame_rate(sample_rate)
    audio.export(output_file, format="wav")

def recognize_speech(file_path: str) -> str:
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language="te-IN")
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Could not get results!!; {e}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
