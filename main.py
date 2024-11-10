from fastapi import FastAPI
from contextlib import asynccontextmanager
import csv
import random

with open('./data/gyul.csv', 'w', newline='') as csvfile:
    fieldnames = ['year', 'amounts']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # 헤더 작성
    writer.writeheader()

    # 2010년부터 2023년까지 데이터 생성
    for year in range(2010, 2024):
        # 랜덤한 amounts 생성 (예시: 10000 ~ 50000 사이)
        amounts = random.randint(10000, 50000)
        writer.writerow({'year': year, 'amounts': amounts})
 


def load_data():
    with open("./data/gyul.csv", "r") as f:
        reader = csv.DictReader(f,delimeter=",")
        result = {
            int(row.pop("year")) : row for row in reader
        }
            
        return result
    
gyul_stats = {}

@asynccontextmanager
async def lifespan(app:FastAPI):
    global gyul_stats
    gyul_stats = load_data()

    yield


app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message":"Hello, Jeju!" } 

@app.get("/stats")
async def get_stats():
    return gyul_stats

@app.get("/stats/{year}")
async def get_single_year_stats(year:int):
    return gyul_stats[year]