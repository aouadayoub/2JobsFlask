# 2JobsFlask: AI-Powered Job Matching

## Overview

2JobsFlask is a sophisticated job matching application built with Python, Flask, and MongoDB. It leverages the power of LLMs to intelligently connect job seekers with suitable job opportunities. 

**Here's how it works:** 2JobsFlask analyzes both user-provided job preferences and skills extracted from uploaded resumes to identify the most relevant job matches. 
 

## Technical Stack

* **Backend:** Flask (Python)
* **Database:** MongoDB
* **Natural Language Processing:** langchain, Together (Meta-Llama), Redis (for caching)
* **PDF Processing:**  pdfplumber
* **Additional Libraries:** pymongo, decouple, flask-cors


## Setup & Installation

### 1. Prerequisites

* **Python 3.8+:**  [https://www.python.org/](https://www.python.org/)
* **MongoDB:**  [https://www.mongodb.com/](https://www.mongodb.com/) 
    * Install and make sure MongoDB is running locally.
* **Redis:** [https://redis.io/](https://redis.io/)
    * Install and ensure Redis is running. 
* **pip (package installer):** Usually included with Python.

### 2. Project Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/2JobsFlask.git
   cd 2JobsFlask 
   ```

2. **Virtual Environment (Recommended):**
   ```bash
   python3 -m venv env
   # On Mac: 
        source env/bin/activate    
   # On Windows: 
        env\Scripts\activate 
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt 
   ```

### 3. Configuration

1. **Create a `.env` file:** 
    * Place this file in the root directory. 
    * Add your MongoDB credentials, replacing the placeholders:

    ```
    together_api_key = YOUR_TOGETHER_API_KEY
    FLASK_ENV=development
    MONGO_URI=mongodb://localhost:27017/  
    DATABASE_NAME=2JOBS
    COLLECTION_NAME=Jobs
    ```

### 4. Running the Application

1. **Make the run script executable:**
   ```bash
   chmod +x run.sh
   ```

2. **Start the application (including MongoDB and Redis):**
   ```bash
   ./run.sh
   ```

   This script will:
   - Start MongoDB
   - Start Redis
   - Wait a few seconds for MongoDB and Redis to initialize
   - Start your Flask application 

   Your application should now be accessible at `http://127.0.0.1:4000/`

## API Usage

The application exposes an API endpoint for job matching:

**Endpoint:** `/process`
**Method:** `POST`
**Request Body (JSON):**
```json
{
  "cv_filename": "your_resume.pdf", 
  "prompt": "I am looking for a software engineer position", 
  "country": "Canada"
}
```

**Response (JSON):**
```json
{
  "matched_jobs": [
    {
      "business": "..",
      "country": "Canada",
      "date": "..",
      "job_link": "..",
      "location": "..",
      "logo": "..",
      "salary": "..",
      "source": "..",
      "title": "Software Engineer"
    },
    // ... more matched jobs 
  ],
  "job_title": "Software Engineer",
  "country": "Canada"
}
```

## Future Enhancements

* **Advanced Filtering:**  Add more filters (salary, experience level, company size, etc.). 
* **Recommendation Engine:** Build a recommendation system to suggest jobs based on user profiles and behavior. 

## Contributing

Contributions are highly encouraged! To contribute:

1. Fork the repository.
2. Create a new branch for your feature.
3. Make your changes and commit.
4. Push your branch to your fork. 
5. Open a pull request to the main repository. 

## License

This project is licensed under the MIT License - see the `LICENSE` file for details. 
