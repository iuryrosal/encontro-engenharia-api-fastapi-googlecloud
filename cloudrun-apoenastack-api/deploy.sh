export PROJECT_ID=glowing-market-431616-d8
export APP=apoena-fastapi 
export REGION="southamerica-east1"
#export TAG="gcr.io/$PROJECT_ID/$APP"
export TAG="southamerica-east1-docker.pkg.dev/$PROJECT_ID/api-images/$APP"
# Set Default Project (all later commands will use it) 
gcloud config set project $PROJECT_ID

gcloud services enable cloudbuild.googleapis.com \
    containerregistry.googleapis.com \
    run.googleapis.com

#Region settings
gcloud config set run/region REGION

# Docker settings
gcloud auth configure-docker 

# É necessário ter a API da Compute Engine Habilitada
gcloud run deploy sample --port 8080 --source .