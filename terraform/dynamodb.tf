variable "table_name" {
    type        = string
    default     = ""
}

resource "aws_dynamodb_table" "table" {
  name           = var.table_name
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "uid"
  range_key      = "create_at"

  attribute {
    name = "uid"
    type = "S"
  }

  attribute {
    name = "create_at"
    type = "S"
  }
}