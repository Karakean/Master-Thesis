variable "debian-ami" {
    description = "AMI of the debian image"
    type        = string
    default     = "ami-064519b8c76274859"
}

variable "current_ip" {
    description = "Current IP address for ingress rules"
    type        = string
}