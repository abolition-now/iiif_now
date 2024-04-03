import requests
from iiif_prezi3 import ResourceItem

class Thumbnail:
    def __init__(self, image_path):
        self.image_path = image_path
        self.best_size = self.__get_best_size()
        self.full_path = f"{self.image_path}/full/{self.best_size.get('width')},{self.best_size.get('height')}/0/default.jpg"

    def __get_best_size(self):
        try:
            r = requests.get(f"{self.image_path}/info.json").json()
            return r['sizes'][-3]
        except requests.exceptions.JSONDecodeError:
            return {'width': 100, 'height': 100}

    def get(self):
        resource = ResourceItem(
            id=self.full_path,
            type="Image",
            format="image/jpeg",
            width=int(self.best_size.get('width')),
            height=int(self.best_size.get('height'))
        )
        resource.make_service(
            id=self.image_path,
            type="ImageService3",
            profile="level2"
        )
        return [resource]

    def __str__(self):
        return str(self.get())
