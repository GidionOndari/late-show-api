# Late Show API
A Flask RESTful API for managing Late Show episodes, guests, and guest appearances with ratings. Features include listing episodes, viewing details, deleting episodes, listing guests, and adding appearances with nested responses. 

## Tech Stack
- Python 3
- Flask
- Flask-RESTful
- Flask-Migrate
- Flask-SQLAlchemy
- SQLite
- SQLAlchemy-Serializer

## Project Structure
late-show-api/
├── server/
│   ├── app.py
│   ├── models.py
│   ├── seed.py
│   └── __init__.py
├── migrations/
├── instance/
│   └── app.db
├── env/
├── requirements.txt
└── README.md

## Setup Instructions
1. Clone the repo and enter the directory:  
   `git clone <repo_url> && cd late-show-api`
2. Create and activate virtual environment:  
   `python -m venv env`  
   `source env/bin/activate` (Linux/Mac) or `env\Scripts\activate` (Windows)
3. Install dependencies:  
   `pip install -r requirements.txt`
4. Run database migrations:  
   `flask db upgrade`
5. Seed the database:  
   `python -m server.seed`
6. Run the server:  
   `python -m server.app`

## API Endpoints
- `GET /` → Check server status  
- `GET /episodes` → List all episodes  
- `GET /episodes/<id>` → Episode details with appearances  
- `DELETE /episodes/<id>` → Delete an episode  
- `GET /guests` → List all guests  
- `POST /appearances` → Add an appearance  
Example JSON body:  
`{ "rating": 4, "episode_id": 1, "guest_id": 2 }`

## Notes
- Ensure migrations run before seeding the database.  
- Use Flask development server only for testing.  
- Ratings must be integers between 1 and 5.

## Author
Gidion Ondari
