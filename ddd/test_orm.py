import unittest
from datetime import date

import orm
from model import OrderLine, Batch

from sqlalchemy import create_engine, select, insert
from sqlalchemy.sql import text
from sqlalchemy.orm import Session

class TestConnection(unittest.TestCase):

    def setUp(self):
        print("setup database connection")
        engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

        #create tables
        orm.mapper_registry.metadata.create_all(engine)

        self.connection = engine.connect()        
        
    def tearDown(self):
        print("close database connection")
        self.connection.close()
        print("connection closed: ",self.connection.closed)

    def test_simple_insert(self):
        statement = text("""INSERT INTO order_lines (order_id, stock_keeping_unit, quantity) 
                         VALUES("test", "test123", 4)""")
        rs = self.connection.execute(statement)  
        
        statement = text('SELECT * FROM order_lines')
        rs = self.connection.execute(statement)
        row = rs.first()
        order_line = OrderLine(str(row[1]), str(row[2]), int(row[3]) )
        self.assertEqual(OrderLine("test", "test123", 4), order_line)
    
    def test_orderline_insert_lines(self):

        data = ({ "order_id": "order1", "stock_keeping_unit": "RED-CHAIR", "quantity": 12 },
                { "order_id": "order1", "stock_keeping_unit": "RED-TABLE", "quantity": 13 },
                { "order_id": "order1", "stock_keeping_unit": "BLUE-LIPSTICK", "quantity": 14 },
        )

        expected = []
        for line in data:

            statement = "INSERT INTO order_lines (order_id, stock_keeping_unit, quantity) "
            statement += f'VALUES("{line["order_id"]}", "{line["stock_keeping_unit"]}", {line["quantity"]}) '
            print(statement)
            self.connection.execute(text(statement))
            expected.append( OrderLine(line["order_id"], line["stock_keeping_unit"], line["quantity"]) )

        statement = select(OrderLine)
        result = self.connection.execute(statement)
        for ((id, order_id, sku, quantity), order_line) in zip(result, expected):
            self.assertEqual(OrderLine(order_id, sku, quantity), order_line)

    def test_insert(self):
        order_line = OrderLine("test", "test123", 4)
        statement = insert(OrderLine).values(order_id=order_line.order_id, 
                                             stock_keeping_unit=order_line.stock_keeping_unit,
                                             quantity=order_line.quantity)
        self.connection.execute(statement)

    def runTest(self):

        self.test_simple_insert()
        self.setUp()
        self.test_orderline_insert_lines()
        self.setUp()
        self.test_insert()



class TestSession(unittest.TestCase):

    def setUp(self):
        engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
        #create tables
        orm.mapper_registry.metadata.create_all(engine)
        self.session = Session(engine)

    def tearDown(self):
        print("close database session")
        self.session.close()
        print("session closed: ",self.session)

    def test_allocation(self):

        order_line_1 = OrderLine("1", "AAA", 5)
        order_lines = [order_line_1, OrderLine("2", "BBB", 5),  OrderLine("2", "AAA", 10)]
        for order_line in order_lines:
            self.session.add(order_line)
        self.session.commit()

        batch_1 = Batch("4711", "AAA", 100, date(2025,12,31))
        batch_1.allocate(order_line_1)
        batches = [batch_1, Batch("4712", "BBB", 100, date(2025,6,30))]

        for batch in batches:
            self.session.add(batch)
        self.session.commit()

        statement = select(Batch).filter_by(reference="4711")
        batches = self.session.scalars(statement).all()
        self.assertEqual(len(batches), 1) # just one batch with reference == 4711
        batch = batches[0]
        self.assertEqual(batch.available_quantity, 95) # 100 -5

    def runTest(self):
        self.test_allocation()

if __name__ == '__main__':
    unittest.main()