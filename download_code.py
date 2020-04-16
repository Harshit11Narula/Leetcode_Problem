from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import json


class openleetcode():

    def setup(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-notifications')
        options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(chrome_options=options)

    def sign_in(self , user , password): 
        self.driver.get("https://leetcode.com/")
        sign_button = self.driver.find_elements_by_css_selector(".nav-right a span")
        sign_button[4].click()

        
        user_button = self.driver.find_element_by_name("login")
        pass_button = self.driver.find_element_by_name("password")
        user_button.send_keys(user)
        pass_button.send_keys(password)
        # wait = WebDriverWait(self.driver, 100)
        # wait.until(EC.presence_of_element_located((By.ID, 'signin_btn')))
        self.driver.find_element_by_id('signin_btn').click()
    
    def problem_set(self):
        wait = WebDriverWait(self.driver, 1000)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'ul.nav.navbar-nav a')))
        problem_button = self.driver.find_elements_by_css_selector("ul.nav.navbar-nav a")
        problem_button[2].click()

    def select_problem(self):
        wait = WebDriverWait(self.driver, 1000)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tbody.reactable-data tr')))
        
        size = Select(self.driver.find_element_by_css_selector('select.form-control'))
        size.select_by_index(3)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tbody.reactable-data tr')))
        all_problem = self.driver.find_elements_by_css_selector('tbody.reactable-data tr')
        cnt = 0
        urls = []
        for x in range(len(all_problem)):
            if all_problem[x].find_elements_by_css_selector('td .text-success'):
                url = all_problem[x].find_elements_by_css_selector('a')[0]
                url = url.get_attribute('href')
                cnt = cnt + 1
                urls.append(url)
        return urls

    
    def store_question(self, url):
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 1000)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-cy=question-title]')))
        problem_name = self.driver.find_element_by_css_selector('[data-cy=question-title]')
        
        problem_name = "codes/"+problem_name.text + ".txt"
        wait = WebDriverWait(self.driver, 1000)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-key=submissions]')))
        self.driver.find_element_by_css_selector('[data-key=submissions]').click()

        wait = WebDriverWait(self.driver, 1000)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tbody.ant-table-tbody td a')))
        all_solutions = self.driver.find_elements_by_css_selector('tbody.ant-table-tbody td a')
        for x in range(len(all_solutions)):
            if all_solutions[x].text == "Accepted":
                submissions_url = all_solutions[x].get_attribute('href')
                self.driver.get(submissions_url)
                wait = WebDriverWait(self.driver, 1000)
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.ace_line_group .ace_line')))
                code_line = self.driver.find_elements_by_css_selector('.ace_line_group .ace_line')
                code = open(problem_name , "w+")
                for line_no in range(len(code_line)):
                    code.write(code_line[line_no].text + "\n")
                code.close()
                break



if __name__ == "__main__":

    testcase = openleetcode()
    
    testcase.setup()
    
    file = open('credential.json',)
    data = json.load(file)
    testcase.sign_in(data['user_name'], data['pass'])
    
    testcase.problem_set()

    problems_url = testcase.select_problem()

    for url in problems_url:
        testcase.store_question(url)

         
