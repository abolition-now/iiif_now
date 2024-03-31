from iiif_prezi3 import Manifest, config, KeyValueString, load_bundled_extensions
import requests
import json


class ANManifest:
    # @Todo: Add navPlace
    # @Todo: Add Video Canvases
    def __init__(self, manifest_data, extensions=[]):
        self.config = config.configs['helpers.auto_fields.AutoLang'].auto_lang = "en"
        self.manifest_data = manifest_data
        self.metadata = self.__build_metadata()
        self.manifest = self.__build_manifest()
        self.extensions = load_bundled_extensions(
            extensions=extensions
        )

    def __build_manifest(self):
        manifest = Manifest(
            id=f"https://raw.githubusercontent.com/markpbaggett/static_iiif/main/manifests/abolition_now/{self.manifest_data['id']}.json",
            label=self.manifest_data['manifest_title'] if self.manifest_data['manifest_title'] != "" else "Untitled",
            metadata=self.metadata
        )
        for canvas in self.manifest_data['canvases']:
            if canvas['type'] == 'Image':
                try:
                    # @Todo: Break Bucket Identifiers Out of Code
                    canvas = manifest.make_canvas_from_iiif(
                        url=f"https://strob6zro3bzklrulaqu2545sy0odbvz.lambda-url.us-east-2.on.aws/iiif/3/{canvas['key']}",
                        id=f"https://aboltion-now-manifests.s3.us-east-2.amazonaws.com/{canvas['key']}/canvas/{canvas['sequence']}",
                        anno_id=f"https://aboltion-now-manifests.s3.us-east-2.amazonaws.com/{canvas['key']}/canvas/{canvas['sequence']}/annotation/1",
                        anno_page_id=f"https://aboltion-now-manifests.s3.us-east-2.amazonaws.com/{canvas['key']}/canvas/{canvas['sequence']}/annotation/1/page/1",
                    )
                # @Todo: Accurately Define Exception
                except:
                    print(f'Missing {canvas["key"]} in bucket.')
        x = manifest.json(indent=2)
        y = json.loads(x)
        y['@context'] = ["http://iiif.io/api/extension/navplace/context.json", "http://iiif.io/api/presentation/3/context.json"]
        # @Todo: Write Manifests in Separate Method
        # with open(f'data/new_copy/{self.metadata["key"]}.json', 'w') as outfile:
        #     outfile.write(json.dumps(y, indent=2))
        return manifest.json(indent=2)

    def __build_metadata(self):
        metadata = []
        for k, v in self.manifest_data['metadata'].items():
            metadata.append(
                KeyValueString(
                    label=k,
                    value={"en": v}
                )
            )
        return metadata


if __name__ == "__main__":
    # Note: This is all temporary until parent package is complete.
    from iiif_now.csvreader import DataReader
    # @Todo: All of this should happen elsewhere. Bring in configuration first then fix.
    reader = DataReader(
        'data/march302024.csv',
        artists_file='data/artists_codes.csv',
        metadata_file='data/new_codes.csv'
    )
    manifests = reader.build_hierarchy()
    for manifest in manifests:
        x = ANManifest(manifest, [])
        print(x.manifest)