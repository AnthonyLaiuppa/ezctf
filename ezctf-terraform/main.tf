provider "aws" {
	access_key        = "${var.aws_access_key}"
	secret_key        = "${var.aws_secret_key}"
	region            = "us-east-2"
}

terraform {
  backend "s3" {
    bucket                = "ezctf_temp_app_bucket"
    key                   = "app/ezctf/ezctf"
    region                = "US-east-2"
  }
}
module "vpc" {
	source            = "./modules/vpc"
}

module "sg" {
	source            = "./modules/sg"
	vpc_id            = "${module.vpc.vpc_id}"
}

module "ec2" {
  source                  = "./modules/ec2"
  app_sn                  = "${module.vpc.ezctf_app_sn}"
  app_sg                  = "${module.sg.ezctf_app_sg}" 

module "rds" {
  source                  = "./modules/rds"
  vpc_id                  = "${module.vpc.vpc_id}"
  db_sn                   = "${module.vpc.ezctf_db_sn}"
  db_sg                   = "${module.sg.ezctf_db_sg}"
}
