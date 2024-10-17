import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL="postgresproject.postgres.database.azure.com"  #TODO: Update value
    POSTGRES_USER="azAdmin" #TODO: Update value
    POSTGRES_PW="abcd1234_"   #TODO: Update value
    POSTGRES_DB="project3"   #TODO: Update value
    DB_URL = 'postgresql://azAdmin:abcd1234_@postgresproject.postgres.database.azure.com/project3'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'QRAKxlm8DIusTVB13izNCiCQQCRsd2w2N+ASbOkzfCc='
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://project3bus.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=lLeBHIWc3xrR2UGP6THDgysdPiqQ+0yp1+ASbDkYUiY=' #TODO: Update value
    SERVICE_BUS_QUEUE_NAME ='notificationqueue'
    ADMIN_EMAIL_ADDRESS: 'info@techconf.com'
    SENDGRID_API_KEY = '' #Configuration not required, required SendGrid Account

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
