terraform {
  required_version = ">= 1.5"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_network" "saas_network" {
  name = "saas_network"
}

resource "docker_volume" "postgres_data" {
  name = "saas_postgres_data"
}

resource "docker_container" "postgres" {
  name  = "saas_postgres"
  image = "postgres:15"

  env = [
    "POSTGRES_USER=postgres",
    "POSTGRES_PASSWORD=postgres",
    "POSTGRES_DB=saas"
  ]

  networks_advanced {
    name = docker_network.saas_network.name
  }

  volumes {
    volume_name    = docker_volume.postgres_data.name
    container_path = "/var/lib/postgresql/data"
  }

  ports {
    internal = 5432
    external = 5433
  }
}

resource "docker_container" "backend" {
  name  = "saas_backend"
  image = var.backend_image

  env = [
    "DATABASE_URL=postgresql://postgres:postgres@saas_postgres:5432/saas",
    "SECRET_KEY=terraform-secret"
  ]

  networks_advanced {
    name = docker_network.saas_network.name
  }

  ports {
    internal = 8000
    external = 8001
  }

  depends_on = [
    docker_container.postgres
  ]
}

