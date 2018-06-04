from django.test import TestCase

from .models import Patient

# Create your tests here.

class PatientModelTests(TestCase):

    def test_bmi(self):
        """
        test bmi calc
        """
        patient = Patient(height=63, weight=125)
        self.assertEqual(patient.bmi, 22.68)