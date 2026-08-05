"""Unit tests for Azure Blob Storage and Event Hubs integrations in pii-radar."""

from __future__ import annotations

from pii_radar.integrations.azure import AzureBlobStreamRedactor, AzureEventHubHandler


class TestAzureIntegration:
    def test_azure_blob_stream_redactor(self):
        redactor = AzureBlobStreamRedactor(
            connection_string="MockConnectionString",
            container_name="test-container",
        )
        total_found, counts = redactor.redact_blob("test_data.csv")
        assert total_found == 0
        assert isinstance(counts, dict)

    def test_azure_event_hub_handler(self):
        handler = AzureEventHubHandler(
            connection_string="MockConnectionString",
            eventhub_name="test-hub",
        )

        test_events = [
            "John Doe,john@example.com,123-45-6789",
            "Jane Smith,jane@domain.com,987-65-4321",
            "Regular telemetry metric status OK",
        ]

        redacted = handler.process_event_batch(test_events)
        assert len(redacted) == 3
        assert "[REDACTED-EMAIL]" in redacted[0] or "john@example.com" not in redacted[0]
        assert "[REDACTED-SSN]" in redacted[0] or "123-45-6789" not in redacted[0]
        assert redacted[2] == "Regular telemetry metric status OK"
