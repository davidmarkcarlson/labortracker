import math
from django.db import models
from .choices import DELIVERY_TYPES

#https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3212654/
traverseTimesNulli = [[5.6, 3.4, 2.4, 1.8, 1.6, 1.9],
                    [6.0, 3.5, 2.4, 1.8, 1.6, 2.0],
                    [6.3, 3.7, 2.5, 1.8, 1.6, 2.1],
                    [7.2, 4.2, 2.7, 2.0, 1.6, 2.2],
                    [9.0, 5.9, 3.0, 2.0, 1.7, 2.2]]

traverseTimesMulti = [[5.4, 2.7, 1.6, 1.1, 0.9, 0.8],
                    [5.3, 2.7, 1.6, 1.1, 0.9, 0.8],
                    [5.6, 2.7, 1.6, 1.1, 0.9, 0.8],
                    [5.7, 2.9, 1.7, 1.1, 0.9, 0.9],
                    [6.8, 2.9, 1.8, 1.1, 0.9, 0.9]]

bmiRanges = [[0, 25.0],
            [25.0, 30.0],
            [30.0, 35.0],
            [35.0, 40.0],
            [40.0, math.inf]]

def get_traverse_times(patient):
    bmi = patient.bmi
    # use correct data set for nulliparas vs multiparas
    times = traverseTimesMulti if patient.vaginal_births >= 1 else traverseTimesNulli
    for i in range(len(bmiRanges)):
        r = bmiRanges[i]
        if r[0] <= bmi < r[1]:
            return times[i]
    raise Exception("unable to get bmi range for value: " + str(bmi))

class Partograph(models.Model):
    patient = models.ForeignKey('authentication.Patient', on_delete=models.CASCADE)
    provider = models.ForeignKey('authentication.Practitioner', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    # Store Finalized Data to complete Partograph
    delivery_time = models.DateTimeField(blank=True, null=True)
    delivery_type = models.IntegerField(choices=DELIVERY_TYPES, null=True)
    caesarian = models.BooleanField(default=False)
    cs_decision_time = models.DateTimeField(null=True)
    initial_apgar = models.CharField(max_length=255, null=True)
    live_birth = models.BooleanField(default=False)
    newborn_weight_lbs = models.IntegerField(null=True)
    newborn_weight_oz = models.IntegerField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_dystocia_points(self):
        traverseTimes = get_traverse_times(self.patient)
        points = [{'x':traverseTimes[0], 'y':4}] 
        dilationStart = 5
        previous = 0
        for i in range(len(traverseTimes)):
            time = traverseTimes[i]
            if i == 0:
                points.append({'x':time, 'y':dilationStart})
            else:
                points.append({'x':time+previous, 'y':dilationStart+i})
            previous = time+previous
        return points


class PartoMeasure(models.Model):
    partograph = models.ForeignKey(Partograph, on_delete=models.CASCADE)
    dilation_cm = models.SmallIntegerField()
    descent = models.IntegerField()  # Stores Descent of Fetal Head
    station = models.CharField(max_length=255)
    time_since_active_labor = models.DurationField()
    # TODO Evaluate
    updated_at = models.DateTimeField(auto_now=True)
    time_taken = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
