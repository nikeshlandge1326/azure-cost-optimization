variable "resource_group_name" {
  default = "billing-optimization-rg"
}

variable "location" {
  default = "East US"
}

variable "cosmosdb_account_name" {
  default = "billingcosmos"
}

variable "storage_account_name" {
  default = "billingstorage"
}

variable "function_app_name" {
  default = "billing-archive-func"
}

