Feature: Tests for daily releases - MOBILE

  #noinspection CucumberUndefinedStep
  @run @madrid @mobile @new_user
  Scenario: Test OP.GG
    Given I open the main OP.GG page
    Then the OP.GG page loaded successfully
    When I search for "test"
    Then I get a result
    And I store the result 
