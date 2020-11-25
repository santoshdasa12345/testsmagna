from time import sleep
from features import settings as env
from behave import *
from selenium import webdriver


@Given("Launch Chrome browser")
def step_impl(context):
    context.driver = webdriver.Chrome(env.CHROME_DRIVER)


@When("User is navigating to Login Page")
def step_impl(context):
    context.driver.get(env.DOMAIN_URL + "/login/")
    context.driver.fullscreen_window()


@When("User need to enter user name as <email address> and password as <Password>")
def step_impl(context):
    context.driver.find_element_by_xpath("//input[@name='email']").send_keys(env.LOGIN_USER_NAME)
    context.driver.find_element_by_xpath("//input[@id='password']").send_keys (env.LOGIN_PASSWORD)
    sleep(2)


@Then("click on login button")
def step_impl(context):
    context.driver.find_element_by_xpath("//button[@id='signup-modal-submit']").click()
    sleep(5)




