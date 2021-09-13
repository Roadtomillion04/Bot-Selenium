from booking.booking import Booking
from booking.constants import *

# to use context managers
# if we want to exit call Booking(teardown=True)
try:
    with Booking() as bot: # calls __exit__ after indentation
        bot.land_first_page()
        bot.change_currnecy(currency ='USD')
        bot.select_place_to_go(place= PLACE)
        bot.select_dates(check_in_date= CHECK_IN_DATE, check_out_date= CHECK_OUT_DATE)
        bot.select_adults(count=ADULTS_COUNT)
        bot.click_search()
        bot.apply_filtration()
        bot.refresh() # A workaround to let our bot collect data properly or it wont work as it's instantaneous
        bot.report_results()

except Exception as err:
    print('There is something wrong! ;(')
    raise err
