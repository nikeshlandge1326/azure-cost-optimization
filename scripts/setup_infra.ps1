# Variables
$resourceGroup = "billing-optimization-rg"
$location = "EastUS"
$storageAccount = "billingstorage$(Get-Random)"
$functionApp = "billing-archive-func$(Get-Random)"
$cosmosAccount = "billingcosmos$(Get-Random)"

# Create Resource Group
az group create --name $resourceGroup --location $location

# Create Storage Account
az storage account create --name $storageAccount --resource-group $resourceGroup --location $location --sku Standard_LRS

# Create Cosmos DB
az cosmosdb create --name $cosmosAccount --resource-group $resourceGroup --locations regionName=$location failoverPriority=0

# Create Azure Function
az functionapp create --resource-group $resourceGroup --consumption-plan-location $location `
  --runtime python --functions-version 4 `
  --name $functionApp --storage-account $storageAccount

Write-Output "Infrastructure setup complete."

