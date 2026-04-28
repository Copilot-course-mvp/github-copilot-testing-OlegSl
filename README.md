[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/YRfhgpv2)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23750017&assignment_repo_type=AssignmentRepo)
# GitHub Copilot Testing Practice — E-Commerce Order Processor

Welcome! This repository is a **hands-on learning environment** designed to help you practice writing tests using **GitHub Copilot**. You will explore a real Python application, understand how it works, and use Copilot to generate and improve the test suite.

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Project Structure](#project-structure)
3. [Prerequisites](#prerequisites)
4. [Getting Started](#getting-started)
5. [Running Tests](#running-tests)
6. [Learning Objectives](#learning-objectives)
7. [Student Exercises](#student-exercises)
8. [Tips for Using GitHub Copilot](#tips-for-using-github-copilot)

---

## Project Overview

The application is a simplified **E-Commerce Order Processing System** with three main layers:

| Layer | Modules | Responsibility |
|-------|---------|----------------|
| **Models** | `Product`, `Customer`, `Order` | Data structures and domain rules |
| **Services** | `InventoryService`, `OrderService`, `PricingService` | Business logic |
| **Utils** | `validators`, `formatters`, `calculator` | Reusable helper functions |

The application intentionally has **incomplete test coverage**. Your job is to use GitHub Copilot to fill in the gaps.

---

## Project Structure

```
├── src/                        # Application source code
│   ├── models/                 # Domain models (Product, Customer, Order)
│   ├── services/               # Business services (Inventory, Order, Pricing)
│   └── utils/                  # Utility functions (validators, formatters, calculator)
├── tests/                      # Unit tests (with intentional gaps)
│   ├── test_models/            # Model unit tests
│   ├── test_services/          # Service unit tests
│   └── test_utils/             # Utility unit tests
├── integration/                # End-to-end integration tests
├── .github/workflows/ci.yml    # GitHub Actions CI configuration
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup
└── pytest.ini                  # Pytest configuration
```

---

## Prerequisites

- Python 3.9 or higher
- pip
- GitHub Copilot access (in VS Code, JetBrains, or GitHub.com)

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/josevicenteayala/GitHubCopilot-Testing.git
cd GitHubCopilot-Testing
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

---

## Running Tests

### Run all unit tests

```bash
pytest tests/ -v
```

### Run all unit tests with coverage report

```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

### Run integration tests

```bash
pytest integration/ -v
```

### Run all tests (unit + integration)

```bash
pytest -v
```

### Run a specific test file

```bash
pytest tests/test_models/test_product.py -v
```

### Run tests matching a name pattern

```bash
pytest -k "test_discount" -v
```

---

## Learning Objectives

By completing the exercises in this repository, you will:

1. ✅ **Understand existing code** using GitHub Copilot's explanations and chat
2. ✅ **Generate missing unit tests** with Copilot suggestions
3. ✅ **Improve test coverage** across all modules
4. ✅ **Write integration tests** that span multiple components
5. ✅ **Validate behaviour** by running tests and interpreting results

---

## Student Exercises

### Exercise 1: Explore the Codebase with Copilot

Open any source file (e.g., `src/models/product.py`) and ask Copilot Chat:
> *"Explain what this class does and what edge cases I should test."*

### Exercise 2: Complete Missing Unit Tests

Search for `# TODO` comments throughout the test files. Each one marks a missing test case. Use Copilot to generate them:

```bash
grep -r "# TODO" tests/
grep -r "# TODO" integration/
```

Expected output lists ~30+ missing test cases across all modules.

### Exercise 3: Improve Branch Coverage

Run tests with coverage and identify uncovered branches:

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

Look for lines marked as not covered and ask Copilot:
> *"Write a test that covers line 45 of src/services/pricing_service.py"*

### Exercise 4: Write Integration Tests

Open `integration/test_order_flow.py` and complete the `# TODO` items in the `TestCancellationFlow` and `TestEdgeCases` classes. These require understanding how multiple services interact.

### Exercise 5: Find and Fix a Bug (Challenge)

The `calculate_percentage_change` function in `src/utils/calculator.py` has a subtle behaviour when given a **negative** old value. Use Copilot to:
1. Write a test that exposes the edge case
2. Determine if the current behaviour is correct or a bug
3. Fix it if necessary

### Exercise 6: Add a New Feature with Tests (Advanced)

Add a `WishlistService` to `src/services/` that allows customers to save products for later. Use Copilot to:
1. Generate the service class
2. Write comprehensive unit tests for it
3. Add an integration test that exercises the wishlist alongside orders

---

## Tips for Using GitHub Copilot

### In the editor
- Place your cursor after a `# TODO` comment and press `Tab` to accept a suggestion
- Write a descriptive test function name (`def test_apply_discount_with_negative_amount_raises_error`) and let Copilot generate the body

### In Copilot Chat
- *"What branches are not covered in `src/services/pricing_service.py`?"*
- *"Generate a pytest test for the `cancel_order` method in `OrderService`"*
- *"What happens if I call `record_purchase` with zero?"*

### Prompt tips
- Be specific: mention the function name, module, and expected behaviour
- Ask for multiple test cases at once: *"Give me 5 edge case tests for `validate_email`"*
- Ask Copilot to explain before generating: *"Explain what `advance_status` does, then write tests for it"*

---

## CI/CD

This repository includes a **GitHub Actions workflow** (`.github/workflows/ci.yml`) that automatically:

- Runs all unit tests (`tests/`) on Python 3.9 and 3.11
- Runs integration tests (`integration/`)
- Reports test coverage
- Uploads a coverage XML artifact

The workflow triggers on every push and pull request. You can view results in the **Actions** tab on GitHub.

---

## Getting Help

- Use **GitHub Copilot Chat** for in-editor assistance
- Check the [pytest documentation](https://docs.pytest.org/) for testing APIs
- Review the source code docstrings for function contracts

Happy testing! 🚀