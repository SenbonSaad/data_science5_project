import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

def resize_image(image, new_width, new_height):
    return cv2.resize(image, (new_width, new_height))

def crop_image(image, top, left, bottom, right):
    return image[top:bottom, left:right]

def translate(img, x, y):
    transMat = np.float32([[1, 0, x], [0, 1, y]])
    dimensions = (img.shape[1], img.shape[0])
    return cv2.warpAffine(img, transMat, dimensions)

def rotate(img, angle, rotPoint=None):
    (height, width) = img.shape[:2]
    if rotPoint is None:
        rotPoint = (width//2, height//2)  # Default to the center of the image
    rotMat = cv2.getRotationMatrix2D(rotPoint, angle, 1.0)
    dimensions = (width, height)
    return cv2.warpAffine(img, rotMat, dimensions)

def plot_histogram(image):
    # Split the image into channels
    b, g, r = cv2.split(image)

    # Calculate histograms
    hist_b = cv2.calcHist([b], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([g], [0], None, [256], [0, 256])
    hist_r = cv2.calcHist([r], [0], None, [256], [0, 256])

    # Plot the histograms
    fig, ax = plt.subplots()
    ax.plot(hist_b, color='b', label='Blue')
    ax.plot(hist_g, color='g', label='Green')
    ax.plot(hist_r, color='r', label='Red')
    ax.set_title('RGB Histogram')
    ax.set_xlabel('Pixel Value')
    ax.set_ylabel('Frequency')
    ax.legend()
    # Display the Matplotlib figure in Streamlit
    st.pyplot(fig)

def apply_custom_filter(image, custom_kernel):
    # Apply the custom convolution kernel to the image
    filtered_image = cv2.filter2D(image, -1, custom_kernel)
    return filtered_image

def generate_random_kernel(size=3):
    # Generate a random convolution kernel of given size
    return np.random.randn(size, size)

def image_proc(image):
    if image is not None:
        # Read the image using OpenCV
        image = cv2.imdecode(np.frombuffer(image.read(), dtype=np.uint8), 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Additional image processing options
        st.header("Image Processing")
        processing_option = st.selectbox(
            "Choose an Image Processing Option", [
                "Original", "Grayscale", "Blur", "Edge Detection", "Clarify Edges", "Histogram","Custom Filter"
                ])

        if processing_option == "Original":
            # Convert to grayscale
            st.image(image, caption="Original Image", use_column_width=True)
        elif processing_option == "Grayscale":
            # Convert to grayscale
            st.image(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), caption=f"Grayscale Image", use_column_width=True)

        elif processing_option == "Blur":
            # Blur image
            st.image(cv2.GaussianBlur(image, (7, 7), cv2.BORDER_DEFAULT), caption=f"Blur Image", use_column_width=True)

        elif processing_option == "Edge Detection":
            # Edge detection
            st.image(cv2.Canny(image, 125, 175), caption=f"Edge Detection", use_column_width=True)

        elif processing_option == "Clarify Edges":
            # Edge clarification
            st.image(cv2.dilate(cv2.Canny(image, 125, 175), (7, 7), iterations=3), caption=f"Clarify Edges", use_column_width=True)

            # Plot RGB Histogram
        elif processing_option == "Histogram":
            plot_histogram(image)

        elif processing_option == "Custom Filter":
            # Custom filter option
            st.header("Convolution")
            st.write("Click the button below to apply a random convolution kernel:")
            if st.button("Generate"):
                # Generate a random convolution kernel
                custom_kernel = generate_random_kernel()
                custom_kernel = np.round(custom_kernel, decimals=2)
                
                st.subheader("Convolution Matrix")
                st.text(custom_kernel)
                
                # Apply the custom filter
                filtered_image = apply_custom_filter(image, custom_kernel)

                # Display the filtered image
                st.image(filtered_image, caption="Custom Filtered Image", use_column_width=True)

        # Image resizer options
        st.header("Image Resizer")
        original_shape = image.shape[:2]
        new_width = st.slider("New Width", 1, 1000, original_shape[1])
        new_height = st.slider("New Height", 1, 1000, original_shape[0])

        # Resize the image
        resized_image = resize_image(image, new_width, new_height)

        # Display the resized image
        st.image(resized_image, caption=f"Resized Image ({new_width}x{new_height})", use_column_width=True)

        # Crop options
        st.header("Image crop")
        top = st.slider("Top", 0, original_shape[0], 0)
        left = st.slider("Left", 0, original_shape[1], 0)
        bottom = st.slider("Bottom", 0, original_shape[0], original_shape[0])
        right = st.slider("Right", 0, original_shape[1], original_shape[1])

        # Crop the image
        processed_image = crop_image(image, top, left, bottom, right)
        st.image(processed_image, caption="Cropped Image", use_column_width=True)

        st.header("Image Translation")
        # Translation options
        translate_x = st.slider("Translate X", -100, 100, 0)
        translate_y = st.slider("Translate Y", -100, 100, 0)
        processed_image = translate(image, translate_x, translate_y)
        st.image(processed_image, caption=f"Translated Image (X={translate_x}, Y={translate_y})", use_column_width=True)

        st.header("Image Rotation")
        # Rotation options
        rotate_angle = st.slider("Rotate Angle (degrees)", -180, 180, 0)
        processed_image = rotate(image, rotate_angle)
        st.image(processed_image, caption=f"Rotated Image ({rotate_angle} degrees)", use_column_width=True)
