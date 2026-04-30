from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from insert_state_database import store_sensor_state
from send_notification import process_data

app = FastAPI(title="Sailo Alert Manager")
@app.get("/")
async def root():
    return {"message": "Application is running fine. This is the thing you looking for..."}

@app.post("/collect")
async def collect(request: Request, background_tasks: BackgroundTasks):
    try:
        data = await request.json()
        if "sensor_states" not in data:
            raise HTTPException(status_code=400, detail="Missing Sensor output")
       
        # Run both tasks in background (non-blocking)
        background_tasks.add_task(process_data, data)
        background_tasks.add_task(store_sensor_state,data)

        return {
            "status": "success",
            "message": "Data written to database",
        }
    except Exception as e:
        print(e)