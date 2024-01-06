# Ucraft ERPNext Integration

This application integrates Ucraft with ERPNext, allowing users to create companies in ERPNext based on their Ucraft
project and authenticate via SSO.

## Features

- Create a company in ERPNext via an API call when a Ucraft user installs the app.
- Authenticate Ucraft users in ERPNext using SSO.

## API Endpoints

### Create Company

**Endpoint:** `/api/method/ucraft.api.create_company_for_ucraft_project`

**Method:** POST

**Description:** Creates a company in ERPNext with the given project ID from Ucraft.

**Request Payload:**

```json
{
  "project_id": "string",
  "company_name": "string"
}
Response:

200 OK on success with company creation message.
409 Conflict if a company with the project ID already exists.
400 Bad Request if required fields are missing.


Authentication
- This app will automatically override and redirect the current Auth UI through UCraft's API.
- Just Install App and Initiate Login
- 