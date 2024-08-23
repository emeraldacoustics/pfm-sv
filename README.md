# SaaS platform using AWS Lambda

This project is a web application designed to facilitate the lookup and update of zip code data stored in two separate databases. The application interacts with CSV files uploaded by the user to either retrieve or update information on internet products and populations within specific zip codes. The solution is implemented using Python for the backend and React for the frontend.

## Project Structure

The project is organized into several key directories and files:

- **`/backend`**: Contains the Python code that powers the serverless backend, including the Lambda functions and utility scripts.
- **`/frontend`**: Contains the React application that provides the user interface.
- **`/data`**: Contains sample CSV files used for testing the application.

## Installation and Setup

To run the application locally or deploy it to the cloud, follow these steps:

### Prerequisites

- Node.js (for running the React application)
- Python 3.x (for running the backend functions)
- AWS CLI (for deploying the backend if using AWS)
- Serverless Framework (for deploying the backend)

### Local Setup

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-repo/pfm-sv-main.git
    cd pfm-sv-main
    ```

2. **Backend Setup**:
    - Navigate to the `backend` directory:
      ```bash
      cd backend
      ```
    - Install Python dependencies:
      ```bash
      pip install -r requirements.txt
      ```
    - Install Node.js dependencies for the Serverless Framework:
      ```bash
      npm install
      ```
    - Run the backend locally using the Serverless Framework:
      ```bash
      serverless offline
      ```

3. **Frontend Setup**:
    - Navigate to the `frontend` directory:
      ```bash
      cd ../frontend
      ```
    - Install Node.js dependencies:
      ```bash
      npm install
      ```
    - Start the React application:
      ```bash
      npm start
      ```

4. **Data Setup**:
    - Sample CSV files are located in the `data` directory for testing purposes.

## Usage

Once the application is running, you can access it through the frontend React application.

### Zip-Code Lookup

1. **Upload CSV**: Navigate to the lookup section for either the Product or Population database.
2. **Download Results**: After uploading, the application will generate a CSV file with the corresponding data from the database.

### Zip-Code Update

1. **Upload CSV**: Navigate to the update section for either the Product or Population database.
2. **Success/Error Messages**: The application will validate the data and update the database accordingly. Any errors (e.g., missing modified user or N/A values) will be displayed to the user.

## Deployment

To deploy the application to AWS, follow these steps:

1. **Ensure the AWS CLI is configured** with the appropriate credentials and region.

2. **Deploy the Backend**:
    - Use the Serverless Framework to deploy the backend to AWS:
        ```bash
        serverless deploy
        ```

3. **Deploy the Frontend**:
    - Host the React application on an S3 bucket or another static site hosting service.

## Testing

The application has been thoroughly tested using sample CSV files located in the `data` directory. These files include:

- `product_master.csv`
- `population_master.csv`
- `lookup.csv`
- `product_update.csv`
- `population_update.csv`

Tests include:

- CSV upload and download functionality.
- Database lookup accuracy.
- Update operations with various edge cases (e.g., missing modified user, N/A values).

## Technical Details

- **Backend**: The backend is implemented using AWS Lambda functions with the Serverless Framework. It uses Python for handling the business logic and interacts with DynamoDB or other databases as specified.
- **Frontend**: The frontend is a React application that provides an intuitive user interface for interacting with the backend services. It uses Tailwind CSS for styling and follows modern best practices.
- **Deployment**: Deployment is handled via the Serverless Framework for the backend, making it easy to scale and manage in the cloud.

## Conclusion

This project demonstrates the ability to build a full-stack web application that interacts with cloud-based databases and services. The application meets all the requirements outlined in the assessment and is ready for deployment in a production environment.
