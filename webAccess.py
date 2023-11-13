from fastapi import FastAPI, Request
from fastapi.params import Query
from fastapi.templating import Jinja2Templates
import uvicorn
import mysql.connector
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Ustawienia połączenia z MariaDB
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),
    "database": os.getenv("DB_NAME", "schema_name")
}

async def fetch_rows(limit=1000):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    if limit == 0:
        cursor.execute("SELECT * FROM data ORDER BY id DESC")
    else:
        cursor.execute("SELECT * FROM data ORDER BY id DESC LIMIT %s", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

@app.get("/stats")
async def stats(request: Request, limit: int = Query(1000, alias="limit")):
    rows = await fetch_rows(limit)
    return templates.TemplateResponse("stats.html", {"request": request, "rows": rows})

@app.get("/popo")
async def stats(request: Request):
    rows = await fetch_rows()
    return templates.TemplateResponse("popo.html", {"request": request, "rows": rows})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
