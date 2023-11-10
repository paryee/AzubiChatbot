terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~>5.15.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "vpc" {
  cidr_block = "10.0.0.0/22"
  enable_dns_hostnames = true
  enable_dns_support = true
  tags = {
    Name = "vpc"
  }
}

resource "aws_internet_gateway" "ig" {
  vpc_id = aws_vpc.vpc.id
}

resource "aws_route_table" "public-rtb" {
  vpc_id = aws_vpc.vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.ig.id
  }

  tags = {
    Name = "public-routetable"
  }
}

resource "aws_subnet" "public" {
  vpc_id = aws_vpc.vpc.id
  availability_zone = "us-east-1a"
  map_public_ip_on_launch = true
  cidr_block = "10.0.0.0/24"
  
  tags = {
    Name = "subnet-public"
  } 
}

resource "aws_route_table_association" "public" {
  subnet_id = aws_subnet.public.id
  route_table_id = aws_route_table.public-rtb.id
}

resource "aws_subnet" "private-a" {
  vpc_id = aws_vpc.vpc.id
  availability_zone = "us-east-1a"
  cidr_block = "10.0.1.0/24"
  tags = {
    Name = "subnet-private"
  } 
}

resource "aws_subnet" "private-b" {
  vpc_id = aws_vpc.vpc.id
  availability_zone = "us-east-1b"
  cidr_block = "10.0.2.0/24"
  
  tags = {
    Name = "subnet-private"
  } 
}


resource "aws_security_group" "server" {
  vpc_id = aws_vpc.vpc.id
  name = "server-sg"

  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = [ "0.0.0.0/0" ]
  }

  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = [ "0.0.0.0/0" ]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = [ "0.0.0.0/0" ]
  }
}

resource "aws_instance" "server" {
  instance_type = "t3.micro"
  subnet_id = aws_subnet.public.id
  vpc_security_group_ids = [ aws_security_group.server.id ]
  ami = "ami-05c13eab67c5d8861"
  key_name = var.key_name

  tags = {
    Name = "server-instance"
  }
}


resource "aws_security_group" "db" {
  name = "db_security_group"
  vpc_id = aws_vpc.vpc.id
  
  ingress {
    from_port = 5432
    to_port = 5432
    protocol = "tcp"
    security_groups = [ aws_security_group.server.id ]
  }

  egress {
    from_port = "0"
    to_port = "0"
    protocol = "-1"
    cidr_blocks = [ "0.0.0.0/0" ]
  }
}

resource "aws_db_subnet_group" "db" {
  name = "db_subnet_group" 
  subnet_ids = [aws_subnet.private-a.id,aws_subnet.private-b.id]
}

resource "aws_db_instance" "db" {
  db_name = "azubichatbot"
  instance_class = "db.t3.micro"
  allocated_storage = 10
  db_subnet_group_name = aws_db_subnet_group.db.name
  engine = "postgres"
  username = var.db_username
  password = var.db_password
  vpc_security_group_ids = [ aws_security_group.db.id ]

  tags = {
    Name = "db"
  }
}

