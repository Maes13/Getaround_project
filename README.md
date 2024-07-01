# GetAround deployment project - Delay analysis and car rental price prediction


## Goal of the project

The goal of this project is to develop and deploy several online apps for data analysis, machine learning training and inference for GetAround.  
To address the needs of your Product Manager and provide meaningful insights for decision-making, we can break down the analysis into several key areas. Here is a structured plan:

Data Analysis Plan

1. Assess Impact on Owner's Revenue
Objective: Estimate the share of the owner's revenue that could be affected by introducing a minimum delay between rentals.
Approach:
Calculate the total revenue for each owner.
Identify the rentals that would be affected by different thresholds (e.g., 1 hour, 2 hours, 4 hours) and scopes (all cars vs. Connect cars only).
Calculate the potential revenue loss by comparing the revenue from affected rentals to the total revenue.
2. Determine Affected Rentals
Objective: Quantify how many rentals would be impacted by the feature based on different thresholds and scopes.
Approach:
Analyze the distribution of the time gap between successive rentals for each car.
Count the number of rentals that fall within the specified thresholds.
3. Analyze Late Check-ins
Objective: Understand the frequency of late check-ins and their impact on subsequent rentals.
Approach:
Calculate the average and distribution of check-in delays.
Identify cases where a late check-in causes a delay for the next rental.
Measure the impact on the next driver in terms of wait time or delayed start.
4. Evaluate Problematic Cases Resolved
Objective: Estimate how many problematic cases (late check-ins affecting the next rental) could be resolved by implementing the feature.
Approach:
Cross-reference the data on late check-ins with the potential delay thresholds.
Calculate the reduction in problematic cases for each threshold and scope.
Additional Relevant Analyses
Driver Satisfaction: Analyze customer feedback or ratings to understand the impact of rental delays on driver satisfaction.
Operational Efficiency: Assess how the minimum delay could improve operational efficiency and reduce conflicts between bookings.
Data Requirements
To perform the analyses, we'll need the following data:

Rental history including check-in and check-out times, car IDs, owner IDs, and revenue per rental.
Car type (Connect car or not).
Any recorded delays in check-ins and the subsequent impacts on rentals.
Customer feedback or ratings related to rental experiences.

## Deliverables

- Web dashboard for delay analysis and simulations : **https://my-app-car-rental-7bbb5ddf45e4.herokuapp.com/**
- Web API for car rental price predictions : **https://my-fastapi-price-pred-fa365ce4b512.herokuapp.com/**

## Author

Mead SOULEIMAN 
