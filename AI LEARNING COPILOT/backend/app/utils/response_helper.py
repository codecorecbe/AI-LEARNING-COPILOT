"""
Response Helper Utilities
Standardized response formatting and error handling.
"""

from fastapi import HTTPException
from app.models.schemas import ErrorResponse
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class ResponseHelper:
    """
    Utility class for consistent API responses.
    """
    
    @staticmethod
    def success_response(data: Any, message: str = "Success") -> Dict[str, Any]:
        """
        Format a success response.
        
        Args:
            data: Response data
            message: Success message
            
        Returns:
            dict: Formatted success response
        """
        return {
            "success": True,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def error_response(
        error_type: str,
        message: str,
        details: str = None,
        status_code: int = 500
    ) -> HTTPException:
        """
        Format an error response and raise HTTPException.
        
        Args:
            error_type: Type of error
            message: Error message
            details: Additional details
            status_code: HTTP status code
            
        Returns:
            HTTPException: Formatted error exception
        """
        logger.error(f"{error_type}: {message}")
        
        return HTTPException(
            status_code=status_code,
            detail={
                "error": error_type,
                "message": message,
                "details": details
            }
        )
    
    @staticmethod
    def handle_service_error(e: Exception, operation: str = "Operation") -> HTTPException:
        """
        Handle service layer errors and convert to HTTP exceptions.
        
        Args:
            e: The caught exception
            operation: Description of the operation that failed
            
        Returns:
            HTTPException: Formatted error response
        """
        error_message = str(e)
        
        # Determine status code based on error type
        if "not found" in error_message.lower():
            status_code = 404
        elif "invalid" in error_message.lower() or "validation" in error_message.lower():
            status_code = 400
        elif "unauthorized" in error_message.lower() or "api key" in error_message.lower():
            status_code = 401
        else:
            status_code = 500
        
        return ResponseHelper.error_response(
            error_type=f"{operation}Error",
            message=f"{operation} failed",
            details=error_message,
            status_code=status_code
        )
    
    @staticmethod
    def validate_request(condition: bool, error_message: str):
        """
        Validate a request condition.
        
        Args:
            condition: Condition to check
            error_message: Error message if condition is False
            
        Raises:
            HTTPException: If condition is False
        """
        if not condition:
            raise ResponseHelper.error_response(
                error_type="ValidationError",
                message=error_message,
                status_code=400
            )


# Create global instance
response_helper = ResponseHelper()
