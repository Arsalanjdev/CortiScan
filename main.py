def main():
    print("Hello from cortiscan!")


if __name__ == "__main__":
    main()


train_dataset = train_dataset.map(normalize_image)
val_dataset = val_dataset.map(normalize_image)
