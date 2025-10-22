from django.test import TestCase
from Api.utils.csv_utils import distance_between_long_lat


class TestDistanceCalculation(TestCase):
    """
    Tests pour la fonction distance_between_long_lat
    Cette fonction calcule la distance entre deux points géographiques
    """
    
    def test_same_coordinates(self):
        """
        Test avec les mêmes coordonnées
        La distance doit être 0
        """
        # Arrange: Coordonnées identiques
        lon1, lat1 = 2.3522, 48.8566  # Paris
        lon2, lat2 = 2.3522, 48.8566  # Paris (même point)
        
        # Act: Calcul de la distance
        distance = distance_between_long_lat(lon1, lat1, lon2, lat2)
        
        # Assert: Vérification
        self.assertEqual(distance, 0.0, "La distance entre deux points identiques doit être 0")
    
    def test_paris_to_lyon(self):
        """
        Test avec Paris et Lyon
        Distance connue d'environ 392km
        """
        # Arrange: Coordonnées Paris et Lyon
        paris_lon, paris_lat = 2.3522, 48.8566  # Paris
        lyon_lon, lyon_lat = 4.8357, 45.7640    # Lyon
        
        # Act: Calcul de la distance
        distance = distance_between_long_lat(paris_lon, paris_lat, lyon_lon, lyon_lat)
        
        # Assert: Vérification avec tolérance
        expected_distance = 392  # km
        tolerance = 10  # km
        self.assertAlmostEqual(
            distance, 
            expected_distance, 
            delta=tolerance,
            msg=f"Distance Paris-Lyon attendue: ~{expected_distance}km, obtenue: {distance:.1f}km"
        )
    
    def test_short_distance(self):
        """
        Test avec une courte distance
        Vérifie que le calcul fonctionne pour de petites distances
        """
        # Arrange: Deux points très proches (quelques mètres)
        lon1, lat1 = 2.3522, 48.8566
        lon2, lat2 = 2.3523, 48.8566  # ~100m plus à l'est
        
        # Act: Calcul de la distance
        distance = distance_between_long_lat(lon1, lat1, lon2, lat2)
        
        # Assert: Vérification
        self.assertLess(distance, 1.0, "Distance courte doit être inférieure à 1km")
        self.assertGreater(distance, 0.0, "Distance doit être positive")
    
    def test_negative_coordinates(self):
        """
        Test avec des coordonnées négatives
        Vérifie que la fonction gère les coordonnées Ouest/Sud
        """
        # Arrange: Coordonnées avec longitude négative (Ouest)
        lon1, lat1 = -74.0060, 40.7128  # New York
        lon2, lat2 = -0.1276, 51.5074   # Londres
        
        # Act: Calcul de la distance
        distance = distance_between_long_lat(lon1, lat1, lon2, lat2)
        
        # Assert: Vérification
        self.assertGreater(distance, 0.0, "Distance doit être positive")
        self.assertLess(distance, 10000.0, "Distance New York-Londres doit être raisonnable")
