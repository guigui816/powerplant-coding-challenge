# ruff: noqa
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_production_plan_zero_wind():
    payload = {
     "load": 80,
        "fuels": {
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20,
            "wind(%)": 0,
        },
        "powerplants": [
            {
                "name": "gasfiredbig1",
                "type": "gasfired",
                "efficiency": 1,
                "pmin": 0,
                "pmax": 120,
            },
            {
                "name": "windpark1",
                "type": "windturbine",
                "efficiency": 1,
                "pmin": 0,
                "pmax": 150,
            },
        ],
    }
    response = client.post("/productionplan", json=payload)
    assert response.status_code == 200
    data = response.json()

    wind_plant = None
    for plant in data:
        if plant["name"] == "windpark1":
            wind_plant = plant
            break
    assert wind_plant is not None
    assert wind_plant["p"] == 0.0

    wind_plant = None
    for plant in data:
        if plant["name"] == "gasfiredbig1":
            wind_plant = plant
            break
    assert wind_plant is not None
    assert wind_plant["p"] == 80.0


def test_production_plan_load_unmet():
    payload = {
        "load": 999,
        "fuels": {
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20,
            "wind(%)": 60,
        },
        "powerplants": [
            {
                "name": "gasfiredbig1",
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 50,
                "pmax": 100,
            },
            {
                "name": "windpark1",
                "type": "windturbine",
                "efficiency": 1,
                "pmin": 0,
                "pmax": 150,
            },
        ],
    }
    response = client.post("/productionplan", json=payload)
    assert response.status_code == 400

def test_production_plan_valid_request():
    payload = {
        "load": 480,
        "fuels": {
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20,
            "wind(%)": 60,
        },
        "powerplants": [
            {
                "name": "gasfiredbig1",
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460,
            },
            {
                "name": "windpark1",
                "type": "windturbine",
                "efficiency": 1,
                "pmin": 0,
                "pmax": 150,
            },
        ],
    }

    response = client.post("/productionplan", json=payload)
    assert response.status_code == 200
    data = response.json()

    wind_plant = None
    gas_plant = None

    for plant in data:
        if plant["name"] == "windpark1":
            wind_plant = plant
        elif plant["name"] == "gasfiredbig1":
            gas_plant = plant

    assert wind_plant is not None
    assert gas_plant is not None

    expected_wind_power = round(150 * 0.6, 1)
    expected_gas_power = round(480 - expected_wind_power, 1)

    assert wind_plant["p"] == expected_wind_power
    assert gas_plant["p"] == expected_gas_power

def test_production_plan_zero_load():
    payload = {
        "load": 0,
        "fuels": {
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20,
            "wind(%)": 60,
        },
        "powerplants": [
            {
                "name": "gasfiredbig1",
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460,
            },
        ],
    }

    response = client.post("/productionplan", json=payload)
    assert response.status_code == 200
    data = response.json()
    for plant in data:
        assert plant["p"] == 0.0
