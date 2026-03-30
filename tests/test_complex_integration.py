import pytest

from src.manager import Manager
from src.models import Parameters
from src.models import Bill


def test_apartment_costs_with_optional_parameters():
    manager = Manager(Parameters())
    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2025-03-15',
        settlement_year=2025,
        settlement_month=2,
        amount_pln=1250.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-03-15',
        settlement_year=2024,
        settlement_month=2,
        amount_pln=1150.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-02-02',
        settlement_year=2024,
        settlement_month=1,
        amount_pln=222.0,
        type='electricity'
    ))

    costs = manager.get_apartment_costs('apartment-1', 2024, 1)
    assert costs is None

    costs = manager.get_apartment_costs('apart-polanka', 2024, 3)
    assert costs == 0.0

    costs = manager.get_apartment_costs('apart-polanka', 2024, 1)
    assert costs == 222.0

    costs = manager.get_apartment_costs('apart-polanka', 2025, 1)
    assert costs == 910.0
    
    costs = manager.get_apartment_costs('apart-polanka', 2024)
    assert costs == 1372.0

    costs = manager.get_apartment_costs('apart-polanka')
    assert costs == 3532.0
from src.models import Apartment
from src.manager import Manager
from src.models import Parameters


def test_sumowanie_rachunkow():
    parameters = Parameters()
    manager = Manager(parameters)
    assert manager.get_apartment_costs('apart-polanka', 2024, 3) == 0.0
    assert manager.get_apartment_costs('apart-polanka', 2025, 1) == 760.00+150.00
    assert manager.get_apartment_costs('apart-polanka67', 2024, 5) == None 
    assert manager.get_apartment_costs('apart-polanka', 2025, 13) == 0.0 


def test_rozliczenie_dla_mieszkan():
    manager = Manager(Parameters())

    z_rachunkami = manager.rozliczenie_dla_mieszkan('apart-polanka', 2025, 1)
    assert z_rachunkami != None
    assert z_rachunkami.apartment == 'apart-polanka'
    assert z_rachunkami.year == 2025
    assert z_rachunkami.month == 1
    assert z_rachunkami.total_bills_pln == 760.00 + 150

    bez_rachunkow = manager.rozliczenie_dla_mieszkan('apart-polanka', 2026, 3)
    assert bez_rachunkow != None
    assert bez_rachunkow.apartment == 'apart-polanka'
    assert bez_rachunkow.year == 2026
    assert bez_rachunkow.month == 3
    assert bez_rachunkow.total_bills_pln == 0.0

def test_rozliczenia_dla_mieszkancow():
    manager = Manager(Parameters())
    apartment_settlement = manager.rozliczenie_dla_mieszkan('apart-polanka', 2025, 1)

    settlements_many = manager.rozliczenia_dla_mieszkancow(apartment_settlement)
    assert isinstance(settlements_many, list)
    assert len(settlements_many) == 3

    expected_share_many = 910.0 / 3.0
    tenant_ids = [settlement.tenant for settlement in settlements_many]
    assert 'tenant-1' in tenant_ids
    assert 'tenant-2' in tenant_ids
    assert 'tenant-3' in tenant_ids

    for settlement in settlements_many:
        assert settlement.apartment_settlement == 'apart-polanka'
        assert settlement.year == 2025
        assert settlement.month == 1
        assert settlement.rent_pln == 0.0
        assert settlement.bills_pln == pytest.approx(expected_share_many)
        assert settlement.total_due_pln == pytest.approx(expected_share_many)
        assert settlement.balance_pln == pytest.approx(-expected_share_many)

    manager.tenants = {'tenant-1': manager.tenants['tenant-1']}
    settlement_pierwszy = manager.rozliczenia_dla_mieszkancow(apartment_settlement)
    assert isinstance(settlement_pierwszy, list)
    assert len(settlement_pierwszy) == 1
    assert settlement_pierwszy[0].tenant == 'tenant-1'
    assert settlement_pierwszy[0].bills_pln == 910.0
    assert settlement_pierwszy[0].total_due_pln == 910.0
    assert settlement_pierwszy[0].balance_pln == -910.0

    manager.tenants = {}
    settlements_none = manager.rozliczenia_dla_mieszkancow(apartment_settlement)
    assert isinstance(settlements_none, list)
    assert len(settlements_none) == 0