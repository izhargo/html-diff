import boto3

BUCKET_NAME = 'latest-html-form-apple'

s3_client = boto3.client('s3')

# client.list_objects_v2(Bucket='latest-html-form-apple').get('Content')
def init_storage():
    return s3_client.list_objects_v2(Bucket=BUCKET_NAME)['KeyCount']


def check_latest_html_form(html_dict):
    storage_init_code = init_storage()
    if storage_init_code:
        storage_success = STORAGE_FUNC[storage_init_code](html_dict)


def save_key_value(html_dict):
    storage_response = s3_client.put_object(Body=html_dict['html_form_binary'], Bucket=BUCKET_NAME,
                                            Key=html_dict['signature'])
    if storage_response == 200:
        return True
    else:
        return False


def compare_html_forms(html_dict):
    obj = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
    current_key = obj['Contents'][0]['Key']
    data = client.get_object(Bucket='latest-html-form-apple', Key='test.txt')

def too_many_forms(html_dict):
    pass


client.put_object(Body=some_binary_data, Bucket='latest-html-form-apple', Key='test_some.txt')

storage_response.get('ResponseMetadata').get('HTTPStatusCode')

STORAGE_FUNC = {
    0: save_key_value,
    1: compare_html_forms,
    2: too_many_forms
}
