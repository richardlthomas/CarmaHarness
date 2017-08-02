"""
Created on May 10, 2017
@author: richard.thomas
"""

import os
import unittest
import time
from selenium import webdriver
from mg_Carma.pages.page_CarmaLogin import CarmaPage
from mg_Carma.base.Common import Methods
from mg_Carma.pages.EditCarrierTabs.tab_Authority import AuthorityTab
from mg_Carma.pages.page_CarrierList import CarrierList
from mg_Carma.pages.page_EditCarrier import EditCarrier
from mg_Carma.pages.page_EditEnterprise import EditEnterprise
from mg_Carma.pages.page_EditPropertySet import EditPropertySet
from mg_Carma.pages.page_EnterpriseList import EnterpriseList
from mg_Carma.pages.EditCarrierTabs.tab_FleetEquipment import FleetEquipment
from mg_Carma.pages.page_OnlineImport import OnlineImport
from mg_Carma.tests.CarmaLoader.loader_test_harness import LoaderTestHarness


class TestLoaderHarness(unittest.TestCase):

    harness = []
    home = []
    common = []
    authority = []
    fleet = []
    carrier_list = []
    edit_carrier = []
    edit_enterprise = []
    enterprise_list = []
    edit_property_set = []
    online_import = []
    cases = []

    def setUp(self):
        # desired_cap = {'browser': 'Chrome', 'browser_version': '58.0', 'os': 'Windows', 'os_version': '7',
        #                'resolution': '1920x1200',
        #                'build': 'Carma - tc03FleetEquipment ' + Methods.todayFormatted + ' ' + Methods.current_time}
        # self.driver = webdriver.Remote(
        #     command_executor='http://mercurygateqa1:Qt5NVisBAZ8Hysdjyypc@hub.browserstack.com:80/wd/hub',
        #     desired_capabilities=desired_cap)
        self.driver = webdriver.Chrome()
        self.verification_errors = []
        self.accept_next_alert = True
        # self.driver.set_window_position(0, 23)
        # self.driver.set_window_size(1900, 1000)
        self.driver.maximize_window()
        self.harness = LoaderTestHarness("./Carma_test_data_demo.xlsx")
        self.home = CarmaPage(self.driver)
        self.common = Methods(self.driver)
        self.authority = AuthorityTab(self.driver)
        self.fleet = FleetEquipment(self.driver)
        self.carrier_list = CarrierList(self.driver)
        self.edit_carrier = EditCarrier(self.driver)
        self.edit_enterprise = EditEnterprise(self.driver)
        self.enterprise_list = EnterpriseList(self.driver)
        self.edit_property_set = EditPropertySet(self.driver)
        self.online_import = OnlineImport(self.driver)
        self.cases = self.harness.load_test_data()

    def test_loader_positive(self):
        for test_case in self.cases:
            prop_set_name = "IM:MasterCarrierLoader" + str(test_case.number)
            self.home.login(self.home.ra_base_url)
            time.sleep(2)
            self.common.change_Enterprise("Regression Testing", "Loader Automation")
            time.sleep(2)
            self.common.goto_PowerButton_Menu("Enterprises", "List")
            self.enterprise_list.edit_enterprise("Loader Automation")
            time.sleep(2)
            self.edit_enterprise.add_property_set(prop_set_name, self.harness.base_properties() + test_case.properties)
            self.common.goto_PowerButton_Menu("Administration", "Online Import")
            self.online_import.set_property_set(prop_set_name)
            time.sleep(2)
            self.online_import.set_file(os.path.abspath(test_case.xml_path))
            time.sleep(2)
            self.online_import.save()
            time.sleep(5)
            self.online_import.finish_import()
            time.sleep(3)
            self.home.login(self.home.ra_base_url)
            time.sleep(2)
            self.common.change_Enterprise("Regression Testing", "Loader Automation")
            time.sleep(2)
            for section in test_case.sections:
                if section == "Carrier":
                    self.carrier_list.gotoEditCarrier("Master Automate")
                    time.sleep(2)
                    for current_property in test_case.properties:
                        self.edit_carrier.goto_tab(current_property.tab)
                        time.sleep(1)
                        self.verify_tab_is_empty("Master Automate")
                        time.sleep(1)
                    self.common.close_portlet("Carrier: Master Automate")
                else:
                    self.common.goto_PowerButton_Menu("Carriers", section)
                    time.sleep(2)
            self.carrier_list.deleteCarriers("Master Automate")
            self.home.login(self.home.ra_base_url)
            time.sleep(2)
            self.common.change_Enterprise("Regression Testing", "Loader Automation")
            time.sleep(2)
            self.common.goto_PowerButton_Menu("Enterprises", "List")
            self.enterprise_list.edit_enterprise("Loader Automation")
            time.sleep(2)
            self.edit_enterprise.delete_property_set(prop_set_name)

    def test_loader_negative(self):
        for test_case in self.cases:
            prop_set_name = "IM:MasterCarrierLoader" + str(test_case.number)
            self.home.login(self.home.ra_base_url)
            time.sleep(2)
            self.common.change_Enterprise("Regression Testing", "Loader Automation")
            time.sleep(2)
            self.common.goto_PowerButton_Menu("Enterprises", "List")
            self.enterprise_list.edit_enterprise("Loader Automation")
            time.sleep(2)
            self.edit_enterprise.add_property_set(prop_set_name, self.harness.base_properties() + test_case.properties)
            time.sleep(2)
            self.edit_enterprise.view_property_set(prop_set_name)
            time.sleep(2)
            self.edit_property_set.delete_first_property()
            self.home.login(self.home.ra_base_url)
            time.sleep(2)
            self.common.change_Enterprise("Regression Testing", "Loader Automation")
            time.sleep(2)
            self.common.goto_PowerButton_Menu("Administration", "Online Import")
            self.online_import.set_property_set(prop_set_name)
            time.sleep(2)
            self.online_import.set_file(os.path.abspath(test_case.xml_path))
            time.sleep(2)
            self.online_import.save()
            time.sleep(5)
            self.online_import.finish_import()
            time.sleep(2)
            self.home.login(self.home.ra_base_url)
            time.sleep(2)
            self.common.change_Enterprise("Regression Testing", "Loader Automation")
            time.sleep(2)
            for section in test_case.sections:
                if section == "Carrier":
                    self.carrier_list.gotoEditCarrier("Master Automate")
                    time.sleep(2)
                    for current_property in test_case.properties:
                        self.edit_carrier.goto_tab(current_property.tab)
                        time.sleep(1)
                        self.verify_tab_is_empty("Master Automate")
                        time.sleep(1)
                    self.common.close_portlet("Carrier: Master Automate")
                else:
                    self.common.goto_PowerButton_Menu("Carriers", section)
            self.carrier_list.deleteCarriers("Master Automate")
            self.home.login(self.home.ra_base_url)
            time.sleep(2)
            self.common.change_Enterprise("Regression Testing", "Loader Automation")
            time.sleep(2)
            self.common.goto_PowerButton_Menu("Enterprises", "List")
            self.enterprise_list.edit_enterprise("Loader Automation")
            time.sleep(2)
            self.edit_enterprise.delete_property_set(prop_set_name)

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verification_errors)

    def verify_tab_is_empty(self, carrier_name):
        first_field = self.driver.find_element_by_xpath("//div[contains(., 'Carrier: " + carrier_name
                                                        + "') and contains(@class, 'x-window-default')]//input").text
        assert first_field == ""

if __name__ == "__main__":
    unittest.main()
