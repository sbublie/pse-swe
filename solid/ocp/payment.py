from abc import ABC, abstractmethod
from order import Order

class PaymentService:

    def pay(self, order: Order, payment_type: str, security_code) -> float:
        
        to_pay = order.total_price()
        print(f"Processing {payment_type} payment type")
        if payment_type == "debit":
            print(f"Verifying security code: {security_code}")
            order.status = "paid"
        elif payment_type == "credit":
            print(f"Verifying security code: {security_code}")
            order.status = "paid"
        else:
            raise Exception(f"Unknown payment type: {payment_type}")
        print(f"Payment of {to_pay} was successful")
        return to_pay


class PaymentServiceInterface(ABC):
    
    @abstractmethod
    def pay(self, order: Order, security_code: str) -> float:
        ...

class CreditCardPaymentProcessor(PaymentServiceInterface):
    def pay(self, order: Order, security_code: str) -> float:
        to_pay = order.total_price()     
        print("Processing credit card payment")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"
        print(f"Payment of {to_pay} was successful")
        return to_pay

class DebitCardPaymentProcessor(PaymentServiceInterface):
    def pay(self, order: Order, security_code: str) -> float:
        to_pay = order.total_price()     
        print("Processing debit card payment")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"
        print(f"Payment of {to_pay} was successful")
        return to_pay

class PaypalPaymentProcessor(PaymentServiceInterface):
    def pay(self, order: Order, security_code: str) -> float:
        to_pay = order.total_price()     
        print("Processing paypal payment")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"
        print(f"Payment of {to_pay} was successful")
        return to_pay
