init:
	mkdir -p backend/app/{core,api/v1,domain/entities,infrastructure/database,schemas,services}
	mkdir -p backend/tests/{unit,integration,e2e}
	touch backend/app/main.py
	touch backend/app/core/{config.py,security.py,database.py}
	touch backend/app/api/v1/{auth.py,links.py}
	touch backend/app/domain/entities/{user.py,link.py}
	touch backend/app/infrastructure/database/models.py
	touch backend/app/schemas/{user.py,link.py}
	touch backend/app/services/{user_service.py,link_service.py}
	touch backend/requirements.txt backend/Dockerfile
	touch docker-compose.yml README.md .env.example LICENSE