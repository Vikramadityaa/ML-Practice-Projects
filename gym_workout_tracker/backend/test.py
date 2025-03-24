from fastapi import FastAPI
import db_fetcher

def get_workout(workout_name: str):
    data = db_fetcher.fetch_workout_info_from_db(workout_name)
    # if data is None:
    #     raise HTTPException(status_code=500, detail="Failed to retrieve workout data from the database.")
    workout = {}

    # workout = {
    #     row["workout_date"]: Workout(
    #         workout_name=workout_name,
    #         max_weight=row["max_weight"],
    #         repetitions=row["repetitions"]
    #     )
    #     for row in data
    # }
    print(data)
    return data

if __name__ == '__main__':
    get_workout('Curl')