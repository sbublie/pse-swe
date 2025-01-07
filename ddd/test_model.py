import unittest
from datetime import date

from model import OrderLine, Batch, allocate, OutOfStock

class TestBatchMethods(unittest.TestCase):

    def test_allocate(self):
        line = OrderLine("1", "SOFA-USA", 10)
        batch = Batch("4711", "SOFA-USA", 25, date(2025,12,31))
        batch.allocate(line)

        self.assertEqual(batch.available_quantity,15)

        line = OrderLine("2", "SOFA-USA", 199)
        possible = True
        try:
            batch.allocate(line)
        except Exception as e:
            possible = False
        
        self.assertEqual(batch.available_quantity,15)

    def test_check_allocation(self):
        line = OrderLine("1", "SOFA-USA", 10)
        batch = Batch("4711", "SOFA-USA", 25, date(2025,12,31))
        possible = batch.check_allocation(line)
        self.assertTrue(possible)

        line = OrderLine("1", "SOFA-USA", 25)
        possible = batch.check_allocation(line)
        self.assertTrue(possible)

        line = OrderLine("1", "SOFA-USA", 26)
        possible = batch.check_allocation(line)
        self.assertFalse(possible)

        line = OrderLine("1", "SOFA-EU", 26)
        possible = batch.check_allocation(line)
        self.assertFalse(possible)              

    def test_allocation_is_idempotent(self):
        line = OrderLine("1", "ANGULAR-DESK", 2)
        batch = Batch("4711", "ANGULAR-DESK", 20, date(2025,12,31))
        try:
            batch.allocate(line)
            batch.allocate(line) # this should raise an exception
        except Exception as e:
            pass
        self.assertEqual(batch.available_quantity, 18)

    def test_allocation_service(self):
        line = OrderLine("1", "ANGULAR-DESK", 2)
        batch_4711 = Batch("4711", "ANGULAR-DESK", 20, date(2025,12,31))
        batch_4712 = Batch("4712", "ANGULAR-DESK", 20, date(2025,12,30))

        batches = [batch_4711, batch_4712]
        ref_id = None
        try:                   
            ref_id = allocate(line, batches)
        except OutOfStock as oos:
            pass
        
        self.assertEqual("4712", ref_id)
        self.assertEqual(batch_4712.available_quantity, 18)

        line = OrderLine("1", "ANGULAR-DESK", 200)
        batch_4711 = Batch("4711", "ANGULAR-DESK", 20, date(2025,12,31))
        batch_4712 = Batch("4712", "ANGULAR-DESK", 20, date(2025,12,30))

        batches = [batch_4711, batch_4712]
        ref_id = None
        try:                   
            ref_id = allocate(line, batches)
        except OutOfStock as oos:
            pass

        self.assertEqual(None, ref_id)
        self.assertEqual(batch_4711.available_quantity, 20)
        self.assertEqual(batch_4712.available_quantity, 20)        

    def runTest(self):
        self.test_allocate()
        self.test_check_allocation()
        self.test_allocation_is_idempotent()
        self.test_allocation_service()


if __name__ == '__main__':
    unittest.main()