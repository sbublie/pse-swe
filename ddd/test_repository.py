import unittest
from datetime import date

import model
import repository
import orm

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

class RepositoryTest(unittest.TestCase):

    def setUp(self):
        engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
        #create tables
        orm.mapper_registry.metadata.create_all(engine)
        self.session = Session(engine)

    def tearDown(self):
        print("close database session")
        self.session.close()
        print("session closed: ",self.session)

    def test_repository_can_save_a_batch(self):

        batch = model.Batch("batch1", "RUSTY-SOAPDISH", 100, eta=None)

        repo = repository.SqlAlchemyRepository(self.session)
        repo.add(batch)
        self.session.commit()

        statement = text('SELECT reference, stock_keeping_unit, _purchased_quantity, eta FROM "batches"')
        rows = self.session.execute(statement)
        self.assertEqual(list(rows), [("batch1", "RUSTY-SOAPDISH", 100, None)])

    def test_repository_list(self):
        repo = repository.SqlAlchemyRepository(self.session)
        repo.add(model.Batch("4711", "AAA", 100, date(2025,12,31)))
        repo.add(model.Batch("4710", "AAA", 100, date(2025,6,30)))
        repo.add(model.Batch("4712", "BBB", 100, date(2025,6,30)))
        batches = repo.list()
        line = model.OrderLine("test123", "AAA", 10)
        batchref = model.allocate(line, batches)
        self.assertEqual(batchref, "4710")


    def runTest(self):
        self.test_repository_can_save_a_batch()
        self.setUp()
        self.test_repository_list()



if __name__ == "__main__":
    unittest.main()
