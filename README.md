# Wellness Retreat Backend Service

## Overview
This project provides a backend service for managing wellness retreats and bookings. It is built using Flask and SQLAlchemy with a PostgreSQL database.

### Prerequisites
- Python 3.x
- PostgreSQL

### Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/peramanoj/Retreat.Git
   cd Retreat
2. **Create a Virtual Environment:**
   python -m venv venv
   source venv/bin/activate   
3. **Install Dependencies:**
   pip install -r requirements.txt
4. **Configure the Database:**
   Update table.py and app.py with your PostgreSQL credentials.
5. **Initialize the Database:**
   Run the following command to create tables and insert sample data:

#### Running the Application:
1. **Start the Flask Application:**
   python app.py
2. **Access the API:**
   Get Retreats: GET /retreats
   Create Booking: POST /book
##### Results:
Used POSTMAN to Send and retreive data 
1. **Retrive all retreats:**
   "http://127.0.0.1:5000/retreats"
2. **Filter the data that present Wellness in it:**
    "http://127.0.0.1:5000/retreats?filter=Wellness"
3. **Filter the data based on location:**
    "http://127.0.0.1:5000/retreats?location=Pune"
4. **Included Pagination:**
    "http://127.0.0.1:5000/retreats?page=1&limit=5"

  


