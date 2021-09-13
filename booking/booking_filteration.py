# this file is responsible to interact with deal searching
from selenium.webdriver.remote.webdriver import WebDriver
# importing typing for driver attribute

class BookingFiltration:
    def __init__(self, driver:WebDriver): # now driver know it's type
        self.driver = driver # we are getting chrome driver from booking class

    def apply_star_rating(self, *star_values:int): # use self.driver, *param same as *args
        star_filtration_box = self.driver.find_element_by_id('filter_class') # this is top class
                                # we are grabbing elements! and * gives all child elements of filtration_box
        star_child_elements = star_filtration_box.find_elements_by_css_selector('*')
        # using condition to filter further

        for star_value in star_values: # for multiple clicks
            for start_element in star_child_elements:
                # innerHTML is convention to find values inside HTML tag i.e <a>1 star</a>
                if str(start_element.get_attribute('innerHTML')).strip() == f'{star_value} stars':
                    # strip removes any whitespaces
                    start_element.click() # if any tags has text matches click that

    def sort_data_by_lowest_price(self):
        lowest_price_button = self.driver.find_element_by_css_selector('li[data-id="price"]')
        lowest_price_button.click()

