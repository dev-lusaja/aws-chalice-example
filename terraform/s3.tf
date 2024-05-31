variable bucket_name {
  type        = string
  default     = ""
}

resource "aws_s3_bucket" "bucket" {
  bucket = var.bucket_name
}