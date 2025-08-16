def main():
    print("Hello from cortiscan!")


if __name__ == "__main__":
    main()


def normalize_image(images, labels):
    # Convert to float32
    images = images.astype(np.float32)
    # Normalize to [0,1]
    images /= 255.0
    # If grayscale, convert to RGB by repeating channels
    if images.ndim == 3 or images.shape[-1] == 1:
        images = np.repeat(images[..., np.newaxis], 3, axis=-1)
    return images, labels


train_dataset = train_dataset.map(normalize_image)
val_dataset = val_dataset.map(normalize_image)
