terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 2.8"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

module "chalice_app" {
  source            = "./terraform"
  bucket_name       = "chalice-lab-koandina-bucket"
  topic_bus_name    = "chalice-lab-koandina-topic"
  topic_email_name  = "chalice-lab-koandina-topic_email"
  table_name        = "chalice-lab-koandina-table"
}