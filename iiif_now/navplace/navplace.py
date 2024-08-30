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
            "Colombia": [4.7110, -74.0721],
            "Red Deer, Alberta, Canada": [52.265636077067995, -113.81252288818361],
            "Faro, Portugal": [37.01406738256919, -7.933502197265626],
            "Paris, France": [48.821332549646655, 2.3730468750000004],
            "Sydney, Australia": [-33.925129700071984, 151.23779296875003],
            "Louisville, Kentucky, USA": [38.229550455326134, -85.7373046875],
            "Atlanta, GA, USA": [33.74903599710342, -84.39079285320364],
            "Ottowa, Canada": [45.39073523253725, -75.66284237176178],
            "Dortmund, Germany": [51.505323427014666, 7.470703035145997],
            "Seattle, WA, USA": [47.591346460403784, -122.28881839960815],
            "St. Paul, MN, USA": [44.95216498263645, -93.06175231587144],
            "Barcelona, Spain": [41.37062542879378, 2.1615598261356577],
            "Nairobi, Kenya": [-1.2784277536395545, 36.81518546964974],
            "Deir al-Balah, Gaza Strip, Palestine": [31.415369393408955, 34.35128688703991],
            "Kabul, Afghanistan": [34.50655670176915, 69.18640107214456],
            "London, United Kingdom": [51.47796190804837, -0.12084971308707894],
            "Brighton, United Kingdom": [50.820902742925384, -0.14059067518450208],
            "Belfast, Northern Ireland": [54.58797988632139, -5.924377511590709],
            "Milwaukee, Wisconsin, USA": [43.00062988908494, -87.93457039833069],
            "Los Angeles, California, USA": [34.03900477003338, -118.24584956288341],
            "Napoli, Italy": [40.83829458945075, 14.24823760602855],
            "Montgomery, AL, USA": [32.37068294257147, -86.29211429983378],
            "Baton Rouge, LA, USA": [30.439202087235607, -91.18103027343751],
            "New Haven, Connecticut": [41.30824499731061, -72.92312622070314],
            "Asheville, NC, USA": [35.59506483918012, -82.55212783813478],
            "Dallas, TX, USA": [32.75032260780972, -96.8115234375],
            "Munich, Germany": [48.134017189048976, 11.579589843750002],
            "Berlin, Germany": [52.49950372242746, 13.3978271484375],
            "Auckland, Aotearoa/New Zealand": [-36.86643755175846, 174.77188110351565],
            "Milan, Italy": [45.46302026511832, 9.190063476562502],
            "Edinburgh, Scotland": [55.95073768027848, -3.197021484375],
            "Chiapas, Mexico": [16.73090658973393, -92.63397216796876],
            "São Paulo, Brazil": [-23.54762199510273, -46.63009643554688],
            "Vienna, Austria": [48.201794985897344, 16.37374877929688],
            "Vancouver, BC, Canada": [49.26354786461457, -123.0842971801758],
            "Lyon, France": [45.75698431353718, 4.835357666015626]
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
                with open('errors.log', 'a') as f:
                    f.write(f'{feature}\n')
        return features
