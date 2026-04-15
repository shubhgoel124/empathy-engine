from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import base64
from emotion import detector
from tts import tts_engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="The Empathy Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SynthesizeRequest(BaseModel):
    text: str

@app.post("/api/synthesize")
async def synthesize_api(req: SynthesizeRequest):
    result = detector.detect(req.text)
    audio_path, params = await tts_engine.synthesize(
        req.text, result["emotion"], result["confidence"]
    )

    with open(audio_path, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode()

    if os.path.exists(audio_path):
        os.remove(audio_path)

    return JSONResponse({
        "emotion": result["emotion"],
        "confidence": result["confidence"],
        "all_scores": result["all_scores"],
        "parameters": params,
        "audio_base64": audio_b64
    })

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "..", "frontend")
os.makedirs(FRONTEND_DIR, exist_ok=True)
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
