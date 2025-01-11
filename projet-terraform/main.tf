provider "aws" {
  region                      = "us-east-1"
  profile                     = "localstack"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  endpoints {
    s3        = "http://localhost:4510"  # Utilisation du port configuré pour S3
    dynamodb  = "http://localhost:4510"  # Même chose pour DynamoDB
  }
}

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}


# Créer une table DynamoDB
resource "aws_dynamodb_table" "my_table1" {
  name           = "my-test-table"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "ID"
  attribute {
    name = "ID"
    type = "S"
  }
}
