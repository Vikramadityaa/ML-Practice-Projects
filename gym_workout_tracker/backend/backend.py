from bokeh.core.property.datetime import Datetime
from fastapi import FastAPI, HTTPException
from datetime import date, datetime
import db_fetcher
from typing import List
from pydantic import BaseModel
from typing import Dict

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#In FastAPI, we use Pydantic's BaseModel to define the structure and validation rules for the incoming request data (JSON body) in a POST request.
class Workout(BaseModel):
    workout_name: str
    repetitions: int
    max_weight: float


@app.post('/workout/{workout_date}')
def add_update_workout(workout_date, workout: Workout):
    print(workout)
    workout_date = datetime.strptime(workout_date, "%Y-%m-%d")
    db_fetcher.delete_workout_for_date(workout_date, workout.workout_name)
    db_fetcher.insert_workout_for_date(workout_date, workout.workout_name, workout.repetitions, workout.max_weight)
    return {"message": "Workout updated successfully"}

@app.get('/workout/{workout_name}', response_model=Dict[date, Workout])
def get_workout(workout_name: str):
    data = db_fetcher.fetch_workout_info_from_db(workout_name)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve workout data from the database.")
    workout = {}

    workout = {
        row["workout_date"]: Workout(
            workout_name=workout_name,
            max_weight=row["max_weight"],
            repetitions=row["repetitions"]
        )
        for row in data
    }
    return workout