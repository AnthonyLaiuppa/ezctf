#Security Group

##Import

variable "vpc_id"{
}

## App Security Group

resource "aws_security_group" "ezctf_app_sg" {
  name            = "ezctf_app_sg"
  descrition      = "ezctf_app_sg"
  vpc_id          = "${var.vpc_id}"

  ingress {
    from_port     = 22
    to_port       = 22
    protocol      = "tcp"
    cidr_blocks   = [""]
  }

  ingress {
    from_port     = 80
    to_port       = 80
    protocol      = "tcp"
    cidr_blocks   = [""]
  }

  ingress {
    from_port     = 443
    to_port       = 433
    protocol      = "tcp"
    cidr_blocks   = [""]
  }

  egress {
    from_port     = 0
    to_port       = 0
    protocol      = "-1"
    cidr_blocks   = ["0.0.0.0/0"]
  }

  tags {
    Name = "ezctf_app_sg"
  }
}

output "ezctf_app_sg" {
  value = "${aws_security_group.ezctf_app_sg.id}"
}


## DB Security Group

resource "aws_security_group" "ezctf_db_sg" {
  name            = "ezctf_db_sg"
  descrition      = "ezctf_dbp_sg"
  vpc_id          = "${var.vpc_id}"

  ingress {
    from_port     = 3306
    to_port       = 3306
    protocol      = "tcp"
    cidr_blocks   = [""]
  }

  egress {
    from_port     = 0
    to_port       = 0
    protocol      = "-1"
    cidr_blocks   = ["0.0.0.0/0"]
  }

  tags {
    Name = "ezctf_db_sg"
  }
}

output "ezctf_db_sg" {
  value = "${aws_security_group.ezctf_db_sg.id}"
}
