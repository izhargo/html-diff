import logging
import boto3

BUCKET_NAME = 'latest-html-form-apple'

s3_client = boto3.client('s3')

logger = logging.getLogger(__name__)


class StorageError(Exception):
    pass


def check_response(response):
    if 200 <= response < 300:
        return True
    else:
        return False


def get_key_count():
    return s3_client.list_objects_v2(Bucket=BUCKET_NAME)['KeyCount']


def check_latest_html_form(html_dict):
    initial_num_count = get_key_count()
    if initial_num_count:
        storage_success = STORAGE_FUNC[initial_num_count](html_dict)
    if not storage_success:
        raise StorageError('Unable to preform storage action')

def save_key_value(html_dict):
    storage_response = s3_client.put_object(Body=html_dict['html_form_binary'], Bucket=BUCKET_NAME,
                                            Key=html_dict['signature'])
    response = storage_response['ResponseMetadata']['HTTPStatusCode']
    return check_response(response)


def delete_current_key(key):
    storage_response = s3_client.delete_object(Bucket=BUCKET_NAME, Key=key)
    response = storage_response['ResponseMetadata']['HTTPStatusCode']
    return check_response(response)


def compare_html_forms(html_dict):
    logger.info('Start comparing existing html form to new form')
    result = True
    obj = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    current_key = obj['Contents'][0]['Key']
    logger.info('Getting existing html from storage')
    data = s3_client.get_object(Bucket=BUCKET_NAME, Key=current_key)
    binary_content = data['Body'].read()
    if html_dict['html_form_binary'] != binary_content:
        logger.info('Found a new html form. Updating storage')
        deletion_success = delete_current_key(current_key)
        if deletion_success:
            logger.info('Deletion of previous html form completed. New form is saved')
            result = save_key_value(html_dict)
        else:
            result = False
    return result


STORAGE_FUNC = {
    0: save_key_value,
    1: compare_html_forms
}
