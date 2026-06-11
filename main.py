# 1. All imports first
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import URL
from schemas import URLCreate, URLResponse
import random
import string

# 2. Create app instance
app = FastAPI(title='URL Shortener API')

# 3. Create tables
Base.metadata.create_all(bind=engine)

# 4. Setup templates
templates = Jinja2Templates(directory='templates')

# 5. Helper function
def generate_short_code(length=7):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choices(characters, k=length))

# 6. All routes
@app.get('/', )
def home():
    return {'message': 'Welcome to URL Shortener API'}

@app.get('/ui', include_in_schema=False)
async def frontend(request: Request):
    return templates.TemplateResponse(request=request, name='index.html')

@app.post('/shorten', response_model=URLResponse)
def shorten_url(url_data: URLCreate, db: Session = Depends(get_db)):
    short_code = generate_short_code()
    while db.query(URL).filter(URL.short_code == short_code).first():
        short_code = generate_short_code()
    new_url = URL(
        original_url=url_data.original_url,
        short_code=short_code
    )
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url

@app.get('/stats/all', response_model=list[URLResponse])
def get_stats(db: Session = Depends(get_db)):
    urls = db.query(URL).order_by(URL.clicks.desc()).all()
    return urls

@app.get('/{short_code}')
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == short_code).first()
    if not url:
        raise HTTPException(status_code=404, detail='URL not found')
    url.clicks += 1
    db.commit()
    return RedirectResponse(url.original_url)