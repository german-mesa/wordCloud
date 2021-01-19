#
# As described here:
# https://www.datacamp.com/community/tutorials/wordcloud-python
#

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


def transform_format(val):
    if val == 0:
        return 255
    else:
        return val


def transform_mask(mask_name):
    mask = np.array(Image.open(os.path.join(os.getcwd(), 'images', 'masks', mask_name)))

    transformed_wine_mask = np.ndarray((mask.shape[0], mask.shape[1]), np.int32)

    for i in range(len(mask)):
        transformed_wine_mask[i] = list(map(transform_format, mask[i]))

    return transformed_wine_mask


def word_cloud_profile(data):
    text = data.description[0]

    word_cloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)

    plt.figure()
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

    word_cloud.to_file(os.path.join(os.getcwd(), 'images', 'outputs', 'word_cloud_profile.png'))


def word_cloud_profile_mask(data, mask_name):
    text = " ".join(review for review in data.description)

    stopwords = set(STOPWORDS)
    stopwords.update(["drink", "now", "wine", "flavor", "flavors"])

    word_cloud = WordCloud(background_color="white",
                           max_words=1000,
                           mask=transform_mask(mask_name),
                           stopwords=stopwords,
                           contour_width=3,
                           contour_color='firebrick')

    word_cloud.generate(text)

    plt.figure(figsize=[20, 10])
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    word_cloud.to_file(os.path.join(os.getcwd(), 'images', 'outputs', 'word_cloud_profile_mask.png'))


def word_cloud_profile_flag(data, countries):
    for country in countries:
        text = " ".join(review for review in data[data["country"] == country].description)

        stopwords = set(STOPWORDS)
        stopwords.update(["drink", "now", "wine", "flavor", "flavors"])

        image = Image.open(os.path.join(os.getcwd(), 'images', 'masks', country.lower() + '.png'))
        image_rgb = image.convert('RGB')

        mask = np.array(image_rgb)
        word_cloud = WordCloud(stopwords=stopwords,
                               background_color="white",
                               mode="RGBA",
                               max_words=1000,
                               mask=mask).generate(text)

        # create coloring from image
        image_colors = ImageColorGenerator(mask)

        plt.figure(figsize=[7, 7])
        plt.imshow(word_cloud.recolor(color_func=image_colors), interpolation="bilinear")
        plt.axis("off")
        plt.savefig(os.path.join(os.getcwd(), 'images', 'outputs', country.lower() + '_profile.png'), format="png")
        plt.show()


if __name__ == '__main__':
    # Load in the dataframe
    df = pd.read_csv(os.path.join(os.getcwd(), 'datasets', 'profile.csv'), index_col=0)

    # Start with one review
    word_cloud_profile(df)

    # With flag image mask
    # word_cloud_profile_flag(df, ["Spain", "Europe"])
