from typing import Literal

from pydantic import BaseModel, Field, confloat


class PowerPlant(BaseModel):
    """Represents a power plant and its technical specifications."""

    name: str = Field(..., title="Name of the power plant.")
    type: Literal["gasfired", "turbojet", "windturbine"] = Field(
        ...,
        description="Type of the power plant: 'gasfired' (Gas), "
                    "'turbojet' (Kerosine), "
                    "or 'windturbine' (Wind).",
    )
    efficiency: confloat(gt=0) = Field(..., description="Efficiency of the power plant.")
    pmin: confloat(ge=0) = Field(
        ..., description="Minimum delivered power (MWh) when the plant is operating.",
    )
    pmax: confloat(gt=0) = Field(
        ..., description="Maximum delivered power (MWh) the plant can produce.",
    )


class Fuels(BaseModel):
    """Represents the different fuel prices and wind availability."""

    gas_euro_per_mwh: float = Field(
        ..., alias="gas(euro/MWh)", description="Price of gas in euro per MWh.",
    )
    kerosine_euro_per_mwh: float = Field(
        ..., alias="kerosine(euro/MWh)", description="Price of kerosine in euros per MWh.",
    )
    co2_euro_per_ton: float = Field(
        ..., alias="co2(euro/ton)", description="Price of CO2 emissions in ton.",
    )
    wind_percentage: confloat(ge=0, le=100) = Field(
        ...,
        alias="wind(%)",
        description="Wind availability as a percentage. The price for using wind is 0.",
    )


class ProductionRequest(BaseModel):
    """Represents the request payload sent to the /productionplan endpoint."""

    load: confloat(ge=0) = Field(
        ..., description="Total load demand in MWh to be met by the available power plants.",
    )
    fuels: Fuels = Field(..., description="List of fuel prices and wind availability.")
    powerplants: list[PowerPlant] = Field(
        ..., description="List of available power plants with their technical specifications.",
    )


class ProductionResponse(BaseModel):
    """Represents the response for each power plant in the production plan."""

    name: str = Field(..., alias="name", description="Name of the power plant.")
    p: confloat(ge=0) = Field(
        ..., description="Assigned production load in MWh. Rounded to the nearest 0.1 MWh.",
    )
