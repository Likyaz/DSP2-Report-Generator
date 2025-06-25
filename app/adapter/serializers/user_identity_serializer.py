from typing import Dict, Any
from app.domain.model.user_identity import UserIdentity


class UserIdentitySerializer:
    """Serializes DSP2 API account data to domain Account objects"""

    @staticmethod
    def from_api_response(api_data: Dict[str, Any]) -> UserIdentity:
        """Convert API response to UserIdentity domain object"""
        return UserIdentity(
            id=api_data["id"],
            prefix=UserIdentity.Prefix[api_data["prefix"]],
            first_name=api_data["first_name"],
            last_name=api_data["last_name"],
            date_of_birth=api_data["date_of_birth"],
        )
