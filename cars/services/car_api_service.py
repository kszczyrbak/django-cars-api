import requests


class CarVPICApiService:

    @staticmethod
    def get_models_by_make(make):
        make = make.lower()
        url = f"https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{make}"

        data = requests.get(url, params={"format": "json"})
        return data.json()
