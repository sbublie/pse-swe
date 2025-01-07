import unittest

import test_model
import test_orm

def suite():
    suite = unittest.TestSuite()
    suite.addTest(test_model.TestBatchMethods())
    suite.addTest(test_orm.TestConnection())
    suite.addTest(test_orm.TestSession())
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
