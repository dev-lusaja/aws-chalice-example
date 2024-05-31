build-chalice:
	@chalice package --pkg-format terraform ./terraform

deploy: build-chalice
	@terraform init
	@terraform plan
	@terraform apply -auto-approve

destroy:
	@terraform destroy -auto-approve
	@rm -rf .chalice/deployments/*
	@rm -rf .terraform
	@rm -f terraform.tfstate.backup
	@rm -f terraform.tfstate
	@rm -f .terraform.lock.hcl
	@rm -f terraform/chalice.tf.json
	@rm -f terraform/deployment.zip
	@rm -f .terraform.tfstate.lock.info

local:
	@chalice local --stage local

test:
	@py.test tests/