import argparse
import pandas as pd
import numpy as np
import os

def topsis(matrix, weights, impacts):

    matrix = np.array(matrix, dtype=float)
    weights = np.array(weights, dtype=float)
    
    normalized_matrix = matrix / np.sqrt((matrix ** 2).sum(axis=0))

    weighted_matrix = normalized_matrix * weights

    ideal_best = [
        max(weighted_matrix[:, i]) if impacts[i] == '+' else min(weighted_matrix[:, i])
        for i in range(len(impacts))
    ]
    ideal_worst = [
        min(weighted_matrix[:, i]) if impacts[i] == '+' else max(weighted_matrix[:, i])
        for i in range(len(impacts))
    ]

    distance_best = np.sqrt(((weighted_matrix - ideal_best) ** 2).sum(axis=1))
    distance_worst = np.sqrt(((weighted_matrix - ideal_worst) ** 2).sum(axis=1))

    scores = distance_worst / (distance_best + distance_worst)

    # ranks = scores.argsort()[::-1] + 1

    sorted_indices = np.argsort(scores)[::-1]
    print(sorted_indices)
    rank = np.empty_like(sorted_indices)

    rank_value = 1
    for i, idx in enumerate(sorted_indices):
        if i > 0 and scores[sorted_indices[i]] != scores[sorted_indices[i - 1]]:
            rank_value = i + 1
        rank[idx] = rank_value

    print(rank)

    return scores, rank


def main():
    parser = argparse.ArgumentParser(description="Perform TOPSIS analysis on a dataset.")
    parser.add_argument("input_file", help="Path to the input dataset (CSV format).")
    parser.add_argument("weights", help="Comma-separated weights (e.g., 1,2,1,1).")
    parser.add_argument("impacts", help="Comma-separated impacts (e.g., +,+,-,+).")
    parser.add_argument("output_file", help="Path to save the output results (CSV format).")
    args = parser.parse_args()

    if not os.path.isfile(args.input_file):
        print("Error: The specified input file does not exist.")
        return
    try:
        data = pd.read_csv(args.input_file)
    except Exception as e:
        print(f"Error: Could not read the input file. {e}")
        return

    print("Data loaded successfully:")
    print(data)
    print(f"Matrix dimensions (rows, criteria): {data.iloc[:, 1:].shape}")

    if data.shape[1] < 3:
        print("Error: The input file must contain at least three columns (one for alternatives and others for criteria).")
        return

    try:
        weights = list(map(float, args.weights.split(',')))
        impacts = args.impacts.split(',')
    except ValueError:
        print("Error: Weights must be numerical and impacts must be '+' or '-'.")
        return

    if len(weights) != data.shape[1] - 1 or len(impacts) != data.shape[1] - 1:
        print(f"Debug: Number of criteria: {data.shape[1] - 1}")
        print(f"Debug: Number of weights provided: {len(weights)}")
        print(f"Debug: Number of impacts provided: {len(impacts)}")
        print("Error: The number of weights and impacts must match the number of criteria.")
        return

    if not all(i in ['+', '-'] for i in impacts):
        print("Error: Impacts must only contain '+' or '-'.")
        return
    
    try:
        matrix = data.iloc[:, 1:].values
        scores, ranks = topsis(matrix, weights, impacts)
    except Exception as e:
        print(f"Error: An issue occurred while performing TOPSIS. {e}")
        return

    data["Topsis Score"] = scores
    data["Rank"] = ranks

    try:
        data.to_csv(args.output_file, index=False)
        print(f"Results successfully saved to {args.output_file}.")
    except Exception as e:
        print(f"Error: Unable to save the output file. {e}")

if __name__ == "__main__":
    main()
