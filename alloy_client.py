import base64
import requests
import json
from models import Applicant

class AlloyError(Exception):
  def __init__(self, response: dict):
    self.response = response
    self.status_code = response.get('status_code')
    self.error = response.get('error', {})
    self.message = self.error.get('message')
    self.details = self.error.get('details', {})
    super().__init__(self.message)

class AlloyEvaluation:
  def __init__(self, response: dict) -> None:
    self.response = response
    self.summary = response.get('summary', {})
    self.evaluation_token = response.get('evaluation_token')
    self.entity_token = response.get('entity_token')
    self.outcome = self.summary.get('outcome')
  
  def is_approved(self):
    return self.outcome == "Approved"
  
  def is_manual_review(self):
    return self.outcome == "Manual Review"
  
  def is_denied(self):
    return self.outcome == "Denied"
    
  def get_outcome_message(self):
    if self.is_approved():
      print("Congratulations! You are approved.")
    elif self.is_manual_review():
      print("Your application is under review. Please wait for further updates.")
    elif self.is_denied():
      print("Unfortunately, we cannot approve your application at this time.")
    else:
      print(f"Received unexpected outcome: {self.outcome}")

class AlloyClient:
  def __init__(self, base_url: str, workflow_token: str, secret_key: str):
    self.base_url = base_url
    self.secret_key = secret_key
    self.workflow_token = workflow_token
    self.__EVALUATION_SUFFIX = "/v1/evaluations"


  def __get_auth_header__(self) -> dict:
    token_bytes = f"{self.workflow_token}:{self.secret_key}".encode("utf-8")
    token = base64.b64encode(token_bytes).decode("utf-8")
    return {
      "Authorization": f"Basic {token}",
      "Content-Type": "application/json"
    }


  def __make_request__(self, method: str, suffix: str, data: dict = None):
    url = f"{self.base_url}{suffix}"
    headers = self.__get_auth_header__()
    if method == "POST":
      response = requests.post(url, headers=headers, json=data)
    elif method == "GET":
      response = requests.get(url, headers=headers)
    else:
      raise ValueError(f"Invalid method: {method}")
    return response
    
    

  def create_evaluation(self, applicant: Applicant):
    try:
      response = self.__make_request__("POST", self.__EVALUATION_SUFFIX, applicant.to_json())
      response_data = response.json()
          
      if response.status_code in (200, 201):
        evaluation = AlloyEvaluation(response_data)
        evaluation.get_outcome_message()
        return evaluation
      else:
        raise AlloyError(response_data)
    except requests.exceptions.RequestException as e:
      raise AlloyError({
        'status_code': 500,
        'error': {
          'message': str(e)
        }
      })

