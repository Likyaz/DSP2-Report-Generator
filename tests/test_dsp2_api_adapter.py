import pytest
from unittest.mock import patch, MagicMock
from app.adapter.dsp2_api_adapter import Dsp2ApiAdapter


@pytest.fixture
def adapter():
    return Dsp2ApiAdapter()


def test_get_token(adapter):
    with patch.object(adapter.session, "post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": "fake-token"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        token = adapter.get_token("user", "pass")
        assert token == "fake-token"
        mock_post.assert_called_once()


def test_get_user_identity(adapter):
    with patch.object(adapter.session, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        with patch(
            "app.adapter.serializers.user_identity_serializer.UserIdentitySerializer.from_api_response"
        ) as mock_serializer:
            mock_serializer.return_value = "user_obj"
            result = adapter.get_user_identity("token")
            assert result == "user_obj"
            mock_get.assert_called_once()


def test_get_accounts(adapter):
    with patch.object(adapter.session, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        with patch(
            "app.adapter.serializers.account_serializer.AccountSerializer.from_api_list"
        ) as mock_serializer:
            mock_serializer.return_value = ["acc1", "acc2"]
            result = adapter.get_accounts("token")
            assert result == ["acc1", "acc2"]
            mock_get.assert_called_once()


def test_get_account(adapter):
    with patch.object(adapter.session, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        with patch(
            "app.adapter.serializers.account_serializer.AccountSerializer.from_api_response"
        ) as mock_serializer:
            mock_serializer.return_value = "acc_obj"
            result = adapter.get_account("token", "accid")
            assert result == "acc_obj"
            mock_get.assert_called_once()


def test_get_balances(adapter):
    with patch.object(adapter.session, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        with patch(
            "app.adapter.serializers.balance_serializer.BalanceSerializer.from_api_list"
        ) as mock_serializer:
            mock_serializer.return_value = ["bal1", "bal2"]
            result = adapter.get_balances("token", "accid")
            assert result == ["bal1", "bal2"]
            mock_get.assert_called_once()


def test_get_transactions(adapter):
    with patch.object(adapter.session, "get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        with patch(
            "app.adapter.serializers.transaction_serializer.TransactionSerializer.from_api_list"
        ) as mock_serializer:
            mock_serializer.return_value = ["tx1", "tx2"]
            result = adapter.get_transactions("token", "accid", 1, 10)
            assert result == ["tx1", "tx2"]
            mock_get.assert_called_once()
