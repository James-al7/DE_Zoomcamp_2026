variable "credentials" {
  description = "Path to the credentials file"
  default     = "./keys/my-cred.json"
}


variable "project_id" {
  description = "The GCP project ID"
  default     = "de-terraform-485406"
}

variable "location" {
  description = "The Project Location"
  default     = "US"
}

variable "region" {
  description = "The GCP region"
  default     = "us-central1"
}

variable "bq_dataset_name" {
  description = "My first bigquery dataset"
  default     = "terra_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage bucket name"
  default     = "de-terraform-485406-demo-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage class"
  default     = "STANDARD"
}
