# Questionnaire Integration Setup

This document explains how to set up the questionnaire integration between the Zeppelin frontend and backend.

## Overview

The integration allows users to submit questionnaire answers from the Vue.js frontend to the Django backend using Token authentication. The answers are stored in the database and can be managed through the Django admin interface.

## Backend Changes

### 1. New API Endpoint
- **URL**: `POST /questionnaire/submit/`
- **Authentication**: Token Authentication
- **Purpose**: Receives questionnaire answers and stores them in the database

### 2. Files Modified/Created
- `zeppelin/src/apps/questionnaire/api_views.py` - Added `submit_questionnaire` function
- `zeppelin/src/apps/questionnaire/api_urls.py` - Added new endpoint route
- `zeppelin/setup_api_token.py` - Helper script for token generation

## Frontend Changes

### 1. Environment Configuration
- Added `VITE_ZEPPELIN_API_TOKEN` to environment variables
- Updated `zeppelin-frontend/src/stores/env.ts` to include token

### 2. API Service Enhancement
- Updated `zeppelin-frontend/src/services/api.ts` to include token authentication
- Added `submitQuestionnaire` function for API calls

### 3. Questionnaire Composable
- Enhanced `zeppelin-frontend/src/composables/useQuestionnaire.ts` with submission functionality
- Added loading states, error handling, and success feedback

### 4. Form Updates
All questionnaire forms now include:
- Real API submission instead of console logging
- Loading states during submission
- Success/error message display
- Form reset after successful submission

## Setup Instructions

### 1. Backend Setup

1. **Create Superuser and API Token**:
   ```bash
   cd zeppelin
   python setup_api_token.py
   ```
   
   This script will:
   - Create a Django superuser (if none exists)
   - Generate an API token
   - Display setup instructions

2. **Alternative Manual Setup**:
   ```bash
   cd zeppelin/src
   python manage.py createsuperuser
   python manage.py shell
   ```
   
   In the Django shell:
   ```python
   from django.contrib.auth.models import User
   from rest_framework.authtoken.models import Token
   
   user = User.objects.get(username='your_username')
   token = Token.objects.create(user=user)
   print(f"Token: {token.key}")
   ```

### 2. Frontend Setup

1. **Create Environment File**:
   ```bash
   cd zeppelin-frontend
   cp .env.example .env
   ```

2. **Configure Environment Variables**:
   Edit `.env` file:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   VITE_CLIENT_ID=your_client_id
   VITE_CLIENT_SECRET=your_client_secret
   VITE_ZEPPELIN_API_TOKEN=your_generated_token_here
   ```

### 3. Running the Application

1. **Start Backend**:
   ```bash
   cd zeppelin
   make up  # or docker-compose up
   ```

2. **Start Frontend**:
   ```bash
   cd zeppelin-frontend
   npm install
   npm run dev
   ```

## API Usage

### Request Format
```json
POST /questionnaire/submit/
Authorization: Token your_token_here
Content-Type: application/json

{
  "questionnaire_type": "innovation_system",
  "answers": {
    "IS.01": {
      "adoption": "fully_adopted",
      "comment": "We have this fully implemented"
    },
    "IS.02": {
      "adoption": "partially_adopted", 
      "comment": "Work in progress"
    }
  }
}
```

### Response Format
```json
{
  "message": "Questionnaire submitted successfully",
  "questionnaire_id": 123,
  "answers_count": 2,
  "answers": [
    {
      "question_code": "IS.01",
      "adoption": "fully_adopted",
      "comment": "We have this fully implemented"
    }
  ]
}
```

### Adoption Levels
- `not_adopted` - 0% adoption
- `partially_adopted` - 50% adoption  
- `fully_adopted` - 100% adoption

## Database Schema

The integration uses existing Django models:
- `Questionnaire` - Stores questionnaire metadata
- `Statement` - Stores question definitions
- `AdoptedLevel` - Stores adoption level definitions
- `Answer` - Stores individual question answers

## Features

### Frontend Features
- ✅ Real-time form validation
- ✅ Loading states during submission
- ✅ Success/error message display
- ✅ Form reset after successful submission
- ✅ Token-based authentication
- ✅ Error handling for network issues

### Backend Features
- ✅ Token authentication
- ✅ Structured JSON API
- ✅ Automatic model creation for new questions/adoption levels
- ✅ Database storage with proper relationships
- ✅ Error handling and validation

## Troubleshooting

### Common Issues

1. **Token Authentication Failed**
   - Verify token is correctly set in `.env`
   - Check token exists in Django admin: `/admin/authtoken/token/`

2. **CORS Issues**
   - Ensure frontend URL is in `CORS_ALLOWED_ORIGINS` in Django settings
   - Default allows `http://localhost:5173`

3. **API Endpoint Not Found**
   - Verify Django URLs are properly configured
   - Check that questionnaire app is in `INSTALLED_APPS`

4. **Database Errors**
   - Run migrations: `python manage.py migrate`
   - Ensure database is properly set up

### Testing the Integration

1. **Test API Directly**:
   ```bash
   curl -X POST http://localhost:8000/questionnaire/submit/ \
     -H "Authorization: Token your_token_here" \
     -H "Content-Type: application/json" \
     -d '{"questionnaire_type":"test","answers":{"T.01":{"adoption":"fully_adopted","comment":"test"}}}'
   ```

2. **Check Database**:
   - Login to Django admin: `http://localhost:8000/admin/`
   - Navigate to Questionnaire > Answers to see submitted data

## Security Notes

- API tokens should be kept secure and not committed to version control
- The current implementation uses Django's built-in Token authentication
- Consider implementing token rotation for production use
- Validate all input data on the backend

## Future Enhancements

Potential improvements for the integration:
- User-specific questionnaire tracking
- Questionnaire versioning
- Bulk answer submission
- Answer history and analytics
- Real-time validation feedback
- Progress saving (draft mode)