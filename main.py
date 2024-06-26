import uvicorn
import pandas as pd
from pydantic import BaseModel, condecimal, validator
from typing import Optional, ClassVar
from fastapi import FastAPI, HTTPException
from joblib import load
import os
import logging
import requests
import io

# Configuration du journal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Définition de l'application FastAPI
description = """
API pour estimer le prix de location d'une voiture en fonction de ses caractéristiques.
"""

tags_metadata = [
    {"name": "Échantillons de voitures", "description": "Afficher des échantillons aléatoires de voitures."},
    {"name": "Recherche de modèle", "description": "Récupérer les données d'un modèle de voiture spécifique."},
    {"name": "Apprentissage automatique", "description": "Prédire le prix de location basé sur les caractéristiques de la voiture."}
]

app = FastAPI(
    title="API de prédiction des prix Getaround",
    description=description,
    version="0.1",
    openapi_tags=tags_metadata
)

# Chargement des données CSV depuis une URL
def load_csv_from_url(url: str) -> pd.DataFrame:
    """
    Charge un fichier CSV depuis une URL.

    Args:
        url (str): L'URL du fichier CSV.

    Returns:
        pd.DataFrame: Le dataframe contenant les données CSV.

    Raises:
        HTTPException: En cas d'erreur lors du chargement du fichier CSV.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lève une exception pour les codes d'état HTTP incorrects
        return pd.read_csv(io.BytesIO(response.content))
    except requests.RequestException as e:
        logger.error(f"Erreur lors du chargement du CSV depuis {url}: {e}")
        raise HTTPException(status_code=500, detail="Échec du chargement du fichier CSV")

# Chargement des données CSV au démarrage de l'application
file_url = "https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv"
try:
    cars = load_csv_from_url(file_url)
except HTTPException as e:
    logger.error(f"Erreur HTTP lors du chargement du CSV : {e}")
    raise

# Définition des endpoints FastAPI

@app.get("/", tags=["Documentation"])
async def root():
    """
    Endpoint racine de l'API.

    Returns:
        dict: Les informations sur les endpoints disponibles.
    """
    return {
        "message": "Bienvenue sur l'API de prédiction des prix Getaround.",
        "endpoints": [
            {"endpoint": "/sample_cars", "description": "Afficher des échantillons aléatoires de voitures."},
            {"endpoint": "/search_model_key/{model_key}", "description": "Récupérer les données d'un modèle de voiture spécifique."},
            {"endpoint": "/predict", "description": "Prédire le prix de location basé sur les caractéristiques de la voiture."},
            {"endpoint": "/docs", "description": "Documentation Swagger UI."},
        ]
    }

@app.get("/sample_cars", tags=["Échantillons de voitures"])
async def sample_cars():
    """
    Endpoint pour récupérer des échantillons aléatoires de voitures.

    Returns:
        dict: Un dictionnaire représentant les échantillons de voitures.
    """
    try:
        sample_cars = cars.sample(5)
        return sample_cars.to_dict("index")
    except Exception as e:
        logger.error(f"Erreur lors du chargement des échantillons de voitures : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@app.get("/search_model_key/{model_key}", tags=["Recherche de modèle"])
async def search_model_key(model_key: str):
    """
    Endpoint pour rechercher les données d'un modèle de voiture spécifique.

    Args:
        model_key (str): La clé du modèle de voiture à rechercher.

    Returns:
        dict: Les données du modèle de voiture spécifique.
    """
    try:
        rental_model = cars[cars["model_key"] == model_key]
        if rental_model.empty:
            raise HTTPException(status_code=404, detail="Modèle non trouvé")
        return rental_model.to_dict("index")
    except Exception as e:
        logger.error(f"Erreur lors de la recherche du modèle {model_key} : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

class Features(BaseModel):
    """
    Modèle pour les caractéristiques d'une voiture utilisé pour prédire le prix de location.
    """
    model_key: str
    mileage: condecimal(gt=0, decimal_places=2)
    engine_power: condecimal(gt=0, decimal_places=2)
    fuel: str
    paint_color: str
    car_type: str
    private_parking_available: Optional[bool]
    has_gps: Optional[bool]
    has_air_conditioning: Optional[bool]
    automatic_car: Optional[bool]
    has_getaround_connect: Optional[bool]
    has_speed_regulator: Optional[bool]
    winter_tires: Optional[bool]
    
    protected_namespaces: ClassVar = ()

    @validator('mileage', 'engine_power')
    def check_range(cls, v):
        """
        Validator pour vérifier que la valeur est positive.
        """
        if v < 0:
            raise ValueError('doit être non négatif')
        return v
    
    @validator('fuel')
    def validate_fuel(cls, v):
        """
        Validator pour valider le type de carburant.
        """
        valid_fuels = ['diesel', 'petrol', 'hybrid_petrol', 'electro']
        if v.lower() not in valid_fuels:
            raise ValueError(f"Type de carburant '{v}' non valide. Les valeurs valides sont : {', '.join(valid_fuels)}")
        return v.lower()
    
    @validator('paint_color')
    def validate_paint_color(cls, v):
        """
        Validator pour valider la couleur de peinture.
        """
        valid_colors = ['black', 'white', 'red', 'silver', 'grey', 'blue', 'orange','beige', 'brown', 'green']
        if v.lower() not in valid_colors:
            raise ValueError(f"Couleur de peinture '{v}' non valide. Les couleurs valides sont : {', '.join(valid_colors)}")
        return v.lower()
    
    @validator('car_type')
    def validate_car_type(cls, v):
        """
        Validator pour valider le type de voiture.
        """
        valid_types = ['sedan', 'hatchback', 'suv', 'van', 'estate', 'convertible', 'coupe', 'subcompact']
        if v.lower() not in valid_types:
            raise ValueError(f"Type de voiture '{v}' non valide. Les types valides sont : {', '.join(valid_types)}")
        return v.lower()

@app.post("/predict", tags=["Apprentissage automatique"])
async def predict(features: Features):
    """
    Endpoint pour prédire le prix de location d'une voiture basé sur ses caractéristiques.

    Args:
        features (Features): Les caractéristiques de la voiture pour prédire le prix.

    Returns:
        dict: La prédiction du prix de location.
    """
    try:
        data = pd.DataFrame([features.dict()])
        model_path = os.path.join("model", "my_mod_xg.joblib")
        
        # Journalisation pour suivre le chargement du modèle
        logger.info(f"Chargement du modèle depuis {model_path}")
        loaded_model = load(model_path)
        
        # Journalisation pour suivre la prédiction
        logger.info("Effectuer la prédiction...")
        prediction = loaded_model.predict(data)
        
        return {"prédiction": prediction.tolist()[0]}
    except Exception as e:
        logger.error(f"Erreur lors de la prédiction : {e}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

# Lancement de l'application FastAPI avec Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
