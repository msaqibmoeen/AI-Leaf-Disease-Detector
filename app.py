from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import base64, logging
from LeafDisease.main import LeafDiseaseDetector
from LeafDisease.config import AppConfig
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Leaf Disease Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    cfg = AppConfig.from_env()
    detector = LeafDiseaseDetector(cfg)
    logger.info("AI engine initialized successfully.")
except Exception as e:
    detector = None
    logger.error(f"AI engine initialization failed: {e}")

@app.get("/")
def home():
    return {
        "message": "Leaf Disease Detection API Running",
        "endpoints": ["/disease-detection-file"],
    }
@app.post("/disease-detection-file")
async def detect_disease(file: UploadFile = File(...)):
    if detector is None:
        return JSONResponse({"error": "AI engine not initialized."}, status_code=500)
    try:
        image_bytes = await file.read()
        b64_image = base64.b64encode(image_bytes).decode()
        result = detector.analyze_leaf_image_base64(b64_image)
        return JSONResponse(result)
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)