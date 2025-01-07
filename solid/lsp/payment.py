from abc import ABC, abstractmethod
from order import Order

class PaymentServiceInterface(ABC):
    
    def pay(self, order: Order) -> float:
        to_pay = order.total_price()
        if order.status == "paid":
            raise Exception(f"Order has already status: {order.status}")
        else:
            self._pay(order=order)
            print(f"Payment of {to_pay} was successful")
            return to_pay
    
    @abstractmethod
    def _pay(self, order: Order) -> None:
        ...

class CreditCardPaymentProcessor(PaymentServiceInterface):

    def __init__(self, security_code: str):
        self.security_code = security_code

    def _pay(self, order: Order) -> None:        
        print("Processing credit card payment")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"


class DebitCardPaymentProcessor(PaymentServiceInterface):
    
    def __init__(self, security_code: str):
        self.security_code = security_code
    
    def _pay(self, order: Order) -> None:    
        print("Processing debit card payment")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"


class PaypalPaymentProcessor(PaymentServiceInterface):

    def __init__(self, email_address: str):
        self.email_address = email_address

    def _pay(self, order: Order) -> None:  
        print("Processing paypal payment")
        print(f"Verifying security code: {self.email_address}")
        order.status = "paid"

