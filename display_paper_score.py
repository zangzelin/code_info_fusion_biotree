import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# 1. Set the plot style (use a clean style commonly seen in AI conference papers)
plt.style.use('classic')  # You can also use 'ggplot' or other styles as needed

# Configure global rc parameters for figures, fonts, and other settings
matplotlib.rcParams.update({
    "figure.dpi": 300,                 # Increase the resolution of the figure
    "savefig.dpi": 300,                # Set the resolution for saved figures
    "font.family": "serif",            # Use serif fonts (e.g., Times New Roman); for sans-serif, set to 'sans-serif'
    "font.size": 14,                   # Set the global font size
    "axes.labelsize": 16,              # Font size for axis labels
    "axes.titlesize": 16,              # Font size for titles
    "xtick.labelsize": 12,             # Font size for x-axis tick labels
    "ytick.labelsize": 12,             # Font size for y-axis tick labels
    "legend.fontsize": 12,             # Font size for legends
    "axes.linewidth": 1.2              # Line width for axes
})

# 2. Load data
# Load the data from a CSV file. The file is expected to have three columns:
# Column 1: Index, Column 2: Year, Column 3: Score
data = np.loadtxt('paper_score.csv', delimiter=',')

# Group the data by year and calculate the average score for each year
dict_year_score = {}
for i in range(len(data)):
    index = data[i][0]  # Index of the data (not used in this calculation)
    year = data[i][1]   # Year of publication
    score = data[i][2]  # Relevance score
    
    # Organize scores by year
    if year in dict_year_score:
        dict_year_score[year].append(score)
    else: 
        dict_year_score[year] = [score]

# Sort years and calculate the average score for each year
year_list = sorted(dict_year_score.keys())  # Sort the years in ascending order
x_list = []  # List to store years
y_list = []  # List to store the average scores

for year in year_list:
    scores = np.array(dict_year_score[year])  # Get all scores for the given year
    scores = scores[scores >= 0]  # Filter out any negative scores
    if year > 1980 and year < 2025:  # Only consider data between 1980 and 2025
        x_list.append(year)
        y_list.append(np.mean(scores))  # Calculate the average score for the year

# 3. Plot the data
fig, ax = plt.subplots(figsize=(7, 4))  # Create a figure and axis with specified size
colors = cm.tab10.colors  # Use a predefined color palette

# Create a bar chart
ax.bar(
    x_list,  # Years (x-axis)
    y_list,  # Average scores (y-axis)
    color=colors[4],  # Set the color for the bars
    label='Average Relevance of Papers on Cell Differentiation and Phylogenetic Trees (Published in Cell, Nature, and Science)'
)

# 4. Beautify the plot
# Remove the top and right spines for a cleaner look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Set axis labels
ax.set_xlabel('Year', fontsize=16, labelpad=8)  # Label for the x-axis
ax.set_ylabel("Relevance of Reference to Information Fusion", fontsize=16, labelpad=8)  # Label for the y-axis

# Adjust the x-axis range to include some padding
ax.set_xlim(min(x_list) - 1, max(x_list) + 1)

# Set x-axis ticks to display every 5 years
year_ticks = np.arange(min(x_list), max(x_list) + 1, 5)  # Generate ticks every 5 years
year_labels = [str(int(year)) for year in year_ticks]  # Convert years to strings for labels
ax.set_xticks(year_ticks)  # Set the ticks on the x-axis
ax.set_xticklabels(year_labels, rotation=45, ha='right')  # Rotate labels 45 degrees for better readability

# Customize tick size and line width
ax.tick_params(axis='both', which='major', length=5, width=1.1)

# Add a legend to the plot
ax.legend(loc='upper left', frameon=False)  # Place the legend in the upper-left corner without a frame
ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)  # Add a light grid for better readability

# 5. Adjust layout and save the figure
plt.tight_layout()  # Automatically adjust the layout to prevent overlap
plt.savefig('average_score_analysis.pdf', dpi=300)  # Save the figure as a high-resolution PDF
# Uncomment the following line to display the plot interactively
# plt.show()
