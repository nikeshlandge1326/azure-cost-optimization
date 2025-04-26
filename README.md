# Azure Cost Optimization - Billing Records Management

## Problem
Billing records are stored in Azure Cosmos DB. Old records (>3 months) are rarely accessed but contribute to significant storage costs.

## Solution
Implement a Hot-Cold Storage architecture:
- Hot: Recent records in CosmosDB (last 3 months)
- Cold: Older records archived in Azure Blob Storage

The system:
- Keeps the API unchanged
- Ensures no data loss
- Provides fallback to Blob Storage for old records

## Architecture

![Architecture](architecture/architecture-diagram.png)

## Components
- **Azure Function:** Moves old records to Blob Storage.
- **Billing API Logic:** Falls back to Blob Storage if CosmosDB does not have the record.


