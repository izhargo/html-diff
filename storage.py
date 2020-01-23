import boto3

BUCKET_NAME = 'latest-html-form-apple'

s3_client = boto3.client('s3')


def check_response(response):
    if 200 <= response < 300:
        return True
    else:
        return False


def init_storage():
    return s3_client.list_objects_v2(Bucket=BUCKET_NAME)['KeyCount']


def check_latest_html_form(html_dict):
    storage_init_code = init_storage()
    if storage_init_code:
        storage_success = STORAGE_FUNC[storage_init_code](html_dict)


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
    result = True
    obj = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    current_key = obj['Contents'][0]['Key']
    data = client.get_object(Bucket=BUCKET_NAME, Key=current_key)
    binary_content = data['Body'].read()
    if html_dict['html_form_binary'] != binary_content:
        deletion_success = delete_current_key(current_key)
        if deletion_success:
            result = save_key_value(html_dict)
        else:
            result = False
    return result


STORAGE_FUNC = {
    0: save_key_value,
    1: compare_html_forms
}
