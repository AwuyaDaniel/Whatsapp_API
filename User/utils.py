import random
import string


def generate_random_string(n):
    # define the pool of characters to choose from
    characters = string.ascii_letters + string.digits

    # generate a random string of length n using the characters pool
    return ''.join(random.choice(characters) for i in range(n))


def check_request_arguments(req, fields: list):
    # Check if all fields are added to the request
    try:
        unavailable_fields = [field for field in fields if not req.query_params.get(field)]
        if not unavailable_fields:
            return {"status": True, "unavailable_fields": unavailable_fields}
        else:
            return {"status": False, "unavailable_fields": unavailable_fields}
    except Exception as E:
        return {"status": False, "unavailable_fields": E}


def check_password(req, password, password2):
    if req.data.get(password) == req.data.get(password2):
        return True
    else:
        return False
