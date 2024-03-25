from selenium.webdriver.common.by import By
from re import search
from time import sleep

def click_function(driver, target, SELECTOR):
    sleep(0.2)
    click_element = target.find_element(By.XPATH, './/*[text()="' + SELECTOR + '"]')
    driver.execute_script("arguments[0].scrollIntoView();", click_element)
    click_element.click()
    sleep(0.6)

def run(id, driver):
    url = f'https://ja.aliexpress.com/store/{id}/pages/all-items.html?sortType=bestmatch_sort&shop_sortType=bestmatch_sort'
    
    try:
        driver.get(url)

        sleep(20)
        page = driver.find_element(By.CSS_SELECTOR, '[totalpage]')
        total_pages = int(page.get_attribute('totalpage'))
        print(f"Total pages: {total_pages} {page.get_attribute('totalpage')}")
        ids = []
        for i in range(total_pages):
            try:
                click_function(driver, page, f'{i+1}')

                disabled_elements = driver.find_elements(By.CSS_SELECTOR, '[ae_object_value]')

                for element in disabled_elements:
                    try: 
                        href = element.get_attribute('href')  # Get the href attribute from the WebElement
                        if href is not None:
                            id_match = search(r'item/(\d+)\.html', href)
                            if id_match:
                                id = id_match.group(1)
                                ids.append(id)
                    except Exception as e:
                        print("Error: ", e)
                        continue
            except Exception as e:
                print("Click Error: ", e)
                continue
        print(ids)

    except Exception as e:
        print("Error: ", e)
        return "error"
    return ids

def main(id, driver):
    return run(id, driver)