import doctest
import unittest

from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.layer import onsetup

import infoporto.companyshowcase

OPTION_FLAGS = doctest.NORMALIZE_WHITESPACE | \
               doctest.ELLIPSIS

ptc.setupPloneSite(products=['infoporto.companyshowcase'])


class TestCase(ptc.PloneTestCase):

    class layer(PloneSite):

        @classmethod
        def setUp(cls):
            zcml.load_config('configure.zcml',
              infoporto.companyshowcase)

        @classmethod
        def tearDown(cls):
            pass


def test_suite():
    return unittest.TestSuite([

        # Unit tests
        #doctestunit.DocFileSuite(
        #    'README.txt', package='infoporto.companyshowcase',
        #    setUp=testing.setUp, tearDown=testing.tearDown),

        #doctestunit.DocTestSuite(
        #    module='infoporto.companyshowcase.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        ztc.ZopeDocFileSuite(
            'INTEGRATION.txt',
            package='infoporto.companyshowcase',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),

        # -*- extra stuff goes here -*-

        # Integration tests for CompaniesList
        ztc.ZopeDocFileSuite(
            'CompaniesList.txt',
            package='infoporto.companyshowcase',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for CompanySearch
        ztc.ZopeDocFileSuite(
            'CompanySearch.txt',
            package='infoporto.companyshowcase',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        # Integration tests for company
        ztc.ZopeDocFileSuite(
            'company.txt',
            package='infoporto.companyshowcase',
            optionflags = OPTION_FLAGS,
            test_class=TestCase),


        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
