import boto3
from botocore.exceptions import ClientError


def create_books_table():
    dynamodb = boto3.resource("dynamodb", region_name="sa-east-1")
    table_name = "books"

    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "isbn", "KeyType": "HASH"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "isbn", "AttributeType": "S"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        table.wait_until_exists()
        print(f"Table {table_name} created successfully!")
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            print(f"Table {table_name} already exists.")
        else:
            raise


if __name__ == "__main__":
    create_books_table()
