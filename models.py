from email_validator import validate_email, EmailNotValidError
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Tuple
import re
from datetime import datetime, date

    
class Applicant(BaseModel):
    name_first: str
    name_last: str
    birth_date: date
    ssn: str = Field(..., min_length=9, max_length=9)
    email: str
    address_line_1: str
    address_line_2: Optional[str] = None
    address_city: str
    address_state: str = Field(..., min_length=2, max_length=2)
    address_postal_code: str
    address_country_code: str = "US"

    @field_validator('ssn')
    @classmethod
    def validate_ssn(cls, v):
        if not v.isdigit():
            raise ValueError('SSN must contain only digits')
        if len(v) != 9:
            raise ValueError('SSN must be 9 digits long')
        return v
     
    @field_validator('address_state')
    @classmethod
    def validate_state(cls, v):
        if not v.isalpha() or not v.isupper():
            raise ValueError('State must be a two-letter uppercase code')
        return v

    @field_validator('address_postal_code')
    @classmethod
    def validate_zip_code(cls, v):
        if not re.match(r'^\d{5}(-\d{4})?$', v):
            raise ValueError('Invalid ZIP code format')
        return v

    @field_validator('address_country_code')
    @classmethod
    def validate_country(cls, v):
        if v != "US":
            raise ValueError('Country must be "US"')
        return v 

    def to_json(self):
        birth_date = self.birth_date.isoformat()
        return {
            "name_first": self.name_first,
            "name_last": self.name_last,
            "birth_date": birth_date,
            "ssn": self.ssn,
            "email": self.email,
            "address_line_1": self.address_line_1,
            "address_line_2": self.address_line_2,
            "address_city": self.address_city,
            "address_state": self.address_state,
            "address_postal_code": self.address_postal_code,
            "address_country_code": self.address_country_code
        }

def is_date_valid(date_str: str) -> Tuple[bool, str]:
    try:
        date.fromisoformat(date_str)
        return (True, "")
    except ValueError:
        return (False, "Invalid date format. Please use YYYY-MM-DD format.")


def is_ssn_valid(ssn: str) -> Tuple[bool, str]:
    if len(ssn) != 9 or not ssn.isdigit():
        return (False, "SSN must be 9 digits without dashes.")
    return (True, "")


def is_email_valid(email: str) -> Tuple[bool, str]:
    try:
        validate_email(email)
        return (True, "")
    except EmailNotValidError as e:
        return (False, f"Invalid email format: {e}")
    
    
# TODO
# serialize response from alloy 
# remove pbd
