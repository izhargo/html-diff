import logging
import boto3

BUCKET_NAME = 'latest-html-form-apple'

s3_client = boto3.client('s3')

logger = logging.getLogger(__name__)


class StorageError(Exception):
    pass


def check_response(status_code):
    if 200 <= status_code < 300:
        return
    else:
        raise StorageError('Unable to preform storage action')


def get_key_count():
    return s3_client.list_objects_v2(Bucket=BUCKET_NAME)['KeyCount']


def check_latest_html_form(html_dict):
    initial_num_count = get_key_count()
    if initial_num_count:
        STORAGE_FUNC[initial_num_count](html_dict)


def save_key_value(html_dict):
    storage_response = s3_client.put_object(Body=html_dict['html_form_binary'], Bucket=BUCKET_NAME,
                                            Key=html_dict['signature'])
    status_code = storage_response['ResponseMetadata']['HTTPStatusCode']
    check_response(status_code)


def delete_current_key(key):
    storage_response = s3_client.delete_object(Bucket=BUCKET_NAME, Key=key)
    status_code = storage_response['ResponseMetadata']['HTTPStatusCode']
    check_response(status_code)


def compare_html_forms(html_dict):
    logger.info('Start comparing existing html form to new form')
    obj = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    current_key = obj['Contents'][0]['Key']
    logger.info('Getting existing html from storage')
    data = s3_client.get_object(Bucket=BUCKET_NAME, Key=current_key)
    binary_content = data['Body'].read()
    if html_dict['html_form_binary'] != binary_content:
        logger.info('Found a new html form. Updating storage')
        delete_current_key(current_key)
        logger.info('Deletion of previous html form completed. New form is saved')
        save_key_value(html_dict)
    else:
        logger.info('No changes in html form')
        return


STORAGE_FUNC = {
    0: save_key_value,
    1: compare_html_forms
}
