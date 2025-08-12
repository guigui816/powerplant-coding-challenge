from fastapi import APIRouter

from app.models.schemas.schemas import ProductionRequest, ProductionResponse
from app.services.production_plan_service import calculate_unit_commitment

router = APIRouter(tags=["productionplan"])


@router.post("/productionplan", response_model=list[ProductionResponse])
def production_plan(request: ProductionRequest) -> list[ProductionResponse]:
    """Generate a production plan for the given power load request.

    This endpoint receives the required load with the list of power plants and fuel costs.
    It calculates and allocate loads among plants based on cost constraints.

    Args:
        request (ProductionRequest): Input payload containing:
            - load: total power demand to be met.
            - fuels: fuel prices and CO2 cost data.
            - powerplants: list of available plants with their capacity and efficiency.

    Returns:
        list[ProductionResponse]: A list where each item contains:
            - name: the power plant name.
            - p: the assigned production in MWh for that plant.

    Raises:
        HTTPException (400): If the required load cannot be met with the power plants given.

    """
    return calculate_unit_commitment(request)
