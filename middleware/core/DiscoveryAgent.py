from typing import Dict, List, Optional
import logging
from .ServiceCatalog import ServiceCatalog
from ..utils.http_client import HttpClient

logger = logging.getLogger(__name__)

class DiscoveryAgent:
    """Handles discovery of new services and APIs in the ecosystem."""
    
    def __init__(self, service_catalog: ServiceCatalog):
        self.service_catalog = service_catalog
        self.httpClient = HttpClient()
        
    def discover_new_services(self) -> Dict[str, str]:
        """
        Discovers new services by checking the Service Catalog.
        Returns a dictionary of newly discovered services with their API endpoints.
        """
        try:
            logger.info("Starting service discovery process.")
            new_services = {}
            
            # Fetch updated list of available services
            services = self.service_catalog.get_updated_service_list()
            
            for service in services:
                if not self.service_catalog.is_service_discovered(service['id']):
                    endpoint = service['api_endpoint']
                    new_services[service['name']] = endpoint
                    logger.info(f"Discovered new service: {service['name']} at {endpoint}")
                    self.service_catalog.mark_service_as_discovered(service['id'])
            
            return new_services
            
        except Exception as e:
            logger.error(f"Error during service discovery: {str(e)}")
            raise

    def get_service_endpoint(self, service_name: str) -> Optional[str]:
        """
        Retrieves the API endpoint for a specific service.
        Returns None if the service is not found or unavailable.
        """
        try:
            return self.service_catalog.get_service_endpoint(service_name)
            
        except KeyError:
            logger.warning(f"Service {service_name} not found in catalog.")
            return None

    def update_service_catalog(self) -> None:
        """Updates the local Service Catalog with the latest service information."""
        try:
            updated_services = self.service_catalog.fetch_updates()
            if updated_services:
                self.service_catalog.update_catalog(updated_services)
                logger.info("Service catalog successfully updated.")
                
        except Exception as e:
            logger.error(f"Failed to update service catalog: {str(e)}")