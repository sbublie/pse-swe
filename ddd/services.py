import model
from model import OrderLine
from repository import AbstractRepository

class InvalidSku(Exception):
    pass

def is_valid_sku(sku, batches):
    return sku in {b.stock_keeping_unit for b in batches}

def allocate(line: OrderLine, repo: AbstractRepository, session=None) -> str:
    batches = repo.list()
    if not is_valid_sku(line.stock_keeping_unit, batches):
        raise InvalidSku(f"Invalid sku {line.stock_keeping_unit}")
    batchref = model.allocate(line, batches)

    if session is not None:
        session.commit()
    return batchref