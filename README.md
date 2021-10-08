# Scrape Images from Google 

## Installations & Checks needed

This code uses the following packages:
1. Selenium 
2. PIL
3. OS
4. Request
5. Io
6. Time

You need to ensure that the chromedriver's version is complementary to the version of Chrome you are on. 

## About the program

The code uses the following parameters

1. Chromedriver_path is the path of the chromedriver 
2. Image_path is where you want the images to be saved 
3. Queries should be a single query or multiple queries separated by ",". Eg: "Iron man, Hulk" will search for Iron man as the first query and Hulk as the second one 
4. No_of_images is the number of images you would like to download 

The following parameters are not available for change from the argument parser. If you want to make any changes to the parameters below you need to head to the driver code to make changes. 
1. Max res is the maximum resolution allowed for the relevant images to be downloaded

## How to run the program
```
python main.py -c "<chromedriver-path>" -i "<image-path"> -n <no-of-images-to-download> -q "query/queries"
```
Example:
```
python main.py -c '\\webdriver\\chromedriver.exe' -i '\\Images' -n 10 -q "Thor Ragnarok, Hulk"
```
