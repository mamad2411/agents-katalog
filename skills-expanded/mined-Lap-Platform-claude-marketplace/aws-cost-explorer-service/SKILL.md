---
name: aws-cost-explorer-service
description: "AWS Cost Explorer Service API skill. Use when working with AWS Cost Explorer Service for root. Covers 41 endpoints."
version: 1.0.0
generator: lapsh
---

# AWS Cost Explorer Service
API version: 2017-10-25

## Auth
AWS SigV4

## Base URL
Not specified.

## Setup
1. Configure auth: AWS SigV4
3. POST / -- create first resource

## Endpoints

41 endpoints across 1 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| POST | / | Creates a new cost anomaly detection monitor with the requested type and monitor specification. |
| POST | / | Adds an alert subscription to a cost anomaly detection monitor. You can use each subscription to define subscribers with email or SNS notifications. Email subscribers can set an absolute or percentage threshold and a time frequency for receiving notifications. |
| POST | / | Creates a new Cost Category with the requested name and rules. |
| POST | / | Deletes a cost anomaly monitor. |
| POST | / | Deletes a cost anomaly subscription. |
| POST | / | Deletes a Cost Category. Expenses from this month going forward will no longer be categorized with this Cost Category. |
| POST | / | Returns the name, Amazon Resource Name (ARN), rules, definition, and effective dates of a Cost Category that's defined in the account. You have the option to use EffectiveOn to return a Cost Category that's active on a specific date. If there's no EffectiveOn specified, you see a Cost Category that's effective on the current date. If Cost Category is still effective, EffectiveEnd is omitted in the response. |
| POST | / | Retrieves all of the cost anomalies detected on your account during the time period that's specified by the DateInterval object. Anomalies are available for up to 90 days. |
| POST | / | Retrieves the cost anomaly monitor definitions for your account. You can filter using a list of cost anomaly monitor Amazon Resource Names (ARNs). |
| POST | / | Retrieves the cost anomaly subscription objects for your account. You can filter using a list of cost anomaly monitor Amazon Resource Names (ARNs). |
| POST | / | Retrieves estimated usage records for hourly granularity or resource-level data at daily granularity. |
| POST | / | Retrieves cost and usage metrics for your account. You can specify which cost and usage-related metric that you want the request to return. For example, you can specify BlendedCosts or UsageQuantity. You can also filter and group your data by various dimensions, such as SERVICE or AZ, in a specific time range. For a complete list of valid dimensions, see the GetDimensionValues operation. Management account in an organization in Organizations have access to all member accounts. For information about filter limitations, see Quotas and restrictions in the Billing and Cost Management User Guide. |
| POST | / | Retrieves cost and usage metrics with resources for your account. You can specify which cost and usage-related metric, such as BlendedCosts or UsageQuantity, that you want the request to return. You can also filter and group your data by various dimensions, such as SERVICE or AZ, in a specific time range. For a complete list of valid dimensions, see the GetDimensionValues operation. Management account in an organization in Organizations have access to all member accounts. Hourly granularity is only available for EC2-Instances (Elastic Compute Cloud) resource-level data. All other resource-level data is available at daily granularity.  This is an opt-in only feature. You can enable this feature from the Cost Explorer Settings page. For information about how to access the Settings page, see Controlling Access for Cost Explorer in the Billing and Cost Management User Guide. |
| POST | / | Retrieves an array of Cost Category names and values incurred cost.  If some Cost Category names and values are not associated with any cost, they will not be returned by this API. |
| POST | / | Retrieves a forecast for how much Amazon Web Services predicts that you will spend over the forecast time period that you select, based on your past costs. |
| POST | / | Retrieves all available filter values for a specified filter over a period of time. You can search the dimension values for an arbitrary string. |
| POST | / | Retrieves the reservation coverage for your account, which you can use to see how much of your Amazon Elastic Compute Cloud, Amazon ElastiCache, Amazon Relational Database Service, or Amazon Redshift usage is covered by a reservation. An organization's management account can see the coverage of the associated member accounts. This supports dimensions, Cost Categories, and nested expressions. For any time period, you can filter data about reservation usage by the following dimensions:   AZ   CACHE_ENGINE   DATABASE_ENGINE   DEPLOYMENT_OPTION   INSTANCE_TYPE   LINKED_ACCOUNT   OPERATING_SYSTEM   PLATFORM   REGION   SERVICE   TAG   TENANCY   To determine valid values for a dimension, use the GetDimensionValues operation. |
| POST | / | Gets recommendations for reservation purchases. These recommendations might help you to reduce your costs. Reservations provide a discounted hourly rate (up to 75%) compared to On-Demand pricing. Amazon Web Services generates your recommendations by identifying your On-Demand usage during a specific time period and collecting your usage into categories that are eligible for a reservation. After Amazon Web Services has these categories, it simulates every combination of reservations in each category of usage to identify the best number of each type of Reserved Instance (RI) to purchase to maximize your estimated savings.  For example, Amazon Web Services automatically aggregates your Amazon EC2 Linux, shared tenancy, and c4 family usage in the US West (Oregon) Region and recommends that you buy size-flexible regional reservations to apply to the c4 family usage. Amazon Web Services recommends the smallest size instance in an instance family. This makes it easier to purchase a size-flexible Reserved Instance (RI). Amazon Web Services also shows the equal number of normalized units. This way, you can purchase any instance size that you want. For this example, your RI recommendation is for c4.large because that is the smallest size instance in the c4 instance family. |
| POST | / | Retrieves the reservation utilization for your account. Management account in an organization have access to member accounts. You can filter data by dimensions in a time period. You can use GetDimensionValues to determine the possible dimension values. Currently, you can group only by SUBSCRIPTION_ID. |
| POST | / | Creates recommendations that help you save cost by identifying idle and underutilized Amazon EC2 instances. Recommendations are generated to either downsize or terminate instances, along with providing savings detail and metrics. For more information about calculation and function, see Optimizing Your Cost with Rightsizing Recommendations in the Billing and Cost Management User Guide. |
| POST | / | Retrieves the details for a Savings Plan recommendation. These details include the hourly data-points that construct the cost, coverage, and utilization charts. |
| POST | / | Retrieves the Savings Plans covered for your account. This enables you to see how much of your cost is covered by a Savings Plan. An organization’s management account can see the coverage of the associated member accounts. This supports dimensions, Cost Categories, and nested expressions. For any time period, you can filter data for Savings Plans usage with the following dimensions:    LINKED_ACCOUNT     REGION     SERVICE     INSTANCE_FAMILY    To determine valid values for a dimension, use the GetDimensionValues operation. |
| POST | / | Retrieves the Savings Plans recommendations for your account. First use StartSavingsPlansPurchaseRecommendationGeneration to generate a new set of recommendations, and then use GetSavingsPlansPurchaseRecommendation to retrieve them. |
| POST | / | Retrieves the Savings Plans utilization for your account across date ranges with daily or monthly granularity. Management account in an organization have access to member accounts. You can use GetDimensionValues in SAVINGS_PLANS to determine the possible dimension values.  You can't group by any dimension values for GetSavingsPlansUtilization. |
| POST | / | Retrieves attribute data along with aggregate utilization and savings data for a given time period. This doesn't support granular or grouped data (daily/monthly) in response. You can't retrieve data by dates in a single response similar to GetSavingsPlanUtilization, but you have the option to make multiple calls to GetSavingsPlanUtilizationDetails by providing individual dates. You can use GetDimensionValues in SAVINGS_PLANS to determine the possible dimension values.   GetSavingsPlanUtilizationDetails internally groups data by SavingsPlansArn. |
| POST | / | Queries for available tag keys and tag values for a specified period. You can search the tag values for an arbitrary string. |
| POST | / | Retrieves a forecast for how much Amazon Web Services predicts that you will use over the forecast time period that you select, based on your past usage. |
| POST | / | Retrieves a list of your historical cost allocation tag backfill requests. |
| POST | / | Get a list of cost allocation tags. All inputs in the API are optional and serve as filters. By default, all cost allocation tags are returned. |
| POST | / | Returns the name, Amazon Resource Name (ARN), NumberOfRules and effective dates of all Cost Categories defined in the account. You have the option to use EffectiveOn to return a list of Cost Categories that were active on a specific date. If there is no EffectiveOn specified, you’ll see Cost Categories that are effective on the current date. If Cost Category is still effective, EffectiveEnd is omitted in the response. ListCostCategoryDefinitions supports pagination. The request can have a MaxResults range up to 100. |
| POST | / | Retrieves a list of your historical recommendation generations within the past 30 days. |
| POST | / | Returns a list of resource tags associated with the resource specified by the Amazon Resource Name (ARN). |
| POST | / | Modifies the feedback property of a given cost anomaly. |
| POST | / | Request a cost allocation tag backfill. This will backfill the activation status (either active or inactive) for all tag keys from para:BackfillFrom up to the when this request is made. You can request a backfill once every 24 hours. |
| POST | / | Requests a Savings Plans recommendation generation. This enables you to calculate a fresh set of Savings Plans recommendations that takes your latest usage data and current Savings Plans inventory into account. You can refresh Savings Plans recommendations up to three times daily for a consolidated billing family.   StartSavingsPlansPurchaseRecommendationGeneration has no request syntax because no input parameters are needed to support this operation. |
| POST | / | An API operation for adding one or more tags (key-value pairs) to a resource. You can use the TagResource operation with a resource that already has tags. If you specify a new tag key for the resource, this tag is appended to the list of tags associated with the resource. If you specify a tag key that is already associated with the resource, the new tag value you specify replaces the previous value for that tag. Although the maximum number of array members is 200, user-tag maximum is 50. The remaining are reserved for Amazon Web Services use. |
| POST | / | Removes one or more tags from a resource. Specify only tag keys in your request. Don't specify the value. |
| POST | / | Updates an existing cost anomaly monitor. The changes made are applied going forward, and doesn't change anomalies detected in the past. |
| POST | / | Updates an existing cost anomaly subscription. Specify the fields that you want to update. Omitted fields are unchanged.  The JSON below describes the generic construct for each type. See Request Parameters for possible values as they apply to AnomalySubscription. |
| POST | / | Updates status for cost allocation tags in bulk, with maximum batch size of 20. If the tag status that's updated is the same as the existing tag status, the request doesn't fail. Instead, it doesn't have any effect on the tag status (for example, activating the active tag). |
| POST | / | Updates an existing Cost Category. Changes made to the Cost Category rules will be used to categorize the current month’s expenses and future expenses. This won’t change categorization for the previous months. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
