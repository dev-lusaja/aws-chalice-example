variable topic_bus_name {
  type        = string
  default     = ""
}

variable topic_email_name {
  type        = string
  default     = ""
}

resource "aws_sns_topic" "topic_bus" {
  name = var.topic_bus_name
}

resource "aws_sns_topic" "topic_email" {
  name = var.topic_email_name
}