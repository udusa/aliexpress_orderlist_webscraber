from selenium import webdriver
import pickle
import time

import sys


NUM_OF_PAGES_TO_SEARCH = 3
KEYS_LIST = ['NAME','ORDER NO','TRACK NO','POU','DELIVERY']

driver = webdriver.Firefox()
driver.get("https://aliexpress.com")
cookies = pickle.load(open("cookies.pickle", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)


def get_item_details(url):
    driver.get(url)
    item_name_tab            = driver.find_elements_by_css_selector('a.baobei-name')
    item_order_num_tab       = driver.find_elements_by_css_selector('dd.order-no')
    item_tracking_num_tab    = driver.find_elements_by_css_selector('td.no')
    ariel_order_num_tab      = driver.find_elements_by_css_selector('span.i18ncopy')
    item_delivery_status_tab = driver.find_elements_by_css_selector('div.list-box')

    row_dict = dict()
    key_index = 0

    for name in item_name_tab:
        row_dict[KEYS_LIST[key_index]]=name.text.replace('\n', ':').replace(',', ':')
        key_index += 1
        # print('NAME : ',name.text)
        break

    for order_no in item_order_num_tab:
        row_dict[KEYS_LIST[key_index]]=order_no.text.replace('\n', ':').replace(',', ':')
        key_index += 1
        # print('ORDER NO : ',order_no.text)
        break

    for item_tracking in item_tracking_num_tab:
        row_dict[KEYS_LIST[key_index]]=item_tracking.text.replace('\n', ':').replace(',', ':')
        key_index += 1
        # print('TRACK NO : ',item_tracking.text)
        break

    for ariel_order in ariel_order_num_tab:
        if 'POU' in ariel_order.text and len(ariel_order.text) < 15:
            row_dict[KEYS_LIST[key_index]]=ariel_order.text.replace('\n', ':').replace(',', ':')
            key_index += 1
            # print('ARIEL NO : ',ariel_order.text)
            break

    for indx,item_delivery_status in enumerate(item_delivery_status_tab):
        row_dict[KEYS_LIST[key_index]]=item_delivery_status.text.replace('\n', ':').replace(',', ':')
        key_index += 1
        # print('DELIVERY : ',item_delivery_status.text)
        break

    #print('---------------------------------------------------------')
    return row_dict


def get_list_of_item_view_details(url):
    driver.get(url)
    links = set()

    for i in range(NUM_OF_PAGES_TO_SEARCH):
        view_details = driver.find_elements_by_css_selector('a.view-detail-link')
        # Fill list of links to check
        for indx,view in enumerate(view_details):
            link = view.get_attribute('href')
            links.add(link)
        # Move to next page
        next_tab = driver.find_elements_by_css_selector('a.ui-pagination-next')
        for n in next_tab:
            n.click()
            break
    
    # Open CSV file
    file = open('aliexpress_oreders.csv','w')
    for col in KEYS_LIST:
        file.write(col+',')
    file.write('\n')

    # Get dict representing a single ROW
    for link in links:
        row_dict = get_item_details(link)
        for key in KEYS_LIST:
            value=''
            try:
                value = row_dict[key]
            except Exception:
                pass
            file.write(value+',')
        file.write('\n')
    
    file.close() 
    driver.close()



# def extract_product_urls_from_list_page(list_page_url):
#     driver.get(list_page_url)
#     time.sleep(5)
#     cats = driver.find_elements_by_css_selector('a.baobei-name')

#     all_links = set()
#     for ind, cat in enumerate(cats):
#         print(cat.text)
#         # try:
#         #     cat.click()
#         # except Exception:
#         #     continue
#         # if ind == 0:
#         #     items = driver.find_elements_by_class_name('item-desc')
#         #     links = [item.get_attribute('href') for item in items]
#         # else:
#         #     items = driver.find_elements_by_css_selector('div.title > a')
#         #     links = [item.get_attribute('href') for item in items]
#         # for link in links:
#         #     all_links.add(link)
#         # time.sleep(2)
#     return all_links


if __name__ == '__main__':
    # extract_product_urls_from_list_page('https://trade.aliexpress.com/orderList.htm?')
    get_list_of_item_view_details('https://trade.aliexpress.com/orderList.htm')

