from selenium import webdriver
import pickle
import time

import sys
# Import the byte stream handler.
from io import BytesIO
# Import urlopen() for either Python 2 or 3.
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


import xlsxwriter




NUM_OF_PAGES_TO_SEARCH = 1
KEYS_LIST = ['IMAGE','NAME','ORDER NO','TRACK NO','POU','DELIVERY']

driver = webdriver.Firefox()
driver.get("https://aliexpress.com")
cookies = pickle.load(open("cookies.pickle", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)

def create_worksheet_columns(size):
    A_CHAR = 65
    list_of_columns = []
    for i in range(size):
        list_of_columns.append(chr(A_CHAR))
        A_CHAR += 1

    return list_of_columns

def write_to_xlsx_file(file_name,list_dict_items):

    list_of_columns = create_worksheet_columns(len(KEYS_LIST))
    row_index = 1

    workbook = xlsxwriter.Workbook(file_name)
    workbook.formats[0].set_font_size(20)
    worksheet = workbook.add_worksheet()

    for col in range(0,100):
        # worksheet.set_column(col, col, 70)
        worksheet.set_column(col,col, 15)
        worksheet.set_row(col, 80) 



    for indx,key in enumerate(KEYS_LIST):
        element_pos = str(list_of_columns[indx])+str(row_index)
        worksheet.write(element_pos, key)

    for dic in list_dict_items:
        row_index += 1

        for indx,key in enumerate(KEYS_LIST):
            value=''
            try:
                value = dic[key]
            except Exception:
                pass
            element_pos = str(list_of_columns[indx])+str(row_index)
            if key == KEYS_LIST[0]:
                # Read an image from a remote url.
                url = value
                image_data = BytesIO(urlopen(url).read())
                # Write the byte stream image to a cell. Note, the filename must be
                # specified. In this case it will be read from url string.
                worksheet.insert_image(element_pos, url, {'image_data': image_data,'x_scale': 1.5, 'y_scale': 1.5,'x_offset': 7, 'y_offset': 7})
            else:
                worksheet.write(element_pos, value)
    workbook.close()


def get_item_details(url):
    driver.get(url)
    item_name_tab            = driver.find_elements_by_css_selector('a.baobei-name')
    item_order_num_tab       = driver.find_elements_by_css_selector('dd.order-no')
    item_tracking_num_tab    = driver.find_elements_by_css_selector('td.no')
    ariel_order_num_tab      = driver.find_elements_by_css_selector('span.i18ncopy')
    item_delivery_status_tab = driver.find_elements_by_css_selector('div.list-box')
    item_image_url           = driver.find_elements_by_css_selector('a.pic')[0].find_elements_by_tag_name('img')[0].get_attribute('src')

    row_dict = dict()
    key_index = 0

    row_dict[KEYS_LIST[key_index]]=item_image_url
    key_index += 1

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
    items_dict_list = []

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
    


    # Get dict representing a single ROW
    for link in links:
        row_dict = get_item_details(link)
        items_dict_list.append(row_dict)

    driver.close()
    return items_dict_list

    # Open CSV file
    # file = open('aliexpress_oreders.csv','w')
    # for col in KEYS_LIST:
    #     file.write(col+',')
    # file.write('\n')
    
    #     for key in KEYS_LIST:
    #         value=''
    #         try:
    #             value = row_dict[key]
    #         except Exception:
    #             pass
    #         file.write(value+',')
    #     file.write('\n')
    
    # file.close() 
    



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
    items_dict_list = get_list_of_item_view_details('https://trade.aliexpress.com/orderList.htm')
    write_to_xlsx_file('aliexpress_oreders.xlsx',items_dict_list)
    #print(create_worksheet_columns(len(KEYS_LIST)))

