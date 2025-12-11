# Questionnaire Integration Setup

This document explains how to set up the questionnaire integration between the Zeppelin frontend and backend.

## Overview

The integration allows users to submit questionnaire answers from the Vue.js frontend to the Django backend using Token authentication. The answers are stored in the database and can be managed through the Django admin interface.

## Backend Changes

### 1. New API Endpoint
- **URL**: `POST /questionnaire/submit/`
- **Authentication**: OAuth2 Authentication (same as existing endpoints)
- **Purpose**: Receives questionnaire answers and stores them in the database

### 2. Files Modified/Created
- `zeppelin/src/apps/questionnaire/api_views.py` - Added `submit_questionnaire` function
- `zeppelin/src/apps/questionnaire/api_urls.py` - Added new endpoint route

## Frontend Changes

### 1. API Service Enhancement
- Updated `zeppelin-frontend/src/services/api.ts` with `submitQuestionnaire` function
- Uses existing OAuth2 authentication system

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

### 1. Frontend Setup

1. **Create Environment File**:
   ```bash
   cd zeppelin-frontend
   cp .env.example .env
   ```

2. **Configure Environment Variables**:
   Edit `.env` file:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   VITE_CLIENT_ID=your_existing_oauth2_client_id
   VITE_CLIENT_SECRET=your_existing_oauth2_client_secret
   ```

   **Note**: Use the same OAuth2 credentials that were already configured for your project.

### 2. Running the Application

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
Authorization: Bearer your_oauth2_access_token
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

1. **OAuth2 Authentication Failed**
   - Verify CLIENT_ID and CLIENT_SECRET are correctly set in `.env`
   - Check OAuth2 application exists in Django admin: `/admin/oauth2_provider/application/`

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
     -H "Authorization: Bearer your_oauth2_access_token" \
     -H "Content-Type: application/json" \
     -d '{"questionnaire_type":"test","answers":{"T.01":{"adoption":"fully_adopted","comment":"test"}}}'
   ```

2. **Check Database**:
   - Login to Django admin: `http://localhost:8000/admin/`
   - Navigate to Questionnaire > Answers to see submitted data

## Security Notes

- OAuth2 credentials should be kept secure and not committed to version control
- The implementation uses the existing OAuth2 authentication system
- OAuth2 access tokens have built-in expiration for security
- Validate all input data on the backend

## Future Enhancements

Potential improvements for the integration:
- User-specific questionnaire tracking
- Questionnaire versioning
- Bulk answer submission
- Answer history and analytics
- Real-time validation feedback
- Progress saving (draft mode)