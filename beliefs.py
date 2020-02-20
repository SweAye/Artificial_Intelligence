# ----------------------------------------------------------------------
# Name:     beliefs
# Purpose:  Probabilistic inference with Bayes' Rule (Belief system)
# ----------------------------------------------------------------------

import utils


class Belief(object):
    """
    Belief class used to track the belief distribution based on the
    sensing evidence.

    """

    def __init__(self, size):
        # Initially all positions are open - have not been observed
        self.open = {(x, y) for x in range(size)
                     for y in range(size)}

        self.current_distribution = {pos: 1 / (size ** 2) for pos in self.open}

    def update(self, color, sensor_position, model):

        """
                Update the belief distribution based on new evidence:  agent
                detected the given color at sensor location: sensor_position.
                :param color: (string) color detected
                :param sensor_position: (tuple) position of the sensor
                :param model (Model object) models the relationship between the
                     treasure location and the sensor data
                :return: None
        """
        pro = []
        for square in self.current_distribution:
            prior_pro = self.current_distribution[square]
            pro_sensor = model.psonargivendist(color, utils.manhattan_distance(sensor_position, square))
            probability = (prior_pro * pro_sensor)
            pro.append(probability)
            self.current_distribution[square] = probability
        total_probability = sum(pro)
        # normalization
        if total_probability > 0:
            for square in self.current_distribution:
                self.current_distribution[square] = ((self.current_distribution.get(square)) / total_probability)

        self.open.remove(sensor_position)

    def recommend_sensing(self):

        unobserved_probability = {}
        observed_probability = {}

        if self.open is not None:
            for square in self.open:
                unobserved_probability[square] = self.current_distribution[square]


        for square in self.current_distribution:
            if square not in self.open:
                observed_probability[square] = self.current_distribution[square]


        if unobserved_probability is not None:
            all_Zero = all(pro == 0 for pro in unobserved_probability.values())


        if len(self.open)>0:  # if there are no more square in the self.open

            if all_Zero:  # all remaining unobserved square has probability of 0
                print ("All Zero: self.open:", self.open)
                # return the unobserved location that is closest to the(observed) location with he highest probablity.

                if observed_probability is not None:
                    high_observed = max(observed_probability, key=lambda x: observed_probability[x])
                    return utils.closest_point(high_observed,self.open)

            else:

                if unobserved_probability is not None:
                    return max(unobserved_probability, key=lambda x: unobserved_probability[x])

        else:

            return max(observed_probability, key=lambda x: observed_probability[x])
