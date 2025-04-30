from typing import List, Optional, Callable

from dotenv import load_dotenv
import os
import models
from alloy_client import AlloyClient

applicant_data =  [
    models.Applicant(
      name_first = "John",
      name_last = "Passing",
      birth_date = "1990-01-01",
      ssn = "123456789",
      email = "john.passing@example.com",
      address_line_1 = "123 Main St",
      address_line_2 = "Apt 1",
      address_city = "Anytown",
      address_state = "CA",
      address_postal_code = "11211-1234",
      address_country_code = "US"
    ),
    models.Applicant(
      name_first = "Willnot",
      name_last = "Fail",
      birth_date = "1990-01-01",
      ssn = "123456789",
      email = "willnot.fail@example.com",
      address_line_1 = "123 Main St",
      address_line_2 = "Apt 1",
      address_city = "Anytown",
      address_state = "CA",
      address_postal_code = "11211-1234",
      address_country_code = "US"
    ),
    models.Applicant(
        name_first = "Needs",
        name_last = "Review",
        birth_date = "1990-01-01",
        ssn = "123456789",
        email = "needs.review@example.com",
        address_line_1 = "123 Main St",
        address_line_2 = "Apt 1",
        address_city = "Anytown",
        address_state = "CA",
        address_postal_code = "11211-1234",
        address_country_code = "US"
    ),
    models.Applicant(
        name_first = "You",
        name_last = "Deny",
        birth_date = "1990-01-01",
        ssn = "123456789",
        email = "you.deny@example.com",
        address_line_1 = "123 Main St",
        address_line_2 = "Apt 1",
        address_city = "Anytown",
        address_state = "CA",
        address_postal_code = "11211-1234",
        address_country_code = "US"
    )
] 

def collect_applicant_attribute(message: str, validator: Callable[[str], str] ) -> str:
    while True:
        user_input = input(message).strip()
        is_valid, error_message = validator(user_input)
        if is_valid:
           return user_input
        else:
           print(f"Invalid input: {error_message}. Please try again.")
    

      
def collect_applicant_details() -> models.Applicant:
    """Collect applicant details from user input."""
    print("Please enter the applicant's details:")
    
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    
    date_of_birth = collect_applicant_attribute("Date of Birth (YYYY-MM-DD): ", models.is_date_valid)
    ssn = collect_applicant_attribute("SSN (9 digits, no dashes): ", models.is_ssn_valid)
    email = collect_applicant_attribute("Email Address: ", models.is_email_valid)
    
    line1=input("Address Line 1: ").strip()
    line2=input("Address Line 2 (optional, press Enter to skip): ").strip() or None
    city=input("City: ").strip()
    state=input("State (2-letter code, e.g., NY, CA): ").strip().upper()
    zip_code=input("ZIP Code: ").strip()
    
    return models.Applicant(
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        ssn=ssn,
        email=email,
        address_line_1=line1,
        address_line_2=line2,
        address_city=city,
        address_state=state,
        address_postal_code=zip_code,
        address_country_code="US"
    )

def display_menu(sample_data: List[models.Applicant]):
    print("\nAvailable sample persons:")
    for i, person in enumerate(sample_data, 1):
        status = "✓" if person.address_state.isalpha() and len(person.address_state) == 2 else "✗"
        print(f"{i}. {person.name_first} {person.name_last} ({status})")
    print("\nEnter the number of the person to use, or 'n' to enter custom data:")


def get_user_choice(sample_data: List[models.Applicant]) -> Optional[int]:
    while True:
        choice = input().strip().lower()
        if choice == 'n':
            return None
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(sample_data):
                return idx
            print(f"Please enter a number between 1 and {len(applicant_data['persons'])}")
        except ValueError:
            print("Please enter a valid number or 'n'")


def submit_applicant(client: AlloyClient, applicant: models.Applicant) -> None:
    client.create_evaluation(applicant)



def main():
    """Main function to collect and submit applicant data."""
    """Set up environment variables"""
    load_dotenv()
    host  = os.getenv("ALLOY_HOST", default=" https://sandbox.alloy.co")
    workflow_token = os.getenv("ALLOY_WORKFLOW_TOKEN", default="")
    secret_key = os.getenv("ALLOY_SECRET_KEY", default="")
    
    client = AlloyClient(host, workflow_token, secret_key)
    try:
        print("Welcome to the Applicant Submission System")
        print("You can either use sample data or enter your own details.")
        display_menu(applicant_data)
        choice = get_user_choice(applicant_data)
        if choice is not None:
           applicant = applicant_data[choice]
           submit_applicant(client, applicant) 
        else:
           applicant = collect_applicant_details()
           submit_applicant(applicant)
                  
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()
