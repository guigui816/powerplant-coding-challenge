
from fastapi import HTTPException

from app.models.schemas.schemas import Fuels, PowerPlant, ProductionRequest, ProductionResponse

CO2_PER_MWH = 0.3


def calculate_real_cost(powerplant: PowerPlant, fuels: Fuels) -> float:
    """Calculate the real cost of producing 1 MWh from a given power plant.

    The calculation depends on the type of the power plant:
    - windturbine: cost is always 0.
    - gasfired: includes fuel cost, efficiency of the plant and CO2 cost.
    - turbojet: includes fuel cost and efficiency of the plant.

    Args:
        powerplant (PowerPlant): The power plant specifications.
        fuels (Fuels): Current fuel prices.

    Returns:
        float: The real cost in euro to produce 1 MWh.

    Raises:
        HTTPException: If the power plant type is unknown.

    """
    if powerplant.type == "windturbine":
        return 0.0
    if powerplant.type == "gasfired":
        fuel_cost = fuels.gas_euro_per_mwh / powerplant.efficiency
        co2_cost = CO2_PER_MWH * fuels.co2_euro_per_ton
        return fuel_cost + co2_cost
    if powerplant.type == "turbojet":
        return fuels.kerosine_euro_per_mwh / powerplant.efficiency
    raise HTTPException(status_code=400, detail="Unknown power plant type")


def order_power_plants_by_cost(fuels: Fuels, power_plants_list: list[PowerPlant]) -> list[PowerPlant]:
    """Order a list of power plants by their real production cost.

    Args:
        fuels (Fuels): Current fuel prices.
        power_plants_list (list[PowerPlant]): List of power plants to sort.

    Returns:
        list[PowerPlant]: A sorted list of PowerPlant associated with their real cost.

    """
    unordered_power_plants = []
    for plant in power_plants_list:
        unordered_power_plants.append(
            {"powerplant": plant, "real_cost": calculate_real_cost(plant, fuels)},
        )

    return sorted(unordered_power_plants, key=lambda x: x["real_cost"])


def calculate_unit_commitment(payload: ProductionRequest) -> list[ProductionResponse]:
    """Allocate production to each power plant to meet the requested load at minimal cost.

    Args:
        payload (ProductionRequest): Contains the requested load, power plants and fuel prices.

    Returns:
        list[ProductionResponse]: The list of plants with their assigned production in MWh.

    """
    result = []

    if payload.load == 0:
        for plant in payload.powerplants:
            result.append(ProductionResponse(name=plant.name, p=0.0))
        return result

    fuels = payload.fuels

    ordered_plants = order_power_plants_by_cost(fuels, payload.powerplants)

    allocation_load = allocate_load(fuels, ordered_plants, payload.load)

    for plant in payload.powerplants:
        load = allocation_load.get(plant.name, 0.0)
        rounded_load = round(load, 1)
        result.append(ProductionResponse(name=plant.name, p=rounded_load))

    return result


def allocate_load(fuels: Fuels, ordered_plants: list[PowerPlant], load: float) -> dict[str, float]:
    """Allocate the load among power plants in order of increasing cost.

    Args:
        fuels (Fuels): Fuel prices and wind availability.
        ordered_plants (list[PowerPlant]): Power plants sorted by production cost.
        load (float): Total required load in MWh.

    Returns:
        dict[str, float]: Power plant names with their assigned production in MWh.

    Raises:
        HTTPException: If the available plants cannot meet the required load.

    """
    allocation_load = {}
    remaining_load = load

    for plant_loop in ordered_plants:
        plant = plant_loop["powerplant"]

        if plant.type == "windturbine":
            if fuels.wind_percentage == 0:
                allocation_load[plant.name] = 0.0
                continue

            load_taken = min(plant.pmax * (fuels.wind_percentage / 100), remaining_load)
        else:
            load_taken = min(plant.pmax, remaining_load)
            load_taken = max(load_taken, plant.pmin)

        remaining_load -= load_taken
        allocation_load[plant.name] = load_taken

        if remaining_load <= 0:
            break

    if remaining_load > 0:
        raise HTTPException(status_code=400, detail="Load could not be met with available plants")

    return allocation_load
