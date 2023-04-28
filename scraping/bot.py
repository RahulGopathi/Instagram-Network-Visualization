from collections import defaultdict
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

TIMEOUT = 15
MAX_FOLLOWERS_SCRAPE_COUNT = 60

class Bot:
    def setUp(self):
        """Start web driver"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--lang=en")
        chrome_options.add_argument("--log-level=3")
        mobile_emulation = {
            "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

        self.driver = webdriver.Chrome(executable_path=CM().install(), options=chrome_options)

    def tear_down(self):
        """Stop web driver"""
        self.driver.quit()

    def go_to_page(self, url):
        """Find and click top-right button"""
        try:
            self.driver.get(url)
        except NoSuchElementException as ex:
            self.fail(ex.msg)

    def login(self, user_name, pass_word):
        self.driver.get('https://www.instagram.com/accounts/login/')

        time.sleep(1)


        #check if cookies 
        try:
            element = self.driver.find_element(By.XPATH,"/html/body/div[4]/div/div/div[3]/div[2]/button")
            element.click()
            
        except NoSuchElementException:
            print("[Info] - Instagram did not require to accept cookies this time.")


            

        print("[Info] - Logging in...")  

        username = WebDriverWait(
            self.driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[name='username']")))

        # target Password
        password = WebDriverWait(
            self.driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[name='password']")))

        # enter username and password
        username.clear()
        username.send_keys(user_name)
        password.clear()
        password.send_keys(pass_word)

        # target the login button and click it
        button = WebDriverWait(
            self.driver, 2).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[type='submit']"))).click()

        time.sleep(10)


    def get_my_followers(self, user_name):
        self.driver.get('https://www.instagram.com/{}/'.format(user_name))

        time.sleep(3.5)

        WebDriverWait(self.driver, TIMEOUT).until(
            EC.presence_of_element_located((
                By.XPATH, "//a[contains(@href, '/followers')]"))).click()

        time.sleep(2)

        print('[Info] - Scraping...')

        users = set()

        for _ in range(round(MAX_FOLLOWERS_SCRAPE_COUNT // 20)):

            ActionChains(self.driver).send_keys(Keys.END).perform()

            time.sleep(1)

        followers = self.driver.find_elements(By.XPATH,
        "//a[contains(@href, '/')]")

        # Getting url from href attribute
        for i in followers:
            if i.get_attribute('href'):
                users.add(i.get_attribute('href').split("/")[3])
            else:
                continue

        print('[Info] - Saving...')
        print('[DONE] - Your followers are saved in followers.txt file!')

        with open('my_followers.txt', 'a') as file:
            file.write('\n'.join(users) + "\n")

    def get_followers(self, my_followers_arr, relations_file):
        for current_profile in my_followers_arr:
            print('[Info] - Scraping followers of {}...'.format(current_profile))
            try:
                self.driver.get('https://www.instagram.com/{}/'.format(current_profile))

                time.sleep(3.5)

                WebDriverWait(self.driver, TIMEOUT).until(
                    EC.presence_of_element_located((
                        By.XPATH, "//a[contains(@href, '/following')]"))).click()

                time.sleep(2)

                print('[Info] - Scraping...')

                current_profile_followers = set()

                for _ in range(round(MAX_FOLLOWERS_SCRAPE_COUNT // 20)):

                    ActionChains(self.driver).send_keys(Keys.END).perform()

                    time.sleep(1)

                followers = self.driver.find_elements(By.XPATH,
                "//a[contains(@href, '/')]")

                # Getting url from href attribute
                for i in followers:
                    if i.get_attribute('href'):
                        current_profile_followers.add(i.get_attribute('href').split("/")[3])
                    else:
                        continue
                
                with open(relations_file, "a") as outfile:
                    for follower in current_profile_followers:
                        line = "https://www.instagram.com/" + follower + "/ " + "https://www.instagram.com/" + current_profile + "/\n"
                        outfile.write(line)
            except:
                print("[Error] - Something went wrong while scraping followers of {}.".format(current_profile))
