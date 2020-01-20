import requests
import logging
import sys
import hashlib
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

DEST_URL = 'https://support.apple.com/en-us/HT201222'
# DEST_URL = 'https://asrJ.com'


def garceful_exit(retry_state):
    error = retry_state.outcome.exception().__class__.__name__
    logger.error('Encountered an error: %s, failed after %s retries', error, retry_state.attempt_number)
    sys.exit(1)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(), retry_error_callback=garceful_exit)
def get_html():
    response = requests.get(DEST_URL, timeout=4)
    if response.content:
        return response.content
    else:
        logger.error('Unable to get any HTML form from destination URL')
        sys.exit(1)


def get_md5(html_form):
    md5_gen = hashlib.md5()
    md5_gen.update(html_form)
    md5_sum = md5_gen.hexdigest()
    return md5_sum


def main():
    html_form = get_html()
    md5_sum = get_md5(html_form)
    print(md5_sum)


if __name__ == '__main__':
    main()
