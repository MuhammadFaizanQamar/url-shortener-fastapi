from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import URL
import random
import string

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title='URL Shortener API')

from schemas import URLCreate, URLResponse

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

@app.get('/{short_code}')
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    url = db.query(URL).filter(URL.short_code == short_code).first()
    
    if not url:
        raise HTTPException(status_code=404, detail='URL not found')
    
    url.clicks += 1
    db.commit()
    
    return RedirectResponse(url.original_url)

@app.get('/stats/all', response_model=list[URLResponse])
def get_stats(db: Session = Depends(get_db)):
    urls = db.query(URL).order_by(URL.clicks.desc()).all()
    return urls


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


@app.get('/')
def home():
    return {'message': 'Welcome to URL Shortener API'}
