import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

from XlsxWriter import xlsxwriter


def main(keyword, x_range):
    chrome_driver_filename = 'chromedriver'
    chrome_driver_dir = os.path.expanduser("~") + '/bin/'
    chrome_driver_path = chrome_driver_dir + chrome_driver_filename
    options = Options()
    options.add_argument('--start-maximized')
    capabilities = options.to_capabilities()
    web_driver = webdriver.Chrome(executable_path=chrome_driver_path, desired_capabilities=capabilities)
    web_driver.get("http://haraj.com/")
    search_bar = web_driver.find_element_by_id("searchBoxContent")
    search_bar.find_element_by_tag_name("input").send_keys(keyword)
    search_icon = web_driver.find_element_by_css_selector("#searchBoxContent button.btn-success")
    search_icon.click()
    time.sleep(2)
    try:
        view_more = web_driver.find_element_by_css_selector("div.loadmore a")
        if view_more.is_displayed():
            view_more.click()
            time.sleep(5)
    except:
        pass
    for i in range(10):
        time.sleep(0.5)
        web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    search_results = web_driver.find_elements_by_css_selector("div.adsx div.adx")

    # export csv file to data frame
    post_titles_list = []
    review_list = []
    dates_list = []
    cites_list = []
    urls_list = []
    user_names_list = []
    postive_feedback_links = []
    negativate_feedback_links = []
    phone_numbers_list = []
    for i in range(100):
        try:
            base_window = web_driver.current_window_handle
            post_titles_list.append(search_results[i].find_element_by_css_selector("div.adxInfo").text.split("\n")[0].strip())
            user_names_list.append(search_results[i].find_element_by_css_selector("div.adxInfo").text.split("\n")[-1])
            extra_info_list = search_results[i].find_elements_by_css_selector("div.adxInfo div.adxExtraInfoPart")
            review_value = extra_info_list[0].text
            if review_value == "":
                review_value = 0
            review_list.append(review_value)
            dates_list.append(extra_info_list[1].text)
            cites_list.append(extra_info_list[2].text)
            try:
                url = search_results[i].find_element_by_css_selector("div.adxInfo div.adxTitle a")
                urls_list.append(url.get_attribute("href"))
                web_driver.execute_script('''window.open("","_blank");''')
                web_driver.switch_to.window(web_driver.window_handles[-1])
                web_driver.get(urls_list[i])
                postive_feedback_links.append(len(web_driver.find_elements_by_css_selector("i.fa-thumbs-up")))
                negativate_feedback_links.append(len(web_driver.find_elements_by_css_selector("i.fa-thumbs-down")))
                try:
                    phone_number = web_driver.find_element_by_css_selector("div.contact strong").text
                    if phone_number == "":
                        phone_number = "No phone number provided"
                except:
                    phone_number = "No phone number provided"
                phone_numbers_list.append(phone_number)
                web_driver.close()
                web_driver.switch_to.window(base_window)
            except:
                web_driver.switch_to.window(base_window)
        except:
            print(f'error happened at {i}')
            pass

    workbook = xlsxwriter.Workbook("scrapping_results.xlsx")
    worksheet = workbook.add_worksheet("sheet1")
    worksheet.write('A1', 'Post Title')
    worksheet.write('B1', 'Reviews')
    worksheet.write('C1', 'Dates')
    worksheet.write('D1', 'City')
    worksheet.write('E1', 'Link')
    worksheet.write('F1', 'Positive Feedback')
    worksheet.write('G1', 'Negative Feedback')
    worksheet.write('H1', 'Phone Number')
    worksheet.write('I1', 'User')

    for i in range(1, x_range):
        worksheet.write(i, 0, post_titles_list[i - 1])
        worksheet.write(i, 1, review_list[i - 1])
        worksheet.write(i, 2, dates_list[i - 1])
        worksheet.write(i, 3, cites_list[i - 1])
        worksheet.write(i, 4, urls_list[i - 1])
        worksheet.write(i, 5, postive_feedback_links[i - 1])
        worksheet.write(i, 6, negativate_feedback_links[i - 1])
        worksheet.write(i, 7, phone_numbers_list[i - 1])
        worksheet.write(i, 8, user_names_list[i - 1])
    workbook.close()
    web_driver.close()


if __name__ == "__main__":
    keyword = input("Please enter keyword u want to scrape:\n")
    x_range = input("Please enter the range u need:\n")
    main(keyword=keyword, x_range=int(x_range))
