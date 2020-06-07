from selenium import webdriver
import time

class SubtitleBot():
    def __init__(self):
        self.driver = webdriver.Chrome()


    def selectFirstMovieOption(self):
        try:
            first_movie_option = self.driver.find_element_by_xpath('/html/body/div[1]/table/tbody/tr[2]')
            first_movie_option.click()
            time.sleep(3)
        except:
            print("This is already the first option")

    def findExactMovieOption(self, movieName):
        table =  self.driver.find_element_by_id('search_results')
        for row in table.find_elements_by_css_selector('tr'):
            for cell in row.find_elements_by_tag_name('td'):
                generated_title = str(cell.text)
                title = generated_title[0:len(movieName) + 1]
                try:
                    if title[len(movieName)] == '(':
                        return cell
                except Exception:
                    return False
                
    def searchForMovie(self, movieName):
        print("Searching for: " + movieName)
        self.driver.get("https://www.opensubtitles.org/en/search/subs")
        input_field = self.driver.find_element_by_xpath('//*[@id="search_text"]')
        input_field.send_keys(movieName)
        time.sleep(3)
        correct_xpath_value = self.findExactMovieOption(movieName)
        try:
            correct_xpath_value.click()
        except Exception: 
            self.selectFirstMovieOption()
        time.sleep(3)
        
    def changeLanguage(self):
        try: 
            language_tab_selector = self.driver.find_element_by_xpath('/html/body/div[1]/form/table/tbody/tr[1]/th[2]')
            language_tab_selector.click()
            time.sleep(3)
            english_selector = self.driver.find_element_by_xpath('//*[@id="wl_en"]')
            english_selector.click()
            print("Selected English")
            try:
                language_confirm = self.driver.find_element_by_class_name("ui-button-text-only")
                language_confirm.click()
                time.sleep(7)
                return True
            except Exception:
                return False
        except:
            return False
        time.sleep(7)

    def selectSubtitle(self):
        try:
            movie_title = self.driver.find_element_by_xpath('/html/body/div[1]/form/table/tbody/tr[2]/td[1]/strong/a')
            movie_title.click()
            time.sleep(3)
        except Exception:
            self.selectSubtitle()

    def downloadSelectedSubtitle(self, movieName):
        try:
            download_button = self.driver.find_element_by_xpath('/html/body/div[1]/div[11]/div/div[4]/fieldset/div[1]/h3/div[2]/a')
            download_button.click()
            print("Downloading " + movieName)
            time.sleep(15)
            print("Done Downloading " + movieName)
            return True
        except Exception:
            return False


