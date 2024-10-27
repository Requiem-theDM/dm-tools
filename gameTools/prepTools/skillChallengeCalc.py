#!/usr/bin/env python3

import argparse as ap
import numpy as np

def parseargs():
    parser = ap.ArgumentParser(description='Simulates how likely a party is to succeed on a skill challenge based on its length and their average ability score value.')
    parser.add_argument('successesRequired',help='Sets the number of required successes.')
    parser.add_argument('averageAbility',help='Sets the average ability score of the party.')
    args = parser.parse_args()
    return args

def skillChallengeSim(successesRequired,averageAbility):
    def run_trial():
            success_count = 0
            failure_count = 0
            ability_usage = [0] * 6
            while success_count < success_goal and failure_count < 3:
                success_rates = [
                    max(initial_success_rate - (useage * 0.05),0)
                    for useage in ability_usage
                ]
                chosen_ability = np.argmax(success_rates)
                if np.random.rand() < success_rates[chosen_ability]:
                    success_count += 1
                else:
                    failure_count += 1
                ability_usage[chosen_ability] += 1
            return success_count >= success_goal
    success_goal = int(successesRequired)
    initial_success_rate = float(int(averageAbility)/20)
    successes = sum(run_trial() for _ in range(10000))
    success_probability = format(successes / 10000 * 100,'.2f')
    print(f"The party's chance of success is {success_probability} %.")


def main():
    args = parseargs()
    skillChallengeSim(args.successesRequired,args.averageAbility)

if __name__ == "__main__":
    main()