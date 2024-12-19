import os

class Config:
    # 基本配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:Ff29098796@127.0.0.1/user_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis 配置
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
    REDIS_DB = int(os.environ.get('REDIS_DB', 0))
    
    # Celery 配置使用 Redis 配置
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or \
        f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or \
        f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

# 為了向後兼容
CELERY_BROKER_URL = Config.CELERY_BROKER_URL