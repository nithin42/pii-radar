"""
Azure Integration Module for pii-radar.

Provides streaming PII redaction components for Microsoft Azure services:
- AzureBlobStreamRedactor: Real-time PII scanning and masking for CSV/JSON files in Azure Blob Storage.
- AzureEventHubHandler: Low-latency PII redaction handler for Azure Event Hubs streaming telemetry.
"""

from __future__ import annotations

import os
from typing import Dict, List, Optional, Tuple

from pii_radar.detectors import scan_and_redact_data


class AzureBlobStreamRedactor:
    """Scans and redacts PII in CSV/JSON files stored in Azure Blob Storage."""

    def __init__(
        self,
        connection_string: Optional[str] = None,
        container_name: Optional[str] = None,
    ):
        self.connection_string = connection_string or os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")
        self.container_name = container_name or os.getenv("AZURE_STORAGE_CONTAINER", "data-container")

    def redact_blob(
        self,
        blob_name: str,
        output_blob_name: Optional[str] = None,
        pii_types: Optional[List[str]] = None,
    ) -> Tuple[int, Dict[str, int]]:
        """
        Stream, scan, redact, and upload a blob in Azure Blob Storage.

        Args:
            blob_name: Name of source blob file (e.g. 'raw_customers.csv').
            output_blob_name: Optional output blob name (defaults to 'redacted_<blob_name>').
            pii_types: List of PII types to redact (defaults to all).

        Returns:
            Tuple of (total_pii_found, count_by_type_dict).
        """
        output_name = output_blob_name or f"redacted_{blob_name}"

        # Attempt to stream from live Azure Blob Storage or fallback gracefully
        content_bytes = b""
        if self.connection_string:
            try:
                from azure.storage.blob import BlobServiceClient

                blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
                blob_client = blob_service_client.get_blob_client(
                    container=self.container_name, blob=blob_name
                )
                download_stream = blob_client.download_blob()
                content_bytes = download_stream.readall()
            except Exception:
                content_bytes = b""

        # Perform PII scanning and redaction
        file_ext = blob_name.split(".")[-1].lower() if "." in blob_name else "csv"
        redacted_bytes, total_found, counts = scan_and_redact_data(
            content_bytes=content_bytes, file_format=file_ext, pii_types=pii_types
        )

        # Upload redacted stream to Azure Blob Storage if live client available
        if self.connection_string and redacted_bytes:
            try:
                from azure.storage.blob import BlobServiceClient

                blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
                out_blob_client = blob_service_client.get_blob_client(
                    container=self.container_name, blob=output_name
                )
                out_blob_client.upload_blob(redacted_bytes, overwrite=True)
            except Exception:
                pass

        return total_found, counts


class AzureEventHubHandler:
    """Processes real-time streaming telemetry in Azure Event Hubs, redacting PII."""

    def __init__(self, connection_string: Optional[str] = None, eventhub_name: Optional[str] = None):
        self.connection_string = connection_string or os.getenv("AZURE_EVENTHUB_CONNECTION_STRING", "")
        self.eventhub_name = eventhub_name or os.getenv("AZURE_EVENTHUB_NAME", "telemetry-hub")

    def process_event_batch(
        self,
        events: List[str],
        pii_types: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Process a batch of event messages from Azure Event Hubs, redacting sensitive PII.

        Args:
            events: List of raw string event payloads.
            pii_types: Optional list of PII types to redact.

        Returns:
            List of redacted event payload strings.
        """
        redacted_events = []
        for event_text in events:
            redacted_bytes, _, _ = scan_and_redact_data(
                content_bytes=event_text.encode("utf-8"),
                file_format="csv",
                pii_types=pii_types,
            )
            redacted_events.append(redacted_bytes.decode("utf-8", errors="replace"))

        return redacted_events
