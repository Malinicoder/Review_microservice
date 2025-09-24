import os
from datetime import timedelta

class Config:
    
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Root@localhost:5432/Review'

    LOG_FILE = os.path.join("logs", "reviews.log") 
