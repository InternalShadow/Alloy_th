# Alloy API Integration

A Python application that integrates with the Alloy API to evaluate applicant data.

## What it does

- Submit applicant data to Alloy for evaluation
- Handle different evaluation outcomes (Approved, Manual Review, Denied)
- Support for both sample data and custom applicant input
- Provides validation and error handling
- Environment variable configuration

## Prerequisites

- Python 3.9.13+
- Alloy API credentials (Workflow Token and Secret Key)
  -- OPTIONAL: `.env` file with required environment variables

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
ALLOY_HOST=https://sandbox.alloy.co
ALLOY_WORKFLOW_TOKEN=your_workflow_token
ALLOY_SECRET_KEY=your_secret_key
```

## Installation

1. Clone the repository
2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application if you add a .env file of your own:

```bash
python main.py
```

If you want to forgo .env file one cli argument:

```bash
ALLOY_WORKFLOW_TOKEN='your_workflow_token' ALLOY_SECRET_KEY='your_secret_key' python main.py
```

The application will:

1. Present a menu with sample applicants
2. Allow you to choose a sample applicant or enter custom data
3. Submit the applicant data to Alloy
4. Display the evaluation outcome

## How Ai was used during the creation of this app

1. Used when looking up things on google i.e forgotten syntax (gemini is enabled by default)
2. Used intellisense to help with function typing, method peaking, autocomplete
