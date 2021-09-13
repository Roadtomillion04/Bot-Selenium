# here we create class methods
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

import booking.constants as const
from booking.booking_filteration import BookingFiltration
from booking.deal_reporting import BookingReport
from prettytable import PrettyTable # this for storing hotel details in table

class Booking(webdriver.Chrome):                           # to control exit
    def __init__(self, driver_path='./chromedriver.exe', teardown=False): # self refers instance objects
        # these are going to execute first when instanced
        self.driver_path = driver_path
        self.teardown = teardown
        # to ignore devtools warnings
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging']) # removes all warnings
        super(Booking, self).__init__(options=options)
        # super responsible for instantiate the instance of inherited class and as well as this class

        self.implicitly_wait(15) # waits until elements are ready
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def land_first_page(self):
        self.get(const.URL_PATH)

    def change_currnecy(self, currency=None): # refer css selector reference
        currency_element = self.find_element_by_css_selector( # always choose the most unique key value pair!
            'button[data-tooltip-text="Choose your currency"]'
)
        currency_element.click()

        select_currency = self.find_element_by_css_selector( # use *= for an expression that contains substring
            f'a[data-modal-header-async-url-param *= "selected_currency={currency}"]'
        ) # try to always find key-pair like this
        select_currency.click()

    def select_place_to_go(self, place:str):
        search_field = self.find_element_by_css_selector('input[data-sb-id="main"]')
        search_field.clear() # best practices
        search_field.send_keys(place)
        # i=0 clicks on first drop-down
        first_place = self.find_element_by_css_selector('li[data-i="0"]')
        # list tag always has relation like i = 0, 1, 2
        first_place.click()

    def select_dates(self, check_in_date, check_out_date):    # td - table data
        check_in_element = self.find_element_by_css_selector(f'td[data-date="{check_in_date}"]')
        check_in_element.click()

        check_out_element = self.find_element_by_css_selector(f'td[data-date="{check_out_date}"]')
        check_out_element.click()

    def select_adults(self, count:int=1): # id is the strongest element most unique
        selection_element = self.find_element_by_id('xp__guests__toggle')
        selection_element.click()

        while True:
            decrease_button_element = self.find_element_by_css_selector(
                'button[aria-label="Decrease number of Adults"]'
            ) # for plus it has Increase so we can modify easily
            decrease_button_element.click()
            # if value is 1 we have to break the loop

            adult_value_element = self.find_element_by_id('group_adults')
            # to get other attributes in that html tag
            adults_value = adult_value_element.get_attribute(name='value') # key_name and returns value

            if int(adults_value) == 1: # to make it easy to increase count by loop
                break


        increase_button_element = self.find_element_by_css_selector(
            'button[aria-label="Increase number of Adults"]'
        )
        for _ in range(count - 1): # the value starts from 1 and range starts from 0
            increase_button_element.click() # use _name if not using

    def click_search(self):
        submit_button = self.find_element_by_css_selector('button[type="submit"]')
        submit_button.click()


    def apply_filtration(self):
        # we instance another class to make it more easy because this page getting long
        filtration = BookingFiltration(driver=self) # chrome driver
        filtration.apply_star_rating(3, 4, 5)
        filtration.sort_data_by_lowest_price()


    def report_results(self):      # top class
        hotel_boxes = self.find_element_by_id("hotellist_inner")

        report = BookingReport(hotel_boxes) # and list of search result can be modified there for cleaner look
        table = PrettyTable(field_names = ['hotel name', 'hotel price', 'hotel review'])
        table.add_rows(report.pull_hotel_info()) # as we returning list there we can simply call
        print(table)
