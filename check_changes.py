import requests
import logging
import sys
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

# DEST_URL = 'https://support.apple.com/en-us/HT201222'
DEST_URL = 'https://asrJ.com'


def garceful_exit(retry_state):
    pass



@retry(stop=stop_after_attempt(3), wait=wait_exponential(), retry_error_callback=garceful_exit)
def get_html():
    response = requests.get(DEST_URL, timeout=4)
    if response.text:
        return response.text
    else:
        logger.warning('Unable to get any HTML form from destination URL')
        sys.exit(1)


if __name__ == '__main__':
    get_html()
