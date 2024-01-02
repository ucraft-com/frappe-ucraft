# Ucraft ERPNext Integration

This application integrates Ucraft with ERPNext, allowing users to create companies in ERPNext based on their Ucraft project and authenticate via SSO.

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
Endpoint: /api/method/ucraft.sso.auth.authenticate_login

Method: POST

Description: Authenticates a Ucraft user in ERPNext using SSO.

Request Payload:

json
Copy code
{
  "project_id": "string",
  "sso_token": "string",
  "window": "boolean",
  "return_url": "string"
}
Response:

200 OK on successful authentication.
Error message on failure.
Installation

Configuration

Ensure that the ucraft_project_id custom field is added to the Company DocType in ERPNext.

Usage

To integrate with Ucraft, make API calls to the provided endpoints with the necessary data as per the API documentation.

![Logo](digram.png)
