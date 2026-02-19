from typing import Dict, Optional
import logging
from .auth.AuthHandler import AuthHandler

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages connections to various APIs and services."""
    
    def __init__(self):
        self.connections = {}
        self.auth_handler = AuthHandler()
        
    def connect_to_service(self, service_name: str, api_key: str) -> bool:
        """
        Establishes a connection to the specified service using the provided API key.
        Returns True if successful, False otherwise.
        """
        try:
            endpoint = self._get_service_endpoint(service_name)
            if not endpoint:
                logger.error(f"Endpoint for {service_name} not found.")
                return False
                
            auth = self.auth_handler.get_auth_headers(api_key)
            response = self.httpClient.make_request("GET", endpoint, headers=auth)
            
            if response.status_code == 200:
                self.connections[service_name] = {
                    'endpoint': endpoint,
                    'auth': auth,
                    'last_check': datetime.now()
                }
                logger.info(f"Successfully connected to {service_name}.")
                return True
            else:
                logger.error(f"Failed to connect to {service_name}: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Connection error for {service_name}: {str(e)}")
            return False

    def _get_service_endpoint(self, service_name: str) -> Optional[str]:
        """Retrieves the API endpoint for the specified service."""
        try:
            # This would typically call a ServiceCatalog or similar to get the endpoint
            return self.service_catalog.get_service_endpoint(service_name)
            
        except Exception as e:
            logger.error(f"Failed to retrieve endpoint for {service_name}: {str(e)}")
            return None

    def test_connection(self, service_name: str) -> bool:
        """
        Tests the existing connection to a service.
        Returns