from datetime import date
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
      email = "john.doe@example.com",
      address_line_1 = "123 Main St",
      address_line_2 = "Apt 1",
      address_city = "Anytown",
      address_state = "CA",
      address_postal_code = "11211-1234",
      address_country_code = "US"
    ),
    models.Applicant(
      name_first = "Invalid",
      name_last = "Fail",
      birth_date = "1990-01-01",
      ssn = "123456789",
      email = "invalid.fail@example.com",
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
        name_first = "Please",
        name_last = "Deny",
        birth_date = "1990-01-01",
        ssn = "123456789",
        email = "please.deny@example.com",
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



# def main
# -parse command line arguments 
# predefined map of person data 
# def main()
# check command line arguments 
# if run predefined person data
# loadSampleData()
# for each person in sample data:
# createPerson(data**) 
# API client
# AllyClient


# def submit_applicant(applicant: models.Applicant, api_url: str, headers: Optional[dict] = None) -> dict:
#     """Submit applicant data to the specified API endpoint."""
#     data = applicant.model_dump()
#     data['date_of_birth'] = data['date_of_birth'].isoformat()
#     return { "status": "success", "message": "Applicant submitted successfully" }




# def validate_and_submit_person(person_data: Optional[dict], api_url: str) -> None:
#     """Validate and submit person data to the API."""
#     try:
#         if person_data:
#             print(f"\nSelected person: {person_data['firstName']} {person_data['lastName']}")
#             # Pre-validate the data before creating Applicant instance
#             if not person_data["address"]["state"].isalpha() or len(person_data["address"]["state"]) != 2 :
#                 print("Warning: Selected person has invalid state code. Please choose a valid person or enter custom data.")
#                 return
#             if len(person_data["ssn"]) != 9 or not person_data["ssn"].isdigit():
#                 print("Warning: Selected person has invalid SSN. Please choose a valid person or enter custom data.")
#                 return
            
#             applicant = Applicant(
#                 first_name=person_data["firstName"],
#                 last_name=person_data["lastName"],
#                 date_of_birth=date.fromisoformat(person_data["dateOfBirth"]),
#                 ssn=person_data["ssn"],
#                 email=person_data["email"],
#                 address=Address(
#                     line1=person_data["address"]["line1"],
#                     line2=person_data["address"]["line2"],
#                     city=person_data["address"]["city"],
#                     state=person_data["address"]["state"],
#                     zip_code=person_data["address"]["zipCode"],
#                     country=person_data["address"]["country"]
#                 )
#             )
#         else:
#             print("\nPlease enter the applicant's details:")
#             applicant = collect_applicant_details()
        
#         response = submit_applicant(applicant, api_url)
#         print(f"\nApplication submitted successfully!")
#         print(f"Response: {response}")
        
#     except ValueError as e:
#         print(f"\nValidation error: {str(e)}")
#     except httpx.HTTPError as e:
#         print(f"\nAPI error: {str(e)}")
#     except Exception as e:
#         print(f"\nUnexpected error: {str(e)}")