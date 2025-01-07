from abc import ABC, abstractmethod
from order import Order

class OldPaymentServiceInterface(ABC):
    
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

    @abstractmethod
    def send_security_code(self, sms: str) -> None:
        ...

class OldCreditCardPaymentProcessor(OldPaymentServiceInterface):

    def __init__(self, security_code: str):
        self.security_code = security_code
        self.authenticated = False

    def _pay(self, order: Order) -> None:
        if self.authenticated:  
            print("Processing credit card payment")
            order.status = "paid"
        else:
            raise Exception(f"Payment was not authenticated with security code: {self.authenticated}")

    def send_security_code(self, sms: str) -> None:
        # sent security code to client via sms
        print(f"Verifying security code: {self.security_code}")
        self.authenticated = True

class OldDebitCardPaymentProcessor(OldPaymentServiceInterface):
    
    def __init__(self, security_code: str):
        self.security_code = security_code
        self.authenticated = False

    def _pay(self, order: Order) -> None:
        if self.authenticated:  
            print("Processing debit card payment")
            order.status = "paid"
        else:
            raise Exception(f"Payment was not authenticated with security code: {self.authenticated}")

    def send_security_code(self, sms: str) -> None:
        # sent security code to client via sms
        print(f"Verifying security code: {self.security_code}")
        self.authenticated = True


class OldPaypalPaymentProcessor(OldPaymentServiceInterface):

    def __init__(self, email_address: str):
        self.email_address = email_address
        self.authenticated = False

    def _pay(self, order: Order) -> None:  
        print("Processing paypal payment")
        print(f"Verifying security code: {self.email_address}")
        order.status = "paid"

    def send_security_code(self, sms: str) -> None:
        raise Exception("Not implemented")