# this class is responsible for reporting deals that appear after filtration
from selenium.webdriver.remote.webdriver import WebDriver

class BookingReport:
    def __init__(self, boxes_section_element:WebDriver):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()


    def pull_deal_boxes(self):  # all child search list places
        return self.boxes_section_element.find_elements_by_class_name("sr_property_block")
        # if we have many values under one key with spaces we can pick either one, all are same!

    def pull_hotel_info(self):
        details = []
        for deal_box in self.deal_boxes:  # gets each hotel name   gets text
            hotel_name = deal_box.find_element_by_class_name(
                "sr-hotel__name").get_attribute('innerHTML').strip()
            hotel_price = deal_box.find_element_by_class_name(
                "prco-valign-middle-helper"
            ).get_attribute('innerHTML').strip() # to remove any outside white spaces
            hotel_ratings = deal_box.get_attribute('data-score').strip()

            details.append([hotel_name, hotel_price, hotel_ratings])
            # now its more organised and can also be stored in database easily
        return details