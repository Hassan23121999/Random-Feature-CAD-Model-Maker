import cadquery as cq
import tkinter as tk
from tkinter import filedialog, simpledialog
import random

# Define possible features to apply
features = ['chamfer', 'fillet', 'hole', 'boss', 'taper', 'rib']  # Removed 'draft' because it's not directly supported

def random_features():
    # Randomly generate dimensions
    length, width, height = random.randint(50, 150), random.randint(50, 150), random.randint(20, 100)
    box = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))  # Ensure Z-min is at origin for tapering

    # Randomly decide features to apply
    chosen_features = random.sample(features, random.randint(2, 4))  # Choose 2-4 random features

    for feature in chosen_features:
        try:
            if feature == 'chamfer':
                box = box.edges().chamfer(random.randint(1, 3))
            elif feature == 'fillet':
                box = box.edges().fillet(random.randint(1, 3))
            elif feature == 'hole':
                box = box.faces(">Z").workplane().hole(random.randint(5, 20))
            elif feature == 'boss':
                boss_height = random.randint(5, 20)
                boss_diameter = random.randint(10, 30)
                box = box.faces(">Z").workplane().circle(boss_diameter / 2).extrude(boss_height)
            elif feature == 'taper':
                taper_angle = random.randint(1, 10)
                taper_height = random.randint(10, 30)
                taper_width = random.randint(10, 30)
                box = box.faces(">Z").workplane().rect(taper_width, taper_height).extrude(height / 2, taper=taper_angle)
            elif feature == 'rib':
                rib_width = random.randint(5, 10)
                box = box.faces(">Z").workplane().rect(length - 10, rib_width).extrude(height / 2)
        except Exception as e:
            print(f"Failed to apply {feature} due to: {str(e)}")

    return box


def save_models():
    num_files = simpledialog.askinteger("Input", "How many STEP files would you like to generate?", minvalue=1, maxvalue=100000000)

    if num_files:
        folder_path = filedialog.askdirectory(title="Select a Folder to Save the STEP Files")
        
        if folder_path:
            for i in range(num_files):
                model = random_features()
                file_path = f"{folder_path}/model_{i+1}.step"
                model.val().exportStep(file_path)
                print(f"Saved STEP file at {file_path}")

# Setup the Tkinter window
root = tk.Tk()
root.title("Generate Random CAD Models")

# Button to start the process
start_button = tk.Button(root, text="Generate and Save Models", command=save_models)
start_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
