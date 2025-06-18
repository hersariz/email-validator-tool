import tldextract

# Daftar domain email umum/personal
COMMON_PERSONAL_DOMAINS = [
    'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com',
    'icloud.com', 'protonmail.com', 'mail.com', 'zoho.com', 'yandex.com',
    'gmx.com', 'tutanota.com', 'fastmail.com', 'live.com', 'msn.com',
    'me.com', 'mail.ru', 'inbox.com', 'comcast.net', 'verizon.net',
    'sbcglobal.net', 'att.net', 'rocketmail.com', 'bellsouth.net', 'cox.net',
    'charter.net', 'earthlink.net'
]

def categorize_email(email):
    """
    Mengkategorikan email sebagai personal atau business berdasarkan domainnya.
    
    Args:
        email (str): Alamat email yang akan dikategorikan
        
    Returns:
        str: 'personal' atau 'business'
    """
    try:
        domain = email.split('@')[-1].lower()
        if domain in COMMON_PERSONAL_DOMAINS:
            return 'personal'
        else:
            return 'business'
    except:
        return 'unknown' 