import boto3

BUCKET_NAME = 'latest-html-form-apple'

s3 = boto3.client('s3')


def init_storage():
    return s3.list_objects_v2(Bucket=BUCKET_NAME).get('KeyCount')



def check_latest_html_form(html_dict):
    result_code = init_storage()
    if result_code:
        STORAGE_FUNC[result_code](html_dict)


def save_key_value(html_dict):
    pass


def compare_html_forms(html_dict):
    pass


def too_many_forms(html_dict):
    pass


STORAGE_FUNC = {
    0: save_key_value,
    1: compare_html_forms,
    2: too_many_forms
}
