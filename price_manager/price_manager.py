from fastapi import FastAPI
import httpx
import json
import uvicorn


app=FastAPI()

@app.get("/number")
def get_number():
    exchange_rate=httpx.get(url="https://v6.exchangerate-api.com/v6/181248d440df79055e2999ea/latest/USD")
    exchange_json=json.loads(exchange_rate.text)
    return {"conversion_rate": exchange_json["conversion_rates"]["EUR"]*1.02}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)