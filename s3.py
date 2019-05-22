import boto3
import config


def transfer_s3():
    """This utility grabs the three data files from S3 and copies them to the user's S3 bucket"""
    s3 = boto3.resource('s3')

    copy_source_1 = {
        'Bucket': 'kupebaseball',
        'Key': 'model_data'}

    copy_source_2 = {
        'Bucket': 'kupebaseball',
        'Key': 'predictions.csv'}

    copy_source_3 = {
        'Bucket': 'kupebaseball',
        'Key': 'results.csv'}

    s3.meta.client.copy(copy_source_1, config.DEST_BUCKET, config.DEST_KEY_1)
    s3.meta.client.copy(copy_source_2, config.DEST_BUCKET, config.DEST_KEY_2)
    s3.meta.client.copy(copy_source_3, config.DEST_BUCKET, config.DEST_KEY_3)


if __name__ == "__main__":
    transfer_s3()
