"""
Now we split the interface into two different ones. One for 
SMS authentication and one for payment processing
"""
from uuid import uuid4
from abc import ABC, abstractmethod
from order import Order, OrderStatus

class PaymentServiceInterface(ABC):
    
    def pay(self, order: Order) -> float:
        to_pay = order.total_price()
        if order.status == OrderStatus.ORDER_CLOSED:
            raise Exception(f"Order has already status: {order.status}")
        else:
            self._pay(order=order)
            print(f"Payment of {to_pay} was successful")
            return to_pay
    
    @abstractmethod
    def _pay(self, order: Order) -> None:
        ...

class PaymentSMSAuthenticatorInterface(ABC):

    @abstractmethod
    def send_security_code(self) -> str:
        ...



class CreditCardPaymentProcessor(PaymentServiceInterface, 
                                 PaymentSMSAuthenticatorInterface):

    def __init__(self, sms: str):
        self.sms = sms
        self.authenticated = False

    def _pay(self, order: Order) -> None:
        print("Processing credit card payment")
        if self.authenticated:  
            order.status = OrderStatus.ORDER_CLOSED
        else:
            raise Exception(f"Payment was not authenticated with security code: {self.authenticated}")

    def send_security_code(self) -> str:
        security_code = str(uuid4())
        # sent security code to client via sms
        print(f"Verifying security code: {security_code} to sms {self.sms}")
        self.authenticated = True
        return security_code

class DebitCardPaymentProcessor(PaymentServiceInterface,
                                PaymentSMSAuthenticatorInterface):
    
    def __init__(self, sms: str):
        self.sms = sms
        self.authenticated = False

    def _pay(self, order: Order) -> None:
        print("Processing debit card payment")
        if self.authenticated:  
            order.status = OrderStatus.ORDER_CLOSED
        else:
            raise Exception(f"Payment was not authenticated with security code: {self.authenticated}")

    def send_security_code(self) -> str:
        security_code = str(uuid4())
        # sent security code to client via sms
        print(f"Verifying security code: {security_code} to sms {self.sms}")
        self.authenticated = True
        return security_code

class PaypalPaymentProcessor(PaymentServiceInterface):

    def __init__(self, email_address: str):
        self.email_address = email_address

    def _pay(self, order: Order) -> None:  
        print("Processing paypal payment")
        print(f"Verifying security code: {self.email_address}")
        order.status = OrderStatus.ORDER_CLOSED
