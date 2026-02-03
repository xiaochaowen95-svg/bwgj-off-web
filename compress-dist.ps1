# PowerShell script to compress the dist folder into a zip file

# Check if dist folder exists
if (Test-Path ".\dist") {
    # Compress the dist folder
    Compress-Archive -Path ".\dist\*" -DestinationPath ".\dist.zip" -Force
    Write-Host "Successfully compressed dist folder to dist.zip"
} else {
    Write-Host "Error: dist folder does not exist. Please run 'npm run build' first."
}