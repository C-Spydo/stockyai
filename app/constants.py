import os 

DATABASE_URL = os.getenv('DATABASE_URL')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_INDEX_HOST = os.getenv('PINECONE_INDEX_HOST')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')

#Flask Config
APP_SECRET_KEY = os.getenv('APP_SECRET_KEY')

#Repsonse Messages
NOT_FOUND_MESSAGE = 'Not found'
SUCCESS_MESSAGE = 'Success'
INTERNAL_SERVER_ERROR_MESSAGE = 'Something went wrong'

PINCONE_INDEX="stocky-ai-index"