# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import collections
from pathlib import Path
from typing import List, Union

import fastai

# from fastai.vision import *
# from fastai.vision import get_image_files
from fastai.vision import open_image, open_mask
from fastai.vision.data import ImageDataBunch
import numpy as np
from numpy import loadtxt
import PIL
from scipy import ndimage


def load_im(
    im_or_path: Union[np.ndarray, Union[str, Path]]
) -> fastai.vision.image.Image:
    """ Load image using "open_image" function from fast.ai.

    Args:
        path: location of image to be loaded

    Return:
        Image
    """
    if isinstance(im_or_path, (str, Path)):
        im = open_image(im_or_path, convert_mode="RGB")
    else:
        im = im_or_path
    return im


def load_mask(
    mask_or_path: Union[np.ndarray, Union[str, Path]]
) -> fastai.vision.image.ImageSegment:
    """ Load mask using "open_mask" function from fast.ai.

    Args:
        path: location of mask to be loaded

    Return:
        Mask
    """
    if isinstance(mask_or_path, (str, Path)):
        mask = open_mask(mask_or_path)
    else:
        mask = mask_or_path
    return mask


def read_classes(path) -> List[str]:
    """ Compute number of pixels in each connected segment of the full dataset.

    Args:
        path: location of text file where each line is a class name

    Return:
        List of class names
    """
    classes = list(loadtxt(path, dtype=str))
    classes = [s.lower() for s in classes]
    return classes


def mask_area_sizes(data: ImageDataBunch) -> collections.defaultdict:
    """ Compute number of pixels in each connected segment of the full dataset.

    Args:
        data: databunch with images and ground truth masks

    Return:
        Sizes of all connected segments, in pixels, and for each class
    """
    areas = collections.defaultdict(list)

    # Loop over all class masks
    for mask_path in data.y.items:
        mask = np.array(PIL.Image.open(mask_path))

        # For each class, find all segments and enumerate
        for class_id in np.unique(mask):
            segments, _ = ndimage.label(
                mask == class_id, structure=[[1, 1, 1], [1, 1, 1], [1, 1, 1]]
            )

            # Loop over each segment of a given label
            for segment_id in range(1, segments.max() + 1):
                area = np.sum(segments == segment_id)
                areas[class_id].append(area)

    return areas