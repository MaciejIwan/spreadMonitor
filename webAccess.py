from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import sqlite3
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

async def fetch_rows():
    conn = sqlite3.connect("resources/my_database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.get("/stats")
async def stats(request: Request):
    rows = await fetch_rows()
    return templates.TemplateResponse("stats.html", {"request": request, "rows": rows})

@app.get("/popo")
async def stats(request: Request):
    rows = await fetch_rows()
    return templates.TemplateResponse("popo.html", {"request": request, "rows": rows})





if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
