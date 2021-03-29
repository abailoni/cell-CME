### Installation
- Clone the repository: `git clone https://github.com/abailoni/cell-CME.git`
- Move to the package directory: `cd cell-CME`
- To install the dependencies, you will need [miniconda](https://docs.conda.io/en/latest/miniconda.html) or [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/)
- Once you have installed conda, run the command  `conda env create --name=cellCME --file=environment.yml`
- Before to run any of the scripts, activate your new environment with `conda activate cellCME`

### Usage
- Data should be organized as follows:

```
ROOT_DATA_DIR:
    input_images:
        Place here the images with .czi or .dv formats (They can also be organized in subdirectories)
    converted_to_tif:
        Converted tif images used by ilastik will be placed here
    converted_to_jpg:
        Converted jpg images will be placed here
    resulting_segmentations:
        Final segmentation images will be placed here
```

- To convert images to tif format (accepted by ilastik):
    - Run `python scripts/convert_input_images.py --ROOT_DATA_DIR=<INSERT-YOUR-PATH-HERE>`
    - Images will be found in the `converted_to_tif` and `converted_to_jpg` subfolders
- To train ilastik classifier, see [Wiki page](https://github.com/abailoni/cell-CME/wiki/Training-ilastik-classifier)
- To plot the final segmentations:
    - Run `python scripts/plot_output_segmentation.py --ROOT_DATA_DIR=<INSERT-YOUR-PATH-HERE>`
    - Images will be found in the `resulting_segmentations` subfolder
- To be continued...  
    



