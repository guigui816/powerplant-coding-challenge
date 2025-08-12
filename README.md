# powerplant-coding-challenge

This project implements an API to calculate the optimal power production plan to meet a given electrical load at the 
lowest possible cost.  
It uses **FastAPI** for the API layer and includes unit tests with **pytest**.

## Tech Stack  

- **Python 3.11**  
- **FastAPI** – API framework  
- **Uvicorn** – Server  
- **Pydantic** – Data validation  
- **pytest** – Testing framework  
- **ruff** – Linter + formatter  

## Launch Guide

### Create a virtual environment
```commandline
python -m venv venv
.\venv\Scripts\Activate.ps1
```


## Installation and usage with Make

### Install dependencies
```commandline
make install
```
### Running the application
```commandline
make run
```
The API will be available at: http://127.0.0.1:8888

The Swagger documentation is available at: http://127.0.0.1:8888/docs

### Testing the application
The application is coming with basic tests to check several cases.
You can run all the tests with the following command:
```commandline
make tests
```


## Installation and usage without Make
### Install dependencies
```commandline
pip install -r requirements.txt
```
### Running the application

You can start the app by calling main without specifying the port
```commandline
python -m app.main
```

Or you can call it and specify the port
```commandline
python -m uvicorn app.main:app --reload --port 8888
```
The API will be available at: http://127.0.0.1:8888

The Swagger documentation is available at: http://127.0.0.1:8888/docs

### Example of request and response for the API endpoint '/productionplan'

Request coming from the provided examples of the challenge "payload3" 
```json
{
  "load": 910,
  "fuels": {
    "gas(euro/MWh)": 13.4,
    "kerosine(euro/MWh)": 50.8,
    "co2(euro/ton)": 20,
    "wind(%)": 60
  },
  "powerplants": [
    { "name": "gasfiredbig1", "type": "gasfired", "efficiency": 0.53, "pmin": 100, "pmax": 460 },
    { "name": "gasfiredbig2", "type": "gasfired", "efficiency": 0.53, "pmin": 100, "pmax": 460 },
    { "name": "gasfiredsomewhatsmaller", "type": "gasfired", "efficiency": 0.37, "pmin": 40, "pmax": 210 },
    { "name": "tj1", "type": "turbojet", "efficiency": 0.3, "pmin": 0, "pmax": 16 },
    { "name": "windpark1", "type": "windturbine", "efficiency": 1, "pmin": 0, "pmax": 150 },
    { "name": "windpark2", "type": "windturbine", "efficiency": 1, "pmin": 0, "pmax": 36 }
  ]
}
```

And the response provided by the application:

```json
[
  { "name": "gasfiredbig1", "p": 460 },
  { "name": "gasfiredbig2", "p": 338.4 },
  { "name": "gasfiredsomewhatsmaller", "p": 0 },
  { "name": "tj1", "p": 0 },
  { "name": "windpark1", "p": 90 },
  { "name": "windpark2", "p": 21.6 }
]
```

### Current limitations of the code

This code was developed with a limited amount of time to complete it.
As a result, it comes naturally with some limitations.

The main limitation in the code is in the production plan algorithm.
While the algorithm is working smoothly, it is not the most optimized approach.
This could be improved for better accuracy and efficiency.

For example, the management of the pmin is handled in a straightforward way.
Currently, if the required power is less than a plant pmin, that plant will still be activated at pmin, possibly leading to overproduction.
#### A potential enhancement would involve:

- First pass: Skip plants where "pmin > remaining load" and store them in a “to optimize” list.
- Second pass, after allocating correct loads: Select the plant from the “to optimize” list that causes the least overproduction, then adjust allocations accordingly.

Another limitation concerns error handling. 
Currently, the API responds with a 400 error if the load cannot be met exactly. 
However, if the algorithm ends up overproducing power, no error is returned. 
This behavior could be improved to better reflect such situations.

## Who am I 

I am Guillaume, a passionate Python software engineer and Scrum Master who loves coding :)
Curious by nature, I enjoy being challenged and learning new things every day.
Outside of work, I’m passionate about Formula 1, gardening, and Legos.

I’m really looking forward to meeting you during the interview, to whoever is reading this!