class NavPlace:
    def __init__(self, data, parent_uri, title):
        """
        class to implement navPlace

        We need to get locations, look up the coords, and add them to the manifest. We also need a manifest title.

        """
        self.features = data
        self.parent_uri = parent_uri
        self.title = title
        self.all_locations = self.__get_values_and_coords()
        self.features = self.__add_navplace_features()

    @staticmethod
    def __get_values_and_coords():
        return {
            "Toronto ": [43.6532, -79.3832],
            "Montreal": [45.5017, -73.5673],
            "Ferguson, MO": [38.7442, -90.3054],
            "Chicago": [41.8781, -87.6298],
            "Oakland": [37.8044, -122.2711],
            "Knoxville, TN": [35.9606, -83.9207],
            "Washington D.C.": [38.9072, -77.0369],
            "Memphis": [35.1495, -90.0490],
            "Palestine": [31.9522, 35.2332],
            "Minneapolis": [44.9778, -93.2650],
            "Standing Rock": [45.8038, -101.8642],
            "New York City, NY": [40.7128, -74.0060],
            "Philadelphia": [39.9526, -75.1652],
            "Boston": [42.3601, -71.0589],
            "Durham": [35.9940, -78.8986],
            "Turtle Island": [36.7783, -119.4179],
            "Colombia": [4.7110, -74.0721]
        }

    def __add_navplace_features(self):
        features = []
        i = 0
        for feature in self.features:
            try:
                features.append(
                    {
                        "id": f"{self.parent_uri}notdereferenceable/feature/{i}",
                        "type": "Feature",
                        "properties": {
                            "label": {
                                "en": [
                                    f"{self.title} -- {feature}"
                                ]
                            }
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [
                                self.all_locations[feature][1],
                                self.all_locations[feature][0]
                            ]
                        }
                    }
                )
                i += 1
            except KeyError:
                print(f"Feature {feature} not found in locations. Add.")
        return features
