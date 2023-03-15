import data_collection
import data_preprocessing
import model_training
import results_analysis
import pandas as pd
from tqdm import tqdm
import time

# Set the desired YouTube channel URL
channel_url = "https://www.youtube.com/c/ExampleChannel/videos"

# Set up the Chrome driver
driver = data_collection.setup_chrome_driver()

# Get video URLs
video_urls = data_collection.get_video_urls_from_channel(driver, channel_url)

# Initialize progress bar
total_steps = 6
progress_bar = tqdm(total=total_steps, desc="Overall progress")

# Collect video metadata
video_metadata_list = []
start_time = time.time()

for video_url in video_urls:
    video_metadata = data_collection.collect_video_metadata(driver, video_url)
    video_metadata_list.append(video_metadata)

progress_bar.update(1)
elapsed_time = time.time() - start_time
remaining_time = (elapsed_time / progress_bar.n) * (progress_bar.total - progress_bar.n)
progress_bar.set_postfix(remaining_time="{:.1f}s".format(remaining_time), refresh=False)

# Quit the Chrome driver
data_collection.quit_chrome_driver(driver)

# Convert the video metadata list to a pandas DataFrame
metadata_df = pd.DataFrame(video_metadata_list)

# Save the metadata to a CSV file
metadata_df.to_csv("video_metadata.csv", index=False)
progress_bar.update(1)
elapsed_time = time.time() - start_time
remaining_time = (elapsed_time / progress_bar.n) * (progress_bar.total - progress_bar.n)
progress_bar.set_postfix(remaining_time="{:.1f}s".format(remaining_time), refresh=False)

# Preprocess the data
preprocessed_data = data_preprocessing.preprocess_data(metadata_df)
progress_bar.update(1)
elapsed_time = time.time() - start_time
remaining_time = (elapsed_time / progress_bar.n) * (progress_bar.total - progress_bar.n)
progress_bar.set_postfix(remaining_time="{:.1f}s".format(remaining_time), refresh=False)

# Train the model
trained_model = model_training.train_model(preprocessed_data)
progress_bar.update(1)
elapsed_time = time.time() - start_time
remaining_time = (elapsed_time / progress_bar.n) * (progress_bar.total - progress_bar.n)
progress_bar.set_postfix(remaining_time="{:.1f}s".format(remaining_time), refresh=False)

# Analyze the results
results_analysis.analyze_results(trained_model, preprocessed_data)
progress_bar.update(1)
elapsed_time = time.time() - start_time
remaining_time = (elapsed_time / progress_bar.n) * (progress_bar.total - progress_bar.n)
progress_bar.set_postfix(remaining_time="{:.1f}s".format(remaining_time), refresh=False)

# Close progress bar
progress_bar.close()
