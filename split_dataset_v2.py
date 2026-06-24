import os
import shutil
import random

SOURCE_DIR = "dataset_v2"
OUTPUT_DIR = "dataset_v2_split"

CLASSES = ["real", "fake"]

TRAIN_RATIO = 0.8
VALID_RATIO = 0.1
TEST_RATIO = 0.1

random.seed(42)

for split in ["train", "valid", "test"]:
    for cls in CLASSES:
        os.makedirs(os.path.join(OUTPUT_DIR, split, cls), exist_ok=True)

for cls in CLASSES:
    class_dir = os.path.join(SOURCE_DIR, cls)

    images = [
        img for img in os.listdir(class_dir)
        if img.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ]

    random.shuffle(images)

    total = len(images)
    train_end = int(total * TRAIN_RATIO)
    valid_end = train_end + int(total * VALID_RATIO)

    train_images = images[:train_end]
    valid_images = images[train_end:valid_end]
    test_images = images[valid_end:]

    split_data = {
        "train": train_images,
        "valid": valid_images,
        "test": test_images
    }

    for split, split_images in split_data.items():
        for img in split_images:
            src = os.path.join(class_dir, img)
            dst = os.path.join(OUTPUT_DIR, split, cls, img)
            shutil.copy2(src, dst)

    print(f"{cls}: {total} images split completed")

print("\nDataset split completed successfully!")
print("Output folder:", OUTPUT_DIR)