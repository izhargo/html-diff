import requests
import logging
import sys
import hashlib
from storage import check_latest_html_form
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

DEST_URL = 'https://support.apple.com/en-us/HT201222'


def garceful_exit(retry_state):
    error = retry_state.outcome.exception().__class__.__name__
    logger.error('Encountered an error when getting html_form: %s, failed after %s retries',
                 error, retry_state.attempt_number)
    sys.exit(1)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(), retry_error_callback=garceful_exit)
def get_html(dest_url):
    logger.info('Getting an html form from destination url')
    response = requests.get(dest_url, timeout=4)
    if response and response.content:
        logger.info('Received an html form from destination url')
        return response
    else:
        logger.error('Unable to get any HTML form from destination URL')
        sys.exit(1)


def get_md5(html_form):
    md5_gen = hashlib.md5()
    md5_gen.update(html_form)
    md5_sum = md5_gen.hexdigest()
    return md5_sum


def create_html_dict(response, md5_sum):
    timestamp = datetime.now()
    signature = f'{timestamp.year}_{timestamp.month}_{timestamp.day}_{timestamp.hour}_{timestamp.minute}_' \
                f'{timestamp.second}_{md5_sum}.txt'
    result = {'md5': md5_sum, 'html_form_binary': response.content, 'signature': signature}
    return result


def main():
    apple_response = get_html(DEST_URL)
    md5_sum = get_md5(apple_response.content)
    html_dict = create_html_dict(apple_response, md5_sum)
    check_latest_html_form(html_dict)
    logger.info('Finished checking website. Latest html form is in storage')


if __name__ == '__main__':
    main()
