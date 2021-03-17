terraform {
  backend "remote" {
    organization = "testecorpfabio"

    workspaces {
      name = "airflow"
    }
  }
}

provider "aws" {
 region = var.aws_region
}