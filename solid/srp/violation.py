"""
This code violates the SRP because it is both responsible for managing the
order and the payment. This results in our code being highly coupled and makes
it harder to understand, maintain, and test.
"""

from dataclasses import dataclass, field


@dataclass
class Order:
    items: list[str]=field(default_factory=lambda: [])
    quantities: list[int]=field(default_factory=lambda: [])
    prices: list[float]=field(default_factory=lambda: [])
    status: str="open"

    def total_price(self) -> float:
        total = 0
        for quantity, price in zip(self.quantities, self.prices):
            total += quantity * price
        return total

    def add_item(self, name: str, quantity: int, price: float) -> None:
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def pay(self, payment_type: str, security_code) -> float:
        to_pay = self.total_price()
        print(f"Processing {payment_type} payment type")
        if payment_type == "debit":
            print(f"Verifying security code: {security_code}")
            self.status = "paid"
        elif payment_type == "credit":
            print(f"Verifying security code: {security_code}")
            self.status = "paid"
        else:
            raise Exception(f"Unknown payment type: {payment_type}")
        print(f"Payment of {to_pay} was successful")
        return to_pay


if __name__ == "__main__":

    order = Order()
    order.add_item("Keyboard", 1, 50.0)
    order.add_item("SSD", 1, 150.0)
    order.add_item("USB cable", 2, 5.0)
    
    total_price = order.pay("debit", "0372846")
    

