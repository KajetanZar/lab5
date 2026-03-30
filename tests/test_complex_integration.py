from src.models import Apartment
from src.manager import Manager
from src.models import Parameters


def test_sumowanie_rachunkow():
    parameters = Parameters()
    manager = Manager(parameters)
    assert manager.get_apartment_costs('apart-polanka', 2024, 3) == 0.0
    assert manager.get_apartment_costs('apart-polanka', 2025, 1) == 760.00+150.00
    assert manager.get_apartment_costs('apart-polanka67', 2024, 5) == None 