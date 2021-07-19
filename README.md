# Master Thesis
Uses two docker containers to host a website and a persistent database

### Website
- Based on FastApi
- Designed to host the thesis's experiment
- Designed to survey participants about the experiment
- Designed to be very user friendly to get a high successful experiment completion rate

### Database
- Postgres
- Provides persistent data storage through restarts 

---

### Try it yourself
Run it: `docker-compose up -d`
Access the database: `psql postgresql://postgres:postgres@localhost:5432/postgres`

Prerequisites:
- Docker
- Docker-compose