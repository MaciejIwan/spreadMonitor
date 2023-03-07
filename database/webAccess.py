from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/stats")
async def stats(request: Request):
    conn = sqlite3.connect("mydatabase.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mytable ORDER BY id DESC")
    rows = cursor.fetchall()
    return templates.TemplateResponse("stats.html", {"request": request, "rows": rows})

print("elo")