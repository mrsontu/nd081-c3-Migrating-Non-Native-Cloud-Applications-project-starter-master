import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL="project3.postgres.database.azure.com"  #TODO: Update value
    POSTGRES_USER="azAdmin" #TODO: Update value
    POSTGRES_PW="abcd1234_"   #TODO: Update value
    POSTGRES_DB="project3"   #TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(POSTGRES_USER,POSTGRES_PW,POSTGRES_URL,POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'QRAKxlm8DIusTVB13izNCiCQQCRsd2w2N+ASbOkzfCc='
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://project3.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=QRAKxlm8DIusTVB13izNCiCQQCRsd2w2N+ASbOkzfCc=' #TODO: Update value
    SERVICE_BUS_QUEUE_NAME ='notificationqueue'
    ADMIN_EMAIL_ADDRESS: 'info@techconf.com'
    SENDGRID_API_KEY = '' #Configuration not required, required SendGrid Account

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
