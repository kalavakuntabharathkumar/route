import pytest
from app.agent import run_agent
from app.database import seed_shipments

@pytest.fixture(autouse=True)
def setup():
    seed_shipments()

def test_health_style_lookup():
    result = run_agent("What is the status of RT-00001?")
    assert result["results"][0]["result"]["found"] is True

@pytest.mark.parametrize("number", range(1, 26))
def test_tool_scenarios(number):
    result = run_agent(f"Check shipment RT-{number:05d} and delay risk")
    assert len(result["results"]) == 2
    assert all("result" in item for item in result["results"])
