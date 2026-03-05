# ⚡ ChartMind AI

**Professional AI-powered trading chart analysis platform.**
Upload a chart screenshot → Get instant technical analysis with annotated charts.

---

## 🚀 Quick Start

### Backend (Python FastAPI)

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Server runs at: **http://localhost:8000**

### Frontend (Next.js)

```bash
cd frontend
npm install
npm run dev
```

App runs at: **http://localhost:3000**

---

## 📁 Project Structure

```
chartmind/
├── backend/
│   ├── main.py          # FastAPI server + endpoints
│   ├── analyzer.py      # OpenCV chart analysis engine
│   ├── requirements.txt # Python dependencies
│   ├── uploads/         # Input chart images (auto-created)
│   └── outputs/         # Annotated chart outputs (auto-created)
│
├── frontend/
│   ├── pages/
│   │   ├── index.jsx    # Landing page
│   │   ├── upload.jsx   # Upload & analyze page
│   │   ├── results.jsx  # Analysis results page
│   │   └── feed.jsx     # Public analysis feed
│   ├── components/
│   │   ├── ChartCanvas.jsx      # Chart annotation renderer
│   │   ├── FeedCard.jsx         # Feed item card
│   │   ├── ShareCard.jsx        # Viral share card
│   │   └── TrendBadge.jsx       # Trend indicator badge
│   ├── package.json
│   └── next.config.js
│
└── README.md
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/analyze` | Upload & analyze chart image |
| GET | `/api/feed?sort=trending` | Get public analysis feed |
| GET | `/api/analysis/{id}` | Get specific analysis |
| POST | `/api/analysis/{id}/vote` | Vote on prediction accuracy |

### Example Usage

```bash
# Analyze a chart
curl -X POST http://localhost:8000/api/analyze \
  -F "file=@my_chart.png"

# Get feed
curl http://localhost:8000/api/feed?sort=trending
```

---

## 🧠 Analysis Pipeline

```
Chart Image
    ↓
Detect Chart Region (OpenCV)
    ↓
Extract Price Structure (brightness analysis)
    ↓
Find Support & Resistance (Hough line transform)
    ↓
Detect Trendlines (geometry)
    ↓
Identify Patterns (heuristics + ML)
    ↓
Detect Indicators (RSI, MACD, MAs)
    ↓
Generate AI Analysis (GPT-style text)
    ↓
Annotate Chart (OpenCV overlay)
    ↓
Return JSON + Annotated Image
```

---

## 📊 Detected Patterns

- Ascending / Descending Triangle
- Symmetrical Triangle
- Bull Flag / Bear Flag
- Head & Shoulders
- Double Top / Double Bottom
- Cup & Handle
- Wedge (Rising / Falling)
- Tight Consolidation / Range

## 📈 Detected Indicators

- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- Moving Averages (SMA, EMA)
- Bollinger Bands
- Volume

---

## 🔧 Configuration

Edit `backend/analyzer.py` to customize:

```python
# Adjust sensitivity
H_LINE_THRESHOLD = 80     # Hough line detection threshold
CLUSTER_THRESHOLD = 0.05  # Level clustering (% of chart height)
PATTERN_MIN_CONFIDENCE = 60  # Minimum pattern confidence %
```

---

## 🌐 Frontend Next.js Setup

```bash
# Create Next.js app
npx create-next-app@latest frontend --js --tailwind --no-app

# Install additional deps
cd frontend
npm install lucide-react

# Copy component files into pages/
# Set backend URL in .env.local:
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

npm run dev
```

---

## ⚡ Features

- ✅ No paid API keys required
- ✅ Fully local / self-hosted
- ✅ OpenCV-based image analysis
- ✅ Real-time analysis progress
- ✅ Annotated chart download
- ✅ Viral share cards
- ✅ Public analysis feed
- ✅ Accuracy voting system
- ✅ Dark mode UI
- ✅ Mobile responsive

---

## 📦 Dependencies

**Backend:**
- FastAPI — API framework
- OpenCV — Computer vision & chart analysis
- NumPy — Numerical operations
- Pillow — Image processing
- Uvicorn — ASGI server

**Frontend:**
- Next.js — React framework
- TailwindCSS — Styling
- React Canvas — Chart annotation

---

## 📄 License

MIT — Free for personal and commercial use.

---

Built with ❤️ by ChartMind AI Team
