from iiif_prezi3 import Manifest, config, KeyValueString, load_bundled_extensions, AnnotationPage, Annotation, ResourceItem
import requests
import json
from iiif_now.homepage import HomePage
from iiif_now.navplace import NavPlace
from iiif_now.study_guide import StudyGuide
from iiif_now.thumbnail import Thumbnail


class ANManifest:
    def __init__(
            self,
            manifest_data,
            image_server_path="https://strob6zro3bzklrulaqu2545sy0odbvz.lambda-url.us-east-2.on.aws/iiif/3/",
            video_location="https://digital.lib.utk.edu/static/",
            manifest_bucket="https://raw.githubusercontent.com/markpbaggett/static_iiif/main/manifests/abolition_now/",
            extensions=[]
    ):
        self.config = config.configs['helpers.auto_fields.AutoLang'].auto_lang = "en"
        self.image_server_path = image_server_path
        self.manifest_bucket = manifest_bucket
        self.video_location = video_location
        self.manifest_data = manifest_data
        self.metadata = self.__build_metadata(manifest_data['metadata'])
        self.features = self.__find_features()
        self.manifest = self.__build_manifest()
        self.extensions = load_bundled_extensions(
            extensions=extensions
        )

    def __build_manifest(self):
        # @Todo: Clean up this method.  It's a mess and doing too much.
        homepage = HomePage(
            self.manifest_data['manifest_title'] if self.manifest_data['manifest_title'] != "" else "Untitled"
        ).body
        rendering = StudyGuide(self.manifest_data['metadata']['Artist']).body
        rights = "http://rightsstatements.org/vocab/InC/1.0/"
        if self.features:
            navplace_data = NavPlace(
                self.features,
                self.manifest_bucket,
                self.manifest_data['manifest_title'] if self.manifest_data['manifest_title'] != "" else "Untitled"
            ).features
            manifest = Manifest(
                id=f"{self.manifest_bucket}{self.manifest_data['id']}.json",
                label=self.manifest_data['manifest_title'] if self.manifest_data['manifest_title'] != "" else "Untitled",
                metadata=self.metadata,
                navPlace={"features": navplace_data},
                homepage=[homepage],
                rights=rights,
                rendering=rendering
            )
        else:
            manifest = Manifest(
                id=f"{self.manifest_bucket}{self.manifest_data['id']}.json",
                label=self.manifest_data['manifest_title'] if self.manifest_data[
                                                                  'manifest_title'] != "" else "Untitled",
                metadata=self.metadata,
                homepage=[homepage],
                rights=rights,
                rendering=rendering
            )
        for canvas in self.manifest_data['canvases']:
            thumbnail = Thumbnail(f"{self.image_server_path}{canvas['thumbnail']}").get()
            if canvas['type'] == 'Image':
                try:
                    # @Todo: Protect anno page and annotation
                    manifest.make_canvas_from_iiif(
                        url=f"{self.image_server_path}{canvas['key']}",
                        label=canvas['label'] if canvas['label'] != "" else "Untitled",
                        id=f"{self.manifest_bucket}{canvas['key']}/canvas/{canvas['sequence']}",
                        anno_id=f"{self.manifest_bucket}{canvas['key']}/canvas/{canvas['sequence']}/annotation/1",
                        anno_page_id=f"{self.manifest_bucket}{canvas['key']}/canvas/{canvas['sequence']}/annotation/1/page/1",
                        thumbnail=thumbnail,
                        metadata=self.__build_metadata(canvas.get('metadata'))
                    )
                except requests.HTTPError as e:
                    print(f'{e}. Missing file in bucket or other image server problem.')
            elif canvas['type'] == 'Video':
                vid_canvas = manifest.make_canvas(
                    id=f"{self.manifest_bucket}{canvas['key']}/canvas/{canvas['sequence']}",
                    label=canvas['label'] if canvas['label'] != "" else "Untitled",
                    thumbnail=thumbnail,
                    metadata=self.__build_metadata(canvas.get('metadata'))
                )
                details = self.__create_video_canvas(
                    canvas=vid_canvas,
                    canvas_data= canvas
                )
                vid_canvas.set_hwd(**details[1])
                vid_canvas.add_item(details[0])
        x = manifest.json(indent=2)
        manifest_as_json = json.loads(x)
        manifest_as_json['@context'] = ["http://iiif.io/api/extension/navplace/context.json", "http://iiif.io/api/presentation/3/context.json"]
        return manifest_as_json

    def __find_features(self):
        all_features = []
        for k, v in self.manifest_data['metadata'].items():
            if k == 'Geography':
                for feature in v:
                    all_features.append(feature)
        return all_features

    @staticmethod
    def __build_metadata(metadata_values):
        metadata = []
        for k, v in metadata_values.items():
            metadata.append(
                KeyValueString(
                    label=k,
                    value={"en": v}
                )
            )
        if not metadata:
            metadata.append(
                KeyValueString(
                    label="Missing metadata?",
                    value={"en": ["Yes"]}
                )
            )
        return metadata

    def write(self, path):
        with open(f'{path}/{self.manifest_data["id"]}.json', 'w') as outfile:
            outfile.write(
                json.dumps(
                    self.manifest, indent=2)
            )

    def __create_video_canvas(self, canvas, canvas_data):
        anno_body = ResourceItem(
            id=f"{self.video_location}{canvas_data['key']}",
            type="Video",
            format="video/mp4"
        )
        anno_page = AnnotationPage(
            id=f"{self.manifest_bucket}{canvas_data['key']}/canvas/{canvas_data['sequence']}/annotation/1/page/1"
        )
        anno = Annotation(
            id=f"{self.manifest_bucket}{canvas_data['key']}/canvas/{canvas_data['sequence']}/annotation/1",
            motivation="painting",
            body=anno_body,
            target=canvas.id
        )
        hwd = {"height": 360, "width": 480, "duration": canvas_data['duration']}
        anno_body.set_hwd(**hwd)
        anno_page.add_item(anno)
        return anno_page, hwd
