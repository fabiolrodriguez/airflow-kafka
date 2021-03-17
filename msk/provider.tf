terraform {
  backend "remote" {
    organization = "testecorpfabio"

    workspaces {
      name = "airflow"
    }
  }
}