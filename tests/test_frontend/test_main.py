
import pytest
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from dash.testing.application_runners import import_app

# driver = webdriver.Chrome(r'tests/chromedriver.exe')


# def test__tstm001_elementtest(browser):
#     browser.get('https://google.com')
#     query_window = browser.find_element_by_name('q')
#     assert query_window.is_displayed()


def test__tstm001_elementtest(dash_duo):
    app = import_app("index")
    dash_duo.start_server(app)
    dash_duo.wait_for_text_to_equal(
        "h1", "Dashboard Analysis for Web Assignment", timeout=4)
    assert dash_duo.find_element(
        "h1").text == "Dashboard Analysis for Web Assignment"

    # dash_duo.wait_for_text_to_equal("#dropdown2", "10002", timeout=5)
    # assert dash_duo.find_element("#dropdown2").text == '10002'
    # WebDriverWait(dash_duo.driver, 10).until(
    #     expected_conditions.visibility_of_element_located(
    #         (By.CSS_SELECTOR, "#graph1")))
    # dash_duo.wait_for_element_by_id('graph1', timeout=30)
    # assert dash_duo.driver.find_element_by_css_selector(
    #     "#example-graph").is_displayed()
    # assert dash_duo.find_element(
    #     "H1").text == "Dashboard Analysis for Web Assignment"
