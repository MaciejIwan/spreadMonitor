from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import sqlite3
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/stats")
async def stats(request: Request):
    conn = sqlite3.connect("resources/my_database.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data ORDER BY id")
    rows = cursor.fetchall()

    for row in rows:
        print(row['id'], row['ts'], row['binance_best_bid'], row['binance_best_ask'], row['okx_best_bid'],
              row['okx_best_ask'], row['bid_diff'], row['ask_diff'])
    return templates.TemplateResponse("stats.html", {"request": request, "rows": rows})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
