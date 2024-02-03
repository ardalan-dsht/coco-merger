import json
import os
import shutil
from pathlib import Path
from typing import Sequence


class CocoMerger:
    """
    A class to merge multiple COCO-formatted datasets into a single dataset.

    This class facilitates the merging of COCO datasets by handling the re-indexing of image and annotation IDs,
    and allows for customization of dataset information and licenses. It is designed to support developers and
    researchers in computer vision and machine learning tasks that require combining datasets for model training
    and evaluation.

    Attributes:
        coco_root_dir (Path): The root directory where the merged dataset will be stored.
        paths_to_merge (Sequence[Path]): A list of paths to the COCO datasets to be merged.
        all_json_annotations (list): A list to store all JSON annotations from the datasets to be merged.
        new_coco_info (dict): The combined COCO dataset information.
        new_coco_license (dict): The combined COCO dataset license information.
        new_coco_categories (list): The combined list of COCO dataset categories.
        new_coco_images (list): The list of images in the merged dataset.
        new_coco_annotations (list): The list of annotations in the merged dataset.

    Methods:
        __init__(self, coco_root_dir: Path, paths_to_merge: Sequence[Path], coco_info=None, coco_license=None):
            Initializes the CocoMerger instance with the specified parameters.
        read_annotation_files(self, root_directory: Path) -> dict:
            Reads and returns the annotation JSON file from the specified directory.
        merge(self):
            Merges the datasets by re-indexing and combining images, annotations, categories, and other information.
    """

    def __init__(
        self,
        coco_root_dir: Path,
        paths_to_merge: Sequence[Path],
        coco_info=None,
        coco_license=None,
    ) -> None:
        """
        Initializes the CocoMerger instance with the specified root directory for the merged dataset,
        the paths to the datasets to be merged, and optionally, custom COCO dataset information and license.

        Parameters:
            coco_root_dir (Path): The root directory where the merged dataset will be stored.
            paths_to_merge (Sequence[Path]): A list of paths to the COCO datasets to be merged.
            coco_info (dict, optional): Custom COCO dataset information. Defaults to None.
            coco_license (dict, optional): Custom COCO dataset license information. Defaults to None.
        """
        self.coco_root_dir = coco_root_dir
        self.paths_to_merge = paths_to_merge
        self.all_json_annotations = []
        for dataset in self.paths_to_merge:
            annotations = self.read_annotaion_files(dataset)
            self.all_json_annotations.append(annotations)

        # Create a python dict which is gonna be the annotations.json file.
        # Info
        if coco_info is None:
            self.new_coco_info = self.all_json_annotations[0]["info"]
        else:
            self.new_coco_info = coco_info
        # Categories
        self.new_coco_categories = self.all_json_annotations[0]["categories"]
        # License
        if coco_license is None:
            self.new_coco_license = self.all_json_annotations[0]["license"]
        else:
            self.new_coco_license = coco_license
        # Images
        self.new_coco_images = []
        # Annotations
        self.new_coco_annotations = []

    def read_annotaion_files(self, root_directory: Path) -> dict:
        """
        Reads and returns the annotation JSON file from the specified directory.

        This method scans the given directory for a JSON file containing COCO annotations and loads it into a dictionary.

        Parameters:
            root_directory (Path): The directory containing the COCO dataset annotation file.

        Returns:
            dict: The loaded COCO dataset annotations.
        """
        for filename in os.listdir(root_directory):
            if filename.split(".")[-1] == "json":
                with open(f"{root_directory}/{filename}", "r") as json_file:
                    annotations = json.load(json_file)
                return annotations

    def merge(self) -> None:
        """
        Merges the datasets by re-indexing and combining images, annotations, categories, and other information.

        This method handles the re-indexing of image and annotation IDs, and combines the datasets into a single COCO-formatted dataset.
        """
        last_image_idx = 0
        last_annotation_idx = 0
        for idx, annotation_file in enumerate(self.all_json_annotations):
            for image in annotation_file["images"]:
                # First handle images
                image_file_format = image["file_name"].split(".")[-1]
                new_image_filename = f"{last_image_idx}.{image_file_format}"
                shutil.copy(
                    self.paths_to_merge[idx] / image["file_name"],
                    self.coco_root_dir / new_image_filename,
                )
                old_image_id = image["id"]
                image["file_name"] = new_image_filename
                image["id"] = last_image_idx
                last_image_idx += 1
                self.new_coco_images.append(image)
                # Next handle annotations
                for annotation in annotation_file["annotations"]:
                    if old_image_id == annotation["image_id"]:
                        annotation["image_id"] = image["id"]
                        annotation["id"] = last_annotation_idx
                        self.new_coco_annotations.append(annotation)
                        last_annotation_idx += 1
        new_coco = {}
        new_coco["annotations"] = self.new_coco_annotations
        new_coco["images"] = self.new_coco_images
        new_coco["info"] = self.new_coco_info
        new_coco["license"] = self.new_coco_license
        new_coco["categories"] = self.new_coco_categories
        with open(self.coco_root_dir / Path("annotations.json"), "w+") as json_file:
            json.dump(new_coco, json_file)
