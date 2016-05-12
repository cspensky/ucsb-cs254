#!/usr/bin/python
import sys

import operator


class SingleBitBimodalPredictor:
    correct_predictions = 0.0
    missed_prediction = {}

    def __init__(self, num_entries):
        self.num_entries = num_entries
        self.bimod_table = [0] * self.num_entries

    def get_prediction(self, pc):
        index = (pc >> 2) % self.num_entries
        return self.bimod_table[index]

    def update(self, pc, branch_outcome):
        index = (pc >> 2) % self.num_entries
        self.bimod_table[index] = branch_outcome


class GlobalPredictor:
    correct_predictions = 0.0
    missed_prediction = {}

    def __init__(self, num_entries=4096):
        self.num_entries = num_entries
        self.bimod_table = [0] * self.num_entries

        self.global_state = 0
        self.global_mask = 0b111111111111

    def _get_index(self, pc):
        return ((pc >> 2) ^ self.global_state) & self.global_mask

    def get_prediction(self, pc):
        index = self._get_index(pc)
        return not self.bimod_table[index] & 0b10 == 0
        # return self.bimod_table[index]

    def update(self, pc, branch_outcome):

        index = self._get_index(pc)

        # Increment up to 3 and decrement down to 0
        if self.bimod_table[index] < 3 and branch_outcome == 1:
            self.bimod_table[index] += 1
        elif self.bimod_table[index] > 1 and branch_outcome == 0:
            self.bimod_table[index] -= 1

        # Update our global state
        self.global_state = self.global_state << 1 | branch_outcome
        self.global_state &= self.global_mask


class LocalPredictor:
    correct_predictions = 0.0
    missed_prediction = {}

    def __init__(self, num_entries=1024):
        self.num_entries = num_entries
        self.local_table = [0] * self.num_entries

        self.local_history = [0] * 256
        self.local_mask = 0b11111111

    def _get_index(self, pc):
        return (pc >> 2) % self.num_entries

    def get_prediction(self, pc):
        index = self._get_index(pc)
        return not self.local_history[self.local_table[index]] & 0b10 == 0

    def update(self, pc, branch_outcome):

        # Get our index into the history table
        index = self._get_index(pc)
        # Get our 8 bit history index
        history_index = self.local_table[index]

        prediction_value = self.local_history[history_index]
        # Increment up to 3 and decrement down to 0
        if prediction_value < 3 and branch_outcome == 1:
            prediction_value += 1
        elif prediction_value > 1 and branch_outcome == 0:
            prediction_value -= 1

        # Update our global state
        history_index = history_index << 1 | branch_outcome
        history_index &= self.local_mask
        self.local_history[history_index] = prediction_value


class TournamentPredictor:
    correct_predictions = 0.0
    missed_prediction = {}

    def __init__(self, num_entries=1024):
        self.num_entries = num_entries
        self.chooser_table = [0] * self.num_entries

        self.predictor_global = GlobalPredictor()
        self.predictor_local = LocalPredictor()

    def _get_index(self, pc):
        return (pc >> 2) % self.num_entries

    def get_prediction(self, pc):
        index = self._get_index(pc)

        if self.chooser_table[index] == 0 or self.chooser_table[index] == 1:
            return self.predictor_local.get_prediction(pc)
        else:
            return self.predictor_global.get_prediction(pc)

    def update(self, pc, branch_outcome):

        global_prediction = self.predictor_global.get_prediction(pc)
        local_prediction = self.predictor_local.get_prediction(pc)

        # Get our index into the history table
        index = self._get_index(pc)

        # Only update if we one was better
        if global_prediction != local_prediction:
            # Increment up to 3 and decrement down to 0
            if self.chooser_table[index] < 3 and \
                            global_prediction == branch_outcome:
                self.chooser_table[index] += 1
            elif self.chooser_table[index] > 1 and \
                            local_prediction == branch_outcome:
                self.chooser_table[index] -= 1

        # Update our global state
        self.predictor_global.update(pc, branch_outcome)
        self.predictor_local.update(pc, branch_outcome)


def main():
    predictors = [SingleBitBimodalPredictor(1024),
                  GlobalPredictor(),
                  LocalPredictor(),
                  TournamentPredictor()]

    total_predictions = 0
    _ = sys.stdin.readline()  # throw away first line
    for line in sys.stdin:
        # get the two fields and convert them to integers
        [pc, branch_outcome] = [int(x, 0) for x in line.split()]

        total_predictions += 1

        # Try all of our predictors
        for predictor in predictors:
            this_prediction = predictor.get_prediction(pc)
            if this_prediction == branch_outcome:
                predictor.correct_predictions += 1.0
            else:
                if pc in predictor.missed_prediction:
                    predictor.missed_prediction[pc] += 1
                else:
                    predictor.missed_prediction[pc] = 1
            predictor.update(pc, branch_outcome)


    # print out the statistics
    print "Total predictions: %d" % total_predictions
    for predictor in predictors:
        print "[%s]" % predictor.__class__.__name__

        missed_predictions = total_predictions - predictor.correct_predictions
        sorted_x = sorted(predictor.missed_prediction.items(), key=operator.itemgetter(1))
        print "- Most missed PC: 0x%08x (%d times)" % (sorted_x[-1][0],
                                                   sorted_x[-1][1])

        print "- Correct: %d (%f%%)" % (predictor.correct_predictions,
                                       100 * predictor.correct_predictions / total_predictions)
        print "- Missed: %d (%f%%)" % (missed_predictions,
                                      100 * missed_predictions / total_predictions)


if __name__ == "__main__":
    main()
