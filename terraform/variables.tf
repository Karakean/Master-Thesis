variable "region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "debian-ami" {
    description = "AMI of the debian image"
    type        = string
    default     = "ami-064519b8c76274859"
}
