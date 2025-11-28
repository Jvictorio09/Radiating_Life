# Environment Variables Setup

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# PostgreSQL Configuration
# Option 1: Use DATABASE_URL (recommended for Railway/Heroku)
DATABASE_URL=postgresql://user:password@host:port/dbname

# Option 2: Use individual PostgreSQL variables (for direct connection)
POSTGRES_DB=your_database_name
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

## Getting Cloudinary Credentials

1. Sign up at [cloudinary.com](https://cloudinary.com)
2. Go to Dashboard
3. Copy your Cloud Name, API Key, and API Secret

## Getting PostgreSQL Connection String

For Railway:
- Go to your Railway project dashboard
- Select your PostgreSQL service
- Copy the connection string from the "Connect" tab

For local PostgreSQL:
- Use the individual variables (POSTGRES_DB, POSTGRES_USER, etc.)

