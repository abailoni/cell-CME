import os

from aicsimageio import AICSImage
from aicsimageio.writers import ome_tiff_writer, png_writer

import numpy as np
from PIL import Image
import argparse

from cmeTools.utils import check_dir_and_create, readHDF5
from cmeTools.vis_utils import plot_segm
from matplotlib import pyplot as plt

plt.style.use('dark_background')


def plot_object_segmentations(tif_images_dir, jpg_images_dir, output_dir_segmentations):
    # Get an AICSImage object
    for (dirpath, dirnames, filenames) in os.walk(tif_images_dir):
        for filename in filenames:
            if filename.endswith("Object Identities.h5") and not filename.startswith("."):
                segm_path = os.sep.join([dirpath, filename])
                segm = readHDF5(segm_path, "exported_data")

                # Deduce path associated jpg image:
                jpg_path = segm_path.replace(tif_images_dir, jpg_images_dir)
                jpg_path = jpg_path.replace("_Object Identities.h5", ".jpg")
                jpg_image = plt.imread(jpg_path)

                # Output_path:
                out_path = jpg_path.replace(jpg_images_dir, output_dir_segmentations)
                out_dir = os.path.split(out_path)[0]
                check_dir_and_create(out_dir)

                # Plot object instances overlayed with original image (for visualization):
                f, ax = plt.subplots(ncols=1, nrows=1,
                                     figsize=(15,15))
                for a in f.get_axes():
                    a.axis('off')
                plot_segm(ax, segm[...,0], background=jpg_image, mask_value=0, alpha_labels=1, alpha_background=0.5)

                plt.subplots_adjust(wspace=0, hspace=0)
                plt.tight_layout()
                f.savefig(out_path)
                plt.close(f)

                # Now plot only object instances (for online labelling?):
                out_path = out_path.replace(".jpg", "_only_object_instances.jpg")
                f, ax = plt.subplots(ncols=1, nrows=1,
                                     figsize=(15,15))
                for a in f.get_axes():
                    a.axis('off')
                plot_segm(ax, segm[...,0], mask_value=0, alpha_labels=1)
                plt.subplots_adjust(wspace=0, hspace=0)
                plt.tight_layout()
                f.savefig(out_path)
                plt.close(f)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ROOT_DATA_DIR', type=str)  # DebugExp
    args = parser.parse_args()

    ROOT_DATA_DIR = args.ROOT_DATA_DIR

    tif_images_dir = os.path.join(ROOT_DATA_DIR, "converted_to_tif")
    jpg_images_dir = os.path.join(ROOT_DATA_DIR, "converted_to_jpg")
    assert os.path.exists(tif_images_dir)
    assert os.path.exists(jpg_images_dir)

    # Convert images to tiff (for ilastik):
    output_dir_segmentations = os.path.join(ROOT_DATA_DIR, "resulting_segmentations")
    plot_object_segmentations(tif_images_dir, jpg_images_dir, output_dir_segmentations)

