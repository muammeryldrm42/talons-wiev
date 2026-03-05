"""
ChartMind AI - Backend API
FastAPI server for chart analysis
Run: python main.py
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import uuid
import json
import os
import time
from pathlib import Path
from analyzer import ChartAnalyzer

app = FastAPI(title="ChartMind AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
ANALYSES_FILE = Path("analyses.json")

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

analyzer = ChartAnalyzer()


def load_analyses():
    if ANALYSES_FILE.exists():
        with open(ANALYSES_FILE) as f:
            return json.load(f)
    return []


def save_analysis(analysis: dict):
    analyses = load_analyses()
    analyses.insert(0, analysis)
    analyses = analyses[:100]  # keep last 100
    with open(ANALYSES_FILE, "w") as f:
        json.dump(analyses, f, indent=2)


@app.post("/api/analyze")
async def analyze_chart(file: UploadFile = File(...)):
    """Analyze an uploaded trading chart image."""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    analysis_id = str(uuid.uuid4())[:8]
    timestamp = int(time.time())

    input_path = UPLOAD_DIR / f"{analysis_id}_input.png"
    output_path = OUTPUT_DIR / f"{analysis_id}_annotated.png"

    contents = await file.read()
    with open(input_path, "wb") as f:
        f.write(contents)

    try:
        result = analyzer.analyze(str(input_path), str(output_path))
        analysis = {
            "id": analysis_id,
            "timestamp": timestamp,
            "filename": file.filename,
            "input_image": f"/uploads/{analysis_id}_input.png",
            "output_image": f"/outputs/{analysis_id}_annotated.png",
            "trend": result["trend"],
            "support_levels": result["support_levels"],
            "resistance_levels": result["resistance_levels"],
            "patterns": result["patterns"],
            "indicators": result["indicators"],
            "analysis_text": result["analysis_text"],
            "trade_idea": result["trade_idea"],
            "confidence": result["confidence"],
            "annotations": result["annotations"],
            "win_rate": 0,
            "votes": 0,
            "accuracy_votes": 0,
        }
        save_analysis(analysis)
        return JSONResponse(content=analysis)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/feed")
async def get_feed(sort: str = "newest", limit: int = 20):
    """Get public analysis feed."""
    analyses = load_analyses()
    if sort == "trending":
        analyses.sort(key=lambda x: x.get("votes", 0), reverse=True)
    elif sort == "accurate":
        analyses.sort(key=lambda x: x.get("win_rate", 0), reverse=True)
    return JSONResponse(content=analyses[:limit])


@app.get("/api/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    """Get a specific analysis by ID."""
    analyses = load_analyses()
    for a in analyses:
        if a["id"] == analysis_id:
            return JSONResponse(content=a)
    raise HTTPException(status_code=404, detail="Analysis not found")


@app.post("/api/analysis/{analysis_id}/vote")
async def vote_accuracy(analysis_id: str, correct: bool = True):
    """Vote on prediction accuracy."""
    analyses = load_analyses()
    for a in analyses:
        if a["id"] == analysis_id:
            a["accuracy_votes"] = a.get("accuracy_votes", 0) + 1
            if correct:
                a["votes"] = a.get("votes", 0) + 1
            total = a["accuracy_votes"]
            wins = a["votes"]
            a["win_rate"] = round((wins / total) * 100) if total > 0 else 0
            with open(ANALYSES_FILE, "w") as f:
                json.dump(analyses, f, indent=2)
            return JSONResponse(content=a)
    raise HTTPException(status_code=404, detail="Analysis not found")


app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

if __name__ == "__main__":
    print("🚀 ChartMind AI Backend starting on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
