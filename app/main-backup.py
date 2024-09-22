from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
import shutil
import os
import glob
import speech_recognition as sr
import joblib
import sys
from time import sleep
from pydub import AudioSegment

r = sr.Recognizer()
lid="te-IN"

base_directory = "/home/kotes/"

app = FastAPI()

# Allow CORS for development (adjust as necessary for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as necessary
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (JavaScript and CSS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Serve HTML templates
templates = Jinja2Templates(directory="app/templates")

# Directory to save uploaded files
UPLOAD_DIRECTORY = "uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
output_file = "output_audio.wav"

@app.get("/", response_class=HTMLResponse)
async def get_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_audio_file(audioFile: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIRECTORY}/{audioFile.filename}"
    with open(file_location, "wb") as file:
        shutil.copyfileobj(audioFile.file, file)

    # Process the audio file and return the result
    result = process_audio(file_location)
    return result

def convert_to_wav(input_file: str, output_file: str, sample_rate: int = 16000):
    """Convert audio file to WAV format with a specific sample rate."""
    # Load the input audio file
    audio = AudioSegment.from_file(input_file)
    
    # Set the sample rate
    audio = audio.set_frame_rate(sample_rate)
    
    # Export as WAV file
    audio.export(output_file, format="wav")    

def process_audio(file_path: str) -> str:
    # Replace this with your actual audio processing logic
    # For demonstration, we're just returning the file path
    #return f"Received file: {file_path}"
    AUDIO_FILE = os.path.join(base_directory, file_path)
    convert_to_wav(AUDIO_FILE, output_file)
    # aud_name=AUDIO_FILE.split('/')[-1].split('.')[0]
    #file=open(wav_path+"/"+aud_name+".txt","w")
    text="cant read wav file"
    try:
        sleep(10)    
        with sr.AudioFile(output_file) as source:
            audio = r.record(source)
        text = r.recognize_google(audio, language=lid)
        #file.write(aud_name +"\t"+text)
        return text
    except:
        #file.write(" "+"Error in segement"+" ")
        return text

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
