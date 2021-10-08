import argparse
import os
from Scraper import ImageScraper

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--chromedriver_path', help='Input the chromedriver path', type=str, required=True)
parser.add_argument('-i', '--image_path', help='Input the image path', type=str,required=True)
parser.add_argument('-n', '--number_of_images', help='Number of images to download', type=int,required=True)
parser.add_argument('-q', '--queries', help='Search query in a list',  type = str,  required=True)
args = parser.parse_args()
arguments = vars(args)

if __name__ == '__main__':
    chromedriver_path = os.path.normpath(os.getcwd()+arguments['chromedriver_path'])
    image_path = os.path.normpath(os.getcwd()+arguments['image_path'])
    queries = arguments['queries'].split(', ')
    no_of_images = arguments['number_of_images']
    headless = False
    max_res = (9999,9999)
    for query in queries:
        image_scraper = ImageScraper(chromedriver_path = chromedriver_path,
                                     image_path = image_path,
                                     query = query,
                                     no_of_images= no_of_images,
                                     headless = headless,
                                     max_res = max_res)
        image_URLs = image_scraper.URLFinder()
        image_scraper.SaveImages(image_URLs)
    del image_scraper