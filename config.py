class Config:
    SECRET_KEY = 'speechTospeech'
    # Add other common configurations

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    # Add production-specific configurations

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    # Add development-specific configurations
