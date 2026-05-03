# MongoDB Data Migrator & Quote Parser

A robust Python utility designed to parse structured JSON data and migrate it into a MongoDB cloud database (Atlas). This project demonstrates the transition from flat file storage to a scalable NoSQL architecture using the MongoEngine ODM.

## Key Features

- **ODM Integration:** Utilizes `MongoEngine` to define strict schemas for unstructured data, ensuring data integrity during migration.
- **Relational Data Modeling in NoSQL:** Implements a reference-based system where quotes are linked to their respective authors via MongoDB `ReferenceField`.
- **Cloud Connectivity:** Securely connects to MongoDB Atlas clusters using URI-based authentication.
- **Automated Ingestion:** Features specialized scripts (`database_authors.py`, `database_quotes.py`) to handle batch imports of complex JSON objects.

## Technical Stack

- **Language:** Python 3.x
- **Database:** MongoDB (via MongoDB Atlas)
- **Library:** [MongoEngine](http://mongoengine.org/) (ODM)
- **Data Format:** JSON

## Project Structure

- `main.py`: The central entry point for coordinating database connections and migration tasks.
- `database_authors.py`: Defines the `Author` model and handles the ingestion of author biographies, birthdates, and locations.
- `database_quotes.py`: Defines the `Quote` model, including tagging systems and author associations.
- `separate_tables.py`: Contains logic for isolating and cleaning data entities before migration.

## Getting Started

### Prerequisites
- Python 3.14.3+
- A MongoDB Atlas account (or local MongoDB instance)

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/strait593/Data-Parser.git](https://github.com/strait593/Data-Parser.git)
   cd Data-Parser/parser
