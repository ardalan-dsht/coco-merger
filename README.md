# Coco Merger

Coco Merger is a Python module designed to simplify the process of merging multiple COCO-formatted datasets. This tool is particularly useful for developers and researchers in the field of computer vision and machine learning who are looking to combine datasets for model training and evaluation.

## Features

- Easy integration into Python projects.
- Supports merging of multiple COCO dataset annotations.
- Handles the re-indexing of image and annotation IDs.
- Allows customization of COCO dataset information and licenses.

## Installation

To install Coco Merger, simply clone the repository into your project directory:

```bash
git clone https://github.com/your-username/Coco-Merger.git
```

## Usage
To use Coco Merger, you need to create an instance of the CocoMerger class and call the merge method. Here's a quick example:
```python
from coco_merger import CocoMerger
from pathlib import Path

# Define the root directory where the merged dataset will be stored
coco_root_dir = Path('/path/to/merged/dataset')

# List of paths to the COCO datasets you want to merge
paths_to_merge = [Path('/path/to/dataset1'), Path('/path/to/dataset2')]

# Initialize Coco Merger
merger = CocoMerger(coco_root_dir, paths_to_merge)

# Merge the datasets
merger.merge()
```

## Documentation
For detailed documentation on how to use Coco Merger, refer to the docstrings within the code. The module is well-commented and provides clear instructions on the functionality and usage of each method.  

## Contributing
Contributions to Coco Merger are welcome! If you have suggestions for improvements or bug fixes, please feel free to fork the repository, make your changes, and submit a pull request.  

## License
Coco Merger is released under the MIT License.  

## Contact
If you have any questions or feedback regarding Coco Merger, please open an issue in the GitHub repository, and we will get back to you as soon as possible.