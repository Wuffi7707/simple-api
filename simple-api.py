from fastapi import FastAPI, UploadFile, File, Query, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
import shutil
import uuid
from PIL import Image
import os
import re

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific origins for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = os.getenv("SECRET_KEY", "defaultsecret")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",") if os.getenv("ALLOWED_HOSTS") else None
STORAGE_DIR = Path("/data/images")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

def sanitize_filename(name: str) -> str:
    name = name.replace("..", "").replace("/", "").replace("\\", "")
    return re.sub(r'[^a-zA-Z0-9._-]', '', name)

# Upload image
@app.post("/upload")
async def upload_image(file: UploadFile = File(...), secret: str = Header(None), host: str = Header(None)):
    if secret != SECRET_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    if ALLOWED_HOSTS and host not in ALLOWED_HOSTS:
        raise HTTPException(status_code=403, detail="Host not allowed")
    
    rand1, rand2 = sanitize_filename(uuid.uuid4().hex[:6]), sanitize_filename(uuid.uuid4().hex[:6])
    filename = sanitize_filename(file.filename)
    
    save_dir = STORAGE_DIR / rand1 / rand2
    save_dir.mkdir(parents=True, exist_ok=True)
    
    img_path = save_dir / filename
    thumb_path = save_dir / f"thumb_{filename}"
    
    with img_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Generate thumbnail
    with Image.open(img_path) as img:
        img.thumbnail((200, 200))
        img.save(thumb_path)
    
    return {"url": f"/images/{rand1}/{rand2}/{filename}"}

# Get image
@app.get("/images/{rand1}/{rand2}/{filename}")
def get_image(rand1: str, rand2: str, filename: str, thumb: bool = Query(False)):
    rand1, rand2, filename = sanitize_filename(rand1), sanitize_filename(rand2), sanitize_filename(filename)
    
    file_path = STORAGE_DIR / rand1 / rand2 / filename
    thumb_path = STORAGE_DIR / rand1 / rand2 / f"thumb_{filename}"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(thumb_path if thumb else file_path)

# Delete image
@app.delete("/delete/{rand1}/{rand2}/{filename}")
def delete_image(rand1: str, rand2: str, filename: str, secret: str = Header(None), host: str = Header(None)):
    if secret != SECRET_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    if ALLOWED_HOSTS and host not in ALLOWED_HOSTS:
        raise HTTPException(status_code=403, detail="Host not allowed")
    
    rand1, rand2, filename = sanitize_filename(rand1), sanitize_filename(rand2), sanitize_filename(filename)
    
    file_path = STORAGE_DIR / rand1 / rand2 / filename
    thumb_path = STORAGE_DIR / rand1 / rand2 / f"thumb_{filename}"
    
    if file_path.exists():
        file_path.unlink()
        if thumb_path.exists():
            thumb_path.unlink()
        return {"detail": "Image deleted"}
    
    raise HTTPException(status_code=404, detail="Image not found")
