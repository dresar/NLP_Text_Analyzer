import os
import sys
import nltk

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nlp_app.settings")

# Download NLTK data jika belum ada
nltk_data_dir = os.path.join(os.path.dirname(__file__), 'nltk_data')
os.environ['NLTK_DATA'] = nltk_data_dir

# Pastikan direktori nltk_data ada
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir)

# Download data NLTK yang diperlukan
try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon', download_dir=nltk_data_dir)

try:
    nltk.data.find('punkt')
except LookupError:
    nltk.download('punkt', download_dir=nltk_data_dir)

try:
    nltk.data.find('stopwords')
except LookupError:
    nltk.download('stopwords', download_dir=nltk_data_dir)

# Import and create the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()