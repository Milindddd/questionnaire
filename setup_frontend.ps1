# Check if Angular CLI is installed
$ngVersion = ng version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing Angular CLI globally..."
    npm install -g @angular/cli
}

# Create new Angular project
Set-Location frontend
ng new mform-upload --style=scss --routing=true --skip-git --minimal=true

# Navigate into project directory
Set-Location mform-upload

# Add Angular Material
ng add @angular/material --theme=custom --typography=true --animations=true

# Install additional dependencies
npm install @angular/flex-layout
npm install file-saver

# Create core components and services
ng generate module core
ng generate module shared
ng generate component components/file-upload
ng generate component components/form-preview
ng generate service services/form-parser

Write-Host "Frontend setup complete!" 