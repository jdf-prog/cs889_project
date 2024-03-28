# Correcting the task assignment as per the clarified requirements
# Creating a comprehensive plan where each of the 12 participants completes all 9 tasks across the 3 devices


import numpy as np

# Function to generate a Latin Square
def generate_latin_square(n):
    """Generates a Latin Square of size n x n."""
    return np.array([(np.arange(n) + i) % n for i in range(n)])

# Generate the 3x3 Latin Square
latin_square_3x3 = generate_latin_square(3)

# Replicate the Latin Square four times to cover 12 participants
# Each row in this matrix will correspond to a sequence for a participant
participant_sequences = np.tile(latin_square_3x3, (4, 1))

# Randomize device order within each sequence to ensure each participant gets a unique sequence
# Assuming devices are represented as 0, 1, 2
np.random.seed(42)  # For reproducibility
for sequence in participant_sequences:
    np.random.shuffle(sequence)

print(participant_sequences)

# Task IDs for easy (1-3), medium (4-6), and hard (7-9) levels
tasks_easy = np.array([1, 2, 3])
tasks_medium = np.array([4, 5, 6])
tasks_hard = np.array([7, 8, 9])

# Create a plan for all 12 participants
final_corrected_plan = []

# Loop through each participant
for p in range(1, 13):
    # Shuffle tasks within each difficulty level for variety
    np.random.shuffle(tasks_easy)
    np.random.shuffle(tasks_medium)
    np.random.shuffle(tasks_hard)

    # Assign tasks to each device for the participant
    for device in range(1, 4):
        participant_tasks = {
            f'Participant {p}, Device {device}': [f'Task-{tasks_easy[device - 1]}',
                                                  f'Task-{tasks_medium[device - 1]}',
                                                  f'Task-{tasks_hard[device - 1]}']
        }
        final_corrected_plan.append(participant_tasks)

# Convert the final plan into a structured form for display
structured_output_final = []
for participant_plan in final_corrected_plan:
    for key, tasks in participant_plan.items():
        participant, device = key.split(', ')
        for task in tasks:
            structured_output_final.append({
                "Participant": participant,
                "Device": device,
                "Task": task
            })

# Display the final corrected plan for all participants
df_final_corrected = pd.DataFrame(structured_output_final)
reshaped_df_final_corrected = df_final_corrected.pivot_table(index='Participant', columns='Device', values='Task',
                                                             aggfunc=lambda x: ' | '.join(x))
reshaped_df_final_corrected.head(12)  # Displaying the plan for all 12 participants
