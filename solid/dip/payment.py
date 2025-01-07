"""
To apply we do authentication in front for payment processing.

Give the responsibility to authenticate some Authenticator

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

class Authenticator(ABC):

    @abstractmethod
    def is_authenticated(self):
        ...


class SMSAuthenticator(Authenticator):
    
    def __init__(self):
        self.authenticated = False

    def verify_code_with_sms(self, sms: str) -> str:
        security_code = str(uuid4())
        print(f"Sent code {security_code} to sms {sms} for verification")
        self.authenticated = True
        return security_code

    def is_authenticated(self):
        return self.authenticated

class EMailAuthenticator(Authenticator):
    
    def __init__(self):
        self.authenticated = False

    def verify_code_with_email(self, email: str) -> str:
        security_code = str(uuid4())
        print(f"Sent code {security_code} to email {email} for verification")
        self.authenticated = True
        return security_code

    def is_authenticated(self):
        return self.authenticated

class NotARobotAuthenticator(Authenticator):
    def __init__(self):
        self.authenticated = False

    def ask(self):
        print("Are you a robot?!!! [┐∵]┘")
        self.authenticated = True

    def is_authenticated(self):
        return self.authenticated



class CreditCardPaymentProcessor(PaymentServiceInterface):

    def __init__(self, authenticator: Authenticator):
        self.authenticator = authenticator

    def _pay(self, order: Order) -> None:
        print("Processing credit card payment")
        if self.authenticator.is_authenticated():  
            order.status = OrderStatus.ORDER_CLOSED
        else:
            raise Exception(f"Payment was not authenticated")

class DebitCardPaymentProcessor(PaymentServiceInterface):
    
    def __init__(self, authenticator: Authenticator):
        self.authenticator = authenticator

    def _pay(self, order: Order) -> None:
        print("Processing debit card payment")
        if self.authenticator.is_authenticated():  
            order.status = OrderStatus.ORDER_CLOSED
        else:
            raise Exception(f"Payment was not authenticated")

class PaypalPaymentProcessor(PaymentServiceInterface):

    def __init__(self, authenticator: Authenticator):
        self.authenticator = authenticator

    def _pay(self, order: Order) -> None:
        print("Processing paypal payment")
        if self.authenticator.is_authenticated():  
            order.status = OrderStatus.ORDER_CLOSED
        else:
            raise Exception(f"Payment was not authenticated")
