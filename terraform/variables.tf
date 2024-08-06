variable "bq_dataset_name" {
    description = "Bigquery wine dataset"
    default = "wine_dataset"
}

variable "project_name" {
    description = "GCP project name"
    default = "dwh-terraform-gcp"
}

variable "bucket_name" {
    description = "GCP bucket name"
    default = "dwh-terraform-gcp-wine"
}

variable "location" {
    description = "GCP location name"
    default = "EU"
}