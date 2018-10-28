#Relational Database Service

##Import vars

variable "vpc_id"{
}
variable "ezctf_db_sn"{
}
variable "db_sg"{
}

# Provides an RDS DB subnet group resource.

resource "aws_db_subnet_group" "ezctf_sbng" {
  name                    = "ezctf_sbng"
  subnet_ids              = ["${var.ezctf_db_sn}"]

  tags {
    Name                  = "My ezctf_DB subnet group"
  }
}


## Provides an RDS instance resource. 
## A DB instance is an isolated database environment in the cloud.

resource "aws_db_instance" "ezctf_db" {
  allocated_storage       = 10
  storage_type            = "gp2"
  engine                  = "mysql"
  engine_version          = "5.7"
  instance_class          = "db.t2.micro"
  name                    = "ezctf"
  username                = "ezctf"
  password                = "${var.db_password}"
  parameter_group_name    = "default.mysql5.7"
  port                    = 3306
  db_subnet_group_name    = "${aws_db_subnet_group.ezctf_sbng.name}"
  vpc_security_group_ids  = ["${var.db_sg"]
}