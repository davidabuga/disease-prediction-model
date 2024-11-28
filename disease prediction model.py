# Import necessary libraries for GUI, graphs, and numerical operations
import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Button
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Define a dictionary containing diseases, stages, and their respective symptoms
disease_symptoms = {
    "Malaria": {
        "Mild": ["Headache", "Nausea", "Fatigue", "Mild fever"],
        "Severe": ["High fever", "Chills", "Sweating", "Seizures"],
    },
    "Dengue Fever": {
        "Mild": ["Joint pain", "Rash"],
        "Severe": ["Severe abdominal pain", "Bleeding gums", "Persistent vomiting", "Shock"],
    },
    "Tuberculosis": {
        "Latent": ["No symptoms or mild cough"],
        "Active": ["Chronic cough", "Chest pain", "Weight loss", "Night sweats"],
    },
    "Typhoid": {
        "Early": ["Weakness", "Stomach pain"],
        "Severe": ["Diarrhea", "Confusion", "Rashes"],
    },
    "Pneumonia": {
        "Mild": ["Cough", "Mild fever", "Shortness of breath"],
        "Severe": ["Chest pain", "High fever", "Bluish lips", "Confusion"],
    },
    "Measles": {
        "Early": ["Runny nose", "Red eyes", "Sore throat"],
        "Severe": ["Skin rashes", "Persistent fever", "Ear infections", "Pneumonia"],
    },
    "Meningitis": {
        "Bacterial": ["Severe headache", "Stiff neck", "Sensitivity to light"],
        "Viral": ["Mild fever", "Fatigue", "Neck pain", "Headache"],
    },
    "Influenza": {
        "Common": ["Cough", "Sore throat", "Muscle aches"],
        "Severe": ["Persistent chest pain", "Severe fatigue", "Confusion"],
    },
    "Chickenpox": {
        "Early": ["Itchy skin", "Fatigue", "Loss of appetite"],
        "Severe": ["Widespread rashes", "Blisters", "Infections"],
    },
    "Hepatitis B": {
        "Acute": ["Jaundice", "Dark urine", "Fatigue"],
        "Chronic": ["Abdominal pain", "Loss of appetite", "Liver damage"],
    },
}

# Define the textual recommendations for different severity levels
response_texts = {
    "Urgent Action Needed": "Critical symptoms detected. Seek immediate medical attention.",
    "Highly Recommended Action": "Symptoms suggest illness. Consult a doctor soon.",
    "Might Need Action": "Symptoms may indicate a health issue. Monitor and seek medical advice if needed.",
}

# Map severity levels to numerical values for graph plotting
rate_mapping = {
    "Might Need Action": 25,
    "Highly Recommended Action": 50,
    "Urgent Action Needed": 75,
}

# Flatten the nested disease-symptoms dictionary for easier GUI handling
flat_symptoms = []
for disease, stages in disease_symptoms.items():
    for stage, symptoms in stages.items():
        for symptom in symptoms:
            # Create a flat list of (symptom, disease, stage) tuples
            flat_symptoms.append((symptom, disease, stage))

# Function to display a graph of disease infection rates based on recommendations
def show_graph(recommendations):
    diseases = list(recommendations.keys())  # Get the list of diseases with recommendations
    might_need_action = []
    highly_recommended_action = []
    urgent_action_needed = []

    # Process the severity levels for each disease
    for disease in diseases:
        might = 0
        high = 0
        urgent = 0
        for stage, action in recommendations[disease].items():
            if action == "Might Need Action":
                might += rate_mapping[action]
            elif action == "Highly Recommended Action":
                high += rate_mapping[action]
            elif action == "Urgent Action Needed":
                urgent += rate_mapping[action]
        might_need_action.append(might)
        highly_recommended_action.append(high)
        urgent_action_needed.append(urgent)

    # Create a bar chart
    x = np.arange(len(diseases))  # Set positions for bars

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x, might_need_action, label="Might Need Action", color="yellow")
    ax.bar(x, highly_recommended_action, bottom=might_need_action, label="Highly Recommended Action", color="orange")
    ax.bar(
        x,
        urgent_action_needed,
        bottom=[i + j for i, j in zip(might_need_action, highly_recommended_action)],
        label="Urgent Action Needed",
        color="red",
    )

    ax.set_xticks(x)
    ax.set_xticklabels(diseases, rotation=45, ha="right")  # Label the bars with disease names
    ax.set_ylabel("Infection Rate (%)")
    ax.set_title("Infection Rates by Disease and Severity")
    ax.legend()

    # Show the graph in a new window
    graph_window = Toplevel(root)
    graph_window.title("Graphical Representation")
    graph_window.geometry("900x600")

    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    Button(graph_window, text="Close", command=graph_window.destroy, font=("Arial", 12)).pack(pady=10)

# Function to evaluate selected symptoms and provide recommendations
def evaluate():
    selected_symptoms = symptom_listbox.curselection()  # Get the indices of selected symptoms
    recommendations = {}

    # Match the selected symptoms to diseases and stages
    for i in selected_symptoms:
        selected_symptom = symptom_listbox.get(i)  # Get the symptom string
        for disease, stages in disease_symptoms.items():
            for stage, symptoms in stages.items():
                if selected_symptom in symptoms:
                    if disease not in recommendations:
                        recommendations[disease] = {}
                    if stage in ["Mild", "Early", "Latent"]:
                        recommendations[disease][stage] = "Might Need Action"
                    elif stage in ["Common", "Acute"]:
                        recommendations[disease][stage] = "Highly Recommended Action"
                    else:
                        recommendations[disease][stage] = "Urgent Action Needed"

    # Check if at least two diseases are matched
    if len(recommendations) < 2:
        messagebox.showinfo("Recommendations", "Please select more symptoms to get recommendations for at least two diseases.")
    else:
        # Prepare a string of results to display
        result = "\n".join(f"{disease} ({stage}): {action}" for disease, stages in recommendations.items() for stage, action in stages.items())
        
        # Show recommendations in a popup window
        popup = Toplevel(root)
        popup.title("Recommendations")
        popup.geometry("400x300")
        Label(popup, text="Your Recommendations:", font=("Arial", 14, "bold")).pack(pady=10)
        Label(popup, text=result, font=("Arial", 12), wraplength=380, justify="left").pack(pady=10)
        Button(popup, text="Show Graph", command=lambda: show_graph(recommendations), font=("Arial", 12)).pack(pady=10)
        Button(popup, text="Close", command=popup.destroy, font=("Arial", 12)).pack(pady=10)

# Set up the main tkinter window
root = tk.Tk()
root.title("Symptom Checker")  # Set the window title
root.geometry("800x600")  # Set the window size
root.configure(bg="blue")  # Set background color

# Create a frame to hold widgets
main_frame = tk.Frame(root, bg="blue")
main_frame.pack(fill="both", expand=True)

# Populate the listbox with symptoms
symptoms = [symptom for symptom, disease, stage in flat_symptoms]
symptom_listbox = tk.Listbox(main_frame, selectmode=tk.MULTIPLE, width=40, height=10, font=("Arial", 14))
for symptom in symptoms:
    symptom_listbox.insert(tk.END, symptom)  # Add each symptom to the listbox
symptom_listbox.pack(pady=20)

# Add an "Evaluate" button to trigger the evaluation process
Button(main_frame, text="Evaluate", command=evaluate, font=("Arial", 14)).pack(pady=20)

# Start the tkinter event loop
root.mainloop()
