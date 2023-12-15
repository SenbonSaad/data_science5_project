import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def line_plot(df, x_axis, y_axis):
    # Set Seaborn style
    sns.set(style="whitegrid")
    # Create a line plot
    plt.figure(figsize=(10, 6))
    sns.lineplot(x=x_axis, y=y_axis, data=df, marker='o', color='b', label=y_axis)

    if x_axis in df.columns and not pd.api.types.is_datetime64_any_dtype(df[x_axis]):
        df[x_axis] = pd.to_datetime(df[x_axis])
    # Add labels
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title('Line Plot')
    plt.xticks(rotation=90)
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(10))
    # Show legend
    plt.legend()
    # Display the plot
    st.pyplot(plt)

def box_plot(df, y_column):
    # Set Seaborn style
    sns.set(style="whitegrid")

    # Create a box plot
    plt.figure(figsize=(10, 6))
    sns.boxplot(y=y_column, data=df)

    # Add labels
    plt.ylabel(y_column)
    plt.title('Box Plot Example')

    # Display the plot
    st.pyplot(plt)

def display_pie_chart(df, selected_column):
    value_counts = df[selected_column].value_counts()
    sns.set(style="whitegrid")

    plt.figure(figsize=(6, 6))
    plt.pie(value_counts, labels=value_counts.index, colors=sns.color_palette('pastel'), autopct='%1.1f%%')
    plt.title(f'Pie Chart for {selected_column}')
    st.pyplot(plt)

def heatmap(dataframe):
    numerical_columns = dataframe.select_dtypes(include=['number'])
    sns.set(style="whitegrid")

    plt.figure(figsize=(10, 8))
    sns.heatmap(numerical_columns.corr(), annot=True, cmap='coolwarm', linewidths=.5)
    plt.title('Correlation Heatmap for Numerical Columns')
    st.pyplot(plt)

def histogram(df, column):
    plt.figure(figsize=(8, 6))
    sns.histplot(df[column], kde=False, color='skyblue', bins=200) 
    plt.title(f'Histogram of {column}')
    plt.xlabel(column)
    plt.xticks(rotation=90)
    plt.ylabel('Frequency')
    st.pyplot(plt)

def kde_plot(df, column):
    plt.figure(figsize=(8, 6))
    sns.histplot(df[column], kde=True, color='skyblue', bins=200) 
    plt.title(f'KDE Plot of {column}')
    plt.xlabel(column)
    plt.xticks(rotation=90)
    plt.ylabel('Density')
    st.pyplot(plt)

def violin_plot(df, x_column, y_column=None, hue_column=None):
    plt.figure(figsize=(8, 6))

    if y_column is None:
        sns.violinplot(x=df[x_column], color='skyblue')
        plt.title(f'Violin Plot of {x_column}')
        plt.xlabel(x_column)
        plt.ylabel('Density')
    else:
        if hue_column is None:
            sns.violinplot(x=df[x_column], y=df[y_column], color='skyblue')
            plt.title(f'Violin Plot of {x_column} vs {y_column}')
            plt.xlabel(x_column)
            plt.ylabel(y_column)
        else:
            sns.violinplot(x=df[x_column], y=df[y_column], hue=df[hue_column], split=True, palette='Set1')
            plt.title(f'Violin Plot of {x_column} vs {y_column} (Hue: {hue_column})')
            plt.xlabel(x_column)
            plt.ylabel(y_column)

    st.pyplot(plt)

def data_proc(data_file):
    if data_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        # Excel file
        df = pd.read_excel(data_file)
    else:
        # CSV file
        df = pd.read_csv(data_file)

    # Display the original data
    st.header("Original Data")
    st.write(df)

    # Data processing options
    st.sidebar.header("Data Processor")
    data_processing_option = st.sidebar.selectbox("Choose a Data Processing Option", ["Original", "Describe", "Head", "Line Plot", "Scatter Plot", "Box Plot", "Histogram", "KDE Plot", "Violin Plot", "Bar Plot", "Heatmap", "Pie Chart"])

    if data_processing_option == "Describe":
        # Display the description of the data
        st.header("Data Description")
        st.write(df.describe())

    elif data_processing_option == "Head":
        # Display the first few rows of the data
        st.header("First Few Rows of Data")
        st.write(df.head())

    elif data_processing_option == "Line Plot":
        st.header("Line Plot")
        x_axis = st.selectbox("Select X-axis", df.columns)
        y_axis = st.selectbox("Select Y-axis", df.select_dtypes(include='number').columns)
        line_plot(df, x_axis, y_axis)

    elif data_processing_option == "Scatter Plot":
        # Scatter plot
        st.header("Scatter Plot")
        x_axis = st.selectbox("Select X-axis", df.columns)
        y_axis = st.selectbox("Select Y-axis", df.columns)
        st.scatter_chart(df[[x_axis, y_axis]])

    elif data_processing_option == "Box Plot":
        st.header("Box Plot")
        y_column = st.selectbox("Select a numeric column for Box Plot", df.select_dtypes(include='number').columns)

        # Call the box plot function
        box_plot(df, y_column)

    elif data_processing_option == "Histogram":
        # Histogram
        st.header("Histogram")
        selected_column = st.selectbox("Select a column for Histogram", df.columns)
        histogram(df, selected_column)

    elif data_processing_option == "KDE Plot":
        # KDE plot (Kernel Density Estimation)
        st.header("KDE Plot")
        selected_column = st.selectbox("Select a column for KDE Plot", df.columns)
        kde_plot(df, selected_column)

    elif data_processing_option == "Violin Plot":
        # Violin plot
        st.header("Violin Plot")
        x_axis = st.selectbox("Select X-axis", df.columns)
        available_columns = [None] + df.columns.tolist()

        y_axis = st.selectbox("Select Y-axis", available_columns)
        hue_column = st.selectbox("Select Hue", available_columns)

        if y_axis is None:
            st.text("Select Y-axis to customize the plot.")
        else:
            if x_axis not in df.columns:
                st.warning(f"Column '{x_axis}' not found in the DataFrame.")
            elif y_axis not in df.columns:
                st.warning(f"Column '{y_axis}' not found in the DataFrame.")
            elif hue_column is not None and hue_column not in df.columns:
                st.warning(f"Column '{hue_column}' not found in the DataFrame.")
            else:
                violin_plot(df, x_axis, y_axis, hue_column)

    elif data_processing_option == "Bar Plot":
        # Bar plot
        st.header("Bar Plot")
        x_axis = st.selectbox("Select X-axis", df.columns)
        y_axis = st.selectbox("Select Y-axis", df.columns)
        st.bar_chart(df[[x_axis, y_axis]])

    elif data_processing_option == "Heatmap":
        # Heatmap
        st.header("Heatmap")
        heatmap(df)

    elif data_processing_option == "Pie Chart":
        # Pie chart
        st.header("Pie Chart")
        valid_columns = [
            col for col in df.columns
            if (
                df[col].dtype not in ['float64', 'int64'] and
                not pd.api.types.is_datetime64_any_dtype(df[col]) and
                df[col].nunique() <= 20
            )
        ]

        if not valid_columns:
            st.warning("No suitable columns available for Pie Chart.")
        else:
            selected_column = st.selectbox("Select a column for Pie Chart", valid_columns)

            # Call the display_pie_chart function
            display_pie_chart(df, selected_column)