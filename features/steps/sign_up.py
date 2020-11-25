import time

from behave import *
from selenium import webdriver

from features import settings as env
from features.helpers.read_email import ReadEmail


@given("User is navigating to signup Page")
def step_impl(context):
    for row in context.table:
        emailaddress = row['emailaddress']
        password = row['password']
        if not hasattr(context, 'driver'):
            context.driver = webdriver.Chrome(env.CHROME_DRIVER)#https://magna-beta.great.uktrade.digital/signup/
            context.driver.refresh()

        context.driver.get(env.DOMAIN_URL + "/signup/")
        context.driver.find_element_by_xpath("//legend[contains(text(),'Sign up to great.gov.uk')]").is_displayed()

        context.execute_steps('''when User need to enter userdetails {emailaddress} and {password}'''
                              .format(emailaddress=emailaddress, password=password))


@when("User need to enter userdetails {emailaddress} and {password}")
def step_impl(context, emailaddress, password):
    context.driver.find_element_by_xpath("//input[@id='email']").send_keys(emailaddress)
    context.driver.find_element_by_xpath("//input[@id='password']").send_keys(password)
    context.driver.find_element_by_xpath("//button[@id='signup-modal-submit']").click()
    time.sleep(5)
    context.execute_steps('''then User should receive an email on {emailaddress} and {password} with confirmation link'''
                          .format(emailaddress=emailaddress, password=password))


@then("User should receive an email on {emailaddress} and {password} with confirmation link")
def step_impl(context, emailaddress, password):
    time.sleep(20)

    # create and load the confirmation code email from the test user
    objreadmail = ReadEmail(env.DEV_GMAIL_HOST, emailaddress, password, env.EMAIL_FETCH_COUNT)
    # search the test user INBOX, read the confirmation code email body text
    email_body_text = objreadmail.reademailbody(env.EMAIL_SEARCH_SUBJECT, env.EMAIL_SEARCH_CRITERIA)

    # check if the email_body_text exists or empty
    if email_body_text:
        # search text position in email_body_text
        c_code_pos = email_body_text.find(env.EMAIL_SEARCH_CRITERIA)
        confirmation_code = '00000' # default
        # check if the required search criteria text found in the email_body_text. -1 indicates not found.
        if c_code_pos != -1:
            confirmation_code = email_body_text[c_code_pos + len(env.EMAIL_SEARCH_CRITERIA):c_code_pos + len(env.EMAIL_SEARCH_CRITERIA) + env.CONFIRMATION_CODE_LENGTH]
        confirmation_code = confirmation_code.strip() # trim left and right

        if confirmation_code.isdigit():

            # wait for 20 seconds to allow loading of the webpage
            context.driver.implicitly_wait(30)  # seconds
            # search for control to enter confirmation code.
            context.driver.find_element_by_xpath("//input[@name='code']").send_keys(confirmation_code)
            context.driver.implicitly_wait(20)  # seconds
            # search and click submit button after entering the confirmation code
            context.driver.find_element_by_xpath("//button[@id='signup-modal-submit-code']").click()
            context.driver.find_element_by_xpath("// h2[contains(text(), 'Sign up complete')]").is_displayed()
            context.driver.find_element_by_xpath("//a[@id='signup-modal-submit-success']").click()
        else:
            assert confirmation_code.isdigit() == True, "Failed to fetch confirmation code from mail"


@then("User should click on  the confirmation email link")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """


@then("User should able to login to Home Page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
