from dataclasses import dataclass, field
from typing import Optional, Set
from datetime import date

"""
A product is identified by a  SKU (stock keeping unit), 
Customers place orders. 
An order is identified by an order reference and comprises multiple order lines
We need to allocate order lines to batches. When we’ve allocated an order line 
to a batch, we will send stock from that specific batch to the customer’s 
delivery address. 
When we allocate x units of stock to a batch, the available quantity is reduced 
by x.
"""

"""
DDD: Dataclasses are great for Value Objects

Whenever we have a business concept that has data but no identity, 
we often choose to represent it using the Value Object pattern. 

A value object is any domain object that is uniquely identified by the data 
it holds; we usually make them immutable:

One of the nice things that dataclasses (or namedtuples) give us is 
value equality.
"""

#@dataclass(frozen=True) # makes the  class immutable
@dataclass(unsafe_hash=True) # hack for not throwing an error by alchemy
                             # dataclasses.FrozenInstanceError: cannot assign to field '_sa_instance_state'
class OrderLine:
    order_id: str
    stock_keeping_unit: str # name
    quantity: int

@dataclass
class Order:
    order_id: str
    order_lines: list[OrderLine] =  field(default_factory=lambda: [])

class Batch:
    """
    Batch wraps available_quantity of a product identified by its 
    stock_keeping_unit
    """
    def __init__(self, reference: str, 
                 stock_keeping_unit: str, 
                 quantity: int, 
                 eta: Optional[date]):
        self.reference = reference
        self.stock_keeping_unit = stock_keeping_unit
        self.eta = eta
        self._purchased_quantity: int = quantity
        self._allocations: Set[OrderLine] = set()

    def allocate(self, line: OrderLine):
        """decrement available_quantity on allocation"""

        if self.check_allocation(line):
            self._allocations.add(line)
        else:
            raise Exception("Could not allocate oder line to this batch")

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.quantity for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def check_allocation(self, line: OrderLine) -> bool:
        return self.stock_keeping_unit == line.stock_keeping_unit and self.available_quantity >= line.quantity

    # make a list of batches sortable
    def __gt__(self, other):
            if self.eta is None:
                return False
            if other.eta is None:
                return True
            return self.eta > other.eta
    
class OutOfStock(Exception):
    pass

# this is a kind of service. it allocates an order line to the batch
# with the earliest eta in a list of batches
def allocate(line: OrderLine, batches: list[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.check_allocation(line))
        batch.allocate(line)
    except StopIteration:
        raise OutOfStock(f"Out of stock for stock keeping unit {line.stock_keeping_unit}")
    return batch.reference