resource "aws_vpc" "vpc-msk-mwaa" {
  cidr_block = "192.168.0.0/22"
}

data "aws_availability_zones" "azs-msk-mwaa" {
  state = "available"
}

resource "aws_subnet" "subnet_az1" {
  availability_zone = data.aws_availability_zones.azs-msk-mwaa.names[0]
  cidr_block        = var.subnet_az1
  vpc_id            = aws_vpc.vpc-msk-mwaa.id
}

resource "aws_subnet" "subnet_az2" {
  availability_zone = data.aws_availability_zones.azs-msk-mwaa.names[1]
  cidr_block        = var.subnet_az2
  vpc_id            = aws_vpc.vpc-msk-mwaa.id
}

resource "aws_subnet" "subnet_az3" {
  availability_zone = data.aws_availability_zones.azs-msk-mwaa.names[2]
  cidr_block        = var.subnet_az3
  vpc_id            = aws_vpc.vpc-msk-mwaa.id
}

# // Create Internet Gateway
# resource "aws_internet_gateway" "igw" {
#   vpc_id = aws_vpc.vpc-msk-mwaa.id
# }

# // Create Subnet
# resource "aws_subnet" "subnet_public_az1" {
#   vpc_id = aws_vpc.vpc-msk-mwaa.id
#   cidr_block = var.subnet_public_az1
#   map_public_ip_on_launch = "true"
#   availability_zone = data.aws_availability_zones.azs-msk-mwaa.names[1]
# }

# resource "aws_subnet" "subnet_public_az2" {
#   vpc_id = aws_vpc.vpc-msk-mwaa.id
#   cidr_block = var.subnet_public_az2
#   map_public_ip_on_launch = "true"
#   availability_zone = data.aws_availability_zones.azs-msk-mwaa.names[2]
# }

# // Create Route table
# resource "aws_route_table" "rtb_public" {
#   vpc_id = aws_vpc.vpc-msk-mwaa.id
# route {
#       cidr_block = "0.0.0.0/0"
#       gateway_id = aws_internet_gateway.igw.id
#   }
# }

# resource "aws_route_table_association" "rta_subnet_public1" {
#   subnet_id      = aws_subnet.subnet_public_az1.id
#   route_table_id = aws_route_table.rtb_public.id
# }

# resource "aws_route_table_association" "rta_subnet_public2" {
#   subnet_id      = aws_subnet.subnet_public_az2.id
#   route_table_id = aws_route_table.rtb_public.id
# }