terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.12.0"
    }
  }
}

provider "google" {
  credentials = "./keys/de-template-224954cb7b70.json"
  project = "de-template"
  region  = "us-central1"
}


resource "google_storage_bucket" "template-bucket" {
  name          = "de-template-bucket-woojin"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}