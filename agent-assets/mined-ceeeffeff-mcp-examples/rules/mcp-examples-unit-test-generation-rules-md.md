---
alwaysApply: false
---

# Unit Test Style Enforcing Rule

## Overview

This rule ensures that all generated unit tests adhere to a consistent and effective style, improving the overall quality and reliability of your codebase.

## Key Points

1. **Modularization**: Each test function should focus on a single aspect or functionality, ensuring clarity and maintainability.
2. **Use of Fixtures**:
    - Utilize fixtures to set up necessary environments for tests without polluting the global namespace.
3. **Mocking and Stubbing with pytest**:
    - Use mocking and stubbing tools like `patch` from the `unittest.mock` module in pytest to simulate external dependencies, keeping tests isolated from production environments.
4. **Parameterized Tests with pytest**: Leverage parameterized tests to cover multiple scenarios efficiently.
5. **Asserts for Expected Outcomes**: Write assertions that validate the expected behavior of the code under test, ensuring correctness.
6. **Coverage of Edge Cases and Error Handling**: Include tests to handle edge cases and exceptions, ensuring robustness.
7. **Separation of Responsibilities**: Each test function should be dedicated to a single responsibility, making them easy to understand and maintain.
8. **Consistent Use of Assertions**: Ensure consistent use of assert statements to validate conditions clearly and effectively.

## Example Poorly Parameterised Tests

### Bad design
Here's an example of tests which don't use fixtures or paramaterisation and so are poor in design.

```python
def test_ensure_sorted_crawl_fn_to_details_validator():
    # Arrange
    config = {
        "crawl_fn_to_details": {
            "Competitor1": CompanyConfiguration(display_order=2),
            "Client1": CompanyConfiguration(display_order=1),
            "Competitor2": CompanyConfiguration(display_order=3)
        }
    }

    # Act
    job_config = JobConfiguration(**config)

    # Assert
    assert job_config.crawl_fn_to_details == {
        "Client1": CompanyConfiguration(display_order=1),
        "Competitor1": CompanyConfiguration(display_order=2),
        "Competitor2": CompanyConfiguration(display_order=3)
    }

def test_ensure_sorted_crawl_fn_to_details_validator_with_no_display_order():
    # Arrange
    config = {
        "crawl_fn_to_details": {
            "Client1": CompanyConfiguration(display_order=None),
            "Competitor1": CompanyConfiguration(display_order=None),
            "Competitor2": CompanyConfiguration(display_order=None)
        }
    }

    # Act
    job_config = JobConfiguration(**config)

    # Assert
    assert job_config.crawl_fn_to_details == {
        "Client1": CompanyConfiguration(display_order=None),
        "Competitor1": CompanyConfiguration(display_order=None),
        "Competitor2": CompanyConfiguration(display_order=None)
    }
```

### Improved design
An now an improved design that used parameterisation and resuable construction - even better would be a callable fixture.

```python
def create_company_configurations(display_orders: List[int]) -> Dict[str, CompanyConfiguration]:
    def name(index: int, order: int):
        return f"company_{index}_{order}"

    return {
        name(index, order): CompanyConfiguration(
            display_order=order if order is not None else 0,
            site_name=name(index, order),
            site_domain=f"{name(index, order)}.com",
            site_cookie=f"cookie{name(index, order)}",
            site_homepage=f"{name(index, order)}.com",
        )
        for index, order in enumerate(display_orders)
    }


@pytest.mark.parametrize(
    "display_orders",
    [
        ([1, 0, 2]),
        ([2, 1, 0]),
        ([3, 1, 0, 2]),
        (
            [
                0,
                2,
                1,
            ]
        ),
        ([None, None, None]),
        ([None, 0, None, 1, None, 2, None]),
    ],
)
def test_ensure_sorted_crawl_fn_to_details_validator(display_orders):
    # Arrange
    config = {"crawl_fn_to_details": create_company_configurations(display_orders)}

    # Act
    job_config = JobConfiguration(
        config=AttemptConfiguration(
            categories=["Category1"],
            market="Market1",
            client="Client1",
            job="Job1",
            job_type=JobType.YMYL,
            crawl_location="crawls",
            derived_fields="derivation/derived_fields_config_extended_with_page_category.yaml",
        ),
        **config,
    )

    # Assert
    expected_display_orders = sorted([display_order if display_order is not None else 0 for display_order in display_orders])
    actual_display_orders = [
        job_config.crawl_fn_to_details[company].display_order for company in job_config.crawl_fn_to_details
    ]

    assert expected_display_orders == actual_display_orders
```

## Another Example of a Better-Structured Test

Here's an example of how a better-structured test might look:

```python
def test_transition_to_next_state_successful_with_db_update(f_job, job_service, mock_db_client):
    # Arrange
    fake_job = f_job()
    # Act
    orig_status = job_service.transition_to_job_state(fake_job, JobStatus.CATEGORISING, "test_message")
    
    # Assert
    assert orig_status != fake_job.status_current
    assert fake_job.status_current.status == JobStatus.CATEGORISING
    
    expected_messages = [
        JobRunStatus(message="Drafted via legacy job creation."),
        JobRunStatus(status=JobStatus.QUEUED_CATEGORISATION, message="Initiated via GCS Object Notification."),
        JobRunStatus(status=JobStatus.CATEGORISING, message="Initiated via GCS Object Notification."),
    ]
    
    for expected_message in expected_messages:
        assert any(m.message == expected_message.message and m.status == expected_message.status for m in fake_job.status_history)
    
    mock_db_client.store_job.assert_called_once_with(fake_job)
```

## How to Generate Tests Like These in Future

1. **Identify Key Scenarios**: Carefully identify the key scenarios and edge cases that need to be tested for each method.
2. **Use Mocks**: Use mocking tools like `patch` from the `unittest.mock` module to simulate dependencies, ensuring tests are isolated.
3. **Write Specific Assertions**: Write assertions that cover specific properties and behavior of the methods under test.
4. **Include Error Handling**: Include checks for exceptions and error handling, ensuring robustness.
5. **Use Fixtures**: Utilize fixtures (e.g., `@pytest.fixture`) to set up consistent test environments before each test. Utilize existing fixtures from conftest.py where applicable.
6. **Concise Code Snippets**: Ensure that code snippets in tests are concise and focused only on the necessary changes.

## Rule Application

This rule applies to all unit tests generated in the future. Ensure that all new or updated tests follow the guidelines outlined above to maintain consistency and effectiveness in your test suite.


https://github.com/continuedev/continue/blob/cab9ce70e01d66dcd994420c3cad4d7859b31c33/core/llm/llms/Ollama.ts#L83