#VPC
resource "aws_vpc" "ezctf_vpc" {
	cidr_block           = "10.10.0.0/20"
	instance_tenancy     = "default"
	enable_dns_hostnames = "true"

	tags{
	  Name               = "ezctf_vpc"
	}
}

output "vpc_id"{
	value = "${aws_vpc.ezctf_vpc.id}"
}


# App Subnet
resource "aws_subnet" "ezctf_app_sn" {
	vpc_id = "${aws_vpc.ezctf_vpc.id}"
	cidr_block = "10.10.1.0/24"

	tags = {
	  Name = "ezctf_app_sn"
	}
}

output "ezctf_app_sn"{
	value = "${aws_vpc.ezctf_app_sn.id}"
}


#DB Subnet
resource "aws_subnet" "ezctf_db_sn" {
	vpc_id = "${aws_vpc.ezctf_vpc.id}"
	cidr_block = "10.10.2.0/24"

	tags = {
	  Name = "ezctf_db_sn"
	}
}

output "ezctf_db_sn"{
	value = "${aws_vpc.ezctf_db_sn.id}"
}
