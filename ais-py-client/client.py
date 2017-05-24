import json

import requests

class AISClient(object):

    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def get(self, endpoint, query, params = None):
        if params is None:
            params = {}
        if self.api_key:
            params["gatekeeperKey"] = self.api_key
        response = requests.get("{}{}/{}".format(self.base_url, endpoint, query), params=params)
        return response.json()

    def search(self, query, params = None):
        return self.get("search", query, params)

    def account(self, opa_number, params = None):
        return self.get("account", opa_number, params)

    def addresses(self, query, params = None):
        return self.get("addresses", query, params)

    def block(self, query, params = None):
        return self.get("block", query, params)

    def dor_parcel(self, regmap_id, params = None):
        return self.get("dor_parcel", regmap_id, params)

    def intersection(self, intersection, params = None):
        return self.get("intersection", intersection, params)

    def owner(self, owner, params = None):
        return self.get("owner", owner, params)

    def pwd_parcel(self, pwd_parcel, params = None):
        return self.get("pwd_parcel", pwd_parcel, params)

    def reverse_geocode(self, coordinates, params = None):
        return self.get("reverse_geocode", coordinates, params)

    def service_areas(self, query, params = None):
        return self.get("service_areas", query, params)

    def batch_search(self, rows, query_column_names, add_or_update_column_relations, remove_column_names, params = None):
        errors = []
        for row in rows:
            for query_column_name in query_column_names:
                result = self.search(row[query_column_name], params)
                try:
                    feature = result["features"][0]
                    break
                except:
                    pass
            if not feature:
                errors.append(row[query_column_name])
                continue
            properties = feature["properties"]
            geometry = feature["geometry"]
            for ais_name, column_name in add_or_update_column_relations.iteritems():
                if ais_name == "long":
                    row[column_name] = geometry["coordinates"][0]
                elif ais_name == "lat":
                    row[column_name] = geometry["coordinates"][1]
                else:
                    row[column_name] = properties[ais_name]
            for column_name in remove_column_names:
                del row[column_name]

        return rows, errors
