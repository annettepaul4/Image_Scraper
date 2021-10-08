import os
import requests
import io
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class ImageScraper():

    def __init__(self, chromedriver_path, image_path, query='superman', no_of_images=10, headless = False, max_res = (2000,2000)):
        #headless enables the script to run automated

        #create a new folder if the folder does not exist
        if not os.path.exists(image_path):
            print('[INFO] Creating new folder as image path does not exist')
            os.makedirs(image_path)

        #next we need to check if chromedrivers are updated or not
        while(True):
            try:
                options = Options()
                chromedriver = webdriver.Chrome(chromedriver_path, chrome_options=options)
                chromedriver.get('https://www.google.com')
                break
            except NameError:
                exit('[ERROR] Need to update chromedriver based on your chrome version.')

        self.chromedriver_path = chromedriver_path
        self.image_path = image_path
        self.max_res = max_res
        self.query = query
        self.no_of_images = no_of_images
        self.headless = headless
        self.save_as_ext = "jpg"
        self.chromedriver = chromedriver
        self.URL = 'https://www.google.com/search?q=%s&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947'%(query)

    def URLFinder(self):
        print('[INFO] Image link is being scraped. This may take few seconds.')
        image_URLs = []
        success_cnt = 0
        miss_cnt = 0
        self.chromedriver.get(self.URL)
        time.sleep(5)
        for i in range(1, self.no_of_images+1):
            try:
                #we need to first find the URL and then click it
                image_URL = self.chromedriver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img'%(str(i)))
                image_URL.click()
                miss_cnt = 0
            except Exception:
                miss_cnt+=1
                if miss_cnt > 15:
                    print('[INFO] There are no more photos to download.')
                    break
                else:
                    continue
            try:
                #now we need to try to select the image from the pop up
                time.sleep(1)
                class_names = ['n3VNCb']
                images = [self.chromedriver.find_elements_by_class_name(class_name) for class_name in class_names if len(self.chromedriver.find_elements_by_class_name(class_name)) != 0][0]
                for image in images:
                    #we need to ensure we download only those that starts with http
                    if(image.get_attribute('src')[:4].lower() in ['http']):
                        print('[INFO] %d. %s'%(success_cnt, image.get_attribute('src')))
                        image_URLs.append(image.get_attribute('src'))
                        success_cnt+=1
                        break
            except Exception:
                print('[ERROR] Unable to get access the link. Proceeding to the next one.')

            try:
                #now we need to scroll the page to load the next image
                if (success_cnt%3 == 0):
                    self.chromedriver.execute_script("window.scrollTo(0, "+str(i*60)+");")
                element = self.chromedriver.find_element_by_class_name('mye4qd')
                element.click()
                print('[INFO] Currently loading more photos.')
                time.sleep(5)
            except Exception:
                time.sleep(1)

        self.chromedriver.quit()

        print('[INFO] The google search has now ended.')
        return image_URLs

    def SaveImages(self, image_URLs):
        print('[INFO] Saving Image.')
        for i, image_URL in enumerate(image_URLs):
            try:
                queries = ''.join(e for e in self.query if e.isalnum())
                filename = '%s%s.%s'%(queries, str(i), self.save_as_ext)
                image_path = os.path.join(self.image_path, filename)
                print('[INFO] %d. Image is saved at: %s' %(i, image_path))
                image = requests.get(image_URL, timeout = 5)
                if image.status_code == 200:
                    with Image.open(io.BytesIO(image.content)) as image_from_web:
                        image_from_web.save(image_path)
                        image_resolution = image_from_web.size
                        if image_resolution != None:
                            if image_resolution[0] > self.max_res[0] or image_resolution[1] > self.max_res[1]:
                                os.remove(image_path)

                        image_from_web.close()
            except Exception as e:
                print('[ERROR] Download has failed.', e)
                pass
        print('[INFO] The download has been completed')
























