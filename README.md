# Hidden Mickey Detection API

## Endpoint
`POST /detect`
- **Form field**: `image` (multipart/form-data)
- **Response**:
```json
{
  "version": "1.0",
  "match_percent": 87.6,
  "highlighted_image_url": "https://...",
  "timestamp": "2025-05-02T00:00:00Z"
}
```

## Setup
```bash
pip install -r requirements.txt
python app.py
```

## Render Deployment
- Build command: `pip install -r requirements.txt`
- Start command: `python app.py`
- Environment variables:
  - `CLOUDINARY_URL`: your Cloudinary API URL
