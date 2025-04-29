# mForm Bulk Upload Demo

A web application for uploading and parsing Excel-based questionnaires in XLSForm-like format.

## Project Structure

```
.
├── frontend/          # Angular frontend application
└── backend/           # Python FastAPI backend application
```

## Features

- Excel file upload (.xls/.xlsx)
- XLSForm parsing
- Live form preview
- JSON download
- Material UI interface

## Tech Stack

### Frontend

- Angular 16+
- Material UI
- SCSS

### Backend

- Python FastAPI
- openpyxl/pandas for Excel parsing

## Setup Instructions

### Frontend Setup

1. Navigate to the frontend directory
2. Run `npm install`
3. Run `ng serve` for development server

### Backend Setup

1. Navigate to the backend directory
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment:
   - Windows: `.\venv\Scripts\activate`
   - Unix: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run development server: `uvicorn main:app --reload`

## Development Phases

1. Project Setup & Basic Structure
2. File Upload Frontend Implementation
3. Backend Parser Implementation
4. Frontend Preview & Download
5. Polish & Optional Features
