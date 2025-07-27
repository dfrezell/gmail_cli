import os
import json
from msal import PublicClientApplication, SerializableTokenCache
from msgraph import GraphServiceClient

SCOPES = ['https://graph.microsoft.com/Mail.Send']

def get_client_id():
    """Get client ID from outlook_client_id.txt file"""
    try:
        with open('outlook_client_id.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(
            "outlook_client_id.txt not found. Please create this file with your Azure app client ID. "
            "See README.md for setup instructions."
        )

def authenticate_outlook():
    """Authenticate with Microsoft Graph API using device code flow"""
    token_cache_file = 'outlook_token_cache.json'
    client_id = get_client_id()
    
    # Create a serializable token cache
    cache = SerializableTokenCache()
    
    # Load token cache if it exists
    if os.path.exists(token_cache_file):
        try:
            with open(token_cache_file, 'r') as f:
                cache_data = f.read()
                if cache_data.strip():
                    cache.deserialize(cache_data)
                    print(f"Loaded token cache from {token_cache_file}")
                else:
                    print("Token cache file is empty")
        except Exception as e:
            print(f"Error loading token cache: {e}")
            # If cache is corrupted, continue without it
            pass
    
    # Create MSAL app for personal Microsoft accounts with the cache
    app = PublicClientApplication(
        client_id=client_id,
        authority="https://login.microsoftonline.com/consumers",
        token_cache=cache
    )
    
    # Try to get token silently first
    accounts = app.get_accounts()
    result = None
    
    print(f"Found {len(accounts)} cached accounts")
    
    if accounts:
        print("Attempting silent token acquisition...")
        # Try to get token silently
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
        if result and "access_token" in result:
            print("Successfully acquired token silently!")
        else:
            print(f"Silent token acquisition failed: {result.get('error') if result else 'No result'}")
    
    if not result or "access_token" not in result:
        # Need to authenticate interactively
        print("Authentication required. Please follow the device code flow:")
        
        # First, initiate the device flow
        flow = app.initiate_device_flow(scopes=SCOPES)
        if "user_code" not in flow:
            raise ValueError("Failed to create device flow. Error: %s" % json.dumps(flow, indent=2))
        
        print("\n" + "="*60)
        print("MICROSOFT AUTHENTICATION REQUIRED")
        print("="*60)
        print(flow["message"])
        print("="*60 + "\n")
        
        # Complete the device flow
        result = app.acquire_token_by_device_flow(flow)
    
    if "access_token" not in result:
        raise Exception(f"Authentication failed: {result.get('error_description', 'Unknown error')}")
    
    # Save token cache
    try:
        if cache.has_state_changed:
            cache_state = cache.serialize()
            print(f"Token cache state length: {len(cache_state)}")
            if cache_state:
                with open(token_cache_file, 'w') as f:
                    f.write(cache_state)
                print(f"Token cache saved to {token_cache_file}")
            else:
                print("Warning: Token cache is empty, not saving")
        else:
            print("Token cache unchanged, not saving")
    except Exception as e:
        print(f"Error saving token cache: {e}")
        # If we can't save cache, continue anyway
        pass
    
    # Create credential object that can provide the access token
    class TokenCredential:
        def __init__(self, access_token):
            self.access_token = access_token
        
        def get_token(self, *scopes, **kwargs):
            from azure.core.credentials import AccessToken
            import time
            # Return token with a future expiry (MSAL handles refresh)
            return AccessToken(self.access_token, int(time.time()) + 3600)
    
    credential = TokenCredential(result['access_token'])
    
    # Create GraphServiceClient
    graph_client = GraphServiceClient(
        credentials=credential,
        scopes=SCOPES
    )
    
    return graph_client