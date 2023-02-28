Feature: Customers
""" 
Confirm that we can browse the customer related pages on our site
"""

Scenario: success for visiting metrics page and display the search resuts
    Given I navigate to the metrics page and input my query
    When I click on the submit button in the form
    Then I should see the filtered output table of CO2 emissions data.