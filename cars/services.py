import requests


def __get_models_by_make(make):
    make = make.lower()
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{make}"

    data = requests.get(url, params={"format": "json"})
    return data.json()


def __find_model_in_api_response(response, model_name):
    for unit in response['Results']:
        model = unit['Model_Name']
        if model.lower() == model_name.lower():
            return True
    return False


def validate_make_and_model(make, model):
    models_response = __get_models_by_make(make)

    return __find_model_in_api_response(models_response, model)
