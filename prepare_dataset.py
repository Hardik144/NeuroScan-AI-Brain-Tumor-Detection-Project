import os
import glob
import h5py
import numpy as np
from PIL import Image

LABEL_NAMES = {
    1: 'Meningioma',
    2: 'Glioma',
    3: 'Pituitary'
}

def prepare(dataset_dirs=('dataset/bt_set1', 'dataset/bt_set2', 'dataset/bt_set3', 'dataset/bt_set4'),
            output_dir='Dataset'):
    images_dir = os.path.join(output_dir, 'bt_images')
    masks_dir = os.path.join(output_dir, 'bt_mask')
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(masks_dir, exist_ok=True)

    csv_path = os.path.join(output_dir, 'labels.csv')
    mat_files = []
    for d in dataset_dirs:
        if os.path.isdir(d):
            mat_files.extend(glob.glob(os.path.join(d, '*.mat')))

    mat_files.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]) if os.path.splitext(os.path.basename(x))[0].isdigit() else x)

    total = len(mat_files)
    print(f"Found {total} .mat files across dataset directories.")
    if total == 0:
        print("No .mat files found in dataset directories.")
        return

    with open(csv_path, 'w') as f_csv:
        f_csv.write("filename,pid,label,label_name\n")
        
        for idx, filepath in enumerate(mat_files, 1):
            base_name = os.path.splitext(os.path.basename(filepath))[0]
            try:
                with h5py.File(filepath, 'r') as f:
                    cjdata = f['cjdata']
                    label = int(cjdata['label'][0][0])
                    pid = "".join([chr(c[0]) for c in cjdata['PID']]) if 'PID' in cjdata else ""
                    raw_img = np.array(cjdata['image'], dtype=np.float32)
                    
                    # Normalize image to 0-255 uint8
                    img_min, img_max = raw_img.min(), raw_img.max()
                    if img_max > img_min:
                        norm_img = ((raw_img - img_min) / (img_max - img_min) * 255.0).astype(np.uint8)
                    else:
                        norm_img = np.zeros_like(raw_img, dtype=np.uint8)
                    
                    img = Image.fromarray(norm_img)
                    img.save(os.path.join(images_dir, f"{base_name}.jpg"))

                    if 'tumorMask' in cjdata:
                        raw_mask = np.array(cjdata['tumorMask'], dtype=np.uint8) * 255
                        mask = Image.fromarray(raw_mask)
                        mask.save(os.path.join(masks_dir, f"{base_name}_mask.jpg"))

                    f_csv.write(f"{base_name}.jpg,{pid},{label},{LABEL_NAMES.get(label, 'Unknown')}\n")
            except Exception as e:
                print(f"Error processing {filepath}: {e}")

            if idx % 500 == 0 or idx == total:
                print(f"Processed {idx}/{total} images...")

    print(f"\nDataset preparation complete!")
    print(f"Images saved to: {images_dir}")
    print(f"Masks saved to: {masks_dir}")
    print(f"Labels CSV saved to: {csv_path}")

if __name__ == '__main__':
    prepare()
