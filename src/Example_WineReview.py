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


def transform_wine_mask():
    wine_mask = np.array(Image.open(os.path.join(os.getcwd(), 'images', 'masks', 'wine_mask.png')))

    transformed_wine_mask = np.ndarray((wine_mask.shape[0], wine_mask.shape[1]), np.int32)

    for i in range(len(wine_mask)):
        transformed_wine_mask[i] = list(map(transform_format, wine_mask[i]))

    return transformed_wine_mask


# WordCloud for one review
def word_cloud_one(data):
    text = data.description[0]

    word_cloud = WordCloud().generate(text)

    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    word_cloud.to_file(os.path.join(os.getcwd(), 'images', 'outputs', '1_word_cloud.png'))


# WordCloud for one review, changing colors
def word_cloud_two(data):
    text = data.description[0]

    word_cloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(text)

    plt.figure()
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

    word_cloud.to_file(os.path.join(os.getcwd(), 'images',  'outputs', '2_word_cloud.png'))


# Combine all wine reviews
def word_cloud_three(data):
    text = " ".join(review for review in df.description)

    stopwords = set(STOPWORDS)
    stopwords.update(["drink", "now", "wine", "flavor", "flavors"])

    word_cloud = WordCloud(stopwords=stopwords, background_color="white").generate(text)

    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    word_cloud.to_file(os.path.join(os.getcwd(), 'images',  'outputs', '3_word_cloud.png'))


# With image mask
def word_cloud_forth(data):
    text = " ".join(review for review in df.description)

    stopwords = set(STOPWORDS)
    stopwords.update(["drink", "now", "wine", "flavor", "flavors"])

    word_cloud = WordCloud(background_color="white",
                           max_words=1000,
                           mask=transform_wine_mask(),
                           stopwords=stopwords,
                           contour_width=3,
                           contour_color='firebrick')

    word_cloud.generate(text)

    plt.figure(figsize=[20, 10])
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    word_cloud.to_file(os.path.join(os.getcwd(), 'images',  'outputs', '4_word_cloud.png'))


# Join all reviews of each country with flag image mask
def word_cloud_fifth(data, countries):
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
        plt.savefig(os.path.join(os.getcwd(), 'images', 'outputs',  country.lower() + '_wine.png'), format="png")
        plt.show()


if __name__ == '__main__':
    # Load in the dataframe
    df = pd.read_csv(os.path.join(os.getcwd(), 'datasets', 'winemag-data-130k-v2.csv'), index_col=0)

    # Start with one review
    word_cloud_one(df)

    # Change the maximum number of word and lighten the background
    word_cloud_two(df)

    # Combine all wine reviews
    word_cloud_three(df)

    # With image mask
    word_cloud_forth(df)

    # With flag image mask
    word_cloud_fifth(df, ["US", "Spain", "France"])

