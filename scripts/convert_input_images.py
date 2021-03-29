import os

from aicsimageio import AICSImage
from aicsimageio.writers import ome_tiff_writer, png_writer

import numpy as np
from PIL import Image
import argparse

from cmeTools.utils import check_dir_and_create

# TODO: convert .dv files

def convert_czi_files(input_data_dir, output_data_dir, output_format='.tif'):
    # Get an AICSImage object
    for (dirpath, dirnames, filenames) in os.walk(input_data_dir):
        for filename in filenames:
            if filename.endswith(".czi") and not filename.startswith("."):
                dataset_path = os.sep.join([dirpath, filename])
                img = AICSImage(dataset_path)
                numpy_data = img.get_image_data("CYX", S=0, T=0, Z=0, B=0, V=0)  # returns 6D STCZYX numpy array
                print(img.shape)  # returns tuple of dimension sizes in STCZYX order
                # zstack_t8 = img.get_image_data("CZYX", S=0, T=0)



                if numpy_data.shape[0] != 4:
                    # If one channel is missing, add an empty one to make it consistent with other images
                    assert numpy_data.shape[0] == 3
                    numpy_data = np.concatenate([numpy_data, numpy_data[[2]]], axis=0)
                    numpy_data[2] = 0

                if output_format == ".png" or output_format == ".jpg":
                    # Get rid of third channel that does not seem important for visualization purpose:
                    numpy_data = np.delete(numpy_data, [2], axis=0)
                    # Invert Blue and Red channels for better visualization:
                    # Red: cells to be segmented (originally channel 3)
                    # Green: dots (originally channel 1)
                    # Blue: cell nucleus? (originally channel 0)
                    numpy_data = numpy_data[::-1]
                    # Move channel dim to last dimension:
                    numpy_data = np.rollaxis(numpy_data, axis=0, start=3)
                    image = Image.fromarray(numpy_data)
                    image = image.convert('RGB')
                else:
                    image = Image.fromarray(np.rollaxis(numpy_data, axis=0, start=3))
                dataset_out = dataset_path.replace(".czi", output_format)
                dataset_out = dataset_out.replace(input_data_dir, output_data_dir)
                out_dir = os.path.split(dataset_out)[0]
                check_dir_and_create(out_dir)
                image.save(dataset_out)

                # dataset_out = dataset_path.replace(".czi", ".tiff")
                # with ome_tiff_writer.OmeTiffWriter(dataset_out) as writer:
                #     writer.save(img.get_image_data("CYX", S=0, T=0, Z=0))

                # png_dataset_out = dataset_path.replace(".czi", ".png")
                # with png_writer.PngWriter(png_dataset_out) as writer2:
                #     writer2.save(img.get_image_data("CYX", S=0, T=0, Z=0)[:3])



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ROOT_DATA_DIR', type=str)  # DebugExp
    args = parser.parse_args()

    ROOT_DATA_DIR = args.ROOT_DATA_DIR

    input_dir = os.path.join(ROOT_DATA_DIR, "input_images")
    assert os.path.exists(input_dir), "Directory with input images not found: {}".format(input_dir)

    # Convert images to tiff (for ilastik):
    output_dir_tif = os.path.join(ROOT_DATA_DIR, "converted_to_tif")
    convert_czi_files(input_dir, output_dir_tif, output_format='.tif')

    # Convert images to jpg (for visualization purposes):
    output_dir_png = os.path.join(ROOT_DATA_DIR, "converted_to_jpg")
    convert_czi_files(input_dir, output_dir_png, output_format='.jpg')

