import logging

import uvicorn
from fastapi import FastAPI

from app.api.routes.production_plan import router

app = FastAPI(
    title="powerplant-coding-challenge",
    description="""
              This API application calculates the optimal power production plan for a given electrical load.
              It take into account the technical specifications of each power plant,
              the cost of the fuels and the CO2 emissions cost.
              The result specifies how much power each plant should produce to meet the demand
              at the lowest possible cost.
              """,
    contact={
        "name": "Guillaume VISSERS",
        "email": "guillaume.vissers@hotmail.com",
    },
)
app.include_router(router)

if __name__ == "__main__":
    logging.info("Starting the power plant API...")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8888, reload=True)
