#ec2


##Import
variable "app_sn"{
}
variable "app_sg"{
}


##Provides a xenial ami

data "aws_ami" "ubuntu" {
  most_recent                 = true

  filter {
    name                      = "name"
    values                    = ["ubuntu/images/hvm-ssd/ubuntu-xenial-16.04-amd64-server-*"]
  }

  filter {
    name                      = "virtualization-type"
    values                    = ["hvm"]
  }

  owners                      = ["099720109477"] # Canonical
}

##Provides an EC2 instance resource
resource "aws_instance" "ezctf_app_01" {
  ami                         = "${data.aws_ami.ubuntu.id}"
  key_name                    = "ezctf"
  subnet_id                   = "${var.ezctf_app_sn}"
  private_ip                  = ""
  instance_type               = "t2.micro"
  vpc_security_group_ids      = ["${var.ezctf_app_sg}"]
  associate_public_ip_address = "true"

  tags {
    Name                      = "ezctf"
    Type                      = "app"
    id                        = "1"
  }
  root_block_device {
    volume_size               = 12
    volume_type               = "gp2"
    iops                      = 100
  }
 
}

output "ezctf_app_01_id"{
  value                       = "${aws_instance.ezctf_app_01.id}"
}

