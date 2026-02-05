import re
import pandas as pd


def validate_field(name, field_name="Name"):
    if not name:
        return False, f"{field_name} is required"
    if not re.match(r'^[A-Za-z\s-]+$', name):
        return False, f"{field_name} should only contain letters, spaces, and hyphens"
    if len(name) < 2:
        return False, f"{field_name} should be at least 2 characters long"
    return True, ""


def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Email address appears to not be valid"
    return True, ""


def validate_phone(phone):
    pattern = r'^[+]?[0-9]+[-. ]?[0-9]{2,5}[-. ]?[0-9]{4,7}$'
    if not re.match(pattern, phone):
        return False, "The provided phone number appears to not be valid"
    return True, ""


def validate_age(age):
    try:
        age = int(age)
        if age < 0 or age > 120:
            return False, "Age must be between 0 and 120"
        return True, ""
    except ValueError:
        return False, "Please enter a valid number"


def safe_str(val):
    """Convert a value to string, returning empty string for NaN/None."""
    return str(val) if pd.notna(val) else ""


def safe_year(val):
    """Convert a value to int for year fields, returning None for NaN/None."""
    return int(val) if pd.notna(val) else None
