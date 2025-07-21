import requests
from utils import categorize_email

def validate_with_abstractapi(email, api_key="bb5407401a0f45bcaffbe59a080d393c"):
    """
    Memvalidasi email menggunakan AbstractAPI Email Validation.
    
    Args:
        email (str): Alamat email yang akan divalidasi
        api_key (str): API key untuk AbstractAPI
        
    Returns:
        dict: Hasil validasi dari API atau None jika terjadi error
    """
    try:
        url = f"https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email}"
        response = requests.get(url)
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Error validasi AbstractAPI: {e}")
        return None

def validate_email(email, use_api=True):
    """
    Melakukan validasi email menggunakan AbstractAPI.
    
    Args:
        email (str): Alamat email yang akan divalidasi
        use_api (bool): Parameter untuk backward compatibility, sekarang selalu menggunakan API
        
    Returns:
        dict: Hasil validasi lengkap
    """
    # Memastikan email adalah string
    if not isinstance(email, str):
        return {
            'email': str(email),
            'category': 'unknown',
            'api_validation': None
        }
    
    # Kategorikan email (personal/business) berdasarkan domain
    category = categorize_email(email)
    
    # Validasi menggunakan API
    api_validation = validate_with_abstractapi(email)
    
    # Hasil validasi
    return {
        'email': email,
        'category': category,
        'api_validation': api_validation
    } 