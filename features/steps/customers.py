from behave import given, when, then

@given(u'I navigate to the metrics page and input my query')
def nav(context):
    """ 
    Navigate to the metrics page
    """
    context.browser.get('http://localhost:5000/metrics')

@when(u'I click on the submit button in the form')
def click(context):
    """ 
    find the desired form in the page
    """
    context.browser.find_element_by_partial_link_text('2').click()

@then(u'I should see the filtered output table of CO2 emissions data')
def details(context):
    """ 
    if successful, then we should see the fitered output in the form of a table.
    """
    # use print(context.browser.page_source) to aid debugging
    print(context.browser.page_source)
    assert context.browser.current_url == 'http://localhost:5000/metrics'
    assert '01595 Amanda Loaf' in context.browser.page_source