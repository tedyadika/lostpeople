import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow logging

import pandas as pd
from PIL import Image
from deepface import DeepFace

# Ensure the "photos" directory exists
if not os.path.exists("photos"):
    os.makedirs("photos")

# Path to your CSV file
csv_file = 'lost_persons.csv'
output_file = 'filtered_lost_persons.csv'
review_file = 'review_lost_persons.csv'
duplicates_file = 'duplicates_lost_persons.csv'

# Load existing data
def load_data(csv_file):
    if os.path.exists(csv_file):
        return pd.read_csv(csv_file)
    else:
        raise FileNotFoundError(f"{csv_file} not found.")

# Function to check if an image contains a human face
def is_human_face(image_path):
    try:
        analysis = DeepFace.analyze(img_path=image_path, actions=['gender'])
        return True
    except Exception as e:
        print(f"Error analyzing {image_path}: {e}")
        return False

# Function to check if two images are of the same person
def are_images_of_same_person(image_path1, image_path2):
    try:
        result = DeepFace.verify(img1_path=image_path1, img2_path=image_path2)
        return result['verified']
    except Exception as e:
        print(f"Error verifying images {image_path1} and {image_path2}: {e}")
        return False

# Process the data
def process_images(data):
    valid_data = []
    review_data = []
    duplicates_data = []

    seen_images = {}

    for i, row in data.iterrows():
        photo_path = row['Photo']
        if pd.notna(photo_path) and os.path.exists(photo_path):
            if is_human_face(photo_path):
                duplicate_found = False
                for seen_photo_path in seen_images.keys():
                    if are_images_of_same_person(photo_path, seen_photo_path):
                        duplicates_data.append(row)
                        duplicate_found = True
                        break
                if not duplicate_found:
                    valid_data.append(row)
                    seen_images[photo_path] = True
            else:
                review_data.append(row)
        else:
            review_data.append(row)

    valid_df = pd.DataFrame(valid_data)
    review_df = pd.DataFrame(review_data)
    duplicates_df = pd.DataFrame(duplicates_data)
    return valid_df, review_df, duplicates_df

# Main function
def main():
    # Load data
    data = load_data(csv_file)
    print(f"Loaded {len(data)} entries from {csv_file}")

    # Process images
    valid_df, review_df, duplicates_df = process_images(data)

    # Save valid, review, and duplicates data to CSV
    valid_df.to_csv(output_file, index=False)
    review_df.to_csv(review_file, index=False)
    duplicates_df.to_csv(duplicates_file, index=False)
    print(f"Saved {len(valid_df)} valid entries to {output_file}")
    print(f"Saved {len(review_df)} entries for review to {review_file}")
    print(f"Saved {len(duplicates_df)} duplicate entries to {duplicates_file}")

if __name__ == "__main__":
    main()
