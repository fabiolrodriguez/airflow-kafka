variable "aws_region" {
  description = "AWS Region"
  default = "us-east-1"
}

variable "subnet_az1" {
  description = "Subnet CIDR"
  default = "192.168.0.0/24"
}

variable "subnet_az2" {
  description = "Subnet CIDR"
  default = "192.168.1.0/24"
}

variable "subnet_az3" {
  description = "Subnet CIDR"
  default = "192.168.2.0/24"
}

variable "subnet_public_az1" {
  description = "Subnet CIDR"
  default = "192.168.10.0/24"
}

variable "subnet_public_az2" {
  description = "Subnet CIDR"
  default = "192.168.11.0/24"
}