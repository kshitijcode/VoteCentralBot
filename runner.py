import argparse
import logging
import os
import urllib.request
import uuid
import time
import pickle
from itertools import repeat
from multiprocessing import Pool

import logger
from browserHelper import BrowserHelper
from captcha2upload import CaptchaUpload


def driver_init(voteLink):
    driver = BrowserHelper.get_browser()
    driver.delete_all_cookies()
    driver.get(voteLink)
    driver.implicitly_wait(30)
    return driver


def upvote(voteNumber, voteLink, captchaToken):
    try:
        logger.log_text(f"Pushing Vote {voteNumber + 1}")
        driver = driver_init(voteLink)
        logger.log_text(f"Solving Captcha for vote {voteNumber + 1}")
        logging.getLogger().setLevel(logging.INFO)
        captcha = CaptchaUpload(captchaToken, log=logging)
        logger.log_text("Fetching captcha image from page")
        images = driver.find_elements_by_css_selector("img[border='0']")
        src = ""
        for image in images:
            if 'button' in image.get_attribute('src'):
                src = image.get_attribute('src')
                print(src)
                break
        logger.log_text("Generating UUID for captcha image")
        id = uuid.uuid1()
        logger.log_text("Saving captcha image")
        urllib.request.urlretrieve(src, f"captcha{id}.png")
        result = captcha.solve(f"captcha{id}.png")
        logger.log_text(f"Entering solved captcha result {result}")
        driver.find_element_by_name('confckno').click()
        driver.find_element_by_name('confckno').send_keys(result)
        driver.find_element_by_css_selector("input[type='submit']").click()
    except Exception as e:
        logger.log_header(e)
    finally:
        try:
            os.remove(f"captcha{id}.png")
            driver.quit()
        except Exception as e:
            logger.log_header(e)


if __name__ == '__main__':
    logger.log_header('STARTING UPVOTER')
    parser = argparse.ArgumentParser(description='Enter the values to the Runner')
    parser.add_argument('--voteLink', help='Enter the voteLink', required=True)
    parser.add_argument('--captchaToken', help='Enter the captcha Token ', required=True)
    parser.add_argument('--numberOfVotes', help='Enter the number of Votes you want to push.', required=True)

    args = parser.parse_args()

    voteLink = args.voteLink
    numberOfVotes = args.numberOfVotes
    captchaToken = args.captchaToken

    with Pool() as pool:
        pool.starmap(upvote, zip(range(0, int(numberOfVotes)), repeat(voteLink), repeat(captchaToken)))

    logger.log_header("OPERATION COMPLETED")
